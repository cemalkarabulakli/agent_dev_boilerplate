from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from core.reference_manager import ReferenceManager
from core.schema import load_yaml, utc_now


@dataclass
class RawSignal:
    id: str
    source: str
    query: str
    title: str
    url: str
    snippet: str
    collected_at: str
    reference_id: str
    raw_file: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcessedSignal:
    id: str
    source: str
    signal_type: str
    query: str
    insight: str
    confidence: float
    reference_ids: list[str]
    processed_file: str = ""
    status: str = "candidate"
    language: str = "unknown"
    tags: list[str] = field(default_factory=list)


class BaseSourceAdapter:
    source_id = "base"
    source_type = "generic"
    signal_kind = "market_signal"
    language = "en"

    def __init__(self, root: Path, source_config: dict[str, Any], registry_entry: dict[str, Any]):
        self.root = root
        self.config = source_config
        self.registry_entry = registry_entry
        self.source_id = str(source_config.get("id") or self.source_id)
        self.mode = str(source_config.get("mode") or "mock")
        self.raw_dir = root / str(registry_entry["raw_dir"])
        self.processed_dir = root / str(registry_entry["processed_dir"])
        self.reports_dir = root / str(registry_entry["reports_dir"])
        self.reference_manager = ReferenceManager(root)

    @classmethod
    def from_source_id(cls, root: Path, source_id: str, registry_entry: dict[str, Any]) -> "BaseSourceAdapter":
        config = load_yaml(root / "research" / "sources" / source_id / "source_config.yaml")
        return cls(root, config, registry_entry)

    def collect(self, queries: list[str], limit: int) -> list[RawSignal]:
        signals: list[RawSignal] = []
        for query in queries:
            for index in range(min(limit, 2)):
                signal_id = f"{self.source_id}_{len(signals) + 1:03d}"
                url = f"mock://{self.source_id}/{signal_id}"
                reference = self.reference_manager.create_reference(
                    source=self.source_id,
                    source_type=self.source_type,
                    query=query,
                    title=f"Mock {self.registry_entry.get('name', self.source_id)} signal {index + 1}",
                    url=url,
                    author_or_channel="mock",
                    raw_file="",
                    processed_file="",
                    confidence=0.45,
                    notes="Mock mode reference. Replace with API/scrape/manual data when configured.",
                )
                signals.append(
                    RawSignal(
                        id=signal_id,
                        source=self.source_id,
                        query=query,
                        title=reference["title"],
                        url=url,
                        snippet=self.mock_snippet(query, index),
                        collected_at=reference["collected_at"],
                        reference_id=reference["id"],
                        metadata={"mode": self.mode, "mock": self.mode == "mock", "source_type": self.source_type},
                    )
                )
        return signals

    def mock_snippet(self, query: str, index: int) -> str:
        return (
            f"Mock {self.source_id} signal for '{query}'. "
            "Potential market pain, objection, desired outcome, tool mention, offer pattern, or content angle. "
            f"Variant {index + 1}."
        )

    def save_raw(self, signals: list[RawSignal]) -> Path:
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        path = self.raw_dir / f"{self.source_id}_{utc_now().replace(':', '').replace('-', '')}_raw.json"
        for signal in signals:
            signal.raw_file = str(path.relative_to(self.root))
        path.write_text(json.dumps([asdict(signal) for signal in signals], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        self.reference_manager.update_raw_files({signal.reference_id: signal.raw_file for signal in signals})
        return path

    def process(self, signals: list[RawSignal]) -> list[ProcessedSignal]:
        processed: list[ProcessedSignal] = []
        for signal in signals:
            processed.append(
                ProcessedSignal(
                    id=f"sig_{signal.id}",
                    source=self.source_id,
                    signal_type=self.signal_kind,
                    query=signal.query,
                    insight=self.extract_insight(signal),
                    confidence=0.55 if signal.metadata.get("mock") else 0.7,
                    reference_ids=[signal.reference_id],
                    status="candidate",
                    language=self.language,
                    tags=self.default_tags(),
                )
            )
        return processed

    def extract_insight(self, signal: RawSignal) -> str:
        return f"Candidate {self.signal_kind} from {self.source_id}: {signal.snippet}"

    def default_tags(self) -> list[str]:
        return ["pain_points", "objections", "desired_outcomes", "offer_patterns"]

    def save_processed(self, signals: list[ProcessedSignal]) -> Path:
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        path = self.processed_dir / f"{self.source_id}_{utc_now().replace(':', '').replace('-', '')}_processed.json"
        for signal in signals:
            signal.processed_file = str(path.relative_to(self.root))
        path.write_text(json.dumps([asdict(signal) for signal in signals], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        self.reference_manager.update_processed_files({reference_id: signal.processed_file for signal in signals for reference_id in signal.reference_ids})
        return path

    def generate_report(self, processed: list[ProcessedSignal]) -> str:
        lines = [
            f"# {self.registry_entry.get('name', self.source_id)} Report",
            "",
            f"Mode: {self.mode}",
            "",
            "## Candidate Signals",
        ]
        for signal in processed:
            lines.append(f"- {signal.insight} (confidence: {signal.confidence}, references: {', '.join(signal.reference_ids)})")
        lines.extend(["", "## References"])
        for signal in processed:
            lines.append(f"- {', '.join(signal.reference_ids)}")
        return "\n".join(lines) + "\n"

    def save_report(self, processed: list[ProcessedSignal]) -> Path:
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        path = self.reports_dir / f"{self.source_id}_report.md"
        path.write_text(self.generate_report(processed), encoding="utf-8")
        return path

    def run(self, queries: list[str], limit: int) -> dict[str, Any]:
        signals = self.collect(queries, limit)
        raw_path = self.save_raw(signals)
        processed = self.process(signals)
        processed_path = self.save_processed(processed)
        report_path = self.save_report(processed)
        return {
            "source": self.source_id,
            "mode": self.mode,
            "raw_file": str(raw_path.relative_to(self.root)),
            "processed_file": str(processed_path.relative_to(self.root)),
            "report_file": str(report_path.relative_to(self.root)),
            "signals": len(signals),
            "processed": len(processed),
            "mock": self.mode == "mock",
        }
