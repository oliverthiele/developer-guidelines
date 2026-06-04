# Documentation Guidelines

Standards for README.md and CHANGELOG.md in TYPO3 extensions published on
Packagist.

---

## README.md

### Title

```markdown
# Extension Name — Short description
```

- Use the human-readable package name, not the extension key
- No `EXT:` prefix, no underscores
- One concise description after the em dash

```markdown
# OT Gallery — TYPO3 Gallery Extension ✓

# EXT:ot_gallery — TYPO3 Gallery Extension ✗  (EXT: prefix, underscore key)

# ot_gallery — TYPO3 Gallery Extension ✗  (underscore key)
```

### Intro sentence

One or two sentences directly below the title — no heading, no blank section.
State the core value: what the extension does and why it is useful.

```markdown
# OT Hero Image — TYPO3 Extension

Full-width hero image content element for TYPO3 v13 and v14, optimised for Core
Web Vitals.
```

### Badges

Always use dynamic Packagist badges. Place them directly after the intro
sentence,
before `---`.

```markdown
[![TYPO3](https://img.shields.io/badge/TYPO3-13.4-orange.svg)](https://typo3.org/)
[![Packagist Version](https://img.shields.io/packagist/v/{vendor}/{package}.svg)](https://packagist.org/packages/{vendor}/{package})
[![PHP](https://img.shields.io/packagist/dependency-v/{vendor}/{package}/php.svg)](https://php.net/)
[![License](https://img.shields.io/packagist/l/{vendor}/{package}.svg)](LICENSE)
[![Changelog](https://img.shields.io/badge/Changelog-CHANGELOG.md-blue.svg)](CHANGELOG.md)
```

Replace `{vendor}` and `{package}` with the Packagist values (e.g.
`oliverthiele`
/ `ot-gallery`).

The TYPO3 badge version must match `composer.json`. For multi-version support,
use
the lowest supported version: `TYPO3-13.4` for `^13.4 | ^14`.

Static badges (hardcoded version numbers) are not allowed for published
packages.

### Separators

Place `---` after the badge block and between all top-level sections:

```markdown
[![...](...)](#)

---

## Features
```

### Optional "Why" section

Add a `## Why {Extension Name}?` section only when the extension solves a
problem
that existing solutions handle poorly — explain the concrete limitation and how
this
extension addresses it. Omit for straightforward content elements.

### Section order

Sections must appear in this order. Optional sections are marked *(optional)*.

| Section                | Heading                     | Notes                                                  |
|------------------------|-----------------------------|--------------------------------------------------------|
| Why                    | `## Why {Name}?`            | Optional — only for opinionated architectural choices  |
| Features               | `## Features`               | Bullet list with bold labels                           |
| Requirements           | `## Requirements`           | Table — see below                                      |
| Installation           | `## Installation`           | `composer require` + `extension:setup`                 |
| Configuration          | `## Configuration`          | Optional — numbered sub-steps                          |
| Usage                  | `## Usage`                  | Optional — code examples                               |
| CLI                    | `## CLI`                    | Optional — only if the extension provides CLI commands |
| Template Customization | `## Template Customization` | Optional — override paths and variables                |
| License                | `## License`                | See format below                                       |
| Author                 | `## Author`                 | See format below                                       |

Do not add sections not in this list without a clear reason.
Do not merge License and Author into one section.

### Features section

Each feature on its own bullet line — bold label followed by a short
explanation:

```markdown
## Features

- **Responsive images** — `<img srcset>` with WebP, calculated from container
  widths
- **Server-side pagination** — cached, SEO-friendly URLs via Route Enhancer
- **SiteSet configuration** — no manual TypoScript includes required
```

### Requirements section

Always a table. Columns: `Requirement` and `Version`.
List TYPO3 and PHP first, then other packages.

```markdown
## Requirements

| Requirement | Version          |
|-------------|------------------|
| TYPO3       | ^13.4 \| ^14.3   |
| PHP         | >=8.3            |
| Bootstrap   | 5.x              |
```

Use `^x.y \| ^z.w` for multi-version ranges — match the `composer.json`
constraint
exactly.

### Installation section

Always start with `composer require`, then optionally the TYPO3 setup command:

````markdown
## Installation

```bash
composer require oliverthiele/ot-gallery
```

Then run the TYPO3 setup:

```bash
vendor/bin/typo3 extension:setup -e ot_gallery
# or via DDEV:
ddev typo3 extension:setup -e ot_gallery
```
````

### License section

```markdown
## License

GPL-2.0-or-later — see [LICENSE](LICENSE)
```

Never inline the copyright year or author name in the License section.

### Author section

```markdown
## Author

Oliver Thiele — [oliver-thiele.de](https://www.oliver-thiele.de)
```

---

## What does NOT belong in README.md

- Changelog entries — use `CHANGELOG.md`
- German translation (`README.de.md`) — GitHub only renders `README.md`
- Emoji in headings
- Internal project notes or WIP remarks
- Planned features (unless they materially affect the integration decision
  today)

---

## CHANGELOG.md

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) + Semantic
Versioning.

### File header

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```

### Entry structure

```markdown
## [1.2.0] — 2025-06-15

### Added

- Server-side pagination via Route Enhancer

### Changed

- Minimum PHP version raised to 8.3

### Fixed

- Missing alt text on lightbox images

### Removed

- Deprecated `Gallery\LegacyProcessor` class
```

Rules:

- Only include subsections (`### Added`, `### Changed`, etc.) that have entries
- Use imperative phrasing — "Add X", not "Added X" or "Adds X"
- One entry per change — do not combine unrelated changes
- Reference issue or PR numbers at the end when applicable: `(#42)`

### Version numbers

| Change type                     | Increment               |
|---------------------------------|-------------------------|
| Backward-compatible new feature | Minor (`1.1.0 → 1.2.0`) |
| Backward-compatible bug fix     | Patch (`1.2.0 → 1.2.1`) |
| Breaking change                 | Major (`1.2.1 → 2.0.0`) |

Breaking changes must appear under `### Removed` or `### Changed` with a
migration
note.
