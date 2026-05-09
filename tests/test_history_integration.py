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

def test_stats_empty():
    response = client.get("/stats")
    assert response.status_code == 200
    assert response.json()["total"] == 0

def test_stats_after_adding():
    client.post("/calculations", json={"a": 3, "b": 4, "type": "Add"})
    client.post("/calculations", json={"a": 10, "b": 2, "type": "Multiply"})
    response = client.get("/stats")
    assert response.status_code == 200
    assert response.json()["total"] == 2

def test_stats_most_used():
    client.post("/calculations", json={"a": 1, "b": 2, "type": "Add"})
    client.post("/calculations", json={"a": 3, "b": 4, "type": "Add"})
    client.post("/calculations", json={"a": 5, "b": 2, "type": "Multiply"})
    response = client.get("/stats")
    assert response.json()["most_used"] == "Add"

def test_stats_average_result():
    client.post("/calculations", json={"a": 2, "b": 2, "type": "Add"})
    client.post("/calculations", json={"a": 4, "b": 4, "type": "Add"})
    response = client.get("/stats")
    assert response.json()["average_result"] == 6.0

def test_history_page_loads():
    response = client.get("/history")
    assert response.status_code == 200

def test_stats_recent_calculations():
    client.post("/calculations", json={"a": 1, "b": 1, "type": "Add"})
    response = client.get("/stats")
    assert len(response.json()["recent"]) == 1
