import os
import tempfile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from openai import OpenAI

from app.auth.security import get_current_doctor

router = APIRouter(
    prefix="/transcriptions",
    tags=["Transcriptions"]
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


@router.post("/whisper")
async def transcribe_audio(
    file: UploadFile = File(...),
    current_doctor=Depends(get_current_doctor)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No audio file uploaded"
        )

    suffix = os.path.splitext(file.filename)[1] or ".m4a"

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:
        with open(temp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        return {
            "text": transcription.text
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)