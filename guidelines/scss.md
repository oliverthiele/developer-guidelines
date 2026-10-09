---
title: SCSS and CSS
scope: frontend
applies_to:
  - "**/*.scss"
  - "**/*.css"
see_also: ["javascript.md", "typo3/content-blocks.md", "third-party-code.md", "bootstrap.md"]
---
# SCSS / CSS Guidelines

CSS and SCSS conventions for all projects.

## Architecture philosophy

We use a **pragmatic CUBE CSS approach** on top of Bootstrap 5:

- **Atomic Design** for component organisation (Atom → Molecule → Organism → Template → Page)
- **CUBE CSS thinking** for CSS structure (Composition / Utility / Block / Exception)
- **Bootstrap 5** as the layout, utility and base-component foundation
- **No BEM** — Bootstrap already provides a consistent class grammar; adding BEM on top creates a second, competing
  system
- Do not introduce a second naming system alongside Bootstrap

## Responsibility and Separation of Concerns

SCSS is responsible for **styling only**.

- CSS classes define layout and visual appearance — never behaviour
- CSS classes must not be used as JavaScript selectors
- CSS must not depend on `data-js` attributes
- JavaScript must not depend on CSS class names

`data-js` is the contract between JavaScript and HTML — SCSS never reads it.

For JavaScript conventions and DOM interaction rules, see → `javascript.md`

## Formatting

Formatting is defined in `.editorconfig`.

Fallback:

- indent_style: space
- indent_size: 4
- charset: utf-8
- end_of_line: lf
- insert_final_newline: true
- trim_trailing_whitespace: true

## Sass compilation — when to actually use it

Default to plain, hand-written CSS with custom properties (see below) — it
needs no build step and matches the portable, dependency-free asset
convention used across this ecosystem's standalone extensions.

Only introduce actual Sass compilation (`.scss` source → compiled `.css`) for
a standalone extension when it **already** has a Node-based build step for
other reasons — typically because its JavaScript is TypeScript (see
`javascript.md`). In that case, name the source file `.scss` even if its
content is currently plain CSS syntax, so the extension is clear it needs
compiling, and compile it via the same build script:

```
Resources/Private/Scss/CountUp.scss   — source (may be plain CSS syntax)
Resources/Public/Css/CountUp.min.css  — compiled + minified, committed
```

```javascript
// build.mjs — compile with `sass`, then minify with esbuild
import { build } from 'esbuild';
import { compile } from 'sass';

const compiledCss = compile('Resources/Private/Scss/CountUp.scss').css;

await build({
  stdin: { contents: compiledCss, loader: 'css', resolveDir: '.' },
  outfile: 'Resources/Public/Css/CountUp.min.css',
  minify: true,
});
```

Do not rename a `.css` file to `.scss` without also wiring up a real Sass
compile step — esbuild alone does not understand Sass-specific syntax
(`@use`, nesting, variables), only plain CSS.

---

## Third-party styles and shipped SCSS

Styles taken from a library keep their license notice as a `/*! */` header;
`//` comments do not survive compilation. Whatever the build tool, check that
the notice arrives in the built CSS. SCSS that an extension ships for projects
to `@use` must not use relative `url()` paths. See
[third-party-code.md](third-party-code.md).

---

## Bootstrap First

Prefer native Bootstrap utilities and components whenever they already solve the problem clearly.

Use custom SCSS only when:

- project-specific styling is required
- Bootstrap utilities would become unreadable or repetitive
- a reusable component needs its own styling API

Do not recreate Bootstrap utilities with custom classes.

Do not use `@extend` with Bootstrap utility or component classes. Bootstrap's
internal selector structure causes unpredictable CSS bloat and broken output when
extended. Use HTML composition or Bootstrap mixins (`@include`) instead:

```scss
// Wrong — @extend on a Bootstrap class
.my-button {
    @extend .btn;
    @extend .btn-primary;
}

// Correct — compose in HTML, or use the Bootstrap mixin
@use 'bootstrap/scss/mixins/buttons' as *;
.my-button {
    @include button-variant(…);
}
```

## IDs

IDs are not used for styling.

Rules:

- Do not use IDs as CSS selectors
- IDs are reserved for JavaScript access or anchor links (see `javascript.md`)
- IDs must use `lowerCamelCase`
- Do not rely on IDs for reusable styling or layout

