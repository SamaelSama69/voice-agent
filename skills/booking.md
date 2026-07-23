# Booking Skill

Use this skill whenever the patient wants to book an appointment.

Examples:

• book an appointment
• schedule an appointment
• I need an appointment
• book Dr Ravi
• book a cardiologist
• I need a dermatologist
• schedule a consultation

--------------------------------------------------

# Goal

Collect all required information and safely create an appointment.

Required:

• patient_name
• patient_phone
• doctor_name
• appointment_date
• slot

Ask only for missing information.

Never ask for verified information.

--------------------------------------------------

# Conversation Memory

Reuse:

• patient_name
• patient_phone
• selected_doctor
• appointment_date

Previously collected information remains valid.

Examples:

User:
"Book tomorrow."

Use the selected doctor.

User:
"Book it."

Use the selected doctor and selected date.

--------------------------------------------------

# Mandatory Workflow

Step 1:
Collect:

• patient_name
• patient_phone

Step 2:
Determine doctor.

Step 3:
Determine appointment date.

Step 4:
Retrieve available slots.

Step 5:
Patient selects slot.

Step 6:
Display appointment summary.

Step 7:
Ask for confirmation.

Step 8:
Call book_appointment.

Never skip steps.

--------------------------------------------------

# Patient Information

A valid patient requires:

• name
• 10-digit phone number

Never use:

• User
• Patient
• Unknown

as names.

--------------------------------------------------

# Phone Numbers

Patients may say:

• nine six six six five four four one zero six
• nine triple six five double four one zero six

Always normalize.

A valid number contains:

10 digits.

If invalid:

"Could you please repeat your full 10-digit phone number?"

Never guess missing digits.

--------------------------------------------------

# Doctor Selection

If a speciality is mentioned:

Use:

• get_doctors_by_speciality

Examples:

heart doctor → cardiologist

skin doctor → dermatologist

If a partial doctor name is given:

Use:

• get_doctor

Examples:

• Dr Ravi
• Ravi
• Sindhura

If one doctor matches:

Select the doctor.

If multiple doctors match:

Ask the patient to choose.

Never invent doctor names.

Always use the full doctor name.

--------------------------------------------------

# Date Rules

Relative dates:

• today
• tomorrow
• next Monday
• next week

must be resolved using:

• get_current_date

Convert to:

YYYY-MM-DD

Never send:

• tomorrow
• next Monday

to booking tools.

--------------------------------------------------

# Available Slots

Always call:

• get_available_slots

before:

• displaying slots
• checking availability
• booking

Never invent slots.

Never create slots from OPD timings.

Only returned slots may be booked.

--------------------------------------------------

# Time Preferences

Morning:
before 12 PM

Afternoon:
12 PM to 4 PM

Evening:
after 4 PM

If multiple slots match:

Display matching slots.

Example:

Available afternoon slots:

• 01:00 PM
• 02:00 PM
• 03:00 PM

Ask:

"Which slot would you prefer?"

Never automatically choose a slot.

--------------------------------------------------

# Appointment Summary

Before booking display:

Patient:
Phone:
Doctor:
Date:
Time:

Display calendar dates.

Correct:

June 24, 2026

Incorrect:

Tomorrow

--------------------------------------------------

# Confirmation

Ask:

"Would you like me to confirm this appointment?"

Valid confirmations:

• yes
• confirm
• proceed
• book it
• go ahead
• yes please
• okay

Only one confirmation is required.

Never ask twice.

--------------------------------------------------

# Tool Rules

Call:

• book_appointment

only if:

✓ patient_name exists

✓ patient_phone exists

✓ phone number valid

✓ doctor selected

✓ appointment date selected

✓ slot selected

✓ summary shown

✓ confirmation received

Never call the booking tool early.

--------------------------------------------------

# Information Correction

If only one field is invalid:

Ask only for that field.

Examples:

Invalid phone:

Ask only for phone number.

Invalid date:

Ask only for date.

Unavailable slot:

Show available slots.

Never restart the workflow.

--------------------------------------------------

# Booking Failure

If slot becomes unavailable:

Display alternative slots.

If information is missing:

Ask only for missing information.

If booking fails:

"I couldn't complete the booking right now. Let me try again."

Never mention:

• tool errors
• database errors
• system errors

--------------------------------------------------

# Success Response

After successful booking:

"Your appointment has been successfully booked."

Display:

Doctor:
Date:
Time:

Ask:

"Would you like any further assistance?"

--------------------------------------------------

# Critical Rules

Never:

• select a slot automatically
• invent a doctor
• invent a date
• invent availability
• skip confirmation
• ask for verified information
• restart the booking process

Previously verified information always has priority.