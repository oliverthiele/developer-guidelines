# Oliver Thiele — Developer Guidelines

Project-independent coding guidelines for all PHP/TYPO3 projects.
Intended for use by developers and as context for AI-assisted development.

## Core Principle

Always prefer minimal, targeted changes.

- Do not refactor existing structures unless explicitly required
- Do not rename variables, methods, or files without necessity
- Preserve existing comments and architecture
- Extend instead of rewriting

## Setup

Clone this repository as a sibling directory next to your projects:

```
PhpstormProjects/
├── developer-guidelines/    ← this repo
├── my-project-a/
├── my-project-b/
└── ...
```

The default path used in `CLAUDE.md` and memory files is
`../developer-guidelines/guidelines/` (relative to the project root).

If the guidelines are located elsewhere, set the environment variable
`DEVELOPER_GUIDELINES_DIR` to the absolute path of the `guidelines/` directory.

Update with `git pull` in this repository — every project reads it directly, so there
is no copy to refresh. Do not vendor these files into a project (no submodule, no
duplication); that would pin each project to a commit and defeat the single pull.

### Project-specific guidelines

Rules that hold for one project only — CSS prefix assignments, build paths, extension
conventions — do not belong in this repository. They live in a `Guidelines/` folder in
the project root, committed with the project:

```
PhpstormProjects/
├── developer-guidelines/    ← this repo, shared rules
└── my-project/
    └── Guidelines/
        └── README.md        ← index of the project rules
```

**`Guidelines/` is evaluated first**, before any file in this repository — comparable to
`Configuration/TCA/Overrides/` in TYPO3, which refines the base definition rather than
replacing it. One difference matters: nothing loads `Guidelines/` automatically. The
project's own `CLAUDE.md` has to point at it, which is what the setup below does.

**On conflict, the project file wins.** Every override there names the shared rule it
replaces and the reason for it.

Never copy shared rules into a project folder. If a rule holds for every project,
propose it here instead.

The folder is spelled `Guidelines/` with a capital G in every project. This is binding:
macOS resolves paths case-insensitively, Linux and CI do not, so a mixed spelling works
on one machine and silently fails on another.

### Setting up a project

Three steps, once per project.

**1.** Create `Guidelines/README.md` as the index — precedence rule, and a table naming
which file covers which work area.

**2.** Point the project's `CLAUDE.md` (and `AGENTS.md`, if present) at it. The project
file must be self-contained — never refer to a personal `~/.claude/CLAUDE.md`, since
collaborators do not have it:

```markdown
## Guidelines — mandatory read protocol

Project rules live in `Guidelines/`. They extend the shared, project-independent
guidelines cloned next to this project in `../developer-guidelines/guidelines/`.

**Read the relevant file before starting work in that area** — also when the task
looks small or the rule seems obvious.

@Guidelines/README.md

On conflict, the project file wins. Never edit files in `../developer-guidelines/`
without explicit confirmation.
```

**3.** Commit `.claude/settings.json` so reading the shared guidelines does not prompt
every collaborator:

```json
{
  "permissions": {
    "allow": [
      "Read(../developer-guidelines/guidelines/**)"
    ]
  }
}
```

## How to use

Each guideline file covers one technology or topic area.

- Load only the relevant guideline file(s) for the current task
- Follow rules strictly — do not reinterpret them
- Prefer existing project patterns over introducing new ones

## Guidelines

| File                                               | Topics                                                                                 |
|----------------------------------------------------|----------------------------------------------------------------------------------------|
| [xliff.md](xliff.md)                               | XLIFF 1.2 / 2.0 file format, attributes, source/translation conventions                |
| [typo3-developer.md](typo3-developer.md)           | TCA, Doctrine DBAL, Fluid — universal + links to version files                         |
| [typo3-integrator.md](typo3-integrator.md)         | TypoScript, translations — universal + links to version files                          |
| [typo3/content-blocks.md](typo3/content-blocks.md) | Content Block structure, portable assets, two-layer CSS, config.yaml                    |
| [typo3/v13/developer.md](typo3/v13/developer.md)   | v13-specific: Fluid 4 argument types, custom views, union types                         |
| [typo3/v13/integrator.md](typo3/v13/integrator.md) | v13-specific: SiteSets, labels.xlf key naming, @import, CE wizard                       |
| [typo3/v14/developer.md](typo3/v14/developer.md)   | v14-specific: Fluid 5, FlexForm DS, TCA shortform, extension title, record-transformation |
| [php.md](php.md)                                   | Naming conventions, PHPStan, PHP CS Fixer, type safety                                 |
| [testing.md](testing.md)                           | Quality checks, execution order, PHPUnit, Playwright                                   |
| [git.md](git.md)                                   | Branching workflow, commit messages, release process                                   |
| [scss.md](scss.md)                                 | Bootstrap-first, CUBE CSS, prefix system, custom properties, state classes             |
| [javascript.md](javascript.md)                     | data-js hooks, Bootstrap JS, ID conventions, framework choice                          |
| [vue.md](vue.md)                                   | Component syntax, script setup, state management, when to use Vue                      |
| [playwright.md](playwright.md)                     | Playwright test patterns, visual regression, functional tests, helpers                 |
| [documentation.md](documentation.md)               | README.md and CHANGELOG.md structure for Packagist extensions                          |

## General rules (apply everywhere)

- Code comments and documentation: **English only**
- No abbreviated variable names — always write them out in full
    - `$breakpoint` not `$bp`
    - `$configuration` not `$config`
    - `$identifier` not `$id`
    - Exception: single-letter loop variables (`$i`, `$k`) are acceptable in
      small loops
- No emojis in code, comments, or documentation unless explicitly requested
- IDE: PhpStorm
- Shell: commands always via `ddev` (e.g. `ddev composer ...`,
  `ddev exec typo3 ...`)

## Decision Rules

- Prefer minimal changes over refactoring
- Follow existing project structure and patterns
- Do not introduce abstractions for one-time use
- Trust framework guarantees — avoid defensive overengineering

## File and directory naming

`UpperCamelCase` for all directories and file names, unless TYPO3 or a tool
requires otherwise.

```
./Directory/SubDirectory/FileName.ext
```

Common exceptions required by TYPO3 or tooling:

- `Configuration/page.tsconfig`
- `config/system/settings.php`
- `composer.json`, `package.json`
- `webpack.config.js`
