# Oliver Thiele — Developer Guidelines

Project-independent coding guidelines for all PHP/TYPO3 projects.
Intended for use by developers and as context for AI-assisted development.

## Core Principle

Always prefer minimal, targeted changes.

- Do not refactor existing structures unless explicitly required
- Do not rename variables, methods, or files without necessity
- Preserve existing comments and architecture — and keep a comment true when
  the code it describes changes, see [Comments](#comments--where-knowledge-belongs)
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

   When the code cannot answer it — what a TypoScript property or a TCA option
   does, how a concept is meant to work — read the official documentation on
   docs.typo3.org, and read it the way that site publishes it for tools:
   - **The project's version in the address** — `14.3`, `13.4` — for how
     something works. The next major's documentation answers a different
     question, whether it is still the way to do it — see
     [New code looks one major ahead](#new-code-looks-one-major-ahead). `main`
     documents an unreleased major and is a provisional preview only
   - **Markdown, not HTML** — the same address with `.md` instead of `.html`:
     the complete page without navigation, at a fraction of the size. A manual
     not rendered since the change answers 404; only then fall back to the HTML
   - **Find the page through the manual's indexes** instead of guessing a path:
     its `llms.txt` lists every page and index, `toc.json` is the table of
     contents, `confvals.json` lists every documented option with type and
     default. When the manual itself is unknown, start at
     [`docs.typo3.org/llms.txt`](https://docs.typo3.org/llms.txt)
   - **Never the reStructuredText sources** (`_sources/`). They miss whatever is
     pulled in while the manual is built: an included file, or the argument
     list of a ViewHelper, which is generated from data that lives elsewhere.
     An incomplete source does not look incomplete — the rendered Markdown is
     the finished page.
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

## New code looks one major ahead

The installed source says what works today. It does not say whether the code
written today survives the next upgrade. For **new** code, among the approaches
that work on the installed version, pick the one the next major does not break:

- **Grep the next released major** — `v14.tsv` for a v13 project — for
  `Deprecation` and `Breaking` entries on every API the new code uses. That
  release is final, so a hit is binding: code that uses a deprecated API today
  has to be touched again at the upgrade.
- **Grep the unreleased major as well** — `v15.tsv`, marked `provisional`. It
  breaks a tie between options that are otherwise equal; it is never a reason
  to rewrite working code, and never a `**Validity:**` line without that caveat.
- **A practice guide decides the recommended approach**, where one exists —
  [typo3/practices/](typo3/practices/README.md). Which way is *better* is not
  in the changelog; a deprecation only says which way is ending.
- **Read the next major's documentation for the direction** — `14.3` for a
  v13 project, as Markdown like any other page. It shows how the core expects
  the thing to be done once the project is upgraded.
- **The code must still run on the installed version.** Never write against an
  API that the project's `vendor/` does not have. When the forward-safe API only
  exists in the next major, use the installed one and leave a comment that names
  the changelog entry, with its title, so the upgrade finds it.

Existing code is not rewritten for this. It is updated when it is touched for
another reason, or at the upgrade itself.

## Guidelines

Which file covers which work area is listed once, in the
[routing table in `AGENTS.md`](../AGENTS.md#routing). It is not repeated here,
so that a new file cannot be added to one list and missed in another.

Each file starts with YAML frontmatter (`applies_to`, `typo3`, `see_also`). The
`applies_to` globs say which files a guideline governs.

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

## Comments — where knowledge belongs

A comment is the weakest place to keep knowledge: it goes stale and nothing
fails. Put each piece of knowledge in the first place that fits:

| Knowledge | Where it goes |
|---|---|
| What the code does | **Names** — variable, method, an extracted method, an enum instead of a magic value |
| What must hold | **Types and tests** — they fail when it stops being true |
| Why this change was made, what was there before | **The commit message** |
| Why the code has to stay this way | **A comment** |
| A decision that spans several files | The project's `Guidelines/` or `Documentation/` folder |
| What an editor needs to know | **The backend** — see [xliff/typo3.md → Texts for editors and visitors](xliff/typo3.md#texts-for-editors-and-visitors) |

**The test for every new comment: is it still true and still useful once the
change is merged?** If not, it belongs in the commit message, or nowhere.

What passes the test: a constraint the code cannot express — an order that must
not be tidied up, see [php.md](php.md) —, a workaround with a link to the
upstream issue, framework behaviour that surprises, a pointer to a changelog
entry the next upgrade has to find.

What does not:

- A comment that says what the next line does
- A change log inside the code: "now uses X instead of Y", "fixed: …"
- A reference to the task or the conversation: "as requested", "per the new
  rule"
- A docblock that repeats the declared types
- Section banners and commented-out code

Existing comments stay — see [Core Principle](#core-principle). Remove one only
after asking. When the code a comment describes changes, update the comment in
the same change, or propose removing it; a stale comment is worse than none.

The reason is cost: every comment is read on every visit to the file, and the
ones that only describe the diff bury the few that explain a constraint.

### No comments in files a tool rewrites

**Basis:** verified against TYPO3 14.3.7 (`typo3/cms-core`)

TYPO3 writes some files from an array. A comment in them disappears the next
time someone saves in the backend, and nobody notices:

- `config/system/settings.php` — `ConfigurationManager::writeLocalConfiguration()`
  rewrites it with `ArrayUtility::arrayExport()`, keys sorted, whenever the
  Install Tool or an extension configuration is saved
- `config/sites/*/config.yaml` and `settings.yaml` — `SiteWriter` rewrites them
  with `Yaml::dump()` when the site or its settings are saved in the backend

The same holds for every generated file: `phpstan-baseline.neon`, lock files,
translation files that come back from a translation service.

The reason for a value in these files goes into the commit message. If it has to
stay next to the configuration, the value moves to `config/system/additional.php`
and the comment goes with it — the core includes that file, and nothing in the
core calls `writeAdditionalConfiguration()`, the method that could overwrite it.

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
