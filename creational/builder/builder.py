"""
Builder pattern - standalone example
=======================================

Scenario: assembling a custom PC. A computer has many optional
components; hard-coding a single constructor with 10 optional parameters
would be unreadable. Instead, a Builder accumulates parts step by step and
produces an immutable Computer only when build() is called. A Director
shows how to script two common, pre-defined configurations, while client
code is also free to drive the builder manually for a fully custom build.

Run directly:
    python3 builder.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


# ---- Product -----------------------------------------------------------

@dataclass(frozen=True)
class Computer:
    """The final, immutable product."""

    cpu: str
    ram_gb: int
    storage_gb: int
    gpu: Optional[str] = None
    peripherals: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        parts = [
            f"CPU: {self.cpu}",
            f"RAM: {self.ram_gb} GB",
            f"Storage: {self.storage_gb} GB",
            f"GPU: {self.gpu or 'integrated graphics'}",
            f"Peripherals: {', '.join(self.peripherals) or 'none'}",
        ]
        return "Computer(\n  " + "\n  ".join(parts) + "\n)"


# ---- Builder -------------------------------------------------------------

class ComputerBuilder:
    """Accumulates parts step by step; nothing is 'final' until build()."""

    def __init__(self) -> None:
        self._cpu = "Generic Dual-Core CPU"
        self._ram_gb = 8
        self._storage_gb = 256
        self._gpu: Optional[str] = None
        self._peripherals: List[str] = []

    def set_cpu(self, cpu: str) -> "ComputerBuilder":
        self._cpu = cpu
        return self  # enables fluent chaining

    def set_ram(self, ram_gb: int) -> "ComputerBuilder":
        self._ram_gb = ram_gb
        return self

    def set_storage(self, storage_gb: int) -> "ComputerBuilder":
        self._storage_gb = storage_gb
        return self

    def set_gpu(self, gpu: str) -> "ComputerBuilder":
        self._gpu = gpu
        return self

    def add_peripheral(self, peripheral: str) -> "ComputerBuilder":
        self._peripherals.append(peripheral)
        return self

    def build(self) -> Computer:
        if self._ram_gb <= 0 or self._storage_gb <= 0:
            raise ValueError("RAM and storage must be positive")
        return Computer(
            cpu=self._cpu,
            ram_gb=self._ram_gb,
            storage_gb=self._storage_gb,
            gpu=self._gpu,
            peripherals=list(self._peripherals),  # defensive copy
        )


# ---- Director (optional) ------------------------------------------------

class ComputerDirector:
    """Knows recipes for common configurations; doesn't know construction
    details -- it just calls builder steps in the right order."""

    @staticmethod
    def build_office_pc(builder: ComputerBuilder) -> Computer:
        return (
            builder.set_cpu("Intel Core i3")
            .set_ram(8)
            .set_storage(512)
            .add_peripheral("keyboard")
            .add_peripheral("mouse")
            .build()
        )

    @staticmethod
    def build_gaming_pc(builder: ComputerBuilder) -> Computer:
        return (
            builder.set_cpu("AMD Ryzen 9")
            .set_ram(32)
            .set_storage(2000)
            .set_gpu("NVIDIA RTX 4080")
            .add_peripheral("mechanical keyboard")
            .add_peripheral("gaming mouse")
            .add_peripheral("RGB headset")
            .build()
        )


def main() -> None:
    print("=== Builder demo ===\n")

    print("Using a Director for a pre-defined 'office PC' configuration:")
    office_pc = ComputerDirector.build_office_pc(ComputerBuilder())
    print(office_pc)

    print("\nUsing a Director for a pre-defined 'gaming PC' configuration:")
    gaming_pc = ComputerDirector.build_gaming_pc(ComputerBuilder())
    print(gaming_pc)

    print("\nDriving the builder directly for a fully custom build:")
    custom_pc = (
        ComputerBuilder()
        .set_cpu("Apple M3 Pro")
        .set_ram(18)
        .set_storage(1000)
        .add_peripheral("USB-C hub")
        .build()
    )
    print(custom_pc)

    print("\n--- the product is immutable once built ---")
    try:
        custom_pc.ram_gb = 999  # type: ignore[misc]
    except Exception as exc:  # dataclasses.FrozenInstanceError
        print(f"Attempting to mutate the built Computer raised: {exc!r}")


if __name__ == "__main__":
    main()
