from __future__ import annotations

import json
import importlib
import inspect
from pathlib import Path
from typing import Any

from core.schema import load_yaml, utc_now
from core.source_registry import SourceRegistry
from tools.adapters.research_sources import ADAPTERS
from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter


class SourceCollector:
    def __init__(self, root: Path):
        self.root = root
        self.registry = SourceRegistry(root)
        self.run_log = root / "research" / "index" / "source_run_log.jsonl"
        self.signal_index = root / "research" / "index" / "signal_index.jsonl"

    def collect_source(self, source_id: str, query: str | None = None, limit: int | None = None) -> dict[str, Any]:
        entry = self.registry.get(source_id)
        config = load_yaml(self.root / "research" / "sources" / source_id / "source_config.yaml")
        adapter_name = str(entry.get("provider") or entry["adapter"])
        adapter_cls = self._resolve_adapter(adapter_name)
        adapter = adapter_cls.from_source_id(self.root, source_id, entry)
        queries = [query] if query else list(config.get("queries", []))
        max_results = int(limit or config.get("collection", {}).get("max_results_per_query", 20))
        result = adapter.run(queries, max_results)
        self._append_jsonl(self.run_log, {"created_at": utc_now(), **result})
        processed = json.loads((self.root / result["processed_file"]).read_text(encoding="utf-8"))
        for signal in processed:
            self._append_jsonl(self.signal_index, signal)
        return result

    def collect_all(self, category: str = "high_ticket_business") -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for source_id in self.registry.enabled_sources():
            result = self.collect_source(source_id)
            result["category"] = category
            results.append(result)
        return results

    def _append_jsonl(self, path: Path, data: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(data, ensure_ascii=False) + "\n")

    def _resolve_adapter(self, adapter_name: str) -> type[BaseSourceAdapter]:
        if adapter_name in ADAPTERS:
            return ADAPTERS[adapter_name]
        if adapter_name.endswith("_source_provider"):
            legacy_name = adapter_name.replace("_source_provider", "_adapter")
            if legacy_name in ADAPTERS:
                return ADAPTERS[legacy_name]
            if "competitor" in adapter_name and "competitor_source_provider" in ADAPTERS:
                return ADAPTERS["competitor_source_provider"]
            if "custom_source_provider" in ADAPTERS:
                return ADAPTERS["custom_source_provider"]
        module = importlib.import_module(f"tools.adapters.research_sources.{adapter_name}")
        candidates = [
            member
            for _, member in inspect.getmembers(module, inspect.isclass)
            if issubclass(member, BaseSourceAdapter) and member is not BaseSourceAdapter
        ]
        if not candidates:
            raise KeyError(f"Adapter class not found in module: {adapter_name}")
        return candidates[0]
