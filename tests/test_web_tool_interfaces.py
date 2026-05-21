from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_web_tool_interfaces_exist_with_methods() -> None:
    expected = {
        "web_search_tool.ts": ["search(", "searchNews(", "findCompetitors(", "findLatest("],
        "web_extractor_tool.ts": ["extract(", "extractMany(", "extractMarkdown(", "extractPricingPage(", "extractLandingPage("],
        "browser_automation_tool.ts": ["open(", "click(", "type(", "screenshot(", "pdf(", "getContent(", "getUrl(", "close("],
        "web_crawler_tool.ts": ["crawl(", "crawlDomain(", "scheduleCrawl("],
        "source_collector_tool.ts": ["collect(", "process(", "generateReport("],
        "trend_provider_tool.ts": ["getTrend(", "compareTrends(", "getRelatedQueries("],
    }
    for filename, methods in expected.items():
        text = (ROOT / "tools" / "web" / "interfaces" / filename).read_text(encoding="utf-8")
        for method in methods:
            assert method in text


def test_agents_do_not_import_direct_web_providers() -> None:
    forbidden = ["import tavily", "from tavily", "import firecrawl", "from firecrawl", "import playwright", "from playwright", "import scrapy", "from scrapy"]
    for path in (ROOT / "agents").glob("**/*"):
        if path.is_file() and path.suffix in {".md", ".yaml"}:
            text = path.read_text(encoding="utf-8").lower()
            assert not any(term in text for term in forbidden), path


def test_source_signal_types_are_python_compatible() -> None:
    text = (ROOT / "tools" / "web" / "types" / "source_signal.ts").read_text(encoding="utf-8")
    for field in ["source_type", "author_or_channel", "collected_at", "reference_id", "raw_signal_ids", "reference_ids", "insight_type", "source_urls", "created_at", "is_mock"]:
        assert field in text
