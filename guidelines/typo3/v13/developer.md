# TYPO3 v13 — Developer

Version-specific additions to `docs/guidelines/typo3-developer.md` for TYPO3
v13 / Fluid 4.

---

## Fluid 4 — Argument types

Union types in `<f:argument>` are **not supported** in Fluid 4 (TYPO3 v13).
They are available from Fluid 5 / TYPO3 v14 onwards.

```xml
<!-- Correct in TYPO3 v13 — one explicit type per argument -->
<f:argument name="columns" type="integer"/>
<f:argument name="breakpoints" type="array"/>

    <!-- Wrong — union type causes "Cannot cast an array to string" in Fluid 4 -->
<f:argument name="columns" type="int|array"/>
```

Where multiple types are needed: use separate arguments or `type="mixed"` as a
last resort.
