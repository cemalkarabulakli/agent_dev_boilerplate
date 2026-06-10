# Lovable Build Prompts

Source: VSL Copywriter Agent — Lovable Integration Framework

## Usage Rules

- Give ONE prompt at a time. Wait for confirmation before the next.
- After each prompt: "Is it done? Would you like any changes before we continue?"
- Fill in all placeholders with the specific user data — never leave generic placeholders in the final prompts.

---

## Prompt 1: Landing Page

Confirm color palette before writing this prompt. Replace all [PLACEHOLDER] values with actual user data.

```
Create a high-converting landing page in the target language.

DESIGN:
- Style: modern, premium, minimalist
- Color palette: [HEX_PRIMARY] background, [HEX_ACCENT] accent, [HEX_TEXT] text
- Typography: clean, readable. Headline: bold, large. Body: comfortable reading size (18px+).
- Layout: single column, mobile-first
- White space: generous

STRUCTURE (top to bottom):

1. HERO SECTION:
- Headline (H1): "[HEADLINE_CHOSEN_BY_USER]"
- Subheadline: "[SUBHEADLINE_CHOSEN_BY_USER]"
- Below subheadline: video placeholder (16:9 aspect ratio) with text "VSL will be added here"
- Below video: small text "Watch to the end before clicking the button."

2. CTA BUTTON:
- Large, prominent button below the video
- Text on button: "Apply for a free consultation"
- Below button: "No promises. No pressure. Just a conversation."
- Button should NOT link anywhere yet — we'll connect it in the next step.

3. FOOTER:
- Simple footer with copyright and contact info

REQUIREMENTS:
- Mobile responsive
- Fast loading
- No animations or distracting elements
- Focus is the video and the button

Use Tailwind CSS. Make it clean and conversion-focused.
```

---

## Prompt 2: Quiz + Button Connection + Database

Fill in the quiz questions from the landing page plan before sending.

```
Now let's add a quiz/application form.

CREATE:
1. A new page/route called "/apply"
2. Connect the main CTA button on the landing page to navigate to "/apply"

QUIZ STRUCTURE:
The quiz should be a multi-step form (one question at a time, with progress bar).

Questions:
[QUESTION_1]
[QUESTION_2]
[QUESTION_3]
[QUESTION_4]

Final step:
- Name
- Email
- Phone

DATA STORAGE:
- Use Supabase (built into Lovable)
- Create a table called "applications" with columns:
  - id (auto)
  - created_at (auto)
  - answer_1, answer_2, answer_3, answer_4 (text)
  - name (text)
  - email (text)
  - phone (text)
  - status (default: "new")

UX:
- One question per screen with smooth transition
- Progress bar at top
- "Next" and "Back" buttons
- After final submission, redirect to "/calendar" page
- Show a brief "Thank you, [Name]!" message before redirect

DESIGN:
- Match the style of the landing page
- Same colors, same typography
```

---

## Prompt 3: Calendar

Before writing this prompt, ask the user: "What hours do you want available for consultations? For example: Monday–Friday, 10:00–17:00, 30-minute slots."

Fill in the availability before sending.

```
Create a calendar booking page at "/calendar".

PURPOSE:
After someone submits the application form, they land here to book a consultation slot.

FUNCTIONALITY:
1. Show available time slots for the next 14 days
2. Available hours: [USER_SPECIFIED_HOURS — e.g. Mon-Fri, 10:00-17:00, 30-min slots]
3. User selects a slot
4. After selection, show confirmation: "Your booking is confirmed for [date and time]"

DATA STORAGE:
- Add a new table "bookings" in Supabase:
  - id (auto)
  - created_at (auto)
  - application_id (foreign key to applications table)
  - booking_date (timestamp)
  - status (default: "confirmed")

- Connect this booking to the application from the previous step (use email or session to match)

DESIGN:
- Same style as landing page and quiz
- Clean calendar interface
- Available slots visible, booked slots greyed out
```

---

## Prompt 4: Zoom Integration

Fill in the expert's name before sending.

```
Add Zoom integration for confirmed bookings.

WHEN A BOOKING IS CONFIRMED:
1. Generate a Zoom meeting link automatically
2. Send the link via email to the applicant
3. Save the Zoom link in the bookings table (add a column "zoom_link")

REQUIREMENTS:
- Use Zoom API (the user will need to add Zoom credentials in environment variables)
- Email should include: date, time, Zoom link, brief reminder of the consultation
- Email should be in the expert's target language

EMAIL TEMPLATE:
Subject: "Your booking is confirmed — [date]"
Body:
"Hey [Name],

Your free consultation booking is confirmed.

Date: [date]
Time: [time]
Zoom link: [zoom link]

See you soon,
[EXPERT_NAME]"

NOTE: If Zoom API setup is complex, alternatively create a manual flow:
- Save booking
- Send email with placeholder text saying "You will receive a Zoom link within 24 hours"
- Notify the admin ([EXPERT_EMAIL]) via email about new booking
```

---

## Color Palette Reference

Niche → Recommended palette:

| Niche | Option A | Option B |
|-------|----------|----------|
| Business/Consulting | dark navy (#0A1628) + gold (#C9A84C) | dark green (#0D2B1D) + lime (#A8E63D) |
| Health/Wellness | soft cream (#FAF7F2) + sage (#7A9E7E) | off-white (#F5F0EB) + terracotta (#C17A5A) |
| Creative/Art | off-black (#1A1A1A) + bright accent | warm beige (#F2EBE0) + bold color |
| Finance/Investment | deep blue (#0B1F3A) + gold (#D4AF37) | charcoal (#2D2D2D) + emerald (#2ECC71) |
| Technology/Online | dark (#0E0E0E) + lime green (#A8E63D) | dark (#0E0E0E) + electric blue (#00A8FF) |
| Coaching/Development | warm white (#FDFAF6) + deep accent | soft tones + bold accent |
