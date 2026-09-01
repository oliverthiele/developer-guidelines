---
title: Git workflow
scope: git
applies_to:
  - "**/.git/**"
see_also: ["documentation.md"]
---
# Git Guidelines

Git workflow and commit conventions for all projects.

These rules are mandatory unless explicitly overridden.

---

## Core Principles

- Keep commits small, focused, and reviewable
- Use consistent commit message format
- Commits must only be created on explicit user request (no autonomous commits)
- Follow project workflow strictly

---

## Formatting

Formatting is defined in `.editorconfig`.

Fallback:

- charset: utf-8
- end_of_line: lf
- insert_final_newline: true
- trim_trailing_whitespace: true

---

## Commit Messages

### Format

`[TYPE] Imperative description`

Examples:

```
[TASK] Add gallery image srcset ViewHelper
[FEATURE] Add pagination support to gallery plugin
[BUGFIX] Fix missing crop context in FAL file references
[DOCS] Update README with SiteSet dependency instructions
[!!!][TASK] Remove deprecated AbstractPlugin base class
[!!!][BUGFIX] Fix session handling — drops old cookie format
```

### Tags

| Tag         | When to use                                         |
|-------------|-----------------------------------------------------|
| `[FEATURE]` | New user-facing functionality                       |
| `[TASK]`    | Maintenance, refactoring, build, dependency updates |
| `[BUGFIX]`  | Bug fix                                             |
| `[DOCS]`    | Documentation only                                  |
| `[!!!]`     | Breaking changes                                    |

### Rules:

- **English only** — always, no exceptions
- Imperative mood: "Add", "Fix", "Remove" — not "Added" or "Fixes"
- No period at the end of the subject line
- Keep subject concise and specific
- Do not mix unrelated changes in one commit

---

## Commit Style (TYPO3)

- Technical and factual — describe what was changed in code or configuration only
- No marketing language or speculation
- No invented benefits ("improves", "enhances")
- Focus on real code/config changes

TYPO3 conventions:

- PSR-12
- TypoScript
- Fluid
- Extbase patterns

---

## Co-Authored-By

Never add `Co-Authored-By: Claude ...` — or any other mention of AI tools — to
commit messages or PR descriptions. This applies to **all** repositories,
public and private alike.

---

## Pre-Staging Checklist

Run these checks **before `git add`** — not just before committing.
Staging unformatted or statically invalid code forces an amend or an extra fixup commit.

```bash
# 1. Static analysis — fix any errors manually before auto-formatting
ddev composer phpstan          # whole project
ddev composer phpstan:ot-faq  # or scoped to the package being released

# 2. Auto-format PHP — runs after manual fixes so the formatter covers them too
ddev composer php-cs-fixer
```

Only stage files after both tools pass without errors.

---

## Commit Authorization

- Commits must only be created on explicit user request (no autonomous commits)
- Do not rewrite history unless instructed

---

## Verify the branch before committing

Check the currently checked-out branch (`git branch --show-current` or
`git status`) immediately before every `git commit` — not once at the start of
a session, but again right before each individual commit, since a prior
`checkout`, `reset`, or a manual fix run by someone else in between can have
moved it without that being obvious from context.

There is no single correct branch to check against — it depends on what is
actually being worked on: `develop`, a `feature/*` branch, a `hotfix/*` branch,
or something else. The check is procedural, not a fixed target.

**`main` is the one exception worth calling out on its own.** In the standard
release workflow (`develop` → release-merge `--no-ff` → `main`, tag on the
merge commit), the only commit that legitimately lands directly on `main` is
that merge commit. A commit on `main` carrying actual file content — not a
merge — is almost always a mistake, regardless of the project's specific
workflow.

---

## No customer data in public repositories

Public repositories — guideline sets, published extensions, anything on Packagist
or a public GitHub remote — must never contain material that identifies a customer
or a customer project.

**The risk is fingerprinting, not naming.** A single detail rarely identifies
anyone; several harmless-looking ones together do. A product term, a language
count and a category name narrow the field to one company for any reader who
knows the sector. Assume every detail will be combined with every other one.

Never commit — in code, comments, documentation, examples, or commit messages:

**Names and identifiers**

- customer names, company names, project names, domains, hostnames
- real extension keys, vendor names, package names
- server names, IP addresses, paths, credentials
- excerpts from customer content, data or screenshots

**Vocabulary taken from the project**

- product, article or object names, article numbers, SKUs
- category names, tag names, menu labels, section titles
- project-specific CSS classes, JS variables and `data-js` values, TypoScript
  object paths, database table or column names

**Quantities — these identify too**

- number of defects, findings, or affected records
- number of languages, sites, domains, or editors
- number of content elements, extensions, or templates

A count reads as neutral, which is why it slips through. It is not: a figure
describes one specific project, and it also reads as if the author had built
those defects rather than inherited them.