```html
<!-- Allowed -->
<div id="productFilterApp"></div>

<!-- Wrong -->
<div id="product-filter-app"></div>
<div id="__myId"></div>
```

## CSS class naming

All classes use `kebab-case`.

### Prefix system

CSS classes are namespaced by origin to avoid collisions and clarify ownership.

- each system or extension defines its own prefix
- the prefix acts as a namespace (similar to `bs-` in Bootstrap)
- prefixes act as stable namespaces and must not change over time

| Prefix       | Scope                              | Example                                       |
|--------------|------------------------------------|-----------------------------------------------|
| *(none)*     | Bootstrap utilities and components | `card`, `btn`, `d-flex`                       |
| `sk-`        | SiteKit base system                | `sk-stage`, `sk-breadcrumb-item`              |
| `{ext-key}-` | TYPO3 extension namespace          | `ot-gallery-figure`, `ot-heroimage-wrapper`   |
| `cb-`        | TYPO3 ContentBlock element         | `cb-price-card-header`, `cb-hero-stage-media` |

Rules:

- every TYPO3 extension must use its own prefix
- do not mix prefixes within a component
- prefixes define ownership and must remain stable
- TYPO3 extension keys use underscores (`ot_gallery`) — convert to hyphens for
  CSS prefixes (`ot-gallery-`). Never use underscores in CSS class names.

#### Deriving the prefix

The default derivation is the extension key (`ot_gallery` → `ot-gallery-`).

A project may instead define a **short prefix scheme** (`my_productfinder` → `mp-`),
for example when extension keys are long enough to dominate the class name. Two
conditions apply:

- the assignment is documented in that project's `Guidelines/` — one prefix per
  extension, listed in full
- the scheme is used consistently across the whole project

Either way the guarantee is the same: one stable, unambiguous prefix per extension.

#### Reserved prefixes — never assign to an extension

| Prefix          | Owner                                     |
|-----------------|-------------------------------------------|
| *(none)*        | Bootstrap utilities and components         |
| `bs-`           | Bootstrap internals                        |
| `sk-`           | SiteKit base system                        |
| `cb-`, `--cb-`  | TYPO3 Content Blocks                       |
| `is-`, `has-`   | state classes (see *State classes* below)  |
| `tx-`           | TYPO3-generated plugin container classes   |

`sk-` is reserved in **every** project, not only in SiteKit projects — otherwise a
project that later adopts SiteKit collides with its own classes.

Third-party libraries own their prefixes too (`fa-`, `mfp-`, `cc-`, …). Which ones
apply depends on the project; record them in the project's `Guidelines/`.

Bootstrap's component names are taken as well. An own class that starts with
one — `.accordion-product-groups`, `.card-teaser` — reads like Bootstrap and is
not. It takes the extension's prefix: `.ot-gallery-accordion`.

### Inner elements — no BEM double-underscore

Inner elements use full prefix + hyphen. No `__`.

```html
<!-- Correct -->
<figure class="ot-gallery-figure">
    <div class="ot-gallery-media">
        <img class="ot-gallery-img">
    </div>
    <figcaption class="ot-gallery-caption"></figcaption>
</figure>

<!-- Wrong — BEM double-underscore -->
<figure class="ot-gallery__figure">
    <div class="ot-gallery__media">
```

### Variants and modifiers — no BEM double-dash

Do not use BEM modifier syntax (`--`). Use these patterns instead:

```html
<!-- Correct -->

<!-- 1. Bootstrap theme -->
<nav class="sk-main-nav" data-bs-theme="dark">…</nav>

<!-- 2. CMS variant -->
<div class="cb-price-card" data-variant="featured">…</div>

<!-- 3. Structural variant -->
<div class="ot-hero-stage ot-hero-stage-fullwidth">…</div>

<!-- Wrong — BEM modifier -->
<div class="ot-hero-stage ot-hero-stage--fullwidth">…</div>
```

Rule: one mechanism per question.

| Question | Mechanism |
|---|---|
| Light or dark? | `data-bs-theme` |
| Which form of the component — `featured`, `muted`, `compact`? | `data-variant` |
| Spacing, columns, aspect ratio | an additional class |
| Which palette colour? | Bootstrap's own — see below, never an own attribute |

**`data-variant` names the role, never the colour:** `featured`, not `red` or
`primary`. A colour value rebuilds Bootstrap's palette as a second system, and
it has to be migrated in every template and every stored record once the
palette changes. The values exclude each other — an element has exactly one —
and a select field in the backend maps onto it without translation:
`data-variant="{data.variant}"`.

