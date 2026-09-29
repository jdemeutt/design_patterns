# Memento

**Category:** Behavioral

## Intent

Without violating encapsulation, capture and externalize an object's
internal state so that the object can be restored to this state later.

## Motivation

Undo functionality, checkpoints, and save/restore features all need a way
to snapshot an object's state and bring it back later. The naive approach
— exposing all of an object's internal fields publicly so external undo
logic can read and rewrite them — breaks encapsulation and couples the
undo mechanism tightly to the object's internal representation.

Memento solves this with three roles:

- The **Originator** is the object whose state needs saving. It knows how
  to create a `Memento` snapshot of its own current state, and how to
  restore itself from a given memento — but the memento's *contents* are
  opaque to everyone else.
- The **Memento** stores that snapshot. It exposes little to nothing to
  outside code (other than perhaps metadata like a timestamp/label) —
  only the `Originator` that created it knows how to interpret its
  internal state.
- The **Caretaker** keeps a history of mementos (e.g., a stack, for undo)
  but never looks inside them or modifies them — it just requests new
  mementos and hands old ones back to the originator to restore.

## Structure

```
Caretaker                     Originator                    Memento
+------------------+          +------------------+          +----------------+
| -history: [Memento]|--------> +create_memento()   |--------> | (opaque state,  |
| +save()            |         | +restore(memento) |<---------|  readable only  |
| +undo()            |         +------------------+          |  by Originator) |
+------------------+                                        +----------------+
```

The Caretaker never inspects or mutates a Memento's contents — it only
stores and returns them, preserving the Originator's encapsulation.

## Pros

- Preserves encapsulation: internal state is exposed only to the
  originator that produced it, not to the caretaker or other code.
- Simplifies the originator: it doesn't need to track its own history —
  that responsibility is delegated to the caretaker.
- Makes it straightforward to implement undo/redo, checkpoints,
  transactional rollback, or "save game" functionality cleanly.

## Cons

- Storing many mementos, especially of large objects, can consume a lot of
  memory — worth considering incremental/diff-based snapshots for large
  state instead of full copies each time.
- If the language doesn't have a way to restrict memento access to only
  the originator (Python has no true "private" access), true encapsulation
  relies on convention (e.g., a leading underscore) rather than enforced
  language rules.
- The caretaker still needs to manage the lifecycle of mementos (how many
  to keep, when to discard old ones) which is extra bookkeeping logic on
  its own side.

## When to use it

- You need to implement undo/redo functionality without exposing an
  object's internal implementation details to the code managing history.
- You want to take periodic snapshots of an object's state for rollback,
  checkpointing, or "save/load" features.
- Direct access to an object's fields to save/restore state would violate
  encapsulation you want to preserve.

## When *not* to use it

- The object's state is trivial (a couple of public fields) — just copy
  the fields directly, a formal Memento is unnecessary ceremony.
- Snapshots would be so large or so frequent that memory/performance
  becomes a real concern, without a mitigation strategy (e.g., diffs,
  compression, or limiting history depth).

## Real-world use cases

- Undo/redo stacks in editors (text, image, code) — this pattern pairs
  extremely well with **Command**, where each undoable command also
  captures a memento of state before it executed.
- "Save game" / checkpoint systems in games, and database
  transaction/rollback mechanisms conceptually mirror this pattern.
- Python's own `pickle` module (or `copy.deepcopy`) is frequently used as
  the underlying mechanism to actually capture an object's full state into
  a memento.
- Form-editing UIs that let a user "cancel" and revert all changes back to
  the state before they started editing.

## Related patterns

- **Command** and Memento are frequently combined: each executed command
  stores a memento of the receiver's state *before* it ran, so `undo()`
  can restore that memento instead of needing custom reverse logic per
  command.
- **Iterator** can be used to traverse the caretaker's history of
  mementos.
- Differs from **Prototype** in intent: Prototype is about creating new
  independent objects by cloning; Memento is about capturing a *snapshot
  of one object's own history* to restore that same object later.
