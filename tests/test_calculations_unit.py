import pytest
from calculator import CalculationFactory
from schemas import CalculationCreate, CalculationTypeEnum

def test_add():
    result = CalculationFactory.compute("Add", 3, 4)
    assert result == 7.0

def test_subtract():
    result = CalculationFactory.compute("Sub", 10, 3)
    assert result == 7.0

def test_multiply():
    result = CalculationFactory.compute("Multiply", 3, 4)
    assert result == 12.0

def test_divide():
    result = CalculationFactory.compute("Divide", 10, 2)
    assert result == 5.0

def test_divide_by_zero_factory():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        CalculationFactory.compute("Divide", 10, 0)

def test_unknown_operation():
    with pytest.raises(ValueError, match="Unknown operation"):
        CalculationFactory.compute("Modulo", 10, 3)

def test_valid_calculation_create():
    calc = CalculationCreate(a=5, b=2, type="Add")
    assert calc.a == 5
    assert calc.b == 2

def test_invalid_type_rejected():
    with pytest.raises(Exception):
        CalculationCreate(a=5, b=2, type="Modulo")

def test_divide_by_zero_schema():
    with pytest.raises(E
cat > ~/Desktop/fastapi-calculator/tests/test_calculations_integration.py << 'EOF'
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

def test_save_subtraction_to_db(db):
    result = CalculationFactory.compute("Sub", 10, 3)
    calc = Calculation(a=10, b=3, type=CalculationType.subtract, result=result)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    assert calc.result == 7.0

def test_save_multiply_to_db(db):
    result = CalculationFactory.compute("Multiply", 3, 4)
    calc = Calculation(a=3, b=4, type=CalculationType.multiply, result=result)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    assert calc.result == 12.0

def test_save_divide_to_db(db):
    result = CalculationFactory.compute("Divide", 10, 2)
    calc = Calculation(a=10, b=2, type=CalculationType.divide, result=result)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    assert calc.result == 5.0

def test_divide_by_zero_not_saved(db):
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        CalculationFactory.compute("Divide", 10, 0)
    count = db.query(Calculation).count()
    assert count == 0
