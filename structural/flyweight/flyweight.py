"""
Flyweight pattern - standalone example
=========================================

Scenario: rendering a forest with potentially millions of trees. Each
tree's "intrinsic" state -- species name, mesh identifier, texture/color
-- is identical across many trees and is expensive-ish to represent, so we
share ONE TreeType (flyweight) object per unique combination. Each planted
Tree only stores its "extrinsic" state -- x/y position -- and holds a
reference to its shared TreeType.

We measure the memory/object-count difference to make the savings
concrete.

Run directly:
    python3 flyweight.py
"""

from __future__ import annotations

from typing import Dict, List, Tuple


# ---- Flyweight (intrinsic, shared state) ------------------------------

class TreeType:
    """Shared, immutable data common to every tree of this type.
    This is expensive-ish to construct and identical across many trees,
    so we only ever want ONE instance per (name, color, texture)."""

    def __init__(self, name: str, color: str, texture: str) -> None:
        self.name = name
        self.color = color
        self.texture = texture  # imagine this is a large mesh/texture blob

    def render(self, x: int, y: int) -> str:
        # Extrinsic state (x, y) is passed in by the caller, not stored here.
        return f"Rendering {self.color} {self.name} (texture={self.texture}) at ({x}, {y})"


# ---- Flyweight Factory ---------------------------------------------------

class TreeTypeFactory:
    """Ensures TreeType objects are shared/reused instead of duplicated."""

    _pool: Dict[Tuple[str, str, str], TreeType] = {}

    @classmethod
    def get_tree_type(cls, name: str, color: str, texture: str) -> TreeType:
        key = (name, color, texture)
        if key not in cls._pool:
            print(f"  [factory] creating NEW shared TreeType for {key}")
            cls._pool[key] = TreeType(name, color, texture)
        return cls._pool[key]

    @classmethod
    def type_count(cls) -> int:
        return len(cls._pool)


# ---- Context object (extrinsic state) ------------------------------------

class Tree:
    """A single planted tree. Only stores what's unique to this instance
    (position) plus a reference to its SHARED TreeType."""

    __slots__ = ("x", "y", "tree_type")

    def __init__(self, x: int, y: int, tree_type: TreeType) -> None:
        self.x = x
        self.y = y
        self.tree_type = tree_type

    def render(self) -> str:
        return self.tree_type.render(self.x, self.y)


class Forest:
    def __init__(self) -> None:
        self._trees: List[Tree] = []

    def plant_tree(self, x: int, y: int, name: str, color: str, texture: str) -> None:
        tree_type = TreeTypeFactory.get_tree_type(name, color, texture)
        self._trees.append(Tree(x, y, tree_type))

    def render(self) -> None:
        for tree in self._trees[:5]:  # only show the first few
            print(f"  {tree.render()}")
        if len(self._trees) > 5:
            print(f"  ... and {len(self._trees) - 5} more trees")

    def tree_count(self) -> int:
        return len(self._trees)


def main() -> None:
    print("=== Flyweight demo ===\n")

    forest = Forest()

    species = [
        ("Oak", "green", "oak_bark.png"),
        ("Pine", "dark-green", "pine_bark.png"),
        ("Birch", "white", "birch_bark.png"),
    ]

    print("Planting 10,000 trees from only 3 species...")
    import random
    random.seed(42)
    for _ in range(10_000):
        name, color, texture = random.choice(species)
        x, y = random.randint(0, 1000), random.randint(0, 1000)
        forest.plant_tree(x, y, name, color, texture)

    print(f"\nTotal Tree (context) objects created: {forest.tree_count()}")
    print(f"Total shared TreeType (flyweight) objects created: "
          f"{TreeTypeFactory.type_count()}")
    print("(Only 3 flyweights back 10,000 trees -- the heavy 'intrinsic' "
          "data was created just 3 times, not 10,000 times.)\n")

    print("Sample rendering:")
    forest.render()

    print("\n--- verifying trees of the same species share the exact same TreeType object ---")
    oaks = [t for t in forest._trees if t.tree_type.name == "Oak"]
    same_object = all(t.tree_type is oaks[0].tree_type for t in oaks)
    print(f"All {len(oaks)} Oak trees share one TreeType instance: {same_object}")


if __name__ == "__main__":
    main()
