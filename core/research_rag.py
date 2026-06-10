"""
Lightweight BM25 search index over collected_references.jsonl.

Uses SQLite FTS5 (stdlib, zero deps). Syncs automatically when the JSONL
changes. No embedding API needed.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

_JSONL = Path("research/index/collected_references.jsonl")
_DB = Path("research/index/research_index.sqlite")


class ResearchIndex:
    def __init__(self, root: Path):
        self.root = root
        self.jsonl = root / _JSONL
        self.db_path = root / _DB

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def sync(self) -> int:
        """Rebuild FTS index from JSONL if the file changed. Returns record count."""
        if not self.jsonl.exists():
            return 0
        mtime = str(self.jsonl.stat().st_mtime)
        with self._connect() as conn:
            self._ensure_schema(conn)
            if self._last_mtime(conn) == mtime:
                return self._row_count(conn)
            records = self._load_jsonl()
            conn.execute("DELETE FROM refs")
            conn.executemany(
                "INSERT INTO refs(id, title, query_text, url, source_type, notes) VALUES (?,?,?,?,?,?)",
                [self._to_row(r) for r in records],
            )
            conn.execute(
                "INSERT OR REPLACE INTO _meta(key, value) VALUES ('mtime', ?)", (mtime,)
            )
        return len(records)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """BM25-ranked keyword search. Returns matching reference dicts."""
        self.sync()
        all_refs = {r.get("id", ""): r for r in self._load_jsonl()}
        with self._connect() as conn:
            self._ensure_schema(conn)
            try:
                rows = conn.execute(
                    "SELECT id, rank FROM refs WHERE refs MATCH ? ORDER BY rank LIMIT ?",
                    (self._escape(query), top_k),
                ).fetchall()
            except sqlite3.OperationalError:
                return []
        results = []
        for ref_id, rank in rows:
            ref = dict(all_refs.get(ref_id, {"id": ref_id}))
            ref["_bm25_score"] = round(-rank, 4)
            results.append(ref)
        return results

    def stats(self) -> dict[str, Any]:
        """Return index stats without triggering a sync."""
        if not self.db_path.exists():
            return {"indexed": 0, "jsonl_lines": self._jsonl_line_count(), "synced": False}
        with self._connect() as conn:
            self._ensure_schema(conn)
            return {
                "indexed": self._row_count(conn),
                "jsonl_lines": self._jsonl_line_count(),
                "last_mtime": self._last_mtime(conn),
                "synced": self._last_mtime(conn) == self._jsonl_mtime(),
            }

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = lambda cur, row: row
        return conn

    def _ensure_schema(self, conn: sqlite3.Connection) -> None:
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS refs USING fts5(
                id UNINDEXED,
                title,
                query_text,
                url UNINDEXED,
                source_type UNINDEXED,
                notes,
                tokenize = 'porter unicode61'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS _meta (key TEXT PRIMARY KEY, value TEXT)
        """)

    def _load_jsonl(self) -> list[dict[str, Any]]:
        if not self.jsonl.exists():
            return []
        out = []
        for line in self.jsonl.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
        return out

    def _to_row(self, r: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
        return (
            str(r.get("id") or ""),
            str(r.get("title") or ""),
            str(r.get("query") or r.get("query_or_input") or ""),
            str(r.get("url") or ""),
            str(r.get("source_type") or ""),
            str(r.get("notes") or ""),
        )

    def _last_mtime(self, conn: sqlite3.Connection) -> str:
        row = conn.execute("SELECT value FROM _meta WHERE key='mtime'").fetchone()
        return row[0] if row else ""

    def _row_count(self, conn: sqlite3.Connection) -> int:
        row = conn.execute("SELECT COUNT(*) FROM refs").fetchone()
        return row[0] if row else 0

    def _jsonl_line_count(self) -> int:
        if not self.jsonl.exists():
            return 0
        return sum(1 for l in self.jsonl.read_text(encoding="utf-8").splitlines() if l.strip())

    def _jsonl_mtime(self) -> str:
        if not self.jsonl.exists():
            return ""
        return str(self.jsonl.stat().st_mtime)

    @staticmethod
    def _escape(query: str) -> str:
        # Wrap bare terms so FTS5 doesn't choke on special chars
        safe = query.replace('"', '""')
        return f'"{safe}"'
