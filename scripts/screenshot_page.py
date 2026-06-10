"""
Take a screenshot of a web page using Playwright or mock provider.

Usage:
    python scripts/screenshot_page.py --url "https://example.com"
    python scripts/screenshot_page.py --url "https://example.com" --provider mock
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

from core.web.reference_builder import build_reference, save_reference


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _mock_screenshot(url: str, output_path: Path) -> dict:
    note = {
        "url": url,
        "action": "screenshot",
        "ok": True,
        "content": None,
        "artifactPath": str(output_path),
        "note": "Mock screenshot — Playwright not available or WEB_TOOLS_MODE=mock. No image was captured.",
        "provider": "mock_browser",
        "isMock": True,
        "retrievedAt": _utc_now(),
    }
    output_path.write_text(json.dumps(note, indent=2), encoding="utf-8")
    return note


def _playwright_screenshot(url: str, output_path: Path) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError("Playwright is not installed. Run: pip install playwright && playwright install chromium")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.screenshot(path=str(output_path), full_page=True)
        browser.close()

    return {
        "url": url,
        "action": "screenshot",
        "ok": True,
        "artifactPath": str(output_path),
        "provider": "playwright",
        "isMock": False,
        "retrievedAt": _utc_now(),
    }


def _run_screenshot(url: str, provider: str, output_path: Path) -> tuple[dict, str, list[str]]:
    mode = os.environ.get("WEB_TOOLS_MODE", "mock")
    playwright_enabled = os.environ.get("PLAYWRIGHT_ENABLED", "true").lower() != "false"
    warnings: list[str] = []

    if provider == "mock" or mode == "mock":
        return _mock_screenshot(url, output_path.with_suffix(".json")), "mock_browser", []

    if provider == "playwright":
        if not playwright_enabled:
            warnings.append("PLAYWRIGHT_ENABLED=false — falling back to mock")
            return _mock_screenshot(url, output_path.with_suffix(".json")), "mock_browser", warnings
        try:
            return _playwright_screenshot(url, output_path), "playwright", warnings
        except Exception as exc:
            warnings.append(f"Playwright failed ({exc}) — falling back to mock")
            return _mock_screenshot(url, output_path.with_suffix(".json")), "mock_browser", warnings

    warnings.append(f"Unknown provider '{provider}' — using mock")
    return _mock_screenshot(url, output_path.with_suffix(".json")), "mock_browser", warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Take a screenshot of a web page")
    parser.add_argument("--url", required=True, help="URL to screenshot")
    parser.add_argument("--provider", default=os.environ.get("DEFAULT_BROWSER_PROVIDER", "playwright"),
                        choices=["playwright", "mock"])
    args = parser.parse_args()

    output_dir = ROOT / "outputs" / "screenshots"
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = urllib.parse.quote_plus(args.url[:60]).replace("%", "_")
    ts = _utc_now()[:19].replace(":", "-")
    screenshot_path = output_dir / f"screenshot_{slug}_{ts}.png"

    result, actual_provider, warnings = _run_screenshot(args.url, args.provider, screenshot_path)
    is_mock = "mock" in actual_provider

    artifact_path = Path(result.get("artifactPath") or str(screenshot_path))

    ref = build_reference(
        {"url": args.url, "title": f"Screenshot of {args.url}", "provider": actual_provider,
         "retrieved_at": result.get("retrievedAt", _utc_now()), "is_mock": is_mock},
        source_type="screenshot",
        query_or_input=args.url,
    )
    if artifact_path.exists():
        ref["raw_file"] = str(artifact_path.relative_to(ROOT))
    save_reference(ref, root=ROOT)

    print(f"[screenshot_page] provider={actual_provider} mock={is_mock}")
    print(f"  artifact -> {artifact_path.relative_to(ROOT)}")
    if warnings:
        for w in warnings:
            print(f"  WARN  {w}")


if __name__ == "__main__":
    main()
