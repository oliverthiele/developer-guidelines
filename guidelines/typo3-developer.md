# TYPO3 Developer Guidelines

TYPO3 v13 conventions for extension development.

## Scope

This file applies to:

- PHP development
- TCA configuration
- Fluid (ViewHelpers, arguments)
- Database interaction

Do not use these rules for:

- TypoScript configuration
- SiteSets
- Integrator tasks

---

## TCA field types

Use current TYPO3 v13 TCA types — never deprecated helpers or legacy APIs.

| Use                       | Avoid                                  |
|---------------------------|----------------------------------------|
| `'type' => 'file'`        | `getFileFieldTCAConfig()`              |
| `'type' => 'passthrough'` | incorrect TCA definitions              |

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

## Doctrine DBAL v4

`\PDO::PARAM_INT` was removed in TYPO3 v13.

Always use Doctrine DBAL parameter types.

```php
$queryBuilder->expr()->eq(
    'uid',
    $queryBuilder->createNamedParameter($uid, \Doctrine\DBAL\ParameterType::INTEGER)
);
```

Rules:

- Always use Doctrine types
- Never use PDO constants

---

## Fluid

### Argument types (TYPO3 v13 / Fluid 4)

Union types are NOT supported.

```xml
<!-- Correct -->
<f:argument name="columns" type="integer"/>
<f:argument name="breakpoints" type="array"/>

<!-- Wrong -->
<f:argument name="columns" type="int|array"/>
```

Rules:

- Always use explicit types
- Use `mixed` only as a last resort
- Prefer multiple arguments over mixed typing

---

## General rules

- Follow PSR-12
- Use meaningful names
- Avoid magic values
- Prefer explicit typing
