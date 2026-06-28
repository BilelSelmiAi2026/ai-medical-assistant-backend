from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.auth.security import get_current_doctor
from app.database import get_db
from app.crud import medical_note_crud
from app.schemas import GenerateNoteRequest, MedicalNote, MedicalNoteUpdateRequest

router = APIRouter(
    prefix="/medical-notes",
    tags=["Medical Notes"]
)


@router.post("/generate", response_model=MedicalNote)
def generate_medical_note(
    request: GenerateNoteRequest,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    note = medical_note_crud.generate_medical_note(
        db,
        request,
        current_doctor.id
    )

    if note is None:
        raise HTTPException(status_code=404, detail="Consultation not found")

    return note


@router.get("", response_model=list[MedicalNote])
def get_medical_notes(
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    return medical_note_crud.get_medical_notes(
        db,
        current_doctor.id
    )


@router.get("/consultation/{consultation_id}", response_model=list[MedicalNote])
def get_medical_notes_by_consultation(
    consultation_id: UUID,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    return medical_note_crud.get_medical_notes_by_consultation(
        db,
        str(consultation_id),
        current_doctor.id
    )


@router.get("/{note_id}", response_model=MedicalNote)
def get_medical_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    note = medical_note_crud.get_medical_note(
        db,
        str(note_id),
        current_doctor.id
    )

    if note is None:
        raise HTTPException(status_code=404, detail="Medical note not found")

    return note


@router.put("/{note_id}", response_model=MedicalNote)
def update_medical_note(
    note_id: UUID,
    request: MedicalNoteUpdateRequest,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    note = medical_note_crud.update_medical_note(
        db,
        str(note_id),
        request,
        current_doctor.id
    )

    if note is None:
        raise HTTPException(status_code=404, detail="Medical note not found")

    return note


@router.delete("/{note_id}")
def delete_medical_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    deleted = medical_note_crud.delete_medical_note(
        db,
        str(note_id),
        current_doctor.id
    )

    if not deleted:
        raise HTTPException(status_code=404, detail="Medical note not found")

    return {
        "message": "Medical note deleted successfully"
    }