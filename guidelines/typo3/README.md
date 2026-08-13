---
title: TYPO3 guidelines index
scope: typo3
applies_to: []
typo3: ["13", "14"]
see_also: ["typo3/versions.md", "README.md"]
---

# TYPO3 Guidelines

All TYPO3 rules live in this folder. Load the file matching the work area.

| File | Covers |
|---|---|
| [integrator.md](integrator.md) | TypoScript, SiteSets, CE wizard, backend configuration |
| [developer.md](developer.md) | PHP, TCA, Fluid, Doctrine DBAL, views |
| [content-blocks.md](content-blocks.md) | Content Block structure, assets, two-layer CSS, `config.yaml` |
| [sitekit.md](sitekit.md) | SiteKit layer model and template path abstraction (SiteKit-based projects only) |
| [practices/](practices/README.md) | decision guides: which approach, and when deliberately not |
| [versions.md](versions.md) | which rule applies to which TYPO3 version |
| [changelog-index/](changelog-index/) | every core changelog entry — **grep only, never read whole** |

XLIFF is not in this folder: the format itself is not TYPO3-specific. See
[../xliff/](../xliff/), whose `typo3.md` covers `labels.xlf` and SiteSet labels.

## How versions are handled

**A rule lives once, in the topic file, and states the versions it applies to.**

```markdown
### TypoScript includes — `@import`, not `<INCLUDE_TYPOSCRIPT:`

**Validity:** deprecated in v13 · removed in v14 · [#105171](…)
```

No `**Validity:**` line means the rule holds for every supported version.

**Major versions only, and dated by usability.** Live sites are updated at LTS
releases, so every site runs the latest minor of its major — `13.1` and `13.4`
are equally available in a v13 project, which makes the minor version a number
nobody decides anything on. Write `v13+`, `deprecated in v13 · removed in v14`.
The exact minor stays available in column 3 of the changelog index.

For the same reason a validity states when something became usable **in
practice**, not when the API first appeared. `record-transformation` exists in
v13 but only becomes worth using in v14, where it is applied automatically and
the surrounding record handling exists — so it is documented as v14.

This replaces the earlier "base file plus per-version overlay" layout. That
layout encoded *"introduced in"* but was read as *"applies only to"* — four of
the five rules in the former `v13/integrator.md` were current rules that hold in
v14 unchanged, and a fifth (`@import`) was *more* binding in v14 while filed
under v13. Reading a single file per topic removes that reconstruction step.

### When a version subfolder is justified

A `v{major}/` subfolder is for rules that cannot be expressed as one rule with a
validity line — where the same task needs substantially different **explanations**
per version, not just a different value or a two-line code pair.

There is currently no such case: every version difference in this repository
(Fluid 4 vs. 5 argument types, FlexForm DS registration, `showitem` shortform)
is clearer as one rule showing both variants side by side. The convention is
documented here so a future divergence has a defined home, not because a folder
is waiting to be filled.

### Stale-knowledge traps

Where the correct rule contradicts what a language model is likely to produce
from training data, the rule carries an explicit marker:

```markdown
> **Stale-knowledge trap:** `GeneralUtility::makeInstance(StandaloneView::class)`
> is the single most common way to build a view in older code and training data.
> It is gone in v14.
```

This is deliberately stronger than a normal rule. It names *why* the default is
wrong, which is what makes it survive under context pressure.

## Rules and practice guides

A rule file says *what is correct*. A [practice guide](practices/README.md) says
*which approach to choose and when deliberately not* — longer, read when a
decision is pending rather than on every change in the area. Menus moving from
`HMENU` to a DataProcessor plus Fluid is that kind of knowledge: no changelog
entry marks it, and it is the part a language model gets wrong most confidently.

## The three levels

| Level | What | When read |
|---|---|---|
| 1 — guideline files | rules where AI or humans repeatedly get it wrong | whenever working in the area |
| 2 — `versions.md` | validity table, points at the rule | on version doubt |
| 3 — `changelog-index/` | every core changelog entry | never read whole — grep by number or symbol |

Level 3 is entered from an ExtensionScanner or PHPStan finding:

```bash
grep -h 'StandaloneView' guidelines/typo3/changelog-index/v1*.tsv
```

A hit often answers the question from the index line alone. See
`skills/typo3-changelog-harvest/SKILL.md` for the query workflow, the trust
order of the columns, and how to record a note when a migration went wrong.
