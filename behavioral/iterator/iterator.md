# Iterator

**Category:** Behavioral

## Intent

Provide a way to access the elements of an aggregate object sequentially
without exposing its underlying representation.

## Motivation

A collection (a list, a tree, a custom data structure) needs to support
being "walked through" element by element. If client code had to know the
collection's internal representation to do that (e.g., manually indexing
into an internal array, or manually managing tree traversal state), the
client would be tightly coupled to implementation details that should be
free to change. Iterator separates "how to traverse" from "what the
collection stores", by introducing an object (the **iterator**) that
tracks traversal position and exposes a uniform way to get the next
element, regardless of what kind of collection is underneath.

This also allows **multiple simultaneous, independent traversals** of the
same collection (each iterator has its own position), and lets a single
collection support **multiple traversal strategies** (e.g., forward,
backward, breadth-first, depth-first) via different iterator classes.

## Structure

```
Aggregate (interface)              Iterator (interface)
+-------------------+              +------------------+
| +create_iterator()  |------------> | +has_next()       |
+-------------------+              | +next()           |
        ^                          +------------------+
+-------+--------+                          ^
ConcreteAggregate               +-----------+-----------+
(holds the actual data)         |                       |
                         ConcreteIteratorA      ConcreteIteratorB
                         (e.g. forward)         (e.g. reverse)
```

## Python-specific notes

Python has **first-class, built-in support for this pattern** via the
iterator protocol:

- Any object implementing `__iter__` (returning an iterator) is
  "iterable" and works with `for x in obj:`.
- Any object implementing `__next__` (and typically `__iter__` returning
  `self`) is an "iterator" per `next(it)` / `StopIteration`.
- **Generators** (`yield`) let you write an iterator's traversal logic as
  simple, linear code instead of hand-rolling a stateful class — this is
  the idiomatic way to implement Iterator in Python for most cases.

## Pros

- **Single Responsibility Principle**: traversal logic lives in the
  iterator, separate from the collection's storage/management logic.
- **Open/Closed Principle**: new traversal algorithms (e.g., a new
  "zig-zag" order) can be added as new iterator classes without changing
  the aggregate.
- Supports multiple independent traversals of the same collection
  simultaneously (each iterator tracks its own position).
- Hides the collection's internal representation completely from client
  code, which only interacts through `has_next()`/`next()` (or Python's
  `for`/`next()`).

## Cons

- For simple, built-in collection types this is often overkill — using a
  plain `for` loop over a list is already an Iterator in disguise, so
  hand-rolling one rarely pays off unless the traversal logic itself is
  non-trivial (e.g., traversing a custom tree, paginating a remote API).
- Maintaining separate iterator state (especially for complex/concurrent
  traversal, e.g. removing elements from a collection while iterating it)
  can introduce subtle bugs if not handled carefully.

## When to use it

- You need to traverse a custom collection/data structure (a tree, graph,
  or other non-linear structure) without exposing how it's stored
  internally.
- You want to support multiple, independent, or simultaneous traversals of
  the same collection.
- You want to provide a uniform traversal interface across several
  different kinds of collections (e.g., iterating over both a list-based
  and tree-based collection the same way).
- You're consuming a large or infinite sequence lazily, one item at a
  time, without materializing the whole thing in memory (Python
  generators excel here).

## When *not* to use it

- A built-in collection (`list`, `dict`, `set`) already supports iteration
  natively — there's nothing to add.
- The traversal is a one-off, simple loop with no reuse value — a plain
  `for` loop or list comprehension is clearer.

## Real-world use cases

- Every `for` loop in Python is powered by this exact pattern under the
  hood (`iter()`/`next()`).
- Database cursors that fetch rows lazily, one batch at a time, instead of
  loading an entire result set into memory.
- Paginated API clients that present "iterate over all results" while
  internally fetching pages behind the scenes.
- Tree/graph traversal utilities (file system walkers like `os.walk`,
  DOM/AST traversal) that hide the recursive traversal logic behind a flat
  iteration interface.

## Related patterns

- **Composite** structures are very commonly traversed via an Iterator
  that hides the recursive tree-walking.
- **Factory Method** is often used by an aggregate's `create_iterator()`
  method to produce the right kind of iterator.
- **Visitor** can traverse a structure similarly to Iterator, but Visitor
  additionally lets you define new *operations* on the elements visited,
  while Iterator focuses purely on traversal/access.
