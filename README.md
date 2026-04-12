# FastAPI Calculator with Secure User Model

A FastAPI application with a secure user model, password hashing, Pydantic validation, database testing, and a full CI/CD pipeline with GitHub Actions and Docker Hub.

## Features

- FastAPI calculator with addition, subtraction, multiplication, division, power, and modulo
- Secure user model using SQLAlchemy with hashed passwords
- Pydantic schemas for data validation
- Password hashing using bcrypt
- Unit and integration tests
- CI/CD pipeline with GitHub Actions
- Docker image pushed to Docker Hub automatically

## How to Run Tests Locally

### Step 1: Make sure PostgreSQL is running
```bash
docker-compose up -d db
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the tests
```bash
pytest tests/test_users.py -v
```

You should see all tests passing!

## How to Run the App Locally

```bash
docker-compose up --build
```

Then open your browser and go to:
```
http://localhost:8000
```

## Docker Hub Repository

The Docker image is available on Docker Hub:

🐳 [hub.docker.com/r/nananjit/fastapi-calculator](https://hub.docker.com/r/nananjit/fastapi-calculator)

To pull and run the image:
```bash
docker pull nananjit/fastapi-calculator
docker run -p 8000:8000 nananjit/fastapi-calculator
```

## Project Structure

- `main.py` - FastAPI app and calculator UI
- `models.py` - SQLAlchemy User model
- `schemas.py` - Pydantic schemas (UserCreate, UserRead)
- `hashing.py` - Password hashing and verification
- `database.py` - Database connection and session
- `operations.py` - Math functions with logging
- `tests/test_users.py` - Unit and integration tests
- `.github/workflows/ci.yml` - GitHub Actions CI/CD pipeline
- `docker-compose.yml` - Docker Compose configuration

## CI/CD Pipeline

Every time code is pushed to the main branch:
1. GitHub Actions runs all tests automatically
2. If tests pass, the Docker image is built and pushed to Docker Hub
