from __future__ import annotations
from pathlib import Path
from typing import Any
from core.business_context_schema import BusinessContext
from core.schema import utc_now

OUTPUT_TEMPLATES = {
    "market_selector": ("market_scorecards", "Market Scorecard", ["Market", "Pain Level", "Urgency", "Ability To Pay", "Accessibility", "Competition", "Current Alternatives", "Transformation Potential", "Delivery Feasibility", "Score", "Risks", "Recommendation", "Next Research Questions"]),
    "avatar_pain_researcher": ("avatar_research", "Avatar & Pain Research", ["Specific Avatar", "Current Situation", "Urgent Pain", "Expensive Consequences", "Dream Outcome", "Emotional Drivers", "Logical Drivers", "Objections", "Buying Triggers", "Current Alternatives", "Messaging Angles", "Research Questions"]),
    "offer_architect": ("offer_audits", "High-Ticket Offer", ["Target Customer", "Painful Problem", "Dream Outcome", "Unique Mechanism", "Core Promise", "Offer Stack", "Bonuses", "Guarantee / Risk Reversal", "Proof Needed", "Price", "Payment Options", "Objections", "Sales Argument", "Next Actions"]),
    "value_stack_builder": ("value_stacks", "Value Stack", ["Core Deliverable", "Implementation Support", "Templates / Assets", "Accountability", "Reviews / Audits", "Bonuses", "Risk Reducers", "Perceived Value Notes", "Simplified Offer Stack"]),
    "pricing_guarantee_optimizer": ("pricing_reviews", "Pricing & Guarantee Review", ["Current Price", "Value Justification", "Pricing Problems", "Better Pricing Options", "Payment Plan Options", "Guarantee Ideas", "Risk Reversal Notes", "Profitability Risks", "Recommendation"]),
    "acquisition_strategy_agent": ("acquisition_plans", "Acquisition Plan", ["Best Lead Source", "Secondary Lead Sources", "Message To Market", "Lead Magnet / CTA", "Qualification Method", "Weekly Actions", "Metrics To Track", "Risks"]),
    "content_authority_agent": ("content_plans", "Authority Content Plan", ["Content Positioning", "Main Content Pillars", "Weekly Content Calendar", "Hooks", "Authority Posts", "Proof Posts", "Objection Posts", "Belief-Shifting Posts", "CTA Posts"]),
    "funnel_builder": ("funnel_maps", "High-Ticket Funnel Map", ["Traffic Source", "Lead Magnet", "Workshop / Webinar", "Application Page", "Booking Page", "Email Sequence", "Retargeting", "Sales Call Flow", "Metrics To Track"]),
    "sales_script_builder": ("sales_scripts", "Sales Call Script", ["Qualification Criteria", "Opening", "Diagnosis Questions", "Pain Questions", "Desired Outcome Questions", "Current Alternative Questions", "Offer Presentation", "Objection Handling", "Close / Next Step", "Follow-Up Notes"]),
    "objection_handler": ("objection_banks", "Objection Bank", ["Main Objections", "Root Cause", "Ethical Response", "Proof Needed", "Offer Adjustment Needed", "Follow-Up Message"]),
    "proof_engine_builder": ("proof_engines", "Proof Engine", ["Proof Assets Needed", "Case Study Collection Process", "Client Metrics To Track", "Before / After Structure", "Testimonial Questions", "Process Proof Ideas", "Authority Proof Ideas", "Ethical Claims Rules"]),
    "delivery_system_designer": ("delivery_systems", "Delivery System", ["Onboarding", "Client Roadmap", "Milestones", "Weekly Delivery Cadence", "Support Model", "Templates / Assets", "SOPs Needed", "Client Dashboard", "Success Metrics", "Fulfillment Risks", "Case Study Collection Points"]),
    "retention_upsell_agent": ("business_scorecards", "Retention & Upsell Plan", ["Continuity Offer", "Advanced Offer", "Upsell Path", "Community / Mastermind", "Renewal Process", "Referral System", "Expansion Opportunities"]),
    "business_scorecard_agent": ("business_scorecards", "High-Ticket Business Scorecard", ["Market Score", "Avatar Score", "Offer Score", "Proof Score", "Acquisition Score", "Funnel Score", "Sales Score", "Delivery Score", "Retention Score", "Main Bottleneck", "Highest Leverage Fix", "7-Day Action Plan"]),
}

HINTS = {"Market": ("market", "market_name"), "Specific Avatar": ("customer", "specific_avatar"), "Target Customer": ("customer", "target_customer"), "Painful Problem": ("customer", "expensive_problem"), "Dream Outcome": ("customer", "dream_outcome"), "Unique Mechanism": ("offer", "unique_mechanism"), "Core Promise": ("offer", "core_promise"), "Current Price": ("offer", "current_price"), "Price": ("offer", "current_price")}

def value(context: BusinessContext, section: str) -> str:
    if section in HINTS:
        source, key = HINTS[section]
        data = context.get(source, key)
        if data not in ("", None, [], {}):
            return ", ".join(data) if isinstance(data, list) else str(data)
    return "Unknown. Treat this as an assumption gap, not a fact."

def render_mock_output(agent_name: str, context: BusinessContext) -> str:
    _, title, sections = OUTPUT_TEMPLATES[agent_name]
    lines = [f"# {title}", "", f"Generated in local mock mode at {utc_now()}.", "", "## Facts", "- Uses only fields from business_context.yaml.", "", "## Assumptions", "- Blank fields are unknown and must be validated before making strong claims.", "", "## Recommendations", "- Fix market, avatar, and offer clarity before scaling traffic.", ""]
    for section in sections:
        lines.extend([f"## {section}"])
        if section == "Main Bottleneck":
            lines.append(context.get("business", "current_bottleneck") or "Offer clarity is the default bottleneck when market, avatar, and offer fields are blank.")
        elif section == "Highest Leverage Fix":
            lines.append("Clarify market, avatar, expensive problem, offer promise, proof required, and delivery capacity.")
        elif section == "7-Day Action Plan":
            lines.append("Day 1-2: clarify market/avatar. Day 3-4: sharpen offer. Day 5: define proof. Day 6: map sales. Day 7: review scorecard.")
        elif "Score" in section and agent_name == "business_scorecard_agent":
            lines.append("5/10 placeholder score until real business data is provided.")
        else:
            lines.append(value(context, section))
        lines.append("")
    lines.extend(["## Ethical Notes", "- No fake claims.", "- No fake testimonials.", "- No fake scarcity.", "- No unrealistic income promises."])
    return "\n".join(lines) + "\n"

def save_output(root: Path, agent_name: str, markdown: str) -> Path:
    directory, _, _ = OUTPUT_TEMPLATES[agent_name]
    path = root / "outputs" / directory / f"{agent_name}_latest.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")
    return path
