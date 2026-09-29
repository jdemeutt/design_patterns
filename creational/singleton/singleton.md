# Singleton

**Category:** Creational

## Intent

Ensure a class has only **one instance**, and provide a single, well-known,
global point of access to it.

## Motivation

Some things in a system genuinely only make sense once: a single connection
pool, a single configuration object loaded from disk, a single logging
facility, a single hardware device driver. If several parts of the code
each created their own instance of such a class, you could get
inconsistent state, wasted resources, or race conditions.

Singleton solves this by making the class itself responsible for tracking
its one instance and handing that same instance back to every caller.

## Structure

```
+------------------+
|    Singleton     |
+------------------+
| -instance: Self   |
+------------------+
| +get_instance()  |<-- returns the same object every time
+------------------+
```

The constructor is effectively hidden from normal use; the only supported
way to obtain the object is through a class-level accessor.

## Implementation approaches in Python

Python doesn't have `private` constructors like C++/Java, so Singleton is
usually implemented one of these ways:

1. **Overriding `__new__`** — the most literal translation of the GoF
   pattern (used in the accompanying example).
2. **A metaclass** — intercepts instantiation (`SomeClass()`) at the
   metaclass level; more "correct" for a whole family of singleton
   classes.
3. **A module** — because Python modules are only imported once and
   cached in `sys.modules`, a module *is* a singleton for free. This is
   the idiomatic Python approach for "global" state, and is often
   preferred over a Singleton class entirely.
4. **`functools.lru_cache`/`cache` on a factory function** — memoizes the
   return value so repeated calls return the same object.

## Pros

- Guarantees a single instance, which is essential for globally shared
  resources (logging, configuration, connection pools, caches).
- Global access point, so client code doesn't need to pass the object
  around through every function/constructor.
- Lazy initialization is easy: the instance is only created the first time
  it's actually requested.

## Cons

- **Global mutable state.** Singletons behave like glorified global
  variables, which makes code harder to reason about and to test (tests
  can leak state into each other via the shared instance).
- **Hides dependencies.** A class that calls `Singleton.get_instance()`
  internally has a hidden dependency that isn't visible in its
  constructor signature, making dependency injection and mocking harder.
- **Concurrency concerns.** In multi-threaded code, naive
  lazy-initialization Singletons can create two instances if two threads
  race to create the first one; this needs explicit locking.
- **Violates the Single Responsibility Principle** in the strict sense: the
  class both manages its business logic *and* manages its own lifecycle.
- Many developers now consider Singleton an anti-pattern for exactly these
  reasons, and prefer **dependency injection** of a single shared instance
  that is constructed once at the application's composition root, instead
  of baking "there is only one" into the class itself.

## When to use it

- You need exactly one instance of a class, accessible from many unrelated
  parts of the code, and passing it explicitly everywhere would be overly
  invasive (e.g., a logger).
- You want stricter control over global state than a bare module-level
  variable would give you (e.g., lazy initialization with validation).

## When *not* to use it

- When you could instead pass the shared object explicitly via
  constructor/function parameters (dependency injection) — this keeps
  dependencies visible and testable.
- When a plain module with module-level state would do the job just as
  well (very common in Python).
- When you might need more than one instance in the future (e.g., multiple
  database connections to different databases) — Singleton actively fights
  against that.

## Real-world use cases

- Logging frameworks (`logging.getLogger()` effectively returns cached
  logger instances keyed by name).
- Configuration managers that parse a config file once and serve it
  everywhere.
- Connection pools / thread pools, where creating more than one would
  waste resources or violate a hardware/software licensing constraint.
- GUI frameworks (only one application-wide event loop / window manager).

## Related patterns

- **Abstract Factory**, **Builder**, and **Prototype** can all be
  implemented using Singletons (e.g., a single factory instance).
- **Facade** objects are frequently implemented as Singletons, since only
  one facade is usually needed.
- A Singleton is essentially a special case of a **Registry** pattern with
  exactly one entry.
