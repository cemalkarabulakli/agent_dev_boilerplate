from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter, RawSignal


class RedditAdapter(BaseSourceAdapter):
    source_id = "reddit"
    source_type = "community"
    signal_kind = "raw_pain_language"

    def extract_insight(self, signal: RawSignal) -> str:
        return f"Candidate raw pain language or objection from Reddit for '{signal.query}': {signal.snippet}"
