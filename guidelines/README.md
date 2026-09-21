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

How to clone this repository next to a project, how a project's own
`Guidelines/` folder relates to it, and the three steps that wire a project up:
[setup.md](setup.md). Read it once per project, not per task.

## How to use

Each guideline file covers one technology or topic area.

- Load only the relevant guideline file(s) for the current task
- Follow rules strictly — do not reinterpret them
- Prefer existing project patterns over introducing new ones

## When a rule is missing

These files do not cover everything, and they are not meant to. When a task
needs a TYPO3 API, a TCA type, a configuration key or a convention that neither
a guideline nor the project's own `Guidelines/` folder covers:

1. **Establish the version first.** Which TYPO3 version does *this* project run?
   Read it from `composer.lock` or `vendor/typo3/cms-core/`, never from memory
   and never from the version a neighbouring project uses. Every answer below
   depends on it, and a right answer for the wrong version is still wrong.

   For a **reusable extension**, the installed version is only half the answer:
   `composer.json` says which range it has to support. An API confirmed in the
   installed v14 core proves nothing about the v13 the extension also declares —
   check the lower bound in the changelog index, and either stay on what both
   carry or branch on `Typo3Version`.
2. **Grep the changelog index.** For version questions — does this class still
   exist, what replaced it, when was it removed —
   [typo3/changelog-index/](typo3/changelog-index/) answers it. Grep it, never
   read it whole.
3. **Read the installed source.** A changelog says what *changed*; it does not
   say how an API is meant to be used. The code in the project's own `vendor/`
   is the version that actually runs — class signatures, docblocks and the
   core's own usages of a class settle most API questions in a minute. Prefer it
   over the published documentation, which defaults to another version, and over
   memory, which has no version at all.
4. **Read the surrounding project code.** The binding pattern for anything
   project-specific. It can be outdated — check it against steps 2 and 3 before
   copying it.
5. **Ask.** If that does not settle it, stop and ask. An unanswered question
   costs one message; a wrong assumption is found in review, or later.
6. **Never invent a fallback.** Do not write against a remembered API, do not
   reconstruct a missing rule by analogy from a neighbouring guideline, and do
   not carry a pattern over from an older TYPO3 version because it used to work
   there.

Steps 2 to 4 are cheap and answer most cases. Step 5 is for the questions they
cannot answer — a decision, a preference, anything where the code shows what is
possible but not what is wanted.

