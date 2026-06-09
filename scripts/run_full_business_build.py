"""
run_full_business_build.py — Full pipeline orchestrator.

Runs all agents in dependency order:
  market_selector → avatar_pain_researcher → offer_architect → ... → launch_campaign_manager

Usage:
  python scripts/run_full_business_build.py
  python scripts/run_full_business_build.py --mode api
  python scripts/run_full_business_build.py --skip-to offer_architect
  python scripts/run_full_business_build.py --only market_selector,avatar_pain_researcher
  python scripts/run_full_business_build.py --group foundation,offer
  python scripts/run_full_business_build.py --dry-run
  python scripts/run_full_business_build.py --no-memory --stop-on-error
  python scripts/run_full_business_build.py --list
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.agent_loader import load_agent
from core.business_context_schema import BusinessContext
from core.memory_manager import MemoryManager
from core.output_templates import render_mock_output, save_output, extract_structured_output, PIPELINE_SCHEMA
from core.pipeline_context import PipelineContext
from scripts._common_generation import _call_api, _format_context, _format_upstream, _TASK_PROMPTS


# ── Pipeline definition ──────────────────────────────────────────────────────

class Stage(NamedTuple):
    agent: str
    label: str
    group: str


PIPELINE: list[Stage] = [
    # Foundation — must run first; everything downstream depends on market + avatar clarity
    Stage("market_selector",              "Market Analysis",       "foundation"),
    Stage("avatar_pain_researcher",       "Avatar & Pain Research","foundation"),
    # Offer — built on market + avatar; value stack and pricing require a defined offer
    Stage("offer_architect",              "Offer Architecture",    "offer"),
    Stage("value_stack_builder",          "Value Stack",           "offer"),
    Stage("pricing_guarantee_optimizer",  "Pricing & Guarantee",   "offer"),
    Stage("proof_engine_builder",         "Proof Engine",          "offer"),
    # Acquisition & Sales — require a validated offer before mapping traffic and scripts
    Stage("acquisition_strategy_agent",   "Acquisition Strategy",  "acquisition"),
    Stage("content_authority_agent",      "Content Authority",     "acquisition"),
    Stage("funnel_builder",               "Funnel Map",            "acquisition"),
    Stage("sales_script_builder",         "Sales Script",          "acquisition"),
    Stage("objection_handler",            "Objection Bank",        "acquisition"),
    # Delivery & Retention — back-end infrastructure, after front-end is defined
    Stage("delivery_system_designer",     "Delivery System",       "delivery"),
    Stage("retention_upsell_agent",       "Retention & Upsell",    "delivery"),
    # Assessment — full-system scorecard, meaningful only after all layers exist
    Stage("business_scorecard_agent",     "Business Scorecard",    "assessment"),
    # Specialists — channel-specific plans that build on a complete business foundation
    Stage("meta_ads_manager",             "Meta Ads Plan",         "specialists"),
    Stage("vsl_copywriter",               "VSL Script",            "specialists"),
    Stage("case_study_writer",            "Case Study",            "specialists"),
    Stage("youtube_strategy_agent",       "YouTube Strategy",      "specialists"),
    # Launch — final orchestration layer; requires everything above to be in place
    Stage("launch_campaign_manager",      "Launch Campaign",       "launch"),
]

GROUP_LABELS: dict[str, str] = {
    "foundation":  "Foundation",
    "offer":       "Offer",
    "acquisition": "Acquisition & Sales",
    "delivery":    "Delivery & Retention",
    "assessment":  "Assessment",
    "specialists": "Specialists",
    "launch":      "Launch",
}


# ── Core runner ──────────────────────────────────────────────────────────────

def run_agent_step(
    agent_name: str,
    context: BusinessContext,
    pipeline: PipelineContext,
    no_memory: bool,
    use_api: bool = False,
    model: str = "claude-sonnet-4-6",
) -> Path:
    schema = PIPELINE_SCHEMA.get(agent_name, {})
    deps, gaps = pipeline.read_deps(schema.get("reads", {}))

    loaded = load_agent(agent_name, ROOT)

    if use_api:
        task = _TASK_PROMPTS.get(
            agent_name,
            "Generate a comprehensive analysis and plan based on the business context above.",
        )
        upstream_section = _format_upstream(deps)
        user_message = f"{upstream_section}{_format_context(context)}\n---\n\n{task}"
        if gaps:
            print(f"              [gaps] {', '.join(gaps)}")
        markdown = _call_api(loaded.system_prompt, user_message, model=model)
    else:
        markdown = render_mock_output(agent_name, context, deps, gaps)

    path = save_output(ROOT, agent_name, markdown)

    structured = extract_structured_output(agent_name, context, deps)
    pipeline.write_output(agent_name, structured, gaps)

    if not no_memory:
        mode_label = "api" if use_api else "mock"
        manager = MemoryManager(loaded.agent_dir)
        manager.append_raw_history(
            "agent",
            f"Generated {path.name}",
            {"script": "run_full_business_build.py", "mode": mode_label},
        )
        manager.save_candidate_memory(
            f"Generated {mode_label} output from business_context.yaml",
            "assumption", "agent", 0.4,
        )
    return path


# ── Formatting helpers ───────────────────────────────────────────────────────

def _sep(char: str = "-", width: int = 64) -> str:
    return char * width


def _group_header(group: str) -> None:
    label = GROUP_LABELS.get(group, group.upper())
    print(f"\n{_sep('=')}")
    print(f"  {label.upper()}")
    print(_sep("="))


# ── CLI ──────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run the full high-ticket business build pipeline.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
groups: foundation | offer | acquisition | delivery | assessment | specialists | launch

examples:
  python scripts/run_full_business_build.py
  python scripts/run_full_business_build.py --list
  python scripts/run_full_business_build.py --skip-to offer_architect
  python scripts/run_full_business_build.py --only market_selector,offer_architect
  python scripts/run_full_business_build.py --group foundation,offer
  python scripts/run_full_business_build.py --dry-run
  python scripts/run_full_business_build.py --no-memory --stop-on-error
        """,
    )
    p.add_argument(
        "--context", default="business_context.yaml",
        help="Path to business context YAML (default: business_context.yaml)",
    )
    p.add_argument(
        "--pipeline", default="pipeline_context.json",
        help="Path to pipeline context JSON for inter-agent data flow (default: pipeline_context.json)",
    )
    p.add_argument(
        "--mode", choices=["api", "mock"], default="mock",
        help="api: call Claude API (requires ANTHROPIC_API_KEY). mock: local placeholder output.",
    )
    p.add_argument(
        "--model", default="claude-sonnet-4-6",
        help="Claude model to use in api mode (default: claude-sonnet-4-6)",
    )
    p.add_argument(
        "--skip-to", metavar="AGENT",
        help="Skip all stages before AGENT and start from AGENT",
    )
    p.add_argument(
        "--only", metavar="AGENTS",
        help="Comma-separated list of specific agents to run",
    )
    p.add_argument(
        "--group", metavar="GROUPS",
        help="Comma-separated group names to run (see groups above)",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Show what would run without executing anything",
    )
    p.add_argument(
        "--no-memory", action="store_true",
        help="Skip memory writes (faster, deterministic)",
    )
    p.add_argument(
        "--stop-on-error", action="store_true",
        help="Halt the pipeline on the first failure",
    )
    p.add_argument(
        "--list", action="store_true",
        help="List all pipeline stages and exit",
    )
    p.add_argument(
        "--confirm", action="store_true",
        help="Skip the api-mode cost confirmation prompt",
    )
    return p.parse_args()


