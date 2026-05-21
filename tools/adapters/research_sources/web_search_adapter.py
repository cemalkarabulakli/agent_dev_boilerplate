from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter, RawSignal


class WebSearchAdapter(BaseSourceAdapter):
    source_id = "web_search"
    source_type = "search"
    signal_kind = "source_discovery"

    def extract_insight(self, signal: RawSignal) -> str:
        return f"Candidate web discovery or official-docs lead for '{signal.query}': {signal.snippet}"
