from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.drug import Drug
from app.models.inventory import InventoryTransaction


def stock_summary(db: Session):
    rows = db.execute(select(Drug.id, Drug.trade_name, Drug.stock_qty, Drug.reorder_level).order_by(Drug.trade_name)).all()
    return [
        {"drug_id": r.id, "trade_name": r.trade_name, "stock_qty": r.stock_qty, "reorder_level": r.reorder_level}
        for r in rows
    ]


def expiry_analysis(db: Session, days: int = 90):
    until = date.today() + timedelta(days=days)
    rows = db.scalars(select(Drug).where(Drug.expiry_date.is_not(None), Drug.expiry_date <= until)).all()
    return [{"drug_code": d.drug_code, "trade_name": d.trade_name, "expiry_date": str(d.expiry_date)} for d in rows]


def dispensing_audit(db: Session):
    rows = db.execute(
        select(InventoryTransaction.drug_id, func.sum(InventoryTransaction.qty).label("total_qty")).where(
            InventoryTransaction.action == "dispense"
        ).group_by(InventoryTransaction.drug_id)
    ).all()
    return [{"drug_id": r.drug_id, "total_qty": r.total_qty} for r in rows]
