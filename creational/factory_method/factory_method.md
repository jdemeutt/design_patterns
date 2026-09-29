# Factory Method

**Category:** Creational

## Intent

Define an interface for creating an object, but let **subclasses decide
which class to instantiate**. Factory Method lets a class defer
instantiation to subclasses.

## Motivation

Imagine a logistics application that plans deliveries. At first it only
supports trucks (road transport). If the class that plans a delivery
directly instantiates `Truck` everywhere, adding `Ship` (sea transport)
later means hunting down and modifying every place a `Truck` was created.

Factory Method fixes this by putting object creation behind a method — a
"factory method" — that subclasses (or, in Python, a configurable
callable/registry) override to produce the right concrete product, while
the calling code only ever depends on the abstract `Transport` interface.

## Structure

```
        Creator (abstract)                  Product (abstract)
        +------------------+                +----------------+
        | +factory_method() |--- creates --> |                |
        | +some_operation() |                +----------------+
        +------------------+                        ^
                 ^                                   |
     +-----------+-----------+            +----------+----------+
     |                       |            |                     |
TruckCreator            ShipCreator      Truck                 Ship
```

- `Creator.some_operation()` contains business logic that is written
  entirely in terms of the abstract `Product`, and calls
  `self.factory_method()` whenever it needs a new product instance.
- Each `ConcreteCreator` overrides `factory_method()` to return a specific
  `ConcreteProduct`.

## Pros

- Removes the binding between a class and the concrete classes it must
  instantiate — the "creator" code depends only on abstractions.
- **Open/Closed Principle**: you can introduce new product types by adding
  a new creator subclass, without touching existing client code.
- **Single Responsibility Principle**: the creation logic lives in one
  place instead of being scattered across the codebase.
- Great for frameworks/libraries that need to let user code plug in custom
  types without the framework knowing about them in advance.

## Cons

- Introduces an extra hierarchy of creator classes purely to produce
  objects, which can feel like ceremony for simple cases.
- Can require parallel class hierarchies (one hierarchy of products, one
  of creators), which adds files and indirection.
- In Python, a lot of Factory Method's value is available more cheaply
  through first-class functions, a dictionary-based registry, or simply
  passing a class/constructor as an argument — full subclassing is often
  unnecessary.

## When to use it

- A class can't anticipate the exact class of objects it needs to create
  ahead of time (e.g., a plugin system).
- You want to give users of your library/framework a way to extend which
  objects get created, by subclassing, without changing your code.
- You want to centralize and reuse object-creation code that's duplicated
  across the codebase.

## When *not* to use it

- There's only one product type and no realistic prospect of more — a
  plain constructor call is simpler and clearer.
- In Python specifically, if the "factory" logic is just "pick a class
  based on a string/enum", a dictionary lookup is usually more readable
  than a class hierarchy.

## Real-world use cases

- GUI toolkits that need to create the right kind of button/scrollbar for
  the current operating system's look and feel.
- ORMs that create the right `Connection`/`Cursor` subclass depending on
  the configured database backend.
- Parsers that create different `Document` subclasses (`PDFDocument`,
  `HTMLDocument`, ...) based on file type, while calling code just works
  with `Document`.
- Python's own `json.loads`/`json.dumps` accept an `object_hook`/`default`
  that acts like a pluggable factory for custom object creation.

## Related patterns

- **Abstract Factory** is often implemented using a set of Factory
  Methods.
- **Template Method** frequently calls a Factory Method internally to
  obtain the object it needs for one of its steps.
- **Prototype** is an alternative to Factory Method when creating an
  object by copying is cheaper/easier than building it from scratch.
