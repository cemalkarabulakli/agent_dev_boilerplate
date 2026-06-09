# Scenarios

Pre-filled `business_context.yaml` files for three different niches.
Each scenario is ready to drop into the pipeline.

## How to use

1. Copy the scenario's `business_context.yaml` to the project root (or pass it via `--context`):

```bash
# Option A — replace root context
copy scenarios\fitness_coaching\business_context.yaml business_context.yaml

# Option B — pass directly (non-destructive)
python scripts/run_full_business_build.py --context scenarios\fitness_coaching\business_context.yaml
```

2. Run any individual agent or the full pipeline:

```bash
# Full pipeline (mock, free)
python scripts/run_full_business_build.py --context scenarios\fitness_coaching\business_context.yaml

# Full pipeline (real Claude API)
python scripts/run_full_business_build.py --context scenarios\fitness_coaching\business_context.yaml --mode api

# Single agent
python scripts/generate_market_scorecard.py --context scenarios\fitness_coaching\business_context.yaml
```

3. See each scenario's `use_case.md` for niche-specific CLI recipes.

---

## Scenarios

| Folder | Niche | Ideal for |
|---|---|---|
| `fitness_coaching/` | Online fitness coaching for busy professionals | Trainers, nutrition coaches, wellness experts |
| `b2b_sales_training/` | B2B SaaS sales training for founders & AEs | Ex-enterprise sellers, sales coaches, GTM advisors |
| `ecommerce_scaling/` | E-commerce brand scaling (Shopify $10k → $100k/mo) | DTC operators, brand builders, e-com consultants |
