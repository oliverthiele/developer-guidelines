# AGENTS.md

Entry point for AI coding assistants working in a repository that uses these
guidelines. Contains no rules of its own — it says which file to read, and in
what order.

Every path in this file is relative to the root of the `developer-guidelines`
repository — usually cloned next to the project as `../developer-guidelines/`,
see [`guidelines/setup.md`](guidelines/setup.md). A file that imports this one
from elsewhere resolves the paths against that root, not against the project.

## Read order

1. **The project's `Guidelines/README.md`**, if the project has one. Project
   rules are evaluated first and win on conflict.
2. **The [routing table](#routing) below** — it maps a work area to the one
   file that covers it.
3. **The file that table names for the current task** — one per work area the
   task actually touches. A task that changes extension PHP and its Playwright
   tests reads those two; it does not read the rest.

[`guidelines/README.md`](guidelines/README.md) holds the rules that cut across
every file — what to do when a rule is missing, how a rule is backed. Read it
when its sections are pointed at, not on every task.

Do not load the whole repository. Each guideline file is self-contained and
names its related files in its `see_also` frontmatter — follow those when the
file itself points at them, not preemptively.

## Routing

**Read the file for a work area before starting work in it** — also when the
task looks small or the rule seems obvious, and never from memory.

| Work area | Read this file first |
|---|---|
| TYPO3 — where to start, version model | [`guidelines/typo3/README.md`](guidelines/typo3/README.md) |
| TYPO3 integration: TypoScript, SiteSets, CE wizard, backend configuration | [`guidelines/typo3/integrator.md`](guidelines/typo3/integrator.md) |
| TYPO3 extension PHP: TCA, Doctrine DBAL, services, commands, views, extension metadata | [`guidelines/typo3/developer.md`](guidelines/typo3/developer.md) |
| TYPO3 Content Blocks: structure, portable assets, two-layer CSS, `config.yaml` | [`guidelines/typo3/content-blocks.md`](guidelines/typo3/content-blocks.md) |
| SiteKit-based projects: layer model, template path abstraction | [`guidelines/typo3/sitekit.md`](guidelines/typo3/sitekit.md) |
| Architecture decision: which approach, and when deliberately not (component or partial, ViewHelper or DataProcessor) | [`guidelines/typo3/practices/README.md`](guidelines/typo3/practices/README.md) |
| TYPO3 version questions: does this still hold in v13, v14? | [`guidelines/typo3/versions.md`](guidelines/typo3/versions.md) |
| A changelog number or a removed/deprecated API, from the ExtensionScanner, PHPStan or memory | [`guidelines/typo3/changelog-index/`](guidelines/typo3/changelog-index/) — grep only, see below |
| Fluid: syntax, ViewHelper arguments, template resolution, Fluid Standalone | [`guidelines/fluid/README.md`](guidelines/fluid/README.md) |
| Fluid inside TYPO3: core ViewHelpers, backend modules, RTE output | [`guidelines/fluid/typo3.md`](guidelines/fluid/typo3.md) |
| XLIFF / XLF files: format, attributes, ICU message format | [`guidelines/xliff/README.md`](guidelines/xliff/README.md) |
| XLIFF key naming and key lifecycle | [`guidelines/xliff/keys.md`](guidelines/xliff/keys.md) |
| XLIFF in TYPO3: LLL references, SiteSet `labels.xlf`, enum labels | [`guidelines/xliff/typo3.md`](guidelines/xliff/typo3.md) |
| PHP in general: naming, PHPStan, PHP CS Fixer, type safety | [`guidelines/php.md`](guidelines/php.md) |
| SCSS / CSS: Bootstrap first, prefix system, custom properties, state classes | [`guidelines/scss.md`](guidelines/scss.md) |
| JavaScript / TypeScript: `data-js` hooks, Bootstrap JS, framework choice | [`guidelines/javascript.md`](guidelines/javascript.md) |
| Vue / Vite | [`guidelines/vue.md`](guidelines/vue.md) |
| Vendored third-party code, license comments, minifier settings, shipped SCSS | [`guidelines/third-party-code.md`](guidelines/third-party-code.md) |
| Testing: quality checks, execution order, PHPUnit | [`guidelines/testing.md`](guidelines/testing.md) |
| Playwright E2E tests: patterns, visual regression, helpers | [`guidelines/playwright.md`](guidelines/playwright.md) |
| Git: branching, commit messages, pull requests, releases | [`guidelines/git.md`](guidelines/git.md) |
| Shell and bash scripts: Bash 3.2 vs 5.x, `ddev exec`, host or container, remote login shell, long-running jobs | [`guidelines/shell.md`](guidelines/shell.md) |
| Documentation: README and CHANGELOG | [`guidelines/documentation.md`](guidelines/documentation.md) |

A new guideline file gets its row here and nowhere else — every other list of
the guideline files points at this table instead of copying it.

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
In short: establish which TYPO3 version the project runs — for a reusable
extension, also the range its `composer.json` supports — grep
[`guidelines/typo3/changelog-index/`](guidelines/typo3/changelog-index/) for
version questions, and read the installed source in the project's `vendor/` for
how an API is meant to be used — a changelog says what changed, the code says
what it is. Where the code cannot answer, read docs.typo3.org at the project's
version, as Markdown (`.md` instead of `.html`), never the reStructuredText
sources. Only then ask, and never answer from memory.

New code also looks one major ahead: grep the next released major's index for
deprecations of every API it uses (binding), the unreleased one as a
tie-breaker, and let a practice guide decide the recommended approach — while
the code still runs on the installed version. Full rule:
[`guidelines/README.md` → New code looks one major ahead](guidelines/README.md#new-code-looks-one-major-ahead).

**Grep those files, never read one whole.** They hold every core changelog entry
since v13 — about 900 lines and 390 KB across three files, most of it symbol
lists, and growing with every core release. `v14.tsv` alone is 195 KB: reading
it loads about two thirds of the text of every guideline file in this repository
combined, to answer a question a single `grep` answers exactly.

```bash
grep -h 'StandaloneView' guidelines/typo3/changelog-index/v1*.tsv
```

Columns, how far to trust each one, and how to open the full entry:
[`skills/typo3-changelog-harvest/SKILL.md`](skills/typo3-changelog-harvest/SKILL.md).

## Editing

Never change a file under `guidelines/` without explicit confirmation. Rules
that hold for one project only belong in that project's `Guidelines/` folder,
never here.

## Other assistants

Tools with their own entry file — `CLAUDE.md`, `.cursor/rules`, Copilot
instructions — should point at this file rather than restate it. A copied rule
drifts from the original; a pointer cannot.
