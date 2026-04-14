"""Calculator module with clean, SOLID-compliant operations."""

import math
from abc import ABC, abstractmethod


class Operation(ABC):
    """Abstract base class for calculator operations (Open/Closed Principle)."""

    @abstractmethod
    def execute(self, a: float, b: float = 0.0) -> float:
        """Execute the operation on the given operands."""


class Add(Operation):
    """Addition operation."""

    def execute(self, a: float, b: float = 0.0) -> float:
        return a + b


class Subtract(Operation):
    """Subtraction operation."""

    def execute(self, a: float, b: float = 0.0) -> float:
        return a - b


class Multiply(Operation):
    """Multiplication operation."""

    def execute(self, a: float, b: float = 0.0) -> float:
        return a * b


class Divide(Operation):
    """Division operation with zero-division guard."""

    def execute(self, a: float, b: float = 0.0) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b


class Power(Operation):
    """Exponentiation operation."""

    def execute(self, a: float, b: float = 0.0) -> float:
        return a ** b


class SquareRoot(Operation):
    """Square root operation (uses only the first operand)."""

    def execute(self, a: float, b: float = 0.0) -> float:
        if a < 0:
            raise ValueError("Cannot compute square root of a negative number.")
        return math.sqrt(a)


class Modulo(Operation):
    """Modulo operation."""

    def execute(self, a: float, b: float = 0.0) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot compute modulo with zero divisor.")
        return a % b


# Registry mapping operation names to their implementations
OPERATIONS: dict[str, Operation] = {
    "add": Add(),
    "sub": Subtract(),
    "mul": Multiply(),
    "div": Divide(),
    "pow": Power(),
    "sqrt": SquareRoot(),
    "mod": Modulo(),
}


def calculate(a: float, b: float, operation_name: str) -> float:
    """Perform a calculation using the specified operation.

    Args:
        a: The first operand.
        b: The second operand.
        operation_name: Name of the operation (add, sub, mul, div, pow, sqrt, mod).

    Returns:
        The result of the operation.

    Raises:
        ValueError: If the operation name is not recognized.
    """
    operation = OPERATIONS.get(operation_name)
    if operation is None:
        raise ValueError(f"Unknown operation: '{operation_name}'")
    return operation.execute(a, b)


def process_pairs(numbers: list[float], operation_name: str) -> list[float]:
    """Apply an operation to all unique pairs in a list of numbers.

    Args:
        numbers: List of numeric values.
        operation_name: Name of the operation to apply.

    Returns:
        A list of results for each (i, j) pair where i != j.
    """
    return [
        calculate(a, b, operation_name)
        for i, a in enumerate(numbers)
        for j, b in enumerate(numbers)
        if i != j
    ]


def display_results(results: list[float]) -> None:
    """Print each result with its index."""
    for index, value in enumerate(results):
        print(f"Result {index}: {value}")


if __name__ == "__main__":
    nums = [10, 5, 3]
    results = process_pairs(nums, "div")
    display_results(results)
