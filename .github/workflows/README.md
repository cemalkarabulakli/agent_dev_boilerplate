# CI/CD Workflows

Seven GitHub Actions workflows cover quality gates, scheduled automation, and package releases.

---

## On Every Push and Pull Request

### CI (`ci.yml`)

The baseline gate. Blocks merges if anything here fails.

| Step | What it does |
|---|---|
| Setup Python 3.12 | Pins the runtime to match local dev |
| Install dependencies | `pip install -r requirements.txt` |
| Run tests | `pytest` — catches broken Python logic |
| Validate YAML | Catches malformed agent YAML files before they silently break at runtime |
| Validate agent structure | Enforces required fields and schema across all agent directories |

### Source Integrity Check (`source-integrity-check.yml`)

Guards the research and data layer specifically. Runs the same checklist runner as the quality job but scoped to source-related checks.

| Step | What it checks |
|---|---|
| Research source checklist | Source adapters are properly configured |
| Reference integrity checklist | Collected signals have reference IDs and valid URLs |
| Cross-source validation checklist | Multi-source signals are correctly joined |
| Web tool provider checklist | Web tool adapters conform to provider contracts |
| Competitor monitoring checklist | Competitor source config is valid |
| Targeted pytest suite | `test_research_sources`, `test_web_tool_interfaces`, `test_web_tool_registry`, `test_source_provider_registry`, `test_competitor_monitoring` |

---

## On Every Push

### Agent Quality Check (`agent-quality-check.yml`)

Goes deeper than CI — checks output quality, not just structure.

| Step | What it does |
|---|---|
| Run checklists (`--all`) | Runs all YAML checklists across every agent |
| Run evals (`--all`) | Scores agent outputs against eval cases |
| Upload quality reports | Saves `outputs/quality_reports/` as an artifact — uploads even on failure so degraded runs are inspectable |

CI checks that agents are valid. This checks that they are good.

---

## Scheduled

All three scheduled jobs use off-peak, non-round-number cron times to avoid GitHub's peak load.

### Scheduled Optimization (`scheduled-optimization.yml`)

**Schedule**: Mondays at 03:17 UTC — also triggerable manually via `workflow_dispatch`.

Keeps agent memory lean without manual intervention.

| Step | What it does |
|---|---|
| Compact contexts | Prunes and compresses agent memory files (`compact_context.py --all`) |
| Run checklists | Weekly hygiene pass across all agents |
| Upload optimization report | Artifact for inspection; nothing is committed back to the repo |

### Weekly Research (`weekly-research.yml`)

**Schedule**: Mondays at 04:23 UTC (1hr after optimization) — also triggerable manually.

Feeds agents with fresh market intelligence on a regular cadence.

| Step | What it does |
|---|---|
| Run weekly research | `run_weekly_research.py` — collects signals from all enabled sources and runs cross-source analysis |
| Upload artifacts | Weekly reports, cross-source reports, candidate insights, and `collected_references.jsonl` |

Outputs are stored as artifacts only. The repo stays clean.

### Competitor Monitoring (`competitor-monitoring.yml`)

**Schedule**: Tuesdays at 05:31 UTC — also triggerable manually.

Dedicated pulse on the target market, one day after general research.

| Step | What it does |
|---|---|
| Resolve competitor query | Reads `market_name` from `business_context.yaml`; falls back to `"high ticket expert offer"`. Override via `workflow_dispatch` `query` input. |
| Run competitor monitoring | `monitor_competitors.py --query <resolved>` |
| Upload artifacts | Results under `outputs/competitor_monitoring/` and `research/sources/competitors/` |

The query is derived from `market_name` in `business_context.yaml` when running on schedule. For manual runs, pass it as the `query` input via `workflow_dispatch`. Update `business_context.yaml` as the single source of truth rather than editing the workflow directly.

---

## On Version Tags

### Release (`release.yml`)

**Trigger**: any tag matching `v*.*.*` (e.g. `v1.2.0`).

Two-job pipeline — the build only runs if tests pass.

**Job 1 — test**

| Step | What it does |
|---|---|
| Install dev dependencies | `pip install -e ".[dev]"` |
| Run tests | `pytest` |
| Validate agent structure | Same check as CI |

**Job 2 — build-and-release** (runs only after test passes)

| Step | What it does |
|---|---|
| Install build tools | `pip install build` |
| Build package | `python -m build` — produces `dist/` |
| Create GitHub Release | Attaches `dist/*`, auto-generates release notes, includes install instructions |
| Publish to PyPI | `pypa/gh-action-pypi-publish` — uses OIDC trusted publishing (no stored API token) |

To cut a release:

```bash
git tag v1.2.0
git push origin v1.2.0
```

---

## Secrets Required

| Secret | Used by |
|---|---|
| `ANTHROPIC_API_KEY` | Any workflow that runs agents in API mode (currently none by default — CI uses mock mode) |
| PyPI trusted publishing (OIDC) | `release.yml` — configured on PyPI under the repo's trusted publisher settings, no secret needed |

---

## Running Locally

Each scheduled or quality script can be run directly without triggering GitHub Actions:

```bash
# Compact all agent contexts
python scripts/compact_context.py --all

# Run all checklists
python scripts/run_checklist.py --all

# Run all evals
python scripts/run_evals.py --all

# Run the weekly research pipeline
python scripts/run_weekly_research.py

# Run competitor monitoring
python scripts/monitor_competitors.py --query "high ticket expert offer"
```