**The colours of an own component come from its variables**, with Bootstrap's
tokens as the fallback; a variant only sets those variables:

```scss
.cb-price-card {
    background-color: var(--cb-price-card-bg, var(--bs-body-bg));
    color: var(--cb-price-card-color, var(--bs-body-color));

    &[data-variant="featured"] {
        --cb-price-card-bg: var(--bs-primary);
        --cb-price-card-color: var(--bs-white);
    }
}
```

**Looking ahead to Bootstrap 6 (provisional):** v6 sets the palette colour with `theme-*`
classes, which define `--theme-bg`, `--theme-fg`, `--theme-border` and
`--theme-contrast` and pass them on to the children. The documentation applies
them to Bootstrap's own components; that an own component reads them as its
fallback is our conclusion from it, see [bootstrap.md](bootstrap.md). A role
value such as `featured` survives that change untouched.

**Bootstrap components keep Bootstrap's variant classes** — `btn-dark`,
`btn-outline-secondary`, `alert-warning` in Bootstrap 5, `btn-solid theme-primary`,
`alert theme-warning` in Bootstrap 6. They are the variant of a Bootstrap
component — not a BEM modifier, and not replaced by `data-variant`.
`data-variant` is for components we build ourselves.

The `data-variant` attribute is matched in SCSS with an attribute selector on the
component class:

```scss
.cb-price-card {
    // base styles

    &[data-variant="featured"] {
        // featured variant styles
    }
}
```

## State classes

States that are **set by JavaScript** and **styled by CSS** use the `is-` or `has-` prefix.

- CSS only reacts to these classes
- JavaScript adds or removes them
- CSS never sets them itself
- State classes must never define base styling
- State classes must only override existing component styles

```html

<div class="sk-accordion" data-js="accordion">
    <div class="sk-accordion-panel is-open"></div>
    <nav class="sk-main-nav has-submenu"></nav>
</div>
```

```scss
.sk-accordion-panel {
  display: none;

  &.is-open {
    display: block;
  }
}
```

Rules:

- state classes must always modify a component
- never use standalone state classes

### Which of two options is the prominent one

A control that shows a state — a tab, a switch, a filter, a toggle — renders
the **selected** option with the full colour as its ground, and the option you
could switch to as an outline in the same colour. Never the other way round: a
page where one control reads one way and the next the other way cannot be read
at all. The colour says *what* an option is; only the fill changes with the
state.

Two links side by side are not a state. If clicking the quiet one navigates,
this rule does not apply; if it changes what the current view shows, it does.

### Anti-patterns

```scss
/* Wrong — standalone state */
.is-open {
  display: block;
}

/* Wrong — CSS controlling state */
.sk-accordion-panel {
  display: block;
}
```

## Nesting

Keep nesting shallow.

Rules:

- prefer flat selectors
- avoid deep nesting
- maximum 2 levels unless necessary
- do not mirror full HTML structure
- prefer composition over nesting

### Anti-patterns

```scss
/* Wrong — mirrors HTML structure */
.page {
  .container {
    .row {
      .col {
        .card {
```

## Selector Strategy

- use classes as primary selectors
- selectors must not depend on DOM structure
- avoid IDs for styling
- never use IDs as primary selectors
- avoid element-only selectors
- avoid deep descendant selectors

### Anti-patterns

```scss
/* Wrong — ID selector */
#mainNavigation {
}

/* Wrong — deep selector */
.page .container .row .card .title {
}
```

## CSS custom properties

Two levels — global design tokens and component-local variables — use different prefixes
so their scope is always obvious.

### Global tokens — `--sk-*`

Global tokens must always be defined in the global `:root` scope.

```scss
:root {
    --sk-color-primary: #0066cc;
    --sk-spacing-4: 1rem;
}
```

### Component variables — `--{ext-key}-*`

```scss
.ot-gallery {
  --ot-gallery-ratio: 4 / 3;
}
```

Component variables must be defined on the component root element to ensure proper scoping.

Rules:

- shared values → global tokens
- component-specific → local variables
- promote reused values to global tokens

### Anti-patterns

```css
/* Wrong — component variable defined globally */
:root {
    --ot-gallery-ratio: 4 / 3;
}

/* Wrong — global variable inside component */
.ot-gallery {
    --sk-color-primary: red;
}

/* Wrong — duplicated values */
.ot-gallery {
    color: #0066cc;
}
```

