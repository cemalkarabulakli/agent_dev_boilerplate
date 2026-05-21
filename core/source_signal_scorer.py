from __future__ import annotations


def score_signal(*, source_count: int, base_confidence: float = 0.55, source_quality: float = 0.7) -> tuple[str, float]:
    confidence = min(0.95, base_confidence + max(0, source_count - 1) * 0.12 + source_quality * 0.1)
    if source_count >= 3 and confidence >= 0.75:
        return "validated", round(confidence, 2)
    if source_count >= 2:
        return "stronger_candidate", round(confidence, 2)
    return "candidate", round(min(confidence, 0.74), 2)
