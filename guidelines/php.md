# PHP Guidelines

PHP coding conventions for all TYPO3 projects.
These rules are mandatory unless explicitly overridden.

---

## Core Principles

- Always use strict typing
- Prefer explicit, readable code over clever shortcuts
- Avoid unnecessary abstractions
- Keep logic simple and predictable

---

## Formatting

Defined in `.editorconfig` — PhpStorm applies this automatically:

| Setting                | Value   |
|------------------------|---------|
| `indent_style`         | `space` |
| `indent_size`          | `4`     |
| `charset`              | `utf-8` |
| `end_of_line`          | `lf`    |
| `insert_final_newline` | `true`  |

Code style is enforced by **TYPO3 Coding Standards** via PHP CS Fixer.

---

## Commands

### Execution Order

1. PHPStan
2. PHP CS Fixer

Both must pass before committing changes.

If any step fails:

- stop execution immediately
- fix the issue before continuing
- do not run subsequent steps

---

### Composer Scripts First

Always prefer project-defined Composer scripts over direct binary calls.

Reasons:

- configuration is versioned in Git
- ensures consistent execution across developers
- avoids hardcoded paths or parameters

Use direct binary calls only if no Composer script exists.

---

### PHP CS Fixer

- Required before every commit
- Mode: fix (not dry-run)

Preferred:

```bash
ddev composer php-cs-fixer
```

Fallback:

```bash
ddev exec vendor/bin/php-cs-fixer fix
```

### Required configuration

Every project that uses both PHP CS Fixer and PHP CodeSniffer must override
`single_line_empty_body` in `.php-cs-fixer.dist.php`:

```php
$config->setRules(array_merge(
    $config->getRules(),
    [
        // Prevents CS Fixer from collapsing empty constructors/methods/classes.
        // Without this, CS Fixer and CodeSniffer conflict on every empty body.
        'single_line_empty_body' => false,
    ]
));
```

Without this override, CS Fixer collapses empty methods to a single line and
CodeSniffer immediately flags the result — the tools loop endlessly.

---

### PHPStan

- Required before commit
- Must pass without errors

Preferred:

```bash
ddev composer phpstan
```

Fallback:

```bash
ddev exec vendor/bin/phpstan analyse
```

---

### Targeted Run

Use for package-specific changes:

```bash
ddev exec vendor/bin/phpstan analyse packages/{package-name}/Classes
```

Prefer package-specific Composer scripts if available.

---

## Naming Conventions

- **No abbreviated variable names** — always write them out in full
- Classes: `PascalCase`
- Methods and variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Private properties: no underscore prefix

---

## File Header

Every PHP file must start with:

```php
<?php

declare(strict_types=1);
```

---

## Decision Rules

- Prefer minimal changes over refactoring
- Do not introduce helpers for one-time use
- Preserve existing structure and comments

---

## Do

- Use explicit type checks
- Use multi-step narrowing for mixed values
- Use typed closures instead of string callbacks
- Use helper methods for repeated typed access

---

## Don't

- Do not cast mixed values directly
- Do not use string callbacks like `'intval'`
- Do not weaken type safety
- Do not introduce unnecessary abstractions
- Do not rename existing variables or methods without clear necessity

---

## PHPStan Configuration

Project-wide level is defined in `phpstan.neon` at the project root.  
Standalone Packagist packages use their own `phpstan.neon.dist`.

| Context            | Level | Config                             |
|--------------------|-------|------------------------------------|
| Project (monorepo) | 8     | `phpstan.neon`                     |
| Standalone package | 9     | `phpstan.neon.dist` in the package |

---

## PHPStan Level 9 Patterns

`$GLOBALS` is typed as `array<string, mixed>` — always use multi-step narrowing:

```php
/** @return array<string, mixed> */
private function getTcaCtrl(string $tableName): array
{
    $tca = $GLOBALS['TCA'] ?? null;
    if (!is_array($tca)) {
        return [];
    }
    $table = $tca[$tableName] ?? null;
    if (!is_array($table)) {
        return [];
    }
    $ctrl = $table['ctrl'] ?? null;
    return is_array($ctrl) ? $ctrl : [];
}
```

---

### Typed DB Access

Never cast `mixed` directly:

```php
private function rowString(array $row, string $field, string $default = ''): string
{
    $value = $row[$field] ?? null;
    return is_scalar($value) ? (string)$value : $default;
}

private function rowInt(array $row, string $field, int $default = 0): int
{
    $value = $row[$field] ?? null;
    return is_numeric($value) ? (int)$value : $default;
}
```

---

### array_map with mixed

```php
// Wrong:
array_map('intval', $mixedArray)

// Correct:
array_map(fn(mixed $value): int => is_numeric($value) ? (int)$value : 0, $mixedArray)
```

---

### Type Narrowing Annotation

```php
if (is_array($overlayedRow[0])) {
    /** @var array<string, mixed> $translatedRow */
    $translatedRow = $overlayedRow[0];
}
```

---

## General Rules

- Comments in **English only**
- No docblocks on obvious methods — only where logic is not self-evident
- Trust framework guarantees — do not guard impossible states
- No backwards-compatibility shims for removed code