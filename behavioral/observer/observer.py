"""
Observer pattern - standalone example
========================================

Scenario: a WeatherStation (Subject) that reads new temperature/humidity
data and needs to notify several independent displays -- a CurrentConditionsDisplay
and a StatisticsDisplay -- whenever new data arrives. The station knows
nothing about what the displays do with the data; displays can be
attached/detached at runtime.

Run directly:
    python3 observer.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


# ---- Observer interface -------------------------------------------------

class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float, humidity: float) -> None:
        ...


# ---- Subject --------------------------------------------------------------

class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        ...

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        ...

    @abstractmethod
    def notify(self) -> None:
        ...


class WeatherStation(Subject):
    def __init__(self) -> None:
        self._observers: List[Observer] = []
        self._temperature: float = 0.0
        self._humidity: float = 0.0

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self._temperature, self._humidity)

    def set_measurements(self, temperature: float, humidity: float) -> None:
        print(f"[WeatherStation] new reading: {temperature}C, {humidity}% humidity")
        self._temperature = temperature
        self._humidity = humidity
        self.notify()  # the station doesn't know or care who's listening


# ---- Concrete observers ----------------------------------------------

class CurrentConditionsDisplay(Observer):
    def update(self, temperature: float, humidity: float) -> None:
        print(f"  [CurrentConditionsDisplay] Now: {temperature}C, {humidity}% humidity")


class StatisticsDisplay(Observer):
    def __init__(self) -> None:
        self._readings: List[float] = []

    def update(self, temperature: float, humidity: float) -> None:
        self._readings.append(temperature)
        avg = sum(self._readings) / len(self._readings)
        print(f"  [StatisticsDisplay] avg={avg:.1f}C over "
              f"{len(self._readings)} reading(s), min={min(self._readings)}C, "
              f"max={max(self._readings)}C")


class AlertDisplay(Observer):
    def update(self, temperature: float, humidity: float) -> None:
        if temperature > 35:
            print(f"  [AlertDisplay] !!! HEAT WARNING: {temperature}C !!!")


def main() -> None:
    print("=== Observer demo ===\n")

    station = WeatherStation()
    current = CurrentConditionsDisplay()
    stats = StatisticsDisplay()
    alerts = AlertDisplay()

    station.attach(current)
    station.attach(stats)
    station.attach(alerts)

    station.set_measurements(22.0, 60)
    station.set_measurements(25.5, 55)

    print("\n-- Detaching the current-conditions display at runtime --")
    station.detach(current)
    station.set_measurements(36.0, 40)  # should trigger the AlertDisplay

    print("\n--- WeatherStation never referenced a concrete display class directly ---")


if __name__ == "__main__":
    main()
