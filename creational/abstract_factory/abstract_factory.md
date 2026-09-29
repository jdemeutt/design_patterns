# Abstract Factory

**Category:** Creational

## Intent

Provide an interface for creating **families of related or dependent
objects** without specifying their concrete classes.

## Motivation

Suppose a UI toolkit must support multiple visual themes — say, a "Light"
theme and a "Dark" theme — and each theme needs its own matching `Button`,
`Checkbox`, and `Scrollbar`. Mixing a Light button with a Dark checkbox
would look broken. Abstract Factory guarantees that once you pick a
factory (`LightThemeFactory` or `DarkThemeFactory`), every widget it
produces belongs to the same consistent family.

This differs from Factory Method: Factory Method produces **one** product
via inheritance/overriding a single method; Abstract Factory produces an
entire **family of related products** via a single object that groups
several factory methods together (often implemented *using* Factory
Methods internally).

## Structure

```
AbstractFactory                    AbstractProductA      AbstractProductB
+-------------------+              +---------------+      +---------------+
| +create_product_a()|              |               |      |               |
| +create_product_b()|              +---------------+      +---------------+
+---------+----------+                     ^                       ^
          |                    +-----------+----------+  +---------+---------+
  +-------+--------+           |                       |  |                   |
LightFactory   DarkFactory  LightProductA  DarkProductA   LightProductB  DarkProductB
```

- Client code depends only on `AbstractFactory` and the abstract product
  interfaces.
- Swapping the concrete factory swaps the *entire* family of concrete
  products used throughout the client code, in one place.

## Pros

- **Guarantees consistency** among products from the same family — you
  cannot accidentally mix a `LightButton` with a `DarkCheckbox`.
- Isolates concrete classes from client code — client code only ever
  references interfaces.
- Makes exchanging an entire product family easy: swap the factory
  instance once (e.g., at application startup) and the whole family
  changes everywhere it's used.
- Supports the Open/Closed Principle: introducing a brand-new family
  (e.g., a "HighContrast" theme) doesn't require touching existing client
  code — only a new concrete factory + concrete products.

## Cons

- Adding a **new kind of product** to the family (e.g., every theme now
  also needs a `Slider`) requires modifying the abstract factory interface
  *and every single concrete factory* — this cuts against the Open/Closed
  Principle in that one dimension.
- More moving parts (more interfaces and classes) than just instantiating
  objects directly, which can be overkill if you only ever have one
  family.
- Can be harder to follow for newcomers to the codebase due to the extra
  layers of indirection.

## When to use it

- Your system needs to work with multiple families of related products,
  and you want to enforce that only matching objects from the same family
  are used together.
- You want to configure a system with one of several families of objects
  at runtime or startup (e.g., choosing a UI theme, a database backend
  family, or a cloud-provider SDK family).
- You're providing a library and want to reveal only interfaces to
  consumers, keeping your concrete implementations private.

## When *not* to use it

- You only have one product, or only one family of products, with no
  realistic need to swap families.
- The relationships between products aren't actually meaningful (i.e.,
  mixing them wouldn't actually break anything) — a simpler Factory Method
  or even direct construction is enough.

## Real-world use cases

- Cross-platform GUI toolkits producing platform-appropriate widgets
  (Windows/macOS/Linux look-and-feel).
- Database-abstraction layers that produce a matching family of
  `Connection`, `Command`, and `DataReader` objects for a specific backend
  (PostgreSQL vs. MySQL vs. SQLite).
- Document-rendering systems that must produce a consistent family of
  renderers for a document type (e.g., all HTML renderers vs. all PDF
  renderers for headings, paragraphs, and images).
- Game engines choosing a family of assets/behaviors depending on the
  selected "world" or "faction".

## Related patterns

- Often implemented using several **Factory Methods**, one per product
  type.
- Concrete factories are frequently themselves **Singletons**, since you
  typically only need one instance of "the current theme factory".
- Can be combined with **Builder** when the products in a family are
  themselves complex to assemble.
