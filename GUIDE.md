# High-Ticket Expert Growth System — Getting Started Guide

> This guide is written for first-time users. It covers all scenarios from setup to real business decisions with examples.

---

## Table of Contents

- [What Does This System Do?](#what-does-this-system-do)
- [Installation](#installation)
- [First Step: Filling Out business_context.yaml](#first-step-filling-out-business_contextyaml)
- [Scenario 1 — Choosing a Market from Scratch](#scenario-1--choosing-a-market-from-scratch)
- [Scenario 2 — Avatar and Pain Research](#scenario-2--avatar-and-pain-research)
- [Scenario 3 — Designing a High-Ticket Offer](#scenario-3--designing-a-high-ticket-offer)
- [Scenario 4 — Value Stack and Pricing](#scenario-4--value-stack-and-pricing)
- [Scenario 5 — Client Acquisition Strategy](#scenario-5--client-acquisition-strategy)
- [Scenario 6 — Authority Content Plan](#scenario-6--authority-content-plan)
- [Scenario 7 — Sales Funnel Map](#scenario-7--sales-funnel-map)
- [Scenario 8 — Sales Script and Objection Handling](#scenario-8--sales-script-and-objection-handling)
- [Scenario 9 — Meta Ads Management](#scenario-9--meta-ads-management)
- [Scenario 10 — Writing a VSL (Video Sales Letter)](#scenario-10--writing-a-vsl-video-sales-letter)
- [Scenario 11 — Client Case Study](#scenario-11--client-case-study)
- [Scenario 12 — YouTube Channel Strategy](#scenario-12--youtube-channel-strategy)
- [Scenario 13 — Planning a Launch Campaign](#scenario-13--planning-a-launch-campaign)
- [Scenario 14 — Market Research and Competitor Tracking](#scenario-14--market-research-and-competitor-tracking)
- [Scenario 15 — Business Scorecard and Bottleneck Detection](#scenario-15--business-scorecard-and-bottleneck-detection)
- [Scenario 16 — Adding a New Agent](#scenario-16--adding-a-new-agent)
- [Scenario 17 — Full Cycle: From Scratch to Scale](#scenario-17--full-cycle-from-scratch-to-scale)
- [Dashboard Usage](#dashboard-usage)
- [Quality and Test Commands](#quality-and-test-commands)
- [Common Mistakes](#common-mistakes)

---

## What Does This System Do?

This system is a **local, modular AI agent factory** designed for professionals who want to turn their expertise into a high-ticket business.

**Example target users:**

- A finance consultant doing advisory work → wants to automate the client acquisition system
- A fitness coach starting to sell courses → wants to structure their offer and sales funnel
- A digital marketer transitioning from freelancer to agency owner
- Any expert who wants to package and sell their knowledge online

**What the system does NOT do:**
- It is not a chatbot like ChatGPT
- It does not require an API key (runs fully in mock/local mode)
- It does not make autonomous decisions; every strategy update requires human approval

**What the system DOES do:**
- Processes the Market → Avatar → Offer → Proof → Acquisition → Sales → Delivery → Retention → Scale chain step by step
- Produces structured Markdown outputs for each stage
- Stores research signals with source labels, requires references
- Applies ethical rules at the system level (no fake claims, no fake testimonials, no fake scarcity)

---

## Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/agent-dev-boilerplate.git
cd agent-dev-boilerplate

# Install dependencies
pip install -r requirements.txt

# Check system health
python -m pytest

# Validate agent structure
python scripts/validate_agent_structure.py

# Start the dashboard (optional)
python dashboard/server.py
# Open in browser: http://localhost:8765
```

No API key required. The system runs fully in mock mode.

---

## First Step: Filling Out business_context.yaml

`business_context.yaml` is the brain of the system. All agents read from this file.

**Rules:**
- Leave fields you don't know empty (the system labels them as "unknown")
- Write estimates in the notes field
- Do not add claims that aren't true

### Example: Fitness Coach

```yaml
{
  "expert": {
    "niche": "online fitness coaching for busy professionals",
    "expertise": "strength training and habit formation",
    "years_experience": "7",
    "credibility_assets": ["NSCA-CPT certification", "500+ clients", "Transformation photos"],
    "audience_size": "8000 Instagram followers",
    "current_channels": ["Instagram", "email list"],
    "delivery_strengths": ["1-on-1 coaching", "group programs"],
    "unique_experience": "Lost 35 kg while working 9-5 and maintained it for 6 years"
  },
  "market": {
    "market_name": "online fitness coaching",
    "urgency_level": "high — health issue or appearance concern",
    "ability_to_pay": "mid-to-high — corporate professionals",
    "competitors": ["Caliber", "Future", "local gym coaches"]
  },
  "customer": {
    "target_customer": "35-50 year old corporate professional",
    "specific_avatar": "Alex, 42, software manager, works 60+ hours/week, 15 kg overweight, quit 3 diets before",
    "main_problem": "no time and energy to stay disciplined",
    "expensive_problem": "health issues and lack of energy affecting career and family life",
    "dream_outcome": "lose 15 kg in 6 months, wake up energized in the mornings",
    "objections": ["I don't have time", "I've tried before and it didn't work", "too expensive"]
  },
  "offer": {
    "current_offer": "3-month 1-on-1 online coaching program",
    "current_price": "3000 USD",
    "core_promise": "minimum 8 kg in 90 days, or money back",
    "guarantee": "90-day results guarantee"
  }
}
```

### Example: B2B Consultant

```yaml
{
  "expert": {
    "niche": "customer success consulting for SaaS companies",
    "expertise": "churn reduction and NPS improvement",
    "years_experience": "12",
    "credibility_assets": ["CSO roles at 3 leading SaaS companies", "2 published case studies"],
    "current_channels": ["LinkedIn", "referrals"],
    "unique_experience": "I have 3 companies where I reduced churn from 34% to 8%"
  },
  "customer": {
    "target_customer": "SaaS company founder with 10-100 employees",
    "expensive_problem": "high churn reduces company valuation and undermines investor confidence",
    "dream_outcome": "cut churn in half in 12 months, grow ARR by 40%"
  },
  "offer": {
    "current_price": "15000 USD",
    "current_offer": "6-month CS transformation program"
  }
}
```

---

## Scenario 1 — Choosing a Market from Scratch

**Situation:** You have multiple niche ideas but don't know which to choose.

**Agent used:** `market_selector`

**Steps:**

```bash
# Run the market scorecard
python scripts/generate_market_scorecard.py \
  --agent market_selector \
  --context business_context.yaml
```

**Output:** Produces a Markdown report in the `outputs/market_scorecards/` folder.

**The report includes:**
- Market pain score (1-10)
- Ability to pay assessment
- Reachability score
- Competition intensity analysis
- Overall market score

### Real Usage Example

Suppose you have three market ideas:
1. Online English language coaching
2. LinkedIn outreach agency for SaaS companies
3. Ad management for e-commerce stores

Enter each one into `business_context.yaml` in turn, run the scorecard, compare.

**Good market signals:**
- People are already paying to solve this problem
- The problem is the kind that gets expensive if delayed
- The target audience is reachable (LinkedIn, YouTube, specific communities)
- Competitors exist but none is a clear market leader

**Bad market signals:**
- Everyone says "great idea" but nobody pays
- The audience is scattered and unreachable
- The problem is a luxury, not a necessity

```bash
# To query the agent directly
python scripts/run_agent.py \
  --agent market_selector \
  --message "I'm choosing between online English coaching and a SaaS LinkedIn outreach agency. Which is the stronger market?"
```

---

## Scenario 2 — Avatar and Pain Research

**Situation:** You've chosen your market but haven't clearly defined your customer. You don't want to fall into the "everyone is my target" trap.

**Agent used:** `avatar_pain_researcher`

**Steps:**

```bash
python scripts/generate_avatar_research.py \
  --agent avatar_pain_researcher \
  --context business_context.yaml
```

**Output:** `outputs/avatar_research/` → specific avatar profile, pain map, buying triggers, customer language examples.

### Example: Coaching Business

**Weak avatar (avoid):**
> "Working women aged 30-50"

**Strong avatar:**
> "Sarah, 38, mid-level manager in London, 2 kids. In the office by 7am, home by 7pm. Starts a new diet every month and quits it. Core fear: becoming diabetic like her mother by the time she's 40. Sunday mornings she browses dietitian Instagram accounts but thinks none of them are 'like her'."

With this avatar definition, your content, ads, and sales scripts become far more specific.

### Validating the Avatar with Research

```bash
# Collect real customer language from Reddit
python scripts/collect_source.py \
  --source reddit \
  --query "busy professional struggling to lose weight"

# Analyze competitor ads
python scripts/collect_source.py \
  --source facebook_ad_library \
  --query "online fitness coaching"

# Cross-source analysis
python scripts/analyze_cross_source_signals.py
```

Collected signals are saved under `research/sources/`. Each signal is labeled with its source; signals from a single source are marked "candidate", signals validated from multiple sources are marked "validated".

---

## Scenario 3 — Designing a High-Ticket Offer

**Situation:** Your avatar is clear. Now you need to design an offer they will actually buy.

**Agent used:** `offer_architect`

**Steps:**

```bash
python scripts/generate_offer_audit.py \
  --agent offer_architect \
  --context business_context.yaml
```

**Output:** `outputs/offer_audits/` → offer strengths/weaknesses, mechanism clarity, value equation assessment.

### Offer Anatomy

The system evaluates your offer on five dimensions (Hormozi's value equation):

| Dimension | Question | Example |
|---|---|---|
| **Outcome** | What does the client get? | 12 kg in 90 days |
| **Probability** | How much does the client believe in success? | 3 client case studies |
| **Time** | In how long? | 90 days, 3 hours/week |
| **Effort** | How much work is required? | Just a shopping list and 30 min workout |
| **Risk** | What if results don't come? | Full money-back guarantee |

### Example: Weak vs. Strong Offer

**Weak:**
> "3-month online fitness coaching — $3,000"

**Strong:**
> "90-Day Body Transformation for Busy Professionals: Lose 8-15 kg with 3×30 minutes per week, or I refund every cent. 21 out of 23 clients reached their goal."

The system asks:
- Is the mechanism specific and hard to copy?
- Are the claims supported?
- Is risk reversed?
- Is there a reason to act urgently?

```bash
# Ask a specific question about your offer
python scripts/run_agent.py \
  --agent offer_architect \
  --message "How do I strengthen the guarantee in my offer? Right now I have 'money back if no results in 90 days' but no one takes it seriously."
```

---

## Scenario 4 — Value Stack and Pricing

**Situation:** You have an offer but don't know how to set the price or raise perceived value.

**Agents used:** `value_stack_builder`, `pricing_guarantee_optimizer`

**Steps:**

```bash
# Build the value stack
python scripts/generate_value_stack.py \
  --agent value_stack_builder \
  --context business_context.yaml

# Pricing and guarantee assessment
python scripts/generate_pricing_guarantee_review.py \
  --agent pricing_guarantee_optimizer \
  --context business_context.yaml
```

### Value Stack Example

Suppose you're selling online fitness coaching. The $3,000 price "feels expensive" because the value stack is missing.

**Weak offer package:**
- 3-month coaching: $3,000

**Strong value stack:**

| Element | Perceived Value |
|---|---|
| 12-week personalized program | $2,400 |
| Weekly 1:1 check-in calls (12 sessions) | $1,800 |
| Personal nutrition plan | $600 |
| WhatsApp support access | $900 |
| **Bonus:** Shopping list and meal-prep guide | $300 |
| **Bonus:** Travel workout pack | $200 |
| **Guarantee:** 8 kg in 90 days or full refund | Unlimited |
| **Total perceived value** | **$6,200** |
| **Real price** | **$3,000** |

The system checks:
- Is the price in line with market benchmarks?
- Should a payment plan option be offered?
- Is the guarantee type (results guarantee, satisfaction, or hybrid?) correctly chosen?

### Pricing Guide

```
Low ticket: Under $1,000 → requires volume, doesn't scale 1-on-1
Mid ticket: $1,000-$10,000 → hybrid scale possible
High ticket: $10,000+ → fewer clients, higher conversion required
```

The system evaluates the price based on whether the customer is experiencing an "expensive problem."

---

## Scenario 5 — Client Acquisition Strategy

**Situation:** Your offer is ready. Now where do clients come from?

**Agent used:** `acquisition_strategy_agent`

**Steps:**

```bash
python scripts/generate_acquisition_plan.py \
  --agent acquisition_strategy_agent \
  --context business_context.yaml
```

**Output:** `outputs/acquisition_plans/` → weekly acquisition actions, channel priorities, cost-benefit assessment.

### Acquisition Channels

The system evaluates these channels:

| Channel | Advantage | Disadvantage |
|---|---|---|
| **Organic content** (LinkedIn, Instagram) | Free, builds authority | Slow, requires consistency |
| **Paid ads** (Meta, Google) | Fast, scalable | Requires budget, fragile |
| **Outbound** (DM, email) | Immediate, controlled | Labor intensive |
| **Partnerships** | Leverage, trust transfer | Relationship-building time |
| **Community** (webinar, event) | High trust | Long-term |
| **Referral** | Highest close rate | Few at the start |

### Example: Acquisition Plan for a B2B Consultant

```bash
python scripts/run_agent.py \
  --agent acquisition_strategy_agent \
  --message "I do CS consulting for SaaS companies. I haven't run any ads yet, I have a LinkedIn profile but it's inactive. I have 10 hours/week. Where should I start?"
```

**System recommendation (example output):**
1. Optimize LinkedIn profile in 72 hours (headline and summary targeting your audience)
2. Week 1-4: 1 post/day (client transformation story, churn insight, Q&A)
3. 15 targeted DMs per week: "I was curious about how you structure your CS team…"
4. Month 2: A webinar: "3 Math Mistakes in SaaS Churn Reduction"
5. Month 3: Build a referral system from your first client

---

## Scenario 6 — Authority Content Plan

**Situation:** You want to become an authority in your niche but don't know what content to produce.

**Agent used:** `content_authority_agent`

**Steps:**

```bash
python scripts/generate_content_plan.py \
  --agent content_authority_agent \
  --context business_context.yaml
```

**Output:** `outputs/content_plans/` → content categories, example headlines, publishing calendar.

### Content Categories

The system organizes content by five purposes:

| Category | Purpose | Example |
|---|---|---|
| **Authority** | "This person knows their stuff" perception | "What I learned from 47 consulting clients in 12 years" |
| **Proof** | Real results | "Alex, 42: How he lost 14 kg in 90 days" |
| **Objection** | Remove barriers | "It's not because you lack time, it's because you haven't built a system" |
| **Demand Creation** | Open awareness | "80% of diabetics received a warning before age 40" |
| **CTA** | Drive action | "5 spots left in my 90-day program" |

### Example Content Calendar (Weekly)

| Day | Type | Example Headline |
|---|---|---|
| Monday | Authority | Counter-intuitive industry insight |
| Wednesday | Proof | Client story (with numbers) |
| Friday | Objection | Address the most common objection |
| Sunday | Personal | A scene from your own story |

---

## Scenario 7 — Sales Funnel Map

**Situation:** You have content, but it's unclear how to collect leads and move them to a sale.

**Agent used:** `funnel_builder`

**Steps:**

```bash
python scripts/generate_funnel_map.py \
  --agent funnel_builder \
  --context business_context.yaml
```

**Output:** `outputs/funnel_maps/` → lead magnet suggestion, application funnel, email sequence, webinar/workshop plan.

### Funnel Flow Example

```
AWARENESS
  └── Instagram reels / LinkedIn articles
        ↓
LEAD MAGNET (free value)
  └── "7-Day Quick Start Guide for Busy Professionals" (PDF)
        ↓
EMAIL SEQUENCE (7-10 emails)
  └── Email 1: Welcome + guide
  └── Email 3: Alex's story (case study)
  └── Email 5: "Why diets don't work" (objection content)
  └── Email 7: Program description
  └── Email 9: Application invitation
        ↓
APPLICATION FORM
  └── Pre-qualification with health status, goal, budget questions
        ↓
DISCOVERY CALL (15-20 min)
  └── Is it a fit? → Continue
        ↓
SALES CALL (45-60 min)
  └── Decision
```

### Lead Magnet Selection

```bash
python scripts/run_agent.py \
  --agent funnel_builder \
  --message "What lead magnet works best for SaaS CS consulting? Webinar, PDF guide, or free audit?"
```

The system scores each option on: ease of delivery, qualification value, perceived value, fast acquisition potential.

---

## Scenario 8 — Sales Script and Objection Handling

**Situation:** You're doing discovery calls but your close rate is low, or you don't know how to handle objections.

**Agents used:** `sales_script_builder`, `objection_handler`

**Steps:**

```bash
# Sales script
python scripts/generate_sales_script.py \
  --agent sales_script_builder \
  --context business_context.yaml

# Objection bank
python scripts/generate_objection_bank.py \
  --agent objection_handler \
  --context business_context.yaml
```

### Sales Call Structure

The system produces five stages for an ethical sales call:

```
1. RAPPORT (5 min)
   — Ask why they joined this call

2. DISCOVERY (15-20 min)
   — Where are you right now?
   — What would happen in 1 year if nothing changed?
   — What have you tried before?
   — Where would solving this problem take you?

3. OFFER PRESENTATION (10 min)
   — Explain the program
   — Show step by step what will happen

4. DECISION FRAMING (5 min)
   — "Does this make sense for you?"
   — Listen to objections and address them

5. CLOSE (5 min)
   — Reach a clear outcome
   — Establish follow-up plan
```

### Objection Bank Examples

| Objection | Ethical Response |
|---|---|
| "Too expensive" | "Is it the budget that's limiting, or is there uncertainty about the value?" |
| "I don't have time" | "How many hours per week do you think this program takes?" |
| "I need to talk to my spouse" | "Of course. Could I call you both tomorrow to make this decision together?" |
| "Let me think about it" | "Of course. May I ask what you'd like to think about?" |

---

## Scenario 9 — Meta Ads Management

**Situation:** Organic growth is slow, you want to accelerate with ads but you're getting lost in Meta ads.

**Agent used:** `meta_ads_manager`

**Steps:**

```bash
python scripts/generate_meta_ads_plan.py \
  --agent meta_ads_manager \
  --context business_context.yaml
```

**Output:** `outputs/meta_ads_plans/` → campaign structure, creative briefs, P.D.A. matrix, budget recommendations.

### Andromeda-First Approach

This agent's core philosophy is based on a reality Meta itself stated: **"Creative IS targeting."** Andromeda (Meta's AI engine) learns who to show ads to not from your targeting settings, but from the creative content.

**Wrong approach:**
- Narrow audience targeting (25-35, London, fitness interest, gym-goer)
- 2-3 creative variants
- Weekly campaign changes

**Right approach:**
- Broad targeting (only language + geography)
- 15-20 conceptually different creatives
- Protect the learning phase: don't touch until 50 conversions

### P.D.A. Creative Matrix

Each creative must differ on three dimensions:

| Dimension | Options |
|---|---|
| **P — Persona** | Budget-focused, status-focused, convenience-focused, beginner, expert, skeptic |
| **D — Desire** | Speed, savings, status, trust, transformation, convenience |
| **A — Awareness** | Problem-aware, solution-aware, product-aware |

**Example Creative Brief:**

```
Creative #1: Persona=Beginner, Desire=Speed, Awareness=Problem
Hook: "If you've quit 3 diets, it's not your fault"
Format: UGC-style phone video
CTA: "See the system"

Creative #2: Persona=Expert, Desire=Transformation, Awareness=Product
Hook: "Why I give a 90-day guarantee"
Format: Talking head, studio
CTA: "Apply"
```

### Weekly Ad Cycle

```
MONDAY: Review metrics (CTR, CPL, quality ranking)
WEDNESDAY: Evaluate campaigns that completed learning phase
FRIDAY: Prepare new creative brief
MONDAY: Upload new creatives
```

**Touch rules:**
- DO NOT touch a campaign in the learning phase
- Do not change budget by more than 20% at once
- Changing creative ≠ changing audience

---

## Scenario 10 — Writing a VSL (Video Sales Letter)

**Situation:** You want a strong script for your sales page or ad videos that moves viewers to a sale.

**Agent used:** `vsl_copywriter`

**Steps:**

```bash
python scripts/generate_vsl_script.py \
  --agent vsl_copywriter \
  --context business_context.yaml
```

**Output:** `outputs/vsl_scripts/` → 5-phase VSL script, landing page draft.

### The 5 Phases of a VSL

```
PHASE 1 — PROFILING
  Script: Who is this for? → Choose one specific person
  Example: "This video is only for people aged 35-50, working 50+ hours per week,
  who have quit at least two diets before"

PHASE 2 — OPENING (First 30 seconds are critical)
  Hook: Pain or paradox
  Example: "Research everywhere says the same thing: it's not a discipline problem,
  it's a systems problem. And today I'm going to show you that system."

PHASE 3 — OFFER
  — Problem → Make it expensive → Present solution
  — State your difference from competitors in one sentence (mechanism)
  — List the value stack visually

PHASE 4 — CLOSE
  — Reveal price after the value stack
  — State the guarantee clearly
  — Scarcity/urgency (if real): "5 spots left this month"

PHASE 5 — LANDING PAGE STRUCTURE
  — Headline: Who it's for + result + timeframe
  — Social proof: Case studies
  — CTA: One clear action
```

---

## Scenario 11 — Client Case Study

**Situation:** You've gotten great results from clients but don't know how to turn them into content.

**Agent used:** `case_study_writer`

**Steps:**

```bash
python scripts/generate_case_study.py \
  --agent case_study_writer \
  --context business_context.yaml
```

**Output:** `outputs/case_studies/` → Hormozi-style high-converting case study.

### Hormozi Case Study Format

Vague stories don't build trust. Specific numbers build trust.

**Weak:**
> "We worked with Alex and he was very satisfied."

**Strong:**
```
TITLE: "Software manager Alex, 42,
        lost 14.3 kg in 91 days and started waking up at 5:30am"

STARTING SITUATION:
- Alex, 87 kg, 174 cm
- 3 different diets in the past 4 years: quit on average after 6 weeks
- Daily energy: "I can barely make it through evening meetings"

OUR INTERVENTION:
- 12-week personalized program
- 3×30 min workouts per week (7:00-7:30 before morning meetings)
- Weekly check-in every Monday at 8:00

RESULTS (day 91):
- Weight: 87 kg → 72.7 kg (−14.3 kg)
- Morning wake time: 07:30 → 05:30
- Client comment: "First time I finished a program"

KEY DECISION:
"When I worked out before Monday morning meetings, the motivation carried
into the meeting — I always cancelled when I tried evenings"
```

**Important rules:**
- Do not use numbers that aren't real
- Get client approval
- Add "results are not typical" disclaimer

---

## Scenario 12 — YouTube Channel Strategy

**Situation:** You want to become a niche authority on YouTube but don't know how to start.

**Agent used:** `youtube_strategy_agent`

**Steps:**

```bash
python scripts/generate_youtube_strategy.py \
  --agent youtube_strategy_agent \
  --context business_context.yaml
```

**Output:** `outputs/youtube_strategies/` → channel strategy, SEO plan, content calendar.

### Core Principles

This agent works with an SEO-first, AI-assisted production approach.

**Core principles:**
1. Channel must be niche-focused from day one
2. Every video must be built around a search term
3. Title > Thumbnail (build the title first, then design the thumbnail)
4. First 48 hours: push to subscriber base → algorithm decision is made there

**Content Types:**

| Type | Purpose | Frequency |
|---|---|---|
| **Evergreen SEO** | Long-term search traffic | 2-3 per week |
| **Trend** | Short-term spike | When opportunity arises |
| **Authority** | "I should follow this person" | 2 per month |

**Example Channel Plan (Fitness Coach):**

```
Week 1-4: Core SEO videos
  — "How to lose weight at home in 30 minutes" (high search volume)
  — "Morning vs. evening workouts — which is better" (controversial = clicks)
  — "5 habits that help you lose weight without dieting"

Week 5-8: Authority videos
  — "The story of my client who lost 14 kg at age 42"
  — "Why most fitness coaches teach it wrong"

Ongoing: Community-based
  — "Answering your questions" format
```

---

## Scenario 13 — Planning a Launch Campaign

**Situation:** You want to launch a new program or product. You don't know how to manage a launch process that spans weeks.

**Agent used:** `launch_campaign_manager`

**Steps:**

```bash
python scripts/generate_launch_campaign.py \
  --agent launch_campaign_manager \
  --context business_context.yaml
```

**Output:** `outputs/launch_campaigns/` → pre-launch plan, cart open/close calendar, email sequence, ad plan, launch debrief.

### Launch Calendar Example (4 Weeks)

```
WEEK 1 — PRE-LAUNCH: Awareness
  — Content: Address avatar's pains
  — Email: "Something big is coming" + waitlist
  — Ads: Traffic campaign, video views

WEEK 2 — PRE-LAUNCH: Value Delivery
  — Content: Free mini-training (YouTube, live)
  — Email: Case study series (3 emails)
  — Ads: Start retargeting (to video viewers)

WEEK 3 — CART OPEN (5-7 days)
  — Daily email (launch sequence):
    — Day 1: Opening + value
    — Day 2: Case study
    — Day 3: Address objections
    — Day 4: Q&A
    — Day 5: Last day notice
    — Day 6: Closing email (morning + evening)
  — Ads: Conversion campaign, retargeting heavy

WEEK 4 — DEBRIEF
  — Record sales numbers
  — Document what didn't work
  — Plan the next launch
```

---

## Scenario 14 — Market Research and Competitor Tracking

**Situation:** You want to learn what the market actually thinks and what competitors are saying.

**Steps:**

```bash
# Collect customer language from Reddit
python scripts/collect_source.py \
  --source reddit \
  --query "online coaching scam expensive"

# Competitor ads from Facebook Ad Library
python scripts/collect_source.py \
  --source facebook_ad_library \
  --query "online fitness coaching"

# Demand direction with Google Trends
python scripts/collect_source.py \
  --source google_trends \
  --query "online coaching"

# Content trends with YouTube
python scripts/collect_source.py \
  --source youtube \
  --query "high ticket coaching funnel"

# Analyze competitor websites
python scripts/monitor_competitors.py \
  --query "online fitness coaching"

# Cross-analyze all signals
python scripts/analyze_cross_source_signals.py
```

### Research Trust System

Each research signal is automatically labeled:

| Status | Meaning | Action |
|---|---|---|
| `candidate` | Came from a single source | Do not make strategy decisions |
| `validated` | Confirmed from multiple sources | Can use for strategy updates |
| `is_mock: true` | Don't treat as real data, it's mock | Ignore in test environment |

**Important rule:** Do not use mock research signals as real market data. The system forcibly labels these.

### Weekly Research Cycle

```bash
# Run all weekly research with a single command
python scripts/run_weekly_research.py
```

This command:
1. Collects from all active sources
2. Processes signals
3. Produces cross-source report
4. Writes all references to `research/index/collected_references.jsonl`

---

## Scenario 15 — Business Scorecard and Bottleneck Detection

**Situation:** You want to understand which stage of your business you're stuck at.

**Agent used:** `business_scorecard_agent`

**Steps:**

```bash
python scripts/generate_business_scorecard.py \
  --agent business_scorecard_agent \
  --context business_context.yaml
```

**Output:** `outputs/business_scorecards/` → bottleneck analysis, priority order, the number one focus for the week.

### Bottleneck Detection

The system scores these stages:

```
TRAFFIC: Are enough potential clients coming in?
  ↓
LEAD QUALITY: Are the people coming the right avatar?
  ↓
APPLICATION: Is the application form qualifying well enough?
  ↓
SHOW UP: What is the call attendance rate?
  ↓
CLOSE: How many are you closing on sales calls?
  ↓
DELIVERY: Are clients getting results?
  ↓
RETENTION: Are they buying again / giving referrals?
```

**Example Bottleneck Diagnosis:**

```
Traffic: 1000 people/month → GOOD
Lead quality: 60% correct avatar → MEDIUM
Application: 8% fill out form → WEAK ← BOTTLENECK IS HERE
Show up: 70% attend → GOOD
Close: 30% closed → MEDIUM

Recommendation: Strengthen application form with qualification questions.
               Filter better with lead magnet.
```

---

## Scenario 16 — Adding a New Agent

**Situation:** The existing agents aren't enough, you want to add a custom agent to the system.

**Example:** Adding a sales page writing agent.

```bash
# Create a new agent from template
python scripts/create_agent.py \
  --name sales_page_reviewer \
  --role "Sales Page Reviewer"
```

This command automatically creates these files:

```
agents/sales_page_reviewer/
  agent.yaml              ← Configuration
  system_prompt.md        ← Agent behavior (you write this)
  checklist.yaml          ← Quality control rules
  knowledge/              ← Agent-specific knowledge
  memory/                 ← Conversation memory
  outputs/                ← Generated files
```

**Then:**

1. Edit `system_prompt.md` → write the agent's role, operating principles, output format
2. Add quality rules to `checklist.yaml`
3. Set allowed tools in `agent.yaml`
4. Test it:

```bash
python scripts/run_agent.py \
  --agent sales_page_reviewer \
  --message "Review this sales page: [URL or text]"
```

**Checklist:**
- Does it work in mock mode?
- Is it not producing fake claims?
- Is the output format defined?
- Were eval cases written?

```bash
python scripts/validate_agent_structure.py
python -m pytest
```

---

## Scenario 17 — Full Cycle: From Scratch to Scale

This scenario shows the complete journey of an expert using the entire system in sequence.

### Profile Used

> **Zoe, 34, freelance UX designer**
> Has been freelancing for 8 years, charges $150/hour. Wants to multiply her income and work with fewer but higher-value clients. Goal: 3x monthly income in 6 months.

---

### Week 1-2: Foundation Setup

```bash
# 1. Set up the project
pip install -r requirements.txt

# 2. Fill out business_context.yaml
# niche: "UX consulting for SaaS startups"
# avatar: "B2B SaaS founder, losing users but doesn't know why"
# offer: "UX audit + roadmap package"
# price: "5000 USD"

# 3. Evaluate the market
python scripts/generate_market_scorecard.py \
  --agent market_selector \
  --context business_context.yaml

# 4. Deepen the avatar
python scripts/generate_avatar_research.py \
  --agent avatar_pain_researcher \
  --context business_context.yaml
```

**Finding:** The system confirms that the UX problem for SaaS startups is in the "expensive problem" category: bad UX = high churn = investor problem.

---

### Week 3-4: Offer and Pricing

```bash
# 5. Strengthen the offer
python scripts/generate_offer_audit.py \
  --agent offer_architect \
  --context business_context.yaml

# 6. Build the value stack
python scripts/generate_value_stack.py \
  --agent value_stack_builder \
  --context business_context.yaml

# 7. Optimize pricing
python scripts/generate_pricing_guarantee_review.py \
  --agent pricing_guarantee_optimizer \
  --context business_context.yaml
```

**Finding:** $5,000 price is too low; market benchmarks and "expensive problem" analysis support the $15,000-$25,000 range. The system recommends adding a value stack.

**New offer package:**
- UX Audit (2 weeks) → $8,000 perceived value
- Priority Improvement Roadmap → $5,000
- 3-month implementation support → $6,000
- User testing facilitation → $3,000
- **Total perceived value: $22,000**
- **Real price: $15,000**

---

### Week 5-6: Acquisition and Content

```bash
# 8. Acquisition strategy
python scripts/generate_acquisition_plan.py \
  --agent acquisition_strategy_agent \
  --context business_context.yaml

# 9. Content plan
python scripts/generate_content_plan.py \
  --agent content_authority_agent \
  --context business_context.yaml

# 10. LinkedIn and Reddit research
python scripts/collect_source.py \
  --source reddit \
  --query "SaaS UX problems user retention"
```

**Primary channel:** LinkedIn (B2B SaaS founders are on LinkedIn)
**First 30-day plan:**
- 1 LinkedIn post/day (UX mistake analysis, case study, Q&A)
- 10 targeted DMs/week: "I noticed something about your product's onboarding flow…"

---

### Week 7-8: Funnel and Sales

```bash
# 11. Funnel map
python scripts/generate_funnel_map.py \
  --agent funnel_builder \
  --context business_context.yaml

# 12. Sales script
python scripts/generate_sales_script.py \
  --agent sales_script_builder \
  --context business_context.yaml

# 13. Objection bank
python scripts/generate_objection_bank.py \
  --agent objection_handler \
  --context business_context.yaml
```

---

### Month 3+: Ads, Proof and Scale

```bash
# 14. First client case study
python scripts/generate_case_study.py \
  --agent case_study_writer \
  --context business_context.yaml

# 15. Meta ads plan
python scripts/generate_meta_ads_plan.py \
  --agent meta_ads_manager \
  --context business_context.yaml

# 16. YouTube strategy (for authority)
python scripts/generate_youtube_strategy.py \
  --agent youtube_strategy_agent \
  --context business_context.yaml

# 17. Business scorecard — every month
python scripts/generate_business_scorecard.py \
  --agent business_scorecard_agent \
  --context business_context.yaml
```

---

## Dashboard Usage

```bash
# Start the dashboard
python dashboard/server.py

# Open in browser
# http://localhost:8765
```

The dashboard shows:
- Status of all agents
- Memory files for each agent
- Recently generated outputs

No API key required. Runs locally only.

---

## Quality and Test Commands

```bash
# Run all tests
python -m pytest

# Run all checklists
python scripts/run_checklist.py --all

# Validate a specific agent
python scripts/run_checklist.py --agent offer_architect

# Check YAML validity
python scripts/validate_yaml.py

# Validate agent structure
python scripts/validate_agent_structure.py

# Compact context (after long conversations)
python scripts/compact_context.py --agent offer_architect
python scripts/compact_context.py --all

# Run evals
python scripts/run_evals.py --all
```

---

## Common Mistakes

### 1. Using a research signal as validated

```
WRONG: Changing your entire strategy based on a single Reddit comment
RIGHT: If the signal is "candidate", wait until it's confirmed from multiple sources
```

### 2. Keeping the avatar broad

```
WRONG: "Working women aged 30-50"
RIGHT: "Sarah, 38, finance sector manager in London, 2 kids, chronic fatigue"
```

### 3. Touching a campaign in the learning phase

```
WRONG: Ad didn't produce results in 3 days, change it
RIGHT: Wait until ~50 conversions are collected. Touching it resets from zero.
```

### 4. Revealing the price before the value stack

```
WRONG: "My program is $15,000..."
RIGHT: First show the value stack ($22,000 perceived value),
       then "but today only $15,000"
```

### 5. Being vague in a case study

```
WRONG: "My client was very satisfied"
RIGHT: "91 days, 14.3 kg, started waking up at 5:30am, now fits into clothes
       from 3 months ago"
```

### 6. Treating mock data as real market data

The system adds `is_mock: true` to mock research results and uses `mock://` URLs. Do not interpret these as real data.

---

## Next Steps

When you want to run the system with live data, see the "How To Add Real Providers Later" section in [README.md](README.md). You can add real APIs behind the same interfaces:

- `TAVILY_API_KEY` → web research
- `FIRECRAWL_API_KEY` → web page extraction
- `REDDIT_CLIENT_ID` + `REDDIT_CLIENT_SECRET` → Reddit research
- `YOUTUBE_API_KEY` → YouTube content analysis
- `FACEBOOK_AD_LIBRARY_TOKEN` → ad library

All these variables are documented in the `.env.example` file.
