from fastapi import FastAPI

from app.chat_api import router as chat_router

from app.database import engine
from app.models import Base
from scripts.load_doctors import load_doctors

Base.metadata.create_all(bind=engine)

load_doctors()

app = FastAPI(
    title="2Care Voice AI",
    description="DeepAgents Hospital Receptionist",
    version="1.0.0"
)

app.include_router(chat_router)


@app.get("/")
def home():
    return {
        "message": "2Care Voice AI Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/debug-count")
def debug_count():

    from app.database import SessionLocal
    from app.models import Doctor, Appointment

    db = SessionLocal()

    result = {
        "doctors": db.query(Doctor).count(),
        "appointments": db.query(Appointment).count()
    }

    db.close()

    return result


@app.get("/debug-appointments")
def debug_appointments():

    from app.database import SessionLocal
    from app.models import Appointment

    db = SessionLocal()

    appointments = db.query(Appointment).all()

    result = []

    for a in appointments:
        result.append(
            {
                "id": a.id,
                "patient_name": a.patient_name,
                "patient_phone": a.patient_phone,
                "doctor": a.doctor_name,
                "date": a.appointment_date,
                "slot": a.slot,
                "status": a.status
            }
        )

    db.close()

    return result