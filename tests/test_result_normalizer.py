import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.web.result_normalizer import (
    normalize_search_result,
    normalize_extraction_result,
    normalize_crawl_result,
)


def test_normalize_search_result_required_fields() -> None:
    raw = {"url": "https://example.com", "snippet": "Example content.", "score": 0.9}
    result = normalize_search_result(raw, provider="tavily", query="test query")
    assert result["url"] == "https://example.com"
    assert result["title"] == "https://example.com", "Missing title should fall back to URL"
    assert result["provider"] == "tavily"
    assert result["query"] == "test query"
    assert "retrieved_at" in result
    assert "is_mock" in result


def test_normalize_search_result_uses_url_as_title_when_missing() -> None:
    raw = {"url": "https://example.com/page"}
    result = normalize_search_result(raw, provider="mock", query="q")
    assert result["title"] == "https://example.com/page"


def test_normalize_search_result_is_mock_default_false() -> None:
    raw = {"url": "https://example.com", "title": "Example"}
    result = normalize_search_result(raw, provider="tavily", query="q")
    assert result["is_mock"] is False


def test_normalize_search_result_is_mock_true_from_raw() -> None:
    raw = {"url": "mock://test/1", "title": "Mock", "isMock": True}
    result = normalize_search_result(raw, provider="mock", query="q", is_mock=True)
    assert result["is_mock"] is True


def test_normalize_search_result_is_mock_propagated_from_arg() -> None:
    raw = {"url": "mock://test/1", "title": "Mock"}
    result = normalize_search_result(raw, provider="mock", query="q", is_mock=True)
    assert result["is_mock"] is True


def test_normalize_extraction_result_required_fields() -> None:
    raw = {"url": "https://example.com", "markdown": "# Hello", "title": "Hello Page"}
    result = normalize_extraction_result(raw, provider="firecrawl", url="https://example.com")
    assert result["url"] == "https://example.com"
    assert result["title"] == "Hello Page"
    assert result["markdown"] == "# Hello"
    assert result["provider"] == "firecrawl"
    assert "retrieved_at" in result
    assert "is_mock" in result


def test_normalize_crawl_result_required_fields() -> None:
    raw = {
        "startUrl": "https://example.com",
        "pages": [{"url": "https://example.com/page", "title": "Page", "text": "content", "status": 200}],
        "crawledAt": "2025-01-01T00:00:00Z",
        "provider": "scrapy",
        "isMock": False,
    }
    result = normalize_crawl_result(raw, provider="scrapy", domain="example.com")
    assert result["domain"] == "example.com"
    assert result["page_count"] == 1
    assert result["provider"] == "scrapy"
    assert result["is_mock"] is False


def test_normalize_search_result_preserves_score() -> None:
    raw = {"url": "https://example.com", "title": "Test", "score": 0.87}
    result = normalize_search_result(raw, provider="exa", query="q")
    assert result["score"] == 0.87
