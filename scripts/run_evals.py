from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import argparse
from core.agent_loader import list_agents
from core.business_context_schema import BusinessContext
from core.output_templates import render_mock_output
from core.schema import EvalCase, load_yaml

def run(agent: str) -> bool:
    output = render_mock_output(agent, BusinessContext.load(ROOT / "business_context.yaml"))
    cases = [EvalCase.from_dict(item) for item in load_yaml(ROOT / "agents" / agent / "evals" / "eval_cases.yaml").get("cases", [])]
    passed = True
    for case in cases:
        missing = [section for section in case.required_sections if section not in output]
        forbidden = [term for term in case.forbidden_terms if term.lower() in output.lower()]
        if missing or forbidden:
            passed = False
            print(f"{agent}:{case.id} FAIL missing={missing} forbidden={forbidden}")
    if passed:
        print(f"{agent}: PASS")
    return passed

def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--agent")
    group.add_argument("--all", action="store_true")
    args = parser.parse_args()
    agents = list_agents(ROOT) if args.all else [args.agent]
    return 0 if all(run(agent) for agent in agents) else 1
if __name__ == "__main__":
    raise SystemExit(main())
