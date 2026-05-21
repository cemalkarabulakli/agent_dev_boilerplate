"""File-based memory management."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.schema import MemoryEntry, ValidationError, utc_now


class MemoryManager:
    def __init__(self, agent_dir: Path):
        self.agent_dir = agent_dir
        self.memory_dir = agent_dir / "memory"
        self.raw_history_path = self.memory_dir / "raw_history.jsonl"
        self.session_notes_path = self.memory_dir / "session_notes.md"
        self.long_term_memory_path = self.memory_dir / "long_term_memory.json"
        self.compacted_context_path = self.memory_dir / "compacted_context.md"

    def ensure_files(self) -> None:
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        if not self.raw_history_path.exists():
            self.raw_history_path.write_text("", encoding="utf-8")
        if not self.session_notes_path.exists():
            self.session_notes_path.write_text("# Session Notes\n\n", encoding="utf-8")
        if not self.long_term_memory_path.exists():
            self.long_term_memory_path.write_text("[]\n", encoding="utf-8")
        if not self.compacted_context_path.exists():
            self.compacted_context_path.write_text("# Compacted Context\n\nNo context compacted yet.\n", encoding="utf-8")

    def append_raw_history(self, role: str, content: str, metadata: dict[str, Any] | None = None) -> None:
        self.ensure_files()
        record = {
            "created_at": utc_now(),
            "role": role,
            "content": content,
            "metadata": metadata or {},
        }
        with self.raw_history_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")

    def read_raw_history(self) -> list[dict[str, Any]]:
        self.ensure_files()
        records: list[dict[str, Any]] = []
        for line in self.raw_history_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            records.append(json.loads(line))
        return records

    def load_long_term_memory(self) -> list[MemoryEntry]:
        self.ensure_files()
        raw = json.loads(self.long_term_memory_path.read_text(encoding="utf-8") or "[]")
        if not isinstance(raw, list):
            raise ValidationError("long_term_memory.json must contain a list")
        return [MemoryEntry.from_dict(item) for item in raw]

    def write_long_term_memory(self, entries: list[MemoryEntry]) -> None:
        self.ensure_files()
        data = [entry.to_dict() for entry in entries]
        self.long_term_memory_path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    def add_memory_entry(self, entry: MemoryEntry) -> None:
        entries = self.load_long_term_memory()
        entries.append(entry)
        self.write_long_term_memory(entries)

    def save_candidate_memory(self, text: str, source: str, memory_type: str = "observation", confidence: float = 0.5) -> MemoryEntry:
        entry = MemoryEntry.candidate(text=text, source=source, memory_type=memory_type, confidence=confidence)
        self.add_memory_entry(entry)
        return entry

    def load_session_notes(self) -> str:
        self.ensure_files()
        return self.session_notes_path.read_text(encoding="utf-8")

    def append_session_note(self, text: str) -> None:
        self.ensure_files()
        with self.session_notes_path.open("a", encoding="utf-8") as handle:
            handle.write(f"\n- {utc_now()}: {text}\n")

    def load_compacted_context(self) -> str:
        self.ensure_files()
        return self.compacted_context_path.read_text(encoding="utf-8")

    def write_compacted_context(self, content: str) -> None:
        self.ensure_files()
        self.compacted_context_path.write_text(content, encoding="utf-8")
