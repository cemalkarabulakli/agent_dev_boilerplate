from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter, RawSignal


class FacebookAdLibraryAdapter(BaseSourceAdapter):
    source_id = "facebook_ad_library"
    source_type = "ad_library"
    signal_kind = "ad_angle"

    def default_tags(self) -> list[str]:
        return ["ad_angles", "cta_patterns", "offer_patterns", "compliance_risks"]

    def extract_insight(self, signal: RawSignal) -> str:
        return f"Candidate ad angle or positioning pattern for '{signal.query}': {signal.snippet}"
