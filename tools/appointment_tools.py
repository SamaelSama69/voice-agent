from langchain_core.tools import tool

from app.database import SessionLocal
from app.models import Doctor, Appointment

from datetime import date, datetime, timedelta

from sqlalchemy import func

import re


# ============================================================
# STANDARD RESPONSE HELPERS
# ============================================================

def success(message: str, data=None):
    return {
        "status": "success",
        "message": message,
        "data": data
    }


def failure(message: str):
    return {
        "status": "failed",
        "message": message
    }


# ============================================================
# PHONE NORMALIZATION
# ============================================================

@tool
def normalize_phone_number(phone: str):
    """
    Convert spoken phone numbers into digits.
    """

    if not phone:
        return failure("phone number required")

    phone = phone.lower()

    words = {
        "zero": "0",
        "oh": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }

    phone = re.sub(r"[^a-zA-Z0-9\s]", " ", phone)

    tokens = phone.split()

    result = []

    i = 0

    while i < len(tokens):

        token = tokens[i]

        if token == "double" and i + 1 < len(tokens):
            digit = words.get(tokens[i + 1])

            if digit:
                result.extend([digit, digit])

            i += 2
            continue

        if token == "triple" and i + 1 < len(tokens):
            digit = words.get(tokens[i + 1])

            if digit:
                result.extend([digit] * 3)

            i += 2
            continue

        if token in words:
            result.append(words[token])

        elif token.isdigit():
            result.extend(list(token))

        i += 1

    normalized = "".join(result)

    if len(normalized) != 10:
        return failure(
            "phone number must contain exactly 10 digits"
        )

    return success(
        "phone number normalized",
        {
            "phone": normalized
        }
    )


@tool
def get_current_date():
    """
    Returns today's and tomorrow's dates.
    """

    today = date.today()

    tomorrow = today + timedelta(days=1)

    return success(
        "current date retrieved",
        {
            "today": today.strftime("%Y-%m-%d"),
            "tomorrow": tomorrow.strftime("%Y-%m-%d")
        }
    )


@tool
def get_doctors():
    """
    Retrieve all doctors.
    """

    db = SessionLocal()

    try:

        doctors = db.query(Doctor).all()

        if not doctors:
            return failure("no doctors found")

        data = []

        for d in doctors:
            data.append({
                "name": d.name,
                "speciality": d.speciality,
                "experience": d.experience,
                "languages": d.languages,
                "timings": d.opd_timings,
                "services": d.services,
                "location": d.location,
                "hospital": d.hospital
            })

        return success(
            "doctors retrieved",
            data
        )

    finally:
        db.close()



@tool
def get_doctors_by_speciality(speciality: str):
    """
    Retrieve doctors by speciality.
    """

    if not speciality:
        return failure("speciality required")

    db = SessionLocal()

    try:

        speciality = speciality.strip().lower()

        doctors = (
            db.query(Doctor)
            .filter(
                Doctor.speciality.ilike(
                    f"%{speciality}%"
                )
            )
            .all()
        )

        if not doctors:
            return failure(
                "no doctors found for this speciality"
            )

        data = []

        for d in doctors:
            data.append({
                "name": d.name,
                "speciality": d.speciality,
                "experience": d.experience,
                "languages": d.languages,
                "timings": d.opd_timings
            })

        return success(
            "doctors found",
            data
        )

    finally:
        db.close()


@tool
def get_doctor(doctor_name: str):
    """
    Search doctor using partial or full name.
    """

    if not doctor_name:
        return failure("doctor name required")

    db = SessionLocal()

    try:

        search_name = (
            doctor_name
            .replace("Dr.", "")
            .replace("Dr", "")
            .strip()
        )

        doctors = (
            db.query(Doctor)
            .filter(
                Doctor.name.ilike(
                    f"%{search_name}%"
                )
            )
            .all()
        )

        if not doctors:
            return failure("doctor not found")

        data = []

        for d in doctors:
            data.append({
                "name": d.name,
                "speciality": d.speciality,
                "experience": d.experience,
                "languages": d.languages,
                "timings": d.opd_timings
            })

        return success(
            "doctor found",
            data
        )

    finally:
        db.close()


