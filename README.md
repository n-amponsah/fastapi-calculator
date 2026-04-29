# FastAPI Calculator

A FastAPI application with JWT authentication, user management, and a calculation engine backed by PostgreSQL.

## Docker Hub
https://hub.docker.com/r/nananjit/fastapi-calculator

## How to Run Locally
```bash
docker-compose up --build
```
Then visit:
- http://localhost:8000/register
- http://localhost:8000/login
- http://localhost:8000/docs

## How to Run Tests Locally
```bash
pip install -r requirements.txt
pytest tests/test_users.py tests/test_calculations_unit.py tests/test_calculations_integration.py tests/test_routes.py -v
```

## How to Run E2E Tests
```bash
playwright install chromium
pytest tests/test_e2e.py -v
```

## API Endpoints
- POST /users/register — Register a new user
- POST /users/login — Login and get JWT token
- GET /calculations — Browse all calculations
- GET /calculations/{id} — Read one calculation
- POST /calculations — Add a new calculation
- PUT /calculations/{id} — Edit a calculation
- DELETE /calculations/{id} — Delete a calculation

## Front-End Pages
- GET /register — Register page
- GET /login — Login page
