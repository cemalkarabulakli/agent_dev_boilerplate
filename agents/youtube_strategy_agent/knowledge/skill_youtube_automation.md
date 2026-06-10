# Skill: YouTube Automation

Source: YouTube Strategy Agent — Automation Pipeline Framework

## When to Activate This Skill

Use this skill:
- When setting up a faceless channel from scratch
- When transitioning an existing channel to a more automated production pipeline
- When scaling to multiple videos per week without proportionally increasing effort
- When building a second or third channel using the same content machine

## The Automation-First Mindset

> Without appearing on camera, without setting up a studio, with just the right strategy and YouTube automation, it is possible to build a sustainable income model.

Automation does not mean low quality. It means removing the creator as the bottleneck in the production pipeline.

## The 7-Stage Automated Production Pipeline

### Stage 1: Keyword Research Automation
**Goal:** Generate a weekly list of validated video ideas without manual research

**Tools:**
- vidIQ Daily Ideas (curated keyword suggestions for your niche, updated daily)
- TubeBuddy "Suggested Videos" keyword feature
- n8n workflow: pull vidIQ RSS → filter by search volume threshold → store in Notion/Airtable

**Output:** Ranked keyword list with search volume + competition score, updated weekly

**Time investment after setup:** 15 minutes/week to review and approve

---

### Stage 2: Script Generation
**Goal:** Produce a full video script from a keyword in under 30 minutes

**Process:**
1. Input: keyword + target audience + video length + tone
2. Generate outline with ChatGPT or Claude (sonnet-class model)
3. Expand outline into full script with timestamp markers
4. Fact-check all statistics and claims manually (non-negotiable — AI hallucinates facts)
5. Review for natural speech rhythm — edit for voiceover delivery

**Prompt template:**
```
You are a YouTube scriptwriter. Write a [length]-minute script for a video titled: "[TITLE]"
Target audience: [AUDIENCE DESCRIPTION]
Tone: [conversational/authoritative/educational]
Format: Hook (30 sec), Problem Setup (1 min), [N main points with timestamps], CTA (30 sec)
Include pattern interrupts every 2 minutes.
Do not include camera directions.
```

**Output:** Full script with timestamps, ready for voiceover

---

### Stage 3: AI Voiceover
**Goal:** Convert script to natural-sounding voiceover without recording

**Primary tool: ElevenLabs**
- Select voice: choose a voice with appropriate authority for the niche
- Set speed: 1.05–1.10x for natural YouTube pacing
- Add pauses: insert `<break time="0.5s"/>` tags at paragraph breaks in SSML
- Download as MP3

**Alternative tools:**
- **Murf.ai**: larger voice library, good for English-language finance content
- **Play.ht**: ultra-realistic voices, multilingual including Turkish
- **Eleven Multilingual v2**: for Turkish-language faceless content

**Quality check:**
- Listen to full voiceover before video assembly
- Flag: unnatural word stress, mispronounced proper nouns, robotic transitions
- Re-generate specific segments if quality is below standard

---

### Stage 4: Video Assembly
**Goal:** Combine voiceover + visuals into a complete video

**Option A: InVideo AI (fastest)**
- Paste script → AI automatically selects B-roll footage + captions
- Edit mismatched clips manually (15–20 min for a 10-minute video)
- Best for: English-language finance, business, productivity content

**Option B: Pictory (intermediate quality)**
- Paste script → auto-match stock footage + auto-captions
- Upload custom ElevenLabs voiceover
- Best for: documentary-style, explainer content

**Option C: CapCut + Manual Assembly (most control)**
- Import voiceover → manually select and sync stock footage from Pexels/Pixabay/Storyblocks
- Add captions with auto-caption feature
- Add b-roll, lower-thirds, transitions, zoom effects
- Best for: Turkish-language content, custom brand style

**Stock footage sources (free):**
- Pexels Video (pexels.com/videos)
- Pixabay Videos (pixabay.com)
- Coverr.co

**Stock footage sources (paid, better quality):**
- Storyblocks (subscription, $15–$30/month)
- Artgrid (cinematic footage)

---

### Stage 5: Thumbnail Creation
**Goal:** Produce a high-CTR thumbnail in under 20 minutes

**Process:**
1. Choose thumbnail template in Canva (or create custom brand template once)
2. Select background: solid color, blurred screenshot, or MidJourney-generated image
3. Add text overlay: max 3–5 words, large font, high contrast
4. Add optional face or reaction image (AI avatar from HeyGen, or royalty-free stock)
5. Export at 1280×720px, < 2MB

