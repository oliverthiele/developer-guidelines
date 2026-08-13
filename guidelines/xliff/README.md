---
title: XLIFF format
scope: xliff
applies_to:
  - "**/Resources/Private/Language/*.xlf"
  - "**/Configuration/Sets/**/*.xlf"
typo3: ["13", "14"]
see_also: ["xliff/keys.md", "xliff/typo3.md"]
---

# XLIFF Guidelines

XLIFF file format conventions: versions, structure, attributes, ICU.

| Also here | |
|---|---|
| [keys.md](keys.md) | key naming conventions and key lifecycle |
| [typo3.md](typo3.md) | how TYPO3 loads XLIFF: `LLL:` references, SiteSet `labels.xlf`, enum labels |

## Version selection

| TYPO3 support          | XLIFF version to use |
|------------------------|----------------------|
| v13 only, or v13 + v14 | **1.2**              |
| v14+ only              | **2.0**              |

**Validity:** XLIFF 2.0 support since 14.0
([#107710](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-107710-SupportForXLIFF2xTranslationFiles.html))
· ICU message format since 14.2

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

**Validity:** since 14.0 — use for extensions that target TYPO3 v14+ only

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

## ICU message format

**Validity:** since 14.2 ·
[#104546](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Feature-104546-SupportICUMessageFormatForPluralForms.html)
· XLIFF 2.0 files only

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
