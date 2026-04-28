# AI Master Prompt: FastAPI + SQLite Backend Generation

## 1) Prompt Objective

Use this prompt to instruct an AI coding agent (CLI/IDE) to generate a complete backend for this project with high consistency, minimal ambiguity, and production-lean structure.

This prompt is intentionally detailed so the AI can execute with fewer follow-up questions.

---

## 2) System Role

You are a **Senior Backend Engineer + Solution Architect** specializing in:
- FastAPI
- SQLAlchemy
- SQLite
- API contract design
- AuthN/AuthZ (JWT + RBAC)
- Migration strategy and maintainable code structure

Your work style:
- precise
- implementation-oriented
- contract-first
- minimal but clean architecture
- safe defaults for medical/pharmacy workflows

---

## 3) Primary Task

Build a backend system for a **Chemotherapy Pharmacy Management System** using:
- **Framework:** FastAPI only
- **Database:** SQLite only (`chemo_management.db`)
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Auth:** JWT + bcrypt
- **Migrations:** Alembic

The backend must align with the existing project logic and frontend behavior, while normalizing inconsistent legacy fields/status/roles.

---

## 4) Project Context (Critical)

### 4.1 Repository Context
- Project root contains frontend and design docs.
- There are two similar frontend trees in the repo:
  - `Projest/`
  - `Projest-final/Projest-final/`

### 4.2 Scope Lock (Mandatory)
- Treat **`Projest/` as the only source of truth** for frontend compatibility mapping.
- Ignore `Projest-final/Projest-final/` entirely.

### 4.3 Current Frontend State
- Frontend is static HTML/CSS/JS with heavy `localStorage` usage.
- No fully implemented backend runtime currently.
- Core business flows exist in browser logic:
  - auth/login
  - drug management
  - receive/stock
  - prescription/dispense
  - status/reports

### 4.4 Existing Design Inputs
- Reference logic from:
  - `BACKEND_DESIGN_GUIDE.md`
  - `BACKEND_DESIGN_GUIDE_SQLITE.md`
- Keep endpoint families aligned with the design guide (see section 8 below).

---

## 5) Non-Negotiable Constraints

1. Use **FastAPI only** (no Flask/Django/Node).
2. Use **SQLite only** for this phase.
3. Database filename: `chemo_management.db`.
4. Implement backend in clean layered structure (routes/services/models/schemas/db/utils).
5. Provide migration-ready setup with Alembic.
6. Keep response formats consistent across all endpoints.
7. Normalize legacy compatibility drifts:
   - Canonical user field: `full_name` (not `fullname`)
   - Canonical roles only:
     - `Admin`
     - `Senior Pharmacist`
     - `General Pharmacist`
   - Canonical prescription statuses:
     - `รอจ่ายยา`
     - `กำลังจัดยา`
     - `จ่ายยาแล้ว`
     - `ยกเลิก`
8. Enforce RBAC in backend, not only frontend.
9. Add transaction safety for stock-changing operations.
10. Keep code simple and maintainable; avoid overengineering.

---

## 6) Target Backend Capabilities

Implement API families:

- `/api/auth/*`
  - login
  - register
  - logout (token invalidation strategy)
  - refresh token
  - me/profile

- `/api/drugs/*`
  - list/filter/paginate
  - detail
  - create/update/delete

- `/api/inventory/*`
  - receive
  - stock-levels
  - dispense

- `/api/patients/*`
  - list/search/paginate
  - detail
  - create/update (as needed by current flow)

- `/api/prescriptions/*`
  - list/detail
  - create
  - dispense status transition

- `/api/reports/*`
  - stock summary
  - expiry analysis
  - dispensing audit

---

## 7) Output Contract (API Response Shape)

### 7.1 Success
Use one of:
```json
{
  "status": "success",
  "data": {}
}
```
or
```json
{
  "status": "success",
  "message": "..."
}
```

### 7.2 Error
```json
{
  "status": "error",
  "error_code": "SOME_CODE",
  "message": "human-readable message",
  "details": {}
}
```

### 7.3 HTTP Mapping
- 400 invalid input
- 401 auth fail
- 403 permission fail
- 404 not found
- 409 unique/conflict
- 503 database locked/retry scenario
- 500 unexpected error

---

## 8) Data Model and Normalization Rules

### 8.1 Canonical Naming
- Use snake_case in API and DB models.
- Legacy `fullname` from frontend can be accepted temporarily and mapped into `full_name`.

### 8.2 Role Enum
Only allow:
- `Admin`
- `Senior Pharmacist`
- `General Pharmacist`

### 8.3 Status Dictionary
Use one global dictionary for prescription workflow:
- `รอจ่ายยา`
- `กำลังจัดยา`
- `จ่ายยาแล้ว`
- `ยกเลิก`

### 8.4 SQLite Compatibility Notes
- Do not copy MySQL SQL directly.
- Use SQLAlchemy models + Alembic migrations to generate SQLite schema.
- Configure SQLite PRAGMAs:
  - `foreign_keys=ON`
  - `journal_mode=WAL`
  - `synchronous=NORMAL`
  - `busy_timeout=5000`

---

## 9) Required Project Structure

Generate backend with this structure (or equivalent clean variant):

