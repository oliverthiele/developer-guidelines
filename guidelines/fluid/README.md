---
title: Fluid — the template engine
scope: fluid
applies_to:
  - "**/Resources/Private/Templates/**/*.html"
  - "**/Resources/Private/Partials/**/*.html"
  - "**/Resources/Private/Layouts/**/*.html"
  - "**/Resources/Private/Components/**/*.html"
  - "**/Classes/ViewHelpers/**/*.php"
typo3: ["13", "14"]
see_also: ["fluid/typo3.md", "typo3/practices/fluid-components.md"]
---

# Fluid Guidelines

Rules for `typo3fluid/fluid` itself: template syntax, the ViewHelper API,
argument handling, file resolution. They hold wherever Fluid runs.

| Also here | |
|---|---|
| [typo3.md](typo3.md) | Fluid inside TYPO3 — core ViewHelpers, backend modules, RTE output |
| [../typo3/practices/fluid-components.md](../typo3/practices/fluid-components.md) | component or partial: a decision guide, not a rule file |

Fluid is not TYPO3-specific. `typo3fluid/fluid` is an independent package and
runs without a core around it, which is why these rules live outside `typo3/` —
the same reason [`../xliff/`](../xliff/README.md) is its own folder.

---

## Which version applies

**In a TYPO3 project, read the TYPO3 major version.** Fluid ships with the core
and the two move together:

