from datetime import date, datetime

from pydantic import BaseModel


class DrugBase(BaseModel):
    drug_code: str
    trade_name: str
    generic_name: str = ""
    unit: str = "vial"
    lot_no: str = ""
    expiry_date: date | None = None
    stock_qty: float = 0
    reorder_level: float = 0


class DrugCreate(DrugBase):
    pass


class DrugUpdate(BaseModel):
    trade_name: str | None = None
    generic_name: str | None = None
    unit: str | None = None
    lot_no: str | None = None
    expiry_date: date | None = None
    reorder_level: float | None = None


class DrugOut(DrugBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
