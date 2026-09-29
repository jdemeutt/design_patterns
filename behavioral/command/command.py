"""
Command pattern - standalone example
=======================================

Scenario: a simple text document editor. Every edit (insert text, delete
text) is wrapped in a Command object with execute() and undo() methods.
An Invoker (the editor's toolbar / undo manager) triggers commands and
keeps a history, enabling full undo/redo without knowing anything about
what each command actually does.

Run directly:
    python3 command.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


# ---- Receiver --------------------------------------------------------

class Document:
    """The object commands actually operate on."""

    def __init__(self) -> None:
        self.text = ""

    def insert(self, position: int, text: str) -> None:
        self.text = self.text[:position] + text + self.text[position:]

    def delete(self, position: int, length: int) -> str:
        removed = self.text[position:position + length]
        self.text = self.text[:position] + self.text[position + length:]
        return removed

    def __str__(self) -> str:
        return f"'{self.text}'"


# ---- Command interface -------------------------------------------------

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...

    @abstractmethod
    def undo(self) -> None:
        ...


# ---- Concrete commands ----------------------------------------------

class InsertTextCommand(Command):
    def __init__(self, document: Document, position: int, text: str) -> None:
        self._document = document
        self._position = position
        self._text = text

    def execute(self) -> None:
        self._document.insert(self._position, self._text)

    def undo(self) -> None:
        self._document.delete(self._position, len(self._text))


class DeleteTextCommand(Command):
    def __init__(self, document: Document, position: int, length: int) -> None:
        self._document = document
        self._position = position
        self._length = length
        self._deleted_text = ""  # captured on execute(), needed for undo()

    def execute(self) -> None:
        self._deleted_text = self._document.delete(self._position, self._length)

    def undo(self) -> None:
        self._document.insert(self._position, self._deleted_text)


class MacroCommand(Command):
    """A command composed of several other commands -- demonstrates
    composing simple commands into a single higher-level operation."""

    def __init__(self, commands: List[Command]) -> None:
        self._commands = commands

    def execute(self) -> None:
        for command in self._commands:
            command.execute()

    def undo(self) -> None:
        for command in reversed(self._commands):
            command.undo()


# ---- Invoker (keeps history for undo/redo) -----------------------------

class EditorInvoker:
    def __init__(self) -> None:
        self._history: List[Command] = []
        self._undone: List[Command] = []

    def do(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        self._undone.clear()  # a new action invalidates the redo stack

    def undo(self) -> None:
        if not self._history:
            print("  Nothing to undo.")
            return
        command = self._history.pop()
        command.undo()
        self._undone.append(command)

    def redo(self) -> None:
        if not self._undone:
            print("  Nothing to redo.")
            return
        command = self._undone.pop()
        command.execute()
        self._history.append(command)


def main() -> None:
    print("=== Command demo ===\n")

    doc = Document()
    editor = EditorInvoker()

    editor.do(InsertTextCommand(doc, 0, "Hello, world!"))
    print(f"After insert: {doc}")

    editor.do(InsertTextCommand(doc, 5, " there"))
    print(f"After 2nd insert: {doc}")

    editor.do(DeleteTextCommand(doc, 0, 6))
    print(f"After delete: {doc}")

    print("\n--- undoing twice ---")
    editor.undo()
    print(f"After undo #1: {doc}")
    editor.undo()
    print(f"After undo #2: {doc}")

    print("\n--- redoing once ---")
    editor.redo()
    print(f"After redo: {doc}")

    print("\n--- macro command: several edits treated as one command ---")
    doc2 = Document()
    editor2 = EditorInvoker()
    macro = MacroCommand([
        InsertTextCommand(doc2, 0, "one "),
        InsertTextCommand(doc2, 4, "two "),
        InsertTextCommand(doc2, 8, "three"),
    ])
    editor2.do(macro)
    print(f"After macro execute: {doc2}")
    editor2.undo()
    print(f"After macro undo (reverses all 3 steps at once): {doc2}")


if __name__ == "__main__":
    main()
