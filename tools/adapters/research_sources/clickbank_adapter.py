from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter, RawSignal


class ClickBankAdapter(BaseSourceAdapter):
    source_id = "clickbank"
    source_type = "marketplace"
    signal_kind = "offer_pattern"

    def default_tags(self) -> list[str]:
        return ["offer_patterns", "niche_monetization", "affiliate_angles", "risk_notes"]

    def extract_insight(self, signal: RawSignal) -> str:
        return f"Candidate digital product offer or monetization pattern for '{signal.query}': {signal.snippet}"
