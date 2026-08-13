---
title: JavaScript
scope: frontend
applies_to:
  - "**/*.js"
  - "**/*.ts"
see_also: ["scss.md", "vue.md"]
---
# JavaScript Guidelines

JavaScript conventions for all projects.

For styling and CSS class conventions, see → `scss.md`
For Vue-specific conventions, see → `vue.md`

---

## Responsibility and Separation of Concerns

JavaScript is responsible for **behaviour only**.

- CSS classes define styling — JavaScript must never select by CSS class
- `data-js` is the contract between JavaScript and HTML
- CSS must never depend on `data-js` attributes
- JavaScript must never depend on CSS class names

This strict separation means: renaming a CSS class never breaks JS, and
removing a `data-js` attribute never affects styling.

---

## Formatting

Formatting is defined in `.editorconfig`.

Fallback:

- indent_style: space
- indent_size: 2
- charset: utf-8
- end_of_line: lf
- insert_final_newline: true
- trim_trailing_whitespace: true

### Quotes

- Single Quotes als Standard für Strings
- Template Literals (`` ` ``) für Interpolation oder mehrzeilige Strings
- Double Quotes nur, wenn der String selbst ein `'` enthält (Vermeidung von Escaping)

```javascript
const label = 'Menu öffnen'              // korrekt
const message = `Hallo ${userName}`      // korrekt – Interpolation
const html = "<div class='card'>"        // korrekt – vermeidet Escaping

const label = "Menu öffnen"              // falsch – Double Quotes ohne Grund
```

### Semicolons

- Semicolons sind Pflicht am Ende jeder Anweisung
- Grund: vermeidet ASI-Fallstricke (Automatic Semicolon Insertion), v. a. bei Zeilen, die mit `(`, `[` oder `` ` `` beginnen

```javascript
const menuToggle = document.querySelector('[data-js="menuToggle"]');

async function loadData(url) {
    const response = await fetch(url);
    return response.json();
}
```

---

## Variable Declarations

- Always use `const` — default for all declarations
- Use `let` only when reassignment is required
- Never use `var`

```javascript
const menuToggle = document.querySelector('[data-js="menuToggle"]')  // default

let counter = 0        // only when reassignment follows
counter++

var label = 'old'      // Wrong — never use var
```

---

## Asynchronous Code

Prefer `async/await` over raw Promise chains or `.then()`:

```javascript
// Correct
async function loadData(url) {
    const response = await fetch(url)
    return response.json()
}

// Wrong
fetch(url).then(r => r.json()).then(data => { …
})
```

---

## Naming Conventions

### IDs

- Use `lowerCamelCase`
- IDs are not the default JavaScript hook — use `data-js` instead
- Allowed only for:
    - App roots (Vue)
    - Anchor links
    - External integrations that require an ID

Rule: if an ID is used in JavaScript, the variable name must match the ID value.

```html

<div id="productFilterApp"></div>
```

```javascript
const productFilterApp = document.getElementById('productFilterApp')
```

---

### JavaScript hooks — `data-js`

JavaScript always selects elements via `data-js`, never via CSS classes or IDs.

- Value: `lowerCamelCase`
- Value must match the JavaScript variable name — a single IDE search finds both

Exception for Vue components: inside Vue templates, do not use `data-js`
attributes or
`document.querySelector`. Use Vue template refs (`ref="elementName"`) or event
bindings
(`@click`) instead.

```html
<!-- Correct -->
<button class="sk-nav-toggle" data-js="menuToggle">

    <!-- Wrong — CSS class used as JS hook -->
    <button class="sk-nav-toggle js-menu-toggle">
```

```javascript
// Correct — same string as in the template
const menuToggle = document.querySelector('[data-js="menuToggle"]')

// Wrong — CSS class selector
document.querySelector('.sk-nav-toggle')
```

---

### Vue component names

- `PascalCase` for component names and file names
- See `vue.md` for all Vue-specific conventions

---

## Selector Strategy

| Priority | Selector             | When                                                 |
|----------|----------------------|------------------------------------------------------|
| 1        | `data-js`            | default for all JS interactions                      |
| 2        | ID                   | only when justified (Vue root, anchor, external lib) |
| 3        | CSS class            | never                                                |
| 4        | Structural selectors | never                                                |

```javascript
// Wrong — structural selector
document.querySelector('.container .row .card button')
```

---

## Framework Choice

### Vanilla JavaScript

Default for all interactions. Use when:

- the interaction is isolated (toggle, scroll handler, modal trigger)
- no shared state is required
- a library like Bootstrap JS already handles it

### Vue

Use when the UI is stateful and complex enough that Vanilla JS becomes hard to
maintain.
Vue is always a **conscious decision** — see `vue.md` for criteria and
conventions.

---

## TypeScript vs. Plain JavaScript

Default to plain JavaScript. Use TypeScript only for a standalone TYPO3
extension's own frontend logic when that logic is non-trivial (animations,
observers, calculations — not a one-off toggle), **and** the extension already
has (or is getting) its own Node-based build step to produce the shipped
`Resources/Public` assets.

Do not introduce TypeScript just because it "seems cleaner" for a trivial
script, and do not introduce a build step purely to enable TypeScript — the
build step must already be justified by the extension needing pre-minified,
dependency-free `Resources/Public` assets for standalone distribution.

When adopted, signal intent through the file extension and matching folder:

```
Resources/Private/JavaScript/CountUp.ts   — source, type-checked
Resources/Public/JavaScript/CountUp.min.js — compiled + minified, committed
```

Minimal reference setup (esbuild transpiles `.ts` directly; `tsc --noEmit` is
used only for type-checking, not compilation):

```json
// package.json (devDependencies)
{
  "esbuild": "^0.25.0",
  "typescript": "^5.7.0"
}
```

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noEmit": true,
    "skipLibCheck": true
  },
  "include": ["Resources/Private/JavaScript/**/*.ts"]
}
```

```javascript
// build.mjs
import { build } from 'esbuild';

await build({
  entryPoints: ['Resources/Private/JavaScript/CountUp.ts'],
  outfile: 'Resources/Public/JavaScript/CountUp.min.js',
  minify: true,
  format: 'iife',
  target: 'es2020',
});
```

Add an npm script `"typecheck": "tsc --noEmit"` and run it before building —
esbuild silently strips types without checking them.

Do **not** move the TypeScript source itself out of the extension package
(e.g. into a consuming project's own `Build/Default`) — the compiled
`Resources/Public` assets must ship with the package either way for it to
work standalone in other projects, so keeping the source out of the package
only removes the ability for other consumers to read or adapt it, without
actually making the package smaller. A consuming project can still replace the
shipped assets as an optional customisation layer on top — by not including the
extension's own asset TypoScript and registering its own bundle instead, or by
pointing the corresponding TypoScript constant at a different file. Note that
`templateRootPaths` does **not** apply here: it resolves Fluid templates, not
`Resources/Public` assets.

---

## Initialization

- Initialize only after DOM is ready
- Guard for missing elements before initializing

```javascript
ready(function () {
    initPopovers()
    initVideoPlayer()
})
```

```javascript
const element = document.querySelector('[data-js="something"]')
if (!element) return
```

---

## Event Handling

- Use `addEventListener`
- No inline handlers
- Do not bind events to unstable selectors

```javascript
menuToggle?.addEventListener('click', () => {
    // logic
})
```

---

## Multiple Elements

```javascript
document.querySelectorAll('[data-js="accordionPanel"]').forEach((panel) => {
    // logic
})
```

---

## Bootstrap JavaScript — `data-bs-*`

Use Bootstrap's native attributes — do not reimplement with `data-js`:

```html

<button data-bs-toggle="modal" data-bs-target="#confirmDialog">
```

---

## Vue App Roots

- Use a dedicated root element with an `lowerCamelCase` ID
- Pass data via `data-*` attributes (rendered via Fluid in TYPO3)
- One root element per app instance

```html

<div id="productFilterApp" data-settings="..." data-items="...">
</div>
```

See `vue.md` for mounting and component conventions.

---

## Entry Points

- One entry point per large feature
- Do not load large scripts globally
- File names: `PascalCase`

```
Build/Default/EntryPoints/ProductFilterApp.js
```

---

## TYPO3 Asset Integration

Register assets explicitly in Fluid — load only where needed:

```html

<f:asset.script identifier="product-filter-app"
                src="EXT:ot_febuild/.../ProductFilterApp.js"/>
```

- Pair JS + CSS per feature
- Use consistent identifiers in `f:asset.*`

---

## Server-to-Client Data

- Provide data via `data-*` attributes
- Avoid global variables
- Prefer JSON-encoded data for complex structures

---

## Anti-patterns

```javascript
// Wrong — CSS class as JS hook
document.querySelector('.sk-nav-toggle')

// Wrong — ID used as generic JS hook
document.getElementById('button')
```

```html
<!-- Wrong — inline handler -->
<button onclick="toggleMenu()">
```

- Do not load feature-specific scripts globally
- Do not use Vue for simple one-off interactions

---

## Quick Reference

| What              | Convention                     | Example                  |
|-------------------|--------------------------------|--------------------------|
| ID                | `lowerCamelCase`               | `id="productFilterApp"`  |
| JS hook           | `data-js="lowerCamelCase"`     | `data-js="menuToggle"`   |
| Selector priority | `data-js` → ID → (never class) |                          |
| JS variable       | matches `data-js` value        | `const menuToggle = ...` |
| Bootstrap JS      | `data-bs-*`                    | `data-bs-toggle="modal"` |
| Vue component     | `PascalCase`                   | `<ProductFilterApp />`   |
| Entry point file  | `PascalCase`                   | `ProductFilterApp.js`    |
| App root ID       | `lowerCamelCase`               | `productFilterApp`       |
