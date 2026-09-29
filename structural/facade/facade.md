# Facade

**Category:** Structural

## Intent

Provide a unified, higher-level interface to a set of interfaces in a
subsystem. Facade defines a simpler entry point that makes the subsystem
easier to use, without hiding it entirely.

## Motivation

A "subsystem" (a video conversion library, a home theater with an
amplifier/projector/streaming device/lights, an ORM's many internal
classes) often exposes a large number of classes and methods that must be
called in a specific sequence with specific coordination to accomplish
one common task. Most client code doesn't need — and shouldn't need — to
understand all of that internal complexity.

Facade introduces one class that knows how to drive the subsystem
correctly for the common cases, exposing a small, task-oriented API
("`watch_movie()`", "`convert_to_mp4(path)`") while the full subsystem
remains available underneath for callers who need finer control.

## Structure

```
Client
  |
  v
Facade
+------------------+
| +simple_operation()|---coordinates--->  SubsystemClassA
+------------------+                     SubsystemClassB
                                          SubsystemClassC
```

The Facade doesn't add new functionality — it *coordinates* existing
subsystem functionality behind a simpler API. The subsystem classes remain
directly accessible for clients that need them.

## Pros

- Shields client code from subsystem complexity, reducing the number of
  objects clients have to deal with and simplifying typical use cases
  dramatically.
- Promotes **loose coupling** between client code and the subsystem: the
  subsystem can be refactored internally as long as the facade's interface
  stays stable.
- Doesn't prevent power users from bypassing the facade and using the
  subsystem's full API directly when they need to.
- A great tool for gradually **layering** a legacy or overly-complex
  system: wrap it with a facade before refactoring the internals.

## Cons

- Can become a **god object** coupled to every class in the subsystem if
  it keeps growing to cover more and more use cases.
- Adds one more layer client code must be aware exists, even though it's
  meant to reduce complexity — if the facade leaks abstractions
  (subsystem exceptions/types bubbling through), it doesn't fully deliver
  its promise.
- Doesn't prevent misuse of the subsystem directly by other code that
  bypasses the facade entirely, unless access to the subsystem classes is
  also restricted.

## When to use it

- You want to provide a simple, easy-to-use interface to a complex
  subsystem, for the common cases most clients actually need.
- You want to decouple client code from a subsystem's internals so that
  the subsystem can evolve independently (as long as the facade's
  interface remains stable).
- You're introducing a new abstraction layer between application code and
  several tightly-coupled classes, to reduce dependencies.

## When *not* to use it

- The subsystem is already simple and has few classes/methods — a facade
  would add indirection without simplifying anything.
- Different callers need fundamentally different, fine-grained control
  over the subsystem such that a single "simplified" interface can't
  serve them all without becoming a leaky abstraction.

## Real-world use cases

- An `email.send(to, subject, body)` convenience function that
  coordinates SMTP connection setup, MIME message construction, TLS
  negotiation, authentication, and sending, hiding all of that from
  typical callers.
- ORM "session"/"engine" objects (e.g., SQLAlchemy's `Session`) act as a
  facade over connection pooling, transaction management, and SQL
  generation.
- Application startup/bootstrap code that wraps configuration loading,
  logging setup, dependency wiring, and service registration behind one
  `bootstrap_app()` call.
- Cloud SDK "client" objects (e.g., a `StorageClient`) that hide
  authentication, retries, and low-level HTTP calls behind simple methods
  like `.upload_file(...)`.

## Related patterns

- **Abstract Factory** can be used alongside Facade to hide which
  concrete subsystem classes are created.
- Unlike **Adapter**, which makes an *existing* interface match a
  *different expected* one, Facade defines a *brand-new, simpler*
  interface to an existing subsystem — no impedance mismatch is being
  solved, just complexity.
- A Facade is often implemented as (or paired with) a **Singleton**, since
  usually only one facade instance is needed to coordinate a subsystem.
