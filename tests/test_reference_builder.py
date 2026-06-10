import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.web.reference_builder import build_reference, save_reference, build_and_save_references


def test_build_reference_required_fields() -> None:
    result = {"url": "https://example.com", "title": "Example", "provider": "tavily", "is_mock": False}
    ref = build_reference(result, source_type="search_result", query_or_input="test query")
    assert "id" in ref
    assert ref["url"] == "https://example.com"
    assert ref["title"] == "Example"
    assert ref["provider"] == "tavily"
    assert "retrieved_at" in ref
    assert ref["is_mock"] is False
    assert ref["source_type"] == "search_result"
    assert ref["query_or_input"] == "test query"


def test_build_reference_uses_url_as_title_when_missing() -> None:
    result = {"url": "https://example.com/page", "provider": "mock"}
    ref = build_reference(result)
    assert ref["title"] == "https://example.com/page"


def test_build_reference_id_is_unique() -> None:
    result = {"url": "https://example.com", "title": "Example", "provider": "mock"}
    ref1 = build_reference(result)
    ref2 = build_reference(result)
    assert ref1["id"] != ref2["id"], "Reference IDs must be unique"


def test_save_reference_writes_jsonl() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        result = {"url": "https://example.com", "title": "Test", "provider": "tavily", "is_mock": False}
        ref = build_reference(result, source_type="search_result", query_or_input="test")
        path = Path(tmpdir) / "refs.jsonl"
        save_reference(ref, path=path)
        assert path.exists()
        lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        assert len(lines) == 1
        saved = json.loads(lines[0])
        assert saved["url"] == "https://example.com"
        assert saved["id"] == ref["id"]


def test_save_reference_appends_multiple() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "refs.jsonl"
        for i in range(3):
            result = {"url": f"https://example.com/{i}", "title": f"Page {i}", "provider": "mock", "is_mock": True}
            ref = build_reference(result)
            save_reference(ref, path=path)
        lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        assert len(lines) == 3


def test_build_and_save_references_batch() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        results = [
            {"url": f"https://example.com/{i}", "title": f"Page {i}", "provider": "tavily", "is_mock": False}
            for i in range(3)
        ]
        path = Path(tmpdir) / "batch_refs.jsonl"
        refs = build_and_save_references(results, source_type="web_search", query_or_input="batch query", path=path)
        assert len(refs) == 3
        lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        assert len(lines) == 3
        for ref in refs:
            assert ref["source_type"] == "web_search"
            assert ref["query_or_input"] == "batch query"


def test_no_api_keys_hardcoded_in_reference_builder() -> None:
    import re
    text = (ROOT / "core" / "web" / "reference_builder.py").read_text(encoding="utf-8")
    hardcoded = re.findall(r'["\'][a-zA-Z0-9_\-]{32,}["\']', text)
    assert not hardcoded, f"reference_builder.py may have hardcoded secrets: {hardcoded}"
