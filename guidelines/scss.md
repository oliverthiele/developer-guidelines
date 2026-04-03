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

## Responsibility

SCSS is responsible for **styling only**.

- CSS classes define layout and visual appearance
- CSS classes must NOT be used as JavaScript selectors
- CSS must not depend on `data-js`
- JavaScript must not depend on CSS class names

This enforces a strict separation between styling and behaviour.

## Relation to JavaScript

SCSS and JavaScript follow a strict separation of concerns:

- SCSS defines **styling only**
- JavaScript defines **behaviour only**
- JavaScript uses `data-js` as its primary hook (see `javascript.md`)
- SCSS must never rely on `data-js`
- JavaScript must never rely on CSS class names

For JavaScript conventions and DOM interaction rules, see:

→ `javascript.md`

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
| Selector priority      | `data-js → ID → class`            |                           |
