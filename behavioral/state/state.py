"""
State pattern - standalone example
=====================================

Scenario: a simplified traffic light / document-workflow-style state
machine using a Document object that moves through Draft -> Review ->
Published -> Archived states. Each state is its own class implementing the
same interface; Document.publish()/review()/archive() delegate to
whichever state object is currently active, and the behavior (and allowed
transitions) automatically changes as the state changes.

Run directly:
    python3 state.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# ---- State interface -------------------------------------------------

class DocumentState(ABC):
    @abstractmethod
    def submit_for_review(self, document: "Document") -> None:
        ...

    @abstractmethod
    def approve(self, document: "Document") -> None:
        ...

    @abstractmethod
    def archive(self, document: "Document") -> None:
        ...

    def name(self) -> str:
        return self.__class__.__name__


# ---- Concrete states ---------------------------------------------------

class Draft(DocumentState):
    def submit_for_review(self, document: "Document") -> None:
        print("  Draft -> Review: submitting for review.")
        document.transition_to(Review())

    def approve(self, document: "Document") -> None:
        print("  Cannot approve: document hasn't been submitted for review yet.")

    def archive(self, document: "Document") -> None:
        print("  Draft -> Archived: discarding an unfinished draft.")
        document.transition_to(Archived())


class Review(DocumentState):
    def submit_for_review(self, document: "Document") -> None:
        print("  Already in review; no action taken.")

    def approve(self, document: "Document") -> None:
        print("  Review -> Published: approved and publishing.")
        document.transition_to(Published())

    def archive(self, document: "Document") -> None:
        print("  Review -> Archived: rejecting and archiving.")
        document.transition_to(Archived())


class Published(DocumentState):
    def submit_for_review(self, document: "Document") -> None:
        print("  Cannot submit for review: document is already published.")

    def approve(self, document: "Document") -> None:
        print("  Document is already published; nothing to approve.")

    def archive(self, document: "Document") -> None:
        print("  Published -> Archived: retiring the document.")
        document.transition_to(Archived())


class Archived(DocumentState):
    def submit_for_review(self, document: "Document") -> None:
        print("  Cannot submit for review: document is archived (final state).")

    def approve(self, document: "Document") -> None:
        print("  Cannot approve: document is archived (final state).")

    def archive(self, document: "Document") -> None:
        print("  Document is already archived.")


# ---- Context -----------------------------------------------------------

class Document:
    def __init__(self) -> None:
        self._state: DocumentState = Draft()

    def transition_to(self, state: DocumentState) -> None:
        self._state = state
        print(f"    [Document] state is now: {self._state.name()}")

    def submit_for_review(self) -> None:
        self._state.submit_for_review(self)

    def approve(self) -> None:
        self._state.approve(self)

    def archive(self) -> None:
        self._state.archive(self)

    @property
    def state_name(self) -> str:
        return self._state.name()


def main() -> None:
    print("=== State demo ===\n")

    doc = Document()
    print(f"Initial state: {doc.state_name}\n")

    print("Trying to approve a Draft directly (invalid transition):")
    doc.approve()

    print("\nSubmitting for review:")
    doc.submit_for_review()

    print("\nApproving (publishing):")
    doc.approve()

    print("\nTrying to submit an already-published document for review:")
    doc.submit_for_review()

    print("\nArchiving the published document:")
    doc.archive()

    print("\nTrying to approve an archived document:")
    doc.approve()

    print(f"\nFinal state: {doc.state_name}")


if __name__ == "__main__":
    main()
