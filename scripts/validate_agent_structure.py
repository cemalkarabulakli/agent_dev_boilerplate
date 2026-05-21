from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.agent_loader import agent_dir, list_agents, load_agent_config  # noqa: E402


REQUIRED_AGENT_PATHS = [
    "agent.yaml",
    "system_prompt.md",
    "checklist.yaml",
    "knowledge",
    "knowledge/sources.yaml",
    "knowledge/raw",
    "knowledge/processed",
    "memory",
    "memory/raw_history.jsonl",
    "memory/long_term_memory.json",
    "memory/session_notes.md",
    "memory/compacted_context.md",
    "tools",
    "evals",
    "evals/eval_cases.yaml",
    "outputs",
]

REQUIRED_WORKFLOWS = [
    ".github/workflows/ci.yml",
    ".github/workflows/agent-quality-check.yml",
    ".github/workflows/scheduled-optimization.yml",
]


def validate_agent(agent_name: str, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    base = agent_dir(agent_name, root)
    for relative in REQUIRED_AGENT_PATHS:
        if not (base / relative).exists():
            errors.append(f"{agent_name}: missing {relative}")
    try:
        config = load_agent_config(agent_name, root)
        if config.name != agent_name and agent_name != "_template":
            errors.append(f"{agent_name}: config name {config.name!r} does not match folder")
    except Exception as exc:  # noqa: BLE001 - return validation error.
        errors.append(f"{agent_name}: invalid agent.yaml: {exc}")
    return errors


def main() -> int:
    errors: list[str] = []
    for workflow in REQUIRED_WORKFLOWS:
        if not (ROOT / workflow).exists():
            errors.append(f"missing {workflow}")
    for agent_name in list_agents(ROOT, include_template=True):
        errors.extend(validate_agent(agent_name, ROOT))
    if errors:
        print("Agent structure validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Agent structure validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
