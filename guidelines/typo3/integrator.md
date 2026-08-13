---
title: TYPO3 Integrator
scope: typo3
applies_to:
  - "**/Configuration/**/*.typoscript"
  - "**/Configuration/Sets/**"
  - "**/*.tsconfig"
typo3: ["13", "14"]
see_also: ["typo3/developer.md", "typo3/versions.md", "xliff/typo3.md"]
---

# TYPO3 Integrator Guidelines

TYPO3 conventions for integrators: TypoScript, SiteSets, backend configuration.

For PHP / TCA / Fluid conventions, see `developer.md`. For XLIFF file format and
key naming, see `../xliff/`.

Every rule below states the versions it applies to. A rule without a
`**Validity:**` line holds for all supported versions. See `versions.md` for the
full table and `README.md` for how the version model works.

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

## TypoScript includes — `@import`, not `<INCLUDE_TYPOSCRIPT:`

**Validity:** deprecated 13.4 · removed 14.0 ·
[#105171](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.4/Deprecation-105171-INCLUDE_TYPOSCRIPTTypoScriptSyntax.html)

> **Stale-knowledge trap:** `<INCLUDE_TYPOSCRIPT:` was the standard for over a
> decade and dominates older documentation and training data. It is gone in v14.
> This rule outranks anything remembered about TypoScript includes.

```typoscript
# Wrong — deprecated since 13.4, removed in v14
<INCLUDE_TYPOSCRIPT: source="FILE:EXT:my_extension/Configuration/TypoScript/setup.typoscript">
<INCLUDE_TYPOSCRIPT: source="DIR:EXT:my_extension/Configuration/TypoScript/" extensions="typoscript">

# Correct
@import 'EXT:my_extension/Configuration/TypoScript/setup.typoscript'
@import 'EXT:my_extension/Configuration/TypoScript/*.typoscript'
```

Rules:

- File extension must be `.typoscript` — rename legacy `.ts`/`.txt` files
  before migrating
- `@import` only resolves `EXT:` paths, not arbitrary paths like `fileadmin/`
- No recursive directory inclusion — use multiple `@import` statements or
  restructure the directory instead of relying on `DIR:` recursion
- Conditions wrap the import; they are not passed as a `condition` parameter:

```typoscript
# Wrong
<INCLUDE_TYPOSCRIPT: source="FILE:EXT:my_extension/Configuration/TypoScript/user.typoscript" condition="[frontend.user.isLoggedIn]">

# Correct
[frontend.user.isLoggedIn]
    @import 'EXT:my_extension/Configuration/TypoScript/user.typoscript'
[END]
```

---

## SiteSets

**Validity:** since 13.1 ·
[#103437](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.1/Feature-103437-IntroduceSiteSets.html)
· unchanged in v14

SiteSets replaced the old "include static" mechanism.

### File structure

```
Configuration/Sets/{SetName}/
    config.yaml                  — Set registration (name, dependencies, label)
    settings.definitions.yaml    — Setting definitions with types and defaults
    setup.typoscript             — TypoScript setup (auto-included via SiteSet)
    constants.typoscript         — TypoScript constants (auto-included via SiteSet)

Resources/Private/Language/
    labels.xlf                   — English labels for settings
    de.labels.xlf                — German translations
```

### TypoScript in SiteSets

TypoScript is still used — it is auto-included when the SiteSet is declared as a
dependency.

Do **not** write "Zero TypoScript" or "no TypoScript needed" for SiteSet-based
extensions.

Correct description: _"TypoScript is provided as part of the TYPO3 SiteSet — no
manual TypoScript includes required, just add the extension as a SiteSet
dependency."_

### Settings definitions — always flat dot-notation

**Validity:** canonical format since 13.4 · nested YAML still read for backwards
compatibility · no dedicated changelog entry — verified in practice

`settings.definitions.yaml` must use flat dot-notation keys. Never use nested
YAML structure.

```yaml
# Correct — flat map
otFoo.mainColor:
    type: color
    default: '#ff0000'

otFoo.subSection.itemLimit:
    type: int
    default: 10
```

```yaml
# Wrong — nested YAML structure
otFoo:
    mainColor:
        type: color
        default: '#ff0000'
```

The reason: nested structure made it impossible to have both `foo.bar` and
`foo.bar.baz` as distinct settings — the tree cannot represent both
simultaneously. The flat map eliminates this limitation.

The XLIFF key is always the full dot-separated path prefixed with `settings.`:

```xml
<trans-unit id="settings.otFoo.mainColor" resname="settings.otFoo.mainColor">
  <source>Main color</source>
</trans-unit>

<trans-unit id="settings.otFoo.subSection.itemLimit"
            resname="settings.otFoo.subSection.itemLimit">
  <source>Item limit</source>
</trans-unit>
```

### labels.xlf key naming

| Key pattern                           | Purpose             |
|---------------------------------------|---------------------|
| `settings.{vendor}.{key}`             | Setting label       |
| `settings.description.{vendor}.{key}` | Setting description |

**Critical:** TYPO3 resolves descriptions via the `settings.description.`
prefix. `settings.{key}.description` (wrong order) means the description is
never displayed.

```xml
<!-- Correct -->
<trans-unit id="settings.description.otFoo.myKey"
            resname="settings.description.otFoo.myKey">
  <source>My setting description</source>
</trans-unit>

<!-- Wrong — description never shown -->
<trans-unit id="settings.otFoo.myKey.description"
            resname="settings.otFoo.myKey.description">
```

For the full SiteSet label conventions and enum label localization, see
`../xliff/typo3.md`.

---

## New Content Element Wizard — auto-registered via TCA

**Validity:** since 13.0 ·
[#102834](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.0/Feature-102834-Auto-registrationOfNewContentElementWizardViaTCA.html)
· unchanged in v14

The wizard entry is generated automatically from the `CType` TCA select item — a
separate `page.tsconfig` wizard registration is no longer needed:

```php
// Configuration/TCA/Overrides/tt_content.php — this alone is sufficient
ExtensionManagementUtility::addTcaSelectItem(
    'tt_content',
    'CType',
    [
        'label' => $ll . 'wizard.title',
        'value' => $extensionKey,
        'icon' => 'my-icon-identifier',
        'group' => 'default',
        'description' => $ll . 'wizard.description',
    ],
    'textmedia',
    'after',
);
```

Do not add a `Configuration/page.tsconfig` with
`mod.wizards.newContentElement.wizardItems…` for a new v13+/v14-only
extension — it is redundant. To hide/remove an item instead, use
`mod.wizards.newContentElement.wizardItems.<group>.removeItems` (the old
`.show := removeFromList(...)` option is no longer evaluated).

### Wizard groups — core defaults vs. `extras`

Core-provided groups (see `EXT:frontend`'s `tt_content.CType.config.itemGroups`):
`default`, `lists`, `menu`, `forms`, `special`, `plugins`.

SiteKit (`ot-sitekit-base`) registers additional custom groups via
`ExtensionManagementUtility::addTcaSelectItemGroup()`, including `extras`.
Use `'group' => 'extras'` for content elements that are not typical page body
content — reserve `default` for elements that are ordinary page content.

This works even for extensions without a hard dependency on SiteKit: without
`ot-sitekit-base` installed, the group simply falls back to showing the raw
key `extras` as its heading instead of a translated label — a cosmetic
degradation, not an error.

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

For XLIFF format, key naming, ICU plurals and file structure, see
→ `../xliff/README.md`
