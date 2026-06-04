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
