"""
morning_briefing.py — Generates DASHBOARD.md with today's todos,
pipeline progress, business next steps, and optionally a Gmail summary.

Usage:
  python scripts/morning_briefing.py
  python scripts/morning_briefing.py --email     # fetch Gmail summary via Claude CLI
  python scripts/morning_briefing.py --open      # open DASHBOARD.md in VS Code after generating
  python scripts/morning_briefing.py --email --open
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.business_context_schema import BusinessContext
from scripts.run_full_business_build import PIPELINE, GROUP_LABELS

# Maps agent name → its dedicated generate script
_AGENT_SCRIPTS: dict[str, str] = {
    "market_selector":             "scripts/generate_market_scorecard.py",
    "avatar_pain_researcher":      "scripts/generate_avatar_research.py",
    "offer_architect":             "scripts/generate_offer_audit.py",
    "value_stack_builder":         "scripts/generate_value_stack.py",
    "pricing_guarantee_optimizer": "scripts/generate_pricing_guarantee_review.py",
    "proof_engine_builder":        "scripts/generate_proof_engine.py",
    "acquisition_strategy_agent":  "scripts/generate_acquisition_plan.py",
    "content_authority_agent":     "scripts/generate_content_plan.py",
    "funnel_builder":              "scripts/generate_funnel_map.py",
    "sales_script_builder":        "scripts/generate_sales_script.py",
    "objection_handler":           "scripts/generate_objection_bank.py",
    "delivery_system_designer":    "scripts/generate_delivery_system.py",
    "retention_upsell_agent":      "scripts/run_agent.py --agent retention_upsell_agent",
    "business_scorecard_agent":    "scripts/generate_business_scorecard.py",
    "meta_ads_manager":            "scripts/generate_meta_ads_plan.py",
    "vsl_copywriter":              "scripts/generate_vsl_script.py",
    "case_study_writer":           "scripts/generate_case_study.py",
    "youtube_strategy_agent":      "scripts/generate_youtube_strategy.py",
    "launch_campaign_manager":     "scripts/generate_launch_campaign.py",
}


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _todos_section(pipeline_ctx: dict[str, Any], biz_ctx: dict[str, Any]) -> str:
    completed = set(pipeline_ctx.keys())
    pending = [s for s in PIPELINE if s.agent not in completed]

    lines = ["## Today's Todos\n"]
    lines.append("- [ ] Read and action emails")
    lines.append("- [ ] Review yesterday's agent outputs (if any)")

    if pending:
        next_stage = pending[0]
        lines.append(f"- [ ] Continue business build → run **{next_stage.label}**")

    notes = biz_ctx.get("notes", {})
    questions = notes.get("open_questions") or []
    if questions:
        lines.append(f"- [ ] Answer {len(questions)} open question(s) in `business_context.yaml`")

    empty_count = sum(
        1
        for section in ["expert", "market", "customer", "offer"]
        for val in (biz_ctx.get(section) or {}).values()
        if val in ("", [], None)
    )
    if empty_count > 10:
        lines.append(f"- [ ] Fill {empty_count} empty fields in `business_context.yaml`")

    lines.append("- [ ] Update `pipeline_context.json` if you completed work outside scripts")

    return "\n".join(lines)


def _pipeline_section(pipeline_ctx: dict[str, Any]) -> str:
    completed = set(pipeline_ctx.keys())
    total = len(PIPELINE)
    done_count = sum(1 for s in PIPELINE if s.agent in completed)
    pct = int(done_count / total * 100)

    lines = [
        "## Agent Pipeline Progress\n",
        f"**{done_count} / {total} stages complete ({pct}%)**\n",
    ]

    current_group = None
    for stage in PIPELINE:
        if stage.group != current_group:
            current_group = stage.group
            group_stages = [s for s in PIPELINE if s.group == current_group]
            all_done = all(s.agent in completed for s in group_stages)
            any_done = any(s.agent in completed for s in group_stages)
            icon = "✅" if all_done else "🔄" if any_done else "⬜"
            group_label = GROUP_LABELS.get(current_group, current_group.title())
            lines.append(f"\n### {icon} {group_label}")

        if stage.agent in completed:
            meta = pipeline_ctx[stage.agent].get("_meta", {})
            gaps = meta.get("upstream_gaps", [])
            gap_note = f" *(⚠ {len(gaps)} gap{'s' if len(gaps) != 1 else ''})*" if gaps else ""
            lines.append(f"- [x] {stage.label}{gap_note}")
        else:
            lines.append(f"- [ ] {stage.label}")

    return "\n".join(lines)


def _next_steps_section(pipeline_ctx: dict[str, Any]) -> str:
    completed = set(pipeline_ctx.keys())
    pending = [s for s in PIPELINE if s.agent not in completed]

    if not pending:
        return (
            "## Business Next Steps\n\n"
            "**All pipeline stages complete!**\n\n"
            "Recommended actions:\n"
            "- Review all outputs in `agents/*/outputs/`\n"
            "- Fill any remaining gaps in `business_context.yaml`\n"
            "- Run in API mode for real AI-generated plans:\n"
            "  ```\n"
            "  python scripts/run_full_business_build.py --mode api\n"
            "  ```\n"
        )

    lines = ["## Business Next Steps\n"]
    for i, stage in enumerate(pending[:5], 1):
        script = _AGENT_SCRIPTS.get(stage.agent, f"scripts/run_agent.py --agent {stage.agent}")
        lines.append(f"{i}. **{stage.label}**")
        lines.append(f"   ```")
        lines.append(f"   python {script}")
        lines.append(f"   ```")

    if len(pending) > 5:
        lines.append(
            f"\n*...and {len(pending) - 5} more stages. "
            "Run `python scripts/run_full_business_build.py --list` to see all.*"
        )

    return "\n".join(lines)


def _insights_section(pipeline_ctx: dict[str, Any], biz_ctx: dict[str, Any]) -> str:
    lines = ["## Insights & Open Gaps\n"]
    has_content = False

    # Upstream gaps per completed agent
    all_gaps: list[tuple[str, list[str]]] = [
        (agent, data["_meta"].get("upstream_gaps", []))
        for agent, data in pipeline_ctx.items()
        if data.get("_meta", {}).get("upstream_gaps")
    ]
    if all_gaps:
        has_content = True
        lines.append("**Upstream data gaps in completed agents:**\n")
        for agent, gaps in all_gaps:
            for gap in gaps:
                lines.append(f"- `{agent}` → missing **{gap}**")
        lines.append("")

    # Open questions from business context
    notes = biz_ctx.get("notes", {})
    questions = notes.get("open_questions") or []
    if questions:
        has_content = True
        lines.append("**Open questions in `business_context.yaml`:**\n")
        for q in questions:
            lines.append(f"- {q}")
        lines.append("")

    # Assumptions
    assumptions = notes.get("assumptions") or []
    if assumptions:
        has_content = True
        lines.append("**Assumptions to validate:**\n")
        for a in assumptions:
            lines.append(f"- {a}")

    if not has_content:
        lines.append("*No gaps or open questions detected. Business context looks complete.*")

    return "\n".join(lines)


def _email_section(use_email: bool) -> str:
    if not use_email:
        return (
            "## Email Summary\n\n"
            "*Not fetched. Run with `--email` to include Gmail summary:*\n"
            "```\n"
            "python scripts/morning_briefing.py --email\n"
            "```\n"
        )

    try:
        result = subprocess.run(
            [
                "claude", "-p",
                (
                    "List my unread emails from today. "
                    "For each: sender, subject, one-line summary. "
                    "Max 10 emails. Plain text, no markdown headers."
                ),
            ],
            capture_output=True,
            text=True,
            timeout=45,
        )
        if result.returncode == 0 and result.stdout.strip():
            return f"## Email Summary\n\n{result.stdout.strip()}\n"
        err = result.stderr[:300] if result.stderr else "no output"
        return f"## Email Summary\n\n*Claude CLI error: {err}*\n"
    except FileNotFoundError:
        return (
            "## Email Summary\n\n"
            "*`claude` CLI not found. Make sure Claude Code is installed and in PATH.*\n"
        )
    except subprocess.TimeoutExpired:
        return "## Email Summary\n\n*Timed out (45 s) while fetching emails.*\n"


def generate(use_email: bool = False) -> str:
    pipeline_ctx = _load_json(ROOT / "pipeline_context.json")
    biz_ctx: dict[str, Any] = {}
    try:
        biz_ctx = BusinessContext.load(ROOT / "business_context.yaml").data
    except Exception:
        pass

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    parts = [
        f"# Morning Briefing — {now}",
        "---",
        _todos_section(pipeline_ctx, biz_ctx),
        _pipeline_section(pipeline_ctx),
        _next_steps_section(pipeline_ctx),
        _insights_section(pipeline_ctx, biz_ctx),
        _email_section(use_email),
        "---",
        f"*Generated by `scripts/morning_briefing.py` at {now}. "
        "Regenerate any time or set up automatic daily generation — "
        "see `scripts/setup_morning_reminder.ps1`.*",
    ]

    return "\n\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate DASHBOARD.md morning briefing.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  python scripts/morning_briefing.py\n"
            "  python scripts/morning_briefing.py --email\n"
            "  python scripts/morning_briefing.py --email --open\n"
        ),
    )
    parser.add_argument("--email", action="store_true", help="Fetch Gmail summary via Claude CLI")
    parser.add_argument("--open", action="store_true", help="Open DASHBOARD.md in VS Code after generating")
    args = parser.parse_args()

    content = generate(use_email=args.email)

    out = ROOT / "DASHBOARD.md"
    out.write_text(content, encoding="utf-8")
    print(f"[dashboard] Written to {out.relative_to(ROOT)}")

    if args.open:
        try:
            subprocess.run(["code", str(out)], check=False)
            print("[dashboard] Opened in VS Code")
        except FileNotFoundError:
            print("[dashboard] VS Code (code) not found in PATH — open DASHBOARD.md manually")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
