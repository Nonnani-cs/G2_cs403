from pydantic import BaseModel


class StockSummaryRow(BaseModel):
    drug_id: int
    trade_name: str
    stock_qty: float
    reorder_level: float
