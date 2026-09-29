# Template Method

**Category:** Behavioral

## Intent

Define the skeleton of an algorithm in a method, deferring some steps to
subclasses. Template Method lets subclasses redefine certain steps of an
algorithm without changing the algorithm's overall structure.

## Motivation

Many algorithms share the same overall sequence of steps but differ in the
details of one or two of those steps. For example, several data-import
pipelines might all need to: (1) open a source, (2) parse records, (3)
validate them, (4) save to a database, (5) close the source — but *how*
parsing and validation work differs between a CSV importer and a JSON
importer.

Rather than duplicating the entire sequence in every subclass (risking the
sequence itself drifting out of sync between them), Template Method puts
the fixed sequence in a single, non-overridable ("template") method on a
base class, and factors the steps that *do* vary out into separate methods
that subclasses override. The overall algorithm's shape lives in exactly
one place; only the varying details are duplicated across subclasses (and
only where they actually differ).

## Structure

```
AbstractClass
+---------------------------+
| +template_method()  [final]| -- calls, in fixed order:
|     step_one()               step_one()    (maybe implemented here)
|     step_two()      <----    step_two()    (abstract -- must override)
|     step_three()             step_three()  (has a default, MAY override -- "hook")
+---------------------------+
             ^
   +---------+---------+
   |                   |
ConcreteClassA   ConcreteClassB
(overrides       (overrides
 step_two,        step_two,
 step_three)       leaves step_three default)
```

- **Abstract steps** *must* be implemented by subclasses.
- **Hook steps** have a default (often no-op) implementation subclasses
  *may* override, but don't have to — useful for optional extension
  points.
- The template method itself is typically not overridden — it defines the
  fixed skeleton/order of steps.

## Pros

- Eliminates duplicated boilerplate for the parts of an algorithm's
  structure that are common across variants — that structure lives in
  exactly one place.
- **Inversion of control** ("the Hollywood principle" — "don't call us,
  we'll call you"): subclasses provide pieces, but the base class decides
  when and in what order they run, which prevents subclasses from
  accidentally reordering or skipping essential steps.
- Makes extension points explicit via clearly named abstract/hook methods,
  which documents exactly what varies.
- **Open/Closed Principle**: adding a new variant is a new subclass, no
  changes to the base algorithm.

## Cons

- Relies on inheritance, which is a fairly rigid form of reuse — a
  subclass is locked into the base class's skeleton. In Python, favoring
  composition (Strategy) over inheritance is often preferred for this
  reason, especially if variants need to combine behaviors from multiple
  "template" sources.
- Can violate the Liskov Substitution Principle if a subclass overrides a
  step in a way that breaks assumptions the template method or other
  steps make about it.
- As the number of steps/hooks grows, the base class can become harder to
  understand — readers need to check every subclass to know the actual
  runtime behavior for a specific case.

## When to use it

- Several classes contain almost identical algorithms with small,
  well-defined differences — factor the invariant part into a base class.
- You want to control precisely *which* parts of an algorithm subclasses
  are allowed to customize, and prevent them from altering the algorithm's
  overall structure/order.
- You want to avoid duplicating a multi-step sequence across many similar
  classes, keeping that sequence's logic in exactly one place.

## When *not* to use it

- The "variants" of the algorithm actually need to differ in structure,
  not just a couple of steps — Template Method assumes a shared skeleton;
  if that assumption doesn't hold, it forces an awkward fit.
- You need to swap the whole algorithm (not just one step) freely at
  runtime for the *same* object — that's closer to Strategy (composition)
  than Template Method (inheritance).

## Real-world use cases

- Data-processing pipelines (ETL) with a fixed extract-transform-load
  skeleton, where extraction/transformation specifics vary by data source.
- Testing frameworks: `unittest.TestCase` defines a fixed test lifecycle
  (`setUp()` -> test method -> `tearDown()`), with `setUp`/`tearDown` as
  hooks subclasses may override.
- Web framework request-handling base classes that define a fixed
  dispatch sequence (authenticate -> authorize -> handle -> render),
  letting specific views override just the "handle" step.
- Report generation frameworks that fix the overall structure
  (header -> body -> footer) while letting subclasses customize each
  section's content.
- Django's class-based views (`View.dispatch()`) are a well-known,
  large-scale example of this pattern.

## Related patterns

- **Factory Method** is frequently *called from within* a Template
  Method's fixed sequence, to let subclasses control which object gets
  created at one particular step.
- **Strategy** achieves similar goals via composition instead of
  inheritance — prefer Strategy when you want to swap the *entire*
  algorithm at runtime, and Template Method when the *overall structure*
  is fixed and only specific steps vary.
