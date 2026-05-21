You are a senior AI systems architect and production-grade software engineer.

Build a reusable LOCAL-FIRST agent template system.

The goal is NOT to build one specific agent.
The goal is to build a template/factory that lets me create many professional agents such as:

- CTO Agent
- Marketer Agent
- Meta Ads Expert Agent
- Researcher Agent
- Product Manager Agent
- SEO Agent
- Copywriter Agent
- Customer Support Agent
- Finance Analyst Agent

The generated system must be reusable, role-based, self-learning, self-optimizing, and safe.

Important:
- Do NOT include my personal data.
- Do NOT hardcode business-specific data.
- The template can include example agents and example knowledge bases.
- Example: include a built-in Meta Ads Agent with a sample official-knowledge placeholder structure, but do not add fake facts.
- The system must be ready to push to GitHub.
- The system must include GitHub Actions workflows that run checks after every push and on a schedule.

Use official AI-provider architecture ideas:
- Agent = model + instructions + tools + guardrails + memory/context.
- Use a clean folder structure.
- Use context compaction.
- Use checklist-based self-review.
- Use tests/evals.
- Use structured outputs where possible.
- Use guardrails for input, output, and tool execution.

Architecture style:
- Simple
- Local-first
- File-based memory and knowledge base first
- Easy to upgrade later to vector DB, Postgres, Supabase, or external APIs
- Python preferred
- No unnecessary framework complexity
- Production-ready but not over-engineered

Create the following repository structure:

agent-template-system/
  README.md
  .gitignore
  .env.example
  pyproject.toml or requirements.txt

  agents/
    _template/
      agent.yaml
      system_prompt.md
      checklist.yaml
      knowledge/
        README.md
        sources.yaml
        raw/
        processed/
      memory/
        long_term_memory.json
        session_notes.md
        compacted_context.md
      tools/
        README.md
      evals/
        eval_cases.yaml
      outputs/
        README.md

    meta_ads_expert/
      agent.yaml
      system_prompt.md
      checklist.yaml
      knowledge/
        README.md
        sources.yaml
        raw/
        processed/
      memory/
        long_term_memory.json
        session_notes.md
        compacted_context.md
      tools/
      evals/
        eval_cases.yaml
      outputs/

    cto/
      agent.yaml
      system_prompt.md
      checklist.yaml
      knowledge/
      memory/
      tools/
      evals/
      outputs/

    researcher/
      agent.yaml
      system_prompt.md
      checklist.yaml
      knowledge/
      memory/
      tools/
      evals/
      outputs/

  core/
    agent_loader.py
    schema.py
    context_compactor.py
    memory_manager.py
    knowledge_loader.py
    checklist_runner.py
    eval_runner.py
    guardrails.py
    tool_registry.py
    logger.py

  scripts/
    create_agent.py
    run_agent.py
    compact_context.py
    run_checklist.py
    run_evals.py
    update_knowledge_index.py
    validate_agent_structure.py

  checklists/
    global_agent_best_practices.yaml
    context_compaction_checklist.yaml
    knowledge_base_checklist.yaml
    tool_safety_checklist.yaml
    github_ready_checklist.yaml

  prompts/
    compact_context_prompt.md
    agent_self_review_prompt.md
    knowledge_extract_prompt.md
    eval_generation_prompt.md

  tests/
    test_agent_structure.py
    test_context_compaction.py
    test_checklists.py
    test_memory_manager.py

  .github/
    workflows/
      ci.yml
      scheduled-optimization.yml
      agent-quality-check.yml

Core requirements:

1. Agent definition

Each agent must have an `agent.yaml` like this:

name: meta_ads_expert
role: "Meta Ads Expert"
description: "Helps plan, review, and improve Meta Ads strategy using official knowledge sources and safe reasoning."
version: "0.1.0"
model:
  provider: "openai"
  name: "gpt-4.1-mini"
context:
  keep_last_n_turns: 5
  compact_when_tokens_exceed: 12000
  tool_output_trim_chars: 3000
memory:
  mode: "file"
  allow_learning: true
  require_memory_review: true
knowledge:
  sources_file: "knowledge/sources.yaml"
  require_source_citations: true
tools:
  allowed:
    - read_knowledge
    - save_memory_note
    - compact_context
guardrails:
  input:
    - no_private_data_required
    - no_illegal_or_harmful_requests
  output:
    - no_fake_claims
    - cite_sources_when_using_knowledge
    - separate_fact_from_recommendation

2. System prompt template

