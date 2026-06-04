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
    "proof_engine_builder": ("proof_engines", "Proof Engine", ["Proof Assets Needed", "Client Metrics To Track", "Before / After Structure", "Testimonial Questions", "Process Proof Ideas", "Authority Proof Ideas", "Ethical Claims Rules"]),
    "delivery_system_designer": ("delivery_systems", "Delivery System", ["Onboarding", "Client Roadmap", "Milestones", "Weekly Delivery Cadence", "Support Model", "Templates / Assets", "SOPs Needed", "Client Dashboard", "Success Metrics", "Fulfillment Risks", "Case Study Collection Points"]),
    "retention_upsell_agent": ("business_scorecards", "Retention & Upsell Plan", ["Continuity Offer", "Advanced Offer", "Upsell Path", "Community / Mastermind", "Renewal Process", "Referral System", "Expansion Opportunities"]),
    "business_scorecard_agent": ("business_scorecards", "High-Ticket Business Scorecard", ["Market Score", "Avatar Score", "Offer Score", "Proof Score", "Acquisition Score", "Funnel Score", "Sales Score", "Delivery Score", "Retention Score", "Main Bottleneck", "Highest Leverage Fix", "7-Day Action Plan"]),
    "meta_ads_manager": ("meta_ads_plans", "Meta Ads Plan — Andromeda-First", ["Campaign Objective", "Target Audience", "Creative Strategy", "Ad Format", "Budget Allocation", "Advantage+ Settings", "Creative Diversification", "Signal Quality", "P.D.A. Framework", "Testing Plan", "KPIs", "Ethical Ad Rules"]),
    "vsl_copywriter": ("vsl_scripts", "VSL Script & Funnel Plan", ["Business Profile", "Offer Selection", "VSL Hook", "Problem Amplification", "Solution Reveal", "Social Proof", "Offer Presentation", "Call To Action", "Landing Page Plan", "Lovable Build Prompts"]),
    "case_study_writer": ("case_studies", "Client Case Study", ["Client Background", "Before State", "Transformation Journey", "Specific Results", "Key Numbers", "Objections Addressed", "Proof Validation", "Usage Rights", "Ethical Claims Rules"]),
    "youtube_strategy_agent": ("youtube_strategies", "YouTube Strategy — Turanlı Method", ["Niche Selection", "SEO Architecture", "Competitor Intelligence", "Content Calendar", "AI-Powered Production", "Channel Monetization", "Growth Metrics", "Thumbnail Strategy", "Title Formula", "Description Template"]),
    "launch_campaign_manager": ("launch_campaigns", "Launch Campaign Plan", ["Launch Timeline", "Pre-Launch Phase", "Cart Open Phase", "Cart Close Phase", "Email Sequence", "VSL / Webinar Plan", "Ad Strategy", "Landing Page Copy", "Post-Launch Debrief", "Revenue Target", "Launch KPIs"]),
}

# Dependency graph: what each agent reads from upstream agents and writes as structured output.
# reads  → {upstream_agent: [section_keys_to_pull]}
# writes → [section_keys_to_extract_and_store]
PIPELINE_SCHEMA: dict[str, dict[str, Any]] = {
    "market_selector": {
        "reads": {},
        "writes": ["Market", "Score", "Risks", "Recommendation"],
    },
    "avatar_pain_researcher": {
        "reads": {"market_selector": ["Market", "Score"]},
        "writes": ["Specific Avatar", "Urgent Pain", "Dream Outcome", "Messaging Angles"],
    },
    "offer_architect": {
        "reads": {
            "avatar_pain_researcher": ["Specific Avatar", "Urgent Pain", "Dream Outcome"],
        },
        "writes": ["Core Promise", "Unique Mechanism", "Price", "Guarantee / Risk Reversal"],
    },
    "value_stack_builder": {
        "reads": {"offer_architect": ["Core Promise", "Price"]},
        "writes": ["Core Deliverable", "Perceived Value Notes"],
    },
    "pricing_guarantee_optimizer": {
        "reads": {"offer_architect": ["Price", "Core Promise"]},
        "writes": ["Recommendation"],
    },
    "acquisition_strategy_agent": {
        "reads": {
            "avatar_pain_researcher": ["Specific Avatar", "Messaging Angles"],
            "offer_architect": ["Core Promise"],
        },
        "writes": ["Best Lead Source", "Message To Market"],
    },
    "content_authority_agent": {
        "reads": {
            "avatar_pain_researcher": ["Specific Avatar", "Urgent Pain"],
            "offer_architect": ["Core Promise"],
        },
        "writes": ["Content Positioning", "Main Content Pillars"],
    },
    "funnel_builder": {
        "reads": {
            "offer_architect": ["Core Promise", "Price"],
            "acquisition_strategy_agent": ["Best Lead Source"],
        },
        "writes": ["Traffic Source", "Lead Magnet"],
    },
    "sales_script_builder": {
        "reads": {
            "avatar_pain_researcher": ["Specific Avatar", "Urgent Pain"],
            "offer_architect": ["Core Promise", "Price"],
        },
        "writes": ["Qualification Criteria"],
    },
    "objection_handler": {
        "reads": {
            "avatar_pain_researcher": ["Specific Avatar"],
            "offer_architect": ["Core Promise", "Price"],
        },
        "writes": ["Main Objections"],
    },
    "proof_engine_builder": {
        "reads": {"offer_architect": ["Core Promise", "Unique Mechanism"]},
        "writes": ["Proof Assets Needed"],
    },
    "delivery_system_designer": {
        "reads": {"offer_architect": ["Core Promise", "Price"]},
        "writes": ["Onboarding", "Client Roadmap"],
    },
    "retention_upsell_agent": {
        "reads": {
            "offer_architect": ["Core Promise", "Price"],
            "delivery_system_designer": ["Onboarding"],
        },
        "writes": ["Continuity Offer", "Upsell Path"],
    },
    "business_scorecard_agent": {
        "reads": {
            "market_selector": ["Market", "Score"],
            "avatar_pain_researcher": ["Specific Avatar"],
            "offer_architect": ["Core Promise", "Price"],
            "acquisition_strategy_agent": ["Best Lead Source"],
        },
        "writes": ["Main Bottleneck", "Highest Leverage Fix"],
    },
    "meta_ads_manager": {
        "reads": {
            "avatar_pain_researcher": ["Specific Avatar", "Messaging Angles"],
            "offer_architect": ["Core Promise", "Price"],
            "acquisition_strategy_agent": ["Best Lead Source", "Message To Market"],
        },
        "writes": ["Campaign Objective", "Creative Strategy", "P.D.A. Framework"],
    },
    "vsl_copywriter": {
        "reads": {
            "avatar_pain_researcher": ["Specific Avatar", "Urgent Pain", "Dream Outcome"],
            "offer_architect": ["Core Promise", "Unique Mechanism", "Price"],
        },
        "writes": ["VSL Hook", "Offer Presentation"],
    },
    "case_study_writer": {
        "reads": {
            "proof_engine_builder": ["Proof Assets Needed"],
            "offer_architect": ["Core Promise"],
        },
        "writes": ["Before State", "Specific Results"],
    },
    "youtube_strategy_agent": {
        "reads": {
            "avatar_pain_researcher": ["Specific Avatar", "Messaging Angles"],
            "content_authority_agent": ["Content Positioning", "Main Content Pillars"],
        },
        "writes": ["Niche Selection", "SEO Architecture"],
    },
    "launch_campaign_manager": {
        "reads": {
            "offer_architect": ["Core Promise", "Price"],
            "funnel_builder": ["Traffic Source", "Lead Magnet"],
            "vsl_copywriter": ["VSL Hook"],
        },
        "writes": ["Launch Timeline", "Revenue Target"],
    },
}