@tool
def get_patient_appointments(
    patient_phone: str,
    patient_name: str
):
    """
    Retrieve active appointments belonging to a verified patient.
    Only BOOKED appointments are returned.
    """

    if not patient_name:
        return failure("patient name required")

    if not patient_phone:
        return failure("phone number required")

    phone_result = normalize_phone_number.invoke(
        {"phone": patient_phone}
    )

    if phone_result["status"] == "failed":
        return phone_result

    patient_phone = phone_result["data"]["phone"]

    normalized_name = patient_name.strip().title()

    db = SessionLocal()

    try:

        appointments = (
            db.query(Appointment)
            .filter(
                func.lower(Appointment.patient_name)
                == normalized_name.lower(),
                Appointment.patient_phone == patient_phone,
                Appointment.status == "BOOKED"
            )
            .order_by(
                Appointment.appointment_date,
                Appointment.slot
            )
            .all()
        )

        if not appointments:
            return failure(
                "no active appointments found"
            )

        data = []

        for a in appointments:
            data.append({
                "doctor": a.doctor_name,
                "date": a.appointment_date,
                "slot": a.slot,
                "status": a.status
            })

        return success(
            "appointments found",
            data
        )

    finally:
        db.close()


@tool
def get_appointment_history(
    patient_phone: str,
    patient_name: str
):
    """
    Retrieve all appointments including:
    BOOKED
    CANCELLED
    COMPLETED
    NO_SHOW
    """

    if not patient_name:
        return failure("patient name required")

    if not patient_phone:
        return failure("phone number required")

    phone_result = normalize_phone_number.invoke(
        {"phone": patient_phone}
    )

    if phone_result["status"] == "failed":
        return phone_result

    patient_phone = phone_result["data"]["phone"]

    normalized_name = patient_name.strip().title()

    db = SessionLocal()

    try:

        appointments = (
            db.query(Appointment)
            .filter(
                func.lower(Appointment.patient_name)
                == normalized_name.lower(),
                Appointment.patient_phone == patient_phone
            )
            .order_by(
                Appointment.appointment_date,
                Appointment.slot
            )
            .all()
        )

        if not appointments:
            return failure(
                "no appointment history found"
            )

        data = []

        for a in appointments:
            data.append({
                "doctor": a.doctor_name,
                "date": a.appointment_date,
                "slot": a.slot,
                "status": a.status
            })

        return success(
            "appointment history found",
            data
        )

    finally:
        db.close()


@tool
def get_available_slots(
    doctor_name: str,
    appointment_date: str
):
    """
    Retrieve available appointment slots.
    """

    if not doctor_name:
        return failure("doctor name required")

    if not appointment_date:
        return failure("appointment date required")

    try:
        datetime.strptime(
            appointment_date,
            "%Y-%m-%d"
        )
    except ValueError:
        return failure(
            "invalid appointment date"
        )

    db = SessionLocal()

    try:

        search_name = (
            doctor_name
            .replace("Dr.", "")
            .replace("Dr", "")
            .strip()
        )

        doctor = (
            db.query(Doctor)
            .filter(
                Doctor.name.ilike(
                    f"%{search_name}%"
                )
            )
            .first()
        )

        if not doctor:
            return failure("doctor not found")

        timing = doctor.opd_timings

        match = re.search(
            r'(\d{1,2}:\d{2}\s*[AP]M).*?(\d{1,2}:\d{2}\s*[AP]M)',
            timing
        )

        if not match:
            return failure(
                "unable to determine doctor timings"
            )

        start_time = datetime.strptime(
            match.group(1),
            "%I:%M %p"
        )

        end_time = datetime.strptime(
            match.group(2),
            "%I:%M %p"
        )

        slots = []

        current = start_time

        while current < end_time:

            slots.append(
                current.strftime("%I:%M %p")
            )

            current += timedelta(hours=1)

        booked = (
            db.query(Appointment)
            .filter(
                Appointment.doctor_name == doctor.name,
                Appointment.appointment_date == appointment_date,
                Appointment.status == "BOOKED"
            )
            .all()
        )

        booked_slots = [
            a.slot for a in booked
        ]

        available = [
            slot
            for slot in slots
            if slot not in booked_slots
        ]

        if not available:
            return failure(
                "no slots available"
            )

        return success(
            "available slots retrieved",
            available
        )

    finally:
        db.close()


