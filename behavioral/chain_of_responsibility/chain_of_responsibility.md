# Chain of Responsibility

**Category:** Behavioral

## Intent

Avoid coupling the sender of a request to its receiver by giving more than
one object a chance to handle the request. Chain the receiving objects and
pass the request along the chain until an object handles it.

## Motivation

Consider a support ticket system: a ticket might be resolvable by a junior
agent, or need escalation to a senior agent, or a manager, or engineering.
Instead of the sender knowing exactly *which* handler is appropriate (a
big `if/elif` chain checking ticket severity), Chain of Responsibility
links a series of handler objects together. Each handler decides either to
handle the request itself, or to pass it along to the next handler in the
chain — the sender only ever talks to the *first* handler and doesn't know
(or care) how many handlers exist or which one eventually processes it.

## Structure

```
Client --> Handler1 --> Handler2 --> Handler3 --> ... --> None
           (checks:    (checks:     (checks:
            can I       can I        can I
            handle?     handle?      handle?
            if not,     if not,      if not,
            forward)    forward)     forward)
```

Each handler implements a common interface with a `handle(request)` method
and holds a reference to the "next" handler. If it can't process the
request, it forwards to `next.handle(request)`; if there is no next
handler, the chain ends (request goes unhandled, or a default behavior
triggers).

## Pros

- Decouples the sender from the specific receiver — the sender just kicks
  off the chain and doesn't know who (if anyone) will actually handle it.
- **Single Responsibility Principle**: each handler focuses on one
  condition/responsibility.
- **Open/Closed Principle**: you can add, remove, or reorder handlers in
  the chain without touching sender code or other handlers.
- Gives you runtime control over the order and composition of processing
  steps (build different chains for different situations).

## Cons

- No guarantee a request will actually be handled — it can fall off the
  end of the chain silently unless you add an explicit fallback/default
  handler.
- Can make it harder to trace exactly which handler processed a request,
  especially in long chains — debugging requires stepping through the
  whole chain.
- Misconfiguring the chain's order can produce different results than
  intended, since handlers are typically checked in sequence.

## When to use it

- More than one object may handle a request, and the handler shouldn't be
  hard-coded — it should be determined at runtime based on the chain's
  configuration.
- You want to issue a request without specifying the receiver explicitly,
  and let several candidate objects decide amongst themselves (in order)
  who handles it.
- The set of objects that can handle a request should be specifiable
  dynamically (add/remove/reorder handlers at runtime).

## When *not* to use it

- There's exactly one, well-known handler for every request — an explicit
  call is simpler and easier to trace than an implicit chain.
- Requests absolutely must be handled and silent fall-through would be a
  bug risk you can't tolerate without very careful guard-rails.

## Real-world use cases

- Middleware pipelines in web frameworks (Django, Express, ASP.NET Core):
  each middleware either handles/short-circuits the request or passes it
  to the next one in the pipeline.
- Event bubbling in GUI frameworks and the DOM: a click event travels up
  through parent widgets/elements until something handles it (or stops
  propagation).
- Logging frameworks: a log record can pass through a chain of handlers
  (console handler, file handler, alerting handler), each deciding
  whether to process it based on severity level.
- Exception handling itself is conceptually a chain: an exception
  propagates up through nested `try/except` blocks until one catches it.
- Approval workflows: an expense report escalates from manager to
  director to VP based on the amount, each link deciding "can I approve
  this, or does it need to go higher?"

## Related patterns

- Often built using a **Command** object to represent the request being
  passed along the chain.
- Similar to **Decorator** in its linked/nested structure, but intent
  differs: Decorator always calls the next link in the chain (auto-runs
  every wrapper), while Chain of Responsibility handlers may choose to
  stop propagation and not call the next handler.
- Can be combined with **Composite**: a request handled by a composite
  node may be passed down to its children as a chain.
