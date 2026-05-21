from pathlib import Path
from core.business_context_schema import BusinessContext
from core.output_templates import render_mock_output
from core.scorecard_schema import BusinessScorecard

def test_business_scorecard_generates_bottleneck_section() -> None:
    context = BusinessContext.load(Path(__file__).resolve().parents[1] / "business_context.yaml")
    output = render_mock_output("business_scorecard_agent", context)
    assert "## Main Bottleneck" in output
    assert "## Highest Leverage Fix" in output

def test_business_scorecard_schema_validates() -> None:
    scorecard = BusinessScorecard({"market": 5, "avatar": 5, "offer": 5, "proof": 5, "acquisition": 5, "funnel": 5, "sales": 5, "delivery": 5, "retention": 5}, "offer", "clarify offer")
    scorecard.validate()
