from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter, RawSignal


class QuoraAdapter(BaseSourceAdapter):
    source_id = "quora"
    source_type = "question_answer"
    signal_kind = "customer_question"

    def extract_insight(self, signal: RawSignal) -> str:
        return f"Repeated question or confusion around '{signal.query}': {signal.snippet}"
