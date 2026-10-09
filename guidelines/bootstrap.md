---
title: Bootstrap versions
scope: frontend
applies_to: []
bootstrap: ["5", "6"]
see_also: ["scss.md", "javascript.md"]
---

# Bootstrap versions

Which of our rules change between Bootstrap 5 and 6, and where to look up the
rest. This is not a copy of the migration guide — that is one page, kept by
Bootstrap, and readable by tools. Only the changes that touch a rule in these
files are listed.

## Status

**Basis:** documented — read on 2026-10-09 from the v6 documentation

Bootstrap 6 is at **6.0.0-alpha.1**. Everything below is **provisional**: an
alpha can still change names and behaviour, and an entry here is re-checked
before it is relied on.

Projects run Bootstrap 5.3. Treat v6 the way [README.md → New code looks one
major ahead](README.md#new-code-looks-one-major-ahead) treats an unreleased
TYPO3 major: it breaks a tie between two ways that both work on 5.3, it is never
a reason to rewrite working code, and no v6 syntax goes into a v5 project.

## Where to look it up

- **Migration guide:** <https://getbootstrap.com/docs/6.0/guides/migration/> —
  every breaking change, old name → new name
- **Index for tools:** <https://getbootstrap.com/llms.txt> — every page of the
  v6 documentation, one line each
- **The installed version decides.** Read `node_modules/bootstrap/scss/` of the
  project before writing against a variable or a class — as with TYPO3, the
  installed source is the version that actually runs

## Changes that touch our rules

### Colour modes — one token, both values

v6 defines every token once on `:root` with `light-dark()`, and `:root` carries
`color-scheme: light dark`, so the visitor's system setting applies without
JavaScript. `data-bs-theme="dark|light"` stays the switch; it sets
`color-scheme` for its subtree. `$enable-dark-mode` is removed — dark mode is
always compiled.

**What it means now:** own tokens are written with `light-dark()` already on 5.3
— see [scss.md → Colour modes](scss.md#colour-modes). They then need no change at
the upgrade.

### Component variants — `theme-*` classes

| Bootstrap 5 | Bootstrap 6 |
|---|---|
| `btn btn-primary` | `btn-solid theme-primary` |
| `btn btn-outline-primary` | `btn-outline theme-primary` |
| `alert alert-primary` | `alert theme-primary` |
| `badge bg-primary` | `badge theme-primary` |
| `text-bg-primary` | `bg-primary fg-contrast-primary` |

A `theme-*` class is inherited by the children of the element it sits on;
`.theme-reset` stops that for a subtree.

**What it means now:** nothing changes in a 5.3 project. The rule that Bootstrap
components keep Bootstrap's own variant classes, and `data-variant` is for our
own components, holds in both versions — see
[scss.md → Variants and modifiers](scss.md#variants-and-modifiers--no-bem-double-dash).

v6 separates the palette colour from the form of a component: `theme-*` says
which colour, `btn-solid` or `btn-outline` says which form. Our rule follows the
same split — `data-variant` names a role (`featured`), never a colour — so that
a v6 project can take the colour from `theme-*` while every stored
`data-variant` value stays valid. That an own component should read
`--theme-bg` and `--theme-fg` as its fallback is our conclusion; the v6
documentation shows the tokens only for Bootstrap's own components.

### Component variables — still the way to change a colour

v6 derives hover, active and disabled from the `--theme-*` tokens. The rule to
set a component's variables and never its properties holds even more — see
[scss.md → Bootstrap components](scss.md#bootstrap-components--set-their-variables-not-their-properties).

**Not settled in the alpha:** the custom property prefix is now added by
PostCSS, and the documentation shows both `--bs-btn-*` and `--btn-*`. Check the
built CSS before writing an override against a v6 project.

### Type sizes

- RFS is removed; the larger sizes use `clamp()`
- `.fs-1`–`.fs-6` become `.fs-xs`–`.fs-6xl` — `.fs-6` (1rem) is `.fs-md`,
  `.fs-1` (2.5rem) is `.fs-4xl`
- `.display-*` and `.lead` are removed; the guide gives `.fs-*` plus `.fw-light`
  as the replacement
- `.h1`–`.h6` stay

**What it means now:** the principle in
[scss.md → Type sizes](scss.md#type-sizes--bootstraps-scale) holds in both
versions. Every utility class name changes, so there is no 5.3 spelling that
survives — keep the scale classes, and change them at the upgrade.

### Class names Bootstrap takes over

v6 adds components and classes whose names an own class without prefix could
already be using: `menu`, `dialog`, `drawer`, `chip`, `avatar`, `stepper`,
`toggler`, `prose`, `field`, `theme-*`, `fg-*`, `bg-1`–`bg-*`.

**What it means now:** the prefix rule in
[scss.md → Prefix system](scss.md#prefix-system) is what keeps an own class from
colliding at the upgrade.

### JavaScript

- Modal → Dialog, Offcanvas → Drawer, Dropdown → Menu, each with new
  `data-bs-toggle` values (`dialog`, `drawer`, `menu`) and renamed events
  (`show.bs.dialog`)
- Collapse no longer sets `.collapsed` on its trigger — state is read from
  `aria-expanded`
- ESM only: no `window.bootstrap` global, CDN scripts need `type="module"`
- Popper.js is replaced by Floating UI (`popperConfig` → `floatingConfig`)

**What it means now:** JavaScript that reacts to Bootstrap components reads
`aria-expanded` rather than `.collapsed`, and imports Bootstrap's classes rather
than reaching for `window.bootstrap` — both already work on 5.3.

### Responsive utilities and browser support

- Responsive and state variants are written as a prefix: `.d-md-none` →
  `.md:d-none`, `.col-md-6` → `.md:col-6`
- Minimum browsers rise to Chrome/Edge 130, Firefox 132, Safari 18

Both are upgrade work, not something to prepare in a 5.3 project. The browser
minimum is a project decision before the upgrade starts.
