# JavaScript Guidelines

JavaScript conventions for all projects.

## Relation to SCSS

JavaScript and SCSS follow a strict separation of concerns:

- CSS classes are used for styling only
- JavaScript must not depend on CSS class names
- JavaScript uses `data-js` as the primary hook for behaviour
- CSS must not depend on JavaScript hooks such as `data-js`

For styling conventions and class naming rules, see:

→ scss.md

## Responsibility

JavaScript is responsible for **behaviour only**.

- JavaScript controls behaviour and interaction
- CSS classes define styling only
- JavaScript must not depend on CSS class names
- CSS must not depend on JavaScript hooks

**Contract:**

- CSS = styling
- JS = behaviour
- data-js = contract between both

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

## Naming Conventions

### IDs

- Use `lowerCamelCase`
- IDs are not the default JavaScript hook (use `data-js` instead)
- Allowed for:
    - App roots (Vue)
    - Anchor links
    - External integrations

Rule:

- If an ID is used in JavaScript, it must match the variable name

```html

<div id="productFilterApp"></div>
```

```javascript
const productFilterApp = document.getElementById('productFilterApp');
```

---

### JavaScript hooks — `data-js`

JavaScript always selects elements via `data-js`.

Rules:

- Use `data-js` for JS hooks
- Never use CSS classes as JS selectors
- Use `lowerCamelCase`
- Value must match JS variable name
- Naming must remain stable to ensure reliable selectors

```html

<button class="sk-nav-toggle" data-js="menuToggle">
```

```javascript
const menuToggle = document.querySelector('[data-js="menuToggle"]');
```

---

### Vue component names

- Use `PascalCase` for components

```html

<ProductFilterApp></ProductFilterApp>
```

---

## Selector Strategy

Priority:

1. `data-js`
2. ID (only when justified)
3. Never CSS classes
4. Never use global or structural selectors for behaviour

```javascript
// Wrong — structural selector
document.querySelector('.container .row .card button');
```

---

## Separation of Concerns

- CSS must not depend on JS hooks
- JS must not depend on CSS classes

---

## Initialization

- Initialize only after DOM is ready
- Initialize only if the required DOM hook exists
- Use centralized init logic
- Do not initialize features globally if they are page-specific

```javascript
ready(function () {
    initPopovers();
    initVideoPlayer();
});
```

- Always guard for missing elements

```javascript
const element = document.querySelector('[data-js="something"]');
if (!element) return;
```

---

## Event Handling

- Use `addEventListener`
- No inline handlers
- Do not bind events to unstable selectors

```javascript
menuToggle?.addEventListener('click', () => {
    // logic
});
```

---

## Multiple Elements

- Use `querySelectorAll`
- Iterate explicitly

```javascript
document.querySelectorAll('[data-js="accordionPanel"]').forEach((panel) => {
    // logic
});
```

---

## Bootstrap JavaScript — `data-bs-*`

Use Bootstrap's native attributes:

```html

<button data-bs-toggle="modal" data-bs-target="#confirmDialog">
```

Do not reimplement with `data-js`.

---

## Framework Choice

### Vanilla JavaScript

- Default for small interactions

### Vue

- Use for complex, stateful UI
- Always a conscious decision

---

## Vue App Roots

- Use a dedicated root element
- ID allowed (`lowerCamelCase`)
- Pass data via `data-*`
- Only one root per app instance

```html

<div id="productFilterApp" data-json="..." data-settings="...">
```

---

## Entry Points

- Use dedicated entry points for large features
- Do not load large scripts globally
- Load entry points only on pages where the feature is used
- Use `UpperCamelCase` for filenames

Example:

```
Build/Default/EntryPoints/ProductFilterApp.js
```

---

## TYPO3 Asset Integration

Register assets explicitly in Fluid:

```html

<f:asset.script identifier="system-compare"
                src="EXT:ot_febuild/.../ProductFilterApp.js"/>
```

Rules:

- Load only where needed
- Pair JS + CSS per feature
- Use consistent identifiers in `f:asset.*`

---

## Server-to-Client Data

- Provide data via `data-*` attributes
- Avoid global variables
- Prefer JSON-encoded data for complex structures

---

## Anti-Patterns

- Using CSS classes as JS hooks
- Inline event handlers
- Global loading of feature JS
- Vue for trivial behaviour

### Examples

```javascript
// Wrong — CSS class as JS hook
document.querySelector('.sk-nav-toggle');

// Wrong — ID used as generic JS hook instead of data-js
document.getElementById('button');

// Wrong — inline handler
<button onclick="toggleMenu()">

// Wrong — global bundle for page-specific feature
// (loading SystemCompare.js on every page)

// Wrong — Vue for simple toggle
```

---

## Quick Reference

| What          | Convention               | Example                                 |
|---------------|--------------------------|-----------------------------------------|
| ID            | lowerCamelCase           | id="productFilterApp"                   |
| JS Hook       | data-js="lowerCamelCase" | data-js="productFilterApp"              |
| data-* config | data-* attributes        | data-settings="..."                     |
| App Root ID   | lowerCamelCase           | productFilterApp                        |
| Vue Component | PascalCase               | `<ProductFilterApp></ProductFilterApp>` |
| EntryPoint    | UpperCamelCase           | ProductFilterApp.js                     |
| Bootstrap JS  | data-bs-*                | data-bs-toggle="dropdown"               |
