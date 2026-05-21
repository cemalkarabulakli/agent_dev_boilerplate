import json
from pathlib import Path

from core.cross_source_analyzer import CrossSourceAnalyzer


def test_one_source_insight_is_candidate(tmp_path: Path) -> None:
    analyzer = CrossSourceAnalyzer(tmp_path)
    insights = analyzer.analyze([
        {"source": "reddit", "signal_type": "pain_points", "confidence": 0.55, "reference_ids": ["ref_1"]}
    ])

    assert insights[0].status == "candidate"
    assert insights[0].source_count == 1


def test_three_source_insight_can_be_validated(tmp_path: Path) -> None:
    analyzer = CrossSourceAnalyzer(tmp_path)
    insights = analyzer.analyze(
        [
            {"source": "reddit", "signal_type": "pain_points", "confidence": 0.7, "reference_ids": ["ref_1"]},
            {"source": "youtube", "signal_type": "pain_points", "confidence": 0.7, "reference_ids": ["ref_2"]},
            {"source": "google_trends", "signal_type": "pain_points", "confidence": 0.7, "reference_ids": ["ref_3"]},
        ]
    )
    report = analyzer.write_report(insights)

    assert insights[0].status == "validated"
    assert "## References" in report.read_text(encoding="utf-8")


def test_cross_source_report_reads_signal_index(tmp_path: Path) -> None:
    signal_index = tmp_path / "research" / "index" / "signal_index.jsonl"
    signal_index.parent.mkdir(parents=True)
    signal_index.write_text(
        json.dumps({"source": "web_search", "signal_type": "tool_mentions", "confidence": 0.6, "reference_ids": ["ref_tool"]}) + "\n",
        encoding="utf-8",
    )

    insights = CrossSourceAnalyzer(tmp_path).analyze()
    assert insights[0].key == "tool_mentions"
