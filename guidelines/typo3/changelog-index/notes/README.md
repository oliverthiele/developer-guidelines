# Curated notes on changelog entries

One file per changelog number: `{number}.md`.

Everything else in `changelog-index/` is generated and gets overwritten. This
folder is the opposite: **hand-written and never touched by the harvest.** The
index only records that a note exists, via the `note` column.

## When to write one

After a changelog entry was handled **wrongly**, and the correct handling is not
obvious from the `.rst` alone. The note is the memory of that mistake.

Do not write a note that merely restates the changelog — the entry is one grep
away and already says it.

## Format

```markdown
# #104773 — Custom Fluid views and Extbase

**Antipattern:** what was done wrong, concretely.

**Correct:** what to do instead, concretely.

**Why it was tempting:** optional, one line — the reason the wrong version
looked right.
```

## When a note becomes a guideline

A note stays a note as long as it concerns this one changelog entry. It is
promoted into a guideline file — with a `Validity:` line and a
`Stale-knowledge trap:` block — only when the same *class* of mistake recurs.
See the inclusion criterion in `guidelines/README.md`.
