"""
Compare SearXNG, Tavily, and Exa results for the same query (all mock-safe).

Usage:
    python scripts/compare_web_tools.py --query "AI automation agency Bulgaria"
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


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _mock_results(query: str, provider: str, count: int = 5) -> list[dict]:
    return [
        {
            "title": f"[{provider}] Mock result {i + 1}: {query[:40]}",
            "url": f"mock://{provider}/{urllib.parse.quote(query[:30])}/{i + 1}",
            "snippet": f"Mock result from {provider}. Set API keys and WEB_TOOLS_MODE=live for real results.",
            "source": f"mock_{provider}",
            "score": round(0.9 - i * 0.08, 2),
            "isMock": True,
            "metadata": {"query": query, "provider": provider},
        }
        for i in range(count)
    ]


def _try_tavily(query: str) -> tuple[list[dict], str]:
    mode = os.environ.get("WEB_TOOLS_MODE", "mock")
    api_key = os.environ.get("TAVILY_API_KEY", "")
    if mode == "mock" or not api_key:
        return _mock_results(query, "tavily"), "mock"
    try:
        body = json.dumps({"query": query, "max_results": 5}).encode("utf-8")
        req = urllib.request.Request(
            "https://api.tavily.com/search",
            data=body,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        return data.get("results") or [], "live"
    except Exception:
        return _mock_results(query, "tavily"), "mock"


def _try_searxng(query: str) -> tuple[list[dict], str]:
    mode = os.environ.get("WEB_TOOLS_MODE", "mock")
    base_url = os.environ.get("SEARXNG_BASE_URL", "http://localhost:8080")
    if mode == "mock":
        return _mock_results(query, "searxng"), "mock"
    try:
        params = urllib.parse.urlencode({"q": query, "format": "json"})
        req = urllib.request.Request(
            f"{base_url.rstrip('/')}/search?{params}",
            headers={"Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        return (data.get("results") or [])[:5], "live"
    except Exception:
        return _mock_results(query, "searxng"), "mock"


def _try_exa(query: str) -> tuple[list[dict], str]:
    mode = os.environ.get("WEB_TOOLS_MODE", "mock")
    api_key = os.environ.get("EXA_API_KEY", "")
    if mode == "mock" or not api_key:
        return _mock_results(query, "exa"), "mock"
    try:
        body = json.dumps({"query": query, "numResults": 5, "useAutoprompt": True}).encode("utf-8")
        req = urllib.request.Request(
            "https://api.exa.ai/search",
            data=body,
            headers={"x-api-key": api_key, "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        return data.get("results") or [], "live"
    except Exception:
        return _mock_results(query, "exa"), "mock"


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare web tools for the same query")
    parser.add_argument("--query", required=True, help="Search query to compare across tools")
    args = parser.parse_args()

    query = args.query
    retrieved_at = _utc_now()

    tavily_raw, tavily_mode = _try_tavily(query)
    searxng_raw, searxng_mode = _try_searxng(query)
    exa_raw, exa_mode = _try_exa(query)

    def _normalize_all(raw_list: list[dict], provider: str, is_mock: bool) -> list[dict]:
        return [normalize_search_result(r, provider=provider, query=query, is_mock=is_mock) for r in raw_list]

    tavily_results = _normalize_all(tavily_raw, "tavily", tavily_mode == "mock")
    searxng_results = _normalize_all(searxng_raw, "searxng", searxng_mode == "mock")
    exa_results = _normalize_all(exa_raw, "exa", exa_mode == "mock")

    output_dir = ROOT / "outputs" / "tool_comparisons"
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "web_tool_comparison.json"
    json_path.write_text(json.dumps({
        "query": query,
        "retrieved_at": retrieved_at,
        "tools": {
            "tavily": {"mode": tavily_mode, "results": tavily_results},
            "searxng": {"mode": searxng_mode, "results": searxng_results},
            "exa": {"mode": exa_mode, "results": exa_results},
        },
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    def _tool_section(name: str, results: list[dict], mode: str) -> list[str]:
        lines = [f"## {name.upper()} ({mode} mode)", ""]
        for i, r in enumerate(results, 1):
            sc = score_result(r)
            lines += [
                f"### {i}. {r['title']}",
                f"**URL:** {r['url']}",
                f"**Quality:** {sc['quality_score']}/5",
                "",
                r["snippet"] or "_No snippet_",
                "",
            ]
        return lines

    md_lines = [
        "# Web Tool Comparison",
        "",
        f"**Query:** {query}",
        f"**Generated:** {retrieved_at}",
        "",
        "| Tool | Mode | Results |",
        "| --- | --- | --- |",
        f"| Tavily | {tavily_mode} | {len(tavily_results)} |",
        f"| SearXNG | {searxng_mode} | {len(searxng_results)} |",
        f"| Exa | {exa_mode} | {len(exa_results)} |",
        "",
        "---",
        "",
    ]
    md_lines += _tool_section("tavily", tavily_results, tavily_mode)
    md_lines += ["---", ""]
    md_lines += _tool_section("searxng", searxng_results, searxng_mode)
    md_lines += ["---", ""]
    md_lines += _tool_section("exa", exa_results, exa_mode)

    md_path = output_dir / "web_tool_comparison.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"[compare_web_tools] query='{query}'")
    print(f"  Tavily={len(tavily_results)} ({tavily_mode})  SearXNG={len(searxng_results)} ({searxng_mode})  Exa={len(exa_results)} ({exa_mode})")
    print(f"  MD   -> {md_path.relative_to(ROOT)}")
    print(f"  JSON -> {json_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
