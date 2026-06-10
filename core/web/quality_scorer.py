from __future__ import annotations

from typing import Any

_HIGH_AUTHORITY_DOMAINS = {
    "wikipedia.org", "github.com", "arxiv.org", "scholar.google.com",
    "hbr.org", "mckinsey.com", "forrester.com", "gartner.com",
    "techcrunch.com", "wired.com", "producthunt.com", "ycombinator.com",
}

_LOW_QUALITY_PATTERNS = ["spam", "casino", "click here", "free download", "lose weight fast"]


def score_result(result: dict[str, Any]) -> dict[str, Any]:
    url = str(result.get("url") or "")
    title = str(result.get("title") or "")
    snippet = str(result.get("snippet") or result.get("content") or "")
    query = str(result.get("query") or "")
    published_at = str(result.get("published_at") or result.get("publishedAt") or "")
    is_mock = bool(result.get("is_mock") or result.get("isMock"))

    reasons: list[str] = []
    score = 3.0

    # Relevance
    query_terms = set(query.lower().split())
    combined = (title + " " + snippet).lower()
    matched = sum(1 for term in query_terms if term in combined)
    if query_terms:
        relevance_ratio = matched / len(query_terms)
        if relevance_ratio >= 0.7:
            score += 0.5
            reasons.append("high relevance to query")
        elif relevance_ratio < 0.3:
            score -= 0.5
            reasons.append("low relevance to query")

    # Recency
    if published_at and published_at[:4].isdigit():
        year = int(published_at[:4])
        if year >= 2024:
            score += 0.5
            reasons.append("recent content (2024+)")
        elif year < 2020:
            score -= 0.5
            reasons.append("older content (pre-2020)")

    # Source authority
    domain = _extract_domain(url)
    if domain in _HIGH_AUTHORITY_DOMAINS:
        score += 0.5
        reasons.append(f"authoritative source ({domain})")
    elif url.startswith("mock://"):
        score = 1.0
        reasons.append("mock result — not a real source")

    # Specificity (snippet length as a proxy)
    if len(snippet) > 200:
        score += 0.25
        reasons.append("detailed snippet")
    elif len(snippet) < 30 and not is_mock:
        score -= 0.25
        reasons.append("very short snippet")

    # Low quality signals
    combined_lower = combined.lower()
    if any(pattern in combined_lower for pattern in _LOW_QUALITY_PATTERNS):
        score -= 1.0
        reasons.append("low quality signals detected")

    # Business usefulness (presence of business keywords)
    business_keywords = ["pricing", "offer", "consulting", "agency", "strategy", "revenue", "client", "service"]
    if any(kw in combined_lower for kw in business_keywords):
        score += 0.25
        reasons.append("business-relevant content")

    # Mock penalty
    if is_mock:
        score = min(score, 2.0)
        if "mock result" not in " ".join(reasons):
            reasons.append("mock data — lower reliability")

    score = round(max(1.0, min(5.0, score)), 2)

    recommended = _recommend_next_step(score, url, snippet)

    return {
        "url": url,
        "quality_score": score,
        "reasons": reasons,
        "recommended_next_step": recommended,
    }


def _extract_domain(url: str) -> str:
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc.replace("www.", "")
    except Exception:
        return ""


def _recommend_next_step(score: float, url: str, snippet: str) -> str:
    if score >= 4.5:
        return "extract_with_firecrawl"
    if score >= 3.5:
        return "save_for_rag"
    if score >= 2.5:
        return "screenshot_with_playwright"
    if "domain" in snippet.lower() or url.endswith("/") or len(url.split("/")) <= 4:
        return "crawl_with_scrapy"
    return "ignore"
