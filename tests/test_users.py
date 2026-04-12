import pytest
from hashing import hash_password, verify_password
from schemas import UserCreate
from pydantic import ValidationError

# ─── Unit Tests ───────────────────────────────────────────────

def test_hash_password_returns_string():
    hashed = hash_password("mypassword")
    assert isinstance(hashed, str)

def test_hash_password_is_not_plaintext():
    hashed = hash_password("mypassword")
    assert hashed != "mypassword"

def test_verify_password_correct():
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed) is True

def test_verify_password_wrong():
    hashed = hash_password("mypassword")
    assert verify_password("wrongpassword", hashed) is False

def test_user_create_valid():
    user = UserCreate(username="nana", email="nana@example.com", password="secret123")
    assert user.username == "nana"
    assert user.email == "nana@example.com"

def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="nana", email="not-an-email", password="secret123")

def test_user_create_short_username():
    with pytest.raises(ValidationError):
        UserCreate(username="ab", email="nana@example.com", password="secret123")

def test_user_create_short_password():
    with pytest.raises(ValidationError):
        UserCreate(username="nana", email="nana@example.com", password="123")

# ─── Integration Tests ────────────────────────────────────────

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User

TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/fastapi_db"
)

@pytest.fixture(scope="module")
def db():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user_in_db(db):
    hashed = hash_password("testpassword")
    user = User(username="testuser", email="test@example.com", password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    assert user.id is not None
    assert user.username == "testuser"

def test_duplicate_username_raises_error(db):
    from sqlalchemy.exc import IntegrityError
    hashed = hash_password("testpassword")
    user = User(username="testuser", email="another@example.com", password_hash=hashed)
    db.add(user)
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()

def test_duplicate_email_raises_error(db):
    from sqlalchemy.exc import IntegrityError
    hashed = hash_password("testpassword")
    user = User(username="newuser", email="test@example.com", password_hash=hashed)
    db.add(user)
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()
