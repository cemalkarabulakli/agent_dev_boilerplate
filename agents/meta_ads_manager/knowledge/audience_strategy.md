# Audience Strategy — The Andromeda Era

## The 2025 Targeting Landscape

Targeting has fundamentally shifted in 2024–2025:
- Meta deprecated specific interest categories (June 23, 2025): categories like "EDM fans," "SUVs," "vegan food" merged into broad groups
- Detailed targeting exclusions removed from Ads Manager (March 2025)
- Meta now defaults to Advantage+ Audience
- Interest-based precision targeting is no longer a viable primary strategy

**The Andromeda principle:** Creative content is the primary audience signal. Andromeda uses creative to find the right users. Manual targeting is a "suggestion" to help Andromeda start — not a hard boundary on who can see your ads.

## Audience Types and Use Cases

### 1. Custom Audiences (First-Party Data) — Highest Signal Value

| Source | How to Create | Best Use |
| --- | --- | --- |
| Website Visitors | Meta Pixel events | Retargeting, exclusions from prospecting |
| Customer List | Upload CSV (email, phone, name) | Retention, upsell, lookalike seed |
| App Activity | SDK events | App re-engagement |
| Video Engagement | 3-sec, 25%/50%/75% completers | Warm audience sequencing |
| Lead Form Opens/Submits | Native to Meta | Lead nurturing |
| Instagram/Facebook Engagers | Profile visits, DMs, saves | Warm retargeting |

Minimum size for reliable performance: 1,000+ matched users.
For lookalike seed: 1,000–50,000 high-quality users (LTV-based, not all purchasers).

### 2. Advantage+ Audience — The New Default for Prospecting

- Provide age, location, and interest suggestions as a starting point
- Meta's AI expands beyond your suggestions when it finds better users
- Reportedly delivers **22% higher ROAS** vs. manual detailed targeting
- Enable for: cold prospecting, new customer acquisition
- Disable for: retargeting (prevents cannibalization of warm audiences)

**Setup guidance:**
- Suggestion inputs: demographics (age/gender), location, 3–5 interest/behavior hints as direction
- Do not over-constrain: broad suggestions let Andromeda explore freely
- Let it run 7–14 days before judging (learning phase)

### 3. Lookalike Audiences — Still Viable, Less Essential

- Meta auto-creates lookalike-style expansions in Advantage+ anyway
- Manual LALs most useful when you need precise control over seed quality
- 1% LAL = tightest match (smallest, highest similarity)
- 1–5% recommended for prospecting; 5–10% for scale
- In 2025: best used as "audience suggestions" inside Advantage+ rather than hard constraints

### 4. Detailed / Interest Targeting — Deprecated, Minimal Use

- "Limited reach" warnings now appear for many categories
- Remaining valid use cases: language-specific targeting, hyper-local geographic, niche B2B
- Primary use: directional hints for Advantage+ Audience, not hard targeting constraints

### 5. Broad Targeting (No Constraints)

- Only age, gender, country filters
- Andromeda + Advantage+ handle all audience discovery
- Best for: Large budgets ($50K+/month), proven creatives at scale
- Minimum recommended audience reach: 20M+

## Audience Exclusions (Still Critical)

- Exclude existing customers from cold prospecting (Custom Audience exclusion)
- Exclude recent purchasers (30–90 day window based on product repurchase cycle)
- Cannot exclude by interest/demographic categories anymore (removed March 2025)
- Use Custom Audiences (website visitors, customer lists) for exclusions

## Retargeting Strategy

In the Andromeda era, retargeting is about sequencing, not just re-exposure:

| Retargeting Segment | Window | Message Type |
| --- | --- | --- |
| Cart abandoners | 1–7 days | Direct offer + urgency |
| Product page viewers | 7–14 days | Social proof + benefits |
| Lead form openers (incomplete) | 1–3 days | Re-engage, simplify action |
| Engaged video viewers (25%+) | 14–30 days | Next-step awareness ad |
| Email list (matched) | Ongoing | Upsell, loyalty, referral |

**Frequency caps for retargeting:**
- Cart abandoners: 3–5/week maximum
- Warm engagers: 2–3/week maximum
- Avoid fatigue from over-retargeting same segment

## Audience Strategy by Campaign Stage

| Stage | Audience Approach | Why |
| --- | --- | --- |
| New brand, no data | Broad + Advantage+ Audience | Let Andromeda find first signals |
| Growing brand, some data | Custom Audiences (website) + Advantage+ prospecting | Mix of known signals + exploration |
| Established brand | ASC (Advantage+ Shopping) full automation | Andromeda has enough signal to run optimally |
| Retargeting layer | Custom Audiences only, Advantage+ disabled | Prevent cannibalization of paid prospecting |
| Lookalike testing | 1–3% LAL from LTV-based seed | Find high-quality expansion audiences |
