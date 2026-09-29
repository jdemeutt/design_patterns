# Bridge

**Category:** Structural

## Intent

Decouple an **abstraction** from its **implementation** so the two can
vary independently, instead of being locked together in a single
inheritance hierarchy.

## Motivation

Imagine you have shapes (`Circle`, `Square`) that each need to be rendered
via different rendering engines (`VectorRenderer`, `RasterRenderer`). If
you model this with straightforward inheritance, you end up needing one
class per combination: `VectorCircle`, `RasterCircle`, `VectorSquare`,
`RasterSquare`... Adding a new shape *or* a new renderer multiplies the
number of classes you need ("combinatorial explosion").

Bridge solves this by splitting the two dimensions into **two separate
hierarchies** — `Shape` (the abstraction) and `Renderer` (the
implementation) — connected by composition: a `Shape` *holds a reference
to* a `Renderer` instead of inheriting behavior tied to a specific
renderer. Now `N` shapes and `M` renderers only need `N + M` classes, not
`N x M`, and either hierarchy can grow without touching the other.

## Structure

```
Abstraction                         Implementor (interface)
+------------------+                +--------------------+
| -implementor      |---has-a------>| +operation_impl()    |
| +operation()      |                +--------------------+
+--------+---------+                          ^
         ^                          +---------+---------+
+--------+---------+                |                    |
RefinedAbstraction  ConcreteImplA  ConcreteImplB
```

- `Abstraction.operation()` delegates the actual work to
  `self.implementor.operation_impl()`.
- Both the `Abstraction` hierarchy and the `Implementor` hierarchy can be
  extended independently.

## Pros

- Avoids the combinatorial class explosion of `N x M` subclasses when two
  dimensions of variation exist.
- Lets you swap implementations at runtime by changing which
  `Implementor` an `Abstraction` holds.
- **Open/Closed Principle**: new abstractions and new implementations can
  be added independently, each in their own hierarchy.
- Hides implementation details from client code entirely, behind the
  abstraction's interface.

## Cons

- Adds indirection and more moving parts than a single, simple hierarchy —
  overkill if you never actually expect a second dimension of variation.
- Can be harder to design correctly up front: you must correctly identify
  which parts of the system are "abstraction" and which are
  "implementation" before writing code, which requires some foresight.

## When to use it

- You want to avoid a permanent binding between an abstraction and one
  particular implementation (e.g., support swapping database drivers,
  rendering backends, or platform-specific code at runtime).
- Both the abstraction and its implementation should be independently
  extensible via subclassing, without every combination needing its own
  class.
- You want to hide implementation details of an abstraction completely
  from client code (across even process/library boundaries).

## When *not* to use it

- There's genuinely only one dimension of variation (only shapes,
  never multiple renderers) — plain inheritance is simpler.
- The two "hierarchies" would each only ever have one member — Bridge
  adds structure for a distinction that doesn't exist yet.

## Real-world use cases

- Cross-platform GUI frameworks where the same widget abstraction
  (`Window`, `Button`) is implemented differently per OS
  (`WindowsWindowImpl`, `MacWindowImpl`).
- Database drivers: a single `Connection` abstraction bridging to
  different underlying driver implementations (`SQLiteImpl`,
  `PostgresImpl`).
- Python's own logging framework: `Logger` (abstraction) is decoupled
  from `Handler`s (implementation) — you can attach a `StreamHandler`,
  `FileHandler`, or `SMTPHandler` to the same logger interface.
- Device drivers: a `RemoteControl` abstraction bridged to different
  `Device` implementations (`TV`, `Radio`).

## Related patterns

- Similar structure to **Adapter**, but different intent: Adapter is
  applied *after the fact* to make incompatible interfaces work together;
  Bridge is designed *up front* to let two hierarchies evolve
  independently.
- **Abstract Factory** can be used to create the right `Implementor` for a
  given `Abstraction` at runtime.
- **Strategy** looks structurally similar (an object holding a reference
  to an interchangeable behavior), but Strategy is about swapping
  *algorithms*, while Bridge is about decoupling a whole class hierarchy
  from its implementation hierarchy.
