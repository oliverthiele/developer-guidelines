# XLIFF Guidelines

XLIFF format conventions for TYPO3 extensions.

## Version selection

| TYPO3 support          | XLIFF version to use |
|------------------------|----------------------|
| v13 only, or v13 + v14 | **1.2**              |
| v14+ only              | **2.0**              |

TYPO3 added XLIFF 2.0 support in v14 and ICU message format for plural forms in
v14.2.
Do not mix versions within one extension.

---

## File naming

| File                  | Purpose                                       |
|-----------------------|-----------------------------------------------|
| `locallang.xlf`       | Source language (English)                     |
| `de.locallang.xlf`    | German translation                            |
| `locallang_db.xlf`    | TCA labels (field labels, select items, etc.) |
| `de.locallang_db.xlf` | German translation of TCA labels              |

Prefix pattern for translations: `{language-code}.{source-filename}.xlf`

---

## Formatting

Defined in `.editorconfig` — PhpStorm applies this automatically.

| Setting                | Value   |
|------------------------|---------|
| `indent_style`         | `space` |
| `indent_size`          | `2`     |
| `charset`              | `utf-8` |
| `end_of_line`          | `lf`    |
| `insert_final_newline` | `true`  |

Additional formatting rules:

- Keep `<source>` and `<target>` on a single line whenever possible
  → Improves side-by-side comparison in IDEs
- Only use blank lines when grouping with XML comments (e.g.
  `<!-- Navigation -->`)
- Only use line breaks when content explicitly requires it (e.g. multiline text,
  emails)
- Treat whitespace as meaningful — do not add or remove spaces inside `<source>`
  or `<target>`
- Use normal spaces by default — only use `&nbsp;` when a non-breaking space is
  explicitly required

---

## XLIFF 1.2

Use for extensions that support TYPO3 v13.

### Source file

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2">
  <file source-language="en" datatype="plaintext"
        original="EXT:my_ext/Resources/Private/Language/locallang.xlf"
        product-name="my-ext">
    <header/>
    <body>
      <trans-unit id="my.key" resname="my.key">
        <source>My label</source>
      </trans-unit>
    </body>
  </file>
</xliff>
```

### Translation file

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2">
  <file source-language="en" target-language="de" datatype="plaintext"
        original="EXT:my_ext/Resources/Private/Language/locallang.xlf"
        product-name="my-ext">
    <header/>
    <body>
      <trans-unit id="my.key" resname="my.key" approved="yes">
        <source>My label</source>
        <target>Meine Beschriftung</target>
      </trans-unit>
    </body>
  </file>
</xliff>
```

### XLIFF 1.2 attributes

**`<file>` — source file:**

| Attribute         | Value                                             | Notes                                 |
|-------------------|---------------------------------------------------|---------------------------------------|
| `source-language` | `en`                                              | always English                        |
| `datatype`        | `plaintext`                                       | always                                |
| `original`        | `EXT:ext_key/Resources/Private/Language/file.xlf` | use `EXT:` prefix, underscore key     |
| `product-name`    | `my-ext`                                          | hyphen-separated composer name suffix |

**`<file>` — translation file:** same as source, plus `target-language="de"`.
`original` points to the **source** file, not the translation file itself.

**`<trans-unit>` — source file:**

| Attribute  | Required | Value                    |
|------------|----------|--------------------------|
| `id`       | yes      | dot-separated key        |
| `resname`  | yes      | identical to `id`        |
| `approved` | no       | not used in source files |

**`<trans-unit>` — translation file:** same as source, plus `approved="yes"`.

---

## XLIFF 2.0

Use for extensions that target TYPO3 v14+ only.

### Source file

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff version="2.0" xmlns="urn:oasis:names:tc:xliff:document:2.0" srcLang="en">
  <file id="my-ext-locallang"
        original="EXT:my_ext/Resources/Private/Language/locallang.xlf">
    <unit id="my.key">
      <segment>
        <source>My label</source>
      </segment>
    </unit>
  </file>
</xliff>
```

### Translation file

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff version="2.0" xmlns="urn:oasis:names:tc:xliff:document:2.0" srcLang="en"
       trgLang="de">
  <file id="my-ext-locallang"
        original="EXT:my_ext/Resources/Private/Language/locallang.xlf">
    <unit id="my.key">
      <segment>
        <source>My label</source>
        <target>Meine Beschriftung</target>
      </segment>
    </unit>
  </file>
</xliff>
```

### XLIFF 2.0 attributes

**`<xliff>`:**

| Attribute | Value                                   | Notes                  |
|-----------|-----------------------------------------|------------------------|
| `version` | `2.0`                                   | always                 |
| `xmlns`   | `urn:oasis:names:tc:xliff:document:2.0` | always                 |
| `srcLang` | `en`                                    | always                 |
| `trgLang` | `de` (etc.)                             | translation files only |

**`<file>`:**

| Attribute  | Value                                             | Notes                                          |
|------------|---------------------------------------------------|------------------------------------------------|
| `id`       | `{ext-key}-{file-name-base}`                      | e.g. `my-ext-locallang`, `my-ext-locallang-db` |
| `original` | `EXT:ext_key/Resources/Private/Language/file.xlf` | same as XLIFF 1.2                              |

**`<unit>`:** replaces `<trans-unit>`. No `resname`, no `approved`.

**What is gone in XLIFF 2.0:**

- No `<body>` wrapper
- No `<header/>` element
- No `resname` attribute
- No `approved` attribute
- No `datatype` attribute on `<file>`

---

## ICU message format (TYPO3 v14.2+)

TYPO3 v14.2 added ICU message format support for plural forms and other variable
interpolation.
Use only in XLIFF 2.0 files (v14+ extensions).

