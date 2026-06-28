from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.auth.security import get_current_doctor
from app.database import get_db
from app.crud import patient_crud
from app.schemas import Patient, PatientCreate, PatientUpdate

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("", response_model=Patient)
def create_patient(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    return patient_crud.create_patient(
        db,
        patient_data,
        current_doctor.id
    )


@router.get("", response_model=list[Patient])
def get_patients(
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    return patient_crud.get_patients(
        db,
        current_doctor.id
    )


@router.get("/{patient_id}", response_model=Patient)
def get_patient(
    patient_id: UUID,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    patient = patient_crud.get_patient(
        db,
        str(patient_id),
        current_doctor.id
    )

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient


@router.put("/{patient_id}", response_model=Patient)
def update_patient(
    patient_id: UUID,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    patient = patient_crud.update_patient(
        db,
        str(patient_id),
        patient_data,
        current_doctor.id
    )

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: UUID,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    patient = patient_crud.delete_patient(
        db,
        str(patient_id),
        current_doctor.id
    )

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {"message": "Patient deleted successfully"}