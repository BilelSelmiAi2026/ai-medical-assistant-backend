from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import AIProfileDB
from app.schemas import AIProfileCreate, AIProfileUpdate


def create_ai_profile(
    db: Session,
    profile_data: AIProfileCreate
):
    profile = AIProfileDB(
        id=str(uuid4()),
        name=profile_data.name,
        language=profile_data.language,
        note_format=profile_data.note_format,
        model=profile_data.model,
        temperature=profile_data.temperature,
        prompt=profile_data.prompt
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def get_ai_profiles(db: Session):
    return db.query(AIProfileDB).all()


def get_ai_profile(
    db: Session,
    profile_id: str
):
    return db.query(AIProfileDB).filter(
        AIProfileDB.id == profile_id
    ).first()


def update_ai_profile(
    db: Session,
    profile_id: str,
    profile_data: AIProfileUpdate
):
    profile = get_ai_profile(db, profile_id)

    if profile is None:
        return None

    update_data = profile_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return profile


def delete_ai_profile(
    db: Session,
    profile_id: str
):
    profile = get_ai_profile(db, profile_id)

    if profile is None:
        return False

    db.delete(profile)
    db.commit()

    return True