from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter


class CustomSourceAdapter(BaseSourceAdapter):
    source_id = "custom_source"
    source_type = "custom"
    signal_kind = "custom_signal"
