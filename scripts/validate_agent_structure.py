from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.agent_loader import list_agents, load_agent_config
REQUIRED = ["agent.yaml", "system_prompt.md", "checklist.yaml", "knowledge/README.md", "memory/raw_history.jsonl", "memory/session_notes.md", "memory/long_term_memory.json", "memory/compacted_context.md", "outputs/README.md", "evals/eval_cases.yaml"]
WORKFLOWS = [".github/workflows/ci.yml", ".github/workflows/agent-quality-check.yml", ".github/workflows/scheduled-optimization.yml"]

def main() -> int:
    errors = []
    for workflow in WORKFLOWS:
        if not (ROOT / workflow).exists():
            errors.append(f"missing {workflow}")
    for agent in list_agents(ROOT, include_template=True):
        base = ROOT / "agents" / agent
        for rel in REQUIRED:
            if not (base / rel).exists():
                errors.append(f"{agent}: missing {rel}")
        try:
            config = load_agent_config(agent, ROOT)
            if agent != "_template" and config.name != agent:
                errors.append(f"{agent}: config name mismatch")
        except Exception as exc:
            errors.append(f"{agent}: {exc}")
    if errors:
        print("\n".join(errors))
        return 1
    print("Agent structure validation passed.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