Each agent must have a `system_prompt.md` with sections:

# Role
# Goal
# Operating Principles
# Allowed Knowledge
# Memory Rules
# Context Compaction Rules
# Tool Rules
# Output Format
# Refusal / Safety Rules
# Self-Review Checklist

The template must be role-neutral so I can clone it for new agents.

3. Context compaction best practice

Implement `core/context_compactor.py`.

The context compactor must NOT simply summarize everything loosely.

It must preserve special data and remove useless noise.

Use this strategy:

A. Keep recent turns verbatim
- Keep last N user turns exactly as-is.
- N is configured per agent.

B. Extract durable facts
Extract and preserve:
- user goals
- agent role decisions
- constraints
- preferences
- important numbers
- deadlines
- selected strategy
- rejected strategy
- open questions
- unresolved tasks
- tool results that are still relevant
- source references
- assumptions
- decisions and rationale
- important examples
- warnings or risks

C. Remove noise
Remove:
- greetings
- repeated confirmations
- failed attempts with no useful lesson
- verbose tool output
- duplicate explanations
- temporary exploration that is no longer relevant
- irrelevant conversation fragments

D. Keep raw history outside context
- Save full raw session history separately.
- Never destroy raw history.
- Compacted context is only for model input.
- Long-term memory stores durable facts.
- Session notes store temporary facts.
- Compacted context stores compressed working context.

E. Use structured JSON/Markdown output
The compacted context must have this format:

# Compacted Context

## Current Goal
...

## Agent Role
...

## Durable Facts
- ...

## User / Project Constraints
- ...

## Decisions Made
- Decision:
  Rationale:
  Date/Session:

## Open Tasks
- ...

## Important Source References
- ...

## Recent Verbatim Turns
<last N turns>

## Do Not Forget
- ...

## Removed Noise
- short explanation of what was intentionally removed

F. Add validation
After compaction, run a validation step:
- Does the compacted context preserve all “must keep” fields?
- Are numbers, names, dates, and decisions preserved?
- Are source references preserved?
- Are recent turns preserved verbatim?
- Is private data handled according to config?
- Did the compactor invent anything? If yes, fail.

4. Memory system

Implement `core/memory_manager.py`.

Memory types:
- raw_history.jsonl
- session_notes.md
- long_term_memory.json
- compacted_context.md

Rules:
- raw_history is append-only
- compacted_context can be regenerated
- long_term_memory requires review flag before accepting durable facts
- memory entries must have:
  - id
  - type
  - text
  - source
  - confidence
  - created_at
  - updated_at
  - status: candidate | accepted | rejected

5. Knowledge base

Implement `core/knowledge_loader.py`.

Each agent has `knowledge/sources.yaml`.

Example:

sources:
  - id: meta_business_help_center
    title: "Meta Business Help Center"
    type: "official_docs"
    url: "https://www.facebook.com/business/help"
    status: "placeholder"
    notes: "Add downloaded or summarized official docs here."

Rules:
- Knowledge base must distinguish official, internal, and user-provided sources.
- Do not treat unsourced knowledge as fact.
- Agent must cite source IDs when answering from knowledge.
- If no source exists, answer as recommendation or assumption, not fact.

6. Checklist system

Implement `core/checklist_runner.py`.

There must be global and per-agent checklists.

Global checklist must check:

Agent Structure:
- agent.yaml exists
- system_prompt.md exists
- checklist.yaml exists
- knowledge folder exists
- memory folder exists
- evals folder exists

Prompt Quality:
- role is clear
- goal is clear
- output format is clear
- tool rules are clear
- memory rules are clear
- source/citation rules are clear

Context Compaction:
- keep_last_n_turns configured
- compact_when_tokens_exceed configured
- durable facts list exists
- raw history is not deleted
- compacted context has validation

Knowledge:
- sources.yaml exists
- source IDs are defined
- official/user/internal source types are separated
- no fake source URLs

Safety:
- tool permissions are explicit
- destructive tools require confirmation
- output guardrails exist
- no secrets in repo

GitHub:
- tests run on push
- checklist runs on push
- scheduled optimization exists
- .env is ignored
- .env.example exists

7. Self-learning / self-optimizing loop

Implement this loop:

On every agent run:
1. Load agent config
2. Load system prompt
3. Load relevant knowledge
4. Load compacted context
5. Load recent memory/session notes
6. Run agent
7. Save raw interaction
8. Extract candidate memories
9. Save candidate memories for review
10. Compact context if threshold reached
11. Run checklist
12. Save quality report

