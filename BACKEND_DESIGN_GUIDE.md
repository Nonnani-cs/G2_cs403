# 🚀 Backend Design Guide
## ระบบจัดการยาเคมีบำบัดโรงพยาบาล (Chemotherapy Pharmacy Management System)

**Document Version:** 1.0  
**Date:** 28 April 2026  
**Author:** Senior Code Analyzer & System Architect  
**Tech Stack Recommendation:** Python (Flask/FastAPI) + MySQL/MariaDB

---

## 📋 Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Tech Stack Recommendation](#tech-stack-recommendation)
3. [Database Integration](#database-integration)
4. [API Endpoints Specification](#api-endpoints-specification)
5. [Authentication & Authorization](#authentication--authorization)
6. [Error Handling & Validation](#error-handling--validation)
7. [Implementation Roadmap](#implementation-roadmap)
8. [Code Structure & Organization](#code-structure--organization)
9. [Security Considerations](#security-considerations)
10. [Testing Strategy](#testing-strategy)

---

## 1. Architecture Overview

### 1.1 Current System (Client-Side Only)
```
┌─────────────────────────────────────┐
│        Frontend (HTML/CSS/JS)       │
│  - 10 HTML pages                    │
│  - localStorage (Mock Data)         │
│  - Tailwind CSS + Lucide Icons      │
└─────────────────────────────────────┘
           NO CONNECTION
┌─────────────────────────────────────┐
│    Database (MySQL/MariaDB)         │
│  - 9 tables (chemo_management)      │
│  - Schema designed but unused       │
└─────────────────────────────────────┘
```

### 1.2 Target Architecture (After Backend Implementation)
```
┌──────────────────────────────────────────────────────────────┐
│                    Frontend Layer                            │
│              (Browser-based HTML/CSS/JS)                     │
│  ├─ login.html, index.html, manage.html                     │
│  ├─ receive.html, prescription.html, dispense.html          │
│  └─ AJAX/Fetch API calls to Backend                         │
└──────────────────────────────────┬───────────────────────────┘
                                   │
                        HTTP/HTTPS (REST API)
                                   │
        ┌──────────────────────────▼──────────────────────────┐
        │              Backend Layer                          │
        │         (Python Flask/FastAPI Server)              │
        │  ├─ Authentication (JWT Tokens)                    │
        │  ├─ Route Handlers (API Endpoints)                 │
        │  ├─ Business Logic                                 │
        │  ├─ Data Validation & Security                     │
        │  └─ Logging & Monitoring                           │
        └──────────────────────────┬───────────────────────────┘
                                   │
                          Database Connection
                                   │
        ┌──────────────────────────▼──────────────────────────┐
        │            Database Layer                          │
        │         (MySQL/MariaDB Server)                     │
        │  ├─ users, patients, drugs                         │
        │  ├─ prescriptions, drug_lots                       │
        │  ├─ receive_orders, drug_labels                    │
        │  └─ Indexes & Query Optimization                  │
        └──────────────────────────────────────────────────────┘
```

---

## 2. Tech Stack Recommendation

### 2.1 Backend Framework
| Component | Recommendation | Alternative | Reason |
|-----------|---|---|---|
| **Language** | Python 3.9+ | Node.js | Easy to learn, strong in medical/pharmacy systems |
| **Framework** | Flask OR FastAPI | Django | Flask: Lightweight, flexible; FastAPI: Modern async |
| **ORM** | SQLAlchemy | Peewee | Industry standard, excellent MySQL support |
| **DBMS** | MySQL 8.0 | PostgreSQL | Compatible with existing schema |
| **Authentication** | JWT (PyJWT) | OAuth2 | Simple, secure token-based auth |
| **Password Hashing** | bcrypt | Argon2 | Battle-tested, OWASP recommended |
| **API Documentation** | Swagger (FastAPI) | Postman | Auto-generated, interactive docs |
| **Testing** | pytest | unittest | More powerful, better for complex tests |

### 2.2 Recommended Stack (I choose FastAPI + SQLAlchemy)
```
Frontend
  ↓ (AJAX/Fetch)
FastAPI (Async Python)
  ├─ Pydantic (Request validation)
  ├─ JWT (Authentication)
  ├─ Bcrypt (Password hashing)
  └─ CORS (Cross-origin requests)
  ↓
SQLAlchemy ORM
  ↓
MySQL 8.0 Database
```

---

## 3. Database Integration

### 3.1 Migration from Mock Data to Real Database

**Phase 1: Initialize Database**
```sql
-- Already provided in chemo_management.sql
-- Just ensure all 9 tables are created with proper indexes
CREATE INDEX idx_user_username ON users(username);
CREATE INDEX idx_patients_hn ON patients(hn);
CREATE INDEX idx_drugs_code ON drugs(drug_code);
CREATE INDEX idx_prescriptions_status ON prescriptions(status);
CREATE INDEX idx_drug_lots_expiry ON drug_lots(expiry_date);
```

**Phase 2: Connection Pool**
```python
# Backend will use SQLAlchemy connection pooling
from sqlalchemy import create_engine

engine = create_engine(
    'mysql+pymysql://user:password@localhost:3306/chemo_management',
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True  # Verify connection before using
)
```

### 3.2 ORM Models (SQLAlchemy)

**Example Structure:**
```python
# models/user.py
from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # bcrypt hash
    full_name = Column(String(100), nullable=False)
    role = Column(Enum('Admin', 'Pharmacist', 'Staff'), default='Pharmacist')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# models/drug.py
class Drug(Base):
    __tablename__ = "drugs"
    
    drug_code = Column(String(20), primary_key=True)
    barcode = Column(String(50), unique=True)
    generic_name = Column(String(255), nullable=False)
    trade_name = Column(String(255), nullable=False)
    total_stock = Column(Integer, default=0)
    is_high_alert = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

## 4. API Endpoints Specification

### 4.1 Authentication Endpoints

#### `POST /api/auth/login`
**Purpose:** User login with credentials
```
Request:
{
  "username": "admin",
  "password": "hashedPassword"
}

Response (Success - 200):
{
  "status": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",  // JWT Token
    "user": {
      "user_id": 1,
      "fullname": "ภก. สมชาย ใจดี",
      "role": "Senior Pharmacist"
    },
    "expires_in": 3600  // seconds
  }
}

Response (Failure - 401):
{
  "status": "error",
  "message": "Invalid username or password"
}
```

#### `POST /api/auth/register`
**Purpose:** Register new pharmacist
```
Request:
{
  "fullname": "ภก. สมหญิง",
  "username": "newuser",
  "password": "securepass123",
  "role": "General Pharmacist"
}

Response (Success - 201):
{
  "status": "success",
  "message": "User registered successfully",
  "user_id": 5
}
```

#### `POST /api/auth/logout`
**Purpose:** Logout (invalidate token)
```
Headers: Authorization: Bearer <token>

Response (Success - 200):
{
  "status": "success",
  "message": "Logged out successfully"
}
```

#### `POST /api/auth/refresh-token`
**Purpose:** Refresh JWT token
```
Headers: Authorization: Bearer <expired_token>

Response (Success - 200):
{
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIs..."  // New token
}
```

---

### 4.2 Drug Management Endpoints

#### `GET /api/drugs`
**Purpose:** List all drugs with pagination
```
Query Parameters:
  - page: 1 (default)
  - per_page: 20 (default)
  - storage: "room" | "ref" | "all" (filter by storage)
  - search: "cisplatin" (search by name)

Response (Success - 200):
{
  "status": "success",
  "data": {
    "total": 45,
    "page": 1,
    "per_page": 20,
    "items": [
      {
        "drug_code": "PD-00007",
        "generic_name": "Cisplatin 50mg",
        "trade_name": "Cisplatin",
        "barcode": "885000000007",
        "total_stock": 250,
        "is_high_alert": false,
        "unit": "ขวด",
        "min_quantity": 100,
        "max_quantity": 1000,
        "cost_price": 50.00,
        "selling_price": 75.00
      }
    ]
  }
}
```

#### `GET /api/drugs/<drug_code>`
**Purpose:** Get detailed drug information
```
Response (Success - 200):
{
  "status": "success",
  "data": {
    "drug_code": "PD-00007",
    "generic_name": "Cisplatin 50mg",
    "barcode": "885000000007",
    "total_stock": 250,
    "lots": [
      {
        "lot_id": 1,
        "lot_number": "CIS-2601",
        "expiry_date": "2027-12-31",
        "quantity": 250,
        "status": "ปกติ"
      }
    ],
    "labels": {
      "thai": {
        "usage_instruction": "หยดยาเข้าหลอดเลือดดำ",
        "special_note": "สวมอุปกรณ์ป้องกันทุกครั้ง"
      },
      "english": {
        "usage_instruction": "IV infusion use only",
        "special_note": "Use PPE during preparation"
      }
    }
  }
}
```

#### `POST /api/drugs`
**Purpose:** Create new drug record (Senior Pharmacist only)
```
Headers: Authorization: Bearer <token>

Request:
{
  "drug_code": "PD-00017",
  "generic_name": "New Drug",
  "trade_name": "Trade Name",
  "barcode": "885000000017",
  "unit": "ขวด",
  "cost_price": 100.00,
  "selling_price": 150.00,
  "max_quantity": 500,
  "min_quantity": 50,
  "is_high_alert": false
}

Response (Success - 201):
{
  "status": "success",
  "message": "Drug created successfully",
  "drug_code": "PD-00017"
}
```

#### `PUT /api/drugs/<drug_code>`
**Purpose:** Update drug information
```
Headers: Authorization: Bearer <token>

Request:
{
  "generic_name": "Updated Name",
  "total_stock": 300,
  "min_quantity": 80
}

Response (Success - 200):
{
  "status": "success",
  "message": "Drug updated successfully"
}
```

#### `DELETE /api/drugs/<drug_code>`
**Purpose:** Delete drug (Admin only)
```
Headers: Authorization: Bearer <token>

Response (Success - 200):
{
  "status": "success",
  "message": "Drug deleted successfully"
}
```

---

### 4.3 Inventory/Stock Endpoints

#### `POST /api/inventory/receive`
**Purpose:** Record incoming drugs (receive order)
```
Request:
{
  "order_no": "REQ-2026-001",
  "order_date": "2026-04-28T10:00:00",
  "expected_receive_date": "2026-05-01",
  "items": [
    {
      "drug_code": "PD-00007",
      "ordered_quantity": 100,
      "received_quantity": 100,
      "unit_price": 50.00,
      "lot_number": "CIS-2601",
      "expiry_date": "2027-12-31"
    }
  ]
}

Response (Success - 201):
{
  "status": "success",
  "message": "Receive order recorded",
  "order_no": "REQ-2026-001",
  "total_amount": 5000.00
}
```

#### `GET /api/inventory/stock-levels`
**Purpose:** Get current stock levels with alerts
```
Response (Success - 200):
{
  "status": "success",
  "data": {
    "total_items": 45,
    "low_stock_alerts": [
      {
        "drug_code": "PD-00008",
        "trade_name": "Endoxan",
        "current_stock": 15,
        "min_required": 30,
        "status": "LOW_STOCK"
      }
    ],
    "expiry_alerts": [
      {
        "drug_code": "PD-00009",
        "lot_number": "DOX-2603",
        "expiry_date": "2026-05-15",
        "days_until_expiry": 17,
        "quantity": 95,
        "status": "EXPIRING_SOON"
      }
    ]
  }
}
```

#### `POST /api/inventory/dispense`
**Purpose:** Record drug dispensing
```
Request:
{
  "prescription_no": "RX-2026-001",
  "items": [
    {
      "drug_code": "PD-00008",
      "lot_id": 2,
      "quantity_dispensed": 1
    }
  ],
  "dispensed_by": 2  // user_id
}

Response (Success - 200):
{
  "status": "success",
  "message": "Drug dispensed successfully",
  "prescription_no": "RX-2026-001"
}
```

---

### 4.4 Patient Endpoints

#### `GET /api/patients`
**Purpose:** List all patients
```
Query Parameters:
  - page: 1
  - per_page: 20
  - search: "สมชาย" (search by HN or name)

Response (Success - 200):
{
  "status": "success",
  "data": {
    "total": 250,
    "items": [
      {
        "hn": "66001234",
        "prefix": "นาย",
        "first_name": "สมชาย",
        "last_name": "ใจดี",
        "gender": "ชาย",
        "birth_date": "1987-07-25",
        "weight": 65.5,
        "allergies": "ไม่พบประวัติการแพ้ยา"
      }
    ]
  }
}
```

#### `GET /api/patients/<hn>`
**Purpose:** Get patient details and prescription history
```
Response (Success - 200):
{
  "status": "success",
  "data": {
    "patient": { /* patient info */ },
    "prescriptions": [
      {
        "prescription_no": "RX-2026-001",
        "doctor_name": "นพ. เก่งกาจ",
        "prescription_date": "2026-02-07T11:00:00",
        "status": "จ่ายยาแล้ว",
        "items": [
          {
            "drug_code": "PD-00008",
            "quantity": 1,
            "dose": "500 mg",
            "duration": "1 วัน"
          }
        ]
      }
    ]
  }
}
```

#### `POST /api/patients`
**Purpose:** Add new patient
```
Request:
{
  "hn": "66001236",
  "prefix": "นาง",
  "first_name": "สมดี",
  "last_name": "ใจดี",
  "gender": "หญิง",
  "birth_date": "1992-03-10",
  "weight": 58.0,
  "insurance_type": "ประกันสังคม",
  "allergies": "Penicillin"
}

Response (Success - 201):
{
  "status": "success",
  "message": "Patient added successfully"
}
```

---

### 4.5 Prescription Endpoints

#### `GET /api/prescriptions`
**Purpose:** List prescriptions with filtering
```
Query Parameters:
  - status: "รอจ่ายยา" | "จ่ายยาแล้ว" | "ยกเลิก"
  - date_from: "2026-04-01"
  - date_to: "2026-04-30"

Response (Success - 200):
{
  "status": "success",
  "data": {
    "total": 128,
    "items": [
      {
        "prescription_no": "RX-2026-001",
        "hn": "66001234",
        "patient_name": "สมชาย ใจดี",
        "doctor_name": "นพ. เก่งกาจ",
        "prescription_date": "2026-02-07T11:00:00",
        "status": "รอจ่ายยา",
        "items_count": 2
      }
    ]
  }
}
```

#### `GET /api/prescriptions/<prescription_no>`
**Purpose:** Get prescription details
```
Response (Success - 200):
{
  "status": "success",
  "data": {
    "prescription_no": "RX-2026-001",
    "patient": { /* patient data */ },
    "doctor_name": "นพ. เก่งกาจ",
    "items": [
      {
        "item_id": 1,
        "drug_code": "PD-00008",
        "trade_name": "Endoxan",
        "quantity": 1,
        "dose": "500 mg",
        "duration": "1 วัน",
        "dispensed_lot_id": null
      }
    ],
    "status": "รอจ่ายยา",
    "dispensed_by": null,
    "dispensed_at": null
  }
}
```

#### `POST /api/prescriptions`
**Purpose:** Create new prescription
```
Request:
{
  "prescription_no": "RX-2026-003",
  "hn": "66001234",
  "doctor_name": "นพ. เก่งกาจ",
  "insurance_used": "สิทธิ์จ่ายตรง",
  "items": [
    {
      "drug_code": "PD-00007",
      "quantity": 2,
      "dose": "50 mg",
      "duration": "5 วัน"
    }
  ]
}

Response (Success - 201):
{
  "status": "success",
  "prescription_no": "RX-2026-003"
}
```

#### `PUT /api/prescriptions/<prescription_no>/dispense`
**Purpose:** Mark prescription as dispensed
```
Request:
{
  "items": [
    {
      "item_id": 1,
      "dispensed_lot_id": 5
    }
  ]
}

Response (Success - 200):
{
  "status": "success",
  "message": "Prescription dispensed successfully",
  "dispensed_at": "2026-04-28T15:30:00"
}
```

---

### 4.6 Report & Analytics Endpoints

#### `GET /api/reports/stock-summary`
**Purpose:** Generate stock summary report
```
Query Parameters:
  - date: "2026-04-28"

Response (Success - 200):
{
  "status": "success",
  "data": {
    "report_date": "2026-04-28",
    "total_drugs": 45,
    "total_value": 125000.00,
    "high_alert_count": 8,
    "expiring_soon": 3,
    "summary_by_category": [
      {
        "category": "Alkylating agents",
        "count": 5,
        "total_stock": 200,
        "total_value": 50000.00
      }
    ]
  }
}
```

#### `GET /api/reports/expiry-analysis`
**Purpose:** Expiry analysis report
```
Response (Success - 200):
{
  "status": "success",
  "data": {
    "expiring_within_7_days": 3,
    "expiring_within_30_days": 12,
    "expired": 0,
    "details": [
      {
        "drug_code": "PD-00009",
        "lot_number": "DOX-2603",
        "expiry_date": "2026-05-15",
        "days_left": 17,
        "quantity": 95
      }
    ]
  }
}
```

#### `GET /api/reports/dispensing-audit`
**Purpose:** Audit trail for dispensed drugs
```
Query Parameters:
  - date_from: "2026-04-01"
  - date_to: "2026-04-30"

Response (Success - 200):
{
  "status": "success",
  "data": {
    "total_dispensed": 156,
    "records": [
      {
        "prescription_no": "RX-2026-001",
        "drug_name": "Endoxan",
        "quantity": 1,
        "dispensed_by": "เภสัชกร สมชาย",
        "dispensed_at": "2026-04-28T10:30:00",
        "patient": "สมชาย ใจดี"
      }
    ]
  }
}
```

---

## 5. Authentication & Authorization

### 5.1 JWT Token Implementation

**Token Structure:**
```python
import jwt
from datetime import datetime, timedelta

def create_token(user_id, username, role, expires_in=3600):
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
```

### 5.2 Role-Based Access Control (RBAC)

| Role | Permissions |
|------|---|
| **Admin** | - Manage all users<br>- Delete drugs<br>- Full system access |
| **Senior Pharmacist** | - Edit drug info<br>- Delete/Modify prescriptions<br>- Override General Pharmacist actions<br>- View audit logs |
| **General Pharmacist** | - View drugs & stock<br>- Create prescriptions<br>- Dispense drugs<br>- View own transactions |

### 5.3 Password Hashing

```python
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

---

## 6. Error Handling & Validation

### 6.1 Standard Error Response Format

```json
{
  "status": "error",
  "error_code": "INVALID_INPUT",
  "message": "ข้อมูลที่ส่งมาไม่ถูกต้อง",
  "details": {
    "field": "drug_code",
    "value": "INVALID-CODE",
    "constraint": "format"
  }
}
```

### 6.2 HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | GET succeeded |
| 201 | Created | POST succeeded, resource created |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing/invalid JWT token |
| 403 | Forbidden | User lacks permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Drug code already exists |
| 500 | Server Error | Unexpected error |

### 6.3 Input Validation

```python
from pydantic import BaseModel, Field

class DrugCreate(BaseModel):
    drug_code: str = Field(..., min_length=5, max_length=20, pattern="^PD-\\d+$")
    generic_name: str = Field(..., min_length=1, max_length=255)
    trade_name: str = Field(..., min_length=1, max_length=255)
    barcode: str = Field(..., min_length=10, max_length=50)
    unit: str = Field(..., regex="^(เม็ด|ขวด|มล.)$")
    cost_price: float = Field(..., ge=0)
    selling_price: float = Field(..., ge=0)
    total_stock: int = Field(..., ge=0)
    max_quantity: int = Field(..., gt=0)
    min_quantity: int = Field(..., ge=0)
    is_high_alert: bool = False
```

---

## 7. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Set up project structure
- [ ] Initialize FastAPI project
- [ ] Configure MySQL connection
- [ ] Create SQLAlchemy models
- [ ] Implement authentication (login/register)
- [ ] Test: Login flow, token generation

### Phase 2: Core CRUD (Week 3-4)
- [ ] Drug management endpoints (GET, POST, PUT, DELETE)
- [ ] Patient management endpoints
- [ ] Prescription creation endpoints
- [ ] Stock tracking endpoints
- [ ] Test: All CRUD operations

### Phase 3: Business Logic (Week 5-6)
- [ ] Prescription dispensing logic
- [ ] Stock level alerts
- [ ] Expiry date tracking
- [ ] High Alert Drug safeguards
- [ ] Test: Business rules validation

### Phase 4: Integration (Week 7)
- [ ] Connect Frontend to Backend APIs
- [ ] Update HTML to use fetch/AJAX
- [ ] Remove mock data from localStorage
- [ ] End-to-end testing
- [ ] UAT with pharmacists

### Phase 5: Reports & Analytics (Week 8)
- [ ] Stock summary reports
- [ ] Expiry analysis
- [ ] Dispensing audit trail
- [ ] User activity logs

### Phase 6: Security & Hardening (Week 9)
- [ ] Add HTTPS/SSL
- [ ] Rate limiting
- [ ] Input sanitization
- [ ] Security headers (CORS, CSP)
- [ ] Penetration testing

---

## 8. Code Structure & Organization

### 8.1 Recommended Project Structure

```
chemo-pharmacy-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration settings
│   ├── requirements.txt
│   │
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── drug.py
│   │   ├── prescription.py
│   │   ├── inventory.py
│   │   └── audit_log.py
│   │
│   ├── schemas/             # Pydantic schemas (validation)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── drug.py
│   │   ├── prescription.py
│   │   └── inventory.py
│   │
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── drugs.py
│   │   ├── patients.py
│   │   ├── prescriptions.py
│   │   ├── inventory.py
│   │   └── reports.py
│   │
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── drug_service.py
│   │   ├── prescription_service.py
│   │   ├── inventory_service.py
│   │   └── report_service.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py      # DB connection & session
│   │   └── base.py          # Base model
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── error_handler.py
│   │   └── logger.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── security.py      # JWT, password hashing
│       ├── validators.py
│       └── constants.py
│
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_drugs.py
│   ├── test_prescriptions.py
│   └── conftest.py
│
├── migrations/              # Alembic migrations
│   └── versions/
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── docs/
    ├── API.md
    └── SETUP.md
```

### 8.2 Example Implementation (auth.py)

```python
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserLogin, UserRegister
from app.utils.security import hash_password, verify_password, create_token
from app.db.database import get_db

router = APIRouter(prefix="/api/auth", tags=["authentication"])

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token = create_token(
        user_id=user.user_id,
        username=user.username,
        role=user.role
    )
    
    return {
        "status": "success",
        "token": token,
        "user": {
            "user_id": user.user_id,
            "fullname": user.full_name,
            "role": user.role
        }
    }

@router.post("/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user_data.username).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    
    new_user = User(
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        full_name=user_data.fullname,
        role=user_data.role
    )
    
    db.add(new_user)
    db.commit()
    
    return {
        "status": "success",
        "message": "User registered successfully",
        "user_id": new_user.user_id
    }
```

---

## 9. Security Considerations

### 9.1 Critical Security Issues to Fix

| Issue | Current State | Solution |
|-------|---------------|----------|
| Password Storage | Plaintext in localStorage | Use bcrypt hashing + JWT tokens |
| Authentication | Client-side validation only | Implement server-side JWT auth |
| HTTPS | No encryption | Use SSL/TLS certificates |
| CORS | No restrictions | Implement proper CORS policy |
| SQL Injection | Possible with string concat | Use SQLAlchemy ORM with parameterized queries |
| Rate Limiting | None | Implement rate limiting (FastAPI-Limiter) |
| Input Validation | Client-side only | Add server-side Pydantic validation |
| Audit Logging | Not implemented | Log all sensitive operations |

### 9.2 Security Headers

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Add security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

---

## 10. Testing Strategy

### 10.1 Unit Tests (Example)

```python
# tests/test_auth.py
import pytest
from app.utils.security import hash_password, verify_password

def test_password_hashing():
    password = "test_password_123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)

def test_login_success(client, db):
    # Setup
    user_data = {
        "fullname": "Test User",
        "username": "testuser",
        "password": "testpass123",
        "role": "General Pharmacist"
    }
    client.post("/api/auth/register", json=user_data)
    
    # Test
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "testpass123"
    })
    
    assert response.status_code == 200
    assert "token" in response.json()["data"]
```

### 10.2 Integration Tests

```python
# tests/test_drugs.py
def test_create_drug_success(client, auth_header):
    drug_data = {
        "drug_code": "PD-00020",
        "generic_name": "Test Drug",
        "trade_name": "Test Trade",
        "barcode": "8850000000020",
        "unit": "ขวด",
        "cost_price": 100.0,
        "selling_price": 150.0,
        "max_quantity": 500,
        "min_quantity": 50
    }
    
    response = client.post(
        "/api/drugs",
        json=drug_data,
        headers=auth_header
    )
    
    assert response.status_code == 201
    assert response.json()["drug_code"] == "PD-00020"
```

### 10.3 E2E Test Scenario

```python
def test_full_prescription_flow(client, auth_header, db):
    # 1. Create patient
    patient = create_test_patient(db)
    
    # 2. Create prescription
    rx = create_test_prescription(client, auth_header, patient.hn)
    
    # 3. Verify prescription created
    response = client.get(f"/api/prescriptions/{rx['prescription_no']}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "รอจ่ายยา"
    
    # 4. Dispense drug
    dispense = client.put(
        f"/api/prescriptions/{rx['prescription_no']}/dispense",
        json={"items": [{"item_id": 1, "dispensed_lot_id": 1}]},
        headers=auth_header
    )
    assert dispense.status_code == 200
    
    # 5. Verify stock updated
    drug_response = client.get("/api/drugs/PD-00008", headers=auth_header)
    updated_stock = drug_response.json()["data"]["total_stock"]
    assert updated_stock < 100  # Stock decreased
```

---

## 11. Deployment & DevOps

### 11.1 Docker Setup

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: chemo_management
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql

  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql+pymysql://root:rootpass@db:3306/chemo_management
      SECRET_KEY: your-secret-key-here
    depends_on:
      - db
    volumes:
      - .:/app

volumes:
  db_data:
```

---

## 12. Quick Start Commands

### 12.1 Setup Backend Locally

```bash
# 1. Clone and navigate
cd chemo-pharmacy-backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install fastapi uvicorn sqlalchemy pymysql pydantic jwt bcrypt python-multipart

# 4. Create .env file
echo "DATABASE_URL=mysql+pymysql://user:password@localhost:3306/chemo_management" > .env
echo "SECRET_KEY=your-secret-key-here" >> .env

# 5. Run migrations (if using Alembic)
alembic upgrade head

# 6. Start server
uvicorn app.main:app --reload --port 8000

# Backend will be available at: http://localhost:8000
# API documentation: http://localhost:8000/docs
```

### 12.2 Update Frontend (HTML)

```javascript
// Example: Replace localStorage login with API call

// OLD (Current):
const users = JSON.parse(localStorage.getItem('chemo_users'));
const foundUser = users.find(u => u.username === user && u.password === pass);

// NEW (With Backend):
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username, password})
});

const data = await response.json();
if (response.ok) {
  localStorage.setItem('token', data.data.token);
  localStorage.setItem('currentUser', JSON.stringify(data.data.user));
  window.location.href = 'index.html';
}
```

---

## 📝 Summary

| Component | Status | Action |
|-----------|--------|--------|
| **Database Schema** | ✅ Complete | Ready to use |
| **Frontend UI** | ✅ Complete | Needs API integration |
| **Backend API** | ❌ Not Started | **Implement Phase 1-6** |
| **Authentication** | ⚠️ Mock | **Replace with JWT** |
| **Deployment** | ⚠️ Planning | **Use Docker** |
| **Testing** | ❌ Missing | **Add unit + E2E tests** |

---

## 🚀 Next Steps

1. **Week 1-2:** Set up FastAPI project + database
2. **Week 3-4:** Implement all CRUD endpoints
3. **Week 5-6:** Add business logic + validations
4. **Week 7:** Integrate Frontend ↔ Backend
5. **Week 8+:** Reports, security hardening, UAT

---

**Document prepared by:** AI Code Analyzer  
**Last Updated:** 28 April 2026  
**Version:** 1.0 - Ready for Implementation
