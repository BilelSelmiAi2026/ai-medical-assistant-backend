from uuid import uuid4

from sqlalchemy.orm import Session

from app.auth.security import hash_password
from app.models import DoctorDB
from app.schemas import DoctorCreate, DoctorUpdate


def create_doctor(
    db: Session,
    doctor_data: DoctorCreate
):
    doctor = DoctorDB(
        id=str(uuid4()),
        username=doctor_data.username,
        hashed_password=hash_password(
            doctor_data.password
        ),
        full_name=doctor_data.full_name,
        role=doctor_data.role,
        ai_profile_id=(
            str(doctor_data.ai_profile_id)
            if doctor_data.ai_profile_id
            else None
        )
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor


def get_doctors(db: Session):
    return db.query(DoctorDB).all()


def get_doctor(
    db: Session,
    doctor_id: str
):
    return db.query(DoctorDB).filter(
        DoctorDB.id == doctor_id
    ).first()


def get_doctor_by_username(
    db: Session,
    username: str
):
    return db.query(DoctorDB).filter(
        DoctorDB.username == username
    ).first()


def update_doctor(
    db: Session,
    doctor_id: str,
    doctor_data: DoctorUpdate
):
    doctor = get_doctor(
        db,
        doctor_id
    )

    if doctor is None:
        return None

    if doctor_data.username is not None:
        doctor.username = doctor_data.username

    if doctor_data.full_name is not None:
        doctor.full_name = doctor_data.full_name

    if doctor_data.password is not None:
        doctor.hashed_password = hash_password(
            doctor_data.password
        )

    if doctor_data.role is not None:
        doctor.role = doctor_data.role

    if doctor_data.ai_profile_id is not None:
        doctor.ai_profile_id = str(
            doctor_data.ai_profile_id
        )

    db.commit()
    db.refresh(doctor)

    return doctor


def update_doctor_ai_profile(
    db: Session,
    doctor_id: str,
    ai_profile_id: str | None
):
    doctor = get_doctor(
        db,
        doctor_id
    )

    if doctor is None:
        return None

    doctor.ai_profile_id = ai_profile_id

    db.commit()
    db.refresh(doctor)

    return doctor


def delete_doctor(
    db: Session,
    doctor_id: str
):
    doctor = get_doctor(
        db,
        doctor_id
    )

    if doctor is None:
        return False

    db.delete(doctor)
    db.commit()

    return True