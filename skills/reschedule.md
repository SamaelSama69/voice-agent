# Reschedule Skill

Use this skill whenever the patient wants to modify an existing appointment.

Examples:

• reschedule my appointment
• change my appointment
• move my appointment
• change my booking
• move it to tomorrow
• change the time
• move it to 3 PM
• reschedule that appointment

--------------------------------------------------

# Goal

Reschedule exactly one active appointment.

A reschedule requires:

• verified patient
• selected appointment
• new date
• new slot
• confirmation

Never reschedule an unidentified appointment.

--------------------------------------------------

# Patient Verification

Required:

• patient_name
• patient_phone

If already verified:

Do not ask again.

Previously verified information remains valid for the entire conversation.

Ask only for missing information.

--------------------------------------------------

# Retrieve Appointments

After verification call:

• get_patient_appointments

Only appointments with status:

• BOOKED

may be rescheduled.

Never reschedule:

• CANCELLED
• COMPLETED
• NO_SHOW

--------------------------------------------------

# No Active Appointments

If no active appointments exist:

"I couldn't find any active appointments associated with your information."

Stop the workflow.

--------------------------------------------------

# Selected Appointment

If an appointment has already been selected:

Reuse:

• doctor
• old_date
• old_slot

Examples:

User:
"Reschedule it."

User:
"Move that appointment."

User:
"Change the same appointment."

Use the selected appointment.

Do not ask again.

--------------------------------------------------

# Single Appointment

If exactly one appointment exists:

Display:

Patient:
Doctor:
Date:
Time:
Status:

Ask:

"Would you like to reschedule this appointment?"

--------------------------------------------------

# Multiple Appointments

If multiple appointments exist:

Display:

1. Doctor — Date — Time
2. Doctor — Date — Time

Ask:

"Which appointment would you like to reschedule?"

Never guess.

Never select the first appointment automatically.

--------------------------------------------------

# Date Changes

Ask:

"What date would you like to reschedule to?"

Accept:

• today
• tomorrow
• next Monday
• June 25
• 25 June

Always resolve relative dates.

Never pass:

• tomorrow
• next Monday

to tools.

Convert to:

YYYY-MM-DD

--------------------------------------------------

# Same Day Changes

Examples:

• same day
• same date
• later that day
• move it to 3 PM

Reuse:

• old_date

Do not ask for another date.

--------------------------------------------------

# Available Slots

After determining the new date call:

• get_available_slots

Always retrieve fresh slots.

Never reuse old slot lists.

Only returned slots may be selected.

--------------------------------------------------

# Time Preferences

Morning:
before 12 PM

Afternoon:
12 PM–4 PM

Evening:
after 4 PM

If multiple slots match:

Display:

• 01:00 PM
• 02:00 PM
• 03:00 PM

Ask:

"Which slot would you prefer?"

Never automatically select a slot.

--------------------------------------------------

# Unavailable Slots

If the requested slot is unavailable:

Display available alternatives.

Example:

"The 2 PM slot is unavailable.

Available slots:

• 11:00 AM
• 01:00 PM
• 03:00 PM"

Ask the patient to choose.

--------------------------------------------------

# Same Date and Same Time

If:

old_date == new_date

and

old_slot == new_slot

Respond:

"Your appointment is already scheduled for that date and time."

Do not call the reschedule tool.

--------------------------------------------------

# Doctor Changes

Rescheduling changes only:

• date
• time

Doctor changes require a new booking.

If the patient wants another doctor:

Start the booking workflow.

--------------------------------------------------

# Appointment Summary

Before rescheduling display:

Patient:
Phone:
Doctor:
Old Date:
Old Time:
New Date:
New Time:

Always display actual calendar dates.

Correct:

June 24, 2026

Incorrect:

Tomorrow

--------------------------------------------------

# Confirmation

Ask:

"Would you like me to confirm this rescheduling?"

Valid confirmations:

• yes
• confirm
• proceed
• go ahead
• reschedule it
• yes please

Only one confirmation is required.

Never ask twice.

--------------------------------------------------

# Tool Rules

Call:

• reschedule_patient_appointment

only if:

✓ patient verified

✓ appointment selected

✓ new date selected

✓ new slot selected

✓ summary displayed

✓ confirmation received

Required arguments:

• patient_name
• patient_phone
• doctor_name
• old_date
• old_slot
• new_date
• new_slot

Never guess values.

Always use the selected appointment.

--------------------------------------------------

# Information Validation

If date is invalid:

Ask only for the date.

If slot is unavailable:

Show available slots.

If phone number is invalid:

Ask only for the phone number.

Never restart the workflow.

--------------------------------------------------

# Success Response

After successful rescheduling:

"Your appointment with Dr. ______ has been successfully rescheduled to June 24, 2026 at 3:00 PM."

Ask:

"Would you like any further assistance?"

--------------------------------------------------

# Privacy Rules

Never:

• reveal other patient appointments
• expose internal IDs
• expose database information

Only verified patients may reschedule appointments.

--------------------------------------------------

# Critical Rules

Never:

• ask for verification twice
• ask for confirmation twice
• ask for the doctor again
• ask for the old appointment again
• select the first appointment automatically
• change doctors during rescheduling
• restart the workflow

Previously selected appointments always have priority.