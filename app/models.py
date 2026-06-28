from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class AIProfileDB(Base):
    __tablename__ = "ai_profiles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    language = Column(String, nullable=False, default="French")
    note_format = Column(String, nullable=False, default="SOAP")
    model = Column(String, nullable=False, default="gpt-4.1-mini")
    temperature = Column(Integer, nullable=False, default=0)
    prompt = Column(Text, nullable=False)


class DoctorDB(Base):
    __tablename__ = "doctors"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="doctor")

    ai_profile_id = Column(
        String,
        ForeignKey("ai_profiles.id"),
        nullable=True
    )

    ai_profile = relationship("AIProfileDB")

    patients = relationship(
        "PatientDB",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )


class PatientDB(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True)

    doctor_id = Column(
        String,
        ForeignKey("doctors.id"),
        nullable=False
    )

    full_name = Column(String, nullable=False)
    record_number = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    doctor = relationship(
        "DoctorDB",
        back_populates="patients"
    )

    consultations = relationship(
        "ConsultationDB",
        back_populates="patient",
        cascade="all, delete-orphan"
    )

    documents = relationship(
        "MedicalDocumentDB",
        back_populates="patient",
        cascade="all, delete-orphan"
    )


class ConsultationDB(Base):
    __tablename__ = "consultations"

    id = Column(String, primary_key=True, index=True)

    patient_id = Column(
        String,
        ForeignKey("patients.id"),
        nullable=False
    )

    transcript = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship(
        "PatientDB",
        back_populates="consultations"
    )

    medical_notes = relationship(
        "MedicalNoteDB",
        back_populates="consultation",
        cascade="all, delete-orphan"
    )

    documents = relationship(
        "MedicalDocumentDB",
        back_populates="consultation",
        cascade="all, delete-orphan"
    )


class MedicalNoteDB(Base):
    __tablename__ = "medical_notes"

    id = Column(String, primary_key=True, index=True)

    consultation_id = Column(
        String,
        ForeignKey("consultations.id"),
        nullable=False
    )

    chief_complaint = Column(Text, nullable=False)
    history_of_present_illness = Column(Text, nullable=False)
    assessment = Column(Text, nullable=False)
    plan = Column(Text, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)

    consultation = relationship(
        "ConsultationDB",
        back_populates="medical_notes"
    )


class MedicalDocumentDB(Base):
    __tablename__ = "medical_documents"

    id = Column(String, primary_key=True, index=True)

    patient_id = Column(
        String,
        ForeignKey("patients.id"),
        nullable=False
    )

    consultation_id = Column(
        String,
        ForeignKey("consultations.id"),
        nullable=False
    )

    document_type = Column(
        String,
        nullable=False,
        default="analysis"
    )

    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    mime_type = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship(
        "PatientDB",
        back_populates="documents"
    )

    consultation = relationship(
        "ConsultationDB",
        back_populates="documents"
    )