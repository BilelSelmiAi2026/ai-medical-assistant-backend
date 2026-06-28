from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import PatientDB
from app.schemas import PatientCreate, PatientUpdate


def create_patient(
    db: Session,
    patient_data: PatientCreate,
    doctor_id: str
):
    patient = PatientDB(
        id=str(uuid4()),
        doctor_id=doctor_id,
        record_number=patient_data.record_number,
        full_name=patient_data.full_name,
        age=patient_data.age,
        notes=patient_data.notes,
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


def get_patients(
    db: Session,
    doctor_id: str
):
    return db.query(PatientDB).filter(
        PatientDB.doctor_id == doctor_id
    ).all()


def get_patient(
    db: Session,
    patient_id: str,
    doctor_id: str
):
    return db.query(PatientDB).filter(
        PatientDB.id == patient_id,
        PatientDB.doctor_id == doctor_id
    ).first()


def update_patient(
    db: Session,
    patient_id: str,
    patient_data: PatientUpdate,
    doctor_id: str
):
    patient = get_patient(
        db,
        patient_id,
        doctor_id
    )

    if patient is None:
        return None

    update_data = patient_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)

    return patient


def delete_patient(
    db: Session,
    patient_id: str,
    doctor_id: str
):
    patient = get_patient(
        db,
        patient_id,
        doctor_id
    )

    if patient is None:
        return None

    db.delete(patient)
    db.commit()

    return patient