# Vue Guidelines

Vue conventions for all projects.

For shared JavaScript conventions (IDs, `data-js`, DOM hooks, entry points),
see:

→ `javascript.md`

---

## When to use Vue

Use Vue when:

- the UI is stateful and multiple components need to share or react to state
- the interaction requires dynamic rendering (lists, conditional blocks,
  computed views)
- the feature has enough complexity that Vanilla JS would become hard to
  maintain

Use Vanilla JS when:

- the interaction is isolated and one-off (toggle, scroll handler, simple modal)
- no shared state is required
- a third-party library (e.g. Bootstrap JS) already handles it

Rule: **Vue is always a conscious decision** — default to Vanilla JS and
escalate to Vue
only when the complexity justifies it.

---

## Component syntax

Always use `<script setup>` (Composition API):

```vue

<script setup>
    import {ref, computed} from 'vue'

    const count = ref(0)
    const doubled = computed(() => count.value * 2)
</script>

<template>
    <div>{{ doubled }}</div>
</template>
```

Never use the Options API for new components.

---

## Component naming

- File name: `PascalCase` — `ProductFilterApp.vue`
- Component name in template: `PascalCase` — `<ProductFilterApp />`
- One component per file

```html
<!-- Correct -->
<ProductFilterApp/>

<!-- Wrong -->
<product-filter-app/>
```

---

## App root integration (TYPO3 / Fluid)

Vue apps are mounted on a dedicated root element in the HTML.

- ID: `lowerCamelCase` (see `javascript.md` → IDs)
- Data is passed via `data-*` attributes, rendered via Fluid
- One root element per app instance

```html
<!-- Fluid template -->
<div id="productFilterApp"
     data-settings="{f:format.json(value: settings)}"
     data-items="{f:format.json(value: items)}">
</div>
```

```javascript
import {createApp} from 'vue'
import ProductFilterApp from './ProductFilterApp.vue'

const rootElement = document.getElementById('productFilterApp')
if (rootElement) {
    createApp(ProductFilterApp).mount(rootElement)
}
```

---

## State management

- Local state: `ref` / `reactive`
- Shared state between components: `provide` / `inject` or a composable
- Use Pinia only when state needs to be accessed across multiple unrelated trees

---

## Props and emits

Always declare props and emits explicitly:

```vue

<script setup>
    const props = defineProps({
        items: {
            type: Array,
            required: true,
        },
        initialPage: {
            type: Number,
            default: 1,
        },
    })

    const emit = defineEmits(['update:page'])
</script>
```

---

## Composables

- File name: `useFeatureName.js` (lowerCamelCase with `use` prefix)
- One responsibility per composable
- Always return reactive values

```javascript
// Correct
export function useProductFilter(items) {
    const query = ref('')
    const filtered = computed(() => items.filter(...))
    return {query, filtered}
}
```

---

## Anti-patterns

- Using Vue for simple one-off interactions (use Vanilla JS instead)
- Options API in new components
- Global state via `window.*`
- Selecting elements inside a Vue component with `document.querySelector`
- Bypassing the root element pattern (inline `createApp` without a dedicated
  root)
