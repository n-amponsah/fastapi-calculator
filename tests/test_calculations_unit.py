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
    with pytest.raises(ValueError):
        CalculationFactory.compute("Divide", 10, 0)

def test_unknown_operation():
    with pytest.raises(ValueError):
        CalculationFactory.compute("Modulo", 10, 3)

def test_valid_calculation_create():
    calc = CalculationCreate(a=5, b=2, type="Add")
    assert calc.a == 5
    assert calc.b == 2

def test_invalid_type_rejected():
    with pytest.raises(Exception):
        CalculationCreate(a=5, b=2, type="Modulo")

def test_subtract_by_zero_allowed():
    calc = CalculationCreate(a=10, b=0, type="Sub")
    assert calc.b == 0
