"""Safe local tool registry."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from core.agent_loader import load_agent_config
from core.context_compactor import compact_context
from core.guardrails import validate_tool_execution
from core.knowledge_loader import KnowledgeBase
from core.memory_manager import MemoryManager


ToolFn = Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolFn] = {}

    def register(self, name: str, fn: ToolFn) -> None:
        self._tools[name] = fn

    def names(self) -> list[str]:
        return sorted(self._tools)

    def run(self, name: str, agent_name: str, root: Path, **kwargs: Any) -> Any:
        config = load_agent_config(agent_name, root)
        errors = validate_tool_execution(name, config)
        if errors:
            raise PermissionError("; ".join(errors))
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name](agent_name=agent_name, root=root, **kwargs)


def default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("read_knowledge", read_knowledge)
    registry.register("save_memory_note", save_memory_note)
    registry.register("compact_context", compact_context_tool)
    return registry


def read_knowledge(agent_name: str, root: Path, query: str) -> list[dict[str, str]]:
    config = load_agent_config(agent_name, root)
    kb = KnowledgeBase(root / "agents" / agent_name, config.knowledge.sources_file)
    return [
        {"path": str(document.path), "source_id": document.source_id, "text": document.text[:1000]}
        for document in kb.search(query)
    ]


def save_memory_note(agent_name: str, root: Path, text: str) -> str:
    manager = MemoryManager(root / "agents" / agent_name)
    manager.append_session_note(text)
    return "saved"


def compact_context_tool(agent_name: str, root: Path) -> str:
    config = load_agent_config(agent_name, root)
    manager = MemoryManager(root / "agents" / agent_name)
    result = compact_context(
        config=config,
        history=manager.read_raw_history(),
        session_notes=manager.load_session_notes(),
        long_term_memory=manager.load_long_term_memory(),
    )
    manager.write_compacted_context(result.markdown)
    return "compacted"
