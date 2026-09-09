"""
FastAPI Application Entry Point.

Configures CORS, database table creation on startup, and registers
REST API v1 routers for Auth, Uploads, Dashboard, and Bilingual Agent.
Mounts legacy static/template directories for backward compatibility.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from app.database import engine, Base
from app.models import SyllabusTopic, Note, NoteChunk, PYQ, TopicImportance  # noqa: F401
from app.routers import auth, dashboard, upload, agent

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all database tables on application startup."""
    Base.metadata.create_all(bind=engine)
    os.makedirs(os.path.join(BASE_DIR, "..", "uploads"), exist_ok=True)
    yield


app = FastAPI(
    title="CampusClimb — NLP Notes System REST API",
    description="Versioned REST API for syllabus-aligned notes deduplication & bilingual Q&A",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration — restrict allowed origins explicitly
cors_env = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
allowed_origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "X-Requested-With"],
)

# Mount legacy static files and templates (untouched for transition)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.state.templates = templates

# Register REST API v1 Routers
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(dashboard.router)
app.include_router(agent.router)
