from pathlib import Path

from core.source_registry import SourceRegistry

ROOT = Path(__file__).resolve().parents[1]


def test_source_provider_registry_exposes_registered_sources() -> None:
    registry_text = (ROOT / "tools" / "web" / "registry" / "source_provider_registry.ts").read_text(encoding="utf-8")
    for source_id, entry in SourceRegistry(ROOT).sources().items():
        provider_name = entry.get("provider") or entry["adapter"]
        assert provider_name in registry_text or source_id == "competitors"
        assert (ROOT / "tools" / "web" / "sources" / f"{provider_name}.ts").exists()
