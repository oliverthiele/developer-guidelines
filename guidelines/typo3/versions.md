---
title: TYPO3 version validity
scope: typo3
applies_to: []
typo3: ["13", "14", "15"]
see_also: ["typo3/README.md", "typo3/integrator.md", "typo3/developer.md"]
---

# TYPO3 version validity

Which rule applies to which TYPO3 version, and where the rule itself lives. Read
this when unsure whether something still holds in the project's TYPO3 version.

**Major versions only.** Live sites are updated at LTS releases, so every site
runs the latest minor of its major — a rule that arrived in 13.1 and one that
arrived in 13.4 are equally available in a v13 project. The minor version
changes no decision and is therefore not carried here. Where it is ever needed,
it sits in column 3 of the changelog index, one `grep` away.

Only rules that **changed between majors** are listed. Rules that hold
everywhere carry no `**Validity:**` line in their guideline file either.

## Integrator

| Topic | v13 | v14 | Rule in |
|---|---|---|---|
| SiteSets ([#103437](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.1/Feature-103437-IntroduceSiteSets.html)) | yes | yes | `integrator.md` |
| `settings.definitions.yaml` flat dot-notation | yes | yes | `integrator.md` |
| New CE Wizard via TCA ([#102834](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.0/Feature-102834-Auto-registrationOfNewContentElementWizardViaTCA.html)) | yes | yes | `integrator.md` |
| `<INCLUDE_TYPOSCRIPT:` ([#105171](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.4/Deprecation-105171-INCLUDE_TYPOSCRIPTTypoScriptSyntax.html)) | deprecated | **removed** | `integrator.md` |

## Developer

| Topic | v13 | v14 | Rule in |
|---|---|---|---|
| `'type' => 'number'` in TCA | yes | yes | `developer.md` |
| `\PDO::PARAM_INT` | **removed** | removed | `developer.md` |
| `Extbase\Mvc\View\AbstractView`, `Extbase\Mvc\View\ViewInterface` | removed | removed | `developer.md` |
| `StandaloneView`, `TemplateView`, `AbstractTemplateView` ([#104773](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.3/Deprecation-104773-CustomFluidViewsAndExtbase.html) → [#105377](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-105377-DeprecatedFunctionalityRemoved.html)) | deprecated | **removed** | `developer.md` |
| `ViewFactoryInterface` | yes | yes | `developer.md` |
| `record-transformation` usable in practice | no | **yes** | `developer.md` |
| Union types in `f:argument` ([#108148](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-108148-UnionTypesForViewHelpers.html)) | no | **yes** | `developer.md` |
| Fluid `.fluid.html` resolution ([#108166](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-108166-FluidFileExtensionAndTemplateResolving.html)) | no | **yes** | `developer.md` |
| `showitem` shortform label references ([#107789](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-107789-CoreTCAAndUserSettingsShowitemStringsUseShortFormReferences.html)) | no | **yes** | `developer.md` |
| FlexForm DS via `columnsOverrides` | no — pointer key | **yes — required** | `developer.md` |
| `ExtensionManagementUtility::addPiFlexFormValue()` ([#107047](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Deprecation-107047-ExtensionManagementUtilityaddPiFlexFormValue.html)) | yes | deprecated, removal announced for v15 | `developer.md` |
| Extension title from `composer.json` ([#108304](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-108304-PopulateExtensionTitleFromComposerJson.html)) | no | **yes** | `developer.md` |

## XLIFF

| Topic | v13 | v14 | Rule in |
|---|---|---|---|
| XLIFF 2.0 support ([#107710](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-107710-SupportForXLIFF2xTranslationFiles.html)) | no — use 1.2 | **yes** | `../xliff/README.md` |
| ICU MessageFormat for plurals ([#104546](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Feature-104546-SupportICUMessageFormatForPluralForms.html)) | no | **yes** | `../xliff/README.md` |
| XLIFF whitespace follows `xml:space` ([#70867](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Important-70867-XLIFFWhitespaceHandlingNowRespectsXmlSpaceAttribute.html)) | no — raw whitespace kept | **yes — collapsed** | `../xliff/README.md` |
| SiteSet `labels.xlf` automatic key resolution | yes | yes | `../xliff/typo3.md` |
| Enum label localization in site settings ([#106640](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Feature-106640-LocalizeEnumLabelsInSiteSettingsDefinitions.html)) | no | **yes** | `../xliff/typo3.md` |

---

## Date it by usability, not by first appearance

A row says when something became usable **in practice**, not when the API first
landed in the core. `record-transformation` is the example: the DataProcessor
exists in v13, but only v14 applies it automatically and ships the surrounding
record handling that makes it worth using. Listing it as a v13 feature would be
technically accurate and practically misleading.

## Keeping this table honest

Every row must be backed by a changelog entry or a verified core source
location. To check or extend it:

```bash
grep -ih 'sitesets\|103437' guidelines/typo3/changelog-index/v1*.tsv
```

See `skills/typo3-changelog-harvest/SKILL.md` for the index and how to query it.

## Looking ahead

`changelog-index/v15.tsv` holds the next major's entries, harvested from the
core's `main` branch and marked `provisional`. Use it to choose between two
approaches that both work today — not to write code for a version no project
runs yet.
