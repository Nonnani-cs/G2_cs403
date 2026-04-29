from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.auth import get_current_user
from app.models.drug import Drug
from app.models.inventory import InventoryTransaction
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.schemas.inventory import DispenseRequest, ReceiveRequest
from app.schemas.prescription import PrescriptionOut
from app.services.inventory_service import dispense_prescription, receive_stock

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.post("/receive", response_model=SuccessResponse)
def receive(payload: ReceiveRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    updated = receive_stock(db, payload.drug_id, payload.qty, user)
    return SuccessResponse(data={"drug_id": updated.id, "stock_qty": updated.stock_qty})


@router.post("/dispense", response_model=SuccessResponse)
def dispense(payload: DispenseRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rx = dispense_prescription(db, payload.prescription_id, user)
    return SuccessResponse(data=PrescriptionOut.model_validate(rx).model_dump())


@router.get("/stock-levels", response_model=SuccessResponse)
def stock_levels(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.query(Drug).order_by(Drug.trade_name).all()
    return SuccessResponse(data=[{"drug_id": d.id, "trade_name": d.trade_name, "stock_qty": d.stock_qty} for d in rows])


@router.get("/transactions", response_model=SuccessResponse)
def transactions(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.query(InventoryTransaction).order_by(InventoryTransaction.created_at.desc()).all()
    data = []
    for r in rows:
        drug = db.get(Drug, r.drug_id)
        data.append({
            "id": r.id,
            "drug_id": r.drug_id,
            "drug_name": drug.generic_name if drug else "Unknown",
            "trade_name": drug.trade_name if drug else "Unknown",
            "lot_no": drug.lot_no if drug else "Unknown",
            "action": r.action,
            "qty": r.qty,
            "actor_user_id": r.actor_user_id,
            "ref_type": r.ref_type,
            "ref_id": r.ref_id,
            "created_at": r.created_at.isoformat()
        })
    return SuccessResponse(data=data)
