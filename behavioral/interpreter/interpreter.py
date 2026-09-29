"""
Interpreter pattern - standalone example
===========================================

Scenario: a tiny arithmetic expression language supporting numbers,
variables, addition, subtraction, and multiplication. Each grammar rule
is its own Expression class; interpreting an expression tree means
recursively calling interpret(context) on the root node. A "context"
dict supplies variable values.

We build a tree by hand here to keep the example self-contained (no
external parser dependency), representing the expression:

    (x + 10) * (y - 2)

Run directly:
    python3 interpreter.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


Context = Dict[str, float]


# ---- Abstract expression -------------------------------------------------

class Expression(ABC):
    @abstractmethod
    def interpret(self, context: Context) -> float:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...


# ---- Terminal expressions ----------------------------------------------

class Number(Expression):
    """A literal number -- a terminal / leaf expression."""

    def __init__(self, value: float) -> None:
        self._value = value

    def interpret(self, context: Context) -> float:
        return self._value

    def __str__(self) -> str:
        return str(self._value)


class Variable(Expression):
    """A named variable, resolved from the context at interpretation
    time -- also a terminal expression."""

    def __init__(self, name: str) -> None:
        self._name = name

    def interpret(self, context: Context) -> float:
        if self._name not in context:
            raise NameError(f"Undefined variable: {self._name}")
        return context[self._name]

    def __str__(self) -> str:
        return self._name


# ---- Nonterminal expressions --------------------------------------------

class BinaryExpression(Expression):
    """Common base for operators that combine two sub-expressions."""

    symbol = "?"

    def __init__(self, left: Expression, right: Expression) -> None:
        self._left = left
        self._right = right

    def __str__(self) -> str:
        return f"({self._left} {self.symbol} {self._right})"


class Add(BinaryExpression):
    symbol = "+"

    def interpret(self, context: Context) -> float:
        return self._left.interpret(context) + self._right.interpret(context)


class Subtract(BinaryExpression):
    symbol = "-"

    def interpret(self, context: Context) -> float:
        return self._left.interpret(context) - self._right.interpret(context)


class Multiply(BinaryExpression):
    symbol = "*"

    def interpret(self, context: Context) -> float:
        return self._left.interpret(context) * self._right.interpret(context)


def main() -> None:
    print("=== Interpreter demo ===\n")

    # Build the expression tree for: (x + 10) * (y - 2)
    expression: Expression = Multiply(
        Add(Variable("x"), Number(10)),
        Subtract(Variable("y"), Number(2)),
    )

    print(f"Expression: {expression}")

    for context in (
        {"x": 5, "y": 10},
        {"x": 0, "y": 2},
        {"x": -10, "y": 12},
    ):
        result = expression.interpret(context)
        print(f"  interpret(context={context}) -> {result}")

    print("\n--- extending the grammar just means adding a new class ---")

    class Divide(BinaryExpression):
        symbol = "/"

        def interpret(self, context: Context) -> float:
            return self._left.interpret(context) / self._right.interpret(context)

    new_expression = Divide(Variable("x"), Number(4))
    print(f"New expression: {new_expression}")
    print(f"  interpret({{'x': 20}}) -> {new_expression.interpret({'x': 20})}")

    print("\n--- undefined variable raises a clear error ---")
    try:
        expression.interpret({"x": 1})  # 'y' missing
    except NameError as exc:
        print(f"  Caught expected error: {exc}")


if __name__ == "__main__":
    main()
