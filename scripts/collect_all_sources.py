from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.cross_source_analyzer import CrossSourceAnalyzer  # noqa: E402
from core.source_collector import SourceCollector  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect all enabled research sources.")
    parser.add_argument("--category", default="high_ticket_business")
    args = parser.parse_args()
    results = SourceCollector(ROOT).collect_all(args.category)
    report = CrossSourceAnalyzer(ROOT).write_report()
    print(f"Collected {len(results)} sources. Cross-source report: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
