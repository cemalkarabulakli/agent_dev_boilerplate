from core.business_context_schema import BusinessContext
from core.checklist_runner import evaluate_business_quality, run_for_agent

def test_checklist_runner_passes_repository_checks() -> None:
    report = run_for_agent("offer_architect")
    assert report.passed

def test_business_quality_fails_if_market_missing() -> None:
    context = BusinessContext.from_dict({"expert": {}, "market": {}, "customer": {"specific_avatar": "Founders", "target_customer": "Founders"}, "offer": {}, "business": {}, "acquisition": {}, "sales": {}, "delivery": {}, "retention": {}, "constraints": {}, "metrics": {}, "notes": {}})
    assert "market is missing" in evaluate_business_quality(context)

def test_business_quality_fails_if_avatar_too_broad() -> None:
    data = {"expert": {}, "market": {"market_name": "Consulting"}, "customer": {"specific_avatar": "everyone", "target_customer": "everyone"}, "offer": {}, "business": {}, "acquisition": {}, "sales": {}, "delivery": {}, "retention": {}, "constraints": {}, "metrics": {}, "notes": {}}
    assert any("avatar" in error for error in evaluate_business_quality(BusinessContext.from_dict(data)))

def test_business_quality_fails_if_offer_has_no_target_customer() -> None:
    data = {"expert": {}, "market": {"market_name": "Consulting"}, "customer": {"specific_avatar": "B2B consultants"}, "offer": {}, "business": {}, "acquisition": {}, "sales": {}, "delivery": {}, "retention": {}, "constraints": {}, "metrics": {}, "notes": {}}
    assert "offer has no target customer" in evaluate_business_quality(BusinessContext.from_dict(data))

def test_business_quality_fails_if_fake_claims_present() -> None:
    data = {"expert": {}, "market": {"market_name": "Consulting"}, "customer": {"specific_avatar": "B2B consultants", "target_customer": "B2B consultants"}, "offer": {"core_promise": "fake testimonial"}, "business": {}, "acquisition": {}, "sales": {}, "delivery": {}, "retention": {}, "constraints": {}, "metrics": {}, "notes": {}}
    assert any("fake" in error for error in evaluate_business_quality(BusinessContext.from_dict(data)))
