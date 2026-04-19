# calculator.py
# The Factory Pattern — picks the right math operation automatically

# -------------------------------------------------------------------
# Step 1: Each operation is its own little class
# -------------------------------------------------------------------

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


# -------------------------------------------------------------------
# Step 2: The Factory — given a type string, returns the right class
# -------------------------------------------------------------------

class CalculationFactory:
    # Map each type string to its operation class
    _operations = {
        "Add":      AddOperation,
        "Sub":      SubOperation,
        "Multiply": MultiplyOperation,
        "Divide":   DivideOperation,
    }

    @staticmethod
    def get_operation(operation_type: str):
        """
        Give it "Add", "Sub", "Multiply", or "Divide"
        and it hands back the right operation object.
        """
        op_class = CalculationFactory._operations.get(operation_type)

        if op_class is None:
            raise ValueError(f"Unknown operation: '{operation_type}'. "
                             f"Must be one of: {list(CalculationFactory._operations.keys())}")

        return op_class()

    @staticmethod
    def compute(operation_type: str, a: float, b: float) -> float:
        """
        Shortcut: give it the type + numbers, get back the answer.
        Example: CalculationFactory.compute("Add", 3, 4) → 7.0
        """
        operation = CalculationFactory.get_operation(operation_type)
        return operation.compute(a, b)