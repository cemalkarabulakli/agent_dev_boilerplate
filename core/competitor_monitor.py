from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.reference_manager import ReferenceManager
from core.schema import load_yaml, utc_now


class CompetitorMonitor:
    def __init__(self, root: Path):
        self.root = root
        self.source_dir = root / "research" / "sources" / "competitors"
        self.raw_dir = self.source_dir / "raw"
        self.processed_dir = self.source_dir / "processed"
        self.reports_dir = self.source_dir / "reports"
        self.screenshots_dir = self.source_dir / "screenshots"
        self.output_dir = root / "outputs" / "competitor_monitoring"
        self.reference_manager = ReferenceManager(root)

    def monitor(self, query: str, screenshots: bool = False) -> dict[str, Any]:
        config = load_yaml(self.source_dir / "source_config.yaml")
        timestamp = utc_now().replace(":", "").replace("-", "")
        competitors = self._mock_competitors(query, int(config.get("collection", {}).get("max_results_per_query", 3)))
        raw_path = self.raw_dir / f"competitors_{timestamp}_raw.json"
        processed_path = self.processed_dir / f"competitors_{timestamp}_processed.json"
        report_path = self.reports_dir / "competitor_monitoring_report.md"
        output_report_path = self.output_dir / "competitor_monitoring_report.md"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        references = []
        for item in competitors:
            reference = self.reference_manager.create_reference(
                source="competitors",
                source_type="competitor_monitoring",
                query=query,
                title=item["title"],
                url=item["url"],
                author_or_channel=item["domain"],
                raw_file=str(raw_path.relative_to(self.root)),
                processed_file=str(processed_path.relative_to(self.root)),
                confidence=item["confidence"],
                is_mock=True,
                notes="Mock competitor monitoring reference. Configure Tavily, Firecrawl, and Playwright for live monitoring.",
            )
            item["reference_id"] = reference["id"]
            references.append(reference)

        raw_payload = {"query": query, "collected_at": utc_now(), "provider_plan": ["tavily", "firecrawl", "playwright_optional"], "results": competitors}
        raw_path.write_text(json.dumps(raw_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        processed = [self._process_competitor(item, processed_path) for item in competitors]
        processed_path.write_text(json.dumps(processed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        self._append_jsonl(self.root / "research" / "index" / "source_run_log.jsonl", {"created_at": utc_now(), "source": "competitors", "query": query, "raw_file": str(raw_path.relative_to(self.root)), "processed_file": str(processed_path.relative_to(self.root)), "mock": True})
        for signal in processed:
            self._append_jsonl(self.root / "research" / "index" / "signal_index.jsonl", signal)

        screenshot_files: list[str] = []
        if screenshots:
            screenshot = self.screenshots_dir / f"competitors_{timestamp}_mock_screenshot.txt"
            screenshot.write_text("Mock screenshot placeholder. Enable Playwright for live screenshots.\n", encoding="utf-8")
            screenshot_files.append(str(screenshot.relative_to(self.root)))

        report = self._render_report(query, competitors, processed, screenshot_files, references)
        report_path.write_text(report, encoding="utf-8")
        output_report_path.write_text(report, encoding="utf-8")
        return {
            "query": query,
            "raw_file": str(raw_path.relative_to(self.root)),
            "processed_file": str(processed_path.relative_to(self.root)),
            "report_file": str(report_path.relative_to(self.root)),
            "output_report_file": str(output_report_path.relative_to(self.root)),
            "references": [reference["id"] for reference in references],
            "mock": True,
        }

    def _mock_competitors(self, query: str, limit: int) -> list[dict[str, Any]]:
        count = max(1, min(limit, 3))
        return [
            {
                "id": f"competitor_{index + 1}",
                "title": f"Mock competitor {index + 1} for {query}",
                "domain": f"mock-competitor-{index + 1}.example",
                "url": f"mock://competitors/{index + 1}",
                "snippet": "Mock competitor result. Configure Tavily for live competitor discovery.",
                "confidence": 0.55,
                "is_mock": True,
            }
            for index in range(count)
        ]

    def _process_competitor(self, item: dict[str, Any], processed_path: Path) -> dict[str, Any]:
        return {
            "id": f"processed_{item['id']}",
            "source": "competitors",
            "raw_signal_ids": [item["id"]],
            "reference_ids": [item["reference_id"]],
            "insight_type": "competitor_signal",
            "summary": f"Candidate competitor positioning signal from {item['title']}.",
            "evidence": [item["snippet"]],
            "source_urls": [item["url"]],
            "confidence": item["confidence"],
            "scores": {"positioning_strength": item["confidence"]},
            "status": "candidate",
            "recommendation": "Review manually before changing offer, pricing, or positioning.",
            "created_at": utc_now(),
            "processed_file": str(processed_path.relative_to(self.root)),
            "is_mock": True,
        }

    def _render_report(self, query: str, competitors: list[dict[str, Any]], processed: list[dict[str, Any]], screenshots: list[str], references: list[dict[str, Any]]) -> str:
        lines = [
            "# Competitor Monitoring Report",
            "",
            "## Query",
            query,
            "",
            "## Competitors Found",
            *[f"- {item['title']} ({item['url']})" for item in competitors],
            "",
            "## Pages Extracted",
            *[f"- Mock extracted markdown for {item['url']}" for item in competitors],
            "",
            "## Screenshots Captured",
            *([f"- {path}" for path in screenshots] or ["- None. Screenshots are optional and require Playwright in live mode."]),
            "",
            "## Positioning Patterns",
            *[f"- {item['summary']}" for item in processed],
            "",
            "## Pricing Signals",
            "- Candidate only. No live pricing extracted in mock mode.",
            "",
            "## Offer Stack Signals",
            "- Candidate only. No live offer stack extracted in mock mode.",
            "",
            "## CTA Patterns",
            "- Candidate only. No live CTA extracted in mock mode.",
            "",
            "## Major Changes",
            "- No previous live run comparison available in mock mode.",
            "",
            "## Recommended Actions",
            "- Review live extracted pages before changing positioning, pricing, or offer stack.",
            "",
            "## References",
            *[f"- {reference['id']} {reference['url']}" for reference in references],
            "",
        ]
        return "\n".join(lines)

    def _append_jsonl(self, path: Path, data: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(data, ensure_ascii=False) + "\n")
