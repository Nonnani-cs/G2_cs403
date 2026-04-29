from fastapi import HTTPException
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.drug import Drug
from app.models.patient import Patient
from app.models.prescription import Prescription, PrescriptionItem
from app.utils.datetime_utils import utc_now
from app.utils.enums import PrescriptionStatus


from sqlalchemy.orm import joinedload

def list_prescriptions(db: Session) -> list[Prescription]:
    return list(db.scalars(select(Prescription).options(joinedload(Prescription.items)).order_by(Prescription.id.desc())).unique().all())


def create_prescription(db: Session, payload) -> Prescription:
    if not payload.items:
        raise HTTPException(status_code=400, detail="Prescription needs items")
    rx = Prescription(
        order_no=payload.order_no,
        patient_id=payload.patient_id,
        notes=payload.notes,
        status=PrescriptionStatus.PENDING.value,
        created_at=utc_now(),
    )
    db.add(rx)
    db.flush()
    for item in payload.items:
        drug = db.get(Drug, item.drug_id)
        if not drug:
            raise HTTPException(status_code=404, detail=f"Drug {item.drug_id} not found")
        db.add(PrescriptionItem(prescription_id=rx.id, drug_id=item.drug_id, qty=item.qty))
    db.commit()
    db.refresh(rx)
    return rx


def sync_prescription(db: Session, payload) -> Prescription:
    # Get or create patient
    patient = db.execute(select(Patient).where(Patient.hn == payload.hn)).scalar_one_or_none()
    if not patient:
        patient = Patient(hn=payload.hn, full_name=payload.patient, created_at=utc_now())
        db.add(patient)
        db.flush()
    else:
        patient.full_name = payload.patient
        db.flush()

    # Get or create prescription
    rx = db.execute(select(Prescription).where(Prescription.order_no == payload.order_no)).scalar_one_or_none()
    if not rx:
        rx = Prescription(
            order_no=payload.order_no,
            patient_id=patient.id,
            notes=payload.doctor,
            status=payload.status,
            created_at=utc_now()
        )
        db.add(rx)
        db.flush()
    else:
        rx.patient_id = patient.id
        rx.notes = payload.doctor
        rx.status = payload.status
        # Delete old items
        db.execute(sqlalchemy.delete(PrescriptionItem).where(PrescriptionItem.prescription_id == rx.id))
        db.flush()

    # Add items
    for item in payload.items:
        drug = db.execute(select(Drug).where(Drug.drug_code == item.code)).scalar_one_or_none()
        if drug:
            db.add(PrescriptionItem(prescription_id=rx.id, drug_id=drug.id, qty=item.qty))
    
    db.commit()
    db.refresh(rx)
    return rx
