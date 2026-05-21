from __future__ import annotations

from core.agent_loader import load_agent_config
from core.context_compactor import compact_context


def test_compact_context_keeps_recent_user_turns_verbatim() -> None:
    config = load_agent_config("meta_ads_expert")
    history = [
        {"role": "user", "content": "hello"},
        {"role": "user", "content": "Goal: build a reusable agent template by 2026-05-21."},
        {"role": "assistant", "content": "ok"},
        {"role": "user", "content": "Constraint: do not include private data."},
    ]
    result = compact_context(config, history)
    assert "Goal: build a reusable agent template by 2026-05-21." in result.markdown
    assert "Constraint: do not include private data." in result.markdown
    assert result.validation.passed


def test_compact_context_preserves_must_keep_facts_and_removes_noise() -> None:
    config = load_agent_config("cto")
    history = [
        {"role": "user", "content": "hi"},
        {"role": "user", "content": "Decision: use file-based memory first."},
        {"role": "user", "content": "Rejected strategy: start with a vector DB in v1."},
        {"role": "assistant", "content": "thanks"},
    ]
    result = compact_context(config, history)
    assert "Decision: use file-based memory first." in result.markdown
    assert "Rejected strategy: start with a vector DB in v1." in result.markdown
    assert "Noise fragments removed:" in result.markdown
    assert result.removed_noise_count >= 1
    assert result.validation.passed
