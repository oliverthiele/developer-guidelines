# Oliver Thiele — Developer Guidelines

Project-independent coding guidelines for all PHP/TYPO3 projects.
Intended for use by developers and as context for AI-assisted development.

## Core Principle

Always prefer minimal, targeted changes.

- Do not refactor existing structures unless explicitly required
- Do not rename variables, methods, or files without necessity
- Preserve existing comments and architecture
- Extend instead of rewriting

## How to use

Each guideline file covers one technology or topic area.

- Load only the relevant guideline file(s) for the current task
- Follow rules strictly — do not reinterpret them
- Prefer existing project patterns over introducing new ones

## Guidelines

| File                                               | Topics                                                                                 |
|----------------------------------------------------|----------------------------------------------------------------------------------------|
| [xliff.md](xliff.md)                               | XLIFF 1.2 file format, attributes, source/translation conventions                      |
| [typo3-developer.md](typo3-developer.md)           | TCA, Doctrine DBAL, Fluid — universal + links to version files                         |
| [typo3-integrator.md](typo3-integrator.md)         | TypoScript, translations — universal + links to version files                          |
| [typo3/v13/developer.md](typo3/v13/developer.md)   | v13-specific: Fluid 4 argument types                                                   |
| [typo3/v13/integrator.md](typo3/v13/integrator.md) | v13-specific: SiteSets, labels.xlf key naming                                          |
| [typo3/v14/developer.md](typo3/v14/developer.md)   | v14-specific: Fluid 5 union types, FlexForm DS, TCA shortform, Extension Title warning |
| [php.md](php.md)                                   | Naming conventions, PHPStan, PHP CS Fixer, type safety                                 |
| [testing.md](testing.md)                           | Quality checks, execution order, PHPUnit, Playwright                                   |
| [git.md](git.md)                                   | Branching workflow, commit messages, release process                                   |
| [scss.md](scss.md)                                 | CUBE CSS, prefix system, custom properties, state classes                              |
| [javascript.md](javascript.md)                     | data-js hooks, Bootstrap JS, ID conventions, framework choice                          |
| [vue.md](vue.md)                                   | Component syntax, script setup, state management, when to use Vue                      |

## General rules (apply everywhere)

- Code comments and documentation: **English only**
- Communication with Oliver: **German**
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
