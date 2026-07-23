from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    qualification = Column(String)

    speciality = Column(String)

    experience = Column(String)

    languages = Column(String)

    location = Column(String)

    opd_timings = Column(String)

    expertise = Column(Text)

    services = Column(Text)

    profile_url = Column(String)

    hospital = Column(String)


class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)

    patient_name = Column(String)

    patient_phone = Column(String)

    doctor_name = Column(String)

    appointment_date = Column(String)

    slot = Column(String)

    status = Column(String)