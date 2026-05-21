from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


class ValidationError(ValueError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_yaml(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be a mapping")
    return value


def require_string(mapping: dict[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str):
        raise ValidationError(f"{key} must be a string")
    return value


def require_bool(mapping: dict[str, Any], key: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise ValidationError(f"{key} must be a boolean")
    return value


def require_int(mapping: dict[str, Any], key: str, minimum: int = 0) -> int:
    value = mapping.get(key)
    if not isinstance(value, int) or value < minimum:
        raise ValidationError(f"{key} must be an integer >= {minimum}")
    return value


def require_number(mapping: dict[str, Any], key: str) -> float:
    value = mapping.get(key)
    if not isinstance(value, (int, float)):
        raise ValidationError(f"{key} must be a number")
    return float(value)


def require_string_list(mapping: dict[str, Any], key: str) -> list[str]:
    value = mapping.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValidationError(f"{key} must be a list of strings")
    return value


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    name: str
    temperature: float

    @classmethod
    def from_dict(cls, data: Any) -> "ModelConfig":
        m = require_mapping(data, "model")
        return cls(require_string(m, "provider"), require_string(m, "name"), require_number(m, "temperature"))


@dataclass(frozen=True)
class ContextConfig:
    keep_last_n_turns: int
    compact_when_tokens_exceed: int
    tool_output_trim_chars: int

    @classmethod
    def from_dict(cls, data: Any) -> "ContextConfig":
        m = require_mapping(data, "context")
        return cls(require_int(m, "keep_last_n_turns", 1), require_int(m, "compact_when_tokens_exceed", 1000), require_int(m, "tool_output_trim_chars", 100))


@dataclass(frozen=True)
class MemoryConfig:
    mode: str
    allow_learning: bool
    require_memory_review: bool

    @classmethod
    def from_dict(cls, data: Any) -> "MemoryConfig":
        m = require_mapping(data, "memory")
        mode = require_string(m, "mode")
        if mode != "file":
            raise ValidationError("memory.mode must be file")
        return cls(mode, require_bool(m, "allow_learning"), require_bool(m, "require_memory_review"))


@dataclass(frozen=True)
class AgentConfig:
    name: str
    role: str
    description: str
    version: str
    model: ModelConfig
    context: ContextConfig
    memory: MemoryConfig
    knowledge: dict[str, Any]
    tools: dict[str, Any]
    guardrails: dict[str, list[str]]
    output: dict[str, str]

    @classmethod
    def from_dict(cls, data: Any) -> "AgentConfig":
        m = require_mapping(data, "agent")
        return cls(
            require_string(m, "name"),
            require_string(m, "role"),
            require_string(m, "description"),
            require_string(m, "version"),
            ModelConfig.from_dict(m.get("model")),
            ContextConfig.from_dict(m.get("context")),
            MemoryConfig.from_dict(m.get("memory")),
            require_mapping(m.get("knowledge"), "knowledge"),
            require_mapping(m.get("tools"), "tools"),
            require_mapping(m.get("guardrails"), "guardrails"),
            require_mapping(m.get("output"), "output"),
        )


@dataclass
class MemoryEntry:
    id: str
    type: str
    text: str
    source: str
    confidence: float
    created_at: str
    updated_at: str
    status: str

    @classmethod
    def candidate(cls, text: str, memory_type: str = "assumption", source: str = "agent", confidence: float = 0.5) -> "MemoryEntry":
        now = utc_now()
        return cls(f"mem_{uuid4().hex[:12]}", memory_type, text, source, confidence, now, now, "candidate")

    @classmethod
    def from_dict(cls, data: Any) -> "MemoryEntry":
        m = require_mapping(data, "memory entry")
        entry = cls(require_string(m, "id"), require_string(m, "type"), require_string(m, "text"), require_string(m, "source"), float(m.get("confidence")), require_string(m, "created_at"), require_string(m, "updated_at"), require_string(m, "status"))
        entry.validate()
        return entry

    def validate(self) -> None:
        if self.type not in {"market", "avatar", "offer", "pricing", "guarantee", "acquisition", "funnel", "sales", "delivery", "proof", "retention", "decision", "constraint", "metric", "assumption"}:
            raise ValidationError("invalid memory type")
        if self.status not in {"candidate", "accepted", "rejected"}:
            raise ValidationError("invalid memory status")
        if self.source not in {"user", "agent", "tool", "business_context"}:
            raise ValidationError("invalid memory source")
        if not 0 <= self.confidence <= 1:
            raise ValidationError("confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return self.__dict__.copy()


@dataclass(frozen=True)
class ChecklistItem:
    id: str
    category: str
    description: str
    severity: str = "warning"
    check: str = "documented"

    @classmethod
    def from_dict(cls, data: Any) -> "ChecklistItem":
        m = require_mapping(data, "checklist item")
        return cls(require_string(m, "id"), require_string(m, "category"), require_string(m, "description"), str(m.get("severity") or "warning"), str(m.get("check") or "documented"))


@dataclass(frozen=True)
class EvalCase:
    id: str
    input: str
    required_sections: list[str] = field(default_factory=list)
    forbidden_terms: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Any) -> "EvalCase":
        m = require_mapping(data, "eval case")
        return cls(require_string(m, "id"), require_string(m, "input"), require_string_list(m, "required_sections") if "required_sections" in m else [], require_string_list(m, "forbidden_terms") if "forbidden_terms" in m else [])
