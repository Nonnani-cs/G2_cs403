from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.auth import get_current_user
from app.models.patient import Patient
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.schemas.patient import PatientCreate, PatientOut, PatientUpdate
from app.services.patient_service import create_patient, list_patients

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.get("/", response_model=SuccessResponse)
def list_all(search: str | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return SuccessResponse(data=[PatientOut.model_validate(p).model_dump() for p in list_patients(db, search)])


@router.get("/{patient_id}", response_model=SuccessResponse)
def detail(patient_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    item = db.get(Patient, patient_id)
    if not item:
        raise HTTPException(status_code=404, detail="Patient not found")
    return SuccessResponse(data=PatientOut.model_validate(item).model_dump())


@router.post("/", response_model=SuccessResponse)
def create(payload: PatientCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return SuccessResponse(data=PatientOut.model_validate(create_patient(db, payload)).model_dump())


@router.put("/{patient_id}", response_model=SuccessResponse)
def update(patient_id: int, payload: PatientUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    item = db.get(Patient, patient_id)
    if not item:
        raise HTTPException(status_code=404, detail="Patient not found")
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return SuccessResponse(data=PatientOut.model_validate(item).model_dump())
