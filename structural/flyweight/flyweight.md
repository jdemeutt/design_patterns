# Flyweight

**Category:** Structural

## Intent

Use sharing to support large numbers of fine-grained objects efficiently,
by splitting an object's state into **intrinsic** (shared, immutable)
state and **extrinsic** (context-specific, supplied by the client) state.

## Motivation

Imagine rendering a text document as thousands of individual character
objects, or a forest simulation with a million trees. If every character
or tree is a fully independent object carrying *all* its data (font,
color, glyph bitmap for characters; mesh, texture, species data for
trees), memory usage explodes even though most of that data is identical
across many instances (all "A" characters in the same font/size/color
share the same glyph; all "Oak" trees share the same mesh/texture).

Flyweight splits object state into two parts:

- **Intrinsic state** — data that's shared and doesn't depend on context
  (the glyph bitmap for "A" in Times New Roman 12pt; the mesh/texture for
  an Oak tree). This is stored once in a shared **Flyweight** object.
- **Extrinsic state** — data that's unique per usage and depends on
  context (the position on the page; the tree's (x, y) location in the
  world). This is *not* stored in the flyweight — it's passed in by the
  client each time an operation is invoked.

A **Flyweight Factory** ensures flyweights are shared: it returns an
existing flyweight for a given intrinsic state if one already exists,
instead of creating a new one.

## Structure

```
Client                    FlyweightFactory              Flyweight
+---------------+         +--------------------+        +-------------------+
| extrinsic state|        | -pool: {key: FW}    |        | +operation(extrinsic)|
| holds ref to FW |------>| +get_flyweight(key) |------->|                     |
+---------------+         +--------------------+        +-------------------+
                                                                  ^ (shared instance,
                                                                     many clients point
                                                                     to the same object)
```

## Pros

- Dramatically reduces memory usage when an application needs huge numbers
  of similar objects, by sharing the parts that are identical across
  instances.
- Centralizes state that would otherwise be duplicated in many places,
  which can also simplify updates to shared data.
- Works well alongside object pools/caches for other kinds of expensive
  shared resources.

## Cons

- Adds real complexity: you must carefully separate intrinsic from
  extrinsic state, and client code now has to manage and pass extrinsic
  state explicitly on every call — the flyweight can no longer hold it.
- Trades memory for a bit of CPU/complexity (extra lookups in the
  flyweight factory, extra parameters threaded through calls).
- Only worthwhile once object counts are large enough that the memory
  savings actually matter — for a handful of objects it's needless
  ceremony.
- Shared (intrinsic) state must be treated as immutable/read-only, since
  mutating it affects every client using that flyweight — this constraint
  has to be enforced by convention/discipline in Python.

## When to use it

- An application needs to create a very large number of similar objects
  that would otherwise consume excessive memory.
- Most of an object's state can be made extrinsic (moved out and supplied
  by context) without much friction.
- Object identity doesn't matter for these instances — group of objects
  can be replaced by shared instances without any observable behavior
  change from the client's perspective.

## When *not* to use it

- The number of objects is small enough that memory isn't actually a
  concern — the added complexity isn't worth it.
- Most of the object's state is genuinely unique per instance (little to
  share) — there's not much "intrinsic" state to factor out.

## Real-world use cases

- Text editors/renderers sharing glyph objects across all occurrences of
  the same character/font/size.
- Game engines sharing mesh/texture/material data across thousands of
  identical-looking entities (trees, bullets, particles), storing only
  position/rotation/health per instance.
- String interning: Python itself interns small integers and some string
  literals so identical values share the same object in memory
  (`sys.intern`, and CPython's automatic interning of short identifier-like
  strings) — a built-in example of this exact pattern.
- Icon/image caching in UI toolkits: the same icon bitmap reused across
  many list items instead of one copy per row.

## Related patterns

- Flyweight is frequently combined with **Factory Method** (a factory
  that returns shared instances) and behaves like a specialized
  object pool.
- **Composite** trees of many small objects are a common place Flyweight
  gets applied, to keep the tree's leaf nodes cheap.
- Differs from **Singleton** in that Flyweight manages *many* shared
  instances (keyed by intrinsic state), while Singleton manages exactly
  *one*.
