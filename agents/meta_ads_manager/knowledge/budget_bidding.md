# Budget and Bidding Strategies

## The Four Core Bid Strategies

### 1. Lowest Cost (Automatic Bidding)
- Algorithm maximizes conversions within budget — no cost constraints
- Best for: New campaigns, learning phase, initial data collection
- Learning phase: Exits fastest (maximum algorithm flexibility)
- Limitation: CPA inflates unpredictably at scale; no cost ceiling

### 2. Cost Cap
- Maintains **average** cost at or below cap — not per-auction
- Set cap: 10–20% above baseline CPA established during Lowest Cost phase
- Requires: 50–100 conversions minimum before setting a realistic cap
- Best for: Mature campaigns needing predictable acquisition cost
- Natural scaling safeguard: extra budget only spends if opportunities meet the cap

### 3. Bid Cap
- Absolute maximum bid per individual auction (not per conversion)
- Never bids above this per auction regardless of opportunity
- Best for: Affiliate marketing, fixed-margin-per-unit business models
- Warning: Severely limits delivery if cap is below market clearing price; campaigns may spend $0
- Requires 50+ conversions and strong CPA data before use

### 4. ROAS Target
- Optimizes for revenue value rather than conversion volume
- Requires: Pixel/CAPI passing accurate purchase values in event payload
- Target calculation: Break-even ROAS = 1 ÷ profit_margin; set 10–20% above current ROAS
- Best for: E-commerce with varied product prices, catalog sales
- Learning phase: Longest to stabilize of all strategies

### Bidding Strategy by Conversion Volume

| Conversion Volume (past 30 days) | Recommended Strategy |
| --- | --- |
| 0–50 conversions | Lowest Cost — collect data, protect learning |
| 50–200 conversions | Cost Cap — predictable CPA |
| 200+ conversions, variable order values | ROAS Target |
| Fixed margin per unit (affiliate, etc.) | Bid Cap (advanced) |

**Andromeda rule:** Never use Cost Cap or ROAS Target with insufficient conversion volume. Setting a cap before the algorithm has enough data causes delivery to stall in learning phase indefinitely.

## Learning Phase Rules

### The 50-Conversion Threshold
Andromeda requires approximately 50 optimization events within a 7-day window to exit learning phase. Below this, delivery is unstable and performance data is unreliable.

**Minimum budget to support learning phase exit:**
```
Weekly budget ≥ 50 × target CPA
```
Example: If target CPA is $30 → Weekly budget must be at least $1,500.

### What Resets the Learning Phase (Never Do These While in Learning)
- Changing bid strategy
- Adjusting bid/cost cap by more than 20%
- Significant targeting modifications (interest changes, audience swaps)
- Substantial creative changes (replacing all active ads)
- Pausing the campaign for 7+ days
- Budget increase greater than 50% in a single change

### Learning Phase Best Practices
- Do not evaluate performance during learning — data is unreliable
- Lowest Cost exits learning fastest
- Restrict strategies (Bid Cap) can keep campaigns in learning indefinitely
- After any budget change: wait 3 full days before judging performance again
- If stuck in learning: add more budget (closer to 50x CPA threshold) or add more creatives

## Scaling Strategies

### Vertical Scaling (increasing budget on current campaigns)
- Conservative: 20–30% increase every 48–72 hours
- Aggressive: 50–100% single jump (avoids repeated partial resets)
- Rule: change budget once, wait 3 full days before judging
- Healthy scale signal: CPA holds within 15% of baseline as budget increases

### Horizontal Scaling (new campaigns/ad sets)
- Duplicate winning campaign and assign 50–70% of original budget
- Prevents internal auction competition (your campaigns bidding against each other)
- Use for: New geographies, new creative concepts at scale, new audience segments
- New duplicates go through learning phase — expect 7-day instability

### Ready-to-Scale Signals
All of these must be true before scaling:
- [ ] Learning phase exited (50+ conversions achieved)
- [ ] CPA at or below target for 7+ consecutive days
- [ ] Frequency below 3.0 in cold prospecting
- [ ] CAPI + Pixel confirmed working (EMQ 7.0+)
- [ ] Creative portfolio not fatigued (Hook Rate above 20%)

## Budget Pacing Notes
- Meta spends budget across the day based on predicted opportunities
- Daily budgets can overspend by up to 25% on high-opportunity days (within weekly average — legally compliant)
- Lifetime budgets give most control over total spend but require end dates
- CBO may allocate $0 to some ad sets if algorithm predicts poor ROI — this is expected behavior

## ASC Minimum Budget
- Absolute minimum: $50/day
- Functional minimum for reliable learning: $100–200/day
- Scale-ready minimum: Weekly budget ≥ 50x target CPA
