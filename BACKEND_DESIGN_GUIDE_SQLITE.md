# Backend Design Guide (FastAPI + SQLite, CLI AI Prompt Edition)
## ระบบจัดการยาเคมีบำบัดโรงพยาบาล (Chemotherapy Pharmacy Management System)

**Document Version:** 2.1  
**Date:** 29 April 2026  
**Author:** AI Code Analyzer  
**Goal:** ใช้งานให้ "ง่ายที่สุด" ด้วย FastAPI ต่อ SQLite ตรง

---

## Table of Contents
1. [Executive Decision](#1-executive-decision)
2. [Scope Lock (Use Projest Only)](#2-scope-lock-use-projest-only)
3. [Architecture (Simple First)](#3-architecture-simple-first)
4. [How to Create SQLite Database File](#4-how-to-create-sqlite-database-file)
5. [Backend Setup (FastAPI + SQLite)](#5-backend-setup-fastapi--sqlite)
6. [Project Structure](#6-project-structure)
7. [Prompt for AI in CLI (Ready to Use)](#7-prompt-for-ai-in-cli-ready-to-use)
8. [Implementation Rules for AI](#8-implementation-rules-for-ai)
9. [Points That Old Structure Cannot Reuse Directly](#9-points-that-old-structure-cannot-reuse-directly)
10. [API Logic Mapping from Existing Design](#10-api-logic-mapping-from-existing-design)
11. [SQLite Operational Notes](#11-sqlite-operational-notes)
12. [Acceptance Checklist](#12-acceptance-checklist)
13. [Future Migration Path](#13-future-migration-path)

---

## 1. Executive Decision

### สรุปคำตอบสั้น
**ทำได้** และเป็นแนวทางที่ตรงกับเงื่อนไขหน้างานที่สุด:
- ใช้ `FastAPI` เป็น backend framework
- ต่อฐานข้อมูล `SQLite` โดยตรง (ไฟล์ `.db`)
- ใช้ logic เดิมตาม `BACKEND_DESIGN_GUIDE.md` ได้เกือบทั้งหมด

### เหตุผลที่เหมาะ
- setup เร็ว
- deploy ง่าย (ไม่ต้องยก MySQL server)
- เหมาะกับงานที่ต้อง "รื้อหลังบ้านใหม่" ภายหลัง

---

## 2. Scope Lock (Use Projest Only)

เพื่อกันความสับสนจากโค้ดที่ซ้ำกัน ให้ล็อกขอบเขต implementation ชัดเจนดังนี้:

- ใช้เฉพาะโฟลเดอร์ `Projest/` เป็น source of truth
- ไม่ใช้และไม่อ้างอิง `Projest-final/Projest-final/` ในการออกแบบ backend รอบนี้
- เอกสารนี้อิง field/flow จาก `Projest/` เท่านั้น

ผลลัพธ์ที่ต้องการ:
- ลดความเสี่ยงแก้สองชุดแล้วพฤติกรรมไม่ตรงกัน
- ให้ API contract มีแหล่งอ้างอิงเดียว

---

## 3. Architecture (Simple First)

```
Frontend (HTML/CSS/JS)
  -> Fetch API
FastAPI
  -> Routers
  -> Services (Business Logic)
  -> SQLAlchemy ORM
SQLite (chemo_management.db)
```

หลักการ: ใช้ API contract เดิม, เปลี่ยนเฉพาะ persistence layer เป็น SQLite

---

## 4. How to Create SQLite Database File

## 4.1 วิธีที่ง่ายที่สุด (สร้างไฟล์เปล่า)

### Windows PowerShell
```powershell
New-Item -ItemType File -Path ".\chemo_management.db" -Force
```

### Bash
```bash
touch chemo_management.db
```

> วิธีนี้สร้างไฟล์ได้ทันที แต่ยังไม่มีตาราง

## 4.2 วิธีแนะนำ (สร้างไฟล์ + schema ผ่าน Python)
```bash
python - <<'PY'
import sqlite3
conn = sqlite3.connect("chemo_management.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  full_name TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'General Pharmacist',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()
conn.close()
print("created chemo_management.db with initial schema")
PY
```

## 4.3 วิธี production-friendly (ผ่าน migration)
```bash
alembic upgrade head
```

> ถ้าใช้ Alembic ถูกต้อง ไฟล์ `chemo_management.db` จะถูกสร้างอัตโนมัติพร้อม schema ล่าสุด

---

## 5. Backend Setup (FastAPI + SQLite)

## 5.1 Install Dependencies
```bash
pip install fastapi uvicorn sqlalchemy alembic pydantic pyjwt bcrypt python-multipart
```

## 5.2 Environment Variables

### Windows PowerShell
```powershell
$env:DATABASE_URL="sqlite:///./chemo_management.db"
$env:SECRET_KEY="change-this-secret"
```

### Bash
```bash
export DATABASE_URL="sqlite:///./chemo_management.db"
export SECRET_KEY="change-this-secret"
```

## 5.3 SQLAlchemy Connection
```python
# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./chemo_management.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

## 5.4 SQLite PRAGMA ที่ต้องเปิด
```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA busy_timeout = 5000;
```

---

## 6. Project Structure

```
chemo-pharmacy-backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db/
│   │   ├── database.py
│   │   └── base.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   ├── middleware/
│   └── utils/
├── migrations/
├── tests/
└── requirements.txt
```

---

## 7. Prompt for AI in CLI (Ready to Use)

คัดลอก Prompt นี้ไปใช้กับ AI ที่ฝังใน CLI ได้เลย

```text
You are a senior FastAPI backend engineer.
Build a production-lean but simple backend for a Chemotherapy Pharmacy Management System.

Hard requirements:
1) Use FastAPI only as backend framework.
2) Use SQLite only as database (file: chemo_management.db), direct via SQLAlchemy.
3) Use only this frontend source for compatibility mapping: Projest/.
   Ignore Projest-final/Projest-final completely in this implementation.
4) Keep API logic aligned with existing design guide:
   - /api/auth/*
   - /api/drugs/*
   - /api/inventory/*
   - /api/patients/*
   - /api/prescriptions/*
   - /api/reports/*
5) Keep response format consistent:
   - success: { "status": "success", "data": ... } or with "message"
   - error: { "status": "error", "error_code": "...", "message": "...", "details": ... }
6) Implement JWT auth, bcrypt password hashing, and RBAC roles:
   - Admin
   - Senior Pharmacist
   - General Pharmacist
7) Use SQLAlchemy models + Pydantic schemas + service layer.
8) Add migration support with Alembic.
9) Add startup SQLite PRAGMA setup:
   - foreign_keys=ON
   - journal_mode=WAL
   - synchronous=NORMAL
   - busy_timeout=5000
10) Add minimal tests with pytest:
   - auth login/register
   - drug create/list
   - prescription create/dispense flow
11) Include run instructions for Windows and Linux/macOS.
12) Normalize compatibility drifts:
   - API uses full_name (not fullname)
   - Roles must be exactly: Admin, Senior Pharmacist, General Pharmacist
   - Keep one status dictionary for prescription workflow

Implementation style:
- Keep code simple and readable.
- Prefer explicit transaction handling for stock receive/dispense.
- Avoid overengineering.
- Keep files small and focused.

Important:
- Create the SQLite DB file command in docs.
- Ensure the project can run locally with:
  uvicorn app.main:app --reload --port 8000

Deliverables:
1) Full project structure and source files.
2) .env.example
3) alembic setup
4) README with setup and commands
5) API docs notes and test commands
```

## 7.1 Prompt เฟสย่อย (ถ้าต้องการสั่งทีละงาน)

### Prompt A: Bootstrap Project
```text
Create a FastAPI project with SQLite (chemo_management.db), SQLAlchemy, Alembic, and JWT utilities.
Do not implement all endpoints yet.
Only scaffold folders, db setup, config, auth utilities, and health check endpoint.
Return file tree and run commands.
```

### Prompt B: Core APIs
```text
Implement auth, drugs, patients, and prescriptions endpoints in FastAPI using existing design logic.
Use SQLite through SQLAlchemy and service layer.
Add request/response schemas and consistent error format.
```

### Prompt C: Inventory + Reports + Tests
```text
Add inventory receive/dispense logic, report endpoints, and pytest coverage for key flows.
Ensure stock transaction consistency and include lock-safe behavior for SQLite.
```

---

## 8. Implementation Rules for AI

- ห้ามเปลี่ยน business terms หลัก
- ชื่อฟิลด์ต้องคงที่ตาม API contract
- transaction ที่ตัด stock ต้อง atomic
- ใช้ `Projest/` เป็นแหล่งอ้างอิงเดียว
- ฝั่ง API ใช้ `full_name` เป็นมาตรฐานเดียว และ map จาก `fullname` ได้เฉพาะช่วง migration
- role enum ต้องตายตัว: `Admin`, `Senior Pharmacist`, `General Pharmacist`
- status dictionary ต้องใช้ชุดเดียวทุก endpoint/DB/UI
- error mapping ต้องชัดเจน:
  - unique conflict -> 409
  - auth fail -> 401
  - permission fail -> 403
  - not found -> 404
  - db lock timeout -> 503
- ทุก endpoint ต้องมี validation

---

## 9. Points That Old Structure Cannot Reuse Directly

หัวข้อนี้คือจุดที่โครงเดิมใช้ตรงๆ ไม่ได้ และต้องแก้ก่อนเริ่ม implement backend

### 9.1 Folder Scope ซ้ำกัน
- ปัญหา: มีทั้ง `Projest/` และ `Projest-final/Projest-final/`
- วิธีแก้: ล็อกใช้เฉพาะ `Projest/` ในรอบนี้

### 9.2 Role ไม่ตรงกัน
- ปัญหาเดิม: บางที่ใช้ `Pharmacist/Staff` แต่หน้าเว็บใช้งานจริง `Senior Pharmacist/General Pharmacist`
- วิธีแก้: มาตรฐานเดียวคือ:
  - `Admin`
  - `Senior Pharmacist`
  - `General Pharmacist`

### 9.3 ชื่อฟิลด์ผู้ใช้ไม่ตรง (`fullname` vs `full_name`)
- ปัญหาเดิม: ฝั่งหน้าเว็บใช้ `fullname` แต่ schema/model ควรใช้ snake_case
- วิธีแก้:
  - API/DB มาตรฐาน: `full_name`
  - ตอน migration รับ `fullname` ได้ชั่วคราวและ map เข้า `full_name`

### 9.4 Endpoint family บางเอกสารไม่ตรงกัน
- ปัญหาเดิม: บางแผนใช้ `/api/receive` และ `/api/dispense` แยก
- วิธีแก้: ยึดชุดหลักเดียว:
  - `/api/inventory/receive`
  - `/api/inventory/stock-levels`
  - `/api/inventory/dispense`

### 9.5 Status Dictionary ไม่คงที่
- ปัญหาเดิม: มีคำสถานะใกล้เคียงแต่ไม่เหมือนกันในบางหน้า
- วิธีแก้: นิยามกลางสำหรับ prescription:
  - `รอจ่ายยา`
  - `กำลังจัดยา`
  - `จ่ายยาแล้ว`
  - `ยกเลิก`

### 9.6 MySQL SQL เดิมใช้กับ SQLite ไม่ได้ตรงๆ
- ปัญหาเดิม: schema เก่าเป็น MySQL syntax (`ENUM`, `CREATE DATABASE`, `USE`)
- วิธีแก้:
  - ใช้ Alembic + SQLAlchemy models เพื่อ generate SQLite schema
  - หลีกเลี่ยง copy MySQL DDL มารัน SQLite ตรงๆ

---

## 10. API Logic Mapping from Existing Design

- Auth: login/register/logout/refresh
- Drugs: list/detail/create/update/delete
- Inventory: receive/stock-levels/dispense
- Patients: list/detail/create
- Prescriptions: list/detail/create/dispense
- Reports: stock-summary/expiry-analysis/dispensing-audit

หมายเหตุ: ให้ยึด logic เดิมจาก `BACKEND_DESIGN_GUIDE.md` แต่ implement บน SQLite

---

## 11. SQLite Operational Notes

### ข้อดี
- setup ง่าย
- ย้ายเครื่องง่าย
- เหมาะกับ pilot และทีมเล็ก

### ข้อควรระวัง
- concurrent write สูงอาจ lock ง่าย
- ไม่เหมาะกับ multi-instance write พร้อมกันหนักๆ

### วิธีลด lock
- transaction สั้น
- commit ทันทีเมื่อเสร็จ
- เปิด WAL และ busy_timeout

---

## 12. Acceptance Checklist

- [ ] รัน server ได้ด้วย `uvicorn`
- [ ] สร้างไฟล์ `chemo_management.db` ได้
- [ ] migration ทำงาน
- [ ] login ได้ JWT
- [ ] endpoint หลักตอบตาม contract
- [ ] stock ลดจริงตอน dispense
- [ ] test หลักผ่าน
- [ ] ใช้เฉพาะ `Projest/` เป็น frontend reference
- [ ] role/field/status normalize ตามข้อ 9 ครบ

---

## 13. Future Migration Path

เมื่อระบบโตและต้อง scale:
- เปลี่ยน `DATABASE_URL` ไป MySQL/PostgreSQL
- คง route/service/schema เดิม
- ปรับ migration และ tuning query/index เพิ่ม

สรุป: เริ่มด้วย FastAPI + SQLite ได้เร็วที่สุด และยังเปิดทางย้าย DB engine ภายหลังโดยกระทบ logic น้อยที่สุด
