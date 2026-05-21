from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter, RawSignal


class YouTubeAdapter(BaseSourceAdapter):
    source_id = "youtube"
    source_type = "video"
    signal_kind = "content_angle"

    def default_tags(self) -> list[str]:
        return ["content_angles", "hook_patterns", "authority_topics", "audience_pain"]

    def extract_insight(self, signal: RawSignal) -> str:
        return f"Candidate content trend, hook, or authority topic for '{signal.query}': {signal.snippet}"
