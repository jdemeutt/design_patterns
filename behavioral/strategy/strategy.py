"""
Strategy pattern - standalone example
========================================

Scenario: a shopping cart that needs to support multiple payment methods.
Each payment method is a strategy implementing a common interface. The
ShoppingCart (context) is configured with whichever strategy the user
picks and delegates to it -- it has zero knowledge of *how* any given
payment method actually works.

We also show the lightweight, very-Pythonic version of Strategy using
plain functions instead of a class hierarchy.

Run directly:
    python3 strategy.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, List


# ---- Strategy interface (class-based) ------------------------------

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        ...


class CreditCardStrategy(PaymentStrategy):
    def __init__(self, card_number: str) -> None:
        self._card_number = card_number

    def pay(self, amount: float) -> str:
        masked = f"**** **** **** {self._card_number[-4:]}"
        return f"Charged ${amount:.2f} to credit card {masked}."


class PayPalStrategy(PaymentStrategy):
    def __init__(self, email: str) -> None:
        self._email = email

    def pay(self, amount: float) -> str:
        return f"Charged ${amount:.2f} via PayPal account '{self._email}'."


class CryptoStrategy(PaymentStrategy):
    def __init__(self, wallet_address: str) -> None:
        self._wallet_address = wallet_address

    def pay(self, amount: float) -> str:
        return (f"Transferred ${amount:.2f} worth of crypto to wallet "
                f"'{self._wallet_address[:8]}...'.")


# ---- Context -------------------------------------------------------------

class ShoppingCart:
    """The context. Holds a reference to a PaymentStrategy and delegates
    to it -- it never contains payment-processing logic itself."""

    def __init__(self) -> None:
        self._items: List[float] = []
        self._payment_strategy: PaymentStrategy | None = None

    def add_item(self, price: float) -> None:
        self._items.append(price)

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        self._payment_strategy = strategy

    def checkout(self) -> str:
        if self._payment_strategy is None:
            raise ValueError("No payment strategy selected.")
        total = sum(self._items)
        return self._payment_strategy.pay(total)


# ---- Lightweight, function-based Strategy (idiomatic Python) -----------

DiscountStrategy = Callable[[float], float]


def no_discount(total: float) -> float:
    return total


def ten_percent_off(total: float) -> float:
    return total * 0.90


def bulk_discount(total: float) -> float:
    return total - 20 if total > 100 else total


def checkout_with_discount(total: float, discount_strategy: DiscountStrategy) -> float:
    """The 'context' here is just a function accepting a strategy function
    -- no class hierarchy needed for such a simple, stateless variation."""
    return discount_strategy(total)


def main() -> None:
    print("=== Strategy demo ===\n")

    print("-- Class-based strategies (swappable payment methods) --")
    cart = ShoppingCart()
    cart.add_item(29.99)
    cart.add_item(15.50)

    cart.set_payment_strategy(CreditCardStrategy("4111111111111234"))
    print(f"  {cart.checkout()}")

    cart.set_payment_strategy(PayPalStrategy("shopper@example.com"))
    print(f"  {cart.checkout()}")

    cart.set_payment_strategy(CryptoStrategy("0xABCDEF1234567890"))
    print(f"  {cart.checkout()}")

    print("\n-- Function-based strategies (lightweight, idiomatic Python) --")
    order_total = 150.0
    for name, strategy in [
        ("no discount", no_discount),
        ("10% off", ten_percent_off),
        ("bulk discount", bulk_discount),
    ]:
        result = checkout_with_discount(order_total, strategy)
        print(f"  {name:15s} -> ${result:.2f}")


if __name__ == "__main__":
    main()
