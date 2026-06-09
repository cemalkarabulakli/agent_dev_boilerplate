# Scenario: AI Process Automation — Balkan SMBs

## Who this is for

A software engineer with 12 years of experience who has proven automation results (hotel: 4hrs→1hr,
warehouse barcode system, 52 paid API integration clients) but currently underprices on Upwork and
has no direct acquisition channel in the Bulgarian/Balkan market.

The goal: move off-platform, charge $3,500-$6,000 per fixed-scope project, and build a direct
pipeline of Bulgarian/Balkan SMB clients — without cold-calling or a sales team.

**Core positioning**: "I eliminate your most painful daily manual process in 3 weeks — fixed price,
no IT project overhead."

---

## Geographic priority

| Phase | Market | Language | Channel | When to start |
|---|---|---|---|---|
| **1 — Bulgaria** | ~200k SMBs, price-sensitive, EU market | Bulgarian + English | Facebook business groups, LinkedIn Bulgaria, direct outreach Sofia | Now — first 3 clients |
| **2 — Turkey** | ~3.5M SMBs, larger deal sizes possible | Turkish + English | LinkedIn Turkey, Instagram, WhatsApp, ERP reseller partnerships | After 3 Bulgarian case studies |
| **3 — Global** | English-speaking SMBs worldwide | English | LinkedIn English content, Upwork (repositioned), inbound from VSL | After Turkey is running |

**Why this order matters:**
- Bulgaria is your home market — trust is easier to build, references travel by word of mouth, you understand the local software landscape (Microinvest, Accounting+, local ERPs)
- Turkey is a natural second step: 10x larger market, you likely have language + cultural familiarity, strong WhatsApp and Instagram business culture matches a relationship-first sales approach
- Global only after the offer is proven and documented — you compete on case studies, not price

---

## The three industries (same offer, different examples)

You do not need to choose one industry. Use whichever industry your prospect is in.
The automation is the same. The story you lead with changes.

| Industry | The daily pain | Your proof to lead with |
|---|---|---|
| **E-commerce** | Orders → accounting → stock, manual every morning | 52 Upwork clients, Shopify/WooCommerce API experience |
| **Logistics / Warehouse** | Barcode scans → stock sheet → reports, manual entry | Barcode + Google Sheets warehouse system |
| **Hospitality** | Booking.com + Airbnb → master sheet → front desk, manual reconciliation | Hotel booking automation (your first project, 2010) |

---

## Recommended pipeline runs

### 1. Foundation — sharpen the avatar and validate the market angle

```bash
python scripts/run_full_business_build.py \
  --context scenarios\ai_automation_balkans\business_context.yaml \
  --group foundation
```

What you get: a market viability score for automation services in the Balkans, a sharpened avatar
profile (which buyer type — e-commerce owner, logistics manager, hotel operator — feels the pain
most acutely and moves fastest to buy), and a competitor gap analysis showing why large IT agencies
and cheap Upwork freelancers both leave this market underserved.

---

### 2. Offer — price the pain, not the code

```bash
python scripts/run_full_business_build.py \
  --context scenarios\ai_automation_balkans\business_context.yaml \
  --group offer
```

What you get: an offer architecture report asking whether $3,500 is correctly priced (answer: probably
not — the hotel automation alone was worth $8,000+ in labor savings in year one), a value stack that
shows the ROI in BGN not USD, and a guarantee structure that removes the "what if it doesn't work"
objection.

Key output to read: `outputs/offer_architect_*.md` — it will pressure-test your price floor.

---

### 3. Acquisition — build a direct pipeline off Upwork

```bash
python scripts/run_full_business_build.py \
  --context scenarios\ai_automation_balkans\business_context.yaml \
  --group acquisition
```

What you get: an acquisition strategy for moving from Upwork-dependent to direct (LinkedIn Bulgaria,
Facebook business groups, outbound to specific verticals), a content authority plan for what to post
to attract inbound leads, a funnel map, a sales script for the 30-min Process Diagnosis call, and
an objection handler for the top 4 objections (cost, trust, local software, timing).

---

### 4. Generate the VSL script (for a landing page or LinkedIn video)

```bash
python scripts/generate_vsl_script.py \
  --context scenarios\ai_automation_balkans\business_context.yaml
```

What you get: a VSL script anchored on the hotel story ("4 hours a day, every day — until it wasn't"),
the ROI calculation reveal (showing the real cost of the manual process in BGN/year), and the
fixed-price + guarantee close.

