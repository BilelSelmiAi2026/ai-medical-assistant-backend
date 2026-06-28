from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.security import get_current_admin_doctor
from app.database import get_db
from app.models import DoctorDB, PatientDB, ConsultationDB, MedicalNoteDB

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_admin_doctor)
):
    return {
        "doctors": db.query(DoctorDB).count(),
        "patients": db.query(PatientDB).count(),
        "consultations": db.query(ConsultationDB).count(),
        "medical_notes": db.query(MedicalNoteDB).count()
    }