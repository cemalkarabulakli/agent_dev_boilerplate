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
- `weekly-research.yml`: weekly at `23 4 * * 1` UTC, runs modular source collection in configured mode and uploads research artifacts.
- `source-integrity-check.yml`: validates research source structure, reference integrity, cross-source validation rules, and research source tests.

Workflows do not auto-commit or push to `main` by default.

## V4 Modular Multi-Source Research Engine

V4 adds a modular research engine for collecting market signals from source adapters. It is designed for evidence-driven high-ticket business research and runs in mock mode unless a source is explicitly configured for API, scrape, or manual collection.

Supported source modules:

- Quora: customer questions, pain language, objections, education gaps.
- BG-Mamma: Bulgarian community language, local trust objections, family and lifestyle discussions.
- Facebook Ad Library: competitor ads, ad angles, creative patterns, offer positioning.
- Reddit: raw pain language, objections, buying frustrations, tool mentions.
- Google Trends: demand direction, seasonality, regional interest, related queries.
- GitHub Trends: new tools, open-source adoption, AI agent tooling signals.
- ClickBank: digital product categories, affiliate offer positioning, niche monetization signals.
- YouTube: content trends, titles, hooks, authority-building topics.
- Web Search: general research, official docs discovery, competitor and tool discovery.

Each source has its own adapter, `source_config.yaml`, raw folder, processed folder, and report folder under `research/sources/{source}/`. New sources can be added without rewriting the collector.

Raw source output is stored separately and never enters agent context directly. Only processed signals with `reference_ids`, confidence scores, source labels, and candidate or validated status can be used in compacted context or strategy reports. Human review is required before candidate insights update business strategy.

References are appended to `research/index/collected_references.jsonl`. Every raw signal has a `reference_id`, every processed signal has `reference_ids`, and every report has a references section. In mock mode, URLs use `mock://...` and are labeled as mock.

Cross-source validation uses source count and confidence:

- 1 source: candidate.
- 2 independent sources: stronger candidate.
- 3 or more independent sources: validated if source quality is acceptable.
- Google Trends + Reddit + YouTube is strong for demand and content signals.
- Facebook Ad Library + ClickBank is strong for offer and ad signals.
- GitHub Trends + Web Search is strong for tool signals.

### Research Commands

```bash
python scripts/collect_source.py --source reddit --query "coaches struggling to get clients"
python scripts/collect_source.py --source bg_mamma --query "детски английски курс"
python scripts/collect_source.py --source facebook_ad_library --query "fitness coaching"
python scripts/collect_source.py --source youtube --query "high ticket coaching funnel"
python scripts/collect_all_sources.py --category high_ticket_business
python scripts/analyze_cross_source_signals.py
python scripts/add_research_source.py --id tiktok --name "TikTok" --type "short_video"
python scripts/run_weekly_research.py
```

Generated research reports are written to:

- Per-source reports: `research/sources/{source}/reports/`
- Cross-source reports: `research/processed/cross_source_reports/` and `outputs/cross_source_reports/`
- Weekly reports: `outputs/weekly_reports/`

## Avoid Fake Claims

Do not invent claims, testimonials, scarcity, income promises, or guaranteed unrealistic results. Label assumptions clearly and collect real proof when proof is missing.

## Add A Real LLM Provider Later

Set provider values in `.env` and add a provider adapter behind the mock interface. The v1 system intentionally runs fully without API keys.
