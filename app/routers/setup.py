from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import hash_password
from app.database import get_db
from app.models import DoctorDB

router = APIRouter(prefix="/setup", tags=["Setup"])


@router.post("/create-default-doctor")
def create_default_doctor(
    db: Session = Depends(get_db)
):
    existing_doctor = db.query(DoctorDB).filter(
        DoctorDB.username == "doctor"
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=400,
            detail="Default doctor already exists"
        )

    doctor = DoctorDB(
        id=str(uuid4()),
        username="doctor",
        hashed_password=hash_password("doctor123"),
        full_name="Default Doctor",
        role="doctor"
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return {
        "message": "Default doctor created",
        "username": doctor.username
    }