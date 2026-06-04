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
