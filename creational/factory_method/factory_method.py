"""
Factory Method pattern - standalone example
=============================================

Scenario: a logistics app that plans deliveries. The planning logic
(`plan_delivery`) is written entirely against the abstract `Transport`
interface. Each concrete "creator" knows how to build the one concrete
transport it's responsible for. Adding a new mode of transport (e.g. Ship)
requires zero changes to existing code -- just a new Creator subclass.

Run directly:
    python3 factory_method.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# ---- Product hierarchy -----------------------------------------------

class Transport(ABC):
    """The abstract product."""

    @abstractmethod
    def deliver(self, cargo: str) -> str:
        ...


class Truck(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Truck delivers '{cargo}' by road."


class Ship(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Ship delivers '{cargo}' by sea."


class Drone(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Drone delivers '{cargo}' by air."


# ---- Creator hierarchy -------------------------------------------------

class Logistics(ABC):
    """The Creator. Contains business logic written purely in terms of
    the abstract Transport product."""

    @abstractmethod
    def factory_method(self) -> Transport:
        """Subclasses override this to produce the concrete transport."""
        ...

    def plan_delivery(self, cargo: str) -> str:
        # This method never mentions Truck, Ship, or Drone directly.
        transport = self.factory_method()
        result = transport.deliver(cargo)
        return f"[{self.__class__.__name__}] planned delivery -> {result}"


class RoadLogistics(Logistics):
    def factory_method(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    def factory_method(self) -> Transport:
        return Ship()


class AirLogistics(Logistics):
    def factory_method(self) -> Transport:
        return Drone()


def main() -> None:
    print("=== Factory Method demo ===\n")

    creators = [RoadLogistics(), SeaLogistics(), AirLogistics()]
    cargo_items = ["medical supplies", "furniture", "urgent documents"]

    for creator, cargo in zip(creators, cargo_items):
        print(creator.plan_delivery(cargo))

    print("\n--- adding a new transport requires no change to plan_delivery ---")

    class RailLogistics(Logistics):
        def factory_method(self) -> Transport:
            class Train(Transport):
                def deliver(self, cargo: str) -> str:
                    return f"Train delivers '{cargo}' by rail."
            return Train()

    print(RailLogistics().plan_delivery("bulk grain"))


if __name__ == "__main__":
    main()
