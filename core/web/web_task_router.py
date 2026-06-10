from __future__ import annotations

from typing import Any

_ROUTING_TABLE: dict[str, dict[str, str]] = {
    "latest_info": {
        "selected_tool": "search",
        "selected_provider": "tavily",
        "reason": "Tavily is best for latest public information and AI-ready search context.",
        "recommended_next_step": "extract_with_firecrawl",
    },
    "market_research": {
        "selected_tool": "search",
        "selected_provider": "tavily",
        "reason": "Tavily is best for market research and discovering online business information.",
        "recommended_next_step": "extract_with_firecrawl",
    },
    "competitor_discovery": {
        "selected_tool": "search",
        "selected_provider": "tavily",
        "reason": "Tavily is best for finding competitors and recent competitive intelligence.",
        "recommended_next_step": "extract_with_firecrawl",
    },
    "rag_source_discovery": {
        "selected_tool": "semantic_search",
        "selected_provider": "exa",
        "reason": "Exa finds semantically relevant high-quality pages for RAG pipelines.",
        "recommended_next_step": "save_for_rag",
    },
    "semantic_search": {
        "selected_tool": "semantic_search",
        "selected_provider": "exa",
        "reason": "Exa is built for semantic search and similar-page discovery.",
        "recommended_next_step": "save_for_rag",
    },
    "self_hosted_search": {
        "selected_tool": "open_source_search",
        "selected_provider": "searxng",
        "reason": "SearXNG is self-hosted, privacy-friendly, and the open-source search fallback.",
        "recommended_next_step": "extract_with_firecrawl",
    },
    "privacy_search": {
        "selected_tool": "open_source_search",
        "selected_provider": "searxng",
        "reason": "SearXNG provides privacy-friendly metasearch without sending data to third parties.",
        "recommended_next_step": "extract_with_firecrawl",
    },
    "page_extraction": {
        "selected_tool": "extractor",
        "selected_provider": "firecrawl",
        "reason": "Firecrawl extracts clean markdown from web pages.",
        "recommended_next_step": "save_for_rag",
    },
    "landing_page_analysis": {
        "selected_tool": "extractor",
        "selected_provider": "firecrawl",
        "reason": "Firecrawl reliably extracts landing page content as clean markdown.",
        "recommended_next_step": "save_for_rag",
    },
    "pricing_page_analysis": {
        "selected_tool": "extractor",
        "selected_provider": "firecrawl",
        "reason": "Firecrawl extracts pricing page content as clean markdown.",
        "recommended_next_step": "save_for_rag",
    },
    "screenshot": {
        "selected_tool": "browser",
        "selected_provider": "playwright",
        "reason": "Playwright captures screenshots and renders JavaScript-heavy pages.",
        "recommended_next_step": "screenshot_with_playwright",
    },
    "browser_workflow": {
        "selected_tool": "browser",
        "selected_provider": "playwright",
        "reason": "Playwright handles browser automation: clicks, forms, and multi-step flows.",
        "recommended_next_step": "screenshot_with_playwright",
    },
    "js_heavy_page": {
        "selected_tool": "browser",
        "selected_provider": "playwright",
        "reason": "Playwright renders JavaScript-heavy pages that Firecrawl cannot fully process.",
        "recommended_next_step": "extract_with_firecrawl",
    },
    "large_crawl": {
        "selected_tool": "crawler",
        "selected_provider": "scrapy",
        "reason": "Scrapy handles large-scale, scheduled, and repeatable domain crawls.",
        "recommended_next_step": "crawl_with_scrapy",
    },
    "scheduled_crawl": {
        "selected_tool": "crawler",
        "selected_provider": "scrapy",
        "reason": "Scrapy is built for scheduled and recurring crawl jobs.",
        "recommended_next_step": "crawl_with_scrapy",
    },
}


def route_web_task(
    task_type: str,
    input_value: str,
    options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    options = options or {}
    route = _ROUTING_TABLE.get(task_type)
    if route is None:
        return {
            "selected_tool": "search",
            "selected_provider": "tavily",
            "reason": f"Unknown task type '{task_type}'. Defaulting to Tavily search.",
            "recommended_next_step": "extract_with_firecrawl",
            "input_value": input_value,
            "task_type": task_type,
            "warning": f"task_type '{task_type}' is not in the routing table — using default.",
        }
    return {**route, "input_value": input_value, "task_type": task_type}


def list_task_types() -> list[str]:
    return list(_ROUTING_TABLE.keys())
