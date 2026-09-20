---
title: Fluid in TYPO3
scope: fluid
applies_to:
  - "**/Resources/Private/Templates/**/*.html"
  - "**/Resources/Private/Partials/**/*.html"
  - "**/Resources/Private/Layouts/**/*.html"
typo3: ["13", "14"]
see_also: ["fluid/README.md", "typo3/developer.md", "typo3/integrator.md", "typo3/versions.md"]
---

# Fluid in TYPO3

Rules for Fluid as the core ships it: core ViewHelpers, backend module
templates, RTE output. None of this exists in a standalone Fluid application.

Engine-level rules — syntax, argument types, tag attributes, file resolution —
are in [README.md](README.md) and apply here too.

Validity lines on this page name the **major TYPO3 version only**. Which sprint
release introduced something is in the changelog index, column 3; what matters
for a project is what the LTS carries.

Related files:

| | |
|---|---|
| [../typo3/developer.md](../typo3/developer.md) | building a view in PHP, `ViewFactoryInterface` |
| [../typo3/content-blocks.md](../typo3/content-blocks.md) | `cb:assetPath()`, asset loading, CB template conventions |
| [../typo3/sitekit.md](../typo3/sitekit.md) | template path layers in SiteKit projects |
| [../xliff/typo3.md](../xliff/typo3.md) | `LLL:` references in templates |

---

## `f:format.html` — never pass an empty `parseFuncTSPath`

**Tooling:** `fluid-lint` detects this · auto-fixable

Always use the inline notation for RTE content. Never pass `parseFuncTSPath=""`.

```html
{record.bodytext -> f:format.html()}
```

`parseFuncTSPath=""` (empty string) causes
`Invoked ContentObjectRenderer::parseFunc without any configuration` — a fatal
error at runtime. The default value (`lib.parseFunc_RTE`) is correct for RTE
fields and must not be overridden with an empty string.

| Pattern                                                     | Result                             |
|-------------------------------------------------------------|------------------------------------|
| `{field -> f:format.html()}`                                | correct — uses `lib.parseFunc_RTE` |
| `<f:format.html>{field}</f:format.html>`                    | correct — same as above            |
| `<f:format.html parseFuncTSPath="">{field}</f:format.html>` | **wrong — runtime error**          |

---

## `f:translate` arguments must be a list — keys start at 0

