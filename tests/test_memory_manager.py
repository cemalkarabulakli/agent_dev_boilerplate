import pytest
from core.schema import MemoryEntry, ValidationError, utc_now

def test_memory_entries_include_status_and_confidence() -> None:
    now = utc_now()
    entry = MemoryEntry("mem_001", "offer", "Offer fact", "user", 0.8, now, now, "candidate")
    entry.validate()
    assert entry.to_dict()["status"] == "candidate"
    assert entry.to_dict()["confidence"] == 0.8

def test_memory_entry_rejects_invalid_status() -> None:
    now = utc_now()
    entry = MemoryEntry("mem_001", "offer", "Offer fact", "user", 0.8, now, now, "pending")
    with pytest.raises(ValidationError):
        entry.validate()
