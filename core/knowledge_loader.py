"""Local file-based knowledge loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from core.schema import KnowledgeSource, ValidationError
from core.yaml_utils import load_yaml


@dataclass(frozen=True)
class KnowledgeDocument:
    path: Path
    source_id: str
    text: str


class KnowledgeBase:
    def __init__(self, agent_dir: Path, sources_file: str = "knowledge/sources.yaml"):
        self.agent_dir = agent_dir
        self.knowledge_dir = agent_dir / "knowledge"
        self.sources_path = agent_dir / sources_file
        self.processed_dir = self.knowledge_dir / "processed"

    def load_sources(self) -> list[KnowledgeSource]:
        if not self.sources_path.exists():
            raise FileNotFoundError(f"Missing knowledge sources file: {self.sources_path}")
        data = load_yaml(self.sources_path)
        raw_sources = data.get("sources", []) if isinstance(data, dict) else []
        if not isinstance(raw_sources, list):
            raise ValidationError("knowledge/sources.yaml must contain a sources list")
        return [KnowledgeSource.from_dict(item) for item in raw_sources]

    def sources_by_type(self) -> dict[str, list[KnowledgeSource]]:
        grouped: dict[str, list[KnowledgeSource]] = {}
        for source in self.load_sources():
            grouped.setdefault(source.type, []).append(source)
        return grouped

    def load_processed_documents(self) -> list[KnowledgeDocument]:
        if not self.processed_dir.exists():
            return []
        source_ids = {source.id for source in self.load_sources()}
        documents: list[KnowledgeDocument] = []
        for path in sorted(self.processed_dir.glob("*")):
            if path.is_dir() or path.name == "index.json" or path.suffix.lower() not in {".md", ".txt"}:
                continue
            source_id = path.stem.split("__", 1)[0]
            if source_id not in source_ids:
                source_id = "unsourced"
            documents.append(KnowledgeDocument(path=path, source_id=source_id, text=path.read_text(encoding="utf-8")))
        return documents

    def search(self, query: str, limit: int = 5) -> list[KnowledgeDocument]:
        terms = [term.lower() for term in query.split() if len(term) > 2]
        if not terms:
            return []
        scored: list[tuple[int, KnowledgeDocument]] = []
        for document in self.load_processed_documents():
            haystack = document.text.lower()
            score = sum(haystack.count(term) for term in terms)
            if score > 0:
                scored.append((score, document))
        return [document for _, document in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]

    def factuality_note(self) -> str:
        sources = self.load_sources()
        if not sources:
            return "No knowledge sources are configured. Treat claims as recommendations or assumptions."
        return "Factual claims must cite source IDs: " + ", ".join(source.id for source in sources)
