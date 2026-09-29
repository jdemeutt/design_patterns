# Interpreter

**Category:** Behavioral

## Intent

Given a language, define a representation for its grammar along with an
interpreter that uses the representation to interpret sentences in the
language.

## Motivation

Some problems are naturally expressed as a small, domain-specific
language: arithmetic expressions, search-query filters (`price > 10 AND
category = "books"`), regular expressions, or simple rule engines. Rather
than hand-writing an ad-hoc parser/evaluator each time, Interpreter
suggests modeling each grammar rule as a class. A sentence in the language
becomes a tree of these classes (an abstract syntax tree), and
"interpreting" the sentence just means recursively calling an
`interpret()` method on the root of that tree — each node interprets
itself, delegating to its children as needed.

## Structure

```
AbstractExpression (interface)
+------------------+
| +interpret(ctx)   |
+------------------+
        ^
   +----+-----------------------------+
   |                                  |
TerminalExpression              NonterminalExpression
(e.g. a Number literal)         (e.g. Add(left, right) --
+------------------+             holds references to child
| +interpret(ctx)   |             expressions and combines
+------------------+             their interpreted results)
                                 +------------------------+
                                 | +interpret(ctx)          |
                                 +------------------------+
```

- **Terminal expressions** represent the grammar's leaf symbols (numbers,
  variable names, literals) and interpret themselves directly.
- **Nonterminal expressions** represent grammar rules that combine other
  expressions (addition, AND, OR) and interpret themselves by recursively
  interpreting their children and combining the results.

## Pros

- Each grammar rule maps to a class, which makes the grammar (and the
  interpreter) easy to extend: adding a new rule/operator is a new class,
  not a change to a monolithic parser function.
- Makes it easy to change or extend the grammar since it's just Python
  classes (**Open/Closed Principle**).
- Expressions compose naturally as trees, mirroring how most small
  languages are structured anyway (arithmetic, logic, filters).

## Cons

- Scales poorly for **complex** grammars: every grammar rule needs its own
  class, so a non-trivial language ends up with a large, unwieldy class
  hierarchy. For real programming-language-scale grammars, dedicated
  parser generator tools (ANTLR, PLY, Lark, `pyparsing`) are used instead.
- Performance can suffer for deeply nested expression trees interpreted
  repeatedly, since it's tree-walking interpretation rather than
  compilation.
- Overlaps with, and is often superseded by, simply writing a small
  recursive-descent parser plus an `eval`-style function — the "one class
  per grammar rule" formalism is sometimes more structure than the problem
  needs.

## When to use it

- The grammar is simple and unlikely to grow into something huge (a small
  filter/query language, simple arithmetic, basic boolean rules).
- Efficiency isn't the primary concern; clarity and extensibility of the
  grammar's representation matter more.
- You want end users or non-programmers to be able to express rules in a
  small custom language embedded in your application (e.g., search
  filters, pricing rules, validation rules).

## When *not* to use it

- The grammar is large or performance-sensitive — use a proper parser
  generator or hand-written recursive-descent parser with a bytecode/AST
  evaluator instead.
- A general-purpose expression library (e.g., Python's own `eval`,
  restricted safely, or a library like `simpleeval`) already covers the
  need.

## Real-world use cases

- Simple rule engines for business logic (discount rules, access-control
  policies) expressed as a small custom grammar.
- Search query parsers (`field:value AND other:value`) in applications
  with a simplified query language.
- Regular expression engines are a more sophisticated real-world
  relative of this idea (matching, not just evaluating, but conceptually
  similar: pattern components interpret input recursively).
- Template engines that support small embedded expressions
  (`{{ price * quantity }}`) often use an Interpreter-like AST internally.
- Python's own `ast` module + `eval`/`exec` machinery is, at a much larger
  scale, built on exactly this "represent a grammar as a tree of nodes,
  then interpret/compile the tree" idea.

## Related patterns

- The expression tree used by Interpreter is a special case of
  **Composite** (nonterminal expressions are composites of other
  expressions; terminal expressions are leaves).
- **Visitor** is frequently used to add new operations over an
  Interpreter's expression tree (e.g., a `PrettyPrintVisitor` alongside
  the `interpret()` evaluation) without modifying the expression classes.
- **Flyweight** can be applied to terminal expressions (e.g., sharing
  `Number` instances) if the same literals recur often in the tree.
