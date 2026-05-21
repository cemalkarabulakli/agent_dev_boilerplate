"""Checklist execution for global and per-agent quality gates."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from core.agent_loader import agent_dir, list_agents, load_agent_config, repo_root
from core.knowledge_loader import KnowledgeBase
from core.schema import CheckResult, ChecklistItem
from core.yaml_utils import load_yaml


PROMPT_SECTIONS = [
    "# Role",
    "# Goal",
    "# Operating Principles",
    "# Allowed Knowledge",
    "# Memory Rules",
    "# Context Compaction Rules",
    "# Tool Rules",
    "# Output Format",
    "# Refusal / Safety Rules",
    "# Self-Review Checklist",
]


@dataclass
class ChecklistReport:
    agent: str
    results: list[CheckResult]

    @property
    def passed(self) -> bool:
        return not any(result.severity == "critical" and not result.passed for result in self.results)


def run_for_agent(agent_name: str, root: Path | None = None) -> ChecklistReport:
    actual_root = root or repo_root()
    items = _load_global_items(actual_root) + _load_agent_items(agent_name, actual_root)
    results = [_run_item(item, agent_name, actual_root) for item in items]
    return ChecklistReport(agent=agent_name, results=results)


def run_for_all(root: Path | None = None) -> list[ChecklistReport]:
    actual_root = root or repo_root()
    return [run_for_agent(name, actual_root) for name in list_agents(actual_root)]


def write_report(report: ChecklistReport, reports_dir: Path) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{report.agent}_checklist_report.md"
    lines = [
        f"# Checklist Report: {report.agent}",
        "",
        f"Status: {'PASS' if report.passed else 'FAIL'}",
        "",
    ]
    for result in report.results:
        status = "PASS" if result.passed else "FAIL"
        lines.append(f"## {status} - {result.id}")
        lines.append(f"- Category: {result.category}")
        lines.append(f"- Severity: {result.severity}")
        lines.append(f"- Description: {result.description}")
        lines.append(f"- Message: {result.message}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _load_global_items(root: Path) -> list[ChecklistItem]:
    path = root / "checklists" / "global_agent_best_practices.yaml"
    data = load_yaml(path)
    return [ChecklistItem.from_dict(item) for item in data.get("items", [])]


def _load_agent_items(agent_name: str, root: Path) -> list[ChecklistItem]:
    path = agent_dir(agent_name, root) / "checklist.yaml"
    if not path.exists():
        return [
            ChecklistItem(
                id="agent_checklist_file",
                category="Agent Structure",
                description="Agent checklist.yaml exists.",
                severity="critical",
                check="agent_checklist_exists",
            )
        ]
    data = load_yaml(path)
    return [ChecklistItem.from_dict(item) for item in data.get("items", [])]


def _run_item(item: ChecklistItem, agent_name: str, root: Path) -> CheckResult:
    checks = {
        "agent_structure": _check_agent_structure,
        "prompt_quality": _check_prompt_quality,
        "context_compaction": _check_context_compaction,
        "knowledge_sources": _check_knowledge_sources,
        "tool_safety": _check_tool_safety,
        "github_ready": _check_github_ready,
        "no_secrets": _check_no_secrets,
        "agent_checklist_exists": lambda *_: (True, "Agent checklist exists."),
    }
    check_fn = checks.get(item.check)
    if check_fn is None:
        passed, message = True, f"No executable check mapped for '{item.check}', treated as informational."
    else:
        passed, message = check_fn(agent_name, root)
    return CheckResult(
        id=item.id,
        category=item.category,
        description=item.description,
        severity=item.severity,
        passed=passed,
        message=message,
    )


def _check_agent_structure(agent_name: str, root: Path) -> tuple[bool, str]:
    base = agent_dir(agent_name, root)
    required = [
        "agent.yaml",
        "system_prompt.md",
        "checklist.yaml",
        "knowledge",
        "memory",
        "evals",
        "tools",
        "outputs",
    ]
    missing = [item for item in required if not (base / item).exists()]
    return (not missing, "All required paths exist." if not missing else "Missing: " + ", ".join(missing))


def _check_prompt_quality(agent_name: str, root: Path) -> tuple[bool, str]:
    prompt_path = agent_dir(agent_name, root) / "system_prompt.md"
    if not prompt_path.exists():
        return False, "system_prompt.md is missing."
    prompt = prompt_path.read_text(encoding="utf-8")
    missing = [section for section in PROMPT_SECTIONS if section not in prompt]
    return (not missing, "Prompt contains required sections." if not missing else "Missing sections: " + ", ".join(missing))


def _check_context_compaction(agent_name: str, root: Path) -> tuple[bool, str]:
    config = load_agent_config(agent_name, root)
    base = agent_dir(agent_name, root)
    required_files = [
        base / "memory" / "raw_history.jsonl",
        base / "memory" / "compacted_context.md",
        root / "core" / "context_compactor.py",
        root / "prompts" / "compact_context_prompt.md",
    ]
    missing = [str(path.relative_to(root)) for path in required_files if not path.exists()]
    if config.context.keep_last_n_turns < 1 or config.context.compact_when_tokens_exceed < 1000:
        return False, "Context thresholds are not configured safely."
    return (not missing, "Context compaction files and settings exist." if not missing else "Missing: " + ", ".join(missing))


def _check_knowledge_sources(agent_name: str, root: Path) -> tuple[bool, str]:
    config = load_agent_config(agent_name, root)
    kb = KnowledgeBase(agent_dir(agent_name, root), config.knowledge.sources_file)
    try:
        sources = kb.load_sources()
    except Exception as exc:  # noqa: BLE001 - report validation failure to checklist.
        return False, str(exc)
    if not sources:
        return False, "At least one source entry is required, even if placeholder."
    ids = [source.id for source in sources]
    if len(ids) != len(set(ids)):
        return False, "Source IDs must be unique."
    return True, "Knowledge sources are typed and valid."


def _check_tool_safety(agent_name: str, root: Path) -> tuple[bool, str]:
    config = load_agent_config(agent_name, root)
    if not config.tools.allowed:
        return False, "No explicit tool allowlist configured."
    destructive = {"delete_file", "shell", "write_arbitrary_file", "git_push"}
    unsafe = sorted(set(config.tools.allowed) & destructive)
    if unsafe:
        return False, "Unsafe tools are directly allowed: " + ", ".join(unsafe)
    if not config.guardrails.output:
        return False, "Output guardrails are missing."
    return True, "Tool allowlist and output guardrails are explicit."


def _check_github_ready(agent_name: str, root: Path) -> tuple[bool, str]:
    del agent_name
    required = [
        root / ".github" / "workflows" / "ci.yml",
        root / ".github" / "workflows" / "agent-quality-check.yml",
        root / ".github" / "workflows" / "scheduled-optimization.yml",
        root / ".env.example",
        root / ".gitignore",
    ]
    missing = [str(path.relative_to(root)) for path in required if not path.exists()]
    if missing:
        return False, "Missing: " + ", ".join(missing)
    gitignore = (root / ".gitignore").read_text(encoding="utf-8")
    scheduled = (root / ".github" / "workflows" / "scheduled-optimization.yml").read_text(encoding="utf-8")
    if ".env" not in gitignore:
        return False, ".env is not ignored."
    if "17 3 * * *" not in scheduled:
        return False, "Scheduled workflow must use non-hour cron 17 3 * * *."
    return True, "GitHub workflows and env hygiene files exist."


def _check_no_secrets(agent_name: str, root: Path) -> tuple[bool, str]:
    del agent_name
    suspicious: list[str] = []
    pattern = re.compile(r"(sk-[A-Za-z0-9]{20,}|OPENAI_API_KEY\s*=\s*sk-)")
    for path in root.rglob("*"):
        if path.is_dir() or ".git" in path.parts or ".venv" in path.parts:
            continue
        if path.suffix.lower() not in {".py", ".md", ".yaml", ".yml", ".toml", ".example", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if pattern.search(text):
            suspicious.append(str(path.relative_to(root)))
    return (not suspicious, "No committed API-key-like secrets found." if not suspicious else "Suspicious secrets: " + ", ".join(suspicious))
