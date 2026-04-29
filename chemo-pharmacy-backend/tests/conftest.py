import os

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_chemo_management.db"
os.environ["SECRET_KEY"] = "test-secret"

from app.db.base import Base
from app.db.database import engine
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def auth_header(client: TestClient):
    client.post(
        "/api/auth/register",
        json={"username": "admin", "password": "1234", "full_name": "Admin User", "role": "Admin"},
    )
    res = client.post("/api/auth/login", json={"username": "admin", "password": "1234"})
    token = res.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
