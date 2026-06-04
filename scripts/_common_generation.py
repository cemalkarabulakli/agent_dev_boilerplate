from __future__ import annotations
import os
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import argparse
from core.agent_loader import load_agent
from core.business_context_schema import BusinessContext
from core.memory_manager import MemoryManager
from core.output_templates import render_mock_output, save_output, extract_structured_output, PIPELINE_SCHEMA
from core.pipeline_context import PipelineContext

# Agent-specific task instructions appended to the formatted business context.
_TASK_PROMPTS: dict[str, str] = {
    "case_study_writer": (
        "Write a complete, high-converting client case study based on the business context above.\n"
        "Structure: Client Background → Before State → Transformation Journey → Specific Results → "
        "Key Numbers → Objections Addressed → Proof Validation → Usage Rights → Ethical Claims Rules.\n"
        "If client data is missing, provide the full framework with exact questions the expert must "
        "answer to complete each section. Mark every gap with [MISSING: what is needed]."
    ),
    "vsl_copywriter": (
        "Create a complete VSL (Video Sales Letter) script and funnel plan based on the business context above.\n"
        "Deliver: Business Profile summary, 3 offer options, VSL Hook (3 variants), Problem Amplification, "
        "Solution Reveal with the unique mechanism, Social Proof section, Offer Presentation, "
        "strong Call To Action, Landing Page structure, and 4 Lovable.dev build prompts for the funnel."
    ),
    "youtube_strategy_agent": (
        "Build a complete YouTube channel strategy using the Turanlı Method based on the business context above.\n"
        "Cover: Niche Selection & Validation (scored), SEO Architecture, Competitor Intelligence approach, "
        "30-day Content Calendar, AI-Powered Production workflow, Monetization plan, Growth KPIs, "
        "Thumbnail Strategy, Title Formula, and a reusable Description Template."
    ),
    "meta_ads_manager": (
        "Create a complete Meta Ads strategy using Andromeda-First principles based on the business context above.\n"
        "Cover: Campaign Objective, Audience setup (broad, not narrow), Creative Strategy with 20+ conceptually "
        "diverse angles, Ad Format mix, Budget Allocation, Advantage+ configuration, CAPI signal quality checklist, "
        "P.D.A. Framework application, 4-week Testing Plan, KPIs, and Ethical Ad Rules."
    ),
    "launch_campaign_manager": (
        "Plan a complete launch campaign based on the business context above.\n"
        "Cover: Launch Timeline (Phase 0–3), Pre-Launch Phase (PLC content plan with 3–5 pieces), "
        "Cart Open Phase, Cart Close Phase (deadline + urgency stack), full Email Sequence arc, "
        "VSL/Webinar Plan, Ad Strategy, Landing Page Copy outline, Post-Launch Debrief template, "
        "Revenue Target breakdown, and Launch KPIs."
    ),
}


def _format_upstream(deps: dict) -> str:
    """Compact upstream section injected at the top of the API prompt."""
    if not deps:
        return ""
    lines = ["## Upstream Agent Outputs (structured summary)\n"]
    for k, v in deps.items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    return "\n".join(lines) + "\n"


def _format_context(context: BusinessContext) -> str:
    """Render business_context.yaml as structured markdown for the agent prompt."""
    lines: list[str] = ["# Business Context\n"]
    section_labels = {
        "expert": "Expert Profile",
        "market": "Market",
        "customer": "Target Customer",
        "offer": "Offer",
        "business": "Business",
        "acquisition": "Acquisition",
        "sales": "Sales",
        "delivery": "Delivery",
        "retention": "Retention",
        "constraints": "Constraints",
        "metrics": "Metrics",
    }
    for key, label in section_labels.items():
        section = context.data.get(key, {})
        if not isinstance(section, dict):
            continue
        lines.append(f"## {label}")
        has_data = False
        for field, value in section.items():
            if value in ("", None, [], {}):
                continue
            label_field = field.replace("_", " ").title()
            display = ", ".join(str(v) for v in value) if isinstance(value, list) else str(value)
            lines.append(f"- **{label_field}**: {display}")
            has_data = True
        if not has_data:
            lines.append("*(No data — flag all outputs as assumptions requiring validation)*")
        lines.append("")

    notes = context.data.get("notes", {})
    if isinstance(notes, dict):
        assumptions = notes.get("assumptions") or []
        questions = notes.get("open_questions") or []
        if assumptions or questions:
            lines.append("## Notes")
            if assumptions:
                lines.append(f"- **Assumptions**: {', '.join(assumptions)}")
            if questions:
                lines.append(f"- **Open Questions**: {', '.join(questions)}")
            lines.append("")

    return "\n".join(lines)


def _call_api(system_prompt: str, user_message: str, model: str) -> str:
    import anthropic
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=8192,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text  # type: ignore[union-attr]


def run_generation(default_agent: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", default=default_agent)
    parser.add_argument("--context", default="business_context.yaml")
    parser.add_argument("--pipeline", default="pipeline_context.json",
                        help="Path to pipeline_context.json for inter-agent data flow.")
    parser.add_argument(
        "--mode", choices=["api", "mock"], default="api",
        help="api: call Claude API (requires ANTHROPIC_API_KEY). mock: local placeholder output.",
    )
    parser.add_argument("--model", default="claude-sonnet-4-6")
    parser.add_argument("--no-memory", action="store_true", help="Skip memory writes for deterministic tests.")
    args = parser.parse_args()

    loaded = load_agent(args.agent, ROOT)
    context = BusinessContext.load(ROOT / args.context)
    pipeline = PipelineContext(ROOT / args.pipeline)

    schema = PIPELINE_SCHEMA.get(args.agent, {})
    deps, gaps = pipeline.read_deps(schema.get("reads", {}))

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    use_api = args.mode == "api" and bool(api_key)

    if args.mode == "api" and not api_key:
        print("[warn] ANTHROPIC_API_KEY not set — falling back to mock mode.", file=sys.stderr)

    if use_api:
        task = _TASK_PROMPTS.get(
            args.agent,
            "Generate a comprehensive analysis and plan based on the business context above.",
        )
        upstream_section = _format_upstream(deps)
        user_message = f"{upstream_section}{_format_context(context)}\n---\n\n{task}"
        print(f"[{args.agent}] Calling {args.model}...", file=sys.stderr)
        if gaps:
            print(f"[{args.agent}] Upstream gaps: {', '.join(gaps)}", file=sys.stderr)
        markdown = _call_api(loaded.system_prompt, user_message, model=args.model)
    else:
        markdown = render_mock_output(args.agent, context, deps, gaps)

    path = save_output(ROOT, args.agent, markdown)
    mode_used = "api" if use_api else "mock"

    structured = extract_structured_output(args.agent, context, deps)
    pipeline.write_output(args.agent, structured, gaps)

    if not args.no_memory:
        manager = MemoryManager(loaded.agent_dir)
        manager.append_raw_history(
            "agent", f"Generated {path.name}", {"script": Path(sys.argv[0]).name, "mode": mode_used},
        )
        manager.save_candidate_memory(
            f"Generated output in {mode_used} mode from business_context.yaml.", "assumption", "agent", 0.4,
        )

    print(path)
    return 0
