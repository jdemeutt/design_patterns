"""
Visitor pattern - standalone example
=======================================

Scenario: a fixed hierarchy of shapes (Circle, Rectangle, Triangle). We
want to support multiple, unrelated operations over these shapes --
computing total area, rendering to a pseudo-SVG string, and exporting to a
dict -- WITHOUT adding methods to the shape classes for each new
operation. Each operation becomes its own Visitor; shapes only need one
small, stable accept() method each.

Run directly:
    python3 visitor.py
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import List


# ---- Element hierarchy (stable; rarely changes) -------------------------

class Shape(ABC):
    @abstractmethod
    def accept(self, visitor: "ShapeVisitor"):
        ...


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def accept(self, visitor: "ShapeVisitor"):
        return visitor.visit_circle(self)


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def accept(self, visitor: "ShapeVisitor"):
        return visitor.visit_rectangle(self)


class Triangle(Shape):
    def __init__(self, base: float, height: float) -> None:
        self.base = base
        self.height = height

    def accept(self, visitor: "ShapeVisitor"):
        return visitor.visit_triangle(self)


# ---- Visitor interface -------------------------------------------------

class ShapeVisitor(ABC):
    @abstractmethod
    def visit_circle(self, circle: Circle):
        ...

    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle):
        ...

    @abstractmethod
    def visit_triangle(self, triangle: Triangle):
        ...


# ---- Concrete visitors: each is a whole new OPERATION -------------------

class AreaVisitor(ShapeVisitor):
    """Operation 1: compute area. No shape class needed to know this logic."""

    def visit_circle(self, circle: Circle) -> float:
        return math.pi * circle.radius ** 2

    def visit_rectangle(self, rectangle: Rectangle) -> float:
        return rectangle.width * rectangle.height

    def visit_triangle(self, triangle: Triangle) -> float:
        return 0.5 * triangle.base * triangle.height


class SvgExportVisitor(ShapeVisitor):
    """Operation 2: render each shape as a (pseudo) SVG snippet."""

    def visit_circle(self, circle: Circle) -> str:
        return f'<circle r="{circle.radius}" />'

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        return f'<rect width="{rectangle.width}" height="{rectangle.height}" />'

    def visit_triangle(self, triangle: Triangle) -> str:
        return f'<polygon data-base="{triangle.base}" data-height="{triangle.height}" />'


class DictExportVisitor(ShapeVisitor):
    """Operation 3: export each shape's data as a plain dict."""

    def visit_circle(self, circle: Circle) -> dict:
        return {"type": "circle", "radius": circle.radius}

    def visit_rectangle(self, rectangle: Rectangle) -> dict:
        return {"type": "rectangle", "width": rectangle.width, "height": rectangle.height}

    def visit_triangle(self, triangle: Triangle) -> dict:
        return {"type": "triangle", "base": triangle.base, "height": triangle.height}


def main() -> None:
    print("=== Visitor demo ===\n")

    shapes: List[Shape] = [
        Circle(radius=3),
        Rectangle(width=4, height=5),
        Triangle(base=6, height=2),
    ]

    print("-- Operation 1: AreaVisitor --")
    area_visitor = AreaVisitor()
    total_area = 0.0
    for shape in shapes:
        area = shape.accept(area_visitor)  # double dispatch happens here
        total_area += area
        print(f"  {shape.__class__.__name__}: area = {area:.2f}")
    print(f"  Total area across all shapes: {total_area:.2f}")

    print("\n-- Operation 2: SvgExportVisitor (added with ZERO shape-class changes) --")
    svg_visitor = SvgExportVisitor()
    for shape in shapes:
        print(f"  {shape.accept(svg_visitor)}")

    print("\n-- Operation 3: DictExportVisitor --")
    dict_visitor = DictExportVisitor()
    for shape in shapes:
        print(f"  {shape.accept(dict_visitor)}")

    print("\n--- Shape classes only ever implemented ONE method: accept() ---")


if __name__ == "__main__":
    main()
