from __future__ import annotations
from core.schema import AgentConfig

BLOCKED = ["steal credentials", "phishing", "malware", "fake testimonial", "fake scarcity"]
UNSAFE = ["guaranteed income", "fake testimonial", "fake scarcity"]

def validate_input(message: str, config: AgentConfig) -> list[str]:
    lowered = message.lower()
    return [f"Blocked unsafe request: {term}" for term in BLOCKED if term in lowered]

def validate_output(text: str, config: AgentConfig) -> list[str]:
    lowered = text.lower()
    return [f"Unsafe output phrase: {term}" for term in UNSAFE if term in lowered]
