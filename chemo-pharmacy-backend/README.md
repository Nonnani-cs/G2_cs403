# Chemotherapy Pharmacy Backend (FastAPI + SQLite)

This backend is aligned to `Projest/` frontend behavior and normalizes key legacy drifts.

## File Tree

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
  alembic.ini
  requirements.txt
  .env.example
  README.md
```

## Setup

### Create venv and install

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

### Set environment

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

### Create SQLite DB file

Option A:
```powershell
New-Item -ItemType File -Path ".\chemo_management.db" -Force
```

Option B:
```bash
python -c "import sqlite3; sqlite3.connect('chemo_management.db').close(); print('created chemo_management.db')"
```

### Run migration and start server

```bash
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Docs URL: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Tests

```bash
pytest -q
```

## Compatibility Notes

- Accepts both `full_name` and legacy `fullname` at registration; stores only `full_name`.
- Enforces canonical roles: `Admin`, `Senior Pharmacist`, `General Pharmacist`.
- Enforces canonical prescription statuses: `รอจ่ายยา`, `กำลังจัดยา`, `จ่ายยาแล้ว`, `ยกเลิก`.
