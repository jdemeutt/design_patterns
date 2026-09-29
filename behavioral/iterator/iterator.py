"""
Iterator pattern - standalone example
========================================

Scenario: a custom "BookShelf" collection that needs to support traversal
without exposing its internal storage. We show three levels of the same
idea:

1. A hand-rolled ConcreteIterator class implementing has_next()/next(),
   as in the classic GoF description.
2. The same collection made "properly Pythonic" by implementing the
   __iter__/__next__ protocol so it works with a normal `for` loop.
3. A generator-based iterator (the idiomatic, least-boilerplate way to
   write custom iteration logic in Python) supporting a different
   traversal order (reverse) without touching the collection's storage.

Run directly:
    python3 iterator.py
"""

from __future__ import annotations

from typing import Iterator as TypingIterator
from typing import List


class Book:
    def __init__(self, title: str, author: str) -> None:
        self.title = title
        self.author = author

    def __repr__(self) -> str:
        return f"'{self.title}' by {self.author}"


# ---- 1. Classic, hand-rolled Iterator (GoF-style) -----------------------

class BookShelfIterator:
    """A standalone iterator object tracking its own position, independent
    of any other iterator over the same shelf."""

    def __init__(self, books: List[Book]) -> None:
        self._books = books
        self._position = 0

    def has_next(self) -> bool:
        return self._position < len(self._books)

    def next(self) -> Book:
        book = self._books[self._position]
        self._position += 1
        return book


class BookShelf:
    """The aggregate. Exposes create_iterator() without revealing that
    it's backed by a plain list internally (could be a linked list, a
    database query, etc. -- callers wouldn't know)."""

    def __init__(self) -> None:
        self._books: List[Book] = []

    def add(self, book: Book) -> None:
        self._books.append(book)

    def create_iterator(self) -> BookShelfIterator:
        return BookShelfIterator(self._books)

    # ---- 2. Pythonic iterator protocol, so `for book in shelf` works ----
    def __iter__(self) -> TypingIterator[Book]:
        return iter(self._books)

    # ---- 3. A second, independent traversal order via a generator ------
    def reverse_iterator(self) -> TypingIterator[Book]:
        for book in reversed(self._books):
            yield book

    def __len__(self) -> int:
        return len(self._books)


def main() -> None:
    print("=== Iterator demo ===\n")

    shelf = BookShelf()
    shelf.add(Book("Design Patterns", "Gang of Four"))
    shelf.add(Book("Clean Code", "Robert C. Martin"))
    shelf.add(Book("The Pragmatic Programmer", "Hunt & Thomas"))

    print("-- 1. Hand-rolled iterator (has_next()/next()) --")
    it = shelf.create_iterator()
    while it.has_next():
        print(f"  {it.next()}")

    print("\n-- 2. Two INDEPENDENT hand-rolled iterators over the same shelf --")
    it_a = shelf.create_iterator()
    it_b = shelf.create_iterator()
    print(f"  it_a.next() -> {it_a.next()}")
    print(f"  it_a.next() -> {it_a.next()}")
    print(f"  it_b.next() -> {it_b.next()}  (it_b is unaffected by it_a's progress)")

    print("\n-- 3. Pythonic iteration via __iter__ (plain 'for' loop) --")
    for book in shelf:
        print(f"  {book}")

    print("\n-- 4. Alternate traversal order via a generator, no shelf changes needed --")
    for book in shelf.reverse_iterator():
        print(f"  {book}")


if __name__ == "__main__":
    main()
