# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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