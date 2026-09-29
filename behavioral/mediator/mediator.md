# Mediator

**Category:** Behavioral

## Intent

Define an object that encapsulates how a set of objects interact.
Mediator promotes loose coupling by keeping objects from referring to each
other explicitly, letting you vary their interaction independently.

## Motivation

Consider a dialog box with many interdependent UI widgets: selecting an
item in a list box might enable a button, checking a checkbox might reveal
a text field, and so on. If each widget directly references and calls
methods on every other widget it needs to affect, you get a dense mesh of
many-to-many dependencies — adding a new widget or changing one
interaction risks breaking several others.

Mediator introduces a single object (the **mediator**) that all the
widgets talk to *instead of* talking to each other directly. Each widget
only knows about the mediator; the mediator knows about all the widgets
and coordinates their interactions. This turns a tangled many-to-many
relationship into a simpler hub-and-spoke (one-to-many) relationship.

## Structure

```
       Mediator (interface)
       +------------------+
       | +notify(sender,   |
       |         event)    |
       +---------+--------+
                 ^
        +--------+---------+
        | ConcreteMediator  |----coordinates--->  ColleagueA
        +------------------+                     ColleagueB
                                                  ColleagueC
Colleague (base)
+------------------+
| -mediator          |----each colleague only
| +some_action()      |    references the mediator,
+------------------+     never other colleagues directly
```

- Each `Colleague` holds a reference only to the `Mediator`, and calls
  `mediator.notify(self, event)` instead of calling other colleagues
  directly.
- The `ConcreteMediator` holds references to all the colleagues and
  contains the actual coordination logic ("when A does X, tell B and C to
  do Y").

## Pros

- **Reduces coupling** between communicating objects from many-to-many
  down to one-to-many (each object <-> the mediator).
- **Single Responsibility Principle**: interaction/coordination logic is
  centralized in one place instead of scattered across many objects.
- **Open/Closed Principle**: you can introduce new colleagues without
  changing existing ones, as long as they only talk through the mediator.
- Simplifies individual objects: each colleague only needs to know how to
  talk to the mediator, not the full API of every other object it might
  need to affect.

## Cons

- The mediator itself can become a **god object** — since it centralizes
  all the coordination logic, it tends to grow complex and become a
  single, hard-to-maintain hotspot as the number of colleagues/
  interactions increases.
- Adds one more object and one more layer of indirection versus direct
  method calls, for the win of reduced coupling.
- Can obscure the overall flow of interaction if the mediator's logic
  itself becomes tangled — moving the mess from "many small tangles" to
  "one big tangle" isn't automatically a win if the mediator isn't well
  organized.

## When to use it

- A set of objects communicate in complex but well-defined ways, and the
  resulting dependencies between them are hard to understand or reuse.
- Reusing an object is difficult because it refers to and communicates
  directly with many other objects.
- You want to customize a behavior that's distributed across several
  classes without creating a lot of subclasses.

## When *not* to use it

- Only a couple of objects interact, and the interaction is simple —
  direct references/calls are clearer than introducing a mediator.
- The "mediator" would just become a thin, pointless pass-through with no
  real coordination logic to centralize.

## Real-world use cases

- GUI dialog/form controllers that coordinate many widgets' enabled/
  visible state based on each other's values.
- Air traffic control: planes (colleagues) don't communicate directly with
  each other — they all communicate through the control tower (mediator),
  which coordinates safe takeoffs/landings.
- Chat room implementations: participants send messages to a central chat
  room/server (mediator), which then distributes messages, rather than
  peers connecting directly to every other peer.
- Workflow/orchestration engines that coordinate calls between several
  independent services or steps, so the services don't need direct
  knowledge of each other.

## Related patterns

- **Observer** is often used to implement the notification mechanism
  between colleagues and the mediator (colleagues "publish" events; the
  mediator "subscribes" and reacts).
- **Facade** also introduces a single object that other code goes through,
  but Facade provides a simplified interface *to a subsystem* (typically
  one-directional: client -> subsystem), whereas Mediator coordinates
  *bidirectional* interaction *among peer objects* that would otherwise
  reference each other.
- Can be combined with **Singleton**, since usually only one mediator
  instance is needed per coordinated group.