@tool
def check_availability(
    doctor_name: str,
    appointment_date: str,
    slot: str
):
    """
    Check whether a slot is available.
    """

    if not slot:
        return failure("slot required")

    slot = slot.strip().upper()

    slot_result = get_available_slots.invoke(
        {
            "doctor_name": doctor_name,
            "appointment_date": appointment_date
        }
    )

    if slot_result["status"] == "failed":
        return slot_result

    available_slots = slot_result["data"]

    return success(
        "availability checked",
        {
            "available": slot in available_slots,
            "requested_slot": slot,
            "available_slots": available_slots
        }
    )



@tool
def book_appointment(
    patient_name: str,
    patient_phone: str,
    doctor_name: str,
    appointment_date: str,
    slot: str
):
    """
    Create a new appointment.

    This tool assumes the agent has already:
    - collected all information
    - shown appointment summary
    - received confirmation
    """

    if not patient_name:
        return failure("patient name required")

    if not patient_phone:
        return failure("phone number required")

    if not doctor_name:
        return failure("doctor name required")

    if not appointment_date:
        return failure("appointment date required")

    if not slot:
        return failure("appointment slot required")

    phone_result = normalize_phone_number.invoke(
        {"phone": patient_phone}
    )

    if phone_result["status"] == "failed":
        return phone_result

    patient_phone = phone_result["data"]["phone"]

    patient_name = patient_name.strip().title()

    invalid_names = [
        "user",
        "patient",
        "unknown"
    ]

    if patient_name.lower() in invalid_names:
        return failure("valid patient name required")

    slot = slot.strip().upper()

    try:
        appointment_dt = datetime.strptime(
            appointment_date,
            "%Y-%m-%d"
        ).date()

        if appointment_dt < date.today():
            return failure(
                "appointments cannot be booked in the past"
            )

    except ValueError:
        return failure(
            "invalid appointment date"
        )

    db = SessionLocal()

    try:

        search_name = (
            doctor_name
            .replace("Dr.", "")
            .replace("Dr", "")
            .strip()
        )

        doctor = (
            db.query(Doctor)
            .filter(
                Doctor.name.ilike(
                    f"%{search_name}%"
                )
            )
            .first()
        )

        if not doctor:
            return failure("doctor not found")

        doctor_name = doctor.name

        duplicate = (
            db.query(Appointment)
            .filter(
                func.lower(Appointment.patient_name)
                == patient_name.lower(),
                Appointment.patient_phone == patient_phone,
                Appointment.doctor_name == doctor_name,
                Appointment.appointment_date == appointment_date,
                Appointment.slot == slot,
                Appointment.status == "BOOKED"
            )
            .first()
        )

        if duplicate:
            return failure(
                "appointment already exists"
            )

        availability = check_availability.invoke(
            {
                "doctor_name": doctor_name,
                "appointment_date": appointment_date,
                "slot": slot
            }
        )

        if availability["status"] == "failed":
            return availability

        if not availability["data"]["available"]:
            return failure(
                "requested slot is unavailable"
            )

        appointment = Appointment(
            patient_name=patient_name,
            patient_phone=patient_phone,
            doctor_name=doctor_name,
            appointment_date=appointment_date,
            slot=slot,
            status="BOOKED"
        )

        db.add(appointment)
        db.commit()

        return success(
            "appointment booked successfully",
            {
                "patient": patient_name,
                "doctor": doctor_name,
                "date": appointment_date,
                "slot": slot,
                "status": "BOOKED"
            }
        )

    finally:
        db.close()


