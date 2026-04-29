from pydantic import BaseModel, Field

from app.utils.enums import RoleEnum


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str = Field(min_length=3)
    full_name: str | None = None
    fullname: str | None = None
    role: RoleEnum = RoleEnum.GENERAL_PHARMACIST


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str
