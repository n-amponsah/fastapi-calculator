import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db
from models import Base

TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_register_user():
    response = client.post("/users/register", json={"username": "testuser", "email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_register_duplicate_username():
    client.post("/users/register", json={"username": "testuser", "email": "test@example.com", "password": "password123"})
    response = client.post("/users/register", json={"username": "testuser", "email": "test2@example.com", "password": "password123"})
    assert response.status_code == 400

def test_login_success():
    client.post("/users/register", json={"username": "testuser", "email": "test@example.com", "password": "password123"})
    response = client.post("/users/login", json={"username": "testuser", "email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    client.post("/users/register", json={"username": "testuser", "email": "test@example.com", "password": "password123"})
    response = client.post("/users/login", json={"username": "testuser", "email": "test@example.com", "password": "wrongpassword"})
    assert response.status_code == 401

def test_add_calculation():
    response = client.post("/calculations", json={"a": 3, "b": 4, "type": "Add"})
    assert response.status_code == 200
    assert response.json()["result"] == 7.0

def test_browse_calculations():
    client.post("/calculations", json={"a": 3, "b": 4, "type": "Add"})
    response = client.get("/calculations")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_read_calculation():
    post = client.post("/calculations", json={"a": 3, "b": 4, "type": "Add"})
    calc_id = post.json()["id"]
    response = client.get(f"/calculations/{calc_id}")
    assert response.status_code == 200
    assert response.json()["result"] == 7.0

def test_edit_calculation():
    post = client.post("/calculations", json={"a": 3, "b": 4, "type": "Add"})
    calc_id = post.json()["id"]
    response = client.put(f"/calculations/{calc_id}", json={"a": 10, "b": 2, "type": "Multiply"})
    assert response.status_code == 200
    assert response.json()["result"] == 20.0

def test_delete_calculation():
    post = client.post("/calculations", json={"a": 3, "b": 4, "type": "Add"})
    calc_id = post.json()["id"]
    response = client.delete(f"/calculations/{calc_id}")
    assert response.status_code == 200

def test_read_nonexistent_calculation():
    response = client.get("/calculations/999")
    assert response.status_code == 404

