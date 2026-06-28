from uuid import uuid4

from app.auth.security import hash_password
from app.database import SessionLocal
from app.models import DoctorDB


db = SessionLocal()

existing_doctor = db.query(DoctorDB).filter(
    DoctorDB.username == "doctor"
).first()

if existing_doctor:
    print("Doctor already exists")
else:
    doctor = DoctorDB(
        id=str(uuid4()),
        username="doctor",
        full_name="Default Doctor",
        hashed_password=hash_password("Doctor123!")
    )

    db.add(doctor)
    db.commit()

    print("Doctor created successfully")
    print("Username: doctor")
    print("Password: Doctor123!")

db.close()