from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import ConsultationDB, DoctorDB, MedicalNoteDB, PatientDB
from app.schemas import GenerateNoteRequest, MedicalNoteUpdateRequest
from app.services.ai_note_service import generate_note_from_transcript


def generate_medical_note(
    db: Session,
    request: GenerateNoteRequest,
    doctor_id: str
):
    consultation = (
        db.query(ConsultationDB)
        .join(PatientDB)
        .filter(
            ConsultationDB.id == str(request.consultation_id),
            PatientDB.doctor_id == doctor_id
        )
        .first()
    )

    if consultation is None:
        return None

    doctor = db.query(DoctorDB).filter(
        DoctorDB.id == doctor_id
    ).first()

    ai_profile = doctor.ai_profile if doctor else None

    generated_note = generate_note_from_transcript(
        consultation_id=consultation.id,
        transcript=consultation.transcript,
        ai_profile=ai_profile
    )

    note = (
        db.query(MedicalNoteDB)
        .filter(
            MedicalNoteDB.consultation_id == str(consultation.id)
        )
        .first()
    )

    if note is None:
        note = MedicalNoteDB(
            id=str(uuid4()),
            consultation_id=str(consultation.id)
        )
        db.add(note)

    note.antecedents = generated_note.antecedents
    note.chief_complaint = generated_note.chief_complaint
    note.history_of_present_illness = generated_note.history_of_present_illness
    note.assessment = generated_note.assessment
    note.plan = generated_note.plan
    note.generated_at = generated_note.generated_at

    db.commit()
    db.refresh(note)

    return note


def get_medical_notes(
    db: Session,
    doctor_id: str
):
    return (
        db.query(MedicalNoteDB)
        .join(ConsultationDB)
        .join(PatientDB)
        .filter(PatientDB.doctor_id == doctor_id)
        .all()
    )


def get_medical_note(
    db: Session,
    note_id: str,
    doctor_id: str
):
    return (
        db.query(MedicalNoteDB)
        .join(ConsultationDB)
        .join(PatientDB)
        .filter(
            MedicalNoteDB.id == note_id,
            PatientDB.doctor_id == doctor_id
        )
        .first()
    )


def get_medical_notes_by_consultation(
    db: Session,
    consultation_id: str,
    doctor_id: str
):
    return (
        db.query(MedicalNoteDB)
        .join(ConsultationDB)
        .join(PatientDB)
        .filter(
            MedicalNoteDB.consultation_id == consultation_id,
            PatientDB.doctor_id == doctor_id
        )
        .all()
    )


def update_medical_note(
    db: Session,
    note_id: str,
    request: MedicalNoteUpdateRequest,
    doctor_id: str
):
    note = get_medical_note(
        db,
        note_id,
        doctor_id
    )

    if note is None:
        return None

    note.antecedents = request.antecedents
    note.chief_complaint = request.chief_complaint
    note.history_of_present_illness = request.history_of_present_illness
    note.assessment = request.assessment
    note.plan = request.plan

    db.commit()
    db.refresh(note)

    return note


def delete_medical_note(
    db: Session,
    note_id: str,
    doctor_id: str
):
    note = get_medical_note(
        db,
        note_id,
        doctor_id
    )

    if note is None:
        return False

    db.delete(note)
    db.commit()

    return True