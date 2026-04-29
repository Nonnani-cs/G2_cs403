from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.utils.datetime_utils import utc_now


def list_patients(db: Session, search: str | None = None) -> list[Patient]:
    stmt = select(Patient)
    if search:
        stmt = stmt.where((Patient.hn.ilike(f"%{search}%")) | (Patient.full_name.ilike(f"%{search}%")))
    return list(db.scalars(stmt.order_by(Patient.id.desc())).all())


def create_patient(db: Session, payload) -> Patient:
    existing = db.execute(select(Patient).where(Patient.hn == payload.hn)).scalar_one_or_none()
    if existing:
        existing.full_name = payload.full_name
        existing.dvc_status = payload.dvc_status
        db.commit()
        db.refresh(existing)
        return existing

    patient = Patient(**payload.model_dump(), created_at=utc_now())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient
