from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest
from app.schemas.common import SuccessResponse
from app.schemas.user import UserOut, UserUpdate
from app.services.auth_service import login_user, register_user, rotate_access_token, list_users, update_user, delete_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=SuccessResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, payload)
    return SuccessResponse(data=UserOut.model_validate(user).model_dump())


@router.post("/login", response_model=SuccessResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return SuccessResponse(data=login_user(db, payload.username, payload.password))


@router.post("/refresh", response_model=SuccessResponse)
def refresh(payload: RefreshRequest):
    return SuccessResponse(data=rotate_access_token(payload.refresh_token))


@router.post("/logout", response_model=SuccessResponse)
def logout():
    return SuccessResponse(message="Logout accepted (stateless JWT strategy)")


@router.get("/me", response_model=SuccessResponse)
def me(user: User = Depends(get_current_user)):
    return SuccessResponse(data=UserOut.model_validate(user).model_dump())


@router.get("/users", response_model=SuccessResponse)
def get_users(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return SuccessResponse(data=[UserOut.model_validate(u).model_dump() for u in list_users(db)])


@router.put("/users/{user_id}", response_model=SuccessResponse)
def edit_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    u = update_user(db, user_id, payload)
    return SuccessResponse(data=UserOut.model_validate(u).model_dump())


@router.delete("/users/{user_id}", response_model=SuccessResponse)
def remove_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    delete_user(db, user_id)
    return SuccessResponse(message="User deleted")
