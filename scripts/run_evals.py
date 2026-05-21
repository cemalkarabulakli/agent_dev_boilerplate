from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.agent_loader import list_agents  # noqa: E402
from core.eval_runner import run_evals, write_eval_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic agent evals.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--agent", help="Agent name under agents/.")
    group.add_argument("--all", action="store_true", help="Run evals for all non-template agents.")
    args = parser.parse_args()

    names = list_agents(ROOT) if args.all else [args.agent]
    reports = [run_evals(name, ROOT) for name in names]
    for report in reports:
        path = write_eval_report(report, ROOT / "reports")
        print(f"{report.agent}: {'PASS' if report.passed else 'FAIL'} -> {path}")
    return 0 if all(report.passed for report in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
