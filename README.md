# Design Patterns — Overview

Design patterns are reusable, proven solutions to recurring problems in
object-oriented software design. They are not finished code you copy and
paste; they are *templates* for how to structure the relationship between
classes and objects to solve a problem in a flexible, maintainable way.

The catalog in this repository follows the classic taxonomy introduced by
the "Gang of Four" (Erich Gamma, Richard Helm, Ralph Johnson, John
Vlissides) in *Design Patterns: Elements of Reusable Object-Oriented
Software* (1994) — 23 patterns split into three categories.

## Why use design patterns at all?

- **Shared vocabulary.** Saying "let's use a Strategy here" communicates an
  entire structural idea in one sentence, instead of a paragraph.
- **Proven solutions.** Each pattern encodes design experience that has
  been tested across many real systems, so you avoid reinventing (and
  potentially breaking) something that already has a well-understood
  solution.
- **Flexibility and maintainability.** Most patterns exist specifically to
  isolate the parts of a system that change from the parts that don't,
  which makes future changes cheaper.

## Why patterns can also hurt you

- **Over-engineering.** Applying a pattern where a plain function or a
  simple `if/else` would do adds indirection, extra files, and cognitive
  load for no real benefit. Patterns solve problems — if you don't have
  the problem yet, you probably don't need the pattern yet.
- **Wrong pattern, wrong problem.** Patterns are shaped by the language
  they were codified in (C++/Smalltalk-era OOP). In Python, some GoF
  patterns are unnecessary or look different because the language already
  gives you first-class functions, duck typing, modules-as-singletons,
  and multiple inheritance.
- **Pattern fever.** Junior (and not-so-junior) developers sometimes
  reach for a named pattern to feel like they're doing "real" software
  architecture. Use a pattern because it solves a concrete problem you can
  point to, not because it has a name.

## The three categories

### 1. Creational patterns — *how objects are created*

These patterns abstract away the instantiation process, so a system is
independent of how its objects are created, composed, and represented.

| Pattern | One-line intent |
|---|---|
| [Singleton](creational/singleton/singleton.md) | Ensure a class has only one instance, with a global access point. |
| [Factory Method](creational/factory_method/factory_method.md) | Let subclasses decide which concrete class to instantiate. |
| [Abstract Factory](creational/abstract_factory/abstract_factory.md) | Produce families of related objects without specifying concrete classes. |
| [Builder](creational/builder/builder.md) | Separate the construction of a complex object from its representation. |
| [Prototype](creational/prototype/prototype.md) | Create new objects by copying an existing instance (a "prototype"). |

### 2. Structural patterns — *how objects are composed*

These patterns deal with the composition of classes or objects to form
larger structures, keeping those structures flexible and efficient.

| Pattern | One-line intent |
|---|---|
| [Adapter](structural/adapter/adapter.md) | Convert the interface of a class into another interface clients expect. |
| [Bridge](structural/bridge/bridge.md) | Decouple an abstraction from its implementation so both can vary independently. |
| [Composite](structural/composite/composite.md) | Compose objects into tree structures and treat individual objects and compositions uniformly. |
| [Decorator](structural/decorator/decorator.md) | Attach additional responsibilities to an object dynamically. |
| [Facade](structural/facade/facade.md) | Provide a unified, simplified interface to a set of subsystems. |
| [Flyweight](structural/flyweight/flyweight.md) | Share fine-grained objects efficiently to support large numbers of them. |
| [Proxy](structural/proxy/proxy.md) | Provide a surrogate/placeholder for another object to control access to it. |

### 3. Behavioral patterns — *how objects communicate and share responsibility*

These patterns are concerned with algorithms and the assignment of
responsibilities between objects.

| Pattern | One-line intent |
|---|---|
| [Chain of Responsibility](behavioral/chain_of_responsibility/chain_of_responsibility.md) | Pass a request along a chain of handlers until one handles it. |
| [Command](behavioral/command/command.md) | Encapsulate a request as an object, enabling queuing, logging, and undo. |
| [Interpreter](behavioral/interpreter/interpreter.md) | Define a grammar and an interpreter for a language. |
| [Iterator](behavioral/iterator/iterator.md) | Provide a way to access elements of a collection sequentially without exposing its representation. |
| [Mediator](behavioral/mediator/mediator.md) | Define an object that encapsulates how a set of objects interact. |
| [Memento](behavioral/memento/memento.md) | Capture and externalize an object's internal state so it can be restored later. |
| [Observer](behavioral/observer/observer.md) | Define a one-to-many dependency so dependents are notified of state changes. |
| [State](behavioral/state/state.md) | Allow an object to alter its behavior when its internal state changes. |
| [Strategy](behavioral/strategy/strategy.md) | Define a family of interchangeable algorithms. |
| [Template Method](behavioral/template_method/template_method.md) | Define the skeleton of an algorithm, letting subclasses override specific steps. |
| [Visitor](behavioral/visitor/visitor.md) | Separate an algorithm from the object structure it operates on. |

## How to read this repository

Every pattern directory contains:

- `<pattern_name>.md` — intent, motivation, structure, pros/cons, real-world
  use cases, related patterns, and Python-specific notes.
- One or more standalone `.py` files — a runnable, self-contained example
  you can execute directly with `python3 <file>.py` to see the pattern in
  action (no external dependencies required).

## General guidance for choosing a pattern

1. **Start with the problem, not the pattern.** Ask "what varies?" — the
   part of your system that changes independently of everything else is
   usually the hint for which pattern applies.
2. **Creation is getting complicated** → look at Creational patterns.
3. **Two class hierarchies need to be glued together, or you want to add
   behavior without subclassing** → look at Structural patterns.
4. **Objects need to communicate, or an algorithm needs to vary at
   runtime** → look at Behavioral patterns.
5. **When in doubt, don't.** A pattern applied prematurely is technical
   debt with a nicer name.

## Further reading

- Gamma, Helm, Johnson, Vlissides — *Design Patterns: Elements of Reusable
  Object-Oriented Software* (1994), the original "Gang of Four" book.
- Freeman & Robson — *Head First Design Patterns* (a friendlier, more
  visual introduction).
- [refactoring.guru/design-patterns](https://refactoring.guru/design-patterns) —
  a free, well-illustrated online reference.
