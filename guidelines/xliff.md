# XLIFF Guidelines

XLIFF 1.2 format conventions for TYPO3 extensions.

These rules are mandatory unless explicitly overridden.

## File naming

| File                  | Purpose                                       |
|-----------------------|-----------------------------------------------|
| `locallang.xlf`       | Source language (English)                     |
| `de.locallang.xlf`    | German translation                            |
| `locallang_db.xlf`    | TCA labels (field labels, select items, etc.) |
| `de.locallang_db.xlf` | German translation of TCA labels              |

Prefix pattern for translations: `{language-code}.{source-filename}.xlf`

## Formatting

Defined in `.editorconfig` — PhpStorm applies this automatically.

| Setting                | Value   |
|------------------------|---------|
| `indent_style`         | `tab`   |
| `indent_size`          | `4`     |
| `charset`              | `utf-8` |
| `end_of_line`          | `lf`    |
| `insert_final_newline` | `true`  |

Additional formatting rules:

- Do not add blank lines between `<trans-unit>` elements  
  → Only use blank lines when grouping with XML comments (e.g. `<!-- Navigation -->`)
- Keep `<source>` and `<target>` on a single line whenever possible  
  → Improves side-by-side comparison in IDEs (e.g. PhpStorm)
- Only use line breaks when content explicitly requires it  
  → e.g. formatted emails, multiline text, or structured content
- Do not introduce line breaks for visual formatting only
- Treat whitespace as meaningful content
- Do not add or remove spaces inside `<source>` or `<target>` unless intentional
  → Includes leading and trailing spaces
- Ensure whitespace is identical between `<source>` and `<target>` when required for correct rendering
- Use normal spaces by default — do not replace them with `&nbsp;`
- Only use `&nbsp;` when a non-breaking space is explicitly required in the UI
- Do not mix normal spaces and `&nbsp;` inconsistently across translations

## Source file structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2">
    <file source-language="en" datatype="plaintext"
          original="EXT:my_extension/Resources/Private/Language/locallang.xlf"
          product-name="my-extension">
        <body>
            <trans-unit id="my.key" resname="my.key">
                <source>My label</source>
            </trans-unit>
        </body>
    </file>
</xliff>
```

### `<file>` attributes

| Attribute         | Value                                                  | Notes                                                                |
|-------------------|--------------------------------------------------------|----------------------------------------------------------------------|
| `source-language` | `en`                                                   | Always English as source                                             |
| `datatype`        | `plaintext`                                            | Always `plaintext`                                                   |
| `original`        | `EXT:ext_key/Resources/Private/Language/locallang.xlf` | Use `EXT:` prefix, underscore extension key                          |
| `product-name`    | `my-extension`                                         | Hyphen-separated package name (matches composer package name suffix) |

### `<trans-unit>` attributes (source file)

| Attribute  | Required | Value                                  |
|------------|----------|----------------------------------------|
| `id`       | yes      | dot-separated key, e.g. `plugin.title` |
| `resname`  | yes      | identical to `id`                      |
| `approved` | **no**   | not used in source files               |

## Translation file structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2">
    <file source-language="en" target-language="de" datatype="plaintext"
          original="EXT:my_extension/Resources/Private/Language/locallang.xlf"
          product-name="my-extension">
        <body>
            <trans-unit id="my.key" resname="my.key" approved="yes">
                <source>My label</source>
                <target>Meine Beschriftung</target>
            </trans-unit>
        </body>
    </file>
</xliff>
```

### Differences from source file

- `target-language` attribute is added to `<file>` (e.g. `de`)
- `<target>` element is added to each `<trans-unit>`
- `approved="yes"` is added to each translated `<trans-unit>`
- `original` points to the **source** file (not the translation file itself)

### `<trans-unit>` attributes (translation file)

| Attribute  | Required | Value                                                |
|------------|----------|------------------------------------------------------|
| `id`       | yes      | identical to source file                             |
| `resname`  | yes      | identical to `id`                                    |
| `approved` | yes      | `"yes"` — only in translation files, never in source |

