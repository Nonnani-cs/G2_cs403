from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.drug import Drug
from app.models.inventory import InventoryTransaction
from app.models.prescription import Prescription, PrescriptionItem
from app.models.report import AuditLog
from app.models.user import User
from app.utils.datetime_utils import utc_now
from app.utils.enums import PrescriptionStatus


def receive_stock(db: Session, drug_id: int, qty: float, user: User) -> Drug:
    if qty <= 0:
        raise HTTPException(status_code=400, detail="qty must be > 0")
    drug = db.get(Drug, drug_id)
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    try:
        drug.stock_qty += qty
        db.add(
            InventoryTransaction(
                drug_id=drug_id,
                action="receive",
                qty=qty,
                actor_user_id=user.id,
                ref_type="manual",
                ref_id=None,
                created_at=utc_now(),
            )
        )
        db.add(AuditLog(action="receive", actor_username=user.username, details=f"drug_id={drug_id}", created_at=utc_now()))
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(drug)
    return drug


def dispense_prescription(db: Session, prescription_id: int, user: User) -> Prescription:
    rx = db.get(Prescription, prescription_id)
    if not rx:
        raise HTTPException(status_code=404, detail="Prescription not found")
    if rx.status == PrescriptionStatus.DISPENSED.value:
        raise HTTPException(status_code=409, detail="Prescription already dispensed")

    items = list(db.scalars(select(PrescriptionItem).where(PrescriptionItem.prescription_id == prescription_id)).all())
    try:
        for item in items:
            drug = db.get(Drug, item.drug_id)
            if drug.stock_qty < item.qty:
                raise HTTPException(status_code=409, detail=f"Insufficient stock for drug_id={item.drug_id}")
            drug.stock_qty -= item.qty
            if drug.stock_qty < 0:
                raise HTTPException(status_code=409, detail="Negative stock is not allowed")
            db.add(
                InventoryTransaction(
                    drug_id=item.drug_id,
                    action="dispense",
                    qty=item.qty,
                    actor_user_id=user.id,
                    ref_type="prescription",
                    ref_id=prescription_id,
                    created_at=utc_now(),
                )
            )
        rx.status = PrescriptionStatus.DISPENSED.value
        db.add(AuditLog(action="dispense", actor_username=user.username, details=f"prescription_id={prescription_id}", created_at=utc_now()))
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(rx)
    return rx
