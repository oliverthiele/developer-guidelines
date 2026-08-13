---
title: XLIFF key naming
scope: xliff
applies_to:
  - "**/Resources/Private/Language/*.xlf"
  - "**/Configuration/Sets/**/*.xlf"
typo3: ["13", "14"]
see_also: ["xliff/README.md", "xliff/typo3.md"]
---

# XLIFF Key Naming

Key conventions and key lifecycle. For the file format itself see
[README.md](README.md), for TYPO3-specific label files see [typo3.md](typo3.md).

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
mirror TYPO3 database identifiers. The underscore is part of the identifier, not
a separator within the key segment.

**Anti-patterns — never use:**

```
current-job-offers      ← hyphens as separator
tx_myext_published_on   ← underscores as separator (TCA exception does not apply here)
applicationByEmail      ← no namespace, missing dot
PublishedOn             ← PascalCase
```

## Key lifecycle

- Keys are part of the public API once used in templates or code
- Do not rename or remove keys without migration
- Keys must be unique within a file
