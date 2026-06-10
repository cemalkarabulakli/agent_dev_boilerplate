"""
Run a web search using Tavily, SearXNG, or mock provider.

Usage:
    python scripts/run_web_search.py --query "AI automation agency Bulgaria"
    python scripts/run_web_search.py --query "AI automation agency Bulgaria" --provider tavily
    python scripts/run_web_search.py --query "AI automation agency Bulgaria" --provider searxng
    python scripts/run_web_search.py --query "AI automation agency" --provider mock
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
            "title": f"Mock search result {i + 1} for: {query}",
            "url": f"mock://web-search/{urllib.parse.quote(query)}/{i + 1}",
            "snippet": f"Mock result {i + 1}. Set TAVILY_API_KEY or SEARXNG_BASE_URL and WEB_TOOLS_MODE=live for real results.",
            "source": "mock_search",
            "score": round(0.9 - i * 0.1, 2),
            "isMock": True,
            "metadata": {"query": query, "provider": "mock"},
        }
        for i in range(5)
    ]


def _tavily_search(query: str, api_key: str, max_results: int = 10) -> list[dict]:
    body = json.dumps({
        "query": query,
        "max_results": max_results,
        "include_raw_content": False,
        "include_answer": True,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.tavily.com/search",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return data.get("results") or []


def _searxng_search(query: str, base_url: str, max_results: int = 10) -> list[dict]:
    params = urllib.parse.urlencode({"q": query, "format": "json", "categories": "general"})
    url = f"{base_url.rstrip('/')}/search?{params}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    return (data.get("results") or [])[:max_results]


def _run_search(query: str, provider: str) -> tuple[list[dict], str, list[str]]:
    mode = os.environ.get("WEB_TOOLS_MODE", "mock")
    warnings: list[str] = []

    if provider == "mock" or mode == "mock":
        return _mock_results(query), "mock", []

    if provider == "tavily":
        api_key = os.environ.get("TAVILY_API_KEY", "")
        if not api_key:
            warnings.append("TAVILY_API_KEY not set — falling back to mock")
            return _mock_results(query), "mock", warnings
        try:
            return _tavily_search(query, api_key), "tavily", warnings
        except Exception as exc:
            warnings.append(f"Tavily search failed ({exc}) — falling back to mock")
            return _mock_results(query), "mock", warnings

    if provider == "searxng":
        base_url = os.environ.get("SEARXNG_BASE_URL", "http://localhost:8080")
        try:
            return _searxng_search(query, base_url), "searxng", warnings
        except Exception as exc:
            warnings.append(f"SearXNG unreachable at {base_url} ({exc}) — falling back to mock")
            return _mock_results(query), "mock", warnings

    warnings.append(f"Unknown provider '{provider}' — using mock")
    return _mock_results(query), "mock", warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a web search")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--provider", default=os.environ.get("DEFAULT_SEARCH_PROVIDER", "tavily"),
                        choices=["tavily", "searxng", "mock"])
    parser.add_argument("--max-results", type=int, default=int(os.environ.get("SEARCH_MAX_RESULTS", 10)))
    args = parser.parse_args()

    raw_results, actual_provider, warnings = _run_search(args.query, args.provider)
    retrieved_at = _utc_now()
    is_mock = actual_provider == "mock"

    normalized = [
        normalize_search_result(r, provider=actual_provider, query=args.query, is_mock=is_mock)
        for r in raw_results[:args.max_results]
    ]
    scored = [score_result(r) for r in normalized]

    output_dir = ROOT / "outputs" / "web_search_results"
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = urllib.parse.quote_plus(args.query[:50])
    ts = retrieved_at[:19].replace(":", "-")

    result_payload = {
        "provider": actual_provider,
        "query": args.query,
        "retrieved_at": retrieved_at,
        "is_mock": is_mock,
        "warnings": warnings,
        "results": normalized,
        "quality_scores": scored,
    }

    json_path = output_dir / f"web_search_{slug}_{ts}.json"
    json_path.write_text(json.dumps(result_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    md_lines = [
        f"# Web Search Results",
        f"",
        f"**Query:** {args.query}",
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
            f"",
            f"**URL:** {res['url']}",
            f"**Score:** {sc['quality_score']}/5 — {', '.join(sc['reasons'][:3])}",
            f"",
            res["snippet"] or "_No snippet_",
            "",
        ]

    md_path = output_dir / f"web_search_{slug}_{ts}.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    build_and_save_references(
        normalized,
        source_type="web_search",
        query_or_input=args.query,
        root=ROOT,
    )

    print(f"[web_search] provider={actual_provider} results={len(normalized)} mock={is_mock}")
    print(f"  JSON  -> {json_path.relative_to(ROOT)}")
    print(f"  MD    -> {md_path.relative_to(ROOT)}")
    if warnings:
        for w in warnings:
            print(f"  WARN  {w}")


if __name__ == "__main__":
    main()
