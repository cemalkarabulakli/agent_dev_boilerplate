"""Basic guardrails for local-first agent runs."""

from __future__ import annotations

from core.schema import AgentConfig


HARMFUL_KEYWORDS = {
    "steal credentials",
    "phishing kit",
    "malware",
    "bypass authentication",
}

PRIVATE_DATA_PROMPTS = {
    "password",
    "social security number",
    "credit card number",
    "private key",
}


def validate_input(message: str, config: AgentConfig) -> list[str]:
    errors: list[str] = []
    lowered = message.lower()
    if "no_illegal_or_harmful_requests" in config.guardrails.input:
        for keyword in HARMFUL_KEYWORDS:
            if keyword in lowered:
                errors.append(f"Input appears to request harmful activity: {keyword}")
    if "no_private_data_required" in config.guardrails.input:
        for keyword in PRIVATE_DATA_PROMPTS:
            if keyword in lowered:
                errors.append(f"Input appears to ask for private data: {keyword}")
    return errors


def validate_tool_execution(tool_name: str, config: AgentConfig) -> list[str]:
    if tool_name not in config.tools.allowed:
        return [f"Tool '{tool_name}' is not in the agent allowlist."]
    destructive_markers = ("delete", "remove", "shell", "exec", "push")
    if any(marker in tool_name for marker in destructive_markers):
        return [f"Tool '{tool_name}' looks destructive and requires explicit confirmation."]
    return []


def output_safety_notes(config: AgentConfig) -> list[str]:
    notes: list[str] = []
    if "no_fake_claims" in config.guardrails.output:
        notes.append("Do not present unsourced claims as facts.")
    if "cite_sources_when_using_knowledge" in config.guardrails.output:
        notes.append("Cite source IDs whenever knowledge files are used.")
    if "separate_fact_from_recommendation" in config.guardrails.output:
        notes.append("Separate facts, assumptions, and recommendations.")
    return notes
