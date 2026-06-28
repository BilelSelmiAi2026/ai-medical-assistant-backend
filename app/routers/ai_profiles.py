from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.auth.security import get_current_admin_doctor
from app.database import get_db
from app.crud import ai_profile_crud
from app.schemas import (
    AIProfile,
    AIProfileCreate,
    AIProfileUpdate,
    AIProfileTestRequest,
    AIProfileTestResponse
)
from app.services.ai_note_service import test_prompt

router = APIRouter(
    prefix="/ai-profiles",
    tags=["AI Profiles"]
)


@router.post("", response_model=AIProfile)
def create_ai_profile(
    profile_data: AIProfileCreate,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_admin_doctor)
):
    return ai_profile_crud.create_ai_profile(db, profile_data)


@router.get("", response_model=list[AIProfile])
def get_ai_profiles(
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_admin_doctor)
):
    return ai_profile_crud.get_ai_profiles(db)


@router.post("/test", response_model=AIProfileTestResponse)
def test_ai_profile(
    request: AIProfileTestRequest,
    current_doctor=Depends(get_current_admin_doctor)
):
    return test_prompt(
        prompt=request.prompt,
        model=request.model,
        transcript=request.transcript
    )


@router.get("/{profile_id}", response_model=AIProfile)
def get_ai_profile(
    profile_id: UUID,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_admin_doctor)
):
    profile = ai_profile_crud.get_ai_profile(db, str(profile_id))

    if profile is None:
        raise HTTPException(status_code=404, detail="AI profile not found")

    return profile


@router.put("/{profile_id}", response_model=AIProfile)
def update_ai_profile(
    profile_id: UUID,
    profile_data: AIProfileUpdate,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_admin_doctor)
):
    profile = ai_profile_crud.update_ai_profile(
        db,
        str(profile_id),
        profile_data
    )

    if profile is None:
        raise HTTPException(status_code=404, detail="AI profile not found")

    return profile


@router.delete("/{profile_id}")
def delete_ai_profile(
    profile_id: UUID,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_admin_doctor)
):
    deleted = ai_profile_crud.delete_ai_profile(db, str(profile_id))

    if not deleted:
        raise HTTPException(status_code=404, detail="AI profile not found")

    return {"message": "AI profile deleted successfully"}