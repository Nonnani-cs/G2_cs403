from pydantic import BaseModel


class ReceiveRequest(BaseModel):
    drug_id: int
    qty: float


class DispenseRequest(BaseModel):
    prescription_id: int
