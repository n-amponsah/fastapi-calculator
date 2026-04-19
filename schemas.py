from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from enum import Enum

# ✅ EXISTING: User schemas (unchanged from Module 10)
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


# 🆕 NEW: Allowed operation types (must match models.py exactly)
class CalculationTypeEnum(str, Enum):
    add      = "Add"
    subtract = "Sub"
    multiply = "Multiply"
    divide   = "Divide"


# 🆕 NEW: What we RECEIVE when someone sends a calculation
class CalculationCreate(BaseModel):
    a:    float
    b:    float
    type: CalculationTypeEnum  # must be Add, Sub, Multiply, or Divide

    @field_validator('b')
    def no_divide_by_zero(cls, v, info):
        # Only block zero if the operation is Divide
        if info.data.get('type') == CalculationTypeEnum.divide and v == 0:
            raise ValueError('Cannot divide by zero!')
        return v

    @field_validator('type', mode='before')
    def type_must_be_valid(cls, v):
        allowed = [e.value for e in CalculationTypeEnum]
        if v not in allowed:
            raise ValueError(f'Type must be one of: {allowed}')
        return v


# 🆕 NEW: What we SEND BACK after a calculation is saved
class CalculationRead(BaseModel):
    id:         int
    a:          float
    b:          float
    type:       str
    result:     float | None  # the computed answer
    created_at: datetime
    user_id:    int | None    # which user made it (optional)

    class Config:
        from_attributes = True