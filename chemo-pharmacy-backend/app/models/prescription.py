from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
import sqlalchemy.orm
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.utils.enums import PrescriptionStatus


class Prescription(Base):
    __tablename__ = "prescriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_no: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), default=PrescriptionStatus.PENDING.value, nullable=False)
    notes: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    items: Mapped[list["PrescriptionItem"]] = sqlalchemy.orm.relationship(
        "PrescriptionItem", back_populates="prescription", cascade="all, delete-orphan"
    )


class PrescriptionItem(Base):
    __tablename__ = "prescription_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prescription_id: Mapped[int] = mapped_column(ForeignKey("prescriptions.id"), nullable=False, index=True)
    drug_id: Mapped[int] = mapped_column(ForeignKey("drugs.id"), nullable=False, index=True)
    qty: Mapped[float] = mapped_column(Float, nullable=False)

    prescription: Mapped["Prescription"] = sqlalchemy.orm.relationship("Prescription", back_populates="items")