On every GitHub push:
1. Validate folder structure
2. Run tests
3. Run checklist
4. Run evals
5. Fail if required quality checks fail

On schedule:
1. Re-run checklists
2. Re-compact stale sessions
3. Rebuild knowledge index
4. Generate optimization report
5. Optionally open a PR with improvements, but do not auto-change critical prompts unless explicitly configured

8. GitHub Actions

Create `.github/workflows/ci.yml`:

- trigger: push, pull_request
- install dependencies
- run tests
- validate agent structure
- run global checklist

Create `.github/workflows/agent-quality-check.yml`:

- trigger: push
- run scripts/run_checklist.py
- run scripts/run_evals.py
- upload quality report artifact

Create `.github/workflows/scheduled-optimization.yml`:

- trigger:
  - schedule, daily at non-peak UTC time
  - workflow_dispatch
- run compact_context
- update knowledge index
- run evals
- generate report

Important GitHub Actions behavior:
- Use non-hour cron time like 17 3 * * *.
- Use workflow_dispatch for manual runs.
- Do not commit changes automatically by default.
- Generate reports as artifacts.
- If auto-PR mode is enabled by config, create branch and PR instead of pushing to main.

9. Scripts

Implement:

scripts/create_agent.py
- CLI command:
  python scripts/create_agent.py --name "meta_ads_expert" --role "Meta Ads Expert"
- Copies agents/_template into agents/{name}
- Replaces placeholders
- Creates folders and starter files

scripts/run_agent.py
- CLI command:
  python scripts/run_agent.py --agent meta_ads_expert --message "Review this ad idea..."
- Loads config
- Runs agent mock or real provider depending on env
- Saves raw history
- Saves candidate memory
- Runs compaction if needed

scripts/compact_context.py
- CLI:
  python scripts/compact_context.py --agent meta_ads_expert
- Reads raw history/session notes
- Keeps last N turns verbatim
- Extracts durable facts
- Removes noise
- Writes compacted_context.md
- Writes validation report

scripts/run_checklist.py
- CLI:
  python scripts/run_checklist.py --agent meta_ads_expert
- Runs global and agent checklist
- Writes reports/{agent}_checklist_report.md
- Exits non-zero if critical checks fail

scripts/run_evals.py
- CLI:
  python scripts/run_evals.py --agent meta_ads_expert
- Reads eval cases
- Runs mock deterministic eval first
- Supports real LLM eval later

10. Compact context prompt

Create `prompts/compact_context_prompt.md`.

The prompt must say:

You are compacting context for an AI agent.
Your job is to reduce tokens without losing important state.

Rules:
- Do not invent facts.
- Do not remove user goals, constraints, preferences, decisions, deadlines, numbers, source references, or unresolved tasks.
- Keep last N user turns verbatim.
- Remove noise, repetition, greetings, failed attempts with no useful lesson, and verbose tool outputs.
- Preserve exact names, dates, IDs, metrics, and decisions.
- If unsure whether something is important, keep it under “Do Not Forget”.
- Separate facts from assumptions.
- Output only the required Markdown structure.

Output structure:
# Compacted Context
## Current Goal
## Agent Role
## Durable Facts
## User / Project Constraints
## Decisions Made
## Open Tasks
## Important Source References
## Recent Verbatim Turns
## Do Not Forget
## Removed Noise
## Validation Checklist

11. Tests

Write tests that verify:

- create_agent creates valid structure
- agent.yaml validates against schema
- compact_context keeps recent turns
- compact_context preserves must-keep facts
- compact_context removes noise
- memory entries include status and confidence
- checklist fails when required files are missing
- GitHub workflow files exist

12. README

README must explain:

- What this system is
- How to create a new agent
- How to run an agent
- How memory works
- How context compaction works
- How checklist-based self-optimization works
- How GitHub Actions work
- How to add a knowledge base
- How to add official sources
- How to avoid personal data
- How to enable real LLM provider later

13. Design principles

Keep it simple:
- File-based first
- No database required
- No vector DB required in v1
- No fake APIs
- No fake claims
- Use placeholders where real integration is needed
- Strong comments
- Clean code
- Type hints
- Pydantic or dataclasses for schema validation
- Deterministic tests

14. Deliverables

Generate all files.
Make the repository runnable locally.

After generation, show:
- folder tree
- how to install
- how to create a new agent
- how to run checklist
- how to run context compaction
- how GitHub Actions will behave

Do not stop after explaining.
Actually create the full codebase.