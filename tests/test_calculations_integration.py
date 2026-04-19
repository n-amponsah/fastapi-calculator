import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Calculation, CalculationType
from calculator import CalculationFactory

TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_save_addition_to_db(db):
    result = CalculationFactory.compute("Add", 3, 4)
    calc = Calculation(a=3, b=4, type=CalculationType.add, result=result)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    assert calc.id is not None
    assert calc.result == 7.0

def test_divide_by_zero_not_saved(db):
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        CalculationFactory.compute("Divide", 10, 0)
    count = db.query(Calculation).count()
    assert count == 0
