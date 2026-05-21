from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.cross_source_analyzer import CrossSourceAnalyzer  # noqa: E402
from core.schema import utc_now  # noqa: E402
from core.source_collector import SourceCollector  # noqa: E402


def run_weekly_research(root: Path = ROOT) -> Path:
    collector = SourceCollector(root)
    results = []
    failed: list[str] = []
    for source_id in collector.registry.enabled_sources():
        try:
            result = collector.collect_source(source_id)
            result["category"] = "high_ticket_business"
            results.append(result)
        except Exception as exc:
            failed.append(f"{source_id}: {exc}")
    cross_report = CrossSourceAnalyzer(root).write_report()
    weekly_dir = root / "outputs" / "weekly_reports"
    weekly_dir.mkdir(parents=True, exist_ok=True)
    weekly_report = weekly_dir / "weekly_research_report.md"
    mock_sources = [result["source"] for result in results if result.get("mock")]
    lines = [
        "# Weekly Research Report",
        "",
        f"## Date\n{utc_now()}",
        "",
        "## Sources Run",
        *[f"- {result['source']} ({result['mode']})" for result in results],
        "",
        "## Sources Failed",
        *([f"- {item}" for item in failed] or ["- None"]),
        "",
        "## Mock Sources",
        *([f"- {item}" for item in mock_sources] or ["- None"]),
        "",
        "## Validated Signals",
        "- See cross-source report.",
        "",
        "## Candidate Signals",
        "- See per-source processed files and cross-source report.",
        "",
        "## Repeated Pain Points",
        "- See cross-source report.",
        "",
        "## Repeated Objections",
        "- See cross-source report.",
        "",
        "## Offer Opportunities",
        "- See cross-source report.",
        "",
        "## Content Opportunities",
        "- See cross-source report.",
        "",
        "## Ad Angle Opportunities",
        "- See cross-source report.",
        "",
        "## Tool Opportunities",
        "- See cross-source report.",
        "",
        "## Recommended Experiments",
        "- Human review required before strategy updates.",
        "",
        "## Human Review Required",
        "- Yes. Do not update business strategy from candidate insights automatically.",
        "",
        "## References",
        f"- {root / 'research' / 'index' / 'collected_references.jsonl'}",
        f"- {cross_report}",
    ]
    weekly_report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    quality_dir = root / "outputs" / "quality_reports"
    quality_dir.mkdir(parents=True, exist_ok=True)
    (quality_dir / "weekly_research_run.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return weekly_report


def main() -> int:
    weekly_report = run_weekly_research(ROOT)
    print(weekly_report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
