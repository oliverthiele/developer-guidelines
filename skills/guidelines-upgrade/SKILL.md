---
name: guidelines-upgrade
description: Bring a project's references to the shared developer guidelines up to date after the guidelines were restructured, and check that reading them is pre-granted. Use when guideline paths in a project point at files that no longer exist, when onboarding a project, or after pulling a new guidelines release.
---

# Guidelines Upgrade

Checks a project against the current release of the shared guidelines and
rewrites references that point at files which have moved.

Run it in the project that needs updating:

```bash
python3 ../developer-guidelines/skills/guidelines-upgrade/upgrade.py
```

Reports only. Add `--apply` to write, and `--apply --grant-read` to also add the
missing read permission. Nothing is ever committed — review the diff and commit
it with the project's own conventions.

## What it checks

**1. Are the guidelines reachable?** Looked for as a sibling clone
(`../developer-guidelines/guidelines/`) or via `DEVELOPER_GUIDELINES_DIR`. If
neither exists, that is the finding — everything else is moot.

**2. Is reading them pre-granted?** `.claude/settings.json` must allow
`Read(../developer-guidelines/**)` — the whole repository, since `AGENTS.md` is
in the root and `skills/` sits next to `guidelines/`. Without it every single
read prompts, and the predictable result is that someone copies guideline text
into the project instead of referencing it — which is exactly what the shared
repository exists to prevent.

**3. Do the referenced files still exist?** Scans `CLAUDE.md`, `AGENTS.md`,
`.claude/memory/*.md`, `Guidelines/**`, `docs/*.md` — and the project's global
memory at `~/.claude/projects/<slug>/memory/*.md`, which lives outside the
project and is therefore the easiest place for stale references to survive
unnoticed. Looks for guideline paths,
rewrites known moves, and lists anything referenced that no longer exists and is
not covered by the map. Those need a human decision — the rule may have moved
somewhere the map does not know about, or it may have been dropped.

A reference is resolved against the repository root when it names one
(`../developer-guidelines/AGENTS.md`), and against `guidelines/` otherwise. Not
everything referenced lives under `guidelines/`: `AGENTS.md` is the prescribed
entry point and `skills/` sits beside it, so resolving those against
`guidelines/` would report a correctly set up project as broken.

## The path map

`path-map.tsv` lists every move ever made, with the release that made it:

```
2.0.0	typo3-integrator.md	typo3/integrator.md
2.0.0	xliff.md	xliff/README.md
```

This is what makes the skill outlive the restructuring it was written for. A
project that skipped two releases is carried forward correctly, because the map
holds the whole history rather than the last step.

**When guidelines move, add rows here in the same commit.** Append only — never
edit or delete a row, or projects still on the old layout lose their path
forward. Longest old path is applied first, so `typo3/v13/integrator.md` is
handled before any shorter pattern that overlaps it.

Hyphenated legacy names are also rewritten without the `.md` suffix, since prose
and tables often name them bare (`typo3-developer` → `typo3/developer`). Short
names are deliberately not treated that way — a bare `xliff` would match far
too much.

## Running it without the skill installed

The skill lives in the guidelines repository, so any project with the sibling
clone can use it even if nothing is installed locally. The prompt is enough:

> Evaluate `../developer-guidelines/skills/guidelines-upgrade/SKILL.md` and
> bring this project up to date.

## Limits

It rewrites paths, not prose. A memory file that describes the *old structure*
("universal file plus version-specific overlays") is not something a path map
can fix — the skill reports the file, the wording is a human's job.
