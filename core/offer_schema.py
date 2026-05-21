from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(frozen=True)
class OfferAudit:
    target_customer: str = ""
    painful_problem: str = ""
    dream_outcome: str = ""
    unique_mechanism: str = ""
    core_promise: str = ""
    offer_stack: list[str] = field(default_factory=list)
    price: str = ""
    guarantee: str = ""
    proof_needed: list[str] = field(default_factory=list)
