# Builder

**Category:** Creational

## Intent

Separate the construction of a complex object from its representation, so
that the same construction process can create different representations,
and so that objects with many optional parts don't require a constructor
with an unmanageable number of parameters.

## Motivation

Consider constructing an HTTP request, a computer, or an HTML document.
Each has many optional parts (headers, body, query params; RAM, GPU,
storage; head, body, scripts). A single constructor trying to cover every
combination either:

- needs a huge parameter list where most arguments are `None`/default most
  of the time (the "telescoping constructor" problem), or
- forces the object to be built in a series of error-prone manual steps
  scattered through client code.

Builder solves this by introducing a separate object (the **Builder**)
whose entire job is to accumulate the pieces step by step, exposing a
fluent, readable API, and only producing the final, possibly immutable,
object when explicitly asked to (`build()`).

## Structure

```
Director                Builder (interface)         ConcreteBuilder
+---------------+       +-------------------+       +-------------------+
| +construct()   |------>| +set_part_a()      |<------|                    |
+---------------+       | +set_part_b()      |       | +get_result()      |
                        | +get_result()      |       +-------------------+
                        +-------------------+                |
                                                               v
                                                          Product
```

- The `Builder` exposes step methods for each part of construction.
- A `Director` (optional) knows *which* steps to call and in what order
  to produce a particular configuration, but doesn't know the details of
  how each step works.
- Client code can also skip the Director and drive the Builder directly
  for full custom control — this is extremely common in Python, often via
  **method chaining** (a "fluent interface").

## Pros

- Lets you construct objects step-by-step, defer construction steps, or
  run steps recursively — impossible with a single constructor call.
- Avoids telescoping constructors / huge parameter lists.
- The same construction process (Director) can produce different
  representations by swapping in a different Builder.
- Encapsulates the complex assembly/validation logic in one place instead
  of spreading it through client code.
- Enables you to produce **immutable** final objects: the builder holds
  mutable state during construction, but `build()` returns a frozen
  object.

## Cons

- Introduces multiple new classes/objects (Builder, sometimes Director),
  which is unnecessary overhead for simple objects with few, mandatory
  fields.
- In Python, keyword arguments with defaults, `@dataclass`, or
  `attrs`/`pydantic` models often solve the "many optional fields"
  problem more concisely than a full Builder hierarchy — Builder earns
  its keep mainly when construction involves multi-step *logic*
  (validation, ordering constraints, incremental assembly), not just a
  lot of optional data.

## When to use it

- An object has many optional components/configuration and you want a
  readable way to construct it (fluent method chaining).
- The construction process must produce different representations of
  the same object (e.g., exporting the same document model to HTML vs.
  Markdown vs. plain text via different builders).
- Construction requires several ordered steps, some of which depend on
  earlier steps, and you want to enforce/encapsulate that ordering.
- You want to keep the "product" object immutable once fully built.

## When *not* to use it

- A `@dataclass` / named constructor with sensible keyword defaults
  already reads cleanly.
- There is no real assembly logic beyond "collect these fields" — a
  Builder would only add ceremony.

## Real-world use cases

- SQL query builders (`.select(...).where(...).order_by(...).build()`).
- HTTP client/request builders (`requests`-like libraries, `URL` builders).
- Test data builders / object mothers in test suites, for constructing
  complex fixture objects with sensible defaults and a few overrides.
- UI layout builders that assemble a widget tree step by step.
- Python's own `str.join`, or libraries like SQLAlchemy's `Query` object,
  are conceptually Builders using fluent chaining.

## Related patterns

- **Abstract Factory** focuses on families of *simple* related products
  created in one call; **Builder** focuses on step-by-step construction of
  *one* complex product, possibly across many calls.
- A **Composite** tree is often assembled using a Builder.
- Builder can be combined with **Director + Strategy** to vary the
  assembly *algorithm* while keeping the same builder steps.
