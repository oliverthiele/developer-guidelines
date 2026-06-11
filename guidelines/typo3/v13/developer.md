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

---

## Custom View classes (replacing AbstractView)

Both `TYPO3\CMS\Extbase\Mvc\View\AbstractView` and
`TYPO3\CMS\Extbase\Mvc\View\ViewInterface` were **removed in v12**.

**Do not use either** — the upgrade scanner reports both as "strong" breaking
changes even on a v13 installation.

The correct replacement is `TYPO3\CMS\Core\View\ViewInterface`
(namespace `TYPO3\CMS\Core\View`, not Extbase).

```php
use TYPO3\CMS\Core\View\ViewInterface;

class MyCustomView implements ViewInterface
{
    protected array $variables = [];

    public function assign(string $key, mixed $value): self
    {
        $this->variables[$key] = $value;
        return $this;
    }

    public function assignMultiple(array $values): self
    {
        foreach ($values as $key => $value) {
            $this->assign($key, $value);
        }
        return $this;
    }

    public function render(string $templateFileName = ''): string
    {
        // access assigned variables via $this->variables
    }
}
```

Key details:
- Return type of `assign()`/`assignMultiple()` is `self`, not `static`
- `render()` signature is `render(string $templateFileName = ''): string`
- `$this->variables` must be declared explicitly — it is no longer inherited
