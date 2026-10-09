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

**Basis:** documented — read on 2026-10-09 from the v6 documentation and the
v5 → v6 migration skill in the Bootstrap repository

Bootstrap 6 is at **6.0.0-alpha.1**. Everything below is **provisional**: an
alpha can still change names and behaviour, and an entry here is re-checked
before it is relied on.

Projects run Bootstrap 5.3. **Where 5.3 can already do what v6 does, new code
does it the v6 way** — so that the upgrade is less work, and so that own code
uses the same techniques as the components Bootstrap will ship. The list is in
[Already usable on 5.3](#already-usable-on-53). Beyond that, v6 is treated the
way [README.md → New code looks one major ahead](README.md#new-code-looks-one-major-ahead)
treats an unreleased TYPO3 major: no v6 syntax goes into a v5 project, and
working code is not rewritten for it.

## Where to look it up

- **Migration guide:** <https://getbootstrap.com/docs/6.0/guides/migration/> —
  every breaking change, old name → new name
- **Index for tools:** <https://getbootstrap.com/llms.txt> — every page of the
  v6 documentation, one line each
- **Migration skill:** `skills/bootstrap-v5-v6-migration/SKILL.md` in
  <https://github.com/twbs/bootstrap> — the guide as step-by-step instructions
  for an assistant, with before/after markup and a list of v5 patterns to search
  for. Fetch the current version when a migration starts; do not install it
  ahead of one — `npx skills add twbs/bootstrap` adds all of Bootstrap's skills,
  not only this one
- **The installed version decides.** Read `node_modules/bootstrap/scss/` of the
  project before writing against a variable or a class — as with TYPO3, the
  installed source is the version that actually runs

## Already usable on 5.3

Each of these works on Bootstrap 5.3 and is what v6 does itself. New code uses
them where the project's browser support allows; details in the sections below.

- **Own colour tokens with `light-dark()`**, declared once —
  [scss.md → Colour modes](scss.md#colour-modes)
- **`color-mix()` instead of the `-rgb` variables** for a transparent colour
- **Component variables, never properties**, to change a Bootstrap component —
  [scss.md → Bootstrap components](scss.md#bootstrap-components--set-their-variables-not-their-properties)
- **`data-variant` names a role, never a colour**, so the colour can come from
  `theme-*` later — [scss.md → Variants](scss.md#variants-and-modifiers--no-bem-double-dash)
- **Logical properties in own CSS** — `margin-inline-start`, `padding-block` —
  which v6 uses for every spacing and border utility
- **`aria-expanded` instead of `.collapsed`**, and **imports instead of
  `window.bootstrap`** in JavaScript
- **A prefix on every own class**, so no name collides with a component v6 adds

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

**The `--bs-` prefix is added by PostCSS.** In v6's Sass every token is written
without a prefix (`--btn-bg`, `--spacer`); only the dist and CDN builds run
PostCSS to make it `--bs-btn-bg`. A project that compiles Bootstrap from source
— as ours do — has unprefixed properties unless it adds that PostCSS step
itself. Check the built CSS before writing an override against a v6 project.

**Cascade layers make a raw property worse.** v6 puts its styles into `@layer`
(`colors, theme, config, root, reboot, layout, content, forms, components,
custom, helpers, utilities`). Own CSS outside any layer wins over all of them,
whatever the specificity. On 5.3 a raw `background-color` on `.btn-primary`
reaches the resting state only; on v6 it overrides every state, and the button
loses its hover. Overrides that relied on specificity or load order need a
second look at the upgrade.

Customising moves from single Sass variables to token maps: `$root-tokens` for
the global tokens, a `$*-tokens` map per component, passed with
`@use "bootstrap/scss/bootstrap" with (…)`.

### Transparent colours — `color-mix()` instead of `-rgb`

v6 removes every `$*-rgb` Sass variable and `--bs-*-rgb` custom property:

```scss
/* v5 pattern — gone in v6 */
background-color: rgba(var(--bs-primary-rgb), .5);

/* v6 — and already valid on 5.3 */
background-color: color-mix(in oklab, var(--bs-primary), transparent 50%);
```

**What it means now:** new code uses `color-mix()` where the project's browser
support allows it. It also works with a token that carries `light-dark()`,
which an `-rgb` triple cannot.

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
  `.md:d-none`, `.col-md-6` → `.md:col-6`; `xxl` becomes `2xl`
- Colour text utilities move to `fg-*`: `.text-primary` → `.fg-primary`,
  `.text-muted` → `.fg-secondary`
- Spacing and border utilities keep their names but use logical properties
- Minimum browsers rise to Chrome/Edge 130, Firefox 132, Safari 18

Both are upgrade work, not something to prepare in a 5.3 project. The browser
minimum is a project decision before the upgrade starts.
