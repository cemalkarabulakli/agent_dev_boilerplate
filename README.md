# Local-First Agent Template System

A reusable template system for building many professional AI agents without hardcoding personal or business-specific data.

The system is intentionally local-first:

- Agent definitions live in files.
- Memory starts as JSONL, JSON, and Markdown.
- Knowledge bases start as source manifests and local documents.
- Checklists and evals run deterministically before any real LLM integration is enabled.
- GitHub Actions run structure, quality, and eval checks on every push.

## What This Is

This repository is a factory for creating role-based agents such as CTO, marketer, Meta Ads expert, researcher, SEO, copywriter, support, or finance analyst agents.

The architecture follows the practical agent pattern:

`agent = model + instructions + tools + guardrails + memory/context`

The default runtime is a local deterministic mock. Real providers can be added later through explicit environment configuration.

## Business Growth Advisory Lens

The base template is tuned for a distinct business-growth operator mindset, not a copy of any living public figure.

Every generated agent should:

- Start with offer clarity before optimizing traffic, tools, prompts, or automation.
- Diagnose the current constraint before recommending tactics.
- Clarify the audience, painful problem, desired outcome, offer, channel, conversion path, economics, and execution bottleneck.
- Turn advice into concrete actions, success metrics, risks, and review points.
- Separate facts, assumptions, and recommendations.
- Avoid impersonating or copying the exact voice of any living public figure.

When creating new agents, the template treats the agent like a business asset: define the user, the expensive problem, the promised outcome, the tools needed, the memory policy, and the evals that prove the agent is useful.

The default operating order is:

1. Offer: buyer, painful problem, desired outcome, promise, proof, risk reduction, delivery constraints, and why the offer is compelling now.
2. Demand: audience access, channel, message, attention, lead quality, and qualification.
3. Money Model: pricing, conversion path, margin, payback period, retention, expansion, and unit economics.
4. Scale: repeatable systems, bottlenecks, quality controls, delegation, automation, and metrics.

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .[dev]
```

On macOS/Linux, activate with:

```bash
source .venv/bin/activate
```

## Create A New Agent

```bash
python scripts/create_agent.py --name product_manager --role "Product Manager"
```

This copies `agents/_template` into `agents/product_manager`, updates the role metadata, and creates starter memory, knowledge, eval, tool, and output files.

Use `--force` only when you intentionally want to replace an existing generated agent.

## Run An Agent

```bash
python scripts/run_agent.py --agent meta_ads_expert --message "Review this ad idea for clarity and risk."
```

By default this uses the local mock runner. It still exercises the agent loop:

1. Load agent config.
2. Load system prompt.
3. Load knowledge source metadata.
4. Load compacted context and recent memory.
5. Produce a deterministic local response.
6. Save raw interaction history.
7. Save candidate memory for review.
8. Compact context when configured thresholds are exceeded.
9. Run checklists.
10. Save quality reports.

## Memory

Each agent has a `memory/` directory:

- `raw_history.jsonl`: append-only raw turns. Never delete this as part of compaction.
- `session_notes.md`: temporary session-level notes.
- `long_term_memory.json`: reviewed memory entries.
- `compacted_context.md`: regenerated working context for model input.

Long-term memory entries use this shape:

```json
{
  "id": "mem_...",
  "type": "preference",
  "text": "The durable fact or preference.",
  "source": "raw_history",
  "confidence": 0.8,
  "created_at": "2026-05-21T12:00:00Z",
  "updated_at": "2026-05-21T12:00:00Z",
  "status": "candidate"
}
```

Entries start as `candidate` when `require_memory_review` is true. Promote them to `accepted` only after review.

## Context Compaction

Run compaction manually:

```bash
python scripts/compact_context.py --agent meta_ads_expert
```

The compactor does not loosely summarize everything. It:

- Keeps the last configured user turns verbatim.
- Extracts durable facts, decisions, constraints, source references, risks, and open tasks.
- Removes greetings, duplicate confirmations, stale exploration, and verbose tool output.
- Writes `memory/compacted_context.md`.
- Writes a validation report under `reports/`.

The raw history remains append-only and is not destroyed.

## Checklist-Based Self-Optimization

Run checklists:

```bash
python scripts/run_checklist.py --agent meta_ads_expert
```

The checklist runner validates:

- Agent folder structure.
- Prompt quality sections.
- Context compaction settings.
- Knowledge source metadata.
- Safety and tool guardrails.
- GitHub readiness.

Critical failures exit non-zero so CI can block unsafe changes.

## Evals

Run evals:

```bash
python scripts/run_evals.py --agent meta_ads_expert
```

The v1 eval runner is deterministic. It verifies required and forbidden terms against the local mock response and can be upgraded later to real model-based evals.

## Knowledge Bases

Each agent has:

```text
knowledge/
  sources.yaml
  raw/
  processed/
