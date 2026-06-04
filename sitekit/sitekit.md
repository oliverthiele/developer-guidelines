# SiteKit Guidelines

Conventions and architecture patterns for SiteKit-based TYPO3 projects.

## Scope

This file applies to:

- Projects using SiteKit extensions
- Structured content element rendering
- Template layering

Do not use these rules for:

- Non-SiteKit TYPO3 projects

---

## Core Idea

SiteKit provides:

- modular content elements
- layered template overrides
- upgrade-safe architecture

---

## Content Element Rendering

SiteKit uses layered overrides via `lib.contentElement`.

Priority order:

0   -> EXT:fluid_styled_content/Resources/Private/…
10  -> {$styles.templates.layoutRootPath} (unused)
15  -> EXT:ot_irrebuttons/Resources/Private/ContentElements/…
60  -> EXT:ot_sitekitbase/Resources/Private/ContentElements/…
70  -> optional themes
80  -> EXT:my_sitekit/Resources/Private/ContentElements/…

---

## Template Directory Abstraction

All template paths must include:

{$sitekit.frameworks.frontend.directory}/

Purpose:

- switch frontend framework without touching every extension
- avoid hardcoded paths
- enable global replacement (e.g. Bootstrap 5 → Bootstrap 6)

---

## Layer responsibilities

| Range | Owner | Purpose |
|---|---|---|
| 0–10 | TYPO3 Core | fallback templates |
| 11–59 | Extensions | reusable components (`tt_content.<CType> =< lib.contentElement`) |
| 60 | SiteKit Base | Bootstrap integration, overrides fluid_styled_content templates |
| 70 | Themes | visual layer, must be below sitepackage to allow overrides |
| 80 | Sitepackage | project-specific overrides |

---

## Rules

- Never modify TYPO3 core templates
- Always override via the correct layer
- Keep layer responsibilities separated

---

## Anti-patterns

- Overriding core templates directly
- Hardcoded template paths (use `{$sitekit.frameworks.frontend.directory}/` instead)
- Mixing layer responsibilities in one extension