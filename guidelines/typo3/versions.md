---
title: TYPO3 version validity
scope: typo3
applies_to: []
typo3: ["13", "14", "15"]
see_also: ["typo3/README.md", "typo3/integrator.md", "typo3/developer.md"]
---

# TYPO3 version validity

Which rule applies to which version, and where the rule itself lives. Read this
when unsure whether something still holds in the project's TYPO3 version.

This table covers rules that **changed between versions**. Rules that hold
everywhere are not listed — they carry no `**Validity:**` line in their
guideline file either.

## Integrator

| Topic | since | deprecated | removed | Rule in |
|---|---|---|---|---|
| SiteSets ([#103437](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.1/Feature-103437-IntroduceSiteSets.html)) | 13.1 | – | – | `integrator.md` |
| `settings.definitions.yaml` flat dot-notation | 13.4 | – | – | `integrator.md` |
| New CE Wizard via TCA ([#102834](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.0/Feature-102834-Auto-registrationOfNewContentElementWizardViaTCA.html)) | 13.0 | – | – | `integrator.md` |
| `<INCLUDE_TYPOSCRIPT:` → `@import` ([#105171](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.4/Deprecation-105171-INCLUDE_TYPOSCRIPTTypoScriptSyntax.html)) | – | 13.4 | 14.0 | `integrator.md` |

## Developer

| Topic | since | deprecated | removed | Rule in |
|---|---|---|---|---|
| `'type' => 'number'` in TCA | 12.0 | – | – | `developer.md` |
| `\PDO::PARAM_INT` → `ParameterType` | – | – | 13.0 | `developer.md` |
| `Extbase\Mvc\View\AbstractView`, `Extbase\Mvc\View\ViewInterface` | – | – | 12.0 | `developer.md` |
| `StandaloneView`, `TemplateView`, `AbstractTemplateView` ([#104773](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.3/Deprecation-104773-CustomFluidViewsAndExtbase.html) → [#105377](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-105377-DeprecatedFunctionalityRemoved.html)) | – | 13.3 | 14.0 | `developer.md` |
| `ViewFactoryInterface` | 13.3 | – | – | `developer.md` |
| `record-transformation` DataProcessor ([#103783](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.2/Feature-103783-RecordTransformationDataProcessor.html)) | 13.2 | – | – | `developer.md` |
| `record-transformation` applied by `lib.contentElement` | 14.0 | – | – | `developer.md` |
| Fluid 5, union types in `f:argument` ([#108148](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-108148-UnionTypesForViewHelpers.html)) | 14.0 | – | – | `developer.md` |
| Fluid `.fluid.html` resolution ([#108166](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-108166-FluidFileExtensionAndTemplateResolving.html)) | 14.0 | – | – | `developer.md` |
| `showitem` shortform label references ([#107789](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-107789-CoreTCAAndUserSettingsShowitemStringsUseShortFormReferences.html)) | 14.0 | – | – | `developer.md` |
| FlexForm DS via `columnsOverrides` | 14.0 | – | – | `developer.md` |
| `ExtensionManagementUtility::addPiFlexFormValue()` ([#107047](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Deprecation-107047-ExtensionManagementUtilityaddPiFlexFormValue.html)) | – | 14.0 | announced 15.0 | `developer.md` |
| Extension title from `composer.json` ([#108304](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-108304-PopulateExtensionTitleFromComposerJson.html)) | 14.0 | – | – | `developer.md` |

## XLIFF

| Topic | since | deprecated | removed | Rule in |
|---|---|---|---|---|
| XLIFF 2.0 support ([#107710](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-107710-SupportForXLIFF2xTranslationFiles.html)) | 14.0 | – | – | `../xliff/README.md` |
| ICU MessageFormat for plurals ([#104546](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Feature-104546-SupportICUMessageFormatForPluralForms.html)) | 14.2 | – | – | `../xliff/README.md` |
| SiteSet `labels.xlf` automatic key resolution | 13.1 | – | – | `../xliff/typo3.md` |
| Enum label localization in site settings ([#106640](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Feature-106640-LocalizeEnumLabelsInSiteSettingsDefinitions.html)) | 14.2 | – | – | `../xliff/typo3.md` |

---

## Not verifiable from the changelog

One entry above has no changelog reference: the flat dot-notation format for
`settings.definitions.yaml`. It is established in practice and the nested form
is still read for backwards compatibility, but no core changelog entry documents
the switch. Treat the version as approximate.

## Keeping this table honest

Every row must be backed by a changelog entry, a verified core source location,
or an explicit note that it is neither. To check or extend it:

```bash
grep -ih 'sitesets\|103437' guidelines/typo3/changelog-index/v1*.tsv
```

See `skills/typo3-changelog-harvest/SKILL.md` for the index and how to query it.

## Looking ahead

`changelog-index/v15.tsv` holds the next major's entries, harvested from the
core's `main` branch and marked `provisional`. Use it to choose between two
approaches that both work today — not to write code for a version no project
runs yet.
