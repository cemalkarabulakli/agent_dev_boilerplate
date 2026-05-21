from __future__ import annotations
from dataclasses import dataclass

SCORE_FIELDS = ["market", "avatar", "offer", "proof", "acquisition", "funnel", "sales", "delivery", "retention"]

@dataclass(frozen=True)
class BusinessScorecard:
    scores: dict[str, int]
    main_bottleneck: str
    highest_leverage_fix: str

    def validate(self) -> None:
        missing = [field for field in SCORE_FIELDS if field not in self.scores]
        if missing:
            raise ValueError("Missing score fields: " + ", ".join(missing))
        if not self.main_bottleneck:
            raise ValueError("Main bottleneck is required")
