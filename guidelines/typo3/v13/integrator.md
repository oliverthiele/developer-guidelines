# TYPO3 v13 — Integrator

Version-specific additions to `docs/guidelines/typo3-integrator.md` for TYPO3
v13.

---

## SiteSets

SiteSets were introduced in TYPO3 v13 as the replacement for the old "include
static" mechanism.

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

Correct description: _"TypoScript is provided as part of the TYPO3 v13 SiteSet —
no manual
TypoScript includes required, just add the extension as a SiteSet dependency."_

### TypoScript includes — use `@import`, not `<INCLUDE_TYPOSCRIPT:`

`<INCLUDE_TYPOSCRIPT:` is deprecated since TYPO3 v13.4 and will be removed in
v14 ([Deprecation #105171](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.4/Deprecation-105171-INCLUDE_TYPOSCRIPTTypoScriptSyntax.html)).
Always use `@import` instead.

```typoscript
# Wrong — deprecated since v13.4, removed in v14
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

### Settings definitions — always flat dot-notation

`settings.definitions.yaml` must use flat dot-notation keys. Never use nested
YAML structure.

```yaml
# Correct — flat map (canonical format since TYPO3 v13.4)
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

TYPO3 v13.4 switched `settings.yaml` storage from tree to flat map format.
The reason: nested structure made it impossible to have both `foo.bar` and
`foo.bar.baz` as distinct settings — the tree cannot represent both
simultaneously. The flat map eliminates this limitation. Nested YAML is still
read for backwards compatibility, but flat dot-notation is the canonical format
and must be used in all new definitions.

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
prefix.
`settings.{key}.description` (wrong order) means the description is never
displayed.

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

---

## New Content Element Wizard — auto-registered via TCA

Since TYPO3 v13.0 (Feature `#102834`), the "New Content Element" wizard entry
is generated automatically from the `CType` TCA select item — a separate
`page.tsconfig` wizard registration is no longer needed:

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
content (e.g. `ot-heroimage`, `ot-markdown`, `ot-cefluidtemplates`,
`ot-sitekit-ce-texticon`, `ot-countup`) — reserve `default` for elements that
are ordinary page content.

This works even for extensions without a hard dependency on SiteKit: without
`ot-sitekit-base` installed, the group simply falls back to showing the raw
key `extras` as its heading instead of a translated label — a cosmetic
degradation, not an error.