@tool
def cancel_patient_appointment(
    patient_name: str,
    patient_phone: str,
    doctor_name: str,
    appointment_date: str,
    slot: str
):
    """
    Cancel exactly one appointment.
    """

    if not patient_name:
        return failure("patient name required")

    if not patient_phone:
        return failure("phone number required")

    if not doctor_name:
        return failure("doctor name required")

    if not appointment_date:
        return failure("appointment date required")

    if not slot:
        return failure("appointment slot required")

    phone_result = normalize_phone_number.invoke(
        {"phone": patient_phone}
    )

    if phone_result["status"] == "failed":
        return phone_result

    patient_phone = phone_result["data"]["phone"]

    patient_name = patient_name.strip().title()

    db = SessionLocal()

    try:

        appointment = (
            db.query(Appointment)
            .filter(
                func.lower(Appointment.patient_name)
                == patient_name.lower(),
                Appointment.patient_phone == patient_phone,
                Appointment.doctor_name == doctor_name,
                Appointment.appointment_date == appointment_date,
                Appointment.slot == slot,
                Appointment.status == "BOOKED"
            )
            .first()
        )

        if not appointment:
            return failure(
                "appointment not found"
            )

        appointment.status = "CANCELLED"

        db.commit()

        return success(
            "appointment cancelled successfully",
            {
                "doctor": doctor_name,
                "date": appointment_date,
                "slot": slot,
                "status": "CANCELLED"
            }
        )

    finally:
        db.close()


@tool
def reschedule_patient_appointment(
    patient_name: str,
    patient_phone: str,
    doctor_name: str,
    old_date: str,
    old_slot: str,
    new_date: str,
    new_slot: str
):
    """
    Reschedule exactly one appointment.
    """

    required = [
        patient_name,
        patient_phone,
        doctor_name,
        old_date,
        old_slot,
        new_date,
        new_slot
    ]

    if not all(required):
        return failure(
            "all appointment details are required"
        )

    phone_result = normalize_phone_number.invoke(
        {"phone": patient_phone}
    )

    if phone_result["status"] == "failed":
        return phone_result

    patient_phone = phone_result["data"]["phone"]

    patient_name = patient_name.strip().title()

    try:
        new_dt = datetime.strptime(
            new_date,
            "%Y-%m-%d"
        ).date()

        if new_dt < date.today():
            return failure(
                "cannot reschedule to a past date"
            )

    except ValueError:
        return failure(
            "invalid new appointment date"
        )

    new_slot = new_slot.strip().upper()

    db = SessionLocal()

    try:

        appointment = (
            db.query(Appointment)
            .filter(
                func.lower(Appointment.patient_name)
                == patient_name.lower(),
                Appointment.patient_phone == patient_phone,
                Appointment.doctor_name == doctor_name,
                Appointment.appointment_date == old_date,
                Appointment.slot == old_slot,
                Appointment.status == "BOOKED"
            )
            .first()
        )

        if not appointment:
            return failure(
                "appointment not found"
            )

        if (
            appointment.appointment_date == new_date
            and appointment.slot == new_slot
        ):
            return failure(
                "appointment already scheduled at this time"
            )

        availability = check_availability.invoke(
            {
                "doctor_name": doctor_name,
                "appointment_date": new_date,
                "slot": new_slot
            }
        )

        if availability["status"] == "failed":
            return availability

        if not availability["data"]["available"]:
            return failure(
                "requested slot unavailable"
            )

        appointment.appointment_date = new_date
        appointment.slot = new_slot

        db.commit()

        return success(
            "appointment rescheduled successfully",
            {
                "doctor": doctor_name,
                "old_date": old_date,
                "old_slot": old_slot,
                "new_date": new_date,
                "new_slot": new_slot
            }
        )

    finally:
        db.close()