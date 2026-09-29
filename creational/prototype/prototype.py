"""
Prototype pattern - standalone example
=========================================

Scenario: a game needs to spawn many enemies of a few "kinds" (goblin,
dragon, ...). Building an enemy from scratch involves an (simulated)
expensive setup step -- loading stats, equipment, and AI behavior. Instead
of re-running that setup for every spawn, we keep one pre-configured
"prototype" instance per enemy kind and clone it, then tweak the copy
(e.g. position, name) per spawned instance.

This example also demonstrates the classic shallow-vs-deep copy pitfall.

Run directly:
    python3 prototype.py
"""

from __future__ import annotations

import copy
import time
from typing import Dict, List


class Enemy:
    """A prototype-capable game entity."""

    def __init__(self, kind: str, health: int, equipment: List[str]) -> None:
        # Simulate an expensive setup (e.g. loading assets/stats from disk).
        time.sleep(0.05)
        self.kind = kind
        self.health = health
        self.equipment = equipment  # a mutable list -- the crux of the demo
        self.position = (0, 0)
        self.name = kind

    def clone(self, deep: bool = True) -> "Enemy":
        """Return a copy of this enemy.

        deep=True (the safe default) ensures the clone's `equipment` list
        is independent of the original's. deep=False demonstrates the
        shallow-copy pitfall: the two enemies would share one list.
        """
        return copy.deepcopy(self) if deep else copy.copy(self)

    def __repr__(self) -> str:
        return (f"Enemy(name={self.name!r}, kind={self.kind!r}, "
                f"health={self.health}, equipment={self.equipment}, "
                f"position={self.position})")


class EnemyRegistry:
    """Holds one pre-built prototype per enemy kind."""

    def __init__(self) -> None:
        self._prototypes: Dict[str, Enemy] = {}

    def register(self, key: str, prototype: Enemy) -> None:
        self._prototypes[key] = prototype

    def spawn(self, key: str, *, name: str, position: tuple) -> Enemy:
        prototype = self._prototypes[key]
        clone = prototype.clone(deep=True)
        clone.name = name
        clone.position = position
        return clone


def main() -> None:
    print("=== Prototype demo ===\n")

    print("Building prototypes (expensive, happens only once per kind):")
    start = time.perf_counter()
    goblin_prototype = Enemy("Goblin", health=30, equipment=["dagger", "leather armor"])
    dragon_prototype = Enemy("Dragon", health=500, equipment=["fire breath", "scales"])
    elapsed = time.perf_counter() - start
    print(f"  Built 2 prototypes in {elapsed:.3f}s\n")

    registry = EnemyRegistry()
    registry.register("goblin", goblin_prototype)
    registry.register("dragon", dragon_prototype)

    print("Spawning 3 goblins by cloning the prototype (fast, no re-setup):")
    start = time.perf_counter()
    goblins = [
        registry.spawn("goblin", name=f"Goblin #{i}", position=(i, 0))
        for i in range(3)
    ]
    elapsed = time.perf_counter() - start
    for g in goblins:
        print(f"  {g}")
    print(f"  Spawned 3 clones in {elapsed:.4f}s (no expensive setup re-run)\n")

    print("--- deep copy keeps clones independent ---")
    goblins[0].equipment.append("stolen shield")
    print(f"goblins[0].equipment -> {goblins[0].equipment}")
    print(f"goblins[1].equipment -> {goblins[1].equipment}  (unaffected)")
    print(f"prototype.equipment  -> {goblin_prototype.equipment}  (unaffected)\n")

    print("--- shallow copy pitfall: equipment list gets SHARED, not copied ---")
    shallow_clone = goblin_prototype.clone(deep=False)
    shallow_clone.equipment.append("cursed ring")
    print(f"shallow_clone.equipment  -> {shallow_clone.equipment}")
    print(f"goblin_prototype.equipment -> {goblin_prototype.equipment}  "
          f"(mutated unintentionally! same list object)")


if __name__ == "__main__":
    main()
