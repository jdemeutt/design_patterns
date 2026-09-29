"""
Memento pattern - standalone example
=======================================

Scenario: a simple text editor that supports undo. The TextEditor
(Originator) can produce an opaque EditorMemento snapshot of its current
state and restore itself from one later. A History object (Caretaker)
stores a stack of mementos but never looks inside them -- it just asks
the editor to save/restore.

Run directly:
    python3 memento.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


# ---- Memento --------------------------------------------------------------

@dataclass(frozen=True)
class EditorMemento:
    """Immutable snapshot. Its fields are intentionally treated as opaque
    by everyone except TextEditor -- the Caretaker never reads or writes
    them, it just stores and returns the object as a whole."""

    _content: str
    _cursor_position: int


# ---- Originator ------------------------------------------------------

class TextEditor:
    def __init__(self) -> None:
        self.content: str = ""
        self.cursor_position: int = 0

    def type(self, text: str) -> None:
        self.content = (
            self.content[: self.cursor_position]
            + text
            + self.content[self.cursor_position:]
        )
        self.cursor_position += len(text)

    def save(self) -> EditorMemento:
        """Create a snapshot of the current state."""
        return EditorMemento(self.content, self.cursor_position)

    def restore(self, memento: EditorMemento) -> None:
        """Restore state from a previously saved snapshot."""
        self.content = memento._content
        self.cursor_position = memento._cursor_position

    def __str__(self) -> str:
        marker_pos = self.cursor_position
        return f"'{self.content[:marker_pos]}|{self.content[marker_pos:]}'"


# ---- Caretaker -------------------------------------------------------

class History:
    """Stores mementos for undo, without ever inspecting their contents."""

    def __init__(self) -> None:
        self._stack: List[EditorMemento] = []

    def push(self, memento: EditorMemento) -> None:
        self._stack.append(memento)

    def pop(self) -> EditorMemento:
        if not self._stack:
            raise IndexError("No history to undo.")
        return self._stack.pop()

    def __len__(self) -> int:
        return len(self._stack)


def main() -> None:
    print("=== Memento demo ===\n")

    editor = TextEditor()
    history = History()

    # Save a checkpoint before each edit so we can undo back to it.
    history.push(editor.save())
    editor.type("Hello")
    print(f"After typing 'Hello':        {editor}")

    history.push(editor.save())
    editor.type(", world")
    print(f"After typing ', world':      {editor}")

    history.push(editor.save())
    editor.type("!!!")
    print(f"After typing '!!!':          {editor}")

    print(f"\nHistory currently holds {len(history)} checkpoints.\n")

    print("-- Undoing three times --")
    editor.restore(history.pop())
    print(f"Undo #1: {editor}")

    editor.restore(history.pop())
    print(f"Undo #2: {editor}")

    editor.restore(history.pop())
    print(f"Undo #3: {editor}")

    print("\n--- the Caretaker (History) never read or modified memento internals ---")
    print(f"Remaining history size: {len(history)}")


if __name__ == "__main__":
    main()
