# Oliver Thiele — Developer Guidelines

Personal coding guidelines for PHP/TYPO3 projects.

Published primarily for developers who collaborate with me on projects — the
rules
here reflect how I structure, name, and maintain code across all my work.

---

## Contents

### `guidelines/`

Technology- and topic-specific coding guidelines that apply to **all projects**.

| File                                                          | Topics                                                                  |
|---------------------------------------------------------------|-------------------------------------------------------------------------|
| [xliff.md](guidelines/xliff.md)                               | XLIFF 1.2 / 2.0 file format, attributes, source/translation conventions |
| [typo3-developer.md](guidelines/typo3-developer.md)           | TCA, Doctrine DBAL, Fluid — universal + links to version files          |
| [typo3-integrator.md](guidelines/typo3-integrator.md)         | TypoScript, translations — universal + links to version files           |
| [typo3/v13/developer.md](guidelines/typo3/v13/developer.md)   | v13-specific: Fluid 4 argument types                                    |
| [typo3/v13/integrator.md](guidelines/typo3/v13/integrator.md) | v13-specific: SiteSets, labels.xlf key naming                           |
| [typo3/v14/developer.md](guidelines/typo3/v14/developer.md)   | v14-specific: Fluid 5 union types, FlexForm DS, TCA shortform           |
| [php.md](guidelines/php.md)                                   | Naming conventions, PHPStan, PHP CS Fixer, type safety                  |
| [testing.md](guidelines/testing.md)                           | Quality checks, execution order, PHPUnit, Playwright                    |
| [git.md](guidelines/git.md)                                   | Branching workflow, commit messages, release process                    |
| [scss.md](guidelines/scss.md)                                 | Bootstrap-first, prefix system, custom properties, state classes        |
| [javascript.md](guidelines/javascript.md)                     | data-js hooks, Bootstrap JS, ID conventions, framework choice           |
| [vue.md](guidelines/vue.md)                                   | Component syntax, script setup, state management, when to use Vue       |
| [playwright.md](guidelines/playwright.md)                     | Playwright test patterns, visual regression, functional tests, helpers  |
| [documentation.md](guidelines/documentation.md)               | README.md and CHANGELOG.md structure for Packagist extensions           |

See [guidelines/README.md](guidelines/README.md) for shared rules that cut
across
all files (naming, formatting, tooling).

### `sitekit/`

Architecture conventions specific to **SiteKit-based TYPO3 extensions** only.
These rules do not apply to generic TYPO3 projects.

| File                                     | Topics                                                            |
|------------------------------------------|-------------------------------------------------------------------|
| [sitekit/sitekit.md](sitekit/sitekit.md) | Layer model, template path abstraction, content element rendering |

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
