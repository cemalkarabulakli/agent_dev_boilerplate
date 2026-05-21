from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter, RawSignal


class BGMammaAdapter(BaseSourceAdapter):
    source_id = "bg_mamma"
    source_type = "forum"
    signal_kind = "local_language_pain"
    language = "bg"

    def mock_snippet(self, query: str, index: int) -> str:
        return f"Mock BG-Mamma сигнал за '{query}'. Оригинален български откъс със загриженост, възражение или локален проблем. Variant {index + 1}."

    def extract_insight(self, signal: RawSignal) -> str:
        return f"Bulgarian customer-language candidate signal: {signal.snippet}"