## Source vs Target

- `<source>` is the single source of truth
- `<source>` must never be modified in translation files
- `<source>` must be identical across all language files
- Only `<target>` contains translated content

## Key naming conventions

- Dot-separated, lowercase, descriptive
- Group by context: `plugin.title`, `plugin.description`, `field.label`, `error.notFound`
- TCA field labels: `{tablename}.{fieldname}`, e.g. `tx_myext_domain_model_product.title`
- Plugin labels: `plugin.{pluginname}.title`, `plugin.{pluginname}.description`
- Keys must remain stable once published
- Do not rename keys without migration or fallback handling
- Keys must be unique within a file
- Avoid duplicate keys across files unless intentionally shared

## Ordering

- Keep `<trans-unit>` elements sorted logically by feature or context
- Do not reorder keys unnecessarily
- Add new keys at the correct logical position

## Grouping

Use XML comments to group related keys when useful.

```xml
<!-- Navigation -->
<trans-unit id="navigation.home" resname="navigation.home">
    <source>Home</source>
</trans-unit>
```

Rules:

- Group by feature or UI context
- Do not overuse grouping
- Keep groups stable

## TYPO3-specific notes

- The `original` attribute is used by TYPO3 to resolve the fallback chain —
  always point it to the English source file, even in translation files
- TYPO3 reads translations via `LLL:EXT:...` references; the path in `original`
  must match the actual file path exactly
- TCA `label` values use the `LLL:EXT:...` prefix:
  ```php
  'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:my.key',
  ```
- `resname` must always match `id`
- TYPO3 internally relies on `resname`, not only `id`
- Do not mix UI labels and TCA labels in the same file
- Use `locallang_db.xlf` strictly for TCA labels
- Never hardcode labels in TCA, Fluid, or PHP — always use LLL references

## HTML in XLIFF

- HTML must be wrapped in CDATA
- CDATA must be used whenever HTML is present
- Do not use raw HTML inside <source> or <target> without CDATA
- Keep HTML identical between source and target
- Do not change structure or tags in translations

Correct:

```xml
<source><![CDATA[Please <strong>confirm</strong> your email]]></source>
<target><![CDATA[Bitte <strong>bestätigen</strong> Sie Ihre E-Mail]]></target>
```

Wrong — no CDATA:

```xml
<source>Please <strong>confirm</strong> your email</source>
```

## Placeholders

- Preserve placeholders exactly as defined in `<source>`
- Do not reorder placeholders unless explicitly required by grammar
- Use ordered placeholders such as `%1$s`, `%2$s` when sentence structure may differ between languages
- Do not use `{1}`, `{2}`
- Prefer full sentences instead of splitting into multiple keys

Correct:

```xml
<source>Hello %1$s, you have %2$s new messages.</source>
<target>Hallo %1$s, Sie haben %2$s neue Nachrichten.</target>
```

Wrong:

```xml
<source>Hello {1}, you have {2} new messages.</source>
```

Wrong — sentence split across multiple keys:

```xml
<trans-unit id="greeting.part1" resname="greeting.part1">
    <source>Hello</source>
</trans-unit>
<trans-unit id="greeting.part2" resname="greeting.part2">
    <source>you have new messages.</source>
</trans-unit>
```

## Whitespace and encoding

- Do not add leading or trailing spaces inside `<source>` or `<target>`
- Preserve intentional spaces exactly
- Use UTF-8 characters directly
- Do not replace normal UTF-8 text with unnecessary HTML entities

## Rules for adding new translations

- Always create a key — never inline text in PHP, Fluid, or JavaScript
- All user-facing text must be translatable via XLIFF

## Key lifecycle

- Keys are part of a public API once used in templates or code
- Do not rename or remove keys without migration
- Deprecated keys must remain until all references are removed

## Fallback behavior

- TYPO3 falls back from translation file to source file automatically
- Missing `<target>` values use `<source>` as fallback
