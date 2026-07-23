import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from deepagents import create_deep_agent

from pathlib import Path


from tools.appointment_tools import (
    get_current_date,
    get_doctors_by_speciality,
    get_doctors,
    get_doctor,
    get_available_slots,
    check_availability,
    book_appointment,
    normalize_phone_number,
    cancel_patient_appointment,
    reschedule_patient_appointment,
    get_patient_appointments,
    get_appointment_history
)

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)


SYSTEM_PROMPT = Path("AGENTS.md").read_text()

agent = create_deep_agent(
    model=llm,

    system_prompt=SYSTEM_PROMPT,

    skills=[
        Path("skills/booking.md").read_text(),
        Path("skills/cancellation.md").read_text(),
        Path("skills/reschedule.md").read_text(),
        Path("skills/doctor_lookup.md").read_text(),
        Path("skills/date_reasoning.md").read_text(),
        Path("skills/emergency.md").read_text(),
        Path("skills/appointment_lookup.md").read_text()
    ],

    tools=[
        get_current_date,
        get_doctors_by_speciality,
        get_doctors,
        get_doctor,
        get_available_slots,
        check_availability,
        book_appointment,
        normalize_phone_number,
        cancel_patient_appointment,
        reschedule_patient_appointment,
        get_patient_appointments,
        get_appointment_history
    ],

    debug=False
)