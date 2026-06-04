# TYPO3 Developer Guidelines

TYPO3 conventions for extension development. Applies to all supported TYPO3
versions
unless a version-specific file states otherwise.

## Scope

- PHP development
- TCA configuration
- Fluid (ViewHelpers, arguments)
- Database interaction

For integrator conventions (SiteSets, TypoScript, labels.xlf), see
`typo3-integrator.md`.

## Version-specific additions

| Version | File                     |
|---------|--------------------------|
| v13     | `typo3/v13/developer.md` |

Load the file matching your project's TYPO3 version in addition to this one.

---

## TCA field types

Use current TCA types — never deprecated helpers or legacy APIs.

| Use                       | Avoid                                      |
|---------------------------|--------------------------------------------|
| `'type' => 'file'`        | `getFileFieldTCAConfig()`                  |
| `'type' => 'number'`      | `'type' => 'input'` with `'eval' => 'int'` |
| `'type' => 'passthrough'` | incorrect TCA definitions                  |

`'type' => 'number'` was introduced in TYPO3 v12. Never use `'eval' => 'int'` on
an input field for integer values — it is deprecated and a common AI-generation
error.

```php
// Correct — v12+
'sorting_value' => [
    'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:sorting_value',
    'config' => [
        'type' => 'number',
    ],
],

// Wrong
'sorting_value' => [
    'config' => [
        'type' => 'input',
        'eval' => 'int',
    ],
],
```

Rules:

- `'type' => 'passthrough'` only for fields already defined in `ext_tables.sql`
- passthrough fields must not be rendered in backend forms

### columnsOverrides — label and config overrides

Use `columnsOverrides` to change a label or partial config for a specific CType
without redeclaring the full field configuration:

```php
$GLOBALS['TCA']['tt_content']['types']['my_ctype']['columnsOverrides'] = [
    'header' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:my_ctype.header',
    ],
];
```

Do not copy the entire field `config` array just to change a label.

### showitem palette syntax

```php
// Correct
'showitem' => '--palette--;;headers, bodytext',

// Wrong
'showitem' => 'header, bodytext',
```

---

## Doctrine DBAL

`\PDO::PARAM_INT` was removed in TYPO3 v13. Use Doctrine DBAL parameter types in
all
projects running v13 or above.

```php
// Correct
$queryBuilder->expr()->eq(
    'uid',
    $queryBuilder->createNamedParameter($uid, \Doctrine\DBAL\ParameterType::INTEGER)
);

// Wrong — PDO constant removed in TYPO3 v13
$queryBuilder->createNamedParameter($uid, \PDO::PARAM_INT)
```

---

## Fluid: f:format.html

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
| `<f:format.html parseFuncTSPath="">{field}</f:format.html>` | **wrong — runtime error**          |

---

## General rules

- Follow PSR-12
- Use meaningful, unabbreviated names
- Avoid magic values
- Prefer explicit typing
