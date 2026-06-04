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
