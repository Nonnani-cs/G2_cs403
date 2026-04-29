from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.services.report_service import dispensing_audit, expiry_analysis, stock_summary

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/stock-summary", response_model=SuccessResponse)
def get_stock_summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return SuccessResponse(data=stock_summary(db))


@router.get("/expiry-analysis", response_model=SuccessResponse)
def get_expiry(days: int = 90, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return SuccessResponse(data=expiry_analysis(db, days))


@router.get("/dispensing-audit", response_model=SuccessResponse)
def get_audit(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return SuccessResponse(data=dispensing_audit(db))
