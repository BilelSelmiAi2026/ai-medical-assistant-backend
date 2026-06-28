from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import MedicalDocumentDB

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path("uploads/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_document(
    patient_id: str = Form(...),
    consultation_id: str = Form(...),
    document_type: str = Form("analysis"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    document_id = str(uuid4())

    file_extension = Path(file.filename or "").suffix or ".jpg"
    file_name = f"{document_id}{file_extension}"
    file_path = UPLOAD_DIR / file_name

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    document = MedicalDocumentDB(
        id=document_id,
        patient_id=patient_id,
        consultation_id=consultation_id,
        document_type=document_type,
        file_name=file_name,
        file_path=str(file_path),
        mime_type=file.content_type
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "id": document.id,
        "message": "Document uploaded successfully",
        "patient_id": document.patient_id,
        "consultation_id": document.consultation_id,
        "document_type": document.document_type,
        "file_name": document.file_name,
        "file_path": document.file_path,
        "mime_type": document.mime_type,
        "uploaded_at": document.uploaded_at
    }

@router.get("/consultation/{consultation_id}")
def get_documents_for_consultation(
    consultation_id: str,
    db: Session = Depends(get_db)
):
    documents = (
        db.query(MedicalDocumentDB)
        .filter(MedicalDocumentDB.consultation_id == consultation_id)
        .order_by(MedicalDocumentDB.uploaded_at.desc())
        .all()
    )

    return documents