---
title: Practice guides
scope: typo3
kind: practice
applies_to: []
typo3: ["13", "14"]
see_also: ["typo3/README.md"]
---

# Practice guides

Decision guidance: **which approach, and when deliberately not.** A fourth
document type next to the rule files, the version table and the changelog index.

| File | Decision it covers |
|---|---|
| [fluid-components.md](fluid-components.md) | Component or partial, Atomic Design levels, v13 vs v14 registration |

## Why these are separate files

The rule files (`../integrator.md`, `../developer.md`) are read whole whenever
work touches their area. A decision guide is long-form and only needed when the
decision is actually being made — putting it there would charge every small
TypoScript change for an essay nobody needs at that moment.

They also answer a different question. The changelog says *what changed*. A
practice guide says *why the approach shifted and when to adopt it*. Some of
these shifts have no changelog entry at all: menus moving from `HMENU` to a
DataProcessor plus Fluid happened over years, as a change in practice rather
than as a release.

This is the content least derivable from a language model's training data,
because the old approach dominates a decade of examples on the internet.

## Structure

```markdown
## Decision      — what is the standard approach today
## When not to   — where the decision deliberately goes the other way, and why
## Why           — what drove the shift
## v13 vs v14    — is it worth adopting now or after the upgrade
## Migration     — what happens to existing code
```

**"When not to" is the most important section.** Without it a rule gets
overgeneralised: "use components" turns into components where a partial was
right. State the boundary explicitly.

## Writing one

Write a guide when the decision is actually pending — never as a stub on
suspicion. These files carry judgement, not facts, and judgement that nobody
needed yet ages badly.

Separate the two sources plainly:

- **Verifiable** — version numbers, APIs, file layouts, core behaviour. Check
  them against the changelog index and the core source, and cite them.
- **Judgement** — when adoption pays off, where the boundary runs, what stays
  untouched. This comes from the maintainer. Ask; do not infer it from what
  seems reasonable.

Where a guide is uncertain, say so in the file. An honest gap is more useful
than a smooth sentence that invents a position.
