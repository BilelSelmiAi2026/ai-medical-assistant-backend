from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.auth.security import get_current_doctor
from app.database import get_db
from app.crud import consultation_crud
from app.schemas import Consultation, ConsultationCreate

router = APIRouter(
    prefix="/consultations",
    tags=["Consultations"]
)


@router.post("", response_model=Consultation)
def create_consultation(
    consultation_data: ConsultationCreate,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    consultation = consultation_crud.create_consultation(
        db,
        consultation_data,
        current_doctor.id
    )

    if consultation is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    return consultation


@router.get("", response_model=list[Consultation])
def get_consultations(
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    return consultation_crud.get_consultations(
        db,
        current_doctor.id
    )


@router.get("/patient/{patient_id}", response_model=list[Consultation])
def get_consultations_by_patient(
    patient_id: UUID,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    return consultation_crud.get_consultations_by_patient(
        db,
        str(patient_id),
        current_doctor.id
    )


@router.get("/{consultation_id}", response_model=Consultation)
def get_consultation(
    consultation_id: UUID,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    consultation = consultation_crud.get_consultation(
        db,
        str(consultation_id),
        current_doctor.id
    )

    if consultation is None:
        raise HTTPException(status_code=404, detail="Consultation not found")

    return consultation