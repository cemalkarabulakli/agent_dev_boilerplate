from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.schema import load_yaml


class SourceRegistry:
    def __init__(self, root: Path):
        self.root = root
        self.path = root / "research" / "index" / "source_registry.yaml"

    def load(self) -> dict[str, Any]:
        return load_yaml(self.path)

    def sources(self) -> dict[str, dict[str, Any]]:
        return dict(self.load().get("sources", {}))

    def get(self, source_id: str) -> dict[str, Any]:
        sources = self.sources()
        if source_id not in sources:
            raise KeyError(f"Unknown research source: {source_id}")
        return sources[source_id]

    def enabled_sources(self) -> dict[str, dict[str, Any]]:
        return {source_id: data for source_id, data in self.sources().items() if data.get("enabled")}

    def save(self, data: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    def register(self, source_id: str, entry: dict[str, Any]) -> None:
        data = self.load()
        data.setdefault("sources", {})[source_id] = entry
        self.save(data)
