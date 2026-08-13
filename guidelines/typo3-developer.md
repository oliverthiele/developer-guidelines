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
| v14     | `typo3/v14/developer.md` |

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

## ExtensionScanner false positives — property/method naming

The TYPO3 ExtensionScanner matches property and method names lexically,
regardless of the actual class. A property or method we define ourselves can
accidentally collide with a name used by a since-removed/deprecated core API,
producing a "weak" match. Unlike PHPStan baselines, the ExtensionScanner has
no way to mark a finding as reviewed/dismissed — it resurfaces every time the
scan runs.

Avoid generic names for properties/methods we define ourselves when they
collide with a removed/deprecated core pattern:

| Avoid   | Collides with (removed TYPO3 v14)             | Prefer instead                     |
|---------|------------------------------------------------|-------------------------------------|
| `$config` | `TypoScriptFrontendController::$config`       | specific name, e.g. `$apiConfiguration` |
| `$data`   | `TypoScriptFrontendController::$data`         | specific name, e.g. `$articleData`  |
| `error()` (custom method we define) | any core class with a same-named removed method | specific name, e.g. `logError()`, `reportError()` |

This only applies to properties/methods **we name ourselves**. It does not
apply to calls on external interfaces we don't control — e.g.
`LoggerInterface::error()` (PSR-3) is the prescribed method name and must be
called as-is. The resulting scanner false positive there is unavoidable and
not worth working around.

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

---

## Version constraints — never guess the current minor version

Never assume a TYPO3 minor version by extrapolating a pattern from prior LTS
releases (e.g. v11.5, v12.4, v13.4 does **not** imply v14.4 exists or is the
target). Before writing `typo3/cms-core` in `composer.json` or `'typo3'` in
`ext_emconf.php`, verify the actual current minor version:

```bash
ddev composer show typo3/cms-core --available | grep "^versions"
```

or check https://get.typo3.org/. Ask the user if still unclear.

---

## General rules

- Follow PSR-12
- Use meaningful, unabbreviated names
- Avoid magic values
- Prefer explicit typing
