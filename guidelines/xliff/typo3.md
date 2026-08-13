---
title: XLIFF in TYPO3
scope: xliff
applies_to:
  - "**/Resources/Private/Language/*.xlf"
  - "**/Configuration/Sets/**/labels.xlf"
  - "**/Configuration/Sets/**/settings.definitions.yaml"
typo3: ["13", "14"]
see_also: ["xliff/README.md", "xliff/keys.md", "typo3/integrator.md"]
---

# XLIFF in TYPO3

How TYPO3 loads and resolves XLIFF files. For the file format see
[README.md](README.md), for key conventions see [keys.md](keys.md).

## LLL references

- The `original` attribute is used by TYPO3 to resolve the fallback chain —
  always point it to the English source file, even in translation files
- TYPO3 reads translations via `LLL:EXT:...` references; the path in `original`
  must match the actual file path exactly
- TCA `label` values use the `LLL:EXT:...` prefix:

  ```php
  'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:my.key',
  ```

- Do not mix UI labels and TCA labels in the same file
- Use `locallang_db.xlf` strictly for TCA labels
- Never hardcode labels in TCA, Fluid, or PHP — always use LLL references

For `<f:translate>`'s `extensionName` argument, see `../typo3/integrator.md`.

---

## SiteSet labels.xlf

**Validity:** since 13.1 (with SiteSets) · unchanged in v14

SiteSet `Configuration/Sets/{Name}/labels.xlf` provides labels via **automatic
key resolution** — no `LLL:` reference is needed in `settings.definitions.yaml`.

### Automatic key conventions

| Key pattern                         | Resolves to                                         |
|-------------------------------------|-----------------------------------------------------|
| `label`                             | SiteSet display name (shown in backend site wizard) |
| `categories.{CategoryName}`         | Category label                                      |
| `settings.{settingKey}`             | Setting label                                       |
| `settings.description.{settingKey}` | Setting description (shown below the field)         |

### settings.definitions.yaml — correct pattern

```yaml
# Correct: no label or description fields — resolved from labels.xlf automatically
categories:
    MyExt:
    MyExt.general:
        parent: MyExt

settings:
    myExt.someOption:
        category: MyExt.general
        type: string
        default: ''
```

```yaml
# Wrong: hardcoded label strings
settings:
    myExt.someOption:
        type: string
        default: ''
        label: 'Some option'               ← wrong: hardcoded string
        description: 'Explanation text'    ← wrong: hardcoded string
```

```yaml
# Wrong: explicit LLL reference — not needed, automatic resolution is sufficient
settings:
    myExt.someOption:
        type: string
        default: ''
        label: 'LLL:EXT:my_ext/Configuration/Sets/MySet/labels.xlf:settings.myExt.someOption'
```

### labels.xlf — correct pattern (XLIFF 2.0 for v14+ extensions)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff version="2.0" xmlns="urn:oasis:names:tc:xliff:document:2.0" srcLang="en">
  <file id="my-ext-labels"
        original="EXT:my_ext/Configuration/Sets/MySet/labels.xlf">
    <unit id="label">
      <segment>
        <source>My Extension</source>
      </segment>
    </unit>
    <unit id="categories.MyExt">
      <segment>
        <source>My Extension</source>
      </segment>
    </unit>
    <unit id="categories.MyExt.general">
      <segment>
        <source>General</source>
      </segment>
    </unit>
    <unit id="settings.myExt.someOption">
      <segment>
        <source>Option label</source>
      </segment>
    </unit>
    <unit id="settings.description.myExt.someOption">
      <segment>
        <source>Description shown below the field.</source>
      </segment>
    </unit>
  </file>
</xliff>
```

**Critical:** descriptions resolve via the `settings.description.` prefix.
`settings.{key}.description` (wrong order) means the description is never
displayed.

---

## Enum label localization

**Validity:** since 14.2 ·
[#106640](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Feature-106640-LocalizeEnumLabelsInSiteSettingsDefinitions.html)

Enum option labels in `settings.definitions.yaml` can be localized via
`labels.xlf`.

**List-style enum — XLIFF keys are auto-derived:**

```yaml
# settings.definitions.yaml
myExt.layout:
    type: string
    default: grid
    enum:
        - grid
        - masonry
        - justified
```

TYPO3 derives the key automatically as `settings.{settingKey}.enum.{enumValue}`:

```xml
<unit id="settings.myExt.layout.enum.grid">
  <segment>
    <source>Grid</source>
  </segment>
</unit>
<unit id="settings.myExt.layout.enum.masonry">
  <segment>
    <source>Masonry</source>
  </segment>
</unit>
```

**Map-style enum — explicit control per option:**

```yaml
myExt.layout:
    type: string
    default: grid
    enum:
        grid: 'LLL:EXT:my_ext/.../labels.xlf:settings.myExt.layout.enum.grid'
        masonry: 'Masonry layout'   # literal — used as-is
        justified:                  # no value — falls back to 'justified'
```

Use list-style for the common case. Map-style is only needed when options
require different label strategies (e.g. mixing `LLL:` references with
literals).
