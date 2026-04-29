from datetime import datetime

from pydantic import BaseModel


class UserUpdate(BaseModel):
    full_name: str
    role: str


class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}
