from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import ConsultationDB, PatientDB
from app.schemas import ConsultationCreate


def create_consultation(
    db: Session,
    consultation_data: ConsultationCreate,
    doctor_id: str
):
    patient = db.query(PatientDB).filter(
        PatientDB.id == str(consultation_data.patient_id),
        PatientDB.doctor_id == doctor_id
    ).first()

    if patient is None:
        return None

    consultation = ConsultationDB(
        id=str(uuid4()),
        patient_id=str(consultation_data.patient_id),
        transcript=consultation_data.transcript,
        created_at=datetime.utcnow()
    )

    db.add(consultation)
    db.commit()
    db.refresh(consultation)

    return consultation


def get_consultations(
    db: Session,
    doctor_id: str
):
    return (
        db.query(ConsultationDB)
        .join(PatientDB)
        .filter(PatientDB.doctor_id == doctor_id)
        .all()
    )


def get_consultation(
    db: Session,
    consultation_id: str,
    doctor_id: str
):
    return (
        db.query(ConsultationDB)
        .join(PatientDB)
        .filter(
            ConsultationDB.id == consultation_id,
            PatientDB.doctor_id == doctor_id
        )
        .first()
    )


def get_consultations_by_patient(
    db: Session,
    patient_id: str,
    doctor_id: str
):
    return db.query(ConsultationDB).filter(
        ConsultationDB.patient_id == patient_id,
        PatientDB.id == patient_id,
        PatientDB.doctor_id == doctor_id
    ).all()