# High-Ticket Expert Growth System

A reusable local-first AI agent system for experts who want to build, improve, and scale a high-ticket business without hardcoded personal data, fake proof, or manipulative marketing.

## What This System Is

This repository is a file-based agent template system for experts who sell transformation, expertise, trust, strategy, implementation, consulting, coaching, education, courses, communities, templates, done-for-you services, or done-with-you services.

It uses deterministic mock mode by default, so every script can run without API keys.

## Who It Is For

- Coaches, consultants, educators, strategists, creators, and service experts.
- Operators building high-ticket offers and delivery systems.
- Builders who want reusable specialist agents for market, avatar, offer, acquisition, funnel, sales, delivery, proof, retention, and scorecards.

## What Problems It Solves

- Choosing a better market.
- Clarifying the customer avatar.
- Building a stronger high-ticket offer.
- Improving value stack, pricing, guarantee, proof, acquisition, funnel, sales, delivery, retention, and business scorecard.

## High-Ticket Business Flow

`market -> avatar -> painful problem -> high-value offer -> proof -> acquisition -> sales system -> delivery system -> retention -> scale`

## Folder Structure

```text
agents/      Specialist agents and the base template
core/        Python runtime, schemas, memory, compaction, guardrails, checklists
knowledge/   Local high-ticket business knowledge placeholders
prompts/     Prompt templates for each workflow
checklists/  YAML-based quality gates
scripts/     CLI commands for generation and validation
outputs/     Generated local artifacts
tests/       Pytest suite
```

## Install

```bash
pip install -r requirements.txt
```

## Edit business_context.yaml

Start with `business_context.yaml`. Fill only what you know. Leave unknown fields blank and the agents will label missing data instead of inventing facts.

## Create A New Expert Agent

```bash
python scripts/create_agent.py --name sales_page_reviewer --role "Sales Page Reviewer"
```

## Run Generators

```bash
python scripts/generate_market_scorecard.py --agent market_selector --context business_context.yaml
python scripts/generate_avatar_research.py --agent avatar_pain_researcher --context business_context.yaml
python scripts/generate_offer_audit.py --agent offer_architect --context business_context.yaml
python scripts/generate_value_stack.py --agent value_stack_builder --context business_context.yaml
python scripts/generate_pricing_guarantee_review.py --agent pricing_guarantee_optimizer --context business_context.yaml
python scripts/generate_acquisition_plan.py --agent acquisition_strategy_agent --context business_context.yaml
python scripts/generate_content_plan.py --agent content_authority_agent --context business_context.yaml
python scripts/generate_funnel_map.py --agent funnel_builder --context business_context.yaml
python scripts/generate_sales_script.py --agent sales_script_builder --context business_context.yaml
python scripts/generate_objection_bank.py --agent objection_handler --context business_context.yaml
python scripts/generate_delivery_system.py --agent delivery_system_designer --context business_context.yaml
python scripts/generate_proof_engine.py --agent proof_engine_builder --context business_context.yaml
python scripts/generate_business_scorecard.py --agent business_scorecard_agent --context business_context.yaml
```

## Context Compaction

```bash
python scripts/compact_context.py --agent offer_architect
```

The compactor keeps recent user turns verbatim, preserves high-ticket business facts, removes noise, and never deletes `raw_history.jsonl`.

## Memory

Each agent stores `raw_history.jsonl`, `session_notes.md`, `long_term_memory.json`, and `compacted_context.md`. Candidate memories are not automatically accepted as facts.

## Checklist-Based Self-Optimization

```bash
python scripts/run_checklist.py --agent offer_architect
```

## GitHub Actions

- `ci.yml`: runs tests, YAML validation, and agent structure validation.
- `agent-quality-check.yml`: runs checklists and evals, then uploads quality reports.
- `scheduled-optimization.yml`: weekly at `17 3 * * 1` UTC, compacts contexts, runs checklists, and uploads reports.

Workflows do not auto-commit or push to `main` by default.

## Avoid Fake Claims

Do not invent claims, testimonials, scarcity, income promises, or guaranteed unrealistic results. Label assumptions clearly and collect real proof when proof is missing.

## Add A Real LLM Provider Later

Set provider values in `.env` and add a provider adapter behind the mock interface. The v1 system intentionally runs fully without API keys.
