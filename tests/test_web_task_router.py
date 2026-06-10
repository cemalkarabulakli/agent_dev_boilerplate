import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.web.web_task_router import route_web_task, list_task_types


def test_market_research_routes_to_tavily() -> None:
    result = route_web_task("market_research", "AI automation agency Bulgaria")
    assert result["selected_provider"] == "tavily"
    assert result["selected_tool"] == "search"


def test_competitor_discovery_routes_to_tavily() -> None:
    result = route_web_task("competitor_discovery", "AI automation agencies")
    assert result["selected_provider"] == "tavily"


def test_latest_info_routes_to_tavily() -> None:
    result = route_web_task("latest_info", "AI trends 2025")
    assert result["selected_provider"] == "tavily"


def test_rag_source_discovery_routes_to_exa() -> None:
    result = route_web_task("rag_source_discovery", "high ticket consulting frameworks")
    assert result["selected_provider"] == "exa"
    assert result["selected_tool"] == "semantic_search"


def test_semantic_search_routes_to_exa() -> None:
    result = route_web_task("semantic_search", "similar pages to example.com")
    assert result["selected_provider"] == "exa"


def test_self_hosted_search_routes_to_searxng() -> None:
    result = route_web_task("self_hosted_search", "AI agency Bulgaria")
    assert result["selected_provider"] == "searxng"
    assert result["selected_tool"] == "open_source_search"


def test_privacy_search_routes_to_searxng() -> None:
    result = route_web_task("privacy_search", "sensitive query")
    assert result["selected_provider"] == "searxng"


def test_page_extraction_routes_to_firecrawl() -> None:
    result = route_web_task("page_extraction", "https://example.com")
    assert result["selected_provider"] == "firecrawl"
    assert result["selected_tool"] == "extractor"


def test_landing_page_analysis_routes_to_firecrawl() -> None:
    result = route_web_task("landing_page_analysis", "https://example.com")
    assert result["selected_provider"] == "firecrawl"


def test_pricing_page_analysis_routes_to_firecrawl() -> None:
    result = route_web_task("pricing_page_analysis", "https://example.com/pricing")
    assert result["selected_provider"] == "firecrawl"


def test_screenshot_routes_to_playwright() -> None:
    result = route_web_task("screenshot", "https://example.com")
    assert result["selected_provider"] == "playwright"
    assert result["selected_tool"] == "browser"


def test_browser_workflow_routes_to_playwright() -> None:
    result = route_web_task("browser_workflow", "https://example.com/login")
    assert result["selected_provider"] == "playwright"


def test_large_crawl_routes_to_scrapy() -> None:
    result = route_web_task("large_crawl", "example.com")
    assert result["selected_provider"] == "scrapy"
    assert result["selected_tool"] == "crawler"


def test_scheduled_crawl_routes_to_scrapy() -> None:
    result = route_web_task("scheduled_crawl", "example.com")
    assert result["selected_provider"] == "scrapy"


def test_unknown_task_type_returns_default_with_warning() -> None:
    result = route_web_task("nonexistent_task_type", "some input")
    assert "warning" in result
    assert result["selected_provider"] == "tavily"


def test_result_includes_input_value_and_task_type() -> None:
    result = route_web_task("market_research", "my input value")
    assert result["input_value"] == "my input value"
    assert result["task_type"] == "market_research"


def test_list_task_types_returns_all_expected() -> None:
    types = list_task_types()
    expected = [
        "market_research", "competitor_discovery", "rag_source_discovery",
        "self_hosted_search", "page_extraction", "screenshot", "large_crawl",
    ]
    for t in expected:
        assert t in types, f"task type '{t}' missing from routing table"
