from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


# =========================
# AI Profile Models
# =========================

class AIProfileCreate(BaseModel):
    name: str
    language: str = "French"
    note_format: str = "SOAP"
    model: str = "gpt-4.1-mini"
    temperature: int = 0
    prompt: str


class AIProfileUpdate(BaseModel):
    name: str | None = None
    language: str | None = None
    note_format: str | None = None
    model: str | None = None
    temperature: int | None = None
    prompt: str | None = None


class AIProfile(BaseModel):
    id: UUID
    name: str
    language: str
    note_format: str
    model: str
    temperature: int
    prompt: str


class AIProfileTestRequest(BaseModel):
    prompt: str
    model: str = "gpt-4.1-mini"
    transcript: str


class AIProfileTestResponse(BaseModel):
    antecedents: str = ""
    chief_complaint: str
    history_of_present_illness: str
    assessment: str
    plan: str


# =========================
# Doctor Models
# =========================

class DoctorCreate(BaseModel):
    username: str
    password: str
    full_name: str
    role: str = "doctor"
    ai_profile_id: UUID | None = None


class DoctorUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    full_name: str | None = None
    role: str | None = None
    ai_profile_id: UUID | None = None


class DoctorAIProfileUpdate(BaseModel):
    ai_profile_id: UUID | None = None


class Doctor(BaseModel):
    id: UUID
    username: str
    full_name: str
    role: str
    ai_profile_id: UUID | None = None


class DoctorLoginResponse(BaseModel):
    id: UUID
    username: str
    full_name: str
    role: str
    ai_profile_id: UUID | None = None


# =========================
# Patient Models
# =========================

class PatientCreate(BaseModel):
    record_number: str | None = None
    full_name: str
    age: int | None = None
    notes: str | None = None


class PatientUpdate(BaseModel):
    record_number: str | None = None
    full_name: str | None = None
    age: int | None = None
    notes: str | None = None


class Patient(BaseModel):
    id: UUID
    record_number: str | None = None
    full_name: str
    age: int | None = None
    notes: str | None = None

    class Config:
        from_attributes = True


# =========================
# Consultation Models
# =========================

class ConsultationCreate(BaseModel):
    patient_id: UUID
    transcript: str


class Consultation(BaseModel):
    id: UUID
    patient_id: UUID
    transcript: str
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# Medical Note Models
# =========================

class GenerateNoteRequest(BaseModel):
    consultation_id: UUID


class MedicalNoteUpdateRequest(BaseModel):
    antecedents: str = ""
    chief_complaint: str
    history_of_present_illness: str
    assessment: str
    plan: str


class MedicalNote(BaseModel):
    id: UUID | None = None
    consultation_id: UUID

    antecedents: str = ""
    chief_complaint: str
    history_of_present_illness: str
    assessment: str
    plan: str

    generated_at: datetime

    class Config:
        from_attributes = True


# =========================
# Authentication Models
# =========================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None