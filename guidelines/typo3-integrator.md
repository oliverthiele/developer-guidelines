# TYPO3 Integrator Guidelines

TYPO3 v13 conventions for integrators.

## Scope

This file applies to:

- TypoScript
- SiteSets
- XLIFF usage in TYPO3 context
- Backend configuration

Do not use these rules for:

- PHP implementation
- TCA internals

---

## SiteSets

### File structure

Configuration/Sets/{SetName}/
config.yaml
settings.definitions.yaml
setup.typoscript
constants.typoscript

Resources/Private/Language/
labels.xlf
de.labels.xlf

---

## TypoScript in SiteSets

TypoScript is still used.

Rules:

- TypoScript is auto-included
- No manual include required
- Do not say "no TypoScript"

---

## labels.xlf key naming

| Key pattern                           | Purpose     |
|---------------------------------------|------------|
| settings.{vendor}.{key}               | label       |
| settings.description.{vendor}.{key}   | description |

Important:

TYPO3 expects:
settings.description.KEY

NOT:
settings.KEY.description

---

## TYPO3 translation usage

Always use:

LLL:EXT:my_extension/...:key

Rules:

- Never hardcode labels
- Always use XLIFF
- Paths must match exactly