# ── List command ─────────────────────────────────────────────────────────────

def list_pipeline() -> None:
    current_group = None
    for i, stage in enumerate(PIPELINE, 1):
        if stage.group != current_group:
            current_group = stage.group
            _group_header(stage.group)
        print(f"  {i:2d}. {stage.label:<32}  ({stage.agent})")
    print()


# ── Stage selection ──────────────────────────────────────────────────────────

def select_stages(args: argparse.Namespace) -> list[Stage] | None:
    """Return the ordered list of stages to run, or None on validation error."""
    stages = list(PIPELINE)

    if args.only:
        names = {n.strip() for n in args.only.split(",")}
        stages = [s for s in stages if s.agent in names]
        unknown = names - {s.agent for s in PIPELINE}
        if unknown:
            print(f"[ERROR] Unknown agents: {', '.join(sorted(unknown))}")
            valid = ", ".join(s.agent for s in PIPELINE)
            print(f"        Valid agents: {valid}")
            return None

    if args.group:
        groups = {g.strip() for g in args.group.split(",")}
        unknown = groups - set(GROUP_LABELS)
        if unknown:
            print(f"[ERROR] Unknown groups: {', '.join(sorted(unknown))}")
            print(f"        Valid groups: {', '.join(GROUP_LABELS)}")
            return None
        stages = [s for s in stages if s.group in groups]

    if args.skip_to:
        agent_names = [s.agent for s in stages]
        if args.skip_to not in agent_names:
            print(f"[ERROR] --skip-to agent '{args.skip_to}' not found in the selected pipeline.")
            return None
        idx = agent_names.index(args.skip_to)
        stages = stages[idx:]

    return stages


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    args = parse_args()

    if args.list:
        list_pipeline()
        return 0

    stages = select_stages(args)
    if stages is None:
        return 1
    if not stages:
        print("[WARN] No stages selected. Nothing to run.")
        return 0

    context_path = ROOT / args.context
    if not context_path.exists():
        print(f"[ERROR] Context file not found: {context_path}")
        return 1

    # ── API mode setup ────────────────────────────────────────────────────────
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    use_api = args.mode == "api" and bool(api_key)
    if args.mode == "api" and not api_key:
        print("[ERROR] --mode api requires ANTHROPIC_API_KEY to be set.")
        return 1

    # ── Header ───────────────────────────────────────────────────────────────
    print(_sep("="))
    print("  FULL BUSINESS BUILD PIPELINE")
    print(_sep("="))
    print(f"  Context  : {context_path.name}")
    print(f"  Pipeline : {args.pipeline}")
    print(f"  Stages   : {len(stages)} / {len(PIPELINE)}")
    print(f"  Mode     : {'API — ' + args.model if use_api else 'mock (local)'}")
    print(f"  Memory   : {'disabled' if args.no_memory else 'enabled'}")
    if args.dry_run:
        print("  Dry run  : nothing will be written")
    print(_sep("="))

    if use_api and not args.dry_run and not args.confirm:
        print(f"\n  Running {len(stages)} agent(s) via Claude API.")
        print("  Each agent makes one API call. Costs apply.")
        answer = input("  Continue? [y/N] ").strip().lower()
        if answer != "y":
            print("  Aborted.")
            return 0
        print()

    # ── Dry run ───────────────────────────────────────────────────────────────
    if args.dry_run:
        current_group = None
        for i, stage in enumerate(stages, 1):
            if stage.group != current_group:
                current_group = stage.group
                _group_header(stage.group)
            print(f"  {i:2d}. {stage.label:<32}  ({stage.agent})")
        print(f"\n{_sep()}")
        print(f"  Would run {len(stages)} agent(s). Re-run without --dry-run to execute.")
        return 0

    # ── Execute ───────────────────────────────────────────────────────────────
    context = BusinessContext.load(context_path)
    pipeline = PipelineContext(ROOT / args.pipeline)

    Result = tuple[Stage, str, float, Path | None]
    results: list[Result] = []
    pipeline_start = time.perf_counter()
    current_group = None

    for i, stage in enumerate(stages, 1):
        if stage.group != current_group:
            current_group = stage.group
            _group_header(stage.group)

        counter = f"[{i:2d}/{len(stages)}]"
        label_col = f"{stage.label:<32}"
        print(f"  {counter}  {label_col} ...", end="", flush=True)

        t0 = time.perf_counter()
        try:
            path = run_agent_step(stage.agent, context, pipeline, args.no_memory, use_api, args.model)
            elapsed = time.perf_counter() - t0
            relative = path.relative_to(ROOT)
            print(f"\r  {counter}  {label_col} OK   ({elapsed:.1f}s)  -> {relative}")
            results.append((stage, "ok", elapsed, path))
        except Exception as exc:
            elapsed = time.perf_counter() - t0
            print(f"\r  {counter}  {label_col} FAIL ({elapsed:.1f}s)")
            print(f"              ERROR: {exc}")
            results.append((stage, "fail", elapsed, None))
            if args.stop_on_error:
                print(f"\n{_sep()}")
                print("  Pipeline halted (--stop-on-error).")
                break

    # ── Summary ───────────────────────────────────────────────────────────────
    total = time.perf_counter() - pipeline_start
    ok_count = sum(1 for _, s, _, _ in results if s == "ok")
    fail_count = sum(1 for _, s, _, _ in results if s == "fail")

    print(f"\n{_sep('=')}")
    print("  SUMMARY")
    print(_sep("="))
    print(f"  Total time : {total:.1f}s")
    print(f"  Completed  : {ok_count} / {len(results)}")
    if fail_count:
        print(f"  Failed     : {fail_count}")
        for stage, status, _, _ in results:
            if status == "fail":
                print(f"    x {stage.agent}")
    else:
        print("  Status     : all agents completed successfully")

    if ok_count:
        print(f"\n  Outputs written to: {ROOT / 'outputs'}")
    print(_sep("="))

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