Use this script for:
- A 5-minute LinkedIn video (your first piece of authority content)
- A landing page for direct outreach follow-up
- A presentation slide deck for in-person meetings with local business owners

---

### 5. Build a case study (from the hotel or warehouse proof)

```bash
python scripts/generate_case_study.py \
  --context scenarios\ai_automation_balkans\business_context.yaml
```

What you get: a structured case study template using your existing proof — the hotel automation
and the warehouse system. These are your two most powerful trust-builders. A one-page case study
for each is worth more than any ad campaign at this stage.

---

### 6. Objection bank — for the sales call

```bash
python scripts/generate_objection_bank.py \
  --context scenarios\ai_automation_balkans\business_context.yaml
```

What you get: scripted responses to the 4 most common objections Balkan SMB owners raise:
- "How much does this cost?" (before ROI is established)
- "We use local software — I doubt you can integrate it"
- "We tried something like this before and it failed"
- "I need to think about it / discuss with my accountant"

---

### 7. Business scorecard — assess current state and identify the highest-leverage move

```bash
python scripts/generate_business_scorecard.py \
  --context scenarios\ai_automation_balkans\business_context.yaml
```

What you get: a full business model assessment. Given that you're at under $5k/month on Upwork,
this will identify the single highest-leverage action — most likely: get 2-3 case studies documented
and launch a direct LinkedIn outreach campaign to Bulgarian e-commerce or logistics companies.

---

### 8. Full pipeline — foundation through acquisition (skip delivery and launch for now)

```bash
python scripts/run_full_business_build.py \
  --context scenarios\ai_automation_balkans\business_context.yaml \
  --group foundation,offer,acquisition \
  --mode api \
  --model claude-sonnet-4-6
```

This runs the 9 most relevant agents for your current stage (pre-launch, pre-funnel). Skip the
delivery and retention groups until you have 3+ clients on the new direct offer.

---

### 9. Dry run first (see what will execute before spending API credits)

```bash
python scripts/run_full_business_build.py \
  --context scenarios\ai_automation_balkans\business_context.yaml \
  --dry-run
```

---

### 10. Full pipeline mock (instant, free, placeholder output)

```bash
python scripts/run_full_business_build.py \
  --context scenarios\ai_automation_balkans\business_context.yaml
```

---

## Priority order for your stage

You are pre-funnel, pre-direct-client. Run these in order:

| Priority | Command | What it unlocks |
|---|---|---|
| 1 | `--group foundation` | Confirms which avatar and industry to lead with |
| 2 | `--group offer` | Gets your price right before you go to market |
| 3 | `generate_case_study.py` | Turns hotel + warehouse proof into a trust asset |
| 4 | `--group acquisition` | Builds the direct pipeline plan |
| 5 | `generate_vsl_script.py` | Creates the core content piece for LinkedIn |
| 6 | `generate_objection_bank.py` | Prepares you for the sales call |

---

## Key outputs to watch

| Agent | Output file | Why it matters |
|---|---|---|
| `market_selector` | `outputs/market_selector_*.md` | Which industry vertical to lead with first |
| `offer_architect` | `outputs/offer_architect_*.md` | Likely recommends raising price above $3,500 |
| `value_stack_builder` | `outputs/value_stack_builder_*.md` | The ROI table in BGN — your sales call foundation |
| `case_study_writer` | `outputs/case_study_writer_*.md` | Hotel and warehouse stories formatted for clients |
| `acquisition_strategy_agent` | `outputs/acquisition_strategy_agent_*.md` | The direct channel plan off Upwork |
| `sales_script_builder` | `outputs/sales_script_builder_*.md` | The 30-min Process Diagnosis call script |

---

## What $3,500 actually competes against

When a Balkan SMB owner objects to $3,500, show them this:

| Option | Cost | Solves it? |
|---|---|---|
| Hire data entry employee | 800-1,200 BGN/month = **9,600-14,400 BGN/year** | No — still same errors |
| Large IT agency project | 15,000-50,000 BGN | Yes, but months of overhead |
| Do nothing | 600-1,000 BGN/month in staff time wasted = **7,200-12,000 BGN/year** | No |
| Kill the Bottleneck package | **~6,800 BGN one-time** | Yes — 3 weeks, fixed price |

Your offer pays for itself in under 12 months in every scenario. That is your close.
