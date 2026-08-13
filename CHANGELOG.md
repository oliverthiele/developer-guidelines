# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] — 2026-08-13

### Added

- `guidelines/README.md` — "Project-specific guidelines": rules that hold for a
  single project live in a `Guidelines/` folder in that project's root and are
  evaluated before the shared files; on conflict the project file wins. Shared
  rules are never copied into a project, and the repository is never vendored
  into one (no submodule) so that a single `git pull` updates every project
- `guidelines/README.md` — "Setting up a project": three-step onboarding with
  copy-paste blocks for the project's `CLAUDE.md` and for a committed
  `.claude/settings.json` granting read access to the shared guidelines
- `scss.md` — a project may define a short CSS prefix scheme
  (`my_productfinder` → `mp-`) instead of the extension-key default, provided the
  assignment is documented per extension in that project's `Guidelines/` and
  applied consistently
- `scss.md` — table of reserved prefixes that must never be assigned to an
  extension: `bs-`, `sk-`, `cb-`/`--cb-`, `is-`/`has-`, `tx-`. `sk-` is reserved
  in every project, not only in SiteKit projects
- `git.md` — "No customer data in public repositories": public repositories must
  never contain customer names, project names, domains, real extension keys or
  server data, examples included; use neutral placeholders

### Changed

- Replaced the extension-key examples in `scss.md` and `typo3-integrator.md` with
  neutral placeholders

### Fixed

- `php.md` — `code-quality` example now defines all three referenced scripts and
  states that unresolved `@`-references abort the chain; corrected "Both must
  pass" to "All three must pass"
- `typo3-developer.md` — added the v14 row to the version-specific file table
- `typo3-integrator.md` — noted that no v14 integrator file exists yet and how to
  read the v13 one in a v14 project; moved the `xliff.md` pointer to the end of
  the translation section
- `typo3/v13/developer.md`, `typo3/v13/integrator.md`, `typo3/v14/developer.md` —
  corrected the non-existent `docs/guidelines/` path in the header line
- `git.md` — the Co-Authored-By ban now applies to all repositories, matching the
  GitKraken instructions further down the file
- `README.md`, `guidelines/README.md` — aligned the XLIFF and SCSS topic
  descriptions with the actual file contents

## [1.0.0] — 2026-07-31

First tagged release of the guideline set.

### Added

- `guidelines/typo3/content-blocks.md` — Content Block conventions: directory
  structure, two-layer CSS architecture with the portable fallback pattern,
  asset loading via `cb:assetPath()`, `config.yaml` and `SiteKit.yaml`
  conventions, per-block README structure
- `git.md` — first push on a new repository: push `main` before `develop` so
  GitHub picks the correct default branch
- `javascript.md` — TypeScript vs. plain JavaScript decision rule, including a
  minimal esbuild + `tsc --noEmit` reference setup
- `scss.md` — when to introduce actual Sass compilation for standalone
  extensions
- `typo3-developer.md` — ExtensionScanner false positives caused by
  property/method naming; rule against guessing the current TYPO3 minor version
- `typo3-integrator.md` — frontend framework folder structure for SiteKit-based
  and standalone extensions; `f:translate` `extensionName` must be
  UpperCamelCase
- `typo3/v13/integrator.md` — `@import` instead of the deprecated
  `<INCLUDE_TYPOSCRIPT:`; New Content Element wizard auto-registration via TCA
  and wizard group selection
- `typo3/v14/developer.md` — `record-transformation` applied by default
  including automatic IRRE relation resolving; Fluid 5 `.fluid.html` file
  resolution

### Changed

- `typo3/v14/developer.md` — replaced the "Extension Title missing" section with
  the actual v14 behavior: the extension title is derived from the
  `composer.json` description, split on the first ` - `

### Fixed

- Added `guidelines/typo3/content-blocks.md` to the file index in both
  `README.md` and `guidelines/README.md`, and refreshed the outdated topic
  descriptions for the version-specific files
- Removed cross-references to sections that do not exist and corrected the claim
  that `templateRootPaths` can override shipped `Resources/Public` assets — it
  resolves Fluid templates only
- Added missing final newlines in `guidelines/php.md`,
  `guidelines/typo3-integrator.md` and `sitekit/sitekit.md` as required by
  `.editorconfig`