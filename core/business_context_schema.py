from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.schema import ValidationError, load_yaml, require_mapping

REQUIRED_SECTIONS = ["expert", "market", "customer", "offer", "business", "acquisition", "sales", "delivery", "retention", "constraints", "metrics", "notes"]


@dataclass(frozen=True)
class BusinessContext:
    data: dict[str, Any]

    @classmethod
    def load(cls, path: Path) -> "BusinessContext":
        return cls.from_dict(load_yaml(path))

    @classmethod
    def from_dict(cls, data: Any) -> "BusinessContext":
        mapping = require_mapping(data, "business_context")
        missing = [section for section in REQUIRED_SECTIONS if section not in mapping]
        if missing:
            raise ValidationError("Missing business context sections: " + ", ".join(missing))
        return cls(mapping)

    def get(self, section: str, key: str, default: Any = "") -> Any:
        value = self.data.get(section, {})
        return value.get(key, default) if isinstance(value, dict) else default

    def has_value(self, section: str, key: str) -> bool:
        return self.get(section, key) not in ("", None, [], {})
