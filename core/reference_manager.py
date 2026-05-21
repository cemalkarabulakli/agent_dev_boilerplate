from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.schema import utc_now


class ReferenceManager:
    def __init__(self, root: Path):
        self.root = root
        self.path = root / "research" / "index" / "collected_references.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def read_all(self) -> list[dict[str, Any]]:
        references: list[dict[str, Any]] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                references.append(json.loads(line))
        return references

    def create_reference(
        self,
        *,
        source: str,
        source_type: str,
        query: str,
        title: str,
        url: str,
        author_or_channel: str = "",
        published_at: str = "",
        raw_file: str = "",
        processed_file: str = "",
        confidence: float = 0.0,
        is_mock: bool = False,
        notes: str = "",
    ) -> dict[str, Any]:
        reference = {
            "id": f"ref_{utc_now()[:10].replace('-', '_')}_{len(self.read_all()) + 1:04d}",
            "source": source,
            "source_type": source_type,
            "query": query,
            "title": title,
            "url": url,
            "author_or_channel": author_or_channel,
            "collected_at": utc_now(),
            "published_at": published_at,
            "raw_file": raw_file,
            "processed_file": processed_file,
            "confidence": confidence,
            "is_mock": is_mock,
            "notes": notes,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(reference, ensure_ascii=False) + "\n")
        return reference

    def update_raw_files(self, raw_files: dict[str, str]) -> None:
        self._update_files(raw_files, "raw_file")

    def update_processed_files(self, processed_files: dict[str, str]) -> None:
        self._update_files(processed_files, "processed_file")

    def _update_files(self, updates: dict[str, str], field: str) -> None:
        if not updates:
            return
        references = self.read_all()
        for reference in references:
            if reference["id"] in updates:
                reference[field] = updates[reference["id"]]
        self.path.write_text("".join(json.dumps(reference, ensure_ascii=False) + "\n" for reference in references), encoding="utf-8")

    def validate_reference(self, reference: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        for field in ["id", "source", "source_type", "query", "collected_at", "raw_file"]:
            if not reference.get(field):
                errors.append(f"reference missing {field}")
        url = str(reference.get("url", ""))
        if not url:
            errors.append("reference missing url")
        if url.startswith("mock://") and not reference.get("is_mock"):
            errors.append("mock URL must set is_mock true")
        if url.startswith("mock://") and "mock" not in str(reference.get("notes", "")).lower():
            errors.append("mock URL must be labeled mock in notes")
        return errors
