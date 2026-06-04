# Tracking and Attribution — Pixel, CAPI, and Signal Quality

## Why Signal Quality Is the Foundation

Andromeda and Advantage+ are powered by conversion signals. Poor signal quality means:
- Andromeda cannot find the right audiences
- Learning phase takes longer and costs more
- Cost cap and ROAS target bid strategies underperform
- You are spending money to train a system that cannot optimize

**Rule: Fix signal quality before scaling budget.**

## Meta Pixel

JavaScript snippet that fires browser-side events when users take actions on your site.

### Standard Events (priority order for Andromeda optimization)
1. Purchase (highest value — use for campaign optimization when possible)
2. InitiateCheckout
3. AddToCart
4. ViewContent
5. AddPaymentInfo
6. Lead
7. CompleteRegistration
8. Search
9. PageView (lowest value for optimization)

### Pixel Limitations (2025)
- iOS 14.5+ opted-out users: not tracked (40–60% of users in many markets)
- Ad blockers: block pixel events entirely
- Safari Intelligent Tracking Prevention: limits cookie lifespans to 7 days
- Pixel-only setup misses approximately 50% of actual conversions

**Pixel alone is not sufficient for Andromeda signal quality.**

## Conversions API (CAPI) — Non-Negotiable

CAPI sends events server-to-server, bypassing all browser-based restrictions.

### Why CAPI Is Required for Andromeda
- Without CAPI, Andromeda operates on ~50% of conversion signal data in high iOS opt-out regions
- CAPI implementation reduces: 17.8% lower cost per result, 13% average CPA reduction
- Shopify merchants: 15% more attributed conversions with native CAPI toggle

### CAPI Implementation Methods

| Method | Cost | Complexity | Best For |
| --- | --- | --- | --- |
| Meta-Enabled One-Click CAPI | Free | Minimal | Standard web events |
| Partner Integration (Shopify, WooCommerce) | Free–low | Low | Standard e-commerce |
| CAPI Gateway | ~$10/month | Moderate | Flexibility + reliability |
| Server-Side GTM | $50–150/month | High | Multi-platform routing |
| Direct API Integration | Dev cost | Highest | Custom/offline/CRM events |

**Shopify:** Admin → Settings → Customer events → Enable "Share data with Meta"

### Event Match Quality (EMQ)

EMQ measures how well Meta matches server-side events to user profiles. Scale: 1–10.

| EMQ Score | Status |
| --- | --- |
| 7.5–9.0 | Target — full signal strength |
| 7.0–7.5 | Acceptable — room to improve |
| 6.0–7.0 | Warning — significant signal loss |
| Below 6.0 | Critical — major share of events not attributable |

**How to improve EMQ:**
- Send hashed PII with events: email (`em`), phone (`ph`), first name (`fn`), last name (`ln`)
- Include `fbclid` (Facebook click ID), `fbp` (Facebook browser ID), `fbc`
- Include IP address, user agent, and `external_id` (your internal user ID)

### Deduplication (Critical — Must Be Correct)

When running Pixel + CAPI together, events will fire from both sources for the same action. Without deduplication, Meta double-counts conversions.

**Correct deduplication process:**
1. Generate a unique `event_id` in the browser when the event fires
2. Send `event_id` with the Pixel event (browser side)
3. Send the **exact same `event_id`** to your server for the CAPI event
4. Meta deduplicates on matching `event_name` + `event_id` within a ~2-hour window
5. Common failure: generating different IDs on browser vs. server side

## Aggregated Event Measurement (AEM)

Privacy-preserving measurement for iOS 14.5+ opted-out users.

**June 2025 update:** The previous 8-event limit and manual event prioritization requirement have been **removed**. AEM is now fully automatic — no setup or ranking needed. The "Aggregated Event Measurement" tab has been removed from Events Manager.

**Current requirements:**
- Correct Pixel + CAPI implementation (still required)
- Consistent event naming across sources
- Reliable deduplication to prevent double-counting
- Domain verification for link ownership (helps prevent pixel blocking)

## Attribution Windows (2025)

| Window | Status | Use Case |
| --- | --- | --- |
| 7-day click | Active — default and recommended | Most campaigns |
| 1-day click | Active | Impulse purchases, short-cycle products |
| 1-day view | Active | Upper-funnel, brand awareness |
| 7-day view | Retired (January 12, 2026) | — |
| 28-day view | Retired (January 12, 2026) | — |

**Recommended standard:** 7-day click + 1-day view for e-commerce campaigns.

CAPI events: `event_time` values must be within Meta's 7-day acceptance window.

## UTM Parameters

Standard UTM structure for Meta:
```
utm_source=facebook
utm_medium=paid_social
utm_campaign={{campaign.name}}
utm_content={{ad.name}}
utm_term={{adset.name}}
```

Meta supports dynamic parameters: `{{campaign.name}}`, `{{adset.name}}`, `{{ad.name}}`. Always use UTMs alongside pixel for cross-validation in GA4 or other analytics.

## Signal Quality Checklist

Before scaling any campaign:
- [ ] Pixel installed and firing on key pages
- [ ] CAPI sending Purchase (or primary conversion) events
- [ ] Event deduplication confirmed (same `event_id` from browser and server)
- [ ] EMQ score checked in Events Manager (target 7.5+)
- [ ] Hashed PII parameters being sent (email, phone)
- [ ] Domain verified in Business Manager
- [ ] No Sensitive Category flag in Events Manager (especially for health/finance)
- [ ] Attribution window set to 7-day click + 1-day view
