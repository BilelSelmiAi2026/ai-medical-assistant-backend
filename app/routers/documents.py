from pathlib import Path
from uuid import UUID, uuid4

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import get_current_doctor
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
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
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
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    documents = (
        db.query(MedicalDocumentDB)
        .filter(MedicalDocumentDB.consultation_id == consultation_id)
        .order_by(MedicalDocumentDB.uploaded_at.desc())
        .all()
    )

    return documents


@router.delete("/{document_id}")
def delete_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    document = db.query(MedicalDocumentDB).filter(
        MedicalDocumentDB.id == str(document_id)
    ).first()

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    file_path = Path(document.file_path)

    if file_path.exists():
        file_path.unlink()

    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully"
    }