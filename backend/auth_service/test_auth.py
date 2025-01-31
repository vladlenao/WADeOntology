import pytest
from fastapi.testclient import TestClient
from main import app
from src.database.connection import Base, engine

# Recreate database tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_register_new_user():
    """Test user registration with a new unique user"""
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"


def test_register_duplicate_user():
    """Test registering a user with an existing email"""
    response = client.post("/auth/register", json={
        "username": "duplicateuser",
        "password": "somepassword",
        "email": "test@example.com"
    })
    assert response.status_code == 400
    assert "Email already exists" in str(response.json()["detail"])


def test_login_user():
    """Test successful user login"""
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword",
        "email": ""
    })
    print (response.json())
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post("/auth/login", json={
        "username": "nonexistent",
        "password": "wrongpassword",
        "email": ""
    })
    assert response.status_code == 401
    assert "Invalid credentials" in str(response.json()["detail"])


def test_read_users_me():
    """Test fetching user details after login"""
    # Login first to get access token
    login_response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword",
        "email": ""
    })
    access_token = login_response.json()["access_token"]

    # Get user details
    response = client.get("/auth/users/me", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_logout_user():
    """Test user logout"""
    # Login first to get access token
    login_response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword",
        "email": ""
    })
    print(login_response.json())
    access_token = login_response.json()["access_token"]

    # Logout
    response = client.post("/auth/logout", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Logged out successfully"}