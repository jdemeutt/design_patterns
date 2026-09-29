"""
Decorator pattern - standalone example
=========================================

Scenario 1 (classic OOP Decorator): a coffee shop where a base Coffee can
be wrapped with any combination of Milk, Sugar, and WhippedCream add-ons,
each adding to the cost and description, stacked in any order.

Scenario 2 (Python's built-in function-decorator sugar): a quick look at
how @decorator syntax is the exact same pattern applied to functions.

Run directly:
    python3 decorator.py
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from functools import wraps


# ---- Component -----------------------------------------------------------

class Beverage(ABC):
    @abstractmethod
    def cost(self) -> float:
        ...

    @abstractmethod
    def description(self) -> str:
        ...


# ---- Concrete component --------------------------------------------------

class Coffee(Beverage):
    def cost(self) -> float:
        return 2.00

    def description(self) -> str:
        return "Coffee"


# ---- Decorator base --------------------------------------------------

class BeverageDecorator(Beverage):
    """Wraps a Beverage and exposes the exact same interface."""

    def __init__(self, wrapped: Beverage) -> None:
        self._wrapped = wrapped

    def cost(self) -> float:
        return self._wrapped.cost()

    def description(self) -> str:
        return self._wrapped.description()


class Milk(BeverageDecorator):
    def cost(self) -> float:
        return self._wrapped.cost() + 0.50

    def description(self) -> str:
        return self._wrapped.description() + " + Milk"


class Sugar(BeverageDecorator):
    def cost(self) -> float:
        return self._wrapped.cost() + 0.25

    def description(self) -> str:
        return self._wrapped.description() + " + Sugar"


class WhippedCream(BeverageDecorator):
    def cost(self) -> float:
        return self._wrapped.cost() + 0.75

    def description(self) -> str:
        return self._wrapped.description() + " + Whipped Cream"


def order(beverage: Beverage) -> None:
    print(f"{beverage.description():40s} -> ${beverage.cost():.2f}")


# ---- Scenario 2: Python's native function-decorator sugar ---------------

def timed(func):
    """A textbook Python function decorator: wraps `func`, adds timing
    behavior around it, and preserves its interface (same call signature,
    same return value) -- exactly the Decorator pattern, just applied to
    a function instead of an object."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  '{func.__name__}' took {elapsed:.2f} ms")
        return result

    return wrapper


@timed
def brew_espresso_shots(count: int) -> str:
    time.sleep(0.01 * count)  # simulate work
    return f"{count} espresso shot(s) brewed"


def main() -> None:
    print("=== Decorator demo ===\n")

    print("-- Object decorators, stacked in different orders --")
    plain = Coffee()
    order(plain)

    milk_sugar = Sugar(Milk(Coffee()))
    order(milk_sugar)

    the_works = WhippedCream(Sugar(Milk(Coffee())))
    order(the_works)

    # Order of wrapping can be varied freely at runtime.
    double_milk = Milk(Milk(Coffee()))
    order(double_milk)

    print("\n-- Client code only ever depends on the Beverage interface --")
    print(f"isinstance(the_works, Beverage): {isinstance(the_works, Beverage)}")

    print("\n-- Python's @decorator syntax is the same pattern for functions --")
    result = brew_espresso_shots(3)
    print(f"  result: {result}")


if __name__ == "__main__":
    main()
