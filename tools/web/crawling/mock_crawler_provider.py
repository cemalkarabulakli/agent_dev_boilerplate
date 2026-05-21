from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.schema import utc_now


@dataclass(frozen=True)
class MockCrawlResult:
    start_url: str
    pages: list[dict[str, Any]]
    crawled_at: str
    provider: str = "mock_crawler"
    is_mock: bool = True


class MockCrawlerProvider:
    def crawl(self, start_url: str, options: dict[str, Any] | None = None) -> MockCrawlResult:
        return MockCrawlResult(
            start_url=start_url,
            pages=[{"url": start_url, "title": "Mock crawled page", "text": "Configure Scrapy for live crawling.", "status": 200}],
            crawled_at=utc_now(),
        )

    def crawl_domain(self, domain: str, options: dict[str, Any] | None = None) -> MockCrawlResult:
        return self.crawl(f"mock://crawl/{domain}", options)

    def schedule_crawl(self, job_config: dict[str, Any]) -> dict[str, Any]:
        return {"job_id": str(job_config.get("id", "mock_crawl_job")), "scheduled": True, "is_mock": True}

