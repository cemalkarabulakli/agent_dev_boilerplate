from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.source_signal_scorer import score_signal


@dataclass(frozen=True)
class CrossSourceInsight:
    key: str
    status: str
    confidence: float
    source_count: int
    sources: list[str]
    reference_ids: list[str]
    insight: str


class CrossSourceAnalyzer:
    def __init__(self, root: Path):
        self.root = root
        self.signal_index = root / "research" / "index" / "signal_index.jsonl"

    def read_signals(self) -> list[dict[str, Any]]:
        if not self.signal_index.exists():
            return []
        return [json.loads(line) for line in self.signal_index.read_text(encoding="utf-8").splitlines() if line.strip()]

    def analyze(self, signals: list[dict[str, Any]] | None = None) -> list[CrossSourceInsight]:
        signals = signals if signals is not None else self.read_signals()
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for signal in signals:
            key = str(signal.get("insight_type") or signal.get("signal_type") or "general_signal")
            grouped[key].append(signal)
        insights: list[CrossSourceInsight] = []
        for key, items in grouped.items():
            sources = sorted({str(item.get("source")) for item in items})
            references = sorted({ref for item in items for ref in item.get("reference_ids", [])})
            base_confidence = max(float(item.get("confidence", 0.5)) for item in items) if items else 0.5
            status, confidence = score_signal(source_count=len(sources), base_confidence=base_confidence)
            insights.append(
                CrossSourceInsight(
                    key=key,
                    status=status,
                    confidence=confidence,
                    source_count=len(sources),
                    sources=sources,
                    reference_ids=references,
                    insight=f"{status.replace('_', ' ').title()} {key} found across {len(sources)} source(s).",
                )
            )
        return insights

    def write_report(self, insights: list[CrossSourceInsight] | None = None) -> Path:
        insights = insights if insights is not None else self.analyze()
        path = self.root / "research" / "processed" / "cross_source_reports" / "cross_source_report.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Cross-Source Research Report",
            "",
            "## Research Summary",
            f"- Insights analyzed: {len(insights)}",
            "",
            "## Sources Used",
        ]
        used_sources = sorted({source for insight in insights for source in insight.sources})
        lines.extend([f"- {source}" for source in used_sources] or ["- None"])
        sections = [
            ("## Validated Pain Signals", lambda i: i.status == "validated" and "pain" in i.key),
            ("## Candidate Pain Signals", lambda i: i.status != "validated" and "pain" in i.key),
            ("## Repeated Objections", lambda i: "objection" in i.key),
            ("## Repeated Desired Outcomes", lambda i: "desired" in i.key),
            ("## Offer Opportunities", lambda i: "offer" in i.key),
            ("## Content Opportunities", lambda i: "content" in i.key),
            ("## Ad Angle Opportunities", lambda i: "ad_angle" in i.key),
            ("## Tool Opportunities", lambda i: "tool" in i.key),
            ("## Weak Signals", lambda i: i.source_count == 1),
            ("## Conflicting Signals", lambda i: False),
        ]
        for heading, predicate in sections:
            lines.extend(["", heading])
            matched = [insight for insight in insights if predicate(insight)]
            lines.extend(self._format_insight(insight) for insight in matched)
            if not matched:
                lines.append("- None")
        lines.extend(["", "## References"])
        all_refs = sorted({ref for insight in insights for ref in insight.reference_ids})
        lines.extend([f"- {ref}" for ref in all_refs] or ["- None"])
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        mirror = self.root / "outputs" / "cross_source_reports" / "cross_source_report.md"
        mirror.parent.mkdir(parents=True, exist_ok=True)
        mirror.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        return path

    def _format_insight(self, insight: CrossSourceInsight) -> str:
        refs = ", ".join(insight.reference_ids)
        sources = ", ".join(insight.sources)
        return f"- {insight.insight} Confidence: {insight.confidence}. Source quality: acceptable. Sources: {sources}. References: {refs}."
