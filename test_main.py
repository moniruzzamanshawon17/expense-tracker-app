import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Create fresh tables before the tests, delete them afterwards."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()          
    try:
        if os.path.exists("test.db"):
            os.remove("test.db")
    except PermissionError:
        pass                  


@pytest.fixture(scope="module")
def headers():
    """Register a user, log in, and return the Authorization header."""
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        },
    )

    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


#Test 1: Create 

def test_create_transaction(headers):
    response = client.post(
        "/transactions",
        json={
            "title": "Lunch",
            "amount": 250.0,
            "type": "expense",
            "category": "Food",
            "date": "2026-01-15",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Lunch"
    assert data["amount"] == 250.0
    assert data["id"] == 1


# Test 2: Get all 

def test_get_all_transactions(headers):
    response = client.get("/transactions", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


# Test 3: Get one 

def test_get_single_transaction(headers):
    response = client.get("/transactions/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Lunch"

    missing = client.get("/transactions/999", headers=headers)
    assert missing.status_code == 404


# Test 4: Update 

def test_update_transaction(headers):
    response = client.put(
        "/transactions/1",
        json={
            "title": "Dinner",
            "amount": 500.0,
            "type": "expense",
            "category": "Food",
            "date": "2026-01-16",
        },
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Dinner"
    assert response.json()["amount"] == 500.0


# Test 5: Delete 

def test_delete_transaction(headers):
    response = client.delete("/transactions/1", headers=headers)
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

    
    check = client.get("/transactions/1", headers=headers)
    assert check.status_code == 404