**Thumbnail design rules:**
- Color must contrast with YouTube's white background and dark mode
- Font: bold, sans-serif (Impact, Anton, Bebas Neue)
- Text: communicates benefit or curiosity in < 2 seconds
- Consistent style across all channel thumbnails = brand recognition + higher CTR over time

**A/B testing:**
- Use TubeBuddy's Thumbnail A/B Test feature
- Test first 48 hours — switch if CTR below 4%

---

### Stage 6: SEO Metadata Automation
**Goal:** Publish with fully optimized metadata in under 10 minutes

**Workflow:**
1. Generate title variations with vidIQ or TubeBuddy keyword tool
2. Choose title with primary keyword in first 60 characters
3. Write description: keyword in first 200 characters + timestamps + links
4. Add tags: primary keyword exact match + 5 variations + 3 broad topic tags
5. Set thumbnail, end screens (auto-applied from template)
6. Schedule publish time (use YouTube Analytics "When your viewers are on YouTube" data)

**n8n automation option:**
- Connect vidIQ keyword feed → ChatGPT API → auto-draft title + description → save to Google Sheets for review

---

### Stage 7: Post-Publish Monitoring
**Goal:** Catch underperforming metrics in the first 48 hours and intervene

**48-hour checklist:**
- [ ] CTR checked: below 4% → queue thumbnail A/B test
- [ ] AVD checked: below 40% → review first 60 seconds of video
- [ ] Impressions: very low? → check if title is shadow-indexed (common with new channels)
- [ ] Comments: respond to all comments in first 24 hours → boosts engagement signal

**Weekly analytics review (30 minutes):**
- Which videos gained traffic from Suggested vs. Search vs. Browse?
- Which videos have highest subscriber conversion rate?
- Which keywords drove the most impressions?
- Update content calendar based on findings.

---

## Full Tool Stack Summary

| Stage | Primary Tool | Backup Tool | Cost |
| --- | --- | --- | --- |
| Keyword Research | vidIQ | TubeBuddy | Free–$49/mo |
| Script Generation | Claude / ChatGPT | Jasper | Free–$20/mo |
| Voiceover | ElevenLabs | Murf.ai | $5–$22/mo |
| Video Assembly | InVideo AI | CapCut | Free–$30/mo |
| Stock Footage | Pexels / Pixabay | Storyblocks | Free–$15/mo |
| Thumbnails | Canva Pro | Adobe Express | $13/mo |
| AI Image Gen | MidJourney | Adobe Firefly | $10/mo |
| SEO Metadata | TubeBuddy | vidIQ | Free–$19/mo |
| Workflow Automation | n8n | Make (Integromat) | Free–$20/mo |
| Analytics | YouTube Studio | Social Blade | Free |

**Estimated monthly tool cost for full stack:** $80–$150/month

---

## n8n Automation Workflows (Advanced)

For scaling to 3+ videos/week, automate these workflows:

### Workflow 1: Weekly Keyword Research Pipeline
```
Trigger: Every Monday 9:00 AM
→ Fetch vidIQ Daily Ideas RSS for niche keywords
→ Filter: search volume > 1,000, competition score < 50
→ Send top 10 keywords to Google Sheets (content calendar)
→ Notify via Telegram/email: "Weekly keyword list ready for review"
```

### Workflow 2: Script-to-Brief Auto-Generation
```
Trigger: New keyword row added to Google Sheets (manually approved)
→ Send keyword to Claude API with script prompt template
→ Save draft script to Notion page
→ Notify: "Draft script ready for fact-check"
```

### Workflow 3: Publish Schedule Monitor
```
Trigger: Every 48 hours after video publish
→ Pull YouTube Data API: CTR + AVD for latest video
→ If CTR < 4%: send Telegram alert "Low CTR — check thumbnail"
→ If AVD < 40%: send Telegram alert "Low AVD — review hook"
```

---

## Automation Readiness Assessment

Before activating this skill, confirm:
- [ ] Niche is validated (niche selection complete)
- [ ] First 10 video topics identified from competitor analysis
- [ ] ElevenLabs voice selected and tested
- [ ] Canva thumbnail template created (matches channel brand)
- [ ] vidIQ or TubeBuddy installed and connected to channel
- [ ] Content calendar spreadsheet created (Google Sheets or Notion)
- [ ] n8n or Make account created (for workflow automation, optional at start)
