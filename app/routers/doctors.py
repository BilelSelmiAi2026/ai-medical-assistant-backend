from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import get_current_admin_doctor
from app.database import get_db
from app.crud import doctor_crud
from app.schemas import (
    Doctor,
    DoctorCreate,
    DoctorUpdate,
    DoctorAIProfileUpdate
)

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.post("", response_model=Doctor)
def create_doctor(
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_admin_doctor)
):
    existing_doctor = doctor_crud.get_doctor_by_username(
        db,
        doctor_data.username
    )

    if existing_doctor is not None:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    return doctor_crud.create_doctor(
        db,
        doctor_data
    )


@router.get("", response_model=list[Doctor])
def get_doctors(
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_admin_doctor)
):
    return doctor_crud.get_doctors(db)


@router.get("/{doctor_id}", response_model=Doctor)
def get_doctor(
    doctor_id: UUID,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_admin_doctor)
):
    doctor = doctor_crud.get_doctor(
        db,
        str(doctor_id)
    )

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.put("/{doctor_id}", response_model=Doctor)
def update_doctor(
    doctor_id: UUID,
    doctor_data: DoctorUpdate,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_admin_doctor)
):
    doctor = doctor_crud.update_doctor(
        db,
        str(doctor_id),
        doctor_data
    )

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.put("/{doctor_id}/ai-profile", response_model=Doctor)
def update_doctor_ai_profile(
    doctor_id: UUID,
    request: DoctorAIProfileUpdate,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_admin_doctor)
):
    doctor = doctor_crud.update_doctor_ai_profile(
        db,
        str(doctor_id),
        str(request.ai_profile_id) if request.ai_profile_id else None
    )

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: UUID,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_admin_doctor)
):
    deleted = doctor_crud.delete_doctor(
        db,
        str(doctor_id)
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return {
        "message": "Doctor deleted successfully"
    }