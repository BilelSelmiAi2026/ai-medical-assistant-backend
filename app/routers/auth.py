from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.auth_service import authenticate_doctor
from app.auth.security import create_access_token, get_current_doctor
from app.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    doctor = authenticate_doctor(
        db,
        form_data.username,
        form_data.password
    )

    if doctor is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        username=doctor.username
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "doctor": {
            "id": doctor.id,
            "username": doctor.username,
            "full_name": doctor.full_name,
            "role": doctor.role
        }
    }


@router.get("/me")
def get_me(
    current_doctor=Depends(get_current_doctor)
):
    return {
        "id": current_doctor.id,
        "username": current_doctor.username,
        "full_name": current_doctor.full_name,
        "role": current_doctor.role
    }