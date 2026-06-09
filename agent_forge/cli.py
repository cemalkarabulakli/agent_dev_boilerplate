"""cli.py — agent-forge command-line interface."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from agent_forge._version import __version__

app = typer.Typer(
    name="agent-forge",
    help="High-ticket business builder — AI agent pipeline CLI",
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()

# ── Helpers ───────────────────────────────────────────────────────────────────

def _find_project_root() -> Path:
    """Walk up from cwd looking for business_context.yaml."""
    here = Path.cwd()
    for candidate in [here, *here.parents]:
        if (candidate / "business_context.yaml").exists():
            return candidate
    return here


def _run_script(script_rel: str, root: Path, extra_args: list[str]) -> int:
    """Run a scripts/ file as a subprocess using the current Python interpreter."""
    script = root / script_rel
    if not script.exists():
        console.print(f"[red]Script not found:[/red] {script}")
        return 1
    result = subprocess.run(
        [sys.executable, str(script), *extra_args],
        cwd=str(root),
    )
    return result.returncode


def _load_json(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _context_fill_pct(data: dict) -> float:
    """Return the percentage of non-empty leaf values in business_context."""
    total = filled = 0
    for section in data.values():
        if not isinstance(section, dict):
            continue
        for v in section.values():
            total += 1
            if v not in ("", None, [], {}):
                filled += 1
    return (filled / total * 100) if total else 0.0


PIPELINE_ORDER = [
    "market_selector", "avatar_pain_researcher", "offer_architect",
    "value_stack_builder", "pricing_guarantee_optimizer", "proof_engine_builder",
    "acquisition_strategy_agent", "content_authority_agent", "funnel_builder",
    "sales_script_builder", "objection_handler",
    "delivery_system_designer", "retention_upsell_agent",
    "business_scorecard_agent",
    "meta_ads_manager", "vsl_copywriter", "case_study_writer",
    "youtube_strategy_agent", "launch_campaign_manager",
]

GROUP_MAP = {
    "market_selector": "Foundation",
    "avatar_pain_researcher": "Foundation",
    "offer_architect": "Offer",
    "value_stack_builder": "Offer",
    "pricing_guarantee_optimizer": "Offer",
    "proof_engine_builder": "Offer",
    "acquisition_strategy_agent": "Acquisition",
    "content_authority_agent": "Acquisition",
    "funnel_builder": "Acquisition",
    "sales_script_builder": "Acquisition",
    "objection_handler": "Acquisition",
    "delivery_system_designer": "Delivery",
    "retention_upsell_agent": "Delivery",
    "business_scorecard_agent": "Assessment",
    "meta_ads_manager": "Specialists",
    "vsl_copywriter": "Specialists",
    "case_study_writer": "Specialists",
    "youtube_strategy_agent": "Specialists",
    "launch_campaign_manager": "Launch",
}


# ── Commands ──────────────────────────────────────────────────────────────────

@app.command()
def version():
    """Show the installed version."""
    rprint(f"agent-forge [bold cyan]{__version__}[/bold cyan]")


@app.command()
def init(
    name: str = typer.Argument(default=".", help="Project directory name. Use '.' for current directory."),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files."),
):
    """Scaffold a new agent project from the built-in template."""
    from agent_forge.scaffold import scaffold_project

    target = Path.cwd() if name == "." else Path.cwd() / name

    if target.exists() and any(target.iterdir()) and not force:
        console.print(f"[yellow]Directory already exists and is not empty:[/yellow] {target}")
        console.print("Use [bold]--force[/bold] to overwrite.")
        raise typer.Exit(1)

    # Template root: prefer the installed package sibling tree, fall back to
    # the directory containing this file (development mode).
    template_root = Path(__file__).resolve().parents[1]

    with console.status(f"Scaffolding [bold]{target.name}[/bold]..."):
        summary = scaffold_project(target, template_root)

    console.print(Panel(
        f"[green]OK[/green] Project created at [bold]{target}[/bold]\n"
        f"  {summary['dirs']} directories, {summary['files']} files copied\n\n"
        f"[bold]Next steps:[/bold]\n"
        f"  1. [cyan]cd {target.name if name != '.' else '.'}[/cyan]\n"
        f"  2. Edit [bold]business_context.yaml[/bold] with your business details\n"
        f"  3. [cyan]agent-forge status[/cyan] — see what's filled\n"
        f"  4. [cyan]agent-forge build --mode api --group foundation[/cyan] — run first agents",
        title="agent-forge init",
        border_style="green",
    ))


@app.command()
def run(
    agent: str = typer.Argument(help="Agent name, e.g. market_selector"),
    mode: str = typer.Option("mock", "--mode", "-m", help="api or mock"),
    model: str = typer.Option("claude-sonnet-4-6", "--model", help="Claude model (api mode only)"),
    no_memory: bool = typer.Option(False, "--no-memory", help="Skip memory writes"),
):
    """Run a single agent and write its output."""
    root = _find_project_root()

    # Map agent name to its generate script if one exists.
    script_map = {
        "market_selector": "scripts/generate_market_scorecard.py",
        "avatar_pain_researcher": "scripts/generate_avatar_research.py",
        "offer_architect": "scripts/generate_offer_audit.py",
        "value_stack_builder": "scripts/generate_value_stack.py",
        "pricing_guarantee_optimizer": "scripts/generate_pricing_guarantee_review.py",
        "acquisition_strategy_agent": "scripts/generate_acquisition_plan.py",
        "content_authority_agent": "scripts/generate_content_plan.py",
        "funnel_builder": "scripts/generate_funnel_map.py",
        "sales_script_builder": "scripts/generate_sales_script.py",
        "objection_handler": "scripts/generate_objection_bank.py",
        "proof_engine_builder": "scripts/generate_proof_engine.py",
        "delivery_system_designer": "scripts/generate_delivery_system.py",
        "retention_upsell_agent": "scripts/generate_business_scorecard.py",
        "business_scorecard_agent": "scripts/generate_business_scorecard.py",
        "meta_ads_manager": "scripts/generate_meta_ads_strategy.py",
        "vsl_copywriter": "scripts/generate_vsl_script.py",
        "case_study_writer": "scripts/generate_case_study.py",
        "youtube_strategy_agent": "scripts/generate_youtube_strategy.py",
        "launch_campaign_manager": "scripts/generate_launch_campaign.py",
    }

    script = script_map.get(agent)
    if not script:
        console.print(f"[red]Unknown agent:[/red] {agent}")
        console.print(f"Valid agents: {', '.join(script_map)}")
        raise typer.Exit(1)

    args = ["--mode", mode, "--model", model]
    if no_memory:
        args.append("--no-memory")

    console.print(f"Running [bold cyan]{agent}[/bold cyan] [{mode}]...")
    code = _run_script(script, root, args)
    raise typer.Exit(code)


@app.command()
def build(
    mode: str = typer.Option("mock", "--mode", "-m", help="api or mock"),
    model: str = typer.Option("claude-sonnet-4-6", "--model", help="Claude model (api mode only)"),
    group: Optional[str] = typer.Option(None, "--group", help="foundation|offer|acquisition|delivery|assessment|specialists|launch"),
    skip_to: Optional[str] = typer.Option(None, "--skip-to", help="Start from this agent"),
    only: Optional[str] = typer.Option(None, "--only", help="Comma-separated agent names"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show plan without executing"),
    no_memory: bool = typer.Option(False, "--no-memory"),
    stop_on_error: bool = typer.Option(False, "--stop-on-error"),
    confirm: bool = typer.Option(False, "--confirm", help="Skip cost confirmation in api mode"),
):
    """Run the full business build pipeline (all 19 agents in order)."""
    root = _find_project_root()
    args = ["--mode", mode, "--model", model]
    if group:
        args += ["--group", group]
    if skip_to:
        args += ["--skip-to", skip_to]
    if only:
        args += ["--only", only]
    if dry_run:
        args.append("--dry-run")
    if no_memory:
        args.append("--no-memory")
    if stop_on_error:
        args.append("--stop-on-error")
    if confirm:
        args.append("--confirm")

    code = _run_script("scripts/run_full_business_build.py", root, args)
    raise typer.Exit(code)


@app.command()
def research(
    source: str = typer.Argument(help="Source ID: reddit, quora, google_trends, youtube, web_search, ..."),
    query: Optional[str] = typer.Option(None, "--query", "-q", help="Search query"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Max results per query"),
    all_sources: bool = typer.Option(False, "--all", help="Run all enabled sources"),
):
    """Collect research signals from a data source."""
    root = _find_project_root()
    if all_sources:
        args: list[str] = []
        if query:
            args += ["--query", query]
        code = _run_script("scripts/collect_all_sources.py", root, args)
    else:
        args = ["--source", source]
        if query:
            args += ["--query", query]
        if limit:
            args += ["--limit", str(limit)]
        code = _run_script("scripts/collect_source.py", root, args)
    raise typer.Exit(code)


@app.command()
def status():
    """Show business context fill % and pipeline completion."""
    root = _find_project_root()
    ctx_path = root / "business_context.yaml"
    pipeline_path = root / "pipeline_context.json"

    # ── Business context ──────────────────────────────────────────────────────
    ctx_data: dict = {}
    if ctx_path.exists():
        import sys as _sys
        _sys.path.insert(0, str(root))
        try:
            from core.schema import load_yaml
            ctx_data = load_yaml(ctx_path)
        except Exception:
            import json as _json
            try:
                ctx_data = _json.loads(ctx_path.read_text(encoding="utf-8"))
            except Exception:
                pass

    fill_pct = _context_fill_pct(ctx_data)

    ctx_table = Table(title="Business Context", show_header=True, header_style="bold magenta")
    ctx_table.add_column("Section")
    ctx_table.add_column("Filled", justify="right")
    ctx_table.add_column("Total", justify="right")
    ctx_table.add_column("Status", justify="center")

    for section_name, section in ctx_data.items():
        if not isinstance(section, dict):
            continue
        total = len(section)
        filled = sum(1 for v in section.values() if v not in ("", None, [], {}))
        pct = filled / total * 100 if total else 0
        if pct == 0:
            bar = "[red]empty[/red]"
        elif pct < 50:
            bar = f"[yellow]{pct:.0f}%[/yellow]"
        elif pct < 100:
            bar = f"[cyan]{pct:.0f}%[/cyan]"
        else:
            bar = "[green]100%[/green]"
        ctx_table.add_row(section_name, str(filled), str(total), bar)

    # ── Pipeline state ────────────────────────────────────────────────────────
    pipeline_data = _load_json(pipeline_path)

    pipeline_table = Table(title="Pipeline State", show_header=True, header_style="bold blue")
    pipeline_table.add_column("#", justify="right", style="dim")
    pipeline_table.add_column("Agent")
    pipeline_table.add_column("Group")
    pipeline_table.add_column("Status", justify="center")

    for i, agent in enumerate(PIPELINE_ORDER, 1):
        agent_data = pipeline_data.get(agent)
        if agent_data:
            meta = agent_data.get("_meta", {})
            gaps = meta.get("upstream_gaps", [])
            if gaps:
                status_text = Text("! gaps", style="yellow")
            else:
                status_text = Text("+ done", style="green")
        else:
            status_text = Text(". pending", style="dim")
        pipeline_table.add_row(str(i), agent, GROUP_MAP.get(agent, ""), status_text)

    # ── Research signals ──────────────────────────────────────────────────────
    signal_index = root / "research" / "index" / "signal_index.jsonl"
    signal_count = 0
    mock_count = 0
    if signal_index.exists():
        for line in signal_index.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                signal_count += 1
                if obj.get("is_mock"):
                    mock_count += 1
            except Exception:
                pass

    console.print()
    console.print(Panel(
        f"Context fill: [bold]{fill_pct:.0f}%[/bold]   "
        f"Signals: [bold]{signal_count}[/bold] "
        f"([dim]{mock_count} mock / {signal_count - mock_count} live[/dim])",
        title=f"agent-forge status  [dim]{root.name}[/dim]",
        border_style="blue",
    ))
    console.print(ctx_table)
    console.print()
    console.print(pipeline_table)
    console.print()


@app.command(name="list")
def list_agents():
    """List all available agents grouped by pipeline phase."""
    table = Table(title="Available Agents", show_header=True, header_style="bold")
    table.add_column("#", justify="right", style="dim")
    table.add_column("Agent")
    table.add_column("Group")
    table.add_column("Run command", style="dim cyan")

    for i, agent in enumerate(PIPELINE_ORDER, 1):
        table.add_row(
            str(i),
            agent,
            GROUP_MAP.get(agent, ""),
            f"agent-forge run {agent}",
        )
    console.print(table)


@app.command()
def context(
    set_key: Optional[str] = typer.Option(None, "--set", help="key.subkey=value, e.g. expert.niche='AI automation'"),
    show: bool = typer.Option(False, "--show", help="Pretty-print the current context"),
):
    """View or edit business_context.yaml fields."""
    root = _find_project_root()
    ctx_path = root / "business_context.yaml"

    if not ctx_path.exists():
        console.print(f"[red]business_context.yaml not found in {root}[/red]")
        raise typer.Exit(1)

    if show or not set_key:
        import sys as _sys
        _sys.path.insert(0, str(root))
        try:
            from core.schema import load_yaml
            data = load_yaml(ctx_path)
        except Exception:
            data = json.loads(ctx_path.read_text(encoding="utf-8"))

        for section, values in data.items():
            if not isinstance(values, dict):
                continue
            console.print(f"\n[bold magenta]{section}[/bold magenta]")
            for k, v in values.items():
                display = str(v) if v not in ("", None, [], {}) else "[dim](empty)[/dim]"
                console.print(f"  [cyan]{k}[/cyan]: {display}")
        return

    if set_key:
        if "=" not in set_key:
            console.print("[red]--set requires key.subkey=value format[/red]")
            raise typer.Exit(1)
        path_part, _, value = set_key.partition("=")
        parts = path_part.strip().split(".")
        if len(parts) != 2:
            console.print("[red]Key must be section.field, e.g. expert.niche[/red]")
            raise typer.Exit(1)

        import sys as _sys
        _sys.path.insert(0, str(root))
        try:
            from core.schema import load_yaml
            data = load_yaml(ctx_path)
        except Exception:
            data = json.loads(ctx_path.read_text(encoding="utf-8"))

        section, field = parts
        if section not in data:
            console.print(f"[red]Unknown section: {section}[/red]")
            raise typer.Exit(1)
        data[section][field] = value.strip("'\"")
        ctx_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        console.print(f"[green]OK[/green] Set [cyan]{section}.{field}[/cyan] = {value}")


if __name__ == "__main__":
    app()
