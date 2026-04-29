import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.db.base import Base
from app.models.drug import Drug
from app.models.user import User
from datetime import datetime

from app.utils.security import hash_password
from app.models.patient import Patient
from app.models.prescription import Prescription, PrescriptionItem
from app.models.inventory import InventoryTransaction
from app.utils.enums import PrescriptionStatus

DEFAULT_CANCER_DRUGS = [
    {'drug_code': 'PD-00007', 'trade_name': 'Cisplatin 50mg', 'generic_name': 'Cisplatin', 'unit': 'ขวด', 'stock_qty': 120, 'reorder_level': 20, 'lot_no': 'CIS-2026-001', 'expiry_date': datetime(2027, 6, 30)},
    {'drug_code': 'PD-00008', 'trade_name': 'Endoxan 500mg', 'generic_name': 'Cyclophosphamide', 'unit': 'ขวด', 'stock_qty': 180, 'reorder_level': 30, 'lot_no': 'END-2026-012', 'expiry_date': datetime(2027, 3, 15)},
    {'drug_code': 'PD-00009', 'trade_name': 'Adriamycin 50mg', 'generic_name': 'Doxorubicin', 'unit': 'ขวด', 'stock_qty': 95, 'reorder_level': 20, 'lot_no': 'ADR-2025-088', 'expiry_date': datetime(2025, 10, 20)},
    {'drug_code': 'PD-00010', 'trade_name': 'Taxol 100mg', 'generic_name': 'Paclitaxel', 'unit': 'ขวด', 'stock_qty': 70, 'reorder_level': 15, 'lot_no': 'TAX-2026-099', 'expiry_date': datetime(2027, 9, 1)},
    {'drug_code': 'PD-00011', 'trade_name': 'Carboplatin 450mg', 'generic_name': 'Carboplatin', 'unit': 'ขวด', 'stock_qty': 88, 'reorder_level': 18, 'lot_no': 'CARB-2026-11', 'expiry_date': datetime(2027, 12, 31)},
    {'drug_code': 'PD-00012', 'trade_name': 'Gemcitabine 1g', 'generic_name': 'Gemcitabine', 'unit': 'ขวด', 'stock_qty': 76, 'reorder_level': 15, 'lot_no': 'GEM-2026-044', 'expiry_date': datetime(2027, 4, 10)},
    {'drug_code': 'PD-00013', 'trade_name': 'Fluorouracil 5g', 'generic_name': 'Fluorouracil', 'unit': 'ขวด', 'stock_qty': 110, 'reorder_level': 25, 'lot_no': 'FU-2026-2024', 'expiry_date': datetime(2026, 6, 10)},
    {'drug_code': 'PD-00014', 'trade_name': 'Oxaliplatin 100mg', 'generic_name': 'Oxaliplatin', 'unit': 'ขวด', 'stock_qty': 64, 'reorder_level': 12, 'lot_no': 'OXA-2026-055', 'expiry_date': datetime(2027, 7, 7)},
    {'drug_code': 'PD-00015', 'trade_name': 'Docetaxel 80mg', 'generic_name': 'Docetaxel', 'unit': 'ขวด', 'stock_qty': 52, 'reorder_level': 10, 'lot_no': 'DOC-2026-033', 'expiry_date': datetime(2026, 6, 20)},
    {'drug_code': 'PD-00016', 'trade_name': 'Irinotecan 100mg', 'generic_name': 'Irinotecan', 'unit': 'ขวด', 'stock_qty': 60, 'reorder_level': 12, 'lot_no': 'IRI-2026-077', 'expiry_date': datetime(2027, 7, 20)}
]

DEFAULT_USERS = [
    {'username': 'admin', 'password': 'password', 'full_name': 'แอดมิน ระบบ', 'role': 'Senior Pharmacist'},
    {'username': 'user1', 'password': 'password', 'full_name': 'เภสัชกร ทดสอบ', 'role': 'General Pharmacist'},
]

DEFAULT_PATIENTS = [
    {'hn': '66001234', 'full_name': 'นายสมชาย ใจดี'},
    {'hn': '66005678', 'full_name': 'นางสาวสมศรี เรียนดี'},
    {'hn': '66011111', 'full_name': 'นายวิชัย มั่นคง'},
    {'hn': '66022222', 'full_name': 'นางรัตนา ทรัพย์มาก'},
]

