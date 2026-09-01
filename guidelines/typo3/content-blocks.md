---
title: TYPO3 Content Blocks
scope: typo3
applies_to:
  - "**/ContentBlocks/**"
typo3: ["13", "14"]
see_also: ["typo3/integrator.md", "fluid/typo3.md", "xliff/typo3.md", "scss.md"]
---
# TYPO3 Content Blocks Guidelines

Conventions for creating portable, reusable TYPO3 Content Blocks.

For general CSS conventions, see → `scss.md`.
For XLIFF conventions, see → `../xliff/README.md` and `../xliff/keys.md`.
For JavaScript conventions, see → `javascript.md`.

---

## Directory structure

```
ContentBlocks/ContentElements/{Name}/
├── config.yaml              # Content Block definition
├── SiteKit.yaml             # SiteKit groups and grid config
├── README.md                # Documents CSS variables, JS behavior, usage notes
├── templates/
│   └── frontend.html        # Fluid template (loads assets via f:asset + cb:assetPath)
├── assets/
│   ├── frontend.css         # Portable default styles (CSS Custom Properties)
│   └── frontend.js          # Portable JS (only if element needs interactivity)
└── language/
    ├── labels.xlf           # English source
    └── de.labels.xlf        # German translation
```

- `{Name}` uses PascalCase (e.g., `TechBadges`, `CardIconHeaderText`)
- The `assets/` folder is the **portability layer** — TYPO3 auto-publishes it via symlink
- Copying the entire CB directory to another TYPO3 installation provides working default styles

---

## Two-layer CSS architecture

Content Block styling is split into two layers:

### Layer 1: Portable defaults (`assets/frontend.css`)

Ships with the Content Block. Works out of the box with Bootstrap 5. No build step required.

Rules:

- **Pure CSS only** — no SCSS, no build dependencies
- **Fallback pattern** — use `var()` with inline fallbacks, never define variables on the root element:

```css
/* Correct — fallback pattern */
.cb-tech-badges-list {
    gap: var(--cb-tech-badges-list-gap, 1rem);
    border-color: var(--cb-tech-badges-border-color, var(--bs-border-color));
}

/* Wrong — variable definition on root (loading order breaks overrides) */
.cb-tech-badges {
    --cb-tech-badges-list-gap: 1rem;
}
```

- The fallback pattern ensures project overrides always win, regardless of CSS loading order
- `f:asset.css` may load after the Build CSS — defining variables on the root would override the project's values
- Use Bootstrap `--bs-*` variables as fallback values where possible
- No project-specific values (design tokens, brand colors) in portable CSS
- Follow the prefix and naming conventions from `scss.md`

### Layer 2: Project overrides (Build system)

Optional. Located at `Build/Default/src/scss/ContentBlocks/_{Name}.scss`.

- **SCSS** — has access to project variables, mixins, Bootstrap SCSS
- Import in `Main.scss` under the "Content Blocks" section
- Sets CSS Custom Properties that override the portable fallbacks:

```scss
.cb-tech-badges {
    --cb-tech-badges-list-gap: var(--space-4);
    --cb-tech-badges-border-color: var(--color-border-default);
}
```

- When a variable is set, it takes precedence over the fallback value in Layer 1
- Can also add entirely new styles, responsive adjustments, or project-specific behaviors

### SCSS interpolation in custom properties

SCSS does not evaluate functions or variables inside CSS Custom Property values.
Always use `#{}` interpolation:

```scss
/* Correct — interpolated */
.cb-card-icon {
    --cb-card-icon-badge-bg: #{rgba($orange-500, 0.12)};
    --cb-card-icon-badge-color: #{$orange-500};
}

/* Wrong — SCSS variable passed raw, outputs literal "$orange-500" in CSS */
.cb-card-icon {
    --cb-card-icon-badge-bg: rgba($orange-500, 0.12);
}
```

This applies to all SCSS variables and functions (`rgba()`, `darken()`, `lighten()`, etc.) used inside `--custom-property:` declarations.

---

## Asset loading in Fluid templates

Load CSS/JS from the `assets/` folder via the `cb:assetPath()` ViewHelper:

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:cb="http://typo3.org/ns/TYPO3/CMS/ContentBlocks/ViewHelpers"
      data-namespace-typo3-fluid="true">
<f:asset.css identifier="cb-{kebab-case-name}" href="{cb:assetPath()}/frontend.css" />
<f:asset.script identifier="cb-{kebab-case-name}" src="{cb:assetPath()}/frontend.js" />
```

Rules:

- Always add `xmlns:cb` namespace when using `cb:assetPath()`
- CSS identifier: `cb-{kebab-case-name}` (e.g., `cb-tech-badges`)
- Only include `f:asset.script` if the CB has a `frontend.js`

---

## JavaScript — two layers

### Layer 1: Portable logic (`assets/frontend.js`)

- Only create if the element needs interactivity
- Vanilla JS — no build dependencies, no imports, no framework dependencies
- Selection: always `data-js="camelCaseName"`, never CSS classes or IDs
- State: `is-*` / `has-*` classes, added/removed by JS
- Use `DOMContentLoaded` or check for element existence before initializing

### Layer 2: Project entry point (Build system)

Optional. Located at `Build/Default/EntryPoints/{Name}.js`.

- For JS that imports libraries (e.g., Swiper, GSAP)
- Loaded conditionally (only when the element is on the page)
- Can enhance or replace the portable JS

---

## README.md per Content Block

Every Content Block must include a README.md. Structure:

```markdown
# {Name}

