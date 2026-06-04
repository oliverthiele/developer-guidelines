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

Do NOT add `Co-Authored-By: Claude ...` in public repositories (e.g. Packagist packages).

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

Tag always on the merge commit in `main` — never on `develop`.

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
