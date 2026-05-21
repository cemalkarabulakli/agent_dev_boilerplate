from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter, RawSignal


class GoogleTrendsAdapter(BaseSourceAdapter):
    source_id = "google_trends"
    source_type = "trend"
    signal_kind = "demand_trend"

    def default_tags(self) -> list[str]:
        return ["trend_direction", "seasonality", "related_queries", "demand_signal"]

    def extract_insight(self, signal: RawSignal) -> str:
        return f"Candidate demand direction signal for '{signal.query}': {signal.snippet}"
