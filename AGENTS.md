# AGENTS.md

Entry point for AI coding assistants working in a repository that uses these
guidelines. Contains no rules of its own — it says which file to read, and in
what order.

## Read order

1. **The project's `Guidelines/README.md`**, if the project has one. Project
   rules are evaluated first and win on conflict.
2. **[`guidelines/README.md`](guidelines/README.md)** in this repository — the
   index. Its table maps a work area to the one file that covers it.
3. **The file that table names for the current task.** Only that one.

Do not load the whole repository. Each guideline file is self-contained and
names its related files in its `see_also` frontmatter.

## When a rule is missing

Look it up, ask, and do not invent a fallback — the full rule is in
[`guidelines/README.md` → When a rule is missing](guidelines/README.md#when-a-rule-is-missing).
For TYPO3 version questions, grep
[`guidelines/typo3/changelog-index/`](guidelines/typo3/changelog-index/) instead
of answering from memory; never read those files whole.

## Editing

Never change a file under `guidelines/` without explicit confirmation. Rules
that hold for one project only belong in that project's `Guidelines/` folder,
never here.

## Other assistants

Tools with their own entry file — `CLAUDE.md`, `.cursor/rules`, Copilot
instructions — should point at this file rather than restate it. A copied rule
drifts from the original; a pointer cannot.
