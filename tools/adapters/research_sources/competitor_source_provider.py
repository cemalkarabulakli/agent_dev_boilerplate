from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter, RawSignal


class CompetitorSourceProvider(BaseSourceAdapter):
    source_id = "competitors"
    source_type = "competitor_monitoring"
    signal_kind = "competitor_signal"

    def default_tags(self) -> list[str]:
        return ["positioning_patterns", "pricing_signals", "offer_stack_signals", "cta_patterns"]

    def extract_insight(self, signal: RawSignal) -> str:
        return f"Candidate competitor positioning or offer signal for '{signal.query}': {signal.snippet}"

