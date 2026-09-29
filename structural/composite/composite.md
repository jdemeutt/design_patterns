# Composite

**Category:** Structural

## Intent

Compose objects into tree structures to represent part-whole hierarchies.
Composite lets clients treat individual objects (**leaves**) and
compositions of objects (**composites**/containers) **uniformly**.

## Motivation

Think of a filesystem: a `File` is a single item; a `Folder` can contain
both `File`s and other `Folder`s. If you want to compute "total size", you
want to call `.size()` the same way on a lone file and on a deeply nested
folder — without the calling code having to check "is this a file or a
folder?" and branch accordingly.

Composite defines a common interface (`Component`) that both leaf objects
and container objects implement. A container simply implements its
operations by delegating to (and combining the results of) its children,
which may themselves be leaves or further containers — the recursion
handles arbitrary nesting depth transparently.

## Structure

```
              Component (interface)
              +-------------------+
              | +operation()       |
              | +add(child)        |
              | +remove(child)     |
              +---------+---------+
                        ^
           +------------+------------+
           |                         |
        Leaf                     Composite
   +-----------+          +----------------------+
   |+operation()|          | +operation()          |
   +-----------+          | -children: [Component] |
                          +----------------------+
                                    |
                          each child.operation()
                          is a Leaf or Composite
```

## Pros

- Client code can treat individual objects and compositions uniformly —
  no `isinstance` checks or branching needed to handle "is this one thing
  or a group of things?".
- Makes it easy to add new kinds of components (new leaf or composite
  types) without changing existing client code (**Open/Closed
  Principle**).
- Naturally represents recursive, tree-shaped domain data: filesystems,
  UI widget trees, organization charts, nested menus, arithmetic
  expressions.
- Operations that would otherwise require manual recursive traversal code
  scattered through the client become a single polymorphic method call.

## Cons

- Can make the design overly general: it becomes tempting to give every
  `Component` the same interface (including `add`/`remove`) even for
  leaves where "adding a child" makes no sense, which either throws at
  runtime or requires extra interface segregation.
- Harder to restrict what kind of children a particular composite may
  contain (e.g., "a `Menu` can hold `MenuItem`s but not other top-level
  `Menu`s") purely through the type system — this often needs runtime
  checks.
- Deeply nested trees can make debugging and reasoning about behavior
  (e.g., where an exception originated) harder, since operations are
  spread recursively across many objects.

## When to use it

- Your domain data is naturally a part-whole hierarchy / tree (folders and
  files, organization structure, UI component trees, nested
  bill-of-materials).
- You want client code to be able to ignore the difference between a
  single object and a group of objects of the same conceptual type.
- You expect the recursive structure to be manipulated uniformly:
  computing totals, rendering, validating, searching, and so on.

## When *not* to use it

- Your data isn't actually recursive/tree-shaped — forcing a flat
  structure into Composite adds complexity for nothing.
- Leaves and containers have such different capabilities that a shared
  interface would be mostly meaningless stubs.

## Real-world use cases

- Filesystem trees (files & directories) — the canonical example.
- GUI toolkits: a `Panel` (composite) containing `Button`s, `Label`s, and
  other `Panel`s (all implementing `Widget`).
- Organization charts: an `Employee` can be an individual contributor
  (leaf) or a `Manager` (composite) with reports.
- Abstract syntax trees for expressions/queries: a `BinaryExpression`
  composite of two `Expression` children (which may themselves be leaves
  like `Literal` or further composites).
- `xml.etree.ElementTree` in Python's standard library: an `Element` can
  contain further `Element` children, and operations traverse uniformly.

## Related patterns

- **Iterator** is frequently used to traverse a Composite tree without
  exposing its internal structure.
- **Visitor** is often used to define new operations over a Composite
  tree's elements without modifying the component classes themselves.
- **Decorator** has a similar recursive/nested structure but a different
  intent: Decorator adds responsibilities to a single object, while
  Composite represents a part-whole hierarchy of many objects.
