from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "Admin"
    SENIOR_PHARMACIST = "Senior Pharmacist"
    GENERAL_PHARMACIST = "General Pharmacist"


class PrescriptionStatus(str, Enum):
    PENDING = "รอจ่ายยา"
    PREPARING = "กำลังจัดยา"
    DISPENSED = "จ่ายยาแล้ว"
    CANCELLED = "ยกเลิก"