Use neutral placeholders instead: `my_extension` / `MyExtension`,
`my_sitepackage`, `example.com`, `acme`. An example must not be traceable to a
real engagement. **State the mechanism, not the measurement** — why something
accumulates unnoticed is the transferable part; how much of it one project had
is not.

Check before every commit to a public repository. This applies to examples and
commit messages in particular — they are the easiest place to leak without
noticing, and a pushed commit keeps the text in its diff even after a later
commit corrects it. The fix has to happen before the push, or the history has to
be rewritten.

Project-specific material belongs in that project's own repository, in its
`Guidelines/` folder — see the setup section in `guidelines/README.md`.

---

## Branch Model

```
main          — stable, tagged releases only
develop       — integration branch, all feature work merged here first
feature/*     — short-lived feature branches (optional, TYPO3 extension work)
```

Rules:

- Development happens on `develop` or feature branches
- `main` only receives merges from `develop`
- Never commit directly to main
- Never use `--force` on main branch

## Release Workflow

1. Finish work on develop
2. Update extension version in ext_emconf.php
3. Create PR develop → main
4. Merge via GitHub
5. Create tag on the merge commit in `main`

```bash
git tag -a 1.2.0 -m "Release 1.2.0"
git push origin 1.2.0
```

Rules:

- Tag only on main merge commit
- Never tag on develop

Use `--no-ff` only when merging locally (GitHub PR merges are already non-fast-forward).

## First Push on a New Repository

Always push `main` before `develop` when initializing a new repository on GitHub.

GitHub sets the **first pushed branch as the default branch**. If `develop` is pushed first, it becomes the default and branch protection rules apply to `develop` instead of `main`.

Correct order:

```bash
git push origin main      # first — becomes default branch on GitHub
git push origin v0.1.0    # tag
git push origin develop   # after main is established
```

Set branch protection for `main` on GitHub afterwards.

---

## CHANGELOG.md

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) + Semantic Versioning.

Example:

```markdown
## [1.2.0] — 2025-06-15

### Added

- Gallery pagination via ArrayPaginator

### Fixed

- Missing crop context when using FAL source

```

Rules:

- Use sections: `Added` / `Changed` / `Fixed` / `Removed`
- Only include sections that apply
- Separate file
- No inline changelogs in README

---

## GitKraken / AI Instructions (Copy & Paste)

These blocks can be copied 1:1 into GitKraken under Preferences > GitKraken AI, so both Claude Code in the terminal and
GitKraken use the same instructions.

The following section headings are intended to match the corresponding fields in GitKraken AI settings.

### Global Instructions

```
Context: TYPO3 extension development

Style:
- Technical and factual — describe what was changed in code or configuration only
- Imperative mood for commits ("Add", "Fix", "Update")
- No speculation, marketing language, or invented benefits
- Focus on actual code/config changes

TYPO3 conventions: PSR-12, TypoScript, Fluid, Extbase patterns

CRITICAL: Never append "Co-Authored-By" or any mention of AI tools in commit messages or PR descriptions.
```

### Commit Message Generation

```plaintext
TYPO3 format:
[TYPE] Subject (max 52 chars, imperative)

Body: List changes, one per line.

Types: [BUGFIX], [FEATURE], [TASK], [DOCS], [!!!]

Example:
[FEATURE] Add FAL support for user avatars

- Add FileReference field to fe_users TCA
- Update UserRepository with file handling
- Add Fluid partial for avatar display
```

### Explain Changes

```markdown
Analyze from TYPO3 developer perspective:

- Affected components (Controller, Model, TCA, TypoScript, Fluid)
- Technical impact on extension functionality
- Database/TCA schema changes
- Breaking changes or migration needs

Technical facts only. No "improves" or "enhances".
```

### Stash Message Generation

```markdown
Brief WIP description:

Format: "WIP: [component] what's in progress"

Examples:

- "WIP: FormController validation logic"
- "WIP: TCA config for new field"
- "WIP: Fluid templates restructure"

Max 50 chars. Component + task.
```

### Pull Request

```markdown
TYPO3 PR format:

## What does this change?

- factual bullet list
- no marketing language

## Technical details

- affected components
- TCA changes
- breaking changes

## Testing

- how to test

Technical and concise.
```

### Conflict Resolution

```markdown
Technical conflict analysis:

- Identify conflicting components (TCA, TS, PHP)
- Compare changes
- Resolve via TYPO3 best practices
- Flag breaking changes

Precise. No assumptions about "better" solutions.
```

### Commit Composer

```markdown
Split changes into logical TYPO3 commits:

Strategy:

1. Database/TCA changes ([TASK]/[FEATURE])
2. Backend logic (Controller, Repository, Model)
3. Frontend (Fluid, TypoScript, Assets)
4. Configuration (ext_*, Services.yaml)
5. Documentation ([DOCS])

Each commit independently functional.
2-4 commits typical. Don't over-split.

Use TYPO3 commit format for each.
```