### Plural forms

```xml

<unit id="items.count">
  <segment>
    <source>{count, plural, one {# result} other {# results}}</source>
  </segment>
</unit>
```

**German translation:**

```xml

<unit id="items.count">
  <segment>
    <source>{count, plural, one {# result} other {# results}}</source>
    <target>{count, plural, one {# Ergebnis} other {# Ergebnisse}}</target>
  </segment>
</unit>
```

### Fluid usage

```html

<f:translate
    key="LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:items.count"
    arguments="{count: items->f:count()}"/>
```

### Escaping special characters in ICU

ICU uses `{`, `}`, and `#` as syntax characters. To output them as literal text,
wrap with single quotes:

| Literal output                | ICU syntax |
|-------------------------------|------------|
| `{`                           | `'{'`      |
| `}`                           | `'}'`      |
| `#` (in plural/selectordinal) | `'#'`      |
| `'` (single quote itself)     | `''`       |

```xml
<!-- Outputs: "1 item {SKU}: abc" -->
<source>{count, plural, one {# item '{SKU}': abc} other {# items}}</source>
```

This is a common AI-generation error — unescaped `{` inside a plural branch is
treated as a nested placeholder and causes a parse error at runtime.

### Supported ICU selectors

| Selector        | Use case           | Example                                                         |
|-----------------|--------------------|-----------------------------------------------------------------|
| `plural`        | Grammatical number | `{n, plural, one {1 item} other {# items}}`                     |
| `select`        | Discrete values    | `{gender, select, male {he} female {she} other {they}}`         |
| `selectordinal` | Ordinal numbers    | `{n, selectordinal, one {#st} two {#nd} few {#rd} other {#th}}` |

**Anti-pattern — never work around missing plural support with separate keys:**

```xml
<!-- Wrong: two keys for singular/plural -->
<unit id="result.singular">
  <segment>
    <source>1 result</source>
  </segment>
</unit>
<unit id="result.plural">
  <segment>
    <source>{count} results</source>
  </segment>
</unit>
```

```xml
<!-- Correct: one key with ICU -->
<unit id="result.count">
  <segment>
    <source>{count, plural, one {# result} other {# results}}</source>
  </segment>
</unit>
```

---

## Key naming conventions

- Use **dots** as separators — never hyphens or underscores
- Use **lowerCamelCase** for each segment: `publishedOn`, not `published_on`
- Start with a meaningful **namespace**: `list.`, `show.`, `error.`, etc.
- Every key must have at least one dot

| Context               | Pattern                               | Example                                        |
|-----------------------|---------------------------------------|------------------------------------------------|
| Frontend UI           | `{view}.{element}`                    | `list.noResults`, `show.validUntil`            |
| TCA field label       | `{tablename}.{fieldname}`             | `tx_myext_domain_model_item.title`             |
| TCA field description | `{tablename}.{fieldname}.description` | `tx_myext_domain_model_item.title.description` |
| TCA select item       | `{tablename}.{fieldname}.{value}`     | `tx_myext_domain_model_item.status.active`     |
| FlexForm tab          | `flexform.tab.{name}`                 | `flexform.tab.general`                         |
| Flash message         | `flash.{action}.{result}`             | `flash.save.success`                           |

**Exception — TCA keys:** field and table names use underscores because they
mirror TYPO3 database
identifiers. The underscore is part of the identifier, not a separator within
the key segment.

**Anti-patterns — never use:**

```
current-job-offers      ← hyphens as separator
tx_myext_published_on   ← underscores as separator (TCA exception does not apply here)
applicationByEmail      ← no namespace, missing dot
PublishedOn             ← PascalCase
```

---

## SiteSet labels.xlf (TYPO3 v13+)

SiteSet `Configuration/Sets/{Name}/labels.xlf` provides labels via **automatic
key resolution** —
no `LLL:` reference is needed in `settings.definitions.yaml`.

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

### Enum label localization (v14.2+)

Since TYPO3 v14.2, enum option labels in `settings.definitions.yaml` can be
localized via `labels.xlf`.

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

TYPO3 derives the key automatically as
`settings.{settingKey}.enum.{enumValue}`:

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

---

## Source vs Target

- `<source>` is the single source of truth — never modify it in translation
  files
- `<source>` must be identical in all language files
- Only `<target>` contains translated content
- Missing `<target>` values use `<source>` as fallback (TYPO3 handles this
  automatically)

---

## HTML in XLIFF

HTML must be wrapped in CDATA. Never use raw HTML inside `<source>` or
`<target>`.

```xml
<!-- Correct -->
<source><![CDATA[Please <strong>confirm</strong> your email]]></source>
<target><![CDATA[Bitte <strong>bestätigen</strong> Sie Ihre E-Mail]]></target>

<!-- Wrong -->
<source>Please <strong>confirm</strong> your email
</source>
```

---

## Placeholders

Use `%1$s`, `%2$s` for ordered placeholders (sentence structure may differ
between languages).

```xml
<!-- Correct -->
<source>Hello %1$s, you have %2$s new messages.</source>
<target>Hallo %1$s, Sie haben %2$s neue Nachrichten.</target>

<!-- Wrong: unordered -->
<source>Hello {1}, you have {2} new messages.</source>

<!-- Wrong: sentence split across keys -->
<unit id="greeting.hello">
  <segment>
    <source>Hello</source>
  </segment>
</unit>
<unit id="greeting.messages">
  <segment>
    <source>you have new messages.</source>
  </segment>
</unit>
```

---

## TYPO3-specific notes

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

---

## Key lifecycle

- Keys are part of the public API once used in templates or code
- Do not rename or remove keys without migration
- Keys must be unique within a file
