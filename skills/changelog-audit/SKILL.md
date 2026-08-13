---
name: changelog-audit
description: Audit the guidelines against the TYPO3 changelog index and propose entries that should become a rule or at least a pointer. Use after regenerating the changelog index, after a core update, or when checking whether the guidelines still reflect current TYPO3.
---

# Changelog Audit

Compares the guideline files against the changelog index and ranks entries that
touch something the guidelines already talk about but do not cite.

```bash
python3 skills/changelog-audit/audit.py
```

## Why it needs a memory

Finding candidates is trivial and worthless: 800 indexed entries face roughly a
dozen citations, so a naive run reports hundreds of hits, gets skimmed once and
is never read again.

Every entry therefore has exactly one of three states:

| State | Where it is recorded |
|---|---|
| covered | a guideline cites `#number` — detected automatically |
| judged | a row in `changelog-index/reviewed.tsv` |
| open | shown by the audit |

After the first triage a run shows only what is genuinely new — a handful after
a core update instead of hundreds.

## Triaging

Record a verdict for **everything** the audit shows, in
`guidelines/typo3/changelog-index/reviewed.tsv`:

```
105441	todo	TCA select with null item values — decide whether developer.md needs a line
102935	not-relevant	Extension Manager internals, no extension code affected
```

- **covered** — a rule now exists; usually unnecessary, because citing the
  number in the guideline is enough
- **not-relevant** — decided against, with the reason. The reason is the point:
  it stops the same entry being re-argued in a year
- **todo** — worth doing, not done. Stays visible in the file rather than
  vanishing from the report

Leaving an entry unjudged means it comes back every run. That is intended.

## How the ranking works

Two signals, deliberately different in weight:

- **symbols** (weight 4) — a class or method name from the entry that appears in
  a guideline file. Strong: a class named in a guideline is a subject of it
- **title terms** (weight 1) — distinctive words from the entry title found in
  the guideline text. Weak, but the signal that catches non-PHP topics. The
  XLIFF whitespace change (`#70867`) has no PHP symbols at all

Plus a type weight: `Breaking` and `Important` count 4, `Deprecation` 3,
`Feature` 1 — what silently changes behaviour outranks what adds possibilities.

Two filters keep the list usable:

- Title words occurring in more than 2% of all entries are dropped. Growing a
  stopword list by hand does not scale; measuring the corpus does
- Only rule and practice files are matched. Index files (`README.md`,
  `versions.md`) name every topic and would dominate the ranking while never
  being the file that needs changing. Files outside `typo3/` and `xliff/` cannot
  be affected by a TYPO3 changelog at all

Citations, however, are read from **all** files — most of them live in
`versions.md`.

## What it cannot do

It only sees topics the guidelines already mention. A subject absent from them
entirely will never surface — that gap belongs to
[practice guides](../../guidelines/typo3/practices/README.md), not here.

And it proposes; it does not decide. Relevance is a judgement about how we work,
which no ranking can make.

## First run, as a record

The first audit found that `TypoScriptFrontendController` and `$GLOBALS['TSFE']`
were deprecated in v13 and removed in v14 while the guidelines said nothing
about it — seven of the twenty-four candidates were facets of that one change.
That is the intended kind of finding: not a missing detail, but a subject the
rules had never covered.
