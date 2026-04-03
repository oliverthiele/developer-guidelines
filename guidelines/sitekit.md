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

- switch frontend framework
- avoid hardcoded paths
- enable global replacement

---

## Layer responsibilities

0–10 TYPO3 Core → fallback  
11–59 Extensions → reusable components  
60 SiteKit Base → Bootstrap integration  
70 Themes → visual layer  
80 Sitepackage → project overrides

---

## Rules

- Never modify TYPO3 core templates
- Always override via correct layer
- Keep responsibilities separated

---

## Anti-patterns

- overriding core templates directly
- hardcoded template paths
- mixing layers in one extension
