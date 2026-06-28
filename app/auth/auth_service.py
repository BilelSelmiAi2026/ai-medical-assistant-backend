from sqlalchemy.orm import Session

from app.auth.security import verify_password
from app.models import DoctorDB


def authenticate_doctor(
    db: Session,
    username: str,
    password: str
):
    doctor = db.query(DoctorDB).filter(
        DoctorDB.username == username
    ).first()

    if doctor is None:
        return None

    if not verify_password(password, doctor.hashed_password):
        return None

    return doctor