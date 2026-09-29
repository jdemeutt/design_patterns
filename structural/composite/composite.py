"""
Composite pattern - standalone example
=========================================

Scenario: a simplified filesystem. A File is a leaf; a Folder is a
composite that can contain Files and other Folders. Client code calls
.size() and .display() identically on a single File or an entire nested
Folder tree, without ever checking "is this a file or a folder?".

Run directly:
    python3 composite.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


# ---- Component -----------------------------------------------------------

class FileSystemComponent(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def size(self) -> int:
        """Total size in bytes."""
        ...

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        ...


# ---- Leaf -----------------------------------------------------------------

class File(FileSystemComponent):
    def __init__(self, name: str, size_bytes: int) -> None:
        super().__init__(name)
        self._size_bytes = size_bytes

    def size(self) -> int:
        return self._size_bytes

    def display(self, indent: int = 0) -> str:
        return f"{'  ' * indent}- {self.name} ({self._size_bytes} bytes)"


# ---- Composite -------------------------------------------------------

class Folder(FileSystemComponent):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._children: List[FileSystemComponent] = []

    def add(self, component: FileSystemComponent) -> "Folder":
        self._children.append(component)
        return self  # allow chaining

    def remove(self, component: FileSystemComponent) -> None:
        self._children.remove(component)

    def size(self) -> int:
        # Recursively sums leaves AND nested composites uniformly.
        return sum(child.size() for child in self._children)

    def display(self, indent: int = 0) -> str:
        lines = [f"{'  ' * indent}+ {self.name}/ ({self.size()} bytes total)"]
        for child in self._children:
            lines.append(child.display(indent + 1))
        return "\n".join(lines)


def main() -> None:
    print("=== Composite demo ===\n")

    # Build a small nested filesystem tree.
    root = Folder("project")
    src = Folder("src")
    src.add(File("main.py", 1200)).add(File("utils.py", 800))

    tests = Folder("tests")
    tests.add(File("test_main.py", 950))

    docs = Folder("docs")
    docs.add(File("README.md", 300))

    root.add(src).add(tests).add(docs).add(File("setup.py", 400))

    print(root.display())
    print(f"\nTotal project size via root.size(): {root.size()} bytes")

    print("\n--- client code treats a lone File and a whole Folder identically ---")

    def report(component: FileSystemComponent) -> None:
        # No isinstance() check needed -- works for a File OR a Folder.
        print(f"'{component.name}' occupies {component.size()} bytes.")

    report(File("standalone.txt", 50))
    report(src)
    report(root)


if __name__ == "__main__":
    main()
