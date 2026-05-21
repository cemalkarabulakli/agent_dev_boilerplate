import json
from pathlib import Path

from scripts.add_research_source import add_source


def test_add_research_source_creates_structure_adapter_and_registry(tmp_path: Path) -> None:
    (tmp_path / "research" / "index").mkdir(parents=True)
    (tmp_path / "research" / "index" / "source_registry.yaml").write_text('{"sources": {}}\n', encoding="utf-8")
    (tmp_path / "tools" / "adapters" / "research_sources").mkdir(parents=True)
    (tmp_path / "tools" / "web" / "sources").mkdir(parents=True)
    (tmp_path / "checklists").mkdir()

    created = add_source("tiktok", "TikTok", "short_video", root=tmp_path)

    assert (created / "source_config.yaml").exists()
    assert (created / "raw").exists()
    assert (created / "processed").exists()
    assert (created / "reports").exists()
    assert (tmp_path / "tools" / "adapters" / "research_sources" / "tiktok_source_provider.py").exists()
    assert (tmp_path / "tools" / "web" / "sources" / "tiktok_source_provider.ts").exists()

    registry = json.loads((tmp_path / "research" / "index" / "source_registry.yaml").read_text(encoding="utf-8"))
    assert registry["sources"]["tiktok"]["adapter"] == "tiktok_source_provider"
