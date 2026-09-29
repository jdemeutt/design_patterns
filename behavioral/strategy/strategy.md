# Strategy

**Category:** Behavioral

## Intent

Define a family of algorithms, encapsulate each one, and make them
interchangeable. Strategy lets the algorithm vary independently from the
clients that use it.

## Motivation

Suppose a navigation app needs to compute a route, and the routing
algorithm depends on the user's chosen mode: driving, walking, cycling, or
public transit. Hard-coding all four algorithms into one big `if/elif`
inside `calculate_route()` makes that method grow every time a new mode is
added, and makes each algorithm hard to test or reuse in isolation.

Strategy extracts each algorithm into its own class implementing a common
interface (e.g., `RouteStrategy.build_route(a, b)`), and the context
object (`Navigator`) holds a reference to whichever strategy is currently
selected, delegating to it. Swapping the algorithm at runtime is just
swapping which strategy object the context holds — no conditional logic,
no subclassing the context itself.

## Structure

```
Context                         Strategy (interface)
+------------------+             +------------------+
| -strategy          |------------> +execute()          |
| +set_strategy()     |             +------------------+
| +do_something()     |                      ^
+------------------+                +----------+----------+
                                    |                       |
                             ConcreteStrategyA       ConcreteStrategyB
```

`Context.do_something()` calls `self._strategy.execute(...)`. The context
never implements the algorithm itself — it only knows the `Strategy`
interface.

## Pros

- Lets you swap algorithms at runtime, cleanly, without touching the
  context's code.
- Isolates the implementation details of an algorithm from the code that
  uses it — each strategy can be developed, tested, and reasoned about
  independently.
- Replaces large conditional blocks (choosing behavior based on a flag/
  type) with polymorphism.
- **Open/Closed Principle**: new strategies can be added without modifying
  the context or existing strategies.
- In Python, strategies are very often just **plain functions** passed
  around, rather than full classes — the language's first-class functions
  make this pattern especially lightweight.

## Cons

- Introduces at least one extra object (and often an extra interface) for
  what might otherwise be a simple parameter or function argument — for a
  small, fixed number of simple variants this can be more structure than
  needed.
- Clients must be aware of the different strategies to choose between
  them, which slightly increases the number of things a caller needs to
  understand versus a single fixed algorithm.
- If most strategies only differ in one tiny detail, having full separate
  classes can duplicate a lot of shared boilerplate (Template Method may
  be a better fit for that case).

## When to use it

- You have several related classes/algorithms that differ only in their
  behavior for one operation, and want to select between them at runtime.
- You need different variants of an algorithm and want to switch between
  them cleanly, without a maze of conditionals.
- An algorithm uses data that callers shouldn't know about — Strategy lets
  you hide those implementation details behind a clean interface.
- You want to unit-test each algorithm variant independently.

## When *not* to use it

- There's really only one algorithm, or the variants are unlikely to grow
  — a single method or a simple `if/else` is simpler.
- The "strategies" barely differ — consider parameterizing one function
  instead of creating a whole family of classes.

## Real-world use cases

- Sorting: Python's `sorted(items, key=...)` accepts a "strategy" function
  determining sort order, without `sorted` needing to know anything about
  what that key function does.
- Payment processing: a `PaymentStrategy` interface with
  `CreditCardStrategy`, `PayPalStrategy`, `CryptoStrategy` implementations,
  chosen at checkout time.
- Compression/serialization libraries that let you plug in different
  algorithms (gzip vs. bzip2 vs. lz4) behind one `compress()` interface.
- Validation frameworks that let you swap in different validation
  strategies per field or per form.
- Route planning / pathfinding: different algorithms (Dijkstra, A*, BFS)
  behind a common `find_path()` interface.

## Related patterns

- Structurally similar to **State**, but different intent: Strategy is
  chosen by, and typically doesn't change without, the client; State
  objects often trigger their own transitions internally as part of the
  domain logic.
- Similar to **Bridge**, but Bridge is designed up front to separate two
  whole class hierarchies, while Strategy is usually applied to swap a
  single algorithm/behavior.
- **Factory Method** or a simple dictionary lookup is frequently used to
  select and construct the right concrete Strategy based on some input
  (e.g., a config value or user choice).
