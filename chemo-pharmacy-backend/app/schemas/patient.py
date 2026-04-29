from datetime import datetime

from pydantic import BaseModel


class PatientCreate(BaseModel):
    hn: str
    full_name: str
    dvc_status: str = ""


class PatientUpdate(BaseModel):
    full_name: str | None = None
    dvc_status: str | None = None


class PatientOut(BaseModel):
    id: int
    hn: str
    full_name: str
    dvc_status: str
    created_at: datetime

    model_config = {"from_attributes": True}
