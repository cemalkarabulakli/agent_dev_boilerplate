from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.checklist_runner import run_for_agent, run_for_all, write_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run global and per-agent checklists.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--agent", help="Agent name under agents/.")
    group.add_argument("--all", action="store_true", help="Run checklists for all non-template agents.")
    args = parser.parse_args()

    reports = run_for_all(ROOT) if args.all else [run_for_agent(args.agent, ROOT)]
    for report in reports:
        path = write_report(report, ROOT / "reports")
        print(f"{report.agent}: {'PASS' if report.passed else 'FAIL'} -> {path}")
    return 0 if all(report.passed for report in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
