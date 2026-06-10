"""
Run a semantic search using Exa or mock provider.

Usage:
    python scripts/run_semantic_search.py --query "high ticket consulting offer examples"
    python scripts/run_semantic_search.py --query "AI automation agency case studies" --provider exa
    python scripts/run_semantic_search.py --query "RAG source discovery" --mode rag
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass
sys.path.insert(0, str(ROOT))

from core.web.result_normalizer import normalize_search_result
from core.web.quality_scorer import score_result
from core.web.reference_builder import build_and_save_references


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _mock_results(query: str) -> list[dict]:
    return [
        {
            "title": f"Semantic result {i + 1}: {query[:40]}",
            "url": f"mock://semantic-search/{urllib.parse.quote(query[:40])}/{i + 1}",
            "snippet": f"Semantically relevant mock result {i + 1}. Set EXA_API_KEY and WEB_TOOLS_MODE=live for real semantic search.",
            "source": "mock_semantic",
            "score": round(0.97 - i * 0.07, 2),
            "isMock": True,
            "metadata": {"query": query, "provider": "mock_semantic", "semantic_score": round(0.97 - i * 0.07, 2)},
        }
        for i in range(5)
    ]


def _exa_search(query: str, api_key: str, max_results: int = 10, mode: str = "search") -> list[dict]:
    body = json.dumps({
        "query": query,
        "numResults": max_results,
        "useAutoprompt": True,
        "contents": {"text": True},
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.exa.ai/search",
        data=body,
        headers={"x-api-key": api_key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return data.get("results") or []


def _run_semantic_search(query: str, provider: str, max_results: int, mode: str) -> tuple[list[dict], str, list[str]]:
    web_mode = os.environ.get("WEB_TOOLS_MODE", "mock")
    warnings: list[str] = []

    if provider == "mock" or web_mode == "mock":
        return _mock_results(query), "mock_semantic", []

    if provider == "exa":
        api_key = os.environ.get("EXA_API_KEY", "")
        if not api_key:
            warnings.append("EXA_API_KEY not set — falling back to mock semantic search")
            return _mock_results(query), "mock_semantic", warnings
        try:
            return _exa_search(query, api_key, max_results, mode), "exa", warnings
        except Exception as exc:
            warnings.append(f"Exa search failed ({exc}) — falling back to mock")
            return _mock_results(query), "mock_semantic", warnings

    warnings.append(f"Unknown provider '{provider}' — using mock")
    return _mock_results(query), "mock_semantic", warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a semantic/RAG search using Exa")
    parser.add_argument("--query", required=True, help="Semantic search query")
    parser.add_argument("--provider", default=os.environ.get("DEFAULT_SEMANTIC_SEARCH_PROVIDER", "exa"),
                        choices=["exa", "mock"])
    parser.add_argument("--mode", default="search", choices=["search", "rag", "similar"],
                        help="search=general, rag=include full text for RAG, similar=find similar pages")
    parser.add_argument("--max-results", type=int, default=int(os.environ.get("SEARCH_MAX_RESULTS", 10)))
    args = parser.parse_args()

    raw_results, actual_provider, warnings = _run_semantic_search(
        args.query, args.provider, args.max_results, args.mode
    )
    retrieved_at = _utc_now()
    is_mock = "mock" in actual_provider

    normalized = [
        normalize_search_result(r, provider=actual_provider, query=args.query, is_mock=is_mock)
        for r in raw_results[:args.max_results]
    ]
    scored = [score_result(r) for r in normalized]

    output_dir = ROOT / "outputs" / "semantic_search_results"
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = urllib.parse.quote_plus(args.query[:50])
    ts = retrieved_at[:19].replace(":", "-")

    result_payload = {
        "provider": actual_provider,
        "query": args.query,
        "mode": args.mode,
        "retrieved_at": retrieved_at,
        "is_mock": is_mock,
        "warnings": warnings,
        "results": normalized,
        "quality_scores": scored,
    }

    json_path = output_dir / f"semantic_search_{slug}_{ts}.json"
    json_path.write_text(json.dumps(result_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    md_lines = [
        "# Semantic Search Results",
        "",
        f"**Query:** {args.query}",
        f"**Mode:** {args.mode}",
        f"**Provider:** {actual_provider}",
        f"**Retrieved:** {retrieved_at}",
        f"**Mock:** {is_mock}",
    ]
    if warnings:
        md_lines += ["", "**Warnings:**"] + [f"- {w}" for w in warnings]
    md_lines += ["", "---", ""]
    for i, (res, sc) in enumerate(zip(normalized, scored), 1):
        md_lines += [
            f"## {i}. {res['title']}",
            "",
            f"**URL:** {res['url']}",
            f"**Semantic Score:** {res.get('score') or 'n/a'} | **Quality:** {sc['quality_score']}/5",
            "",
            res["snippet"] or "_No snippet_",
            "",
        ]

    md_path = output_dir / f"semantic_search_{slug}_{ts}.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    build_and_save_references(
        normalized,
        source_type="semantic_search",
        query_or_input=args.query,
        root=ROOT,
    )

    print(f"[semantic_search] provider={actual_provider} results={len(normalized)} mock={is_mock}")
    print(f"  JSON  -> {json_path.relative_to(ROOT)}")
    print(f"  MD    -> {md_path.relative_to(ROOT)}")
    if warnings:
        for w in warnings:
            print(f"  WARN  {w}")


if __name__ == "__main__":
    main()