**Validity:** v14+ (14.2) ·
[#104546](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Feature-104546-SupportICUMessageFormatForPluralForms.html)
· changed behaviour against v13

Since 14.2 a label can be an ICU message, and `LanguageService::translate()`
decides which of the two ways to fill it by looking at the argument array:

```php
if ($arguments !== []) {
    if (!array_is_list($arguments)) {
        return $this->formatIcuMessage($result, $arguments);   // ICU, named arguments
    }
    return vsprintf($result, $arguments);                      // sprintf, positional
}
```

`array_is_list()` is true only for keys `0, 1, 2, …` without gaps. An array that
starts at 1 is not a list, so it takes the ICU branch — and ICU has no `%1$s`, so
the placeholder is left standing and reaches the page:

```html
<!-- Wrong — renders "Type %1$s is also available" -->
<f:translate key="type.also_available" arguments="{1: '{product.type}'}"/>

<!-- Correct -->
<f:translate key="type.also_available" arguments="{0: '{product.type}'}"/>
```

**This is silent, and it is a change.** v13 called
`sprintf($value, ...array_values($arguments))`, which ignores the keys entirely —
so `{1: …}` worked there and reads as if it pairs up with the `%1$s` in the label.
Nothing warns on upgrade: no exception, no deprecation, no log entry. The only
symptom is the raw placeholder in the rendered page.

The same applies to `LocalizationUtility::translate()` in PHP, which passes its
argument array straight through.

When auditing a code base for this, grep the **rendered output**, not the
templates — a multi-line `arguments="…"` attribute is easy to miss:

```bash
curl -s https://example.com/some-page | grep -o '%[0-9]*\$\?[sd]'
```

Named arguments (`arguments="{count: items.count}"`) are the ICU case and are
correct by construction — but then the label must be an ICU message, not a
`%d` string.

---

## Backend module templates need the `Module` layout

A template rendered through `ModuleTemplate::renderResponse()` must declare the
core layout and put its markup into a `Content` section:

```html

<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:layout name="Module"/>

<f:section name="Content">
    …
</f:section>

</html>
```

> **Common AI-generation error:** a template without `f:layout` still renders,
> and the module looks almost right — which is why this slips through. Nothing
> errors, so only a side-by-side comparison with another module reveals it.

`EXT:backend/Resources/Private/Layouts/Module.html` supplies three things the
template does not get on its own:

| Element                                      | Consequence when the layout is missing                                                                                                  |
|----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| `<div class="module-body t3js-module-body">` | The content sits flush against the edge — every other backend module has padding, this one does not                                     |
| `<f:flashMessages/>`                         | **Flash messages never appear.** `addFlashMessage()` still queues them, so the code looks correct and the message is silently swallowed |
| `DocHeader` partial                          | Doc header buttons and the module menu are not rendered                                                                                 |

The second one is the damaging one: an action reports success or failure through
a flash message, the user sees nothing, and there is no error anywhere to
notice.

---

## `f:render.contentArea` — content areas without `f:cObject`

**Validity:** v14+ ·
[#108726](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Feature-108726-IntroduceFluidRenderContentAreaViewHelper.html)
· verified in `ContentAreaViewHelper` (core 14.3.4)

Render a content area from the `page-content` DataProcessor directly:

```html
<f:render.contentArea contentArea="{content.main}"/>

{content.main -> f:render.contentArea()}
```

The `{content}` variable comes from the processor, commonly behind `PAGEVIEW`:

```typoscript
page = PAGE
page {
    10 = PAGEVIEW
    10 {
        paths.10 = EXT:my_sitepackage/Resources/Private/Templates/
        dataProcessing.10 = page-content
    }
}
```

> **Stale-knowledge trap:** the established way to render a column is
> `<f:cObject typoscriptObjectPath="lib.dynamicContent">`, or an `<f:for>` over
> the column with a partial per element. Both dominate a decade of examples and
> are the default a language model reaches for. Neither *fails* — which is why
> it survives review — but both opt the template out of the event below.

Two arguments, and no others:

| Argument | Type | Purpose |
|---|---|---|
| `contentArea` | `TYPO3\CMS\Core\Page\ContentArea` | the area from the processor |
| `recordAs` | `string` | variable name for the current record |

`recordAs` is what replaces the `f:for` — wrap each element without leaving the
ViewHelper:

```html
<div id="sidebar">
    <f:render.contentArea contentArea="{content.left}" recordAs="record">
        <div id="sidebarItem{record.uid}">
            <f:render.record record="{record}"/>
        </div>
    </f:render.contentArea>
</div>
```

**Why this matters beyond convenience:** rendering through the ViewHelper emits
`ModifyRenderedContentAreaEvent`, so other extensions can modify a content
area's output. An `f:cObject` or `f:for` template produces the same HTML and no
event — the extension point is simply absent, and nothing indicates that.

---

## The request in a ViewHelper — an attribute, not `getRequest()`

**Validity:** deprecated in v13 · **removed in v14** ·
[#104684](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.3/Deprecation-104684-FluidRenderingContext-getRequest.html)

> **Stale-knowledge trap:** `$this->renderingContext->getRequest()` is the line
> nearly every custom ViewHelper used to reach the request with. It no longer
> exists in v14, and the ExtensionScanner deliberately does not look for it —
> the method name is too common to scan without flooding the report with false
> positives. Nothing warns before the fatal error.

Fluid standalone keeps its rendering context free of PSR-7, so the request is
carried as an attribute instead:

```php
use Psr\Http\Message\ServerRequestInterface;

// Correct — v14
$request = null;
if ($this->renderingContext->hasAttribute(ServerRequestInterface::class)) {
    $request = $this->renderingContext->getAttribute(ServerRequestInterface::class);
}

// Wrong — removed in v14, fatal error
$request = $this->renderingContext->getRequest();
```

Check with `hasAttribute()` first: a ViewHelper rendered outside a request —
a CLI command building a mail body, for instance — has no request, and
`getAttribute()` alone would fail there.

The core's own ViewHelpers use exactly this call; `TranslateViewHelper` and
`CObjectViewHelper` are short examples to read.

---

## Building a view

Never instantiate a view directly — inject `ViewFactoryInterface`. The full
rule, including custom view classes and the `Core\View` vs. Extbase namespace
trap, is in [../typo3/developer.md](../typo3/developer.md) → *Views — never
instantiate a view directly*.

The standalone counterpart is the exact opposite; see
[README.md](README.md) → *Building a view — standalone* before carrying a
snippet from one context into the other.
