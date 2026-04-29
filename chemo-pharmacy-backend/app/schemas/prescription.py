from datetime import datetime

from pydantic import BaseModel

from app.utils.enums import PrescriptionStatus


class PrescriptionItemIn(BaseModel):
    drug_id: int
    qty: float


class PrescriptionCreate(BaseModel):
    order_no: str
    patient_id: int
    notes: str = ""
    items: list[PrescriptionItemIn]


class PrescriptionStatusUpdate(BaseModel):
    status: PrescriptionStatus


class PrescriptionSyncItemIn(BaseModel):
    code: str
    qty: float
    name: str = ""

class PrescriptionSyncIn(BaseModel):
    order_no: str
    hn: str
    patient: str
    doctor: str = ""
    status: str = "รอดำเนินการ"
    items: list[PrescriptionSyncItemIn]


class PrescriptionItemOut(BaseModel):
    id: int
    drug_id: int
    qty: float
    model_config = {"from_attributes": True}


class PrescriptionOut(BaseModel):
    id: int
    order_no: str
    patient_id: int
    status: str
    notes: str
    created_at: datetime
    items: list[PrescriptionItemOut]

    model_config = {"from_attributes": True}
