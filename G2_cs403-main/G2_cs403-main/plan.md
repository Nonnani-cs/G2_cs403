Project plan: Backend for Hospital Medication Stock Management System (Flask + SQLite)

Problem
- Frontend is static with mocked data. Multiple Python scrapers/editors mutate HTML (fragile).
- No real backend, no persistent DB, no API, no auth/validation.

Goal
Build a minimal but production-structured backend (MVP) and integrate it with the existing frontend so pages call APIs instead of using mock data.

Approach
- Stack: Flask + SQLAlchemy + Alembic (migrations) + SQLite for local/dev.
- Validate requests with Pydantic/Marshmallow; return JSON APIs consumed by frontend fetch().
- Keep frontend changes incremental: replace mock data with API calls, preserve UI structure.

Initial DB schema (minimal)
- drugs(id, code, name, category, unit, price, high_alert)
- lots(id, drug_id, lot_no, qty, expiry_date, location)
- inventory(drug_id, lot_id, qty)
- transactions(id, type(receive|dispense), created_by, created_at)
- transaction_lines(id, transaction_id, drug_id, lot_id, qty, price)
- users(id, username, password_hash, role)

MVP API endpoints
- GET /api/drugs?filter=&page=&per_page=
- GET /api/drugs/{code}
- GET /api/lots?drug_code=
- POST /api/receive  (record receive transaction)
- POST /api/dispense (record dispense transaction)
- POST /api/auth/login (simple mock JWT initially)

Todos
1. Create Flask project skeleton, virtualenv, run script, README update.
2. Implement models with SQLAlchemy and add Alembic migrations.
3. Seed minimal data and provide a small seeder script.
4. Implement MVP APIs with input validation and basic error handling.
5. Add simple auth (JWT) and protected endpoints for write actions.
6. Replace frontend mock data fetches incrementally (receive/manage/dispense pages).
7. Add unit tests for APIs and a basic integration test.
8. Document run/dev steps and backup policy for HTML-edit scripts.

Next step (awaiting your confirmation)
- After you confirm, scaffold the Flask project and create initial models + migrations.

"วิเคราะห์การทำงานของระบบเรียบร้อย พร้อมรับคำสั่งพัฒนาต่อแล้วครับ (หากมีข้อสงสัยในคำสั่งถัดไป ผมจะสอบถามก่อนลงมือทำเสมอ)"