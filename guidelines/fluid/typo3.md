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

## Building a view

Never instantiate a view directly — inject `ViewFactoryInterface`. The full
rule, including custom view classes and the `Core\View` vs. Extbase namespace
trap, is in [../typo3/developer.md](../typo3/developer.md) → *Views — never
instantiate a view directly*.

The standalone counterpart is the exact opposite; see
[README.md](README.md) → *Building a view — standalone* before carrying a
snippet from one context into the other.
