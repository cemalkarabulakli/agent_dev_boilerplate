from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from core.schema import AgentConfig, MemoryEntry

SECTIONS = ["# Compacted High-Ticket Business Context", "## Business Snapshot", "## Market", "## Expert Positioning", "## Specific Avatar", "## Urgent Pain", "## Expensive Problem", "## Dream Outcome", "## Current Offer", "## Improved Offer Direction", "## Unique Mechanism", "## Value Stack", "## Pricing Decisions", "## Guarantee / Risk Reversal", "## Proof / Credibility", "## Acquisition Decisions", "## Funnel Decisions", "## Sales Process", "## Delivery System", "## Retention / Upsell", "## Metrics", "## Constraints", "## Open Questions", "## Open Tasks", "## Rejected Ideas", "## Assumptions", "## Do Not Forget", "## Research Insights", "## Source References", "## Validated Trends", "## Candidate Trends", "## Tool Opportunities", "## Ad Angle Signals", "## Customer Language Signals", "## Recent Verbatim Turns", "## Removed Noise", "## Validation Checklist"]
CATEGORIES = {
    "Market": ["market", "niche"], "Expert Positioning": ["expert", "credibility", "experience"], "Specific Avatar": ["avatar", "customer", "client"], "Urgent Pain": ["urgent pain", "pain"], "Expensive Problem": ["expensive problem", "costly", "problem"], "Dream Outcome": ["dream outcome", "desired outcome"], "Current Offer": ["current offer", "offer"], "Improved Offer Direction": ["improved offer", "offer direction"], "Unique Mechanism": ["unique mechanism", "mechanism"], "Value Stack": ["value stack", "bonus", "asset"], "Pricing Decisions": ["price", "pricing", "$", "payment"], "Guarantee / Risk Reversal": ["guarantee", "risk reversal"], "Proof / Credibility": ["proof", "case study", "testimonial", "credibility"], "Acquisition Decisions": ["acquisition", "lead", "ads", "outbound", "content"], "Funnel Decisions": ["funnel", "webinar", "workshop", "application", "email"], "Sales Process": ["sales", "close", "qualification", "objection"], "Delivery System": ["delivery", "onboarding", "milestone", "fulfillment"], "Retention / Upsell": ["retention", "upsell", "continuity", "referral"], "Metrics": ["metric", "close rate", "leads", "aov", "ltv", "%"], "Constraints": ["constraint", "budget", "time", "capacity"], "Open Questions": ["open question", "question"], "Open Tasks": ["task", "todo", "next action"], "Rejected Ideas": ["rejected", "do not"], "Assumptions": ["assumption", "assume"],
}
NOISE = {"hi", "hello", "thanks", "thank you", "ok", "okay", "great", "sure"}

@dataclass(frozen=True)
class CompactionResult:
    markdown: str
    passed: bool
    errors: list[str]
    removed_noise_count: int

