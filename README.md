# Oliver Thiele — Developer Guidelines

Personal coding guidelines for PHP/TYPO3 projects.

Published primarily for developers who collaborate with me on projects — the
rules
here reflect how I structure, name, and maintain code across all my work.

---

## Contents

### `guidelines/`

Technology- and topic-specific coding guidelines that apply to **all projects**.

| File                                                              | Topics                                                                     |
|-------------------------------------------------------------------|----------------------------------------------------------------------------|
| [typo3/](guidelines/typo3/README.md)                              | TYPO3 topic root — index and version model                                 |
| [typo3/integrator.md](guidelines/typo3/integrator.md)             | TypoScript, SiteSets, CE wizard, backend configuration                     |
| [typo3/developer.md](guidelines/typo3/developer.md)               | PHP, TCA, Fluid, Doctrine DBAL, views                                      |
| [typo3/content-blocks.md](guidelines/typo3/content-blocks.md)     | Content Block structure, portable assets, two-layer CSS, config.yaml       |
| [typo3/sitekit.md](guidelines/typo3/sitekit.md)                   | SiteKit layer model, template path abstraction (SiteKit projects only)     |
| [typo3/versions.md](guidelines/typo3/versions.md)                 | which rule applies to which TYPO3 version                                  |
| [typo3/changelog-index/](guidelines/typo3/changelog-index/)       | every core changelog entry — grep only, never read whole                   |
| [xliff/](guidelines/xliff/README.md)                              | XLIFF 1.2 / 2.0 file format, attributes, ICU message format                |
| [xliff/keys.md](guidelines/xliff/keys.md)                         | Key naming conventions, key lifecycle                                      |
| [xliff/typo3.md](guidelines/xliff/typo3.md)                       | LLL references, SiteSet labels.xlf, enum label localization                |
| [php.md](guidelines/php.md)                                       | Naming conventions, PHPStan, PHP CS Fixer, type safety                     |
| [testing.md](guidelines/testing.md)                               | Quality checks, execution order, PHPUnit, Playwright                       |
| [git.md](guidelines/git.md)                                       | Branching workflow, commit messages, release process                       |
| [scss.md](guidelines/scss.md)                                     | Bootstrap-first, CUBE CSS, prefix system, custom properties, state classes |
| [javascript.md](guidelines/javascript.md)                         | data-js hooks, Bootstrap JS, ID conventions, framework choice              |
| [vue.md](guidelines/vue.md)                                       | Component syntax, script setup, state management, when to use Vue          |
| [playwright.md](guidelines/playwright.md)                         | Playwright test patterns, visual regression, functional tests, helpers     |
| [documentation.md](guidelines/documentation.md)                   | README.md and CHANGELOG.md structure for Packagist extensions              |

See [guidelines/README.md](guidelines/README.md) for shared rules that cut
across
all files (naming, formatting, tooling).

Changes between releases are documented in [CHANGELOG.md](CHANGELOG.md).

### `skills/`

Claude Code skills that work with these guidelines. They live in this
repository because they depend on its structure and must stay in sync with it.

| File                                                        | Topics                                                            |
|-------------------------------------------------------------|-------------------------------------------------------------------|
| [typo3-changelog-harvest](skills/typo3-changelog-harvest/SKILL.md) | Build and query the TYPO3 changelog index |

See [skills/README.md](skills/README.md) for installation.

---

## How to use

**As a developer working with me:**
Load the relevant guideline file(s) for the area you are working in and follow
the
rules as written. When in doubt, prefer the existing project pattern over
introducing
a new one.

**As an AI assistant:**
Load only the files relevant to the current task. Follow rules strictly — do not
reinterpret or override them based on general conventions. The guidelines take
precedence over defaults.

---

## License

These guidelines are published for reference and collaboration. Feel free to
adapt
them for your own projects.
