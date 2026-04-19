class AddOperation:
    def compute(self, a: float, b: float) -> float:
        return a + b

class SubOperation:
    def compute(self, a: float, b: float) -> float:
        return a - b

class MultiplyOperation:
    def compute(self, a: float, b: float) -> float:
        return a * b

class DivideOperation:
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        return a / b

class CalculationFactory:
    _operations = {
        "Add":      AddOperation,
        "Sub":      SubOperation,
        "Multiply": MultiplyOperation,
        "Divide":   DivideOperation,
    }

    @staticmethod
    def get_operation(operation_type: str):
        op_class = CalculationFactory._operations.get(operation_type)
        if op_class is None:
            raise ValueError(f"Unknown operation: '{operation_type}'. "
                             f"Must be one of: {list(CalculationFactory._operations.keys())}")
        return op_class()

    @staticmethod
    def compute(operation_type: str, a: float, b: float) -> float:
        operation = CalculationFactory.get_operation(operation_type)
        return operation.compute(a, b)
