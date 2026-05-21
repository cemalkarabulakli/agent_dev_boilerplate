from core.agent_loader import load_agent_config
from core.context_compactor import compact_context

def test_compact_context_preserves_key_facts_and_recent_turns() -> None:
    config = load_agent_config("offer_architect")
    history = [
        {"role": "user", "content": "hello"},
        {"role": "user", "content": "Market: executive coaches. Avatar: founder doing $30k/month. Offer: 8-week advisory. Price: $5000."},
        {"role": "user", "content": "Acquisition decision: use workshops. Sales decision: application call. Delivery decision: weekly milestones. Rejected idea: fake scarcity."},
    ]
    result = compact_context(config, history)
    assert result.passed
    assert "executive coaches" in result.markdown
    assert "$5000" in result.markdown
    assert "Rejected idea" in result.markdown

def test_compact_context_removes_noise() -> None:
    config = load_agent_config("market_selector")
    result = compact_context(config, [{"role": "user", "content": "hi"}, {"role": "user", "content": "Market: dentists with urgent hiring pain."}])
    assert result.removed_noise_count >= 1

def test_compact_context_excludes_raw_research_dumps() -> None:
    config = load_agent_config("offer_architect")
    result = compact_context(
        config,
        [
            {"role": "user", "content": "Market: consultants. Offer: advisory. Price: $5000."},
            {"role": "tool", "content": "Raw research dump: copied forum page with raw source output and irrelevant fragments."},
            {"role": "tool", "content": "Processed candidate insight with confidence 0.62 and reference_ids ref_2026_0001."},
        ],
    )

    assert result.passed
    assert "Raw research dump" not in result.markdown
    assert "Processed candidate insight" in result.markdown
