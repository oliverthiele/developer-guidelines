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

| Use                       | Avoid                     |
|---------------------------|---------------------------|
| `'type' => 'file'`        | `getFileFieldTCAConfig()` |
| `'type' => 'passthrough'` | incorrect TCA definitions |

Rules:

- `'type' => 'passthrough'` only for fields already defined in `ext_tables.sql`
- passthrough fields must not be rendered in backend forms

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