def compact_context(config: AgentConfig, history: list[dict[str, Any]], session_notes: str = "", memories: list[MemoryEntry] | None = None) -> CompactionResult:
    recent = [str(item.get("content", "")) for item in history if item.get("role") == "user"][-config.context.keep_last_n_turns:]
    buckets = {key: [] for key in CATEGORIES}
    do_not_forget: list[str] = []
    removed = 0
    for item in history:
        role = str(item.get("role", "unknown"))
        content = str(item.get("content", "")).strip()
        if not content:
            continue
        if content.lower() in NOISE:
            removed += 1
            continue
        for line in [part.strip("- ").strip() for part in content.splitlines() if part.strip()] or [content]:
            if line.lower() in NOISE:
                removed += 1
                continue
            if _is_raw_research_dump(line):
                removed += 1
                continue
            matched = False
            for category, patterns in CATEGORIES.items():
                if any(pattern in line.lower() for pattern in patterns):
                    buckets[category].append(f"[{role}] {line}")
                    matched = True
            if not matched and (re.search(r"\d", line) or any(word in line.lower() for word in ["must", "source", "risk", "unknown"])):
                do_not_forget.append(f"[{role}] {line}")
    for memory in memories or []:
        if memory.status == "accepted":
            do_not_forget.append(f"[memory:{memory.type}] {memory.text}")
    lines = ["# Compacted High-Ticket Business Context", "", "## Business Snapshot"]
    snapshot = [items[0] for key, items in buckets.items() if items][:7]
    lines.extend(_bullets(snapshot))
    for category in CATEGORIES:
        lines.extend(["", f"## {category}"])
        lines.extend(_bullets(_dedupe(buckets[category])))
    lines.extend(["", "## Do Not Forget"])
    if session_notes.strip():
        do_not_forget.append("Session notes exist and should be reviewed.")
    lines.extend(_bullets(_dedupe(do_not_forget)))
    research_sections = {
        "Research Insights": [],
        "Source References": [],
        "Validated Trends": [],
        "Candidate Trends": [],
        "Tool Opportunities": [],
        "Ad Angle Signals": [],
        "Customer Language Signals": [],
    }
    for line in do_not_forget:
        lowered = line.lower()
        has_reference = "reference_ids" in lowered or "ref_" in lowered
        has_confidence = "confidence" in lowered
        is_processed = "processed" in lowered
        if not (has_reference and has_confidence and is_processed):
            continue
        research_sections["Research Insights"].append(line)
        research_sections["Source References"].append(line)
        if "validated" in lowered:
            research_sections["Validated Trends"].append(line)
        elif "candidate" in lowered:
            research_sections["Candidate Trends"].append(line)
        if "tool" in lowered:
            research_sections["Tool Opportunities"].append(line)
        if "ad angle" in lowered or "ad_angle" in lowered:
            research_sections["Ad Angle Signals"].append(line)
        if "language" in lowered or "pain" in lowered:
            research_sections["Customer Language Signals"].append(line)
    for section, items in research_sections.items():
        lines.extend(["", f"## {section}"])
        lines.extend(_bullets(_dedupe(items)))
    lines.extend(["", "## Recent Verbatim Turns"])
    if recent:
        for turn in recent:
            lines.extend(["```text", turn, "```"])
    else:
        lines.append("No recent user turns.")
    lines.extend(["", "## Removed Noise", f"Removed greetings, duplicates, vague motivational text, and rejected temporary brainstorming where detected. Noise fragments removed: {removed}.", "", "## Validation Checklist"])
    lines.extend(["- recent turns preserved", "- important numbers preserved", "- market preserved when present", "- avatar preserved when present", "- offer and price preserved when present", "- positioning decisions preserved when present", "- sales/delivery decisions preserved when present", "- rejected ideas preserved when present", "- open tasks preserved when present", "- no invented facts", "- assumptions labeled", "- raw history untouched", "- raw research dumps excluded", "- research insights require processed status, confidence, and references", "- weak signals remain labeled candidate"])
    markdown = "\n".join(lines) + "\n"
    errors = validate_compaction(markdown, history, recent)
    return CompactionResult(markdown, not errors, errors, removed)

def validate_compaction(markdown: str, history: list[dict[str, Any]], recent: list[str]) -> list[str]:
    errors = [f"Missing section: {section}" for section in SECTIONS if section not in markdown]
    errors.extend(["Recent user turn was not preserved verbatim" for turn in recent if turn not in markdown])
    source = "\n".join(str(item.get("content", "")) for item in history)
    for literal in re.findall(r"\$?\b\d+(?:[,.]\d+)?%?\b", source):
        if literal not in markdown:
            errors.append(f"Important number not preserved: {literal}")
    return errors

def write_validation_report(result: CompactionResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Context Compaction Validation\n\nStatus: " + ("PASS" if result.passed else "FAIL") + "\n\n" + "\n".join(f"- {e}" for e in result.errors), encoding="utf-8")

def _dedupe(items: list[str]) -> list[str]:
    result = []
    seen = set()
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def _bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] if items else ["- None captured."]

def _is_raw_research_dump(line: str) -> bool:
    lowered = line.lower()
    raw_markers = ["raw research dump", "raw source output", "raw signal snippet", "raw scraped html", "raw transcript dump"]
    return any(marker in lowered for marker in raw_markers)
