from __future__ import annotations

from pathlib import Path

import pytest

from core.knowledge_loader import KnowledgeBase
from core.schema import ValidationError


def test_knowledge_sources_reject_invalid_missing_required_fields(tmp_path: Path) -> None:
    agent_dir = tmp_path / "agent"
    source_dir = agent_dir / "knowledge"
    source_dir.mkdir(parents=True)
    (source_dir / "sources.yaml").write_text(
        "sources:\n"
        "  - id: bad_source\n"
        "    title: \"Bad Source\"\n"
        "    type: \"official_docs\"\n"
        "    status: \"active\"\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError):
        KnowledgeBase(agent_dir).load_sources()


def test_knowledge_sources_reject_example_url_when_not_placeholder(tmp_path: Path) -> None:
    agent_dir = tmp_path / "agent"
    source_dir = agent_dir / "knowledge"
    source_dir.mkdir(parents=True)
    (source_dir / "sources.yaml").write_text(
        "sources:\n"
        "  - id: fake_source\n"
        "    title: \"Fake Source\"\n"
        "    type: \"official_docs\"\n"
        "    url: \"https://example.com/fake\"\n"
        "    status: \"active\"\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError):
        KnowledgeBase(agent_dir).load_sources()
