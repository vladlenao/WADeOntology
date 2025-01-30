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
        "username": "testuser1",
        "password": "testpassword",
        "email": "test@example.com"
    })
    assert response.status_code == 200, print(response.text)  # Print error if test fails
    assert response.json() == {"username": "testuser", "email": "test@example.com"}

def test_login_user(db):
    response = client.post("/auth/login", json={"username": "testuser", "password": "testpassword", "email": ""})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_read_users_me(db):
    response_login = client.post("/auth/login", json={"username": "testuser", "password": "testpassword", "email": ""})
    response = client.get("/auth/users/me", headers={"Authorization": f"Bearer {response_login.json()['access_token']}"})
    assert response.status_code == 200
    assert response.json() == {"username": "testuser", "email": "test@example.com"}

def test_logout_user(db):
    response_login = client.post("/auth/login", json={"username": "testuser", "password": "testpassword", "email": ""})
    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {response_login.json()['access_token']}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Logged out successfully"}
