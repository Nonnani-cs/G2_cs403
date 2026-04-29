from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.base import Base
from app.db.database import engine
from app.middleware.error_handler import register_error_handlers
from app.middleware.request_context import request_context_middleware
from app.routes import auth, drugs, inventory, patients, prescriptions, reports

# Ensure model metadata is imported for table creation.
from app import models  # noqa: F401

app = FastAPI(title=settings.app_name)
app.middleware("http")(request_context_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(drugs.router)
app.include_router(patients.router)
app.include_router(prescriptions.router)
app.include_router(inventory.router)
app.include_router(reports.router)

register_error_handlers(app)


@app.get("/health")
def health():
    return {"status": "success", "data": {"service": "ok"}}


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
