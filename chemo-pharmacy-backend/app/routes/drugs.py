from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.auth import get_current_user, require_roles
from app.models.drug import Drug
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.schemas.drug import DrugCreate, DrugOut, DrugUpdate
from app.services.drug_service import create_drug, list_drugs
from app.utils.enums import RoleEnum

router = APIRouter(prefix="/api/drugs", tags=["drugs"])


@router.get("/", response_model=SuccessResponse)
def list_all(search: str | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    items = [DrugOut.model_validate(d).model_dump() for d in list_drugs(db, search)]
    return SuccessResponse(data=items)


@router.get("/{drug_id}", response_model=SuccessResponse)
def detail(drug_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    drug = db.get(Drug, drug_id)
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return SuccessResponse(data=DrugOut.model_validate(drug).model_dump())


@router.post("/", response_model=SuccessResponse)
def create(payload: DrugCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(RoleEnum.ADMIN.value, RoleEnum.SENIOR_PHARMACIST.value))):
    return SuccessResponse(data=DrugOut.model_validate(create_drug(db, payload)).model_dump())


@router.put("/{drug_id}", response_model=SuccessResponse)
def update(drug_id: int, payload: DrugUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(RoleEnum.ADMIN.value, RoleEnum.SENIOR_PHARMACIST.value))):
    drug = db.get(Drug, drug_id)
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(drug, k, v)
    db.commit()
    db.refresh(drug)
    return SuccessResponse(data=DrugOut.model_validate(drug).model_dump())


@router.delete("/{drug_id}", response_model=SuccessResponse)
def delete(drug_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(RoleEnum.ADMIN.value))):
    drug = db.get(Drug, drug_id)
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    db.delete(drug)
    db.commit()
    return SuccessResponse(message="Drug deleted")
