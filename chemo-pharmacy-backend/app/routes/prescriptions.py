from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.auth import get_current_user
from app.models.prescription import Prescription
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.schemas.prescription import PrescriptionCreate, PrescriptionOut, PrescriptionStatusUpdate, PrescriptionSyncIn
from app.services.prescription_service import create_prescription, list_prescriptions, sync_prescription

router = APIRouter(prefix="/api/prescriptions", tags=["prescriptions"])


@router.get("/", response_model=SuccessResponse)
def list_all(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return SuccessResponse(data=[PrescriptionOut.model_validate(r).model_dump() for r in list_prescriptions(db)])


@router.get("/{prescription_id}", response_model=SuccessResponse)
def detail(prescription_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rx = db.get(Prescription, prescription_id)
    if not rx:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return SuccessResponse(data=PrescriptionOut.model_validate(rx).model_dump())


@router.post("/", response_model=SuccessResponse)
def create(payload: PrescriptionCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rx = create_prescription(db, payload)
    return SuccessResponse(data=PrescriptionOut.model_validate(rx).model_dump())


@router.post("/sync", response_model=SuccessResponse)
def sync(payload: PrescriptionSyncIn, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rx = sync_prescription(db, payload)
    return SuccessResponse(data=PrescriptionOut.model_validate(rx).model_dump())


@router.patch("/{prescription_id}/status", response_model=SuccessResponse)
def update_status(prescription_id: int, payload: PrescriptionStatusUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rx = db.get(Prescription, prescription_id)
    if not rx:
        raise HTTPException(status_code=404, detail="Prescription not found")
    rx.status = payload.status.value
    db.commit()
    db.refresh(rx)
    return SuccessResponse(data=PrescriptionOut.model_validate(rx).model_dump())
