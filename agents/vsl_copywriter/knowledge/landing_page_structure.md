# Landing Page Structure

Source: VSL Copywriter Agent — Landing Page Framework

## Purpose

A single-page funnel designed to move one type of visitor to one action: applying for a free consultation. Everything on the page serves this one goal.

---

## Sections (Fixed Order)

### 1. Headline (Audience Address)

One sentence that tells the visitor WHO this page is for.

Template: "For [type of person] who [pain]"

Rules:
- Maximum 1-2 lines
- Name the exact person and their exact problem
- Do not try to include everyone
- Provide 2 variants for the user to choose from

---

### 2. Subheadline (Big Promise)

1-2 sentences. Specific result + specific timeframe + without what pain/obstacle.

Template: "Discover how to [specific result] in [specific timeframe], without [what they don't need]"

Rules:
- Must include a measurable or observable result
- Must include a time frame
- Must name what they do NOT need to do or sacrifice
- No generic promises like "change your life"
- Provide 2 variants for the user to choose from

---

### 3. VSL Embed

- 16:9 video placeholder
- Under the placeholder: "Watch to the end before clicking the button."
- Purpose: hold attention before CTA

---

### 4. CTA Button

- Large, prominent, single button
- Default text: "Apply for a free consultation"
- Below button: "No promises. No pressure. Just a conversation."
- Button links to: /apply page

Rules:
- One CTA only on the page
- Trust reducer below button is mandatory
- No secondary links or navigation that pull away from the CTA

---

### 5. Qualification Quiz (Multi-step form on /apply)

Questions to qualify applicants before they book a call. One question per screen with progress bar.

**For Beginner or small offer:**
1. What do you do right now?
2. What is your biggest problem right now?
3. What have you tried so far?
4. When do you want to start?

**For Medium or high-ticket offer:**
1. What do you do right now and what is your revenue?
2. How much can you invest in development?
3. What have you tried so far?
4. When do you want to see results?

Always end with: Name, Email, Phone

After submission: redirect to /calendar with a brief "Thank you, [Name]!" message.

---

### 6. Calendar (/calendar page)

- Shows available slots for the next 14 days
- After slot selection: "Your booking is confirmed for [date and time]"
- After confirmation: Zoom link sent via email
- Data stored in Supabase bookings table

---

## Design Principles

- Mobile-first, single column
- Generous white space
- No animations or distracting elements
- No navigation menu
- No social media links
- Focus: video → button → done

---

## Color Strategy by Niche

Business/Consulting: dark navy + gold accent | dark green + lime accent
Health/Wellness: soft cream + sage green | off-white + terracotta
Creative/Art: off-black + bright accent | warm beige + bold color
Finance/Investment: deep blue + gold | charcoal + emerald
Technology/Online business: dark + lime green | dark + electric blue
Coaching/Development: warm white + deep accent | soft tones + bold accent

Always explain WHY a specific palette fits the niche before applying it.
