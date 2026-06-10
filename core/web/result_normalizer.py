from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_search_result(
    raw: dict[str, Any],
    *,
    provider: str,
    query: str,
    is_mock: bool = False,
) -> dict[str, Any]:
    url = str(raw.get("url") or raw.get("link") or "")
    title = str(raw.get("title") or raw.get("name") or "") or url
    snippet = str(raw.get("snippet") or raw.get("content") or raw.get("text") or "")
    published_at = str(raw.get("publishedAt") or raw.get("published_at") or raw.get("date") or "")
    score = raw.get("score") or raw.get("relevance_score")

    return {
        "title": title,
        "url": url,
        "snippet": snippet,
        "content": raw.get("content") or raw.get("text"),
        "published_at": published_at or None,
        "source": str(raw.get("source") or raw.get("engine") or provider),
        "score": float(score) if score is not None else None,
        "provider": provider,
        "query": query,
        "retrieved_at": str(raw.get("retrieved_at") or raw.get("retrievedAt") or _utc_now()),
        "is_mock": bool(raw.get("isMock", is_mock)),
        "metadata": raw.get("metadata") or {},
    }


def normalize_extraction_result(
    raw: dict[str, Any],
    *,
    provider: str,
    url: str,
    is_mock: bool = False,
) -> dict[str, Any]:
    title = str(raw.get("title") or "") or url
    markdown = str(raw.get("markdown") or raw.get("content") or "")
    text = str(raw.get("text") or markdown)

    return {
        "url": url,
        "title": title,
        "markdown": markdown,
        "text": text,
        "provider": provider,
        "retrieved_at": str(raw.get("extractedAt") or raw.get("retrieved_at") or _utc_now()),
        "is_mock": bool(raw.get("isMock", is_mock)),
        "metadata": raw.get("metadata") or {},
    }


def normalize_crawl_result(
    raw: dict[str, Any],
    *,
    provider: str,
    domain: str,
    is_mock: bool = False,
) -> dict[str, Any]:
    pages = raw.get("pages") or []
    return {
        "domain": domain,
        "start_url": str(raw.get("startUrl") or raw.get("start_url") or f"https://{domain}"),
        "pages": [
            {
                "url": str(p.get("url") or ""),
                "title": str(p.get("title") or p.get("url") or ""),
                "text": str(p.get("text") or ""),
                "status": int(p.get("status") or 200),
            }
            for p in pages
        ],
        "page_count": len(pages),
        "provider": provider,
        "retrieved_at": str(raw.get("crawledAt") or raw.get("retrieved_at") or _utc_now()),
        "is_mock": bool(raw.get("isMock", is_mock)),
        "metadata": raw.get("metadata") or {},
    }