One sentence describing what the element does.

## CSS Custom Properties

| Variable | Default | Description |
|---|---|---|
| `--cb-{name}-gap` | `1rem` | Gap between items |
| `--cb-{name}-border-color` | `var(--bs-border-color)` | Item border color |

## JavaScript

Describe interactive behavior, `data-js` attributes used, and state classes set.
If no JS: "This element has no JavaScript dependencies."

## Usage notes

Any special requirements, known limitations, or tips for integrators.
```

- Focus on what's configurable (variables) and what's special (behavior)
- This is a quick reference for someone copying the CB to another project

---

## config.yaml conventions

```yaml
name: {vendor}/{kebab-case-name}    # e.g., oliverthiele/tech-badges
prefixFields: false                  # Always false — use existing fields
basics:
  - TYPO3/Appearance
  - TYPO3/Links                      # Only if link fields are used
fields:
  - identifier: header
    useExistingField: true
```

Rules:

- `name:` uses vendor from `composer.json` + kebab-case element name
- `prefixFields: false` — always, to use existing TYPO3 fields directly
- Prefer `useExistingField: true` for standard fields (header, bodytext, header_link, subheader, icon_identifier, assets, image)
- Custom field identifiers: `snake_case`, descriptive, not abbreviated
- Collection field identifiers: `cb_{blockname}_{purpose}` (e.g., `cb_techbadges_items`)
- Never hardcode labels in config.yaml — use XLIFF files instead

---

## SiteKit.yaml conventions

```yaml
groups: [group_content_small, group_content_wide]
grid: { minCols: 2, requiresFullWidth: false }
```

- `minCols`: minimum columns this element should span (2, 3, 4, 6, 12)
- `requiresFullWidth`: true only for hero-level elements

---

## Fluid template conventions

- Namespace: `xmlns:f`, `xmlns:i` (ot-icons), `xmlns:cb` (content-blocks) — only what's used
- CSS class prefix: `cb-{kebab-case-name}-` (e.g., `cb-tech-badges-item`)
- No BEM (`__`, `--`), use flat prefix-hyphen naming
- Anchor: `<span class="anchor" id="c{data.uid}"></span>` when element has margin
- Icons: `<i:icon identifier="{data.icon_identifier}" aria-hidden="true" />` — no hardcoded `iconStyle`
- State classes: `is-*` / `has-*` pattern, set by JS
- All text content via `{data.fieldname}` — bodytext via `{data.bodytext -> f:format.html()}`
- Header hierarchy: use `f:switch` on `{data.header_layout}` for configurable heading levels

---

## XLIFF labels

Content Blocks resolve labels automatically from `language/labels.xlf` inside the CB directory. Always create XLIFF files.

- `title` and `description` keys define the element name and wizard description
- Field labels: `{fieldIdentifier}.label` and `{fieldIdentifier}.description`
- Collection child fields: `{collectionIdentifier}.{childFieldIdentifier}.label`
- Remove all `title:` and `label:` strings from config.yaml after creating the XLIFF files
- See → `../xliff/README.md` for format rules

---

## Common mistakes

- Don't hardcode `iconStyle="solid"` — let SiteSet default handle it
- Don't use `prefixFields: true` when using existing fields
- Don't create custom fields for things that already exist
- Don't add inline styles — always use CSS/SCSS
- Don't skip `assets/frontend.css` — every CB needs portable default styles
- Don't write SCSS in `assets/` — only plain CSS
- Don't forget the README.md
- Don't put project-specific values in `assets/frontend.css`
- Don't forget `#{}` interpolation for SCSS variables in custom properties
- Don't define CSS Custom Properties on the root element in `assets/frontend.css` — use the fallback pattern

---

## Quick reference

| What                     | Convention                                          | Example                                  |
|--------------------------|-----------------------------------------------------|------------------------------------------|
| Directory name           | PascalCase                                          | `TechBadges`                             |
| config.yaml name         | `{vendor}/{kebab-case}`                             | `oliverthiele/tech-badges`               |
| CSS class prefix         | `cb-{kebab-case-name}-`                             | `cb-tech-badges-item`                    |
| CSS variable prefix      | `--cb-{kebab-case-name}-`                           | `--cb-tech-badges-gap`                   |
| Collection identifier    | `cb_{blockname}_{purpose}`                          | `cb_techbadges_items`                    |
| Portable CSS             | `assets/frontend.css`                               | Fallback pattern, pure CSS               |
| Project override SCSS    | `Build/Default/src/scss/ContentBlocks/_{Name}.scss` | Variable overrides, project styles       |
| Asset loading            | `f:asset.css` + `cb:assetPath()`                    | `href="{cb:assetPath()}/frontend.css"`   |
| f:asset.css identifier   | `cb-{kebab-case-name}`                              | `cb-tech-badges`                         |
