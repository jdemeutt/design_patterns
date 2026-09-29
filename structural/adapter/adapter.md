# Adapter

**Category:** Structural

## Intent

Convert the interface of a class into another interface clients expect.
Adapter lets classes work together that couldn't otherwise because of
incompatible interfaces.

## Motivation

You're integrating a third-party library (or legacy code you can't modify)
whose API doesn't match the interface your application expects. Rewriting
the third-party code is not an option (you don't own it, or it's used
elsewhere unchanged). Adapter wraps the incompatible object in a thin
translation layer that exposes the interface your code already expects,
delegating the actual work to the wrapped object.

A classic real analogy: a physical power-plug adapter doesn't change what
electricity is — it just changes the *shape of the interface* so a plug
from one country fits a socket from another.

## Structure

Two common variants:

**Object Adapter (composition — preferred in Python):**
```
Client -----> Target (interface)      Adaptee (existing, incompatible)
                    ^                  +------------------+
                    |                  | +specific_request()|
              +-----+------+           +------------------+
              |   Adapter   |------has-a-------^
              +------------+
              | +request() |  -- internally calls adaptee.specific_request()
              +------------+
```

**Class Adapter (inheritance — needs multiple inheritance, less common in
Python because it's more rigid and requires inheriting from the adaptee):**
the Adapter subclasses both the Target interface and the Adaptee.

Python favors the **object adapter** (composition) because it works even
when the adaptee's class is final/unmodifiable, and it doesn't require
multiple inheritance gymnastics.

## Pros

- Lets incompatible interfaces work together without changing either
  side's existing code.
- **Single Responsibility Principle**: interface-translation logic is
  isolated in the adapter, not smeared into business logic.
- **Open/Closed Principle**: you can introduce new adapters for new
  incompatible classes without touching existing client code.
- Especially valuable for wrapping third-party/legacy code you cannot or
  should not modify.

## Cons

- Adds a layer of indirection — occasionally a chain of adapters
  (adapter wrapping an adapter) becomes confusing to trace.
- Sometimes simply changing the incompatible class directly (if you *can*
  safely change it) is less code overall than writing and maintaining an
  adapter.
- Doesn't fix underlying design mismatches, semantic (not just syntactic)
  differences between what the two interfaces actually *mean* can still
  cause subtle bugs even after the shapes match.

## When to use it

- You want to use an existing class, but its interface doesn't match what
  the rest of your code expects, and you can't or shouldn't modify the
  existing class.
- You're integrating with a third-party library, legacy system, or
  external API and want to isolate your codebase from its specific
  interface (so if you swap the library later, only the adapter changes).
- You want several existing subclasses that lack some common
  functionality to be usable via one interface.

## When *not* to use it

- You own and can freely modify the class in question — just changing its
  interface directly is usually simpler.
- The interfaces already match closely enough that translation would add
  no value.

## Real-world use cases

- Wrapping a third-party payment gateway SDK behind your own
  `PaymentProcessor` interface so the rest of the app doesn't depend on
  that SDK's specific method names.
- Adapting different data-format parsers (XML, JSON, CSV) to a common
  `DataSource.read()` interface.
- Python's `io` module: file-like wrappers (e.g., adapting a socket to
  behave like a file object) are effectively Adapters.
- Adapting an old synchronous API to be usable in an async codebase (an
  "async adapter") or vice versa.

## Related patterns

- **Bridge** is designed up front to let two hierarchies vary
  independently; **Adapter** is typically applied *after the fact* to make
  already-existing, incompatible interfaces work together.
- **Facade** defines a *new, simplified* interface to a subsystem; Adapter
  makes an *existing* interface match one that's already expected
  elsewhere.
- **Decorator** enhances an object while keeping the same interface;
  Adapter changes the interface itself.
