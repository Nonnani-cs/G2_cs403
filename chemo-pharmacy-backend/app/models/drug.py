from sqlalchemy import Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Drug(Base):
    __tablename__ = "drugs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drug_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    trade_name: Mapped[str] = mapped_column(String(255), nullable=False)
    generic_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    unit: Mapped[str] = mapped_column(String(30), default="vial", nullable=False)
    lot_no: Mapped[str] = mapped_column(String(50), default="", nullable=False)
    expiry_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    stock_qty: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    reorder_level: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
