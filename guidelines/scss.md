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

Rule: use an additional class for structural/layout variants, and `data-variant`
or `data-bs-theme` for visual/thematic variants (colours, themes):

- Layout changes (spacing, columns, aspect ratio) → additional class
- Visual changes (colour scheme, theme, brand) → `data-variant` or `data-bs-theme`

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

/* Correct — define Bootstrap variable overrides in your global variables file
   BEFORE importing Bootstrap. Overrides placed after the import have no effect. */
$btn-primary-bg: #000;
$btn-primary-border-color: #000;
$btn-primary-color: #fff;
```

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
