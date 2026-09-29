# Command

**Category:** Behavioral

## Intent

Encapsulate a request as an object, thereby letting you parameterize
clients with different requests, queue or log requests, and support
undoable operations.

## Motivation

Think of a text editor's toolbar buttons, or a remote control's buttons:
each button needs to trigger some action, but the button widget itself
shouldn't need to know the details of *how* to perform that action (nor
should it be hard-wired to one specific receiver). By wrapping "an action
plus the object it acts on plus the parameters it needs" into a `Command`
object with a uniform `execute()` method, the invoker (the button, a menu
item, a macro recorder) can trigger *any* action without knowing anything
about it.

Because the command is a full object (not just a function call that
happens and is forgotten), it can be stored, queued, logged, sent across a
network, or — critically — paired with an `undo()` method to support undo
stacks.

## Structure

```
Invoker                 Command (interface)        Receiver
+---------------+       +----------------+       +------------------+
| +set_command() |------>| +execute()      |------>| does the actual  |
| +invoke()      |       | +undo()         |       | work             |
+---------------+       +----------------+       +------------------+
                                ^
                    +-----------+-----------+
                    |                       |
             ConcreteCommandA        ConcreteCommandB
             (holds receiver +       (holds receiver +
              needed parameters)      needed parameters)
```

- The `Invoker` only knows about the `Command` interface; it doesn't know
  the `Receiver` or what `execute()` actually does.
- Each `ConcreteCommand` binds together a `Receiver` and the action to
  invoke on it (plus any parameters), so `execute()` needs no arguments.

## Pros

- Decouples the object that invokes an operation from the object that
  knows how to perform it (**Single Responsibility Principle**).
- Commands are first-class objects: they can be stored in lists (undo/redo
  stacks, macro sequences), serialized, queued, scheduled, or logged for
  auditing/replay.
- Makes **undo/redo** straightforward: each command knows how to reverse
  itself, and an undo stack is just a list of executed commands.
- Supports composing simple commands into **macro commands** (a command
  that executes a list of other commands).
- **Open/Closed Principle**: new commands can be introduced without
  changing invoker or receiver code.

## Cons

- Introduces a new class for every distinct action/operation, which adds
  boilerplate for simple cases — in Python, a plain function or `partial`
  can substitute for very simple commands (though without built-in
  undo/queueing support).
- Undo support specifically requires each command to store enough state to
  reverse itself, which can be non-trivial for operations with side
  effects that aren't cleanly invertible.
- Command objects that capture a lot of context/state can end up holding
  more responsibility than they should if not designed carefully.

## When to use it

- You want to parameterize objects (buttons, menu items, schedulers) with
  an action to perform, decided at runtime.
- You need to queue, schedule, log, or send operations across a
  process/network boundary as discrete units.
- You need **undo/redo** functionality.
- You want to assemble complex operations out of simpler ones (macro
  commands / composite commands).

## When *not* to use it

- The action is simple, always the same, and never needs to be queued,
  logged, undone, or parameterized — a direct method call or plain
  function is simpler.
- You don't actually need any of Command's benefits (undo, queuing,
  logging, deferred execution) — the extra class hierarchy is unjustified
  ceremony.

## Real-world use cases

- GUI frameworks: menu items, toolbar buttons, and keyboard shortcuts are
  frequently bound to Command objects rather than hard-coded callbacks.
- Undo/redo stacks in text editors, image editors, and IDEs.
- Task queues / job scheduling systems (Celery tasks, background jobs) —
  a task is essentially a serialized Command sent to a worker.
- Transactional systems that log commands for replay/auditing (event
  sourcing is closely related: a sequence of Command-like events
  reconstructs state).
- `functools.partial` and closures in Python are lightweight, function-
  based cousins of the Command pattern for simple, non-undoable cases.

## Related patterns

- **Memento** is often used alongside Command to capture the state needed
  for a command's `undo()`.
- **Composite** is used to implement macro commands (a command made up of
  a list of other commands).
- **Strategy** and Command look structurally similar (both wrap behavior
  as an object passed around), but Strategy is about choosing *how* to do
  something (an interchangeable algorithm), while Command is about
  encapsulating a specific *request/action* to perform, often including
  history/undo semantics.
