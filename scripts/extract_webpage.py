"""
Extract clean markdown from a web page using Firecrawl or mock provider.

Usage:
    python scripts/extract_webpage.py --url "https://example.com/pricing"
    python scripts/extract_webpage.py --url "https://example.com" --provider mock
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

from core.web.result_normalizer import normalize_extraction_result
from core.web.reference_builder import build_reference, save_reference


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _mock_extract(url: str) -> dict:
    return {
        "url": url,
        "title": f"Mock extraction of {url}",
        "markdown": f"# Mock Extraction\n\nThis is a mock extraction of `{url}`.\n\nSet `FIRECRAWL_API_KEY` and `WEB_TOOLS_MODE=live` for real extraction.\n",
        "text": f"Mock extraction of {url}. Set FIRECRAWL_API_KEY and WEB_TOOLS_MODE=live for real extraction.",
        "isMock": True,
        "provider": "mock_extractor",
        "extractedAt": _utc_now(),
        "metadata": {"url": url, "provider": "mock_extractor"},
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
    if not data.get("success") or not data.get("data"):
        raise ValueError(f"Firecrawl returned unsuccessful response for {url}")
    page = data["data"]
    return {
        "url": url,
        "title": (page.get("metadata") or {}).get("title") or url,
        "markdown": page.get("markdown") or "",
        "text": (page.get("markdown") or "").replace("#", "").strip(),
        "isMock": False,
        "provider": "firecrawl",
        "extractedAt": _utc_now(),
        "metadata": page.get("metadata") or {},
    }


def _run_extract(url: str, provider: str) -> tuple[dict, str, list[str]]:
    mode = os.environ.get("WEB_TOOLS_MODE", "mock")
    warnings: list[str] = []

    if provider == "mock" or mode == "mock":
        return _mock_extract(url), "mock_extractor", []

    if provider == "firecrawl":
        api_key = os.environ.get("FIRECRAWL_API_KEY", "")
        if not api_key:
            warnings.append("FIRECRAWL_API_KEY not set — falling back to mock extraction")
            return _mock_extract(url), "mock_extractor", warnings
        try:
            return _firecrawl_extract(url, api_key), "firecrawl", warnings
        except Exception as exc:
            warnings.append(f"Firecrawl extraction failed ({exc}) — falling back to mock")
            return _mock_extract(url), "mock_extractor", warnings

    warnings.append(f"Unknown provider '{provider}' — using mock")
    return _mock_extract(url), "mock_extractor", warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract clean markdown from a web page")
    parser.add_argument("--url", required=True, help="URL to extract")
    parser.add_argument("--provider", default=os.environ.get("DEFAULT_EXTRACTOR_PROVIDER", "firecrawl"),
                        choices=["firecrawl", "mock"])
    args = parser.parse_args()

    raw, actual_provider, warnings = _run_extract(args.url, args.provider)
    is_mock = "mock" in actual_provider

    normalized = normalize_extraction_result(raw, provider=actual_provider, url=args.url, is_mock=is_mock)

    output_dir = ROOT / "outputs" / "extracted_pages"
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = urllib.parse.quote_plus(args.url[:60]).replace("%", "_")
    ts = _utc_now()[:19].replace(":", "-")

    json_path = output_dir / f"extraction_{slug}_{ts}.json"
    json_path.write_text(json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8")

    md_path = output_dir / f"extraction_{slug}_{ts}.md"
    header = [
        f"# {normalized['title']}",
        "",
        f"**URL:** {args.url}",
        f"**Provider:** {actual_provider}",
        f"**Extracted:** {normalized['retrieved_at']}",
        f"**Mock:** {is_mock}",
    ]
    if warnings:
        header += ["", "**Warnings:**"] + [f"- {w}" for w in warnings]
    header += ["", "---", ""]
    md_path.write_text("\n".join(header) + "\n" + normalized["markdown"], encoding="utf-8")

    ref = build_reference(
        {"url": args.url, "title": normalized["title"], "provider": actual_provider,
         "retrieved_at": normalized["retrieved_at"], "is_mock": is_mock},
        source_type="page_extraction",
        query_or_input=args.url,
    )
    ref["raw_file"] = str(json_path.relative_to(ROOT))
    ref["processed_file"] = str(md_path.relative_to(ROOT))
    save_reference(ref, root=ROOT)

    print(f"[extract_webpage] provider={actual_provider} mock={is_mock}")
    print(f"  JSON  -> {json_path.relative_to(ROOT)}")
    print(f"  MD    -> {md_path.relative_to(ROOT)}")
    if warnings:
        for w in warnings:
            print(f"  WARN  {w}")


if __name__ == "__main__":
    main()
