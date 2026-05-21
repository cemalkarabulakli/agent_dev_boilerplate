from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import argparse
from core.agent_loader import list_agents
from core.checklist_runner import run_for_agent, run_named_checklist, write_report

def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--agent")
    group.add_argument("--all", action="store_true")
    group.add_argument("--checklist")
    args = parser.parse_args()
    if args.checklist:
        report = run_named_checklist(args.checklist, ROOT)
        print(f"{args.checklist}: {'PASS' if report.passed else 'FAIL'} -> {write_report(report, ROOT / 'outputs' / 'quality_reports')}")
        return 0 if report.passed else 1
    agents = list_agents(ROOT) if args.all else [args.agent]
    reports = [run_for_agent(agent, ROOT) for agent in agents]
    for report in reports:
        print(f"{report.agent}: {'PASS' if report.passed else 'FAIL'} -> {write_report(report, ROOT / 'outputs' / 'quality_reports')}")
    return 0 if all(report.passed for report in reports) else 1

if __name__ == "__main__":
    raise SystemExit(main())
