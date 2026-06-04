# Andromeda Core — Meta's AI Ad Retrieval Engine

Source: Meta Engineering Blog (December 2024), Meta Business News (2025)

## What Andromeda Is

Andromeda is Meta's next-generation AI retrieval engine that powers the first stage of ad delivery. The ad delivery pipeline is:

```
Retrieval (Andromeda) → Ranking → Auction → Delivery
```

Andromeda's job is to select which ads are even eligible to compete in an auction, filtering from tens of millions of candidates down to thousands of finalists. It replaced simpler approximate nearest-neighbor retrieval with deep neural networks capable of **10,000x more model complexity**.

Meta confirmed: **8% improvement in ads quality** after Andromeda rolled out globally in December 2024.

## How Andromeda Works Mechanistically

1. Every ad creative receives an **Entity ID** — a semantic fingerprint derived from:
   - Visual elements (images, video frames)
   - Text: captions, overlays, ad copy
   - Audio content and pacing (for video)
   - On-screen actions and context

2. A **hierarchical indexing system** clusters semantically similar ads. Minor tweaks (color swap, headline rewording) do not generate new Entity IDs. Andromeda recognizes them as the same concept.

3. It dynamically reconstructs user-ad interaction signals in real-time rather than relying on static pre-engineered features.

4. It acts as a "bouncer" — deciding which ads are even eligible before ranking begins.

## Why Creative IS the Targeting

Before Andromeda, advertisers controlled audience reach through demographic and interest targeting. Andromeda changed this:

- Creative content signals to Andromeda what type of person should see the ad
- Two ads for the same product with different angles ("efficiency-focused" vs. "family-oriented") reach different audiences even under identical broad targeting
- Narrow audience constraints limit the signal pool Andromeda can learn from
- The algorithm finds the right audience better than manual interest stacking — if you give it enough diverse creatives to test

**Consequence:** Creative diversity is now an audience strategy, not just a testing strategy.

## What Andromeda Needs from Advertisers

### 1. Genuine Creative Variety (not surface variants)
- Volume with conceptual diversity is the primary fuel
- Successful accounts: 8–20 conceptually distinct creatives per ad set
- Minor variations (button color, synonym copy) do not register as new concepts
- Andromeda saturates a viable audience in 2–3 weeks; creative refresh is mandatory

### 2. High-Quality Conversion Signals (CAPI)
- Andromeda is powered by first-party signal data
- CAPI bypasses iOS 14+ privacy restrictions that block 40–60% of pixel events
- Without CAPI: Andromeda operates on approximately 50% of conversion data
- CAPI + high Event Match Quality (EMQ 7.5–9.0) = full signal strength

### 3. Learning Phase Protection
- Andromeda requires ~50 optimization events to exit learning phase
- Any significant change (bid strategy, targeting, creative) resets the learning clock
- Editing campaigns mid-learning destroys accumulated signal
- Never optimize based on day-1 or day-2 data; wait for learning phase exit

### 4. Advantage+ as the Delivery Vehicle
- Advantage+ Shopping Campaigns (ASC) were designed specifically for Andromeda at scale
- ASC consolidates targeting into a single optimization pool, letting Andromeda allocate freely
- Advantage+ grew 70% YoY in Q4 2024; advertisers using it see 17% lower cost per purchase

## What Does NOT Work in the Andromeda Era

- **Narrow interest targeting as the primary strategy**: Interest categories deprecated June 2025; Andromeda finds audiences better than manual stacking anyway
- **Set-and-forget creative**: Fatigue in 2–3 weeks means static portfolios collapse
- **Surface-level creative variants**: Andromeda ignores them as duplicate concepts
- **High-frequency campaigns without creative refresh**: CPM stays stable but CTR collapses = Andromeda saturating the audience
- **Editing campaigns in learning phase**: Resets signal accumulation, wastes budget
- **Running without CAPI**: Half the signal = slower learning, higher CPA, worse optimization

## Andromeda Performance Data (Official Meta Sources)

| Feature | Impact |
| --- | --- |
| Andromeda overall (vs. prior system) | +8% ads quality improvement |
| Advantage+ Sales Campaigns | 9% lower cost per action |
| Image generation (Advantage+ Creative) | 11% higher CTR, 7.6% higher conversion rate |
| Partnership ads | 19% lower CPA average |
| ASC vs. manual campaigns | 17% lower cost per purchase, 32% lower cost per incremental conversion |
| CAPI implementation | 17.8% lower cost per result, 13% CPA reduction on average |
| Advantage+ Audience vs. manual targeting | 22% higher ROAS |

## The Core Implication for Every Campaign Decision

Every recommendation must answer: **"Does this give Andromeda more signal, more genuine creative variety, and less interference with its learning?"**

If the answer is no — do not recommend it.
