from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    def username_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Username cannot be empty')
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        return v

    @field_validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
