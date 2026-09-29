"""
Chain of Responsibility pattern - standalone example
=======================================================

Scenario: a customer-support ticketing system. A ticket is submitted once,
to the front of a chain of handlers (Tier1Support -> Tier2Support ->
Tier3Support -> ManagerEscalation). Each handler decides, based on the
ticket's severity, whether it can resolve it or must forward it along.
The submitter never needs to know which handler eventually deals with it.

Run directly:
    python3 chain_of_responsibility.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Ticket:
    subject: str
    severity: int  # 1 (low) .. 5 (critical)


class SupportHandler(ABC):
    """Base handler: holds a reference to the next handler in the chain."""

    def __init__(self) -> None:
        self._next: Optional["SupportHandler"] = None

    def set_next(self, handler: "SupportHandler") -> "SupportHandler":
        self._next = handler
        return handler  # allows fluent chaining: h1.set_next(h2).set_next(h3)

    def handle(self, ticket: Ticket) -> str:
        if self._can_handle(ticket):
            return self._resolve(ticket)
        if self._next is not None:
            return self._next.handle(ticket)
        return f"Ticket '{ticket.subject}' (severity {ticket.severity}) went unhandled!"

    @abstractmethod
    def _can_handle(self, ticket: Ticket) -> bool:
        ...

    @abstractmethod
    def _resolve(self, ticket: Ticket) -> str:
        ...


class Tier1Support(SupportHandler):
    def _can_handle(self, ticket: Ticket) -> bool:
        return ticket.severity <= 1

    def _resolve(self, ticket: Ticket) -> str:
        return f"[Tier1Support] resolved '{ticket.subject}' (routine issue)"


class Tier2Support(SupportHandler):
    def _can_handle(self, ticket: Ticket) -> bool:
        return ticket.severity <= 3

    def _resolve(self, ticket: Ticket) -> str:
        return f"[Tier2Support] resolved '{ticket.subject}' (needed technical expertise)"


class Tier3Support(SupportHandler):
    def _can_handle(self, ticket: Ticket) -> bool:
        return ticket.severity <= 4

    def _resolve(self, ticket: Ticket) -> str:
        return f"[Tier3Support] resolved '{ticket.subject}' (deep technical/engineering issue)"


class ManagerEscalation(SupportHandler):
    def _can_handle(self, ticket: Ticket) -> bool:
        return True  # the end of the chain: always handles what's left

    def _resolve(self, ticket: Ticket) -> str:
        return f"[ManagerEscalation] personally handling critical ticket '{ticket.subject}'"


def build_support_chain() -> SupportHandler:
    tier1 = Tier1Support()
    tier2 = Tier2Support()
    tier3 = Tier3Support()
    manager = ManagerEscalation()
    tier1.set_next(tier2).set_next(tier3).set_next(manager)
    return tier1  # client only ever talks to the first handler


def main() -> None:
    print("=== Chain of Responsibility demo ===\n")

    chain = build_support_chain()

    tickets = [
        Ticket("Can't find the settings menu", severity=1),
        Ticket("Intermittent login failures", severity=3),
        Ticket("Payment processing is down for some users", severity=4),
        Ticket("Full production outage", severity=5),
    ]

    for ticket in tickets:
        print(chain.handle(ticket))

    print("\n--- a chain WITHOUT a catch-all handler can leave requests unhandled ---")
    partial_chain = Tier1Support()
    partial_chain.set_next(Tier2Support())
    print(partial_chain.handle(Ticket("Critical security breach", severity=5)))


if __name__ == "__main__":
    main()
