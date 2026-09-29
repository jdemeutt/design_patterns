# Decorator

**Category:** Structural

## Intent

Attach additional responsibilities to an object **dynamically**.
Decorators provide a flexible alternative to subclassing for extending
functionality.

## Motivation

Suppose you're modeling coffee orders: a plain `Coffee`, optionally with
`Milk`, `Sugar`, `WhippedCream`, in any combination. Modeling every
combination with subclassing (`CoffeeWithMilkAndSugar`,
`CoffeeWithMilkAndSugarAndCream`, ...) explodes combinatorially, just like
in Bridge — except here the "extra features" are meant to be **stacked at
runtime**, per individual object, not fixed per class.

Decorator solves this by wrapping the original object in one or more
decorator objects, each implementing the *same interface* as the object
they wrap, and each adding its own behavior before/after delegating to the
wrapped object. Because a decorator has the same interface as what it
wraps, decorators can be **stacked** arbitrarily, and client code can't
tell (or care) whether it's holding a plain object or a heavily decorated
one.

## Structure

```
Component (interface)
+----------------+
| +operation()    |
+----------------+
        ^
   +----+---------------------+
   |                          |
ConcreteComponent       Decorator (also a Component)
                        +------------------+
                        | -wrapped: Component|
                        | +operation()      |----calls----> wrapped.operation()
                        +------------------+                 (then adds its own behavior)
                                 ^
                    +------------+------------+
                    |                         |
             ConcreteDecoratorA        ConcreteDecoratorB
```

## Pros

- Adds responsibilities to individual objects at runtime, without
  affecting other instances of the same class.
- Avoids a combinatorial explosion of subclasses for every possible
  combination of features.
- **Single Responsibility Principle**: each decorator handles one added
  concern (logging, caching, compression, formatting...).
- Decorators can be composed/stacked in any order and combination the
  caller chooses.
- Python has first-class syntactic support for a special case of this —
  **function decorators** (`@my_decorator`) — which is one of the most
  commonly used patterns in the entire language.

## Cons

- A stack of many small decorators can be harder to debug — an error
  might occur several layers deep, and stepping through the call stack
  means stepping through every wrapper.
- Decorators must faithfully preserve the wrapped object's interface;
  identity-sensitive code (`isinstance` checks, `is` comparisons on the
  wrapped object) can behave unexpectedly once something is wrapped.
- Order of decoration can matter and isn't always obvious from reading the
  call site (compressing-then-encrypting is different from
  encrypting-then-compressing).

## When to use it

- You want to add responsibilities to individual objects, dynamically and
  transparently, without affecting other objects of the same class.
- Extension via subclassing is impractical (too many independent
  optional features) or impossible (the class is final/sealed).
- You want responsibilities that can be added *and later removed* at
  runtime, since decorators are just objects that can be composed or
  discarded.

## When *not* to use it

- The set of extensions is small and fixed — a couple of subclasses or a
  simple flag/parameter is simpler.
- You need to inspect or depend on the concrete type of the wrapped object
  frequently — heavy wrapping fights against that.

## Real-world use cases

- Python's built-in `@decorator` syntax for functions/methods: `@property`,
  `@staticmethod`, `@functools.lru_cache`, `@app.route(...)` in Flask, are
  all this pattern applied to functions rather than general objects.
- I/O stream wrapping: `io.BufferedReader`, `gzip.GzipFile`, or
  `io.TextIOWrapper` wrapping a raw byte stream, each adding one
  responsibility (buffering, compression, text decoding).
- Web middleware/handler chains (auth, logging, rate-limiting) that wrap
  a request handler, each adding one cross-cutting concern.
- UI toolkits: adding borders, scrollbars, or shadows to a visual
  component by wrapping it.

## Related patterns

- **Adapter** changes an object's *interface*; **Decorator** enhances an
  object's *behavior* while preserving the same interface.
- **Composite** and **Decorator** share a similar recursive/nested
  structure, but Composite represents part-whole hierarchies of many
  objects, while Decorator wraps a single object to add responsibilities.
- **Strategy** changes an object's internal algorithm via composition;
  Decorator wraps the *whole object* from the outside, layering behavior
  around it.
