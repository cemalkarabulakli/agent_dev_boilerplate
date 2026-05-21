from pathlib import Path

from core.reference_manager import ReferenceManager


def test_reference_manager_validates_mock_reference_after_raw_file_update(tmp_path: Path) -> None:
    manager = ReferenceManager(tmp_path)
    reference = manager.create_reference(
        source="reddit",
        source_type="community",
        query="coaches struggling to get clients",
        title="Mock source",
        url="mock://reddit/item-001",
        raw_file="research/sources/reddit/raw/mock.json",
        confidence=0.55,
        notes="Mock mode reference.",
    )

    assert manager.validate_reference(reference) == []
    assert manager.read_all()[0]["id"] == reference["id"]