## TYPO3-specific anti-patterns

### Never use content element UIDs as selectors

TYPO3 assigns a database UID to every content element (`#c113`, `#c64`, etc.).
These IDs change when an element is deleted and recreated, migrated to another
environment, or imported from a different database. CSS targeting a UID is broken
by design.

```scss
/* Wrong — UID is a database primary key, not a stable CSS hook */
#c113.frame-layout-1 {
    background-color: #fff;
}

#c64.frame-layout-0 {
    background-color: $green-old;
}
```

If a content element needs unique styling, add a CSS class via the TYPO3 backend
field "Additional CSS class" (`tx_contentblock_css_class`, `space_before_class`,
or the "Appearance" tab) and target that class instead.

### Never override Bootstrap component classes with `!important`

`!important` in component overrides is a sign of a specificity battle. The root
cause is always a selector that is too specific or in the wrong place — fix the
architecture, not the symptom.

```scss
/* Wrong — !important to win a specificity war */
#c64 .btn-primary {
    background-color: #000 !important;
    border-color: #000 !important;
    color: #fff !important;

    &:hover {
        background-color: #000 !important;
    }
}

/* Correct, for the whole site — the theme colour, set BEFORE importing
   Bootstrap. Overrides placed after the import have no effect. */
$primary: #000;

/* Correct, for one area — the component's CSS variables, see below */
.ot-section-dark .btn-primary {
    --bs-btn-bg: #000;
    --bs-btn-border-color: #000;
    --bs-btn-hover-bg: #333;
}
```

Bootstrap 5 has no `$btn-primary-bg` — the button variants are generated from
`$theme-colors`. A variable that Bootstrap does not read changes nothing and
raises no error.

### Never use deep structural selectors tied to framework internals

Selectors that chain TYPO3 or Bootstrap class names to reach an element break
whenever the framework changes its markup or the template is refactored.

```scss
/* Wrong — 6-level structural selector */
.frame-type-form_formframework form .actions .form-navigation .btn.btn-primary {
    background-color: #000;
}

/* Correct — add a semantic class to the element and target that */
.ot-form-submit {
    background-color: var(--sk-color-primary);
}
```

### Never hardcode magic values — use custom properties

Hardcoded color hex values and pixel sizes scattered across selectors cannot be
maintained. A single brand color change requires hunting through hundreds of
lines.

```scss
/* Wrong — magic values hardcoded in every selector */
#c64 {
    background-color: #2d6a4f;
    padding: 30px;

    h2 { font-size: 24px; line-height: 36px; }
    p  { font-size: 16px; line-height: 24px; }
}

/* Correct — values defined once as custom properties */
:root {
    --sk-color-brand: #2d6a4f;
    --sk-spacing-section: 1.875rem;
}

.ot-section-highlight {
    background-color: var(--sk-color-brand);
    padding: var(--sk-spacing-section);
}
```

---

## Bootstrap components — set their variables, not their properties

**Basis:** verified against Bootstrap 5.3.8

A Bootstrap 5.3 component reads its colours from CSS variables in every state.
`.btn` sets `background-color: var(--bs-btn-hover-bg)` in `:hover` and
`var(--bs-btn-disabled-bg)` in `:disabled`, both with a more specific selector
than `.btn-primary`. A raw property therefore reaches the resting state only:

```scss
/* Wrong — hover, focus and disabled keep the variant's colour */
.btn-primary {
    background-color: var(--sk-color-brand);
}

/* Correct — every state Bootstrap defines reads it */
.btn-primary {
    --bs-btn-bg: var(--sk-color-brand);
    --bs-btn-border-color: var(--sk-color-brand);
}
```

The same holds for `--bs-alert-*`, `--bs-table-*`, `--bs-card-*` and the other
components. Own rules state only the difference; a rule that repeats what
Bootstrap already sets is a copy that drifts. Bootstrap 6 derives every state
from the `--theme-*` tokens, so a raw property misses even more there — see
[bootstrap.md](bootstrap.md).

**Sass variables and CSS variables do different jobs.** `$primary` is resolved
at compile time and applies everywhere. `--bs-btn-bg` is resolved at runtime,
inherits, and can be set for one area of the page. A change for the whole site
is a Sass variable before the import; a change for one area is a CSS variable.

## Colour modes

