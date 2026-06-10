from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.schema import utc_now


def build_reference(
    result: dict[str, Any],
    *,
    source_type: str = "search_result",
    query_or_input: str = "",
    confidence: float = 0.0,
) -> dict[str, Any]:
    url = str(result.get("url") or "")
    title = str(result.get("title") or "") or url
    provider = str(result.get("provider") or "unknown")
    is_mock = bool(result.get("is_mock") or result.get("isMock"))
    retrieved_at = str(result.get("retrieved_at") or result.get("retrievedAt") or utc_now())

    ref_id = _make_id(provider)

    return {
        "id": ref_id,
        "provider": provider,
        "source_type": source_type,
        "query_or_input": query_or_input,
        "title": title,
        "url": url,
        "retrieved_at": retrieved_at,
        "raw_file": "",
        "processed_file": "",
        "is_mock": is_mock,
        "confidence": confidence,
    }


def save_reference(
    reference: dict[str, Any],
    path: Path | None = None,
    root: Path | None = None,
) -> Path:
    if path is None:
        base = root or Path.cwd()
        path = base / "research" / "index" / "collected_references.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(reference, ensure_ascii=False) + "\n")
    return path


def build_and_save_references(
    results: list[dict[str, Any]],
    *,
    source_type: str = "search_result",
    query_or_input: str = "",
    path: Path | None = None,
    root: Path | None = None,
) -> list[dict[str, Any]]:
    refs = [build_reference(r, source_type=source_type, query_or_input=query_or_input) for r in results]
    for ref in refs:
        save_reference(ref, path=path, root=root)
    return refs


def _make_id(provider: str) -> str:
    ts = utc_now().replace(":", "").replace("-", "").replace("T", "_").replace("Z", "")
    import random
    suffix = f"{random.randint(0, 9999):04d}"
    return f"web_ref_{provider}_{ts}_{suffix}"
