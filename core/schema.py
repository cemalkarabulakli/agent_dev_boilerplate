"""Validation models for agents, memory, knowledge, checklists, and evals."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4


class ValidationError(ValueError):
    """Raised when repository configuration is invalid."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def require_mapping(data: Any, label: str) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValidationError(f"{label} must be a mapping")
    return data


def require_list(data: Any, label: str) -> list[Any]:
    if not isinstance(data, list):
        raise ValidationError(f"{label} must be a list")
    return data


def require_str(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{key} must be a non-empty string")
    return value


def require_bool(data: dict[str, Any], key: str) -> bool:
    value = data.get(key)
    if not isinstance(value, bool):
        raise ValidationError(f"{key} must be a boolean")
    return value


def require_int(data: dict[str, Any], key: str, minimum: int = 0) -> int:
    value = data.get(key)
    if not isinstance(value, int) or value < minimum:
        raise ValidationError(f"{key} must be an integer >= {minimum}")
    return value


def require_str_list(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValidationError(f"{key} must be a list of non-empty strings")
    return value


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    name: str

    @classmethod
    def from_dict(cls, data: Any) -> "ModelConfig":
        mapping = require_mapping(data, "model")
        return cls(provider=require_str(mapping, "provider"), name=require_str(mapping, "name"))


@dataclass(frozen=True)
class ContextConfig:
    keep_last_n_turns: int
    compact_when_tokens_exceed: int
    tool_output_trim_chars: int

    @classmethod
    def from_dict(cls, data: Any) -> "ContextConfig":
        mapping = require_mapping(data, "context")
        return cls(
            keep_last_n_turns=require_int(mapping, "keep_last_n_turns", 1),
            compact_when_tokens_exceed=require_int(mapping, "compact_when_tokens_exceed", 1000),
            tool_output_trim_chars=require_int(mapping, "tool_output_trim_chars", 100),
        )


@dataclass(frozen=True)
class MemoryConfig:
    mode: str
    allow_learning: bool
    require_memory_review: bool

    @classmethod
    def from_dict(cls, data: Any) -> "MemoryConfig":
        mapping = require_mapping(data, "memory")
        mode = require_str(mapping, "mode")
        if mode != "file":
            raise ValidationError("memory.mode must be 'file' in v1")
        return cls(
            mode=mode,
            allow_learning=require_bool(mapping, "allow_learning"),
            require_memory_review=require_bool(mapping, "require_memory_review"),
        )


@dataclass(frozen=True)
class KnowledgeConfig:
    sources_file: str
    require_source_citations: bool

    @classmethod
    def from_dict(cls, data: Any) -> "KnowledgeConfig":
        mapping = require_mapping(data, "knowledge")
        return cls(
            sources_file=require_str(mapping, "sources_file"),
            require_source_citations=require_bool(mapping, "require_source_citations"),
        )


@dataclass(frozen=True)
class ToolsConfig:
    allowed: list[str]

    @classmethod
    def from_dict(cls, data: Any) -> "ToolsConfig":
        mapping = require_mapping(data, "tools")
        return cls(allowed=require_str_list(mapping, "allowed"))


@dataclass(frozen=True)
class GuardrailsConfig:
    input: list[str]
    output: list[str]

    @classmethod
    def from_dict(cls, data: Any) -> "GuardrailsConfig":
        mapping = require_mapping(data, "guardrails")
        return cls(input=require_str_list(mapping, "input"), output=require_str_list(mapping, "output"))


@dataclass(frozen=True)
class AgentConfig:
    name: str
    role: str
    description: str
    version: str
    model: ModelConfig
    context: ContextConfig
    memory: MemoryConfig
    knowledge: KnowledgeConfig
    tools: ToolsConfig
    guardrails: GuardrailsConfig

    @classmethod
    def from_dict(cls, data: Any) -> "AgentConfig":
        mapping = require_mapping(data, "agent config")
        return cls(
            name=require_str(mapping, "name"),
            role=require_str(mapping, "role"),
            description=require_str(mapping, "description"),
            version=require_str(mapping, "version"),
            model=ModelConfig.from_dict(mapping.get("model")),
            context=ContextConfig.from_dict(mapping.get("context")),
            memory=MemoryConfig.from_dict(mapping.get("memory")),
            knowledge=KnowledgeConfig.from_dict(mapping.get("knowledge")),
            tools=ToolsConfig.from_dict(mapping.get("tools")),
            guardrails=GuardrailsConfig.from_dict(mapping.get("guardrails")),
        )


MemoryStatus = Literal["candidate", "accepted", "rejected"]


@dataclass
class MemoryEntry:
    id: str
    type: str
    text: str
    source: str
    confidence: float
    created_at: str
    updated_at: str
    status: MemoryStatus

    @classmethod
    def candidate(cls, text: str, source: str, memory_type: str = "observation", confidence: float = 0.5) -> "MemoryEntry":
        now = utc_now()
        return cls(
            id=f"mem_{uuid4().hex[:12]}",
            type=memory_type,
            text=text,
            source=source,
            confidence=confidence,
            created_at=now,
            updated_at=now,
            status="candidate",
        )

    @classmethod
    def from_dict(cls, data: Any) -> "MemoryEntry":
        mapping = require_mapping(data, "memory entry")
        entry = cls(
            id=require_str(mapping, "id"),
            type=require_str(mapping, "type"),
            text=require_str(mapping, "text"),
            source=require_str(mapping, "source"),
            confidence=float(mapping.get("confidence")),
            created_at=require_str(mapping, "created_at"),
            updated_at=require_str(mapping, "updated_at"),
            status=mapping.get("status"),
        )
        entry.validate()
        return entry

    def validate(self) -> None:
        if not 0 <= self.confidence <= 1:
            raise ValidationError("memory confidence must be between 0 and 1")
        if self.status not in ("candidate", "accepted", "rejected"):
            raise ValidationError("memory status must be candidate, accepted, or rejected")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "id": self.id,
            "type": self.type,
            "text": self.text,
            "source": self.source,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
        }


@dataclass(frozen=True)
class KnowledgeSource:
    id: str
    title: str
    type: str
    url: str
    status: str
    notes: str = ""

    @classmethod
    def from_dict(cls, data: Any) -> "KnowledgeSource":
        mapping = require_mapping(data, "knowledge source")
        source = cls(
            id=require_str(mapping, "id"),
            title=require_str(mapping, "title"),
            type=require_str(mapping, "type"),
            url=require_str(mapping, "url"),
            status=require_str(mapping, "status"),
            notes=str(mapping.get("notes") or ""),
        )
        source.validate()
        return source

    def validate(self) -> None:
        allowed_types = {"official_docs", "official", "internal", "user_provided"}
        if self.type not in allowed_types:
            raise ValidationError(f"knowledge source {self.id} has unsupported type {self.type}")
        if not self.url.startswith(("https://", "file://", "internal://")):
            raise ValidationError(f"knowledge source {self.id} must use https://, file://, or internal://")
        if "example.com" in self.url and self.status != "placeholder":
            raise ValidationError(f"knowledge source {self.id} uses an example URL without placeholder status")


@dataclass(frozen=True)
class ChecklistItem:
    id: str
    category: str
    description: str
    severity: str = "warning"
    check: str = ""

    @classmethod
    def from_dict(cls, data: Any) -> "ChecklistItem":
        mapping = require_mapping(data, "checklist item")
        severity = str(mapping.get("severity") or "warning")
        if severity not in ("critical", "warning", "info"):
            raise ValidationError("checklist severity must be critical, warning, or info")
        return cls(
            id=require_str(mapping, "id"),
            category=require_str(mapping, "category"),
            description=require_str(mapping, "description"),
            severity=severity,
            check=str(mapping.get("check") or ""),
        )


@dataclass(frozen=True)
class EvalCase:
    id: str
    input: str
    expected_behavior: list[str]
    required_terms: list[str] = field(default_factory=list)
    forbidden_terms: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Any) -> "EvalCase":
        mapping = require_mapping(data, "eval case")
        return cls(
            id=require_str(mapping, "id"),
            input=require_str(mapping, "input"),
            expected_behavior=require_str_list(mapping, "expected_behavior"),
            required_terms=require_str_list(mapping, "required_terms") if "required_terms" in mapping else [],
            forbidden_terms=require_str_list(mapping, "forbidden_terms") if "forbidden_terms" in mapping else [],
        )


@dataclass
class CheckResult:
    id: str
    category: str
    description: str
    severity: str
    passed: bool
    message: str


@dataclass
class ValidationReport:
    passed: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def fail(self, message: str) -> None:
        self.passed = False
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)