**Basis:** verified against Bootstrap 5.3.8 — `[data-bs-theme="dark"]` sets
`color-scheme: dark` and redefines the `--bs-*` palette for its subtree; the
light block sets no `color-scheme`

Write every rule so that it can follow a switch to dark mode, also before the
switch exists. Everything that reads `--bs-*` variables flips by itself;
everything that carries a literal colour stays light.

- **No literal colour in a component rule** — not `#fff`, not
  `rgba(0, 0, 0, .06)`. A colour is a token; the rule reads `var(…)`.
- **Bootstrap's semantic variables first:** `--bs-body-bg`, `--bs-body-color`,
  `--bs-border-color`, `--bs-secondary-bg`, `--bs-tertiary-bg`,
  `--bs-emphasis-color`. They already change with the mode.
- **An own token carries both values and is declared once**, with
  `light-dark()`. The browser resolves it against the `color-scheme` of the
  element that uses it, so one declaration on `:root` serves every subtree:

  ```scss
  :root {
      --sk-color-surface: light-dark(#fff, #1a1a1a);
  }

  // Bootstrap 5.3 sets no color-scheme for light — without this line a light
  // subtree inside a dark page resolves to the dark value
  [data-bs-theme="light"] {
      color-scheme: light;
  }
  ```

  This is how Bootstrap 6 defines its own tokens, so the token survives the
  upgrade unchanged — see [bootstrap.md](bootstrap.md).
- **Where the project's browser support rules out `light-dark()`**, declare the
  token twice, in the same commit: under `:root` and under
  `[data-bs-theme="dark"]`. A token that exists in only one of them breaks the
  day the switch is built.
- **A transparent colour is mixed, not built from `-rgb`:**
  `color-mix(in oklab, var(--bs-primary), transparent 50%)` instead of
  `rgba(var(--bs-primary-rgb), .5)`. It works with a `light-dark()` token, and
  Bootstrap 6 removes the `-rgb` variables — see [bootstrap.md](bootstrap.md).
- **Check both modes before calling it done.** In the browser console:
  `document.documentElement.dataset.bsTheme = 'dark'`.

## Type sizes — Bootstrap's scale

**Basis:** verified against Bootstrap 5.3.8

A font size comes from a class of Bootstrap's scale. No `font-size` in `rem` or
`px` in a component rule — also not when a design mock-up names one.

- **Heading level and size are separate.** The element follows the document
  outline, the class sets the size: `<h3 class="card-title h5">`. `.h1`–`.h6`
  stay in Bootstrap 6.
- **When a step of the scale is wrong, change the step**, not one element. An
  override on a single element is how a size stops being adjustable from one
  place.
- **Before changing a step, measure.** It reaches every element at that level —
  templates, XLIFF labels and content stored in the database alike.

In Bootstrap 5:

- The scale is `.h1`–`.h6`, `.fs-1`–`.fs-6`, `.small`, `.lead`, `.display-*`;
  a step is changed with `$h5-font-size` and its siblings before the import.
- With `$enable-rfs` (on by default) Bootstrap shrinks every size above
  `$rfs-base-value` (1.25rem) on small screens. A `font-size` in a component
  rule switches that off for the element.

Bootstrap 6 drops RFS for `clamp()`, renames the utilities to
`.fs-xs`–`.fs-6xl` and removes `.lead` and `.display-*` — see
[bootstrap.md](bootstrap.md).

---

## Quick reference

| What                   | Convention                        | Example                   |
|------------------------|-----------------------------------|---------------------------|
| ID                     | `lowerCamelCase`                  | `productFilterApp`        |
| CSS class              | `kebab-case`                      | `ot-gallery-figure`       |
| SiteKit class          | `sk-{element}`                    | `sk-stage-media`          |
| Extension class        | `{ext-key}-{component}-{element}` | `ot-gallery-caption`      |
| ContentBlock class     | `cb-{blockname}-{element}`        | `cb-price-card-header`    |
| State class            | `is-{state}`, `has-{state}`       | `is-open`, `has-image`    |
| Global CSS variable    | `--sk-{category}-{name}`          | `--sk-color-primary`      |
| Component CSS variable | `--{ext-key}-{name}`              | `--ot-gallery-ratio`      |
| CMS variant            | `data-variant="{value}"`          | `data-variant="featured"` |
| Theme variant          | `data-bs-theme="{value}"`         | `data-bs-theme="dark"`    |
