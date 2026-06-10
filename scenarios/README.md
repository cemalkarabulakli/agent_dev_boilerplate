# Scenarios

Example `business_context.example.yaml` files for different niches showing what a filled context looks like.

**`business_context.yaml` files are gitignored** — your real data stays local and is never committed. Only the `.example` files are committed to the repo.

## How to use

1. Copy the scenario's example file as a starting point:

   ```bash
   # macOS/Linux
   cp scenarios/ai_automation_balkans/business_context.example.yaml business_context.yaml

   # Windows PowerShell
   Copy-Item scenarios\ai_automation_balkans\business_context.example.yaml business_context.yaml

   # Or pass directly without touching root context
   python scripts/run_full_business_build.py --context scenarios\ai_automation_balkans\business_context.yaml
   ```

2. Fill in your real data in `business_context.yaml` — it will never be committed.

3. Run any individual agent or the full pipeline:

   ```bash
   python scripts/run_full_business_build.py --mode mock
   python scripts/run_full_business_build.py --mode api
   python scripts/generate_market_scorecard.py
   ```

4. See each scenario's `use_case.md` for niche-specific CLI recipes.

---

## Scenarios

| Folder                      | Niche                            | Ideal for                                                    |
| --------------------------- | -------------------------------- | ------------------------------------------------------------ |
| `ai_automation_balkans/`    | AI process automation for SMBs   | Software engineers, automation specialists, ops consultants  |

Add your own scenario by creating a new folder with `business_context.example.yaml` and `use_case.md`.
