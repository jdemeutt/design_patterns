# Prototype

**Category:** Creational

## Intent

Specify the kinds of objects to create using a prototypical instance, and
create new objects by **copying** this prototype, rather than building
each one from scratch.

## Motivation

Some objects are expensive or awkward to construct from scratch: maybe
they load data from a database or file, run an expensive computation, or
have a deeply nested structure that's tedious to reconstruct field by
field. If you already have an object in exactly (or almost exactly) the
state you want, it's often far cheaper to **clone** it and tweak the copy
than to build a brand-new one.

Prototype also helps when the exact class of an object shouldn't matter to
the code that's duplicating it — as long as it implements a `clone()`
method, calling code can copy *any* object without knowing its concrete
class or how to construct it.

## Structure

```
Prototype (interface)          ConcretePrototypeA        ConcretePrototypeB
+----------------+             +------------------+      +------------------+
| +clone()        |<------------|                  |      |                  |
+----------------+             +------------------+      +------------------+

Client
+----------------+
| p2 = p1.clone() |
+----------------+
```

Client code holds a reference to some `Prototype` and calls `clone()`
without needing to know (or import!) the concrete class behind it.

## Shallow vs. deep copy

This is the central implementation concern for Prototype in Python:

- **Shallow copy** (`copy.copy`) duplicates the top-level object, but
  nested mutable objects (lists, dicts, other objects) are still *shared*
  between the original and the copy — mutating a nested list in the clone
  also mutates it in the original.
- **Deep copy** (`copy.deepcopy`) recursively duplicates every nested
  object too, so the clone is completely independent.

Getting this distinction wrong is the most common Prototype bug: code
looks correct until someone mutates a nested collection in the "copy" and
is baffled that the original changed too.

## Pros

- Lets you produce new objects without coupling to their concrete classes
  (you don't need to know/import `SpecificClass`, only call
  `existing_object.clone()`).
- Avoids repeating expensive initialization logic (parsing, computation,
  I/O) when a suitable pre-built object already exists.
- Lets you add/remove prototypes (pre-configured objects) at runtime,
  effectively giving you a dynamic, extensible set of "classes" without
  touching class definitions.
- Simplifies producing complex objects that have many possible
  pre-configured states ("presets").

## Cons

- Cloning objects with circular references, or objects wrapping external
  resources (open file handles, network sockets, database connections),
  is tricky or outright wrong — those references can't simply be
  duplicated.
- Choosing between shallow and deep copy correctly for every field
  requires care and can be a source of subtle bugs.
- Classes need a `clone()` method (or Python's `copy`/`__copy__`/
  `__deepcopy__` hooks implemented correctly), which is extra code to
  maintain.

## When to use it

- Creating a new object is more expensive (in time or code) than copying
  an existing, similar one.
- You want to avoid a proliferation of Factory subclasses just to produce
  slightly different "flavors" of the same object — instead, keep a
  registry of pre-configured prototype instances and clone the one you
  need.
- The classes to instantiate are only known/decided at runtime, and are
  handed to you as already-constructed instances to copy.

## When *not* to use it

- Objects are cheap and simple to construct from scratch — cloning adds
  no benefit and the shallow/deep copy nuance adds risk for nothing.
- The object wraps unclonable external resources (sockets, file handles,
  locks) — those need a fresh acquire, not a copy.

## Real-world use cases

- Game development: cloning a "prototype" enemy/item template to spawn
  many instances instead of re-running expensive setup for each one.
- GUI editors: "duplicate" functionality for shapes/objects on a canvas.
- Configuration objects: keep a base config prototype and clone +
  override a couple of fields per environment (dev/staging/prod).
- Python's own `copy.copy`/`copy.deepcopy` are direct, general-purpose
  implementations of this pattern, usable on almost any object.

## Related patterns

- Prototype is often used **instead of** Factory Method/Abstract Factory
  when the "recipe" for an object is easier expressed as an example
  instance than as construction code.
- A registry of named prototypes is frequently paired with a **Singleton**
  (one shared prototype registry) or exposed through a small factory
  wrapper.