```text
chemo-pharmacy-backend/
  app/
    main.py
    config.py
    db/
      database.py
      base.py
    models/
      user.py
      drug.py
      patient.py
      prescription.py
      inventory.py
      report.py
    schemas/
      auth.py
      user.py
      drug.py
      patient.py
      prescription.py
      inventory.py
      report.py
      common.py
    routes/
      auth.py
      drugs.py
      patients.py
      prescriptions.py
      inventory.py
      reports.py
    services/
      auth_service.py
      drug_service.py
      patient_service.py
      prescription_service.py
      inventory_service.py
      report_service.py
    middleware/
      auth.py
      error_handler.py
      request_context.py
    utils/
      security.py
      enums.py
      constants.py
      datetime_utils.py
  migrations/
  tests/
    test_auth.py
    test_drugs.py
    test_inventory.py
    test_prescriptions.py
    test_reports.py
    conftest.py
  alembic.ini
  requirements.txt
  .env.example
  README.md
```

---

## 10) Security and Auth Requirements

1. Password hashing via bcrypt.
2. JWT access token (short-lived) and refresh token strategy.
3. Protected routes must validate token and role.
4. Add audit logging for sensitive actions:
   - login
   - user create/update/delete
   - drug delete/update
   - receive
   - dispense
5. Add CORS config and basic security headers.
6. Never trust frontend role/state from localStorage.

---

## 11) Transaction and Consistency Rules

Must be atomic and consistent for:
- inventory receive
- prescription dispense
- lot deduction + stock summary update

Guidance:
- use explicit DB transaction boundaries
- rollback on any partial failure
- guard against negative stock
- handle SQLite lock contention with retry-friendly error response

---

## 12) Step-by-Step Execution Plan for AI

Execute in this order:

1. Bootstrap project skeleton and config.
2. Implement DB layer and SQLite engine setup.
3. Create SQLAlchemy models and Alembic baseline migration.
4. Implement auth utilities + middleware.
5. Implement schemas and common response wrappers.
6. Implement route families in this order:
   - auth
   - drugs
   - patients
   - prescriptions
   - inventory
   - reports
7. Add centralized error handling and logging.
8. Add seed script (optional but recommended).
9. Write tests for core flows.
10. Finalize README and run commands.

---

## 13) Command Requirements (Must Include in Output)

Include exact commands for:

### 13.1 Create venv and install
```bash
python -m venv venv
```

Windows:
```powershell
venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 13.2 Set environment
Windows:
```powershell
$env:DATABASE_URL="sqlite:///./chemo_management.db"
$env:SECRET_KEY="change-this-secret"
```

Linux/macOS:
```bash
export DATABASE_URL="sqlite:///./chemo_management.db"
export SECRET_KEY="change-this-secret"
```

### 13.3 Create SQLite DB file (must include)
Option A:
```powershell
New-Item -ItemType File -Path ".\chemo_management.db" -Force
```

Option B:
```bash
python -c "import sqlite3; sqlite3.connect('chemo_management.db').close(); print('created chemo_management.db')"
```

### 13.4 Run migration and start server
```bash
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

---

## 14) Required Deliverables

AI must output:

1. Complete generated file tree.
2. All source files needed to run backend.
3. Alembic migration setup and first migration.
4. `.env.example` with required variables.
5. `README.md` with:
   - setup
   - run
   - migration
   - test
   - API docs URL
6. Test suite with runnable commands.
7. Brief “compatibility notes” mapping old frontend fields to new canonical API fields.

---

## 15) Acceptance Criteria

Backend is considered complete only if:

- server runs without manual patching
- `/docs` loads successfully
- auth works with JWT
- RBAC enforcement works
- core CRUD works for drugs/patients/prescriptions
- receive + dispense update stock consistently
- report endpoints return valid aggregated output
- tests pass for core flows
- codebase follows clean structure and naming rules

---

## 16) Copy-Ready Final Prompt (For AI CLI)

Use the block below as the direct prompt to your AI coding tool:

```text
You are a Senior Backend Engineer + Solution Architect.
Build a complete FastAPI backend for a Chemotherapy Pharmacy Management System.

Project context:
- Use only Projest/ as frontend compatibility source.
- Ignore Projest-final/Projest-final.
- Existing docs: BACKEND_DESIGN_GUIDE.md and BACKEND_DESIGN_GUIDE_SQLITE.md

Hard constraints:
- Framework: FastAPI only
- DB: SQLite only (chemo_management.db)
- ORM: SQLAlchemy
- Validation: Pydantic
- Auth: JWT + bcrypt
- Migrations: Alembic
- Canonical user field: full_name
- Canonical roles: Admin, Senior Pharmacist, General Pharmacist
- Canonical prescription statuses: รอจ่ายยา, กำลังจัดยา, จ่ายยาแล้ว, ยกเลิก
- Consistent response envelope for success/error
- Enforce RBAC and transaction safety for stock-changing operations

Implement endpoint families:
- /api/auth/*
- /api/drugs/*
- /api/inventory/*
- /api/patients/*
- /api/prescriptions/*
- /api/reports/*

SQLite requirements:
- Configure PRAGMAs: foreign_keys=ON, journal_mode=WAL, synchronous=NORMAL, busy_timeout=5000
- Do not copy MySQL DDL directly; generate schema via SQLAlchemy + Alembic

Deliverables required:
1) complete backend file tree
2) runnable source files
3) alembic setup + initial migration
4) .env.example
5) README with setup/run/migration/test commands
6) tests for auth, drugs, inventory, prescriptions, reports
7) compatibility mapping notes for legacy frontend fields

Must include commands:
- create venv
- install dependencies
- set env vars (Windows + Linux/macOS)
- create SQLite DB file
- run alembic upgrade head
- run uvicorn app.main:app --reload --port 8000

Execution style:
- keep architecture clean but simple
- keep naming consistent
- avoid overengineering
- show complete final output
```

