from __future__ import annotations

import pytest

from core.schema import MemoryEntry, ValidationError, utc_now


def test_memory_entry_requires_status_and_confidence() -> None:
    now = utc_now()
    entry = MemoryEntry(
        id="mem_test",
        type="preference",
        text="User prefers local-first storage.",
        source="test",
        confidence=0.8,
        created_at=now,
        updated_at=now,
        status="candidate",
    )
    entry.validate()
    assert entry.to_dict()["status"] == "candidate"
    assert entry.to_dict()["confidence"] == 0.8


def test_memory_entry_rejects_invalid_status() -> None:
    now = utc_now()
    entry = MemoryEntry(
        id="mem_test",
        type="preference",
        text="Invalid status example.",
        source="test",
        confidence=0.8,
        created_at=now,
        updated_at=now,
        status="pending",  # type: ignore[arg-type]
    )
    with pytest.raises(ValidationError):
        entry.validate()
