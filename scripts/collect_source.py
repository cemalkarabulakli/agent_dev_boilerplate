from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.source_collector import SourceCollector  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect one research source in mock/api/scrape/manual mode.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--query")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    result = SourceCollector(ROOT).collect_source(args.source, args.query, args.limit)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
