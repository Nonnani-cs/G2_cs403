from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models.report import AuditLog
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.utils.constants import CONFLICT_ERROR
from app.utils.datetime_utils import utc_now
from app.utils.security import create_access_token, create_refresh_token, hash_password, verify_password


def register_user(db: Session, payload: RegisterRequest) -> User:
    full_name = payload.full_name or payload.fullname
    if not full_name:
        raise HTTPException(status_code=400, detail="full_name is required")

    existing = db.scalar(select(User).where(User.username == payload.username))
    if existing:
        raise HTTPException(status_code=409, detail=CONFLICT_ERROR)

    user = User(
        username=payload.username,
        full_name=full_name,
        password_hash=hash_password(payload.password),
        role=payload.role.value,
        created_at=utc_now(),
    )
    db.add(user)
    db.add(AuditLog(action="user_create", actor_username=payload.username, details="", created_at=utc_now()))
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, username: str, password: str) -> dict:
    user = db.scalar(select(User).where(User.username == username))
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    db.add(AuditLog(action="login", actor_username=user.username, details="", created_at=utc_now()))
    db.commit()
    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
        "token_type": "bearer",
    }


def rotate_access_token(refresh_token: str) -> dict:
    try:
        payload = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        username = payload.get("sub")
        return {"access_token": create_access_token(username), "refresh_token": refresh_token, "token_type": "bearer"}
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from exc

def list_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.id)).all())


def update_user(db: Session, user_id: int, payload) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.full_name = payload.full_name
    user.role = payload.role
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
