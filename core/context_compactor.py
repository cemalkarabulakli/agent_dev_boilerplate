"""Deterministic context compaction with validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.schema import AgentConfig, MemoryEntry, ValidationReport


REQUIRED_SECTIONS = [
    "# Compacted Context",
    "## Current Goal",
    "## Agent Role",
    "## Durable Facts",
    "## User / Project Constraints",
    "## Decisions Made",
    "## Open Tasks",
    "## Important Source References",
    "## Recent Verbatim Turns",
    "## Do Not Forget",
    "## Removed Noise",
    "## Validation Checklist",
]

MUST_KEEP_PATTERNS = [
    r"\bgoal\b",
    r"\brole\b",
    r"\bconstraint\b",
    r"\bprefer",
    r"\bdeadline\b",
    r"\bdue\b",
    r"\bdecision\b",
    r"\bselected\b",
    r"\brejected\b",
    r"\bopen question\b",
    r"\bunresolved\b",
    r"\btask\b",
    r"\btodo\b",
    r"\bsource\b",
    r"https?://",
    r"\bassumption\b",
    r"\brisk\b",
    r"\bwarning\b",
    r"\bmust\b",
    r"\brequire",
    r"\bdo not\b",
    r"\bno fake\b",
    r"\b\d+([.,:]\d+)?(%|k|K|m|M)?\b",
]

NOISE_EXACT = {
    "hi",
    "hello",
    "hey",
    "thanks",
    "thank you",
    "ok",
    "okay",
    "great",
    "sounds good",
    "sure",
}


@dataclass
class CompactionResult:
    markdown: str
    validation: ValidationReport
    recent_user_turns: list[str]
    durable_facts: list[str]
    removed_noise_count: int


def compact_context(
    config: AgentConfig,
    history: list[dict[str, Any]],
    session_notes: str = "",
    long_term_memory: list[MemoryEntry] | None = None,
) -> CompactionResult:
    recent_user_turns = _recent_user_turns(history, config.context.keep_last_n_turns)
    facts, removed_noise_count = _extract_durable_facts(history, config.context.tool_output_trim_chars)

    accepted_memories = [
        f"[memory:{entry.type}] {entry.text}"
        for entry in (long_term_memory or [])
        if entry.status == "accepted"
    ]
    durable_facts = _dedupe(facts + accepted_memories)

    current_goal = _first_matching(durable_facts, ["goal", "task", "must", "require"]) or "Not specified yet."
    constraints = _filter_matching(durable_facts, ["constraint", "prefer", "must", "require", "do not", "no fake"])
    decisions = _filter_matching(durable_facts, ["decision", "selected", "rejected"])
    open_tasks = _filter_matching(durable_facts, ["open question", "unresolved", "task", "todo"])
    source_refs = _filter_matching(durable_facts, ["source", "http://", "https://", "citation"])
    do_not_forget = _dedupe(
        [item for item in durable_facts if item not in constraints + decisions + open_tasks + source_refs]
    )

    markdown = _render_markdown(
        config=config,
        current_goal=current_goal,
        durable_facts=durable_facts,
        constraints=constraints,
        decisions=decisions,
        open_tasks=open_tasks,
        source_refs=source_refs,
        recent_user_turns=recent_user_turns,
        do_not_forget=do_not_forget,
        removed_noise_count=removed_noise_count,
        session_notes=session_notes,
    )
    validation = validate_compacted_context(markdown, history, recent_user_turns, durable_facts)
    return CompactionResult(
        markdown=markdown,
        validation=validation,
        recent_user_turns=recent_user_turns,
        durable_facts=durable_facts,
        removed_noise_count=removed_noise_count,
    )


def write_validation_report(result: CompactionResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Context Compaction Validation",
        "",
        f"Status: {'PASS' if result.validation.passed else 'FAIL'}",
        "",
        "## Errors",
    ]
    lines.extend([f"- {error}" for error in result.validation.errors] or ["- None"])
    lines.append("")
    lines.append("## Warnings")
    lines.extend([f"- {warning}" for warning in result.validation.warnings] or ["- None"])
    lines.append("")
    lines.append("## Details")
    for key, value in result.validation.details.items():
        lines.append(f"- {key}: {value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_compacted_context(
    markdown: str,
    history: list[dict[str, Any]],
    recent_user_turns: list[str],
    durable_facts: list[str],
) -> ValidationReport:
    report = ValidationReport(passed=True)
    for section in REQUIRED_SECTIONS:
        if section not in markdown:
            report.fail(f"Missing required section: {section}")

    for turn in recent_user_turns:
        if turn not in markdown:
            report.fail("Recent user turn was not preserved verbatim")

    source_text = "\n".join(str(item.get("content", "")) for item in history)
    for literal in _important_literals(source_text):
        if literal in source_text and literal not in markdown:
            report.fail(f"Important literal was not preserved: {literal}")

    for fact in durable_facts:
        normalized = _strip_fact_prefix(fact)
        if normalized and normalized not in source_text and not fact.startswith("[memory:"):
            report.fail(f"Potential invented fact not found in source history: {fact}")

    report.details.update(
        {
            "recent_user_turns": len(recent_user_turns),
            "durable_facts": len(durable_facts),
            "important_literals": len(_important_literals(source_text)),
        }
    )
    return report


def _recent_user_turns(history: list[dict[str, Any]], keep_last_n_turns: int) -> list[str]:
    turns = [str(item.get("content", "")) for item in history if item.get("role") == "user"]
    return turns[-keep_last_n_turns:]


def _extract_durable_facts(history: list[dict[str, Any]], trim_chars: int) -> tuple[list[str], int]:
    facts: list[str] = []
    removed_noise_count = 0
    for item in history:
        role = str(item.get("role", "unknown"))
        content = str(item.get("content", "")).strip()
        if not content:
            continue
        if _is_noise(content):
            removed_noise_count += 1
            continue
        if role == "tool" and len(content) > trim_chars:
            content = content[:trim_chars] + " [trimmed]"
        for candidate in _split_candidates(content):
            if _is_noise(candidate):
                removed_noise_count += 1
                continue
            if _must_keep(candidate):
                facts.append(f"[{role}] {candidate}")
    return _dedupe(facts), removed_noise_count


def _split_candidates(content: str) -> list[str]:
    lines = [line.strip("- ").strip() for line in content.splitlines() if line.strip()]
    if len(lines) > 1:
        return lines
    parts = re.split(r"(?<=[.!?])\s+", content)
    return [part.strip() for part in parts if part.strip()]


def _must_keep(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in MUST_KEEP_PATTERNS)


def _is_noise(text: str) -> bool:
    lowered = re.sub(r"\s+", " ", text.strip().lower())
    return lowered in NOISE_EXACT or len(lowered) <= 2


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = re.sub(r"\s+", " ", item).strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(item)
    return result


def _first_matching(items: list[str], terms: list[str]) -> str | None:
    matches = _filter_matching(items, terms)
    return matches[0] if matches else None


def _filter_matching(items: list[str], terms: list[str]) -> list[str]:
    lowered_terms = [term.lower() for term in terms]
    return [item for item in items if any(term in item.lower() for term in lowered_terms)]


def _render_markdown(
    config: AgentConfig,
    current_goal: str,
    durable_facts: list[str],
    constraints: list[str],
    decisions: list[str],
    open_tasks: list[str],
    source_refs: list[str],
    recent_user_turns: list[str],
    do_not_forget: list[str],
    removed_noise_count: int,
    session_notes: str,
) -> str:
    lines: list[str] = [
        "# Compacted Context",
        "",
        "## Current Goal",
        current_goal,
        "",
        "## Agent Role",
        config.role,
        "",
        "## Durable Facts",
    ]
    lines.extend(_bullets(durable_facts))
    lines.extend(["", "## User / Project Constraints"])
    lines.extend(_bullets(constraints))
    lines.extend(["", "## Decisions Made"])
    if decisions:
        for decision in decisions:
            lines.extend(["- Decision:", f"  {decision}", "  Rationale: Captured from conversation.", "  Date/Session: Unknown"])
    else:
        lines.append("- None captured.")
    lines.extend(["", "## Open Tasks"])
    lines.extend(_bullets(open_tasks))
    lines.extend(["", "## Important Source References"])
    lines.extend(_bullets(source_refs))
    lines.extend(["", "## Recent Verbatim Turns"])
    if recent_user_turns:
        for turn in recent_user_turns:
            lines.extend(["```text", turn, "```"])
    else:
        lines.append("No recent user turns.")
    lines.extend(["", "## Do Not Forget"])
    lines.extend(_bullets(do_not_forget))
    if session_notes.strip():
        lines.append(f"- Session notes exist and should be reviewed before final answers.")
    lines.extend(
        [
            "",
            "## Removed Noise",
            f"Removed greetings, duplicate confirmations, and low-signal fragments. Noise fragments removed: {removed_noise_count}.",
            "",
            "## Validation Checklist",
            "- Must-keep fields are represented.",
            "- Numbers, names, dates, and decisions from extracted facts are preserved.",
            "- Source references from extracted facts are preserved.",
            "- Recent user turns are preserved verbatim.",
            "- Raw history remains outside compacted context.",
            "- The deterministic compactor only uses source history, accepted memory, and fixed section labels.",
        ]
    )
    return "\n".join(lines) + "\n"


def _bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] if items else ["- None captured."]


def _important_literals(text: str) -> list[str]:
    literals = set(re.findall(r"https?://[^\s)]+", text))
    literals.update(re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text))
    literals.update(re.findall(r"\b\d+(?:[.,:]\d+)?(?:%|k|K|m|M)?\b", text))
    return sorted(literals)


def _strip_fact_prefix(fact: str) -> str:
    return re.sub(r"^\[[^\]]+\]\s*", "", fact).strip()
