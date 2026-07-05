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

DEFAULT_ANTECEDENTS = (
    "Aucun antécédent médical ou chirurgical rapporté."
)

DEFAULT_PROMPT = """
You are an experienced medical scribe.

Analyze the consultation transcript and generate a professional medical note.

Language rules:
- The consultation transcript may be in Arabic, Tunisian Arabic, French, German, or English.
- Generate the medical note ONLY in French.
- Translate the medical information into professional medical French.
- Never generate the note in Arabic.

Medical note structure:
- Antécédents
- Motif principal
- Histoire de la maladie actuelle
- Évaluation
- CAT : Conduite à tenir

Output rules:
- Return ONLY valid JSON.
- Do NOT use markdown.
- Do NOT wrap the response in ```json blocks.
- Populate all fields.
- If no antecedents are mentioned, write:
  "Aucun antécédent médical ou chirurgical rapporté."

Required JSON structure:

{
  "antecedents": "",
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
            "antecedents": DEFAULT_ANTECEDENTS,
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
        antecedents=data.get(
            "antecedents",
            DEFAULT_ANTECEDENTS
        ),
        chief_complaint=data.get(
            "chief_complaint",
            "Not provided"
        ),
        history_of_present_illness=data.get(
            "history_of_present_illness",
            "Not provided"
        ),
        assessment=data.get(
            "assessment",
            "Not provided"
        ),
        plan=data.get(
            "plan",
            "Not provided"
        ),
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
        "antecedents": data.get(
            "antecedents",
            DEFAULT_ANTECEDENTS
        ),
        "chief_complaint": data.get(
            "chief_complaint",
            "Not provided"
        ),
        "history_of_present_illness": data.get(
            "history_of_present_illness",
            "Not provided"
        ),
        "assessment": data.get(
            "assessment",
            "Not provided"
        ),
        "plan": data.get(
            "plan",
            "Not provided"
        )
    }