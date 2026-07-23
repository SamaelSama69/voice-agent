# Date Reasoning Skill

Use this skill whenever the patient mentions:

• today
• tomorrow
• day after tomorrow
• next Monday
• this Friday
• next week
• same day
• same date
• that day
• June 25
• 25 June
• tomorrow morning
• tomorrow afternoon

--------------------------------------------------

# Goal

Resolve relative dates safely and consistently.

All appointment tools require:

YYYY-MM-DD

Never pass:

• tomorrow
• next Monday
• same day

to tools.

--------------------------------------------------

# Tool Rule

Before resolving any relative date call:

• get_current_date

This tool is the source of truth.

Never calculate dates using model memory.

Never assume today's date.

--------------------------------------------------

# Relative Dates

Examples:

today

tomorrow

day after tomorrow

next Monday

this Friday

next week

Always convert to:

YYYY-MM-DD

--------------------------------------------------

# Examples

Current date:

2026-06-23

today

→ 2026-06-23

tomorrow

→ 2026-06-24

day after tomorrow

→ 2026-06-25

--------------------------------------------------

# Weekday Resolution

Examples:

• next Monday
• next Tuesday
• this Friday

Always calculate the actual calendar date.

Display:

"Next Monday is June 29, 2026."

--------------------------------------------------

# Partial Dates

Examples:

• June 25
• 25 June
• 23rd this month

Use the current year unless the patient specifies another year.

Convert to:

YYYY-MM-DD

Examples:

June 25

→ 2026-06-25

--------------------------------------------------

# Ambiguous Dates

Examples:

• sometime next week
• later this month
• weekend
• next weekend

Ask for clarification.

Examples:

"Which day next week would you prefer?"

"Would you prefer Saturday or Sunday?"

Never guess.

--------------------------------------------------

# Conversation Context

Dates already selected remain valid.

Remember:

• appointment_date
• selected_appointment

Examples:

User:

"Same day."

Use the existing appointment date.

User:

"Move it to 3 PM."

Reuse the current appointment date.

--------------------------------------------------

# Selected Appointment Priority

If an appointment is already selected:

Reuse:

• appointment date

Examples:

User:

"Move it to 2 PM."

Keep the existing date.

User:

"Same day afternoon."

Reuse the existing date.

Previously selected appointment information has priority.

--------------------------------------------------

# Same Day Changes

Examples:

• same day
• same date
• that day
• later that day

Use:

selected appointment date

Do not ask for another date.

--------------------------------------------------

# Time Preferences

Examples:

• morning
• afternoon
• evening

Morning:

before 12 PM

Afternoon:

12 PM to 4 PM

Evening:

after 4 PM

These are not appointment slots.

Available slots must be retrieved.

Examples:

Available:

• 12:00 PM
• 01:00 PM
• 02:00 PM

User:

"Tomorrow afternoon."

Respond:

"The available afternoon slots are 12:00 PM, 1:00 PM, and 2:00 PM. Which would you prefer?"

Never automatically choose a slot.

--------------------------------------------------

# Past Dates

Appointments cannot be:

• booked in the past
• rescheduled to the past

If the calculated date is earlier than today:

"Appointments cannot be scheduled for a past date."

Stop the workflow.

--------------------------------------------------

# Date Display

Never display:

• today
• tomorrow
• next Monday
• same day

in appointment summaries.

Always display calendar dates.

Correct:

June 24, 2026

Incorrect:

Tomorrow

--------------------------------------------------

# Tool Rules

Before calling:

• get_available_slots
• check_availability
• book_appointment
• reschedule_patient_appointment

Always convert dates to:

YYYY-MM-DD

Correct:

2026-06-24

Incorrect:

tomorrow

--------------------------------------------------

# Voice Examples

Examples:

• tomorrow morning
• tomorrow afternoon
• next Tuesday evening

Workflow:

1. Resolve the date.
2. Retrieve available slots.
3. Filter matching times.
4. Ask the patient.

Never create slots.

--------------------------------------------------

# Information Validation

If the date is unclear:

Ask only for the date.

Examples:

"Which day next week would you prefer?"

Never restart the workflow.

--------------------------------------------------

# Success Examples

Examples:

"Tomorrow is June 24, 2026."

"Next Monday is June 29, 2026."

"The available afternoon slots on June 24, 2026 are 1 PM and 2 PM."

--------------------------------------------------

# Critical Rules

Never:

• guess dates
• assume today's date
• pass relative dates to tools
• create appointment slots
• select a slot automatically

Date resolution must happen before appointment tools are called.