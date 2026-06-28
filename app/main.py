from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine

from app.routers import auth
from app.routers import patients
from app.routers import consultations
from app.routers import medical_notes
from app.routers import transcriptions
from app.routers import doctors
from app.routers import admin
from app.routers import ai_profiles
from app.routers import documents
from app.routers import setup

app = FastAPI(
    title="AI Medical Assistant API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(consultations.router)
app.include_router(medical_notes.router)
app.include_router(transcriptions.router)
app.include_router(doctors.router)
app.include_router(admin.router)
app.include_router(ai_profiles.router)
app.include_router(documents.router)
app.include_router(setup.router)


@app.get("/")
def root():
    return {
        "message": "AI Medical Assistant API is running"
    }