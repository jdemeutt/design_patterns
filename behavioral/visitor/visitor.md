# Visitor

**Category:** Behavioral

## Intent

Represent an operation to be performed on the elements of an object
structure. Visitor lets you define a new operation without changing the
classes of the elements on which it operates.

## Motivation

Suppose you have a stable class hierarchy of shapes (`Circle`, `Square`,
`Triangle`) and you need to perform several unrelated operations on them
over time: compute area, render to SVG, export to JSON, validate geometry.
Putting every operation as a method directly on each shape class works
initially, but every time you think of a *new* operation, you must revisit
and modify *every single shape class* to add it — this violates the
Open/Closed Principle and clutters the shape classes with concerns
unrelated to "being a shape".

Visitor flips the direction of this dependency using a technique called
**double dispatch**: each element class gets one small, stable `accept(visitor)`
method that simply calls back into the visitor
(`visitor.visit_circle(self)`), and all the operation-specific logic lives
in separate `Visitor` subclasses instead — one per operation. Adding a new
operation means adding a new `Visitor` subclass, with zero changes to any
element class.

## Structure

```
Element (interface)                     Visitor (interface)
+------------------+                    +----------------------+
| +accept(visitor)   |------------------>| +visit_circle(c)       |
+------------------+                    | +visit_square(s)       |
        ^                                +----------------------+
+-------+--------+                                 ^
|                |                        +---------+---------+
Circle          Square                    |                   |
+---------------+   +---------------+  AreaVisitor       RenderVisitor
| accept(v):       |   | accept(v):    |
|   v.visit_circle |   |   v.visit_square|
|      (self)       |   |      (self)    |
+---------------+   +---------------+
```

**Double dispatch**: `element.accept(visitor)` calls
`visitor.visit_<concrete_type>(element)` — the *actual runtime type* of
both the element *and* the visitor determine which method body runs,
which is how Visitor achieves per-type behavior without `isinstance`
checks or modifying element classes.

## Pros

- Adds new operations over an existing object structure without modifying
  any of the element classes (**Open/Closed Principle**), as long as the
  element hierarchy itself doesn't change.
- Gathers related behavior that would otherwise be scattered thinly across
  many element classes into one cohesive visitor class per operation —
  useful when operations are more numerous/likely to change than element
  types are.
- Can accumulate state across a traversal (e.g., a visitor summing areas
  across a whole shape collection) more naturally than if the logic were
  smeared across each element's own method.

## Cons

- Adding a **new element type** requires updating the `Visitor` interface
  and *every* concrete visitor class to handle it — the opposite trade-off
  from adding operations. Visitor is a poor fit if the element hierarchy
  changes often.
- Breaks encapsulation somewhat: visitors often need access to element
  internals that wouldn't otherwise need to be exposed, to do their work
  from outside the element class.
- Adds noticeable ceremony (the accept/visit double-dispatch machinery) —
  in Python this is often replaced by simpler alternatives like
  `functools.singledispatch`, an `isinstance` chain, or a dictionary
  dispatching on `type(element)`, especially since Python doesn't need
  true double dispatch to inspect an object's runtime type.

## When to use it

- An object structure contains many different classes and you need to
  perform several distinct, unrelated operations on its elements, where
  operations change/grow more often than the element types themselves.
- You want to keep unrelated operations (rendering, exporting, validating)
  out of the element classes, whose primary responsibility is just
  representing the data/structure.
- You need to accumulate information across a traversal of a heterogeneous
  structure (e.g., total cost across a shopping cart of different item
  types).

## When *not* to use it

- The element hierarchy changes frequently — you'd be constantly updating
  every visitor.
- Python's `functools.singledispatch`, plain `isinstance` checks, or a
  type-keyed dictionary would achieve the same per-type dispatch far more
  simply, which is very often true for small hierarchies in Python.

## Real-world use cases

- Compiler/interpreter AST processing: separate visitors for type
  checking, code generation, optimization, and pretty-printing, all
  operating over the same fixed set of AST node classes.
- `ast.NodeVisitor` in Python's own standard library is a direct,
  textbook implementation of this pattern for walking Python syntax
  trees.
- Document object models (rendering the same document tree to HTML, PDF,
  or plain text via different visitors).
- Static analysis tools/linters that walk a fixed code structure applying
  many different independent checks (each check is a visitor).

## Related patterns

- Almost always applied to a **Composite** structure (the "object
  structure" being visited is typically a composite tree).
- **Iterator** is often used internally to walk the structure while each
  element's `accept()` is invoked.
- Python's `functools.singledispatch` provides a lighter-weight,
  decorator-based alternative that achieves similar type-based dispatch
  without a formal Visitor class hierarchy.
