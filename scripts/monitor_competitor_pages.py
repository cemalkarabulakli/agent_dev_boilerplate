"""
Competitor monitoring: discover -> extract -> screenshot -> report.

Workflow:
  1. Tavily: find competitor pages for the query
  2. Firecrawl: extract landing/pricing pages (mock-safe)
  3. Playwright: screenshot if enabled (mock-safe)
  4. Save references
  5. Compare with previous run if available
  6. Generate competitor monitoring report

Usage:
    python scripts/monitor_competitor_pages.py --query "AI automation agency Bulgaria"
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

from core.web.result_normalizer import normalize_search_result, normalize_extraction_result
from core.web.quality_scorer import score_result
from core.web.reference_builder import build_reference, save_reference


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ─── Search step ──────────────────────────────────────────────────────────────

def _mock_competitors(query: str) -> list[dict]:
    return [
        {"title": f"Mock competitor {i}: {query[:30]}", "url": f"mock://competitor/{i}", "snippet": f"Mock competitor {i} for {query}.", "source": "mock_search", "score": 0.9 - i * 0.1, "isMock": True, "metadata": {}}
        for i in range(1, 4)
    ]


def _find_competitors(query: str) -> tuple[list[dict], str]:
    mode = os.environ.get("WEB_TOOLS_MODE", "mock")
    api_key = os.environ.get("TAVILY_API_KEY", "")
    if mode == "mock" or not api_key:
        return _mock_competitors(query), "mock"
    try:
        body = json.dumps({"query": f"top competitors {query}", "max_results": 5}).encode("utf-8")
        req = urllib.request.Request(
            "https://api.tavily.com/search",
            data=body,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        return data.get("results") or [], "live"
    except Exception:
        return _mock_competitors(query), "mock"


# ─── Extraction step ──────────────────────────────────────────────────────────

def _mock_extract(url: str) -> dict:
    return {
        "url": url, "title": f"Mock: {url}", "markdown": f"# Mock\n\nMock extraction of `{url}`.",
        "text": f"Mock extraction of {url}.", "isMock": True, "provider": "mock_extractor",
        "extractedAt": _utc_now(), "metadata": {},
    }


def _firecrawl_extract(url: str, api_key: str) -> dict:
    body = json.dumps({"url": url, "formats": ["markdown"], "onlyMainContent": True}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v1/scrape",
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    if not data.get("success"):
        raise ValueError(f"Firecrawl: no success for {url}")
    page = data.get("data") or {}
    return {
        "url": url, "title": (page.get("metadata") or {}).get("title") or url,
        "markdown": page.get("markdown") or "", "text": page.get("markdown", "").replace("#", "").strip(),
        "isMock": False, "provider": "firecrawl", "extractedAt": _utc_now(),
        "metadata": page.get("metadata") or {},
    }


def _extract_page(url: str) -> tuple[dict, bool]:
    if url.startswith("mock://"):
        return _mock_extract(url), True
    mode = os.environ.get("WEB_TOOLS_MODE", "mock")
    api_key = os.environ.get("FIRECRAWL_API_KEY", "")
    if mode == "mock" or not api_key:
        return _mock_extract(url), True
    try:
        return _firecrawl_extract(url, api_key), False
    except Exception:
        return _mock_extract(url), True


# ─── Screenshot step ──────────────────────────────────────────────────────────

def _try_screenshot(url: str, output_path: Path) -> tuple[str | None, bool]:
    if url.startswith("mock://"):
        return None, True
    mode = os.environ.get("WEB_TOOLS_MODE", "mock")
    playwright_enabled = os.environ.get("PLAYWRIGHT_ENABLED", "true").lower() != "false"
    if mode == "mock" or not playwright_enabled:
        return None, True
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.screenshot(path=str(output_path), full_page=True)
            browser.close()
        return str(output_path), False
    except Exception:
        return None, True


# ─── Report generation ────────────────────────────────────────────────────────

def _load_previous_report(output_dir: Path, query: str) -> dict | None:
    slug = urllib.parse.quote_plus(query[:40])
    for f in sorted(output_dir.glob(f"competitor_monitoring_{slug}_*.json"), reverse=True):
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor competitor pages")
    parser.add_argument("--query", required=True, help="Niche or market to monitor competitors for")
    args = parser.parse_args()

    query = args.query
    retrieved_at = _utc_now()
    ts = retrieved_at[:19].replace(":", "-")
    slug = urllib.parse.quote_plus(query[:40])

    output_dir = ROOT / "outputs" / "competitor_monitoring"
    screenshot_dir = ROOT / "outputs" / "screenshots"
    output_dir.mkdir(parents=True, exist_ok=True)
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Find competitors
    raw_competitors, search_mode = _find_competitors(query)
    competitors = [
        normalize_search_result(r, provider="tavily" if search_mode == "live" else "mock", query=query, is_mock=search_mode == "mock")
        for r in raw_competitors
    ]

    # Step 2–4: Extract + screenshot each competitor
    competitor_data = []
    references = []

    for comp in competitors:
        url = comp["url"]
        raw_ext, ext_mock = _extract_page(url)
        extraction = normalize_extraction_result(raw_ext, provider=raw_ext.get("provider", "mock_extractor"), url=url, is_mock=ext_mock)

        ss_path = screenshot_dir / f"competitor_{urllib.parse.quote_plus(url[:40]).replace('%', '_')}_{ts}.png"
        ss_artifact, ss_mock = _try_screenshot(url, ss_path)
        quality = score_result(comp)

        competitor_data.append({
            "search_result": comp,
            "extraction": extraction,
            "screenshot": ss_artifact,
            "screenshot_mock": ss_mock,
            "quality": quality,
        })

        ref = build_reference(
            {"url": url, "title": comp["title"], "provider": comp["provider"],
             "retrieved_at": retrieved_at, "is_mock": comp["is_mock"]},
            source_type="competitor_monitoring",
            query_or_input=query,
        )
        save_reference(ref, root=ROOT)
        references.append(ref)

    # Step 5: Load previous for comparison
    previous = _load_previous_report(output_dir, query)
    new_urls = {c["search_result"]["url"] for c in competitor_data}
    prev_urls = {c["search_result"]["url"] for c in (previous or {}).get("competitors", [])} if previous else set()
    new_this_run = new_urls - prev_urls
    disappeared = prev_urls - new_urls

    # Step 6: Save JSON
    run_data = {
        "query": query,
        "retrieved_at": retrieved_at,
        "search_mode": search_mode,
        "is_mock": search_mode == "mock",
        "competitors": competitor_data,
        "references": references,
        "diff": {
            "new_this_run": sorted(new_this_run),
            "disappeared": sorted(disappeared),
        },
    }
    json_path = output_dir / f"competitor_monitoring_{slug}_{ts}.json"
    json_path.write_text(json.dumps(run_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Step 7: Generate report
    md_lines = [
        "# Competitor Monitoring Report",
        "",
        f"**Query:** {query}",
        f"**Generated:** {retrieved_at}",
        f"**Search Mode:** {search_mode}",
        f"**Competitors Found:** {len(competitor_data)}",
        "",
    ]
    if new_this_run:
        md_lines += ["**New this run:**"] + [f"- {u}" for u in sorted(new_this_run)] + [""]
    if disappeared:
        md_lines += ["**No longer appearing:**"] + [f"- {u}" for u in sorted(disappeared)] + [""]
    md_lines += ["---", ""]

    for cd in competitor_data:
        res = cd["search_result"]
        ext = cd["extraction"]
        q = cd["quality"]
        md_lines += [
            f"## {res['title']}",
            "",
            f"**URL:** {res['url']}",
            f"**Quality:** {q['quality_score']}/5 — {', '.join(q['reasons'][:3])}",
            f"**Screenshot:** {'captured' if cd['screenshot'] else 'mock/unavailable'}",
            "",
            f"### Extracted Content",
            "",
            (ext.get("markdown") or "_No content extracted_")[:800],
            "",
        ]

    md_lines += [
        "---",
        "",
        "## References",
        "",
    ]
    for ref in references:
        md_lines.append(f"- [{ref['title']}]({ref['url']}) — `{ref['id']}`")

    report_path = output_dir / "competitor_monitoring_report.md"
    report_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"[monitor_competitor_pages] query='{query}' competitors={len(competitor_data)} mock={search_mode == 'mock'}")
    print(f"  Report -> {report_path.relative_to(ROOT)}")
    print(f"  JSON   -> {json_path.relative_to(ROOT)}")
    if new_this_run:
        print(f"  New: {', '.join(sorted(new_this_run))}")


if __name__ == "__main__":
    main()
