# Campaign Structure — Meta Ads 2025

## The Three-Tier Hierarchy

```
CAMPAIGN
  └── Objective (defines optimization goal and available features)
  └── Budget type: CBO (Advantage Campaign Budget) or ABO
      └── AD SET(S)
          └── Audience targeting (or Advantage+ Audience)
          └── Placements (or Advantage+ Placements)
          └── Schedule and bid strategy (if ABO)
              └── ADS
                  └── Creative assets
                  └── Copy
                  └── Destination URL
```

## Campaign Objectives (2025)

| Objective | Use Case | Optimize For |
| --- | --- | --- |
| Awareness | Brand recall, reach | Reach, ThruPlay, Brand Recall Lift |
| Traffic | Site/app visits | Link Clicks, Landing Page Views |
| Engagement | Video views, post interactions, messaging | ThruPlays, Post Engagement, Conversations |
| Leads | Lead forms, website leads, calls | Lead events, Contacts |
| App Promotion | App installs, in-app events | App Installs, App Events |
| Sales | Purchases, conversions, catalog sales | Purchase, Add-to-Cart, Custom conversions |

**Andromeda rule:** Always optimize for the deepest conversion event you can sustain data for. Optimizing for Landing Page Views when Purchase data exists wastes Andromeda's signal potential — it trains on the wrong event.

## Budget Types

### CBO — Advantage Campaign Budget (Meta's pushed default)
- Single budget at campaign level; Meta distributes across ad sets in real-time
- Algorithm allocates more to ad sets with best predicted results
- Now the default and strongly recommended by Meta for scale
- Best for: Scaling validated winners, broad audiences (20M+ reach), mature campaigns
- Minimum: Weekly budget = 50x target CPA

### ABO — Ad Set Budget
- Fixed budget per ad set regardless of relative performance
- Full manual control per audience or creative group
- Best for: Testing phase (equal exposure per variable), new market testing
- Use to validate creatives before migrating to CBO

**Recommended hybrid:**
1. Test phase: ABO — equal budget per creative or audience, identify winners
2. Scale phase: CBO — migrate winners, let algorithm optimize distribution

## Advantage+ Campaign Types

| Type | Goal | Key Feature |
| --- | --- | --- |
| Advantage+ Shopping (ASC) | Sales / Purchases | Full automation of audience + placements; up to 150 creative combos |
| Advantage+ App | App installs / events | Fully automated delivery for mobile |
| Advantage+ Leads | Lead generation | Automated audience for lead forms |
| Advantage+ Audience | Any | AI-expanded audience from your suggestion |
| Advantage Campaign Budget | Any | Auto-distributes budget across ad sets |
| Advantage+ Creative | Any | Auto-generates text/image/audio variations |
| Advantage+ Placements | Any | Delivery across all Meta surfaces |

## Advantage+ Shopping Campaigns (ASC) — Full Detail

ASC is the primary Andromeda-optimized campaign vehicle for e-commerce.

### When to Use ASC
- Selling products with a connected catalog
- 50+ purchases in past 30 days (pixel + CAPI confirmed)
- Capable of providing 10–15+ distinct creative assets
- $50+/day minimum budget available
- Shipping to defined country/region

### When NOT to Use ASC
- Lead generation, app installs, or pure awareness objectives
- Strict audience exclusions required (e.g., exclude a specific geography)
- Testing a new offer with insufficient conversion data (< 50 events)

### ASC Setup Process
1. Confirm 50+ conversions in past 30 days + pixel/CAPI active
2. Create campaign: Sales objective → Enable Advantage+ Shopping
3. Set daily budget ($50+ minimum; $100–200 for higher-ticket)
4. Configure geography (country or region targeting)
5. Set Existing Customer Budget Cap to 25–30% (prevents over-retargeting existing customers)
6. Load 10–15+ creative assets (diverse formats: UGC, product shots, lifestyle, video testimonials, carousels, dynamic catalog)
7. Set attribution: 7-day click + 1-day view
8. Allow minimum 7 days before making changes (learning phase)

### ASC Performance Data (Meta)
- 17% lower cost per purchase vs. manual BAU campaigns
- 32% lower cost per incremental conversion when alongside manual

### Budget Allocation Guidance
- Established e-commerce brands: 50–70% of paid social budget to ASC
- Newer brands (< 6 months data): 30–50% to ASC

## Campaign Consolidation Principle

Meta's algorithm works better with fewer, larger, focused campaigns:
- Recommended: 1–3 campaigns per objective
- 1–3 ad sets per campaign
- 8–20 distinct creatives per ad set
- Fragmentation = slower learning, split signals, higher CPMs

**Andromeda rationale:** More campaigns competing against each other in the same auction = internal bid inflation. Fewer campaigns = more signal per ad set = faster learning phase exit.

## Structure Decision Guide

| Situation | Recommended Structure |
| --- | --- |
| E-commerce, 50+ purchases/month | 1 ASC campaign + 1 retargeting campaign |
| E-commerce, < 50 purchases/month | 1 manual sales campaign (ABO testing → CBO scale) |
| Lead gen, high volume | 1 Advantage+ Leads campaign |
| Lead gen, new business | 1 manual leads campaign (ABO, collect 50 leads before optimizing) |
| App install | 1 Advantage+ App campaign |
| Brand awareness | 1 manual awareness campaign, broad, ThruPlay optimization |
| Multi-country | Separate campaigns per country (not ad sets) |
