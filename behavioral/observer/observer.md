# Observer

**Category:** Behavioral

## Intent

Define a one-to-many dependency between objects so that when one object
(the **subject**) changes state, all its dependents (**observers**) are
notified and updated automatically.

## Motivation

Many systems need to keep several objects consistent with the state of one
"source of truth" object, without hard-wiring that object to know
everything that depends on it. For example, a spreadsheet cell's value
change might need to update several charts and summary cells that depend
on it. If the cell directly called methods on every chart and summary
cell it knew about, adding a new dependent view would require modifying
the cell's code — and the cell would be needlessly coupled to UI concerns
it shouldn't know about.

Observer decouples this: the subject maintains a list of observers (just
objects implementing a common `update()` interface) and calls `update()`
on all of them whenever its state changes, without knowing or caring what
each observer actually does with that notification. Observers can be
added or removed dynamically, at runtime, without the subject's code
changing at all.

## Structure

```
Subject                                  Observer (interface)
+-------------------+                    +----------------+
| -observers: [Obs]   |                    | +update(state) |
| +attach(observer)   |                    +----------------+
| +detach(observer)   |                            ^
| +notify()           |----for each observer----->|
+-------------------+     calls observer.update()  |
                                          +---------+---------+
                                          |                   |
                                   ConcreteObserverA    ConcreteObserverB
```

## Pros

- **Loose coupling**: the subject only depends on the abstract `Observer`
  interface, not on concrete observer classes — you can add new kinds of
  observers without touching the subject.
- Supports a dynamic, runtime-configurable number of dependents —
  observers can subscribe/unsubscribe at any time.
- Establishes a clean broadcast/publish-subscribe communication style,
  which fits many real-time and event-driven systems naturally.
- **Open/Closed Principle**: new observer types can be introduced freely.

## Cons

- Notification order between observers is usually unspecified/arbitrary
  unless you design for it explicitly — code that implicitly relies on a
  particular order is fragile.
- Can cause unexpected cascades: an observer's `update()` triggering
  further changes that trigger more notifications can be hard to trace
  and debug ("notification storms").
- Memory leaks are a classic pitfall: if a subject holds strong references
  to observers, forgetting to `detach()` an observer that should have gone
  out of scope keeps it alive indefinitely (this is why some
  implementations use weak references).
- Doesn't guarantee observers handle a notification efficiently or
  correctly — a slow observer can block/delay all other observers if
  notifications are synchronous.

## When to use it

- A change to one object requires changing others, and you don't know (or
  don't want to hard-code) how many, or which, other objects need to
  change.
- An object should be able to notify other objects without making
  assumptions about who those objects are.
- You're implementing event-driven or publish/subscribe style
  communication, especially across loosely related parts of a system
  (e.g., UI updates reacting to backend model changes).

## When *not* to use it

- The dependency between the two objects is simple, fixed, and unlikely to
  change — direct method calls are clearer.
- Notification cascades would be hard to reason about for your use case,
  and a more explicit, traceable communication style (direct calls,
  explicit orchestration) would be safer.

## Real-world use cases

- GUI frameworks: widgets observing a data model and re-rendering when it
  changes (the "Model" in MVC notifies its "Views").
- Event systems / pub-sub message buses (`EventEmitter` in Node.js, Qt's
  signals & slots, Python's own `unittest.mock` call tracking).
- Reactive programming libraries (RxPy, reactive streams) generalize
  Observer into composable event streams.
- Stock ticker / live-dashboard style applications where many independent
  displays need to react to price changes from one central feed.
- Python's `watchdog`/file-system-watcher libraries notify multiple
  handlers when a file changes.

## Related patterns

- **Mediator** and Observer both decouple a set of collaborating objects,
  but Mediator centralizes and encapsulates arbitrary *interaction logic*
  between colleagues, while Observer specifically models "one subject
  notifies many independent observers of state changes" — mediators are
  often implemented using Observer internally.
- **Publish-Subscribe** systems are a distributed, often asynchronous
  generalization of Observer, usually decoupling subject and observers
  through an intermediary broker.
- Observers are sometimes implemented via **Command** objects
  (callbacks) rather than a full interface, especially in a
  duck-typed/functional style.
