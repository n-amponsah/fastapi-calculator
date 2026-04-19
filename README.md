# FastAPI Calculator

A FastAPI application with user management and a calculation engine backed by PostgreSQL.

## Docker Hub
https://hub.docker.com/r/nananjit/fastapi-calculator

## How to Run Tests Locally

### 1. Start the database
```bash
docker-compose up -d
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run all tests
```bash
pytest tests/ -v
```

### 4. Run only calculation tests
```bash
pytest tests/test_calculations_unit.py tests/test_calculations_integration.py -v
```

## What's in this project?
- `models.py` — SQLAlchemy User + Calculation database models
- `schemas.py` — Pydantic validation schemas
- `calculator.py` — Factory pattern for math operations
- `tests/` — Unit and integration tests