| TYPO3 | `typo3fluid/fluid` | Changelog |
|---|---|---|
| v13.1 | 2.11 | [#103560](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.1/Feature-103560-UpdateFluidStandalone.html) |
| v13.2 | 2.12 | [#104223](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.2/Feature-104223-UpdateFluidStandaloneTo212.html) |
| v13.3 | 4.0 | [#104896](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.3/Feature-104896-RaiseFluidStandaloneTo40.html) |
| v14.0 | 5.0 | [#108148](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-108148-Fluid50.html) |

The 2 → 4 jump inside v13 was a version-number change, not a break — it was made
*because* nothing breaking had accumulated. So the major TYPO3 version decides
the rule, and the Fluid number never has to be looked up in a TYPO3 project.

**Standalone has no TYPO3 version.** There the constraint in `composer.json` is
the only answer, and it is unrelated to any core release: a project on
`^2.11` resolving to 2.15 today has neither Fluid 4 nor Fluid 5 behaviour, while
a v14 site of the same age is on Fluid 5. Check what is actually installed:

```bash
composer show typo3fluid/fluid
```

Every rule below therefore states both axes.

---

## Arbitrary tag attributes, and the empty-value trap

**Validity:** Fluid 2.12+ · TYPO3 v13+ ·
[#104223](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.2/Feature-104223-UpdateFluidStandaloneTo212.html)

Tag-based ViewHelpers take any attribute without registering it first:

```html
<f:link.page pageUid="1786" data-fancybox="true" data-type="iframe">
```

**An empty value is the exception, and it fails silently.** Written straight
onto the tag, the attribute is dropped from the output — no error, no warning,
and the template still looks correct:

| Notation | Output |
|---|---|
| `<f:link.page … data-caption="text">` | `data-caption="text"` |
| `<f:link.page … data-caption="">` | **attribute missing** |
| `<f:link.page … data="{caption: ''}">` | `data-caption=""` |

Free attributes travel through `$this->additionalArguments`, where
`AbstractTagBasedViewHelper::initialize()` filters them:

```php
// This condition is left here for compatibility reasons. Removing this will be a breaking change
// because TagBuilder renders empty strings as empty attributes (as it should be).
if ($argumentValue !== null && $argumentValue !== '') {
    $this->tag->addAttribute($argumentName, $argumentValue);
}
```

The `data` and `aria` array arguments a few lines above call `addAttribute()`
unconditionally and skip that filter, so they are the way to emit a deliberately
empty attribute.

A variable that happens to resolve to an empty string hits the same filter, so
`data-caption="{file.description}"` produces no attribute at all for a file
without a description — which is a different DOM from `data-caption=""`, not a
cosmetic difference.

That distinction matters wherever the attribute is load-bearing rather than
decorative:

- a selector a script binds on (`[data-fancybox]`) — the element drops out of
  the binding entirely
- a marker that switches behaviour **off** (`data-caption=""` to suppress a
  lightbox caption) — the suppression silently does not happen

Verify in the rendered page, never in the template:

```bash
curl -s https://example.ddev.site/some-page | grep -o 'data-caption="[^"]*"'
```

---

## Argument types

**Validity:** union types in Fluid 5 · TYPO3 v14+ ·
[#108148](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-108148-UnionTypesForViewHelpers.html)
· not supported in Fluid 4 / TYPO3 v13

```xml
<!-- Fluid 5 / TYPO3 v14 -->
<f:argument name="columns" type="int|array"/>

    <!-- Fluid 4 / TYPO3 v13 — one explicit type per argument -->
<f:argument name="columns" type="integer"/>
<f:argument name="breakpoints" type="array"/>
```

In Fluid 4 a union type causes `Cannot cast an array to string` at runtime.
Where multiple types are needed there: use separate arguments, or `type="mixed"`
as a last resort.

---

## Template file resolution — `.fluid.html`

**Validity:** Fluid 5 · TYPO3 v14+ ·
[#108166](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-108166-FluidFileExtensionAndTemplateResolving.html)
**Tooling:** `fluid-lint` flags templates not yet renamed · auto-fixable

Fluid 5 natively resolves `{Name}.fluid.{format}` before `{Name}.{format}` for
Templates, Partials and Layouts — see `TemplatePaths::resolveFileInPaths()` in
`typo3fluid/fluid`. No TypoScript or `view.format` configuration is needed.

Prefer naming Fluid template files `*.fluid.html` (e.g. `Default.fluid.html`) in
v14-only extensions — this is the project convention going forward and gives
IDEs unambiguous syntax highlighting for Fluid vs. plain HTML.

The resolution lives in the engine, not in the core, so it is **not** available
on Fluid 4 or on a standalone project pinned below 5 — `TemplatePaths.php` in
2.15 has no `.fluid.` handling at all. Renaming files there silently stops them
being found.

---

## CDATA no longer comments code out

**Validity:** Fluid 5 · TYPO3 v14+ ·
[#108148](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-108148-CDATASectionsNoLongerRemoved.html)
**Tooling:** `fluid-lint` detects this · auto-fixable with `--fix`

> **Stale-knowledge trap:** `<f:comment><![CDATA[ … ]]></f:comment>` is the
> idiom a decade of templates and examples use to comment out Fluid safely. It
> is the first thing to reach for, and from v14 on it does the opposite of what
> it says.

Fluid used to **remove** everything wrapped in `<![CDATA[ ]]>` from the template
before parsing. That is what made it a comment: the parser never saw the block,
so invalid Fluid or a stray ViewHelper call inside it could not break rendering.

Fluid 5 stops stripping CDATA. The content is no longer removed, so the
construct comments nothing out — and it writes a deprecation entry on **every
render** from TYPO3 13.4.21 on. A template set that used the idiom consistently
fills its deprecation log with them.

```html
<!-- Wrong from v14 on — no longer a comment -->
<f:comment><![CDATA[
    <f:render partial="Old" />
]]></f:comment>

<!-- Correct -->
<f:comment>
    <f:render partial="Old" />
</f:comment>
```

The plain `<f:comment>` is enough on its own: since v13.3 it ignores Fluid
syntax errors in its body
([#104904](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.3/Feature-104904-IgnoreFluidSyntaxErrorInFComment.html)),
which is exactly what the CDATA used to provide.

### CDATA is not gone — it means something else now

**Validity:** Fluid 5 · TYPO3 v14+ ·
[#108148](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-108148-AlternativeFluidSyntaxForCDATASections.html)

Inside a CDATA section, Fluid now ignores the normal `{…}` syntax and disables
tag-based syntax entirely; `{{{…}}}` accesses variables and ViewHelpers. This
exists to stop inline CSS and JavaScript from colliding with Fluid's braces:

```html
<style>
<![CDATA[
    @media (min-width: 1000px) {
        p { background-color: {{{color}}}; }
    }
]]>
</style>
```

Do not read that as an invitation. The core changelog says plainly that inline
CSS and JavaScript in a template remains bad practice — pass values through
`data-*` attributes or CSS custom properties instead. The point here is that
CDATA is *reserved for something else now*, which is why it can no longer be a
comment.

---

## Namespace URI — `http://`, never `https://`

**Tooling:** `fluid-lint` detects this · auto-fixable

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">
```

The `xmlns` value is an identifier, not an address — nothing is ever fetched
from it. `https://typo3.org/ns/…` throws a runtime exception. The scheme is not
a modernisation candidate: leave it as `http://`, in every template, forever.

---

## Building a view — standalone

**Validity:** Fluid 2.x through 5.x · verified against 2.15.0 and 5.3.1

Standalone code constructs the view itself:

```php
use TYPO3Fluid\Fluid\View\TemplateView;

$view = new TemplateView();
```

`TYPO3Fluid\Fluid\View\TemplateView` is `@api` and still constructible in Fluid
5 — it is a different class from the core's `TYPO3\CMS\Fluid\View\TemplateView`,
which is the one v14 removed.

> **This is the opposite of the TYPO3 rule.** Inside TYPO3, instantiating a view
> directly is wrong: inject `ViewFactoryInterface`, see
> [`../typo3/developer.md`](../typo3/developer.md) → *Views — never instantiate
> a view directly*. Neither rule transfers to the other context. There is no
> `ViewFactoryInterface` outside the core, and nothing in the standalone package
> deprecates `new TemplateView()`. The similar class names are what makes this
> easy to get backwards — check the namespace, not the class name.

### Template paths move to the RenderingContext in Fluid 5

**Validity:** breaking between Fluid 4 and 5 · TYPO3 v14+ ·
verified in `AbstractTemplateView` (2.15.0 line 96) and its absence in 5.3.1

`getTemplatePaths()` is no longer on the view. It exists only on the
`RenderingContext`:

```php
// Fluid 2.x / 4.x — works, and is gone in 5
$paths = $view->getTemplatePaths();

// Fluid 5 — the only remaining route
$paths = $view->getRenderingContext()->getTemplatePaths();
```

`TemplatePaths` itself is unchanged: `setTemplateRootPaths()`,
`setLayoutRootPaths()`, `setPartialRootPaths()`,
`setTemplatePathAndFilename()` and `setLayoutPathAndFilename()` all still exist.
Only the way to reach the object changed.

The Fluid 5 view exposes just `getRenderingContext()`,
`setRenderingContext()`, `assign()`, `assignMultiple()`, `render()`,
`renderSection()` and `renderPartial()` — a wrapper class that reaches for
anything else will not survive the upgrade.
