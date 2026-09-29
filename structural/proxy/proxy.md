# Proxy

**Category:** Structural

## Intent

Provide a surrogate or placeholder for another object to **control access**
to it. A proxy implements the same interface as the real object, so it can
be used anywhere the real object would be, while adding behavior around
access to it (lazy loading, access control, caching, logging, remote
communication...).

## Motivation

Sometimes you want to interpose behavior between a client and a "real"
object, without the client knowing or caring:

- The real object is **expensive to create** and you want to defer that
  cost until it's actually needed (*virtual proxy* / lazy loading).
- Access to the real object should be **restricted** based on permissions
  (*protection proxy*).
- The real object **lives on another machine** and calls to it need to be
  marshalled over the network (*remote proxy*).
- You want to **cache** or **log** calls transparently (*caching/logging
  proxy*).

In every case, the Proxy implements the same interface as the real subject,
so it's a drop-in substitute — client code doesn't need an `if using proxy`
branch anywhere.

## Structure

```
Client
  |
  v
Subject (interface)
+----------------+
| +request()      |
+--------+-------+
         ^
    +----+-----------------+
    |                       |
   RealSubject             Proxy
+----------------+     +----------------------+
| +request()      |<----| -real_subject         |
+----------------+     | +request()            |----(controls access, may
                        +----------------------+     lazily create/forward to
                                                      real_subject.request())
```

## Pros

- Controls access to the real object without the real object (or the
  client) needing to know a proxy is involved — fully transparent.
- **Virtual proxy**: defers expensive object creation until it's actually
  needed, improving startup time/memory usage.
- **Protection proxy**: enforces access control/permissions in one place,
  outside the real object's own logic.
- **Remote proxy**: hides the complexity of network communication behind a
  normal-looking local interface.
- **Caching proxy**: can serve repeated requests without hitting the real
  (possibly expensive) subject again.
- Follows the Open/Closed Principle: you can introduce a new proxy without
  changing the real subject or client code.

## Cons

- Adds another layer of indirection, which is unnecessary overhead if none
  of the proxy's benefits (lazy loading, access control, caching, remote
  access) are actually needed.
- Response time can *increase* slightly due to the extra hop through the
  proxy, even for proxies that don't do much extra work.
- Bugs in the proxy (e.g., a caching proxy serving stale data) can be
  subtle since the client believes it's talking to the real subject.

## When to use it

- Object creation is expensive and you want to defer it until first real
  use (virtual proxy / lazy initialization).
- You need to check permissions before allowing an operation to reach the
  real object (protection proxy).
- The real object lives in a different process/machine and you want local
  code to interact with it as if it were local (remote proxy — this is
  effectively what RPC/gRPC-generated client stubs are).
- You want to add caching, logging, reference counting, or other
  cross-cutting behavior transparently in front of an existing interface.

## When *not* to use it

- None of the cross-cutting concerns above are actually needed — a direct
  reference to the real object is simpler and has no extra hop.
- The overhead of an additional indirection layer is not justified by
  actual measured benefit (e.g., caching a cheap, fast operation).

## Real-world use cases

- ORMs: lazy-loaded relationship attributes are classic virtual proxies —
  accessing `user.orders` triggers a database query only the first time
  it's touched.
- `unittest.mock.Mock`/`MagicMock` objects act as proxies (and spies) that
  stand in for real objects in tests.
- RPC/gRPC client stubs are remote proxies: calling a "local" method
  actually serializes arguments and sends them over the network.
- Security/authorization layers that wrap a service so every call is
  checked against the caller's permissions before reaching the real
  service.
- `weakref.proxy` in Python's standard library is a literal, built-in
  Proxy pattern implementation.

## Related patterns

- Structurally almost identical to **Decorator** — both wrap an object
  behind the same interface — but the *intent* differs: Decorator adds
  new responsibilities/behavior; Proxy controls access to (and may defer
  creation of) the object it wraps.
- **Adapter** changes an interface to match what's expected; Proxy keeps
  the exact same interface as the real subject.
- A **Facade** simplifies access to a whole subsystem; a Proxy stands in
  for one specific object.
