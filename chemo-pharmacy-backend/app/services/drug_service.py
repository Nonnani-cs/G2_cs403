from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.drug import Drug
from app.utils.datetime_utils import utc_now


def list_drugs(db: Session, search: str | None = None) -> list[Drug]:
    stmt: Select[tuple[Drug]] = select(Drug)
    if search:
        stmt = stmt.where(Drug.trade_name.ilike(f"%{search}%"))
    return list(db.scalars(stmt.order_by(Drug.id.desc())).all())


def create_drug(db: Session, payload) -> Drug:
    drug = Drug(**payload.model_dump(), created_at=utc_now())
    db.add(drug)
    db.commit()
    db.refresh(drug)
    return drug
