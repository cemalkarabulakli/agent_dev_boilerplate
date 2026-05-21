from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.competitor_monitor import CompetitorMonitor  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Monitor competitor websites in mock-safe mode by default.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--screenshots", action="store_true")
    args = parser.parse_args()
    result = CompetitorMonitor(ROOT).monitor(args.query, screenshots=args.screenshots)
    print(result["output_report_file"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