HINTS = {"Market": ("market", "market_name"), "Specific Avatar": ("customer", "specific_avatar"), "Target Customer": ("customer", "target_customer"), "Painful Problem": ("customer", "expensive_problem"), "Dream Outcome": ("customer", "dream_outcome"), "Unique Mechanism": ("offer", "unique_mechanism"), "Core Promise": ("offer", "core_promise"), "Current Price": ("offer", "current_price"), "Price": ("offer", "current_price")}


def value(context: BusinessContext, section: str, deps: dict[str, Any] | None = None) -> str:
    if section in HINTS:
        source, key = HINTS[section]
        data = context.get(source, key)
        if data not in ("", None, [], {}):
            return ", ".join(data) if isinstance(data, list) else str(data)
    if deps:
        for dep_key, dep_val in deps.items():
            if dep_key.split(".", 1)[-1] == section:
                return str(dep_val)
    return "Unknown. Treat this as an assumption gap, not a fact."


_UNKNOWN = "Unknown. Treat this as an assumption gap, not a fact."


def extract_structured_output(
    agent_name: str,
    context: BusinessContext,
    deps: dict[str, Any],
) -> dict[str, Any]:
    writes = PIPELINE_SCHEMA.get(agent_name, {}).get("writes", [])
    result = {}
    for section in writes:
        v = value(context, section, deps)
        if v != _UNKNOWN:
            result[section] = v
    return result


def render_mock_output(
    agent_name: str,
    context: BusinessContext,
    deps: dict[str, Any] | None = None,
    gaps: list[str] | None = None,
) -> str:
    deps = deps or {}
    gaps = gaps or []
    _, title, sections = OUTPUT_TEMPLATES[agent_name]
    lines = [f"# {title}", "", f"Generated in local mock mode at {utc_now()}.", ""]

    upstream_values = {k: v for k, v in deps.items() if not k.startswith("_")}
    if upstream_values:
        lines.extend(["## Upstream Inputs", ""])
        for k, v in upstream_values.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")

    if gaps:
        lines.extend(["## Upstream Gaps", ""])
        for g in gaps:
            lines.append(f"- {g} — not available, treating as unknown")
        lines.append("")

    lines.extend(["## Facts", "- Uses only fields from business_context.yaml.", "", "## Assumptions", "- Blank fields are unknown and must be validated before making strong claims.", "", "## Recommendations", "- Fix market, avatar, and offer clarity before scaling traffic.", ""])

    for section in sections:
        lines.append(f"## {section}")
        if section == "Main Bottleneck":
            lines.append(context.get("business", "current_bottleneck") or "Offer clarity is the default bottleneck when market, avatar, and offer fields are blank.")
        elif section == "Highest Leverage Fix":
            lines.append("Clarify market, avatar, expensive problem, offer promise, proof required, and delivery capacity.")
        elif section == "7-Day Action Plan":
            lines.append("Day 1-2: clarify market/avatar. Day 3-4: sharpen offer. Day 5: define proof. Day 6: map sales. Day 7: review scorecard.")
        elif "Score" in section and agent_name == "business_scorecard_agent":
            lines.append("5/10 placeholder score until real business data is provided.")
        else:
            lines.append(value(context, section, deps))
        lines.append("")

    lines.extend(["## Ethical Notes", "- No fake claims.", "- No fake testimonials.", "- No fake scarcity.", "- No unrealistic income promises."])
    return "\n".join(lines) + "\n"


def save_output(root: Path, agent_name: str, markdown: str) -> Path:
    directory, _, _ = OUTPUT_TEMPLATES[agent_name]
    path = root / "outputs" / directory / f"{agent_name}_latest.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")
    return path