DEFAULT_PRESCRIPTIONS = [
    {
        'order_no': 'RX-2026-001',
        'hn': '66001234',
        'status': PrescriptionStatus.PENDING.value,
        'items': [
            {'drug_code': 'PD-00008', 'qty': 2.0},
            {'drug_code': 'PD-00009', 'qty': 1.0}
        ]
    },
    {
        'order_no': 'RX-2026-002',
        'hn': '66005678',
        'status': PrescriptionStatus.PENDING.value,
        'items': [
            {'drug_code': 'PD-00010', 'qty': 3.0}
        ]
    },
    {
        'order_no': 'RX-2026-003',
        'hn': '66022222',
        'status': PrescriptionStatus.PENDING.value,
        'items': [
            {'drug_code': 'PD-00013', 'qty': 1.0},
            {'drug_code': 'PD-00014', 'qty': 2.0}
        ]
    },
    {
        'order_no': 'RX-2026-004',
        'hn': '66011111',
        'status': PrescriptionStatus.PENDING.value,
        'items': [
            {'drug_code': 'PD-00007', 'qty': 2.0},
            {'drug_code': 'PD-00016', 'qty': 2.0}
        ]
    }
]

DEFAULT_TRANSACTIONS = [
    {'action': 'receive', 'drug_code': 'PD-00008', 'qty': 50, 'ref_type': 'manual'},
    {'action': 'receive', 'drug_code': 'PD-00009', 'qty': 30, 'ref_type': 'manual'},
    {'action': 'dispense', 'drug_code': 'PD-00010', 'qty': 10, 'ref_type': 'patient'},
    {'action': 'dispense', 'drug_code': 'PD-00013', 'qty': 2, 'ref_type': 'damage'}
]

Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()
try:
    print("Seeding Drugs...")
    for item in DEFAULT_CANCER_DRUGS:
        existing = db.query(Drug).filter(Drug.drug_code == item['drug_code']).first()
        if not existing:
            drug = Drug(
                drug_code=item['drug_code'],
                trade_name=item['trade_name'],
                generic_name=item['generic_name'],
                unit=item['unit'],
                stock_qty=item['stock_qty'],
                reorder_level=item['reorder_level'],
                lot_no=item['lot_no'],
                expiry_date=item['expiry_date'],
                created_at=datetime.utcnow()
            )
            db.add(drug)
    db.commit()

    print("Seeding Users...")
    for u in DEFAULT_USERS:
        existing = db.query(User).filter(User.username == u['username']).first()
        if not existing:
            user = User(
                username=u['username'],
                full_name=u['full_name'],
                password_hash=hash_password(u['password']),
                role=u['role'],
                created_at=datetime.utcnow()
            )
            db.add(user)
    db.commit()

    print("Seeding Patients...")
    for p in DEFAULT_PATIENTS:
        existing = db.query(Patient).filter(Patient.hn == p['hn']).first()
        if not existing:
            patient = Patient(
                hn=p['hn'],
                full_name=p['full_name'],
                created_at=datetime.utcnow()
            )
            db.add(patient)
    db.commit()

    print("Seeding Prescriptions...")
    for rx_data in DEFAULT_PRESCRIPTIONS:
        existing = db.query(Prescription).filter(Prescription.order_no == rx_data['order_no']).first()
        if not existing:
            patient = db.query(Patient).filter(Patient.hn == rx_data['hn']).first()
            if patient:
                rx = Prescription(
                    order_no=rx_data['order_no'],
                    patient_id=patient.id,
                    status=rx_data['status'],
                    created_at=datetime.utcnow()
                )
                db.add(rx)
                db.commit()
                db.refresh(rx)
                
                for item_data in rx_data['items']:
                    drug = db.query(Drug).filter(Drug.drug_code == item_data['drug_code']).first()
                    if drug:
                        db.add(PrescriptionItem(
                            prescription_id=rx.id,
                            drug_id=drug.id,
                            qty=item_data['qty']
                        ))
                db.commit()

    print("Seeding Transactions...")
    if db.query(InventoryTransaction).count() == 0:
        admin_user = db.query(User).filter(User.username == 'admin').first()
        for tx in DEFAULT_TRANSACTIONS:
            drug = db.query(Drug).filter(Drug.drug_code == tx['drug_code']).first()
            if drug and admin_user:
                db.add(InventoryTransaction(
                    drug_id=drug.id,
                    action=tx['action'],
                    qty=tx['qty'],
                    actor_user_id=admin_user.id,
                    ref_type=tx['ref_type'],
                    ref_id=None,
                    created_at=datetime.utcnow()
                ))
        db.commit()

    print("Seeding complete.")
except Exception as e:
    print(f"Error seeding: {e}")
    db.rollback()
finally:
    db.close()
