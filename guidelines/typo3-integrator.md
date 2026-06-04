# TYPO3 Integrator Guidelines

TYPO3 conventions for integrators. Applies to all supported TYPO3 versions
unless a version-specific file states otherwise.

## Scope

- TypoScript
- SiteSets
- XLIFF usage in TYPO3 context
- Backend configuration

For PHP / TCA / Fluid conventions, see `typo3-developer.md`.

## Version-specific additions

| Version | File                      |
|---------|---------------------------|
| v13     | `typo3/v13/integrator.md` |

Load the file matching your project's TYPO3 version in addition to this one.

---

## TYPO3 translation usage

Always reference labels via `LLL:EXT:`:

```php
'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:my.key',
```

Rules:

- Never hardcode labels
- Always use XLIFF files
- Paths in `LLL:EXT:` must match the actual file path exactly
- The `original` attribute in XLIFF files must point to the English source file