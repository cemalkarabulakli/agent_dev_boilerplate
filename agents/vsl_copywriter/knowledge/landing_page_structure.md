# Landing Page Structure

Source: VSL Copywriter Agent — Landing Page Framework

## Purpose

A single-page funnel designed to move one type of visitor to one action: applying for a free consultation. Everything on the page serves this one goal.

---

## Sections (Fixed Order)

### 1. Headline (Обръщение към аудиторията)

One sentence that tells the visitor WHO this page is for.

Template: "За [тип човек], който [болка]"

Rules:
- Maximum 1-2 lines
- Name the exact person and their exact problem
- Do not try to include everyone
- Provide 2 variants for the user to choose from

---

### 2. Subheadline (Голямо обещание)

1-2 sentences. Specific result + specific timeframe + without what pain/obstacle.

Template: "Открий как да [конкретен резултат] в [конкретно време], без [без какво]"

Rules:
- Must include a measurable or observable result
- Must include a time frame
- Must name what they do NOT need to do or sacrifice
- No generic promises like "change your life"
- Provide 2 variants for the user to choose from

---

### 3. VSL Embed

- 16:9 video placeholder
- Under the placeholder: "Гледай до края, преди да кликнеш бутона."
- Purpose: hold attention before CTA

---

### 4. CTA Button

- Large, prominent, single button
- Default text: "Кандидатствай за безплатна консултация"
- Below button: "Без обещания. Без натиск. Само разговор."
- Button links to: /apply page

Rules:
- One CTA only on the page
- Trust reducer below button is mandatory
- No secondary links or navigation that pull away from the CTA

---

### 5. Qualification Quiz (Multi-step form on /apply)

Questions to qualify applicants before they book a call. One question per screen with progress bar.

**For Beginner or small offer:**
1. Какво правиш в момента?
2. Какъв е най-големият ти проблем точно сега?
3. Какво си опитвал досега?
4. Кога искаш да започнеш?

**For Medium or high-ticket offer:**
1. Какво правиш в момента и какъв оборот?
2. Колко можеш да инвестираш в развитие?
3. Какво си опитвал досега?
4. Кога искаш да видиш резултат?

Always end with: Име, Имейл, Телефон

After submission: redirect to /calendar with a brief "Благодаря, [Име]!" message.

---

### 6. Calendar (/calendar page)

- Shows available slots for the next 14 days
- After slot selection: "Резервацията ти е потвърдена за [дата и час]"
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
