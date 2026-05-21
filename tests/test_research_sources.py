import json
import shutil
from pathlib import Path

from core.schema import load_yaml
from core.source_collector import SourceCollector
from core.source_registry import SourceRegistry

ROOT = Path(__file__).resolve().parents[1]


def test_every_registered_source_has_config_folders_and_adapter() -> None:
    registry = SourceRegistry(ROOT)
    for source_id, entry in registry.sources().items():
        source_dir = ROOT / "research" / "sources" / source_id
        assert (source_dir / "source_config.yaml").exists()
        assert (source_dir / "raw").exists()
        assert (source_dir / "processed").exists()
        assert (source_dir / "reports").exists()
        assert (ROOT / "tools" / "adapters" / "research_sources" / f"{entry['adapter']}.py").exists()


def test_every_builtin_adapter_supports_mock_mode() -> None:
    registry = SourceRegistry(ROOT)
    for source_id, entry in registry.sources().items():
        config = load_yaml(ROOT / "research" / "sources" / source_id / "source_config.yaml")
        assert config["mode"] == "mock"
        assert (ROOT / "tools" / "adapters" / "research_sources" / f"{entry['adapter']}.py").exists()


def test_collect_source_creates_raw_processed_report_and_references(tmp_path: Path) -> None:
    root = _single_source_root(tmp_path, "reddit")
    result = SourceCollector(root).collect_source("reddit", "coaches struggling to get clients", limit=1)

    assert (root / result["raw_file"]).exists()
    assert (root / result["processed_file"]).exists()
    assert (root / result["report_file"]).exists()

    processed = json.loads((root / result["processed_file"]).read_text(encoding="utf-8"))
    assert processed
    assert all(signal["reference_ids"] for signal in processed)

    references = (root / "research" / "index" / "collected_references.jsonl").read_text(encoding="utf-8").splitlines()
    assert references
    assert json.loads(references[0])["raw_file"] == result["raw_file"]


def _single_source_root(tmp_path: Path, source_id: str) -> Path:
    root = tmp_path
    entry = SourceRegistry(ROOT).get(source_id)
    (root / "research" / "index").mkdir(parents=True)
    (root / "research" / "index" / "source_registry.yaml").write_text(
        json.dumps({"sources": {source_id: entry}}, indent=2) + "\n",
        encoding="utf-8",
    )
    for name in ["collected_references.jsonl", "source_run_log.jsonl", "signal_index.jsonl"]:
        (root / "research" / "index" / name).write_text("", encoding="utf-8")
    shutil.copytree(ROOT / "research" / "sources" / source_id, root / "research" / "sources" / source_id)
    return root
