# State

**Category:** Behavioral

## Intent

Allow an object to alter its behavior when its internal state changes.
The object will appear to change its class.

## Motivation

Objects that go through distinct states with different valid operations
in each — a document (`Draft` -> `Moderation` -> `Published`), a vending
machine, a TCP connection, an order in an e-commerce system — are often
implemented as one class with a `status` field and behavior methods full
of `if status == X: ... elif status == Y: ...` branches. As the number of
states and transitions grows, these conditional blocks get long, are
duplicated across every method that behaves differently per state, and are
easy to get wrong (a status check missed in one method but not another).

State solves this by giving **each state its own class**, implementing the
same interface, with its own version of each state-dependent behavior.
The main object (the **Context**) holds a reference to its *current state
object* and delegates behavior calls to it. Transitioning to a new state
is just swapping which state object the context points to — after that,
subsequent calls automatically behave differently, because they're now
being handled by a different (state) object.

## Structure

```
Context                          State (interface)
+------------------+             +------------------+
| -state: State      |------------> +handle()          |
| +request()         |             +------------------+
+------------------+                      ^
                              +-----------+-----------+
                              |                       |
                        ConcreteStateA          ConcreteStateB
                        (may transition          (may transition
                         context to StateB)        context to StateA)
```

`Context.request()` simply delegates to `self._state.handle(self)`. Each
`ConcreteState.handle()` implements the behavior appropriate for that
state, and may call `context.transition_to(new_state)` to change the
context's current state.

## Pros

- Eliminates large conditional blocks (`if/elif` on a status field)
  scattered across multiple methods — each state's behavior lives in one
  cohesive class.
- **Single Responsibility Principle**: state-specific behavior and
  transition logic are organized by state, not interleaved across
  unrelated methods.
- **Open/Closed Principle**: adding a new state is adding a new class,
  without modifying the context or other existing state classes (as long
  as transitions into/out of the new state are wired up).
- Makes state transitions explicit and easy to locate (they're the
  `context.transition_to(...)` calls inside state classes).

## Cons

- Introduces a class for every state, which can be overkill for objects
  with only two or three simple states and little state-specific
  behavior — a simple flag/enum with a couple of `if` statements may be
  clearer.
- Distributing behavior across many small state classes can make it
  harder to see, at a glance, the *entire* set of valid transitions —
  that picture has to be assembled by reading every state class.
- State objects need a way to trigger transitions on the context, which
  creates some coupling between state classes and the context (or an
  explicit state-transition table).

## When to use it

- An object's behavior depends heavily on its current state, and that
  behavior must change at runtime as its state changes.
- Methods contain large, multi-branch conditionals whose branches depend
  on the object's current state, and these same conditions recur across
  many methods.
- You want to model an explicit, well-defined state machine (order
  processing, connection lifecycle, game character states, workflow
  approval stages).

## When *not* to use it

- There are only one or two states with trivial differences in behavior —
  a boolean flag or small `if` statement is simpler and more readable.
- State transitions are rare or the "state" doesn't actually affect
  behavior meaningfully (it's just informational/display data).

## Real-world use cases

- Order-processing systems (`Pending` -> `Paid` -> `Shipped` ->
  `Delivered`/`Cancelled`), where each state allows/forbids different
  actions.
- TCP connection state machines (`Closed`, `Listen`, `SynSent`,
  `Established`, ...), a classic real-world State example.
- Media player controls: `Playing`, `Paused`, `Stopped` states each
  interpret "press play/pause/stop" differently.
- Game character/AI states (`Idle`, `Patrolling`, `Chasing`, `Attacking`),
  where the same "update" call produces very different behavior depending
  on the current state.
- Parsers/lexers implemented as explicit state machines transitioning
  between recognition states as input is consumed.

## Related patterns

- Structurally very similar to **Strategy** — both delegate behavior to a
  composed object — but the *intent* differs: Strategy lets a *client*
  choose an interchangeable algorithm explicitly; State lets state
  objects transition *themselves* (and the context) automatically based
  on internal logic, usually without the client choosing directly.
- **Singleton** is sometimes applied to stateless state objects (a state
  with no per-context data can be shared as one instance across many
  contexts, since it holds no context-specific data itself).
- Can be combined with a **Factory Method** to construct the right initial
  state object for a context.
