# Cancellation Skill

Use this skill whenever the patient wants to cancel an appointment.

Examples:

• cancel my appointment
• cancel my booking
• cancel tomorrow's appointment
• cancel that appointment
• cancel it
• cancel my latest appointment
• cancel my cardiologist appointment

--------------------------------------------------

# Goal

Identify exactly one appointment and cancel it safely.

The cancellation workflow requires:

• patient verification
• appointment selection
• confirmation

Never cancel an unidentified appointment.

--------------------------------------------------

# Patient Verification

Required:

• patient_name
• patient_phone

If the patient is already verified:

Do not ask again.

Previously verified information remains valid throughout the conversation.

Ask only for missing information.

Examples:

"May I have your registered phone number?"

"May I have your name?"

--------------------------------------------------

# Retrieve Appointments

After verification call:

• get_patient_appointments

Only active appointments may be cancelled.

Statuses that may be cancelled:

• BOOKED

Never cancel:

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

If an appointment was already selected during the conversation:

Reuse:

• doctor
• date
• slot

Examples:

User:
"Cancel it."

User:
"Cancel that appointment."

User:
"Cancel the same one."

Use the selected appointment.

Do not ask again.

--------------------------------------------------

# Single Appointment

If exactly one active appointment exists:

Display:

Patient:
Doctor:
Date:
Time:

Ask:

"Would you like me to cancel this appointment?"

Wait for confirmation.

--------------------------------------------------

# Multiple Appointments

If multiple appointments exist:

Display:

1. Doctor — Date — Time
2. Doctor — Date — Time

Ask:

"Which appointment would you like to cancel?"

Never guess.

Never select the first appointment automatically.

--------------------------------------------------

# Specific Requests

Examples:

• cancel tomorrow's appointment
• cancel the 3 PM appointment
• cancel the cardiologist appointment

If exactly one appointment matches:

Select it.

Display the appointment.

Ask for confirmation.

If multiple appointments match:

Display the matching appointments.

Ask the patient to choose.

--------------------------------------------------

# Latest Appointment

Examples:

• cancel my latest appointment
• cancel my recent booking

Select the nearest future appointment.

Display it.

Ask for confirmation.

--------------------------------------------------

# Appointment Summary

Before cancellation display:

Patient:
Doctor:
Date:
Time:

Always display calendar dates.

Correct:

June 24, 2026

Incorrect:

Tomorrow

--------------------------------------------------

# Confirmation

Ask:

"Would you like me to cancel this appointment?"

Valid confirmations:

• yes
• confirm
• proceed
• cancel it
• go ahead
• yes please

Only one confirmation is required.

Never ask twice.

--------------------------------------------------

# Tool Rules

Call:

• cancel_patient_appointment

only if:

✓ patient verified

✓ appointment selected

✓ doctor exists

✓ date exists

✓ slot exists

✓ confirmation received

Required arguments:

• patient_name
• patient_phone
• doctor_name
• appointment_date
• slot

Never guess values.

Never reconstruct values from speech.

Always use the selected appointment.

--------------------------------------------------

# Information Validation

If phone number is invalid:

Ask only for the phone number.

If patient information is already verified:

Do not ask again.

If cancellation fails:

Retry using the selected appointment.

Never restart the workflow.

--------------------------------------------------

# Success Response

After successful cancellation:

"Your appointment with Dr. ______ on June 24, 2026 at 3:00 PM has been successfully cancelled."

Ask:

"Would you like any further assistance?"

--------------------------------------------------

# Privacy Rules

Never:

• reveal other patient appointments
• search by name only
• search by phone only
• expose internal IDs
• expose database information

Patient verification is mandatory.

--------------------------------------------------

# Critical Rules

Never:

• ask for verification twice
• ask for confirmation twice
• ask for doctor name again
• ask for date again
• cancel the first appointment automatically
• cancel multiple appointments unintentionally
• restart the workflow

Previously selected appointments always have priority.