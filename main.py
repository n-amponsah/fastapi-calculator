from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base, User, Calculation, CalculationType
from schemas import UserCreate, UserRead, CalculationCreate, CalculationRead
from hashing import hash_password, verify_password
from calculator import CalculationFactory
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# JWT Settings
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# -------------------------------------------------------
# Front-End Pages
# -------------------------------------------------------

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# -------------------------------------------------------
# User Endpoints
# -------------------------------------------------------

@app.post("/users/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/users/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

# -------------------------------------------------------
# Calculation Endpoints (BREAD)
# -------------------------------------------------------

@app.get("/calculations", response_model=list[CalculationRead])
def browse(db: Session = Depends(get_db)):
    return db.query(Calculation).all()

@app.get("/calculations/{id}", response_model=CalculationRead)
def read(id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc

@app.post("/calculations", response_model=CalculationRead)
def add(calc: CalculationCreate, db: Session = Depends(get_db)):
    try:
        result = CalculationFactory.compute(calc.type.value, calc.a, calc.b)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    new_calc = Calculation(
        a=calc.a,
        b=calc.b,
        type=CalculationType[calc.type.name],
        result=result
    )
    db.add(new_calc)
    db.commit()
    db.refresh(new_calc)
    return new_calc

@app.put("/calculations/{id}", response_model=CalculationRead)
def edit(id: int, calc: CalculationCreate, db: Session = Depends(get_db)):
    db_calc = db.query(Calculation).filter(Calculation.id == id).first()
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    result = CalculationFactory.compute(calc.type.value, calc.a, calc.b)
    db_calc.a = calc.a
    db_calc.b = calc.b
    db_calc.type = CalculationType[calc.type.name]
    db_calc.result = result
    db.commit()
    db.refresh(db_calc)
    return db_calc

@app.delete("/calculations/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    db_calc = db.query(Calculation).filter(Calculation.id == id).first()
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(db_calc)
    db.commit()
    return {"message": "Calculation deleted successfully"}
