import json
import os
from datetime import datetime
from uuid import UUID

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas import MedicalNote

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

DEFAULT_MODEL = "gpt-4.1-mini"

DEFAULT_PROMPT = """
You are an experienced medical scribe.

Analyze the consultation transcript and generate a professional SOAP-style medical note.

Language rules:
- The consultation transcript may be in Arabic, Tunisian Arabic, French, German, or English.
- Generate the medical note ONLY in French.
- Translate the medical information into professional medical French.
- Never generate the note in Arabic.

Output rules:
- Return ONLY valid JSON.
- Do NOT use markdown.
- Do NOT wrap the response in ```json blocks.
- Populate all fields.
- If information is missing, explicitly state that the information was not mentioned.

Required JSON structure:

{
  "chief_complaint": "",
  "history_of_present_illness": "",
  "assessment": "",
  "plan": ""
}
"""


def _generate_note_data(
    prompt: str,
    model: str,
    transcript: str
) -> dict:
    response = client.responses.create(
        model=model,
        input=f"""
{prompt}

Consultation Transcript:

{transcript}
"""
    )

    raw_text = response.output_text.strip()

    raw_text = (
        raw_text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        return json.loads(raw_text)

    except Exception:
        return {
            "chief_complaint": "Unable to parse AI response",
            "history_of_present_illness": raw_text,
            "assessment": "Parsing failed",
            "plan": "Review AI output manually"
        }


def generate_note_from_transcript(
    consultation_id: UUID,
    transcript: str,
    ai_profile=None
) -> MedicalNote:

    model = DEFAULT_MODEL
    prompt = DEFAULT_PROMPT

    if ai_profile is not None:
        if ai_profile.model:
            model = ai_profile.model

        if ai_profile.prompt:
            prompt = ai_profile.prompt

    data = _generate_note_data(
        prompt=prompt,
        model=model,
        transcript=transcript
    )

    return MedicalNote(
        consultation_id=consultation_id,
        chief_complaint=data.get("chief_complaint", "Not provided"),
        history_of_present_illness=data.get(
            "history_of_present_illness",
            "Not provided"
        ),
        assessment=data.get("assessment", "Not provided"),
        plan=data.get("plan", "Not provided"),
        generated_at=datetime.utcnow()
    )


def test_prompt(
    prompt: str,
    model: str,
    transcript: str
):
    data = _generate_note_data(
        prompt=prompt,
        model=model,
        transcript=transcript
    )

    return {
        "chief_complaint": data.get("chief_complaint", "Not provided"),
        "history_of_present_illness": data.get(
            "history_of_present_illness",
            "Not provided"
        ),
        "assessment": data.get("assessment", "Not provided"),
        "plan": data.get("plan", "Not provided")
    }