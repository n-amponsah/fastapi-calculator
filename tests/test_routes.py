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

# -------------------------------------------------------
# User Tests
# -------------------------------------------------------

def test_register_user():
    response = client.post("/users/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_register_duplicate_username():
    client.post("/users/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post("/
ls ~/Desktop/fastapi-calculator/tests/
cat > ~/Desktop/fastapi-calculator/.github/workflows/ci.yml << 'MYEOF'
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: fastapi_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Create test database
        env:
          PGPASSWORD: postgres
        run: |
          psql -h localhost -U postgres -c "CREATE DATABASE test_db;"

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/fastapi_db
        run: |
          export PYTHONPATH=$PYTHONPATH:$(pwd)
          pytest tests/test_users.py tests/test_calculations_unit.py tests/test_calculations_integration.py tests/test_routes.py -v

  deploy:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Log in to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build Docker image
        run: docker build -t nananjit/fastapi-calculator .

      - name: Push Docker image
        run: docker push nananjit/fastapi-calculator
