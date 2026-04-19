from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

# ✅ EXISTING: User model (unchanged from Module 10)
class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String(50), unique=True, nullable=False, index=True)
    email         = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at    = Column(DateTime, default=datetime.utcnow)

    # Link to calculations (one user can have many calculations)
    calculations  = relationship("Calculation", back_populates="user")


# 🆕 NEW: The allowed math operation types
class CalculationType(str, enum.Enum):
    add      = "Add"
    subtract = "Sub"
    multiply = "Multiply"
    divide   = "Divide"


# 🆕 NEW: Calculation model
class Calculation(Base):
    __tablename__ = "calculations"

    id      = Column(Integer, primary_key=True, index=True)
    a       = Column(Float, nullable=False)                      # first number
    b       = Column(Float, nullable=False)                      # second number
    type    = Column(Enum(CalculationType), nullable=False)      # which operation
    result  = Column(Float, nullable=True)                       # stored answer
    created_at = Column(DateTime, default=datetime.utcnow)

    # Link back to the User who made this calculation
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user    = relationship("User", back_populates="calculations")