**Silence in these files is not permission.** It usually means the case has not
come up yet — see [What belongs in here](#what-belongs-in-here) for why the set
is deliberately small. If the gap keeps recurring, propose a rule for it.

This holds for humans too, but it is written for AI assistants, which are the
ones that fill a gap with a plausible-looking guess instead of leaving it open.

## Guidelines

| File                                               | Topics                                                                     |
|----------------------------------------------------|----------------------------------------------------------------------------|
| [typo3/](typo3/README.md)                          | TYPO3 topic root — index and version model                                 |
| [typo3/integrator.md](typo3/integrator.md)         | TypoScript, SiteSets, CE wizard, backend configuration                     |
| [typo3/developer.md](typo3/developer.md)           | PHP, TCA, Doctrine DBAL, views                                              |
| [typo3/content-blocks.md](typo3/content-blocks.md) | Content Block structure, portable assets, two-layer CSS, config.yaml       |
| [typo3/sitekit.md](typo3/sitekit.md)               | SiteKit layer model, template path abstraction (SiteKit projects only)     |
| [typo3/practices/](typo3/practices/README.md)      | decision guides: which approach, and when deliberately not                 |
| [typo3/versions.md](typo3/versions.md)             | which rule applies to which TYPO3 version                                  |
| [typo3/changelog-index/](typo3/changelog-index/)   | every core changelog entry — grep only, never read whole                   |
| [fluid/](fluid/README.md)                          | Fluid engine: syntax, ViewHelper arguments, template resolution            |
| [fluid/typo3.md](fluid/typo3.md)                   | Fluid in TYPO3: core ViewHelpers, backend modules, RTE output              |
| [xliff/](xliff/README.md)                          | XLIFF 1.2 / 2.0 file format, attributes, ICU message format                |
| [xliff/keys.md](xliff/keys.md)                     | Key naming conventions, key lifecycle                                      |
| [xliff/typo3.md](xliff/typo3.md)                   | LLL references, SiteSet labels.xlf, enum label localization                |
| [php.md](php.md)                                   | Naming conventions, PHPStan, PHP CS Fixer, type safety                     |
| [testing.md](testing.md)                           | Quality checks, execution order, PHPUnit, Playwright                       |
| [git.md](git.md)                                   | Branching workflow, commit messages, release process                       |
| [shell.md](shell.md)                               | Bash 3.2 vs 5.x, set -u array guards, running scripts via ddev exec        |
| [scss.md](scss.md)                                 | Bootstrap-first, CUBE CSS, prefix system, custom properties, state classes |
| [javascript.md](javascript.md)                     | data-js hooks, Bootstrap JS, ID conventions, framework choice              |
| [vue.md](vue.md)                                   | Component syntax, script setup, state management, when to use Vue          |
| [playwright.md](playwright.md)                     | Playwright test patterns, visual regression, functional tests, helpers     |
| [documentation.md](documentation.md)               | README.md and CHANGELOG.md structure for Packagist extensions              |

Each file starts with YAML frontmatter (`applies_to`, `typo3`, `see_also`). The
`applies_to` globs say which files a guideline governs; the table above is
derived from that metadata.

## Own tooling

Packages that check rules automatically, and the `**Tooling:**` line that points
at them from a rule: [tooling.md](tooling.md). The rules never depend on a tool
being present.

## What belongs in here

These files are **not** a TYPO3 manual. A rule earns its place only when both
hold:

1. the mistake actually happened — in this project or another one, by a human or
   by an AI assistant; and
2. the correct rule is not derivable from the surrounding project code.

Everything else stays out. The reason is cost: every rule here is read on every
task in its area, so an unnecessary rule is paid for repeatedly and dilutes the
ones that matter.

Version facts that do not meet this bar belong in
[typo3/changelog-index/](typo3/changelog-index/) — searched on demand, free
until then.

**Expiry:** the end of a version's support removes **instructions**, not
**warnings**. A rule explaining how to do something in a version nobody runs any
more can go — the changelog index keeps it at no cost. A warning about a pattern
that was removed stays as long as the wrong pattern is still being produced:
support ends on a schedule, training data does not. `StandaloneView` is the
example — gone since v14, and still the first thing a model reaches for.

## How a rule is backed — the `**Basis:**` line

A rule traced through the core source and a rule taken from one project's
upgrade read the same on the page, and a reader applies both with the same
confidence. The `**Basis:**` line tells them apart. It sits directly under a
section's heading, next to `**Validity:**` and `**Tooling:**`:

```markdown
### `addPlugin()` takes two arguments

**Validity:** v14 · [#107047](…)
**Basis:** verified against TYPO3 14.3.7
```

Three levels, strongest first:

| Level | Meaning | Written as |
|---|---|---|
| **verified** | traced in the source, or reproduced | `verified against TYPO3 14.3.7` — always with the package and the exact version checked |
| **documented** | backed by a changelog entry or official documentation, not traced further | `documented` — the entry is linked in the section |
| **observed** | seen in a project, neither traced nor documented | `observed` |

There is no level for an assumption. What is only assumed does not go in — see
[When a rule is missing](#when-a-rule-is-missing).

**One level per section, the weakest that applies.** A statement that is weaker
than the rest of its section carries the level inline, at its start, so that a
single `grep` finds both forms:

```markdown
**Basis: observed** — Rector moves the icon to `Icons.php` and leaves that line
behind.
```

**What the level changes for the reader.** Verified and documented rules are
applied as written. An observed rule is applied too — it describes a mistake
that did happen — but where the code at hand contradicts it, the code wins, and
the contradiction is reported so the rule can be corrected.

**What it covers.** Statements of fact: what an API does, what breaks, what an
error says. A decision — use this set, prefer that approach — is not verified or
observed; it is a decision, and its section states the reason instead.

**Adoption.** Every new section carries the line. An existing section gets it
when it is next changed; until then it is *unclassified*, which says nothing
about its quality. `verified against` with a version is what makes a later
re-check possible: after a core update, the sections verified against an older
release are the list to go through.

```bash
grep -rnE 'Basis:(\*\*)? observed' guidelines/                # to verify
grep -rn 'Basis:\*\* verified against TYPO3 13' guidelines/     # to re-check
```

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

Applies to **project source trees**, not to documentation repositories. This
repository and other documentation repos use lowercase file names, following
GitHub convention — `readme.md`, `guidelines/typo3/integrator.md`. The rule
below governs the code you write, not the docs you write about it.

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
