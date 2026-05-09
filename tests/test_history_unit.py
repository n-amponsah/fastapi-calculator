import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import CalculationFactory

def test_history_add_operation():
    result = CalculationFactory.compute("Add", 10, 5)
    assert result == 15.0

def test_history_subtract_operation():
    result = CalculationFactory.compute("Sub", 10, 5)
    assert result == 5.0

def test_history_multiply_operation():
    result = CalculationFactory.compute("Multiply", 10, 5)
    assert result == 50.0

def test_history_divide_operation():
    result = CalculationFactory.compute("Divide", 10, 5)
    assert result == 2.0

def test_history_divide_by_zero():
    import pytest
    with pytest.raises(ValueError):
        CalculationFactory.compute("Divide", 10, 0)
