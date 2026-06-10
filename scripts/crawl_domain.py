"""
Crawl a domain using Scrapy or mock provider.

Usage:
    python scripts/crawl_domain.py --domain "example.com"
    python scripts/crawl_domain.py --domain "example.com" --provider mock
"""

from __future__ import annotations

import argparse
import json
import os
import sys
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

from core.web.result_normalizer import normalize_crawl_result
from core.web.reference_builder import build_reference, save_reference


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _mock_crawl(domain: str) -> dict:
    return {
        "startUrl": f"mock://crawl/{domain}",
        "pages": [
            {"url": f"mock://crawl/{domain}/page-{i}", "title": f"Mock page {i} of {domain}", "text": f"Mock content for page {i}.", "status": 200}
            for i in range(1, 6)
        ],
        "crawledAt": _utc_now(),
        "provider": "mock_crawler",
        "isMock": True,
        "metadata": {"domain": domain, "provider": "mock_crawler"},
    }


def _scrapy_crawl(domain: str) -> dict:
    try:
        import subprocess
        result = subprocess.run(
            ["scrapy", "crawl", "generic_spider", "-a", f"domain={domain}", "-o", "-:json"],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr[:200])
        pages = json.loads(result.stdout or "[]")
        return {
            "startUrl": f"https://{domain}",
            "pages": pages,
            "crawledAt": _utc_now(),
            "provider": "scrapy",
            "isMock": False,
        }
    except FileNotFoundError:
        raise RuntimeError("Scrapy is not installed. Run: pip install scrapy")


def _run_crawl(domain: str, provider: str) -> tuple[dict, str, list[str]]:
    mode = os.environ.get("WEB_TOOLS_MODE", "mock")
    scrapy_enabled = os.environ.get("SCRAPY_ENABLED", "true").lower() != "false"
    warnings: list[str] = []

    if provider == "mock" or mode == "mock":
        return _mock_crawl(domain), "mock_crawler", []

    if provider == "scrapy":
        if not scrapy_enabled:
            warnings.append("SCRAPY_ENABLED=false — falling back to mock crawler")
            return _mock_crawl(domain), "mock_crawler", warnings
        try:
            return _scrapy_crawl(domain), "scrapy", warnings
        except Exception as exc:
            warnings.append(f"Scrapy crawl failed ({exc}) — falling back to mock")
            return _mock_crawl(domain), "mock_crawler", warnings

    warnings.append(f"Unknown provider '{provider}' — using mock")
    return _mock_crawl(domain), "mock_crawler", warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Crawl a domain")
    parser.add_argument("--domain", required=True, help="Domain to crawl (e.g. example.com)")
    parser.add_argument("--provider", default=os.environ.get("DEFAULT_CRAWLER_PROVIDER", "scrapy"),
                        choices=["scrapy", "mock"])
    args = parser.parse_args()

    raw, actual_provider, warnings = _run_crawl(args.domain, args.provider)
    is_mock = "mock" in actual_provider

    normalized = normalize_crawl_result(raw, provider=actual_provider, domain=args.domain, is_mock=is_mock)

    output_dir = ROOT / "outputs" / "crawl_results"
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = _utc_now()[:19].replace(":", "-")
    slug = urllib.parse.quote_plus(args.domain[:40])

    json_path = output_dir / f"crawl_{slug}_{ts}.json"
    json_path.write_text(json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8")

    ref = build_reference(
        {"url": f"https://{args.domain}", "title": f"Crawl of {args.domain}",
         "provider": actual_provider, "retrieved_at": normalized["retrieved_at"], "is_mock": is_mock},
        source_type="crawl",
        query_or_input=args.domain,
    )
    ref["raw_file"] = str(json_path.relative_to(ROOT))
    save_reference(ref, root=ROOT)

    print(f"[crawl_domain] provider={actual_provider} pages={len(normalized['pages'])} mock={is_mock}")
    print(f"  JSON  -> {json_path.relative_to(ROOT)}")
    if warnings:
        for w in warnings:
            print(f"  WARN  {w}")


if __name__ == "__main__":
    main()