```

Add official, internal, or user-provided source metadata to `sources.yaml`. Put downloaded or summarized documents in `processed/`. The system does not treat unsourced knowledge as fact.

Example source:

```yaml
sources:
  - id: meta_business_help_center
    title: "Meta Business Help Center"
    type: "official_docs"
    url: "https://www.facebook.com/business/help"
    status: "placeholder"
    notes: "Add downloaded or summarized official docs here."
```

If no source exists for a claim, the agent must present it as a recommendation or assumption, not as a fact.

## Avoiding Personal Data

- Do not commit `.env`.
- Do not place personal information in agent templates.
- Keep business-specific files out of the reusable template.
- Store local secrets only in ignored environment files.
- Review candidate memories before accepting them into long-term memory.

## Real LLM Providers Later

Copy `.env.example` to `.env` and configure provider settings only when you are ready to add a real integration.

The current v1 scaffold intentionally does not call external APIs. It is structured so a provider adapter can later be added behind explicit environment flags.

## GitHub Actions

The workflows are:

- `ci.yml`: runs on push and pull request. Installs dependencies, runs tests, validates agent structure, and runs checklists.
- `agent-quality-check.yml`: runs on push. Runs checklists and evals, then uploads reports.
- `scheduled-optimization.yml`: runs daily at `17 3 * * *` UTC and manually through `workflow_dispatch`. It compacts contexts, rebuilds knowledge indexes, runs evals, and uploads reports.
- `readme-project-scan.yml`: runs daily at `23 4 * * *` UTC and manually through `workflow_dispatch`. It updates the generated project scan section and opens a PR when project files changed.

The scheduled workflow does not commit to `main` by default. Auto-PR behavior is only scaffolded behind explicit configuration.

## Useful Commands

```bash
python scripts/validate_agent_structure.py
python scripts/run_checklist.py --all
python scripts/run_evals.py --all
python scripts/update_knowledge_index.py --all
python scripts/update_readme_project_scan.py --check
python -m pytest
```

<!-- PROJECT_SCAN:START -->
## Project Scan

This section is machine-generated by `scripts/update_readme_project_scan.py`.

Last scan: 2026-05-21T13:31:26Z

- Files scanned: 101
- Agents: cto, meta_ads_expert, researcher
- Workflows: agent-quality-check.yml, ci.yml, readme-project-scan.yml, scheduled-optimization.yml

### Changes Since Last Scan
- Added: tests/test_business_growth_lens.py
- Changed: agents/_template/agent.yaml, agents/_template/evals/eval_cases.yaml, agents/_template/system_prompt.md, agents/cto/agent.yaml, agents/cto/evals/eval_cases.yaml, agents/cto/system_prompt.md, agents/meta_ads_expert/agent.yaml, agents/meta_ads_expert/evals/eval_cases.yaml, agents/meta_ads_expert/system_prompt.md, agents/researcher/agent.yaml, agents/researcher/evals/eval_cases.yaml, agents/researcher/system_prompt.md, checklists/global_agent_best_practices.yaml, core/checklist_runner.py, core/eval_runner.py, core/guardrails.py, prompts/agent_self_review_prompt.md, prompts/eval_generation_prompt.md, scripts/create_agent.py
- Deleted: None
<!-- PROJECT_SCAN:END -->

