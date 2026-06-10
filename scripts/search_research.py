"""
Search indexed research references using BM25 keyword ranking.

Usage:
    python scripts/search_research.py --query "avatar pain high ticket"
    python scripts/search_research.py --query "competitor pricing" --top 10
    python scripts/search_research.py --sync          # rebuild index only
    python scripts/search_research.py --stats         # show index stats
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.research_rag import ResearchIndex


def main() -> None:
    parser = argparse.ArgumentParser(description="Search collected research references")
    parser.add_argument("--query", "-q", help="Search query")
    parser.add_argument("--top", "-k", type=int, default=5, help="Max results (default 5)")
    parser.add_argument("--sync", action="store_true", help="Rebuild index and exit")
    parser.add_argument("--stats", action="store_true", help="Show index stats and exit")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output raw JSON")
    args = parser.parse_args()

    index = ResearchIndex(ROOT)

    if args.stats:
        s = index.stats()
        print(json.dumps(s, indent=2))
        return

    if args.sync:
        n = index.sync()
        print(f"[research_rag] synced {n} records into {index.db_path.relative_to(ROOT)}")
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    results = index.search(args.query, top_k=args.top)

    if args.as_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    if not results:
        print(f"[research_rag] no results for: {args.query!r}")
        return

    print(f"\n[research_rag] {len(results)} result(s) for: {args.query!r}\n")
    for i, ref in enumerate(results, 1):
        score = ref.get("_bm25_score", "n/a")
        title = ref.get("title") or ref.get("url") or ref.get("id")
        url = ref.get("url", "")
        source_type = ref.get("source_type", "")
        query_used = ref.get("query") or ref.get("query_or_input") or ""
        print(f"  {i}. [{score}] {title}")
        if url and not url.startswith("mock://"):
            print(f"     {url}")
        if source_type:
            print(f"     type={source_type}", end="")
        if query_used:
            print(f"  query={query_used!r}", end="")
        print()
    print()


if __name__ == "__main__":
    main()
