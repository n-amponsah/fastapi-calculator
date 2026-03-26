import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def post(endpoint, a, b):
    return client.post(endpoint, json={"a": a, "b": b})


class TestRootEndpoint:
    def test_returns_html(self):
        r = client.get("/")
        assert r.status_code == 200

    def test_html_contains_calculator(self):
        r = client.get("/")
        assert "CALCULATOR" in r.text.upper()


class TestAddEndpoint:
    def test_basic(self):
        r = post("/add", 3, 4)
        assert r.status_code == 200
        assert r.json()["result"] == 7

    def test_response_shape(self):
        r = post("/add", 1, 2)
        data = r.json()
        assert data["operation"] == "add"

    def test_negative(self):
        assert post("/add", -5, 3).json()["result"] == -2

    def test_floats(self):
        assert post("/add", 1.5, 2.5).json()["result"] == pytest.approx(4.0)

    def test_invalid_body_returns_422(self):
        r = client.post("/add", json={"a": "hello", "b": 2})
        assert r.status_code == 422


class TestSubtractEndpoint:
    def test_basic(self):
        assert post("/subtract", 10, 3).json()["result"] == 7

    def test_negative_result(self):
        assert post("/subtract", 3, 10).json()["result"] == -7

    def test_operation_field(self):
        assert post("/subtract", 1, 1).json()["operation"] == "subtract"


class TestMultiplyEndpoint:
    def test_basic(self):
        assert post("/multiply", 3, 4).json()["result"] == 12

    def test_by_zero(self):
        assert post("/multiply", 99, 0).json()["result"] == 0

    def test_operation_field(self):
        assert post("/multiply", 1, 1).json()["operation"] == "multiply"


class TestDivideEndpoint:
    def test_basic(self):
        assert post("/divide", 10, 2).json()["result"] == 5.0

    def test_divide_by_zero_returns_400(self):
        r = post("/divide", 5, 0)
        assert r.status_code == 400

    def test_divide_by_zero_detail(self):
        r = post("/divide", 5, 0)
        assert "zero" in r.json()["detail"].lower()

    def test_operation_field(self):
        assert post("/divide", 6, 2).json()["operation"] == "divide"


class TestPowerEndpoint:
    def test_basic(self):
        assert post("/power", 2, 3).json()["result"] == 8

    def test_zero_exponent(self):
        assert post("/power", 5, 0).json()["result"] == 1

    def test_operation_field(self):
        assert post("/power", 2, 2).json()["operation"] == "power"


class TestModuloEndpoint:
    def test_basic(self):
        assert post("/modulo", 10, 3).json()["result"] == 1

    def test_modulo_by_zero_returns_400(self):
        r = post("/modulo", 5, 0)
        assert r.status_code == 400

    def test_operation_field(self):
        assert post("/modulo", 7, 3).json()["operation"] == "modulo"