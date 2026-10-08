# Oliver Thiele — Developer Guidelines

Personal coding guidelines for PHP/TYPO3 projects.

Published primarily for developers who collaborate with me on projects — the
rules here reflect how I structure, name, and maintain code across all my work.

---

## Contents

### `AGENTS.md`

Entry point for AI coding assistants: read order, and what to do when a rule is
missing. See [AGENTS.md](AGENTS.md). `CLAUDE.md` only imports it, so that
Claude Code loads it inside this repository.

### `guidelines/`

Technology- and topic-specific coding guidelines that apply to **all projects**.
Two files sit next to them and are read once, not per task:
[setup.md](guidelines/setup.md) (placing the repository, wiring up a project)
and [tooling.md](guidelines/tooling.md) (the packages that check rules
automatically).

Which file covers which work area: the
[routing table in AGENTS.md](AGENTS.md#routing), the one list of guideline files.

See [guidelines/README.md](guidelines/README.md) for shared rules that cut
across
all files (naming, formatting, tooling).

Changes between releases are documented in [CHANGELOG.md](CHANGELOG.md).

### `skills/`

Claude Code skills that work with these guidelines. They live in this
repository because they depend on its structure and must stay in sync with it.

| File                                                               | Topics                                                                              |
|--------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| [typo3-changelog-harvest](skills/typo3-changelog-harvest/SKILL.md) | Build and query the TYPO3 changelog index                                           |
| [changelog-audit](skills/changelog-audit/SKILL.md)                 | Find changelog entries the guidelines should react to, with a triage log            |
| [guidelines-upgrade](skills/guidelines-upgrade/SKILL.md)           | Update a project's guideline references after a restructuring, and check permissions |
| [create-content-block](skills/create-content-block/SKILL.md)       | Scaffold a TYPO3 Content Block following the shared conventions                     |

See [skills/README.md](skills/README.md) for installation.

---

## How to use

**As a developer working with me:**
Load the relevant guideline file(s) for the area you are working in and follow
the rules as written. When in doubt, prefer the existing project pattern over
introducing a new one.

**As an AI assistant:**
Start with [AGENTS.md](AGENTS.md). Load only the files relevant to the current
task. Follow rules strictly — do not reinterpret or override them based on
general conventions. The guidelines take precedence over defaults. When a rule
is missing, look it up or ask — never invent a fallback.

---

## License

These guidelines are published for reference and collaboration. Feel free to
adapt
them for your own projects.
