from fastapi.testclient import TestClient
from auth_service.main import app
from auth_service.database import get_db, SessionLocal
import pytest

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_register_user(db):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com"
    })
    assert response.status_code == 200, response.text  # Print error if test fails
    assert response.json() == {"username": "testuser", "email": "test@example.com"}

def test_login_user(db):
    response = client.post("/auth/login", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
