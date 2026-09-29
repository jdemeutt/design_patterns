"""
Bridge pattern - standalone example
======================================

Scenario: we need to render shapes (Circle, Square, ...) using different
rendering backends (Vector, Raster, ...). Without Bridge we'd need
VectorCircle, RasterCircle, VectorSquare, RasterSquare, etc -- a
combinatorial explosion. Bridge splits "shape" and "renderer" into two
independent hierarchies connected by composition.

Run directly:
    python3 bridge.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# ---- Implementor hierarchy -----------------------------------------

class Renderer(ABC):
    """The implementation-side interface."""

    @abstractmethod
    def render_circle(self, radius: float) -> str:
        ...

    @abstractmethod
    def render_square(self, side: float) -> str:
        ...


class VectorRenderer(Renderer):
    def render_circle(self, radius: float) -> str:
        return f"Drawing a circle of radius {radius} as scalable vector paths."

    def render_square(self, side: float) -> str:
        return f"Drawing a square of side {side} as scalable vector paths."


class RasterRenderer(Renderer):
    def render_circle(self, radius: float) -> str:
        pixel_count = int(3.14159 * radius * radius)
        return f"Drawing a circle of radius {radius} as ~{pixel_count} pixels."

    def render_square(self, side: float) -> str:
        pixel_count = int(side * side)
        return f"Drawing a square of side {side} as ~{pixel_count} pixels."


# ---- Abstraction hierarchy ---------------------------------------------

class Shape(ABC):
    """The abstraction. Holds a reference to a Renderer (the 'bridge') and
    delegates the actual drawing work to it."""

    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer

    @abstractmethod
    def draw(self) -> str:
        ...

    @abstractmethod
    def resize(self, factor: float) -> None:
        ...


class Circle(Shape):
    def __init__(self, renderer: Renderer, radius: float) -> None:
        super().__init__(renderer)
        self.radius = radius

    def draw(self) -> str:
        return self.renderer.render_circle(self.radius)

    def resize(self, factor: float) -> None:
        self.radius *= factor


class Square(Shape):
    def __init__(self, renderer: Renderer, side: float) -> None:
        super().__init__(renderer)
        self.side = side

    def draw(self) -> str:
        return self.renderer.render_square(self.side)

    def resize(self, factor: float) -> None:
        self.side *= factor


def main() -> None:
    print("=== Bridge demo ===\n")

    vector = VectorRenderer()
    raster = RasterRenderer()

    shapes = [
        Circle(vector, radius=5),
        Circle(raster, radius=5),
        Square(vector, side=4),
        Square(raster, side=4),
    ]

    for shape in shapes:
        print(f"[{shape.__class__.__name__} + {shape.renderer.__class__.__name__}] "
              f"{shape.draw()}")

    print("\n--- swapping a shape's renderer at runtime, no class changes needed ---")
    circle = Circle(vector, radius=10)
    print(f"Before swap: {circle.draw()}")
    circle.renderer = raster  # swap the implementor, abstraction code untouched
    print(f"After swap:  {circle.draw()}")

    print("\n--- resizing works identically regardless of renderer ---")
    circle.resize(2.0)
    print(f"After resize x2: {circle.draw()}")


if __name__ == "__main__":
    main()
