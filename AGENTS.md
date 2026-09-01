# AGENTS.md

Entry point for AI coding assistants working in a repository that uses these
guidelines. Contains no rules of its own — it says which file to read, and in
what order.

## Read order

1. **The project's `Guidelines/README.md`**, if the project has one. Project
   rules are evaluated first and win on conflict.
2. **[`guidelines/README.md`](guidelines/README.md)** in this repository — the
   index. Its table maps a work area to the one file that covers it.
3. **The file that table names for the current task** — one per work area the
   task actually touches. A task that changes extension PHP and its Playwright
   tests reads those two; it does not read the rest.

Do not load the whole repository. Each guideline file is self-contained and
names its related files in its `see_also` frontmatter — follow those when the
file itself points at them, not preemptively.

## Document types

Four kinds of file, read in different situations:

| Type | Where | Read it |
|---|---|---|
| Rule files | `guidelines/*.md`, `guidelines/typo3/*.md`, `guidelines/fluid/*.md`, `guidelines/xliff/*.md` | Whenever work touches the area |
| Practice guides | [`guidelines/typo3/practices/`](guidelines/typo3/practices/README.md) | When choosing an approach — which one, and when deliberately not |
| Version table | [`guidelines/typo3/versions.md`](guidelines/typo3/versions.md) | When a rule depends on the TYPO3 version |
| Changelog index | [`guidelines/typo3/changelog-index/`](guidelines/typo3/changelog-index/) | Grep only, for a specific API or changelog number |

Architecture decisions are the practice guides' job. Do not settle "component or
partial", "ViewHelper or DataProcessor" from general knowledge without checking
whether a guide covers it.

## When a rule is missing

Look it up, ask, and do not invent a fallback — the full rule is in
[`guidelines/README.md` → When a rule is missing](guidelines/README.md#when-a-rule-is-missing).
For TYPO3 version questions, grep
[`guidelines/typo3/changelog-index/`](guidelines/typo3/changelog-index/) instead
of answering from memory.

**Grep those files, never read one whole.** They hold every core changelog entry
since v13 — over 800 lines and 320 KB across three files, most of it symbol
lists, and growing with every core release. `v14.tsv` alone is 170 KB: reading
it loads about as much text as every guideline file in this repository combined,
to answer a question a single `grep` answers exactly.

## Editing

Never change a file under `guidelines/` without explicit confirmation. Rules
that hold for one project only belong in that project's `Guidelines/` folder,
never here.

## Other assistants

Tools with their own entry file — `CLAUDE.md`, `.cursor/rules`, Copilot
instructions — should point at this file rather than restate it. A copied rule
drifts from the original; a pointer cannot.
