from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter, RawSignal


class GitHubTrendsAdapter(BaseSourceAdapter):
    source_id = "github_trends"
    source_type = "tool_trend"
    signal_kind = "tool_opportunity"

    def default_tags(self) -> list[str]:
        return ["tool_mentions", "developer_adoption", "tool_opportunities"]

    def extract_insight(self, signal: RawSignal) -> str:
        return f"Candidate tool opportunity or open-source adoption signal for '{signal.query}': {signal.snippet}"
