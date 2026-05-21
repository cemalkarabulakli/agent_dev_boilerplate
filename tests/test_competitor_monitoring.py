import json
import shutil
from pathlib import Path

from core.competitor_monitor import CompetitorMonitor
from core.source_registry import SourceRegistry

ROOT = Path(__file__).resolve().parents[1]


def test_competitor_monitoring_report_includes_references(tmp_path: Path) -> None:
    _copy_competitor_fixture(tmp_path)
    result = CompetitorMonitor(tmp_path).monitor("AI automation agency Bulgaria")

    assert (tmp_path / result["raw_file"]).exists()
    assert (tmp_path / result["processed_file"]).exists()
    report = (tmp_path / result["output_report_file"]).read_text(encoding="utf-8")
    assert "# Competitor Monitoring Report" in report
    assert "## References" in report
    assert result["references"]
    assert (tmp_path / "research" / "index" / "signal_index.jsonl").read_text(encoding="utf-8").strip()


def _copy_competitor_fixture(tmp_path: Path) -> None:
    entry = SourceRegistry(ROOT).get("competitors")
    (tmp_path / "research" / "index").mkdir(parents=True)
    (tmp_path / "research" / "index" / "source_registry.yaml").write_text(
        json.dumps({"sources": {"competitors": entry}}, indent=2) + "\n",
        encoding="utf-8",
    )
    for name in ["collected_references.jsonl", "source_run_log.jsonl", "signal_index.jsonl"]:
        (tmp_path / "research" / "index" / name).write_text("", encoding="utf-8")
    shutil.copytree(ROOT / "research" / "sources" / "competitors", tmp_path / "research" / "sources" / "competitors")
