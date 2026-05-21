import json
import shutil
from pathlib import Path

from core.source_registry import SourceRegistry
from scripts.run_weekly_research import run_weekly_research

ROOT = Path(__file__).resolve().parents[1]


def test_weekly_research_report_includes_references(tmp_path: Path) -> None:
    source_id = "youtube"
    entry = SourceRegistry(ROOT).get(source_id)
    (tmp_path / "research" / "index").mkdir(parents=True)
    (tmp_path / "research" / "index" / "source_registry.yaml").write_text(
        json.dumps({"sources": {source_id: entry}}, indent=2) + "\n",
        encoding="utf-8",
    )
    for name in ["collected_references.jsonl", "source_run_log.jsonl", "signal_index.jsonl"]:
        (tmp_path / "research" / "index" / name).write_text("", encoding="utf-8")
    shutil.copytree(ROOT / "research" / "sources" / source_id, tmp_path / "research" / "sources" / source_id)

    report = run_weekly_research(tmp_path)
    text = report.read_text(encoding="utf-8")

    assert "# Weekly Research Report" in text
    assert "## References" in text
    assert "collected_references.jsonl" in text
