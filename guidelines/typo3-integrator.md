# TYPO3 Integrator Guidelines

TYPO3 conventions for integrators. Applies to all supported TYPO3 versions
unless a version-specific file states otherwise.

## Scope

- TypoScript
- SiteSets
- XLIFF usage in TYPO3 context
- Backend configuration

For PHP / TCA / Fluid conventions, see `typo3-developer.md`.

## Version-specific additions

| Version | File                      |
|---------|---------------------------|
| v13     | `typo3/v13/integrator.md` |

Load the file matching your project's TYPO3 version in addition to this one.

There is no integrator file for v14 yet. In a v14 project, read
`typo3/v13/integrator.md` with care: rules describing something as *deprecated
in v13, removed in v14* (e.g. `<INCLUDE_TYPOSCRIPT:`) describe an already
completed removal there, and statements about SiteSets and the New Content
Element wizard must be verified against v14 before being applied.

---

## Script Directories

| Directory      | Purpose                                                             | Deployed to live |
|----------------|---------------------------------------------------------------------|------------------|
| `bin-dev/`     | Dev-workflow scripts (watch processes, DB sync, environment setup)  | No               |
| `Build/*/bin/` | Build-tool-specific scripts (Node/npm utilities, Bootstrap upgrade) | No               |
| `bin/`         | Scripts required in production (Deployer tasks, cron helpers)       | Yes              |

Rule of thumb: if it runs via `node`/`npm` and belongs to the build tooling,
place it in `Build/*/bin/`. If it is a shell script for the local dev workflow,
place it in `bin-dev/`. Exclude `bin-dev/` from deployments.

---

## Frontend Framework Folder Structure

Group `Templates`/`Partials`/`Layouts` under a framework/flavor folder instead
of TYPO3's more common `Templates/{Flavor}/` layout, so a single folder name
(or TypoScript constant) switches the entire template set at once — useful
when an extension may need to support more than one design system over its
lifetime.

Two variants are in use, depending on whether the extension depends on
SiteKit:

**SiteKit-integrated extensions** — flavor is a TypoScript constant, giving
per-site configurability without touching TypoScript at all:

```
Resources/Private/Templates/{$sitekit.frameworks.frontend.directory}/
    Templates/CeCard.html
    Partials/…
    Layouts/…
```

```typoscript
# packages/ot-sitekit-ce-card/Configuration/TypoScript/setup.typoscript
templateRootPaths {
  20 = EXT:ot_sitekitcecard/Resources/Private/Templates/{$sitekit.frameworks.frontend.directory}/Templates/
}
partialRootPaths {
  20 = EXT:ot_sitekitcecard/Resources/Private/Templates/{$sitekit.frameworks.frontend.directory}/Partials/
}
```

**Standalone extensions** (no SiteKit dependency) — flavor is a hardcoded
top-level folder instead, since there is no SiteKit constant to depend on:

```
Resources/Private/Bootstrap5/
    Templates/CountUp.html
    Partials/Item.html
```

```typoscript
# packages/ot-countup/Configuration/TypoScript/setup.typoscript
templateRootPaths {
  10 = EXT:ot_countup/Resources/Private/Bootstrap5/Templates/
}
partialRootPaths {
  10 = EXT:ot_countup/Resources/Private/Bootstrap5/Partials/
}
```

Rules:

- Use index `10`/`20` (not `0`) for the extension's own root paths.
  `TemplatePaths` resolves paths in reverse order (highest index first), so a
  higher index is checked before the core-inherited `0` — using `0` would
  overwrite the inherited default path (e.g. `fluid_styled_content`'s own
  Templates directory) instead of adding to it, removing a fallback that may
  still be needed.
- A consuming project can always override the whole template set, regardless of
  which variant is used, by registering its own path at an even higher index:

  ```typoscript
  # Project sitepackage — wins over the extension's own index 10
  templateRootPaths.100 = EXT:my_sitepackage/Resources/Private/Templates/CountUp/
  ```

  Only the files actually present there are overridden; everything else still
  falls back to the extension's own templates.

---

## TYPO3 translation usage

Always reference labels via `LLL:EXT:`:

```php
'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:my.key',
```

Rules:

- Never hardcode labels
- Always use XLIFF files
- Paths in `LLL:EXT:` must match the actual file path exactly
- The `original` attribute in XLIFF files must point to the English source file

### f:translate — `extensionName` must be UpperCamelCase

`<f:translate>`'s `extensionName` argument expects the **UpperCamelCased**
extension key (e.g. `MySitepackage` for `my_sitepackage`), per
`TranslateViewHelper::initializeArguments()`: `'UpperCamelCased extension key
(for example BlogExample)'`.

```html
<!-- Correct -->
<f:translate key="my_key" extensionName="MySitepackage" />

<!-- Wrong — works today because TYPO3 normalizes it internally, but violates
     the documented argument contract and is a common AI-generation error -->
<f:translate key="my_key" extensionName="my_sitepackage" />
```

Lowercase/underscored values happen to resolve today because TYPO3 normalizes
the extension key internally, but that's an implementation detail, not a
guarantee — always write the UpperCamelCase form.

---

For XLIFF format, key naming, ICU plurals and file structure, see → `xliff.md`
