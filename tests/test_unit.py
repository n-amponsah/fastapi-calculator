import pytest
from operations import add, subtract, multiply, divide, power, modulo


class TestAdd:
    def test_positive_numbers(self):
        assert add(3, 4) == 7

    def test_negative_numbers(self):
        assert add(-2, -5) == -7

    def test_mixed_signs(self):
        assert add(-3, 10) == 7

    def test_floats(self):
        assert add(1.5, 2.5) == pytest.approx(4.0)

    def test_zero(self):
        assert add(0, 0) == 0

    def test_large_numbers(self):
        assert add(1_000_000, 2_000_000) == 3_000_000


class TestSubtract:
    def test_basic(self):
        assert subtract(10, 3) == 7

    def test_negative_result(self):
        assert subtract(3, 10) == -7

    def test_zero(self):
        assert subtract(5, 5) == 0

    def test_floats(self):
        assert subtract(5.5, 2.2) == pytest.approx(3.3)

    def test_negative_operands(self):
        assert subtract(-4, -6) == 2


class TestMultiply:
    def test_positive(self):
        assert multiply(3, 4) == 12

    def test_by_zero(self):
        assert multiply(99, 0) == 0

    def test_negative(self):
        assert multiply(-3, 4) == -12

    def test_two_negatives(self):
        assert multiply(-3, -4) == 12

    def test_floats(self):
        assert multiply(2.5, 4.0) == pytest.approx(10.0)


class TestDivide:
    def test_basic(self):
        assert divide(10, 2) == 5.0

    def test_float_result(self):
        assert divide(7, 2) == pytest.approx(3.5)

    def test_negative_dividend(self):
        assert divide(-10, 2) == -5.0

    def test_divide_by_zero_raises(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)

    def test_zero_dividend(self):
        assert divide(0, 5) == 0.0


class TestPower:
    def test_basic(self):
        assert power(2, 3) == 8

    def test_zero_exponent(self):
        assert power(5, 0) == 1

    def test_one_exponent(self):
        assert power(7, 1) == 7

    def test_float_exponent(self):
        assert power(4, 0.5) == pytest.approx(2.0)


class TestModulo:
    def test_basic(self):
        assert modulo(10, 3) == 1

    def test_exact_division(self):
        assert modulo(9, 3) == 0

    def test_modulo_by_zero_raises(self):
        with pytest.raises(ValueError, match="Cannot perform modulo by zero"):
            modulo(5, 0)

    def test_zero_dividend(self):
        assert modulo(0, 5) == 0
