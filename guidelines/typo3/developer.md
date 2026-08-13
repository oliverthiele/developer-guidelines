---
title: TYPO3 Developer
scope: typo3
applies_to:
  - "**/Classes/**/*.php"
  - "**/Configuration/TCA/**/*.php"
  - "**/Resources/Private/**/*.html"
  - "**/ext_localconf.php"
  - "**/ext_tables.php"
typo3: ["13", "14"]
see_also: ["typo3/integrator.md", "typo3/versions.md", "php.md"]
---

# TYPO3 Developer Guidelines

TYPO3 conventions for extension development: PHP, TCA, Fluid, database access.

For integrator conventions (SiteSets, TypoScript, backend configuration), see
`integrator.md`.

Every rule below states the versions it applies to. A rule without a
`**Validity:**` line holds for all supported versions. See `versions.md` for the
full table and `README.md` for how the version model works.

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

### showitem — shortform label references

**Validity:** v14+ ·
[#107789](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-107789-CoreTCAAndUserSettingsShowitemStringsUseShortFormReferences.html)
· longform still valid in v14, required in v13

```php
// v14 — shortform
'--div--;core.form.tabs:access'

// v13 and v14 — longform
'--div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access'
```

Do not use shortform in extensions that still support v13.

---

## FlexForm data structure registration

**Validity:** `columnsOverrides` required in v14 · pointer-key approach
required in v13 · `ExtensionManagementUtility::addPiFlexFormValue()` deprecated
in v14 ([#107047](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Deprecation-107047-ExtensionManagementUtilityaddPiFlexFormValue.html)),
removal announced for v15

```php
// v14 — correct
$GLOBALS['TCA']['tt_content']['types']['my_ctype']['columnsOverrides']['pi_flexform']['config']['ds']
    = 'FILE:EXT:my_ext/Configuration/FlexForm/FlexForm.xml';

// v13 — pointer-key approach
$GLOBALS['TCA']['tt_content']['columns']['pi_flexform']['config']['ds']['*,my_ctype']
    = 'FILE:EXT:my_ext/Configuration/FlexForm/FlexForm.xml';
```

`addPiFlexFormValue()` internally uses `columnsOverrides` — use that directly
instead.

For extensions that must support both v13 and v14, use a version check:

```php
use TYPO3\CMS\Core\Information\Typo3Version;

if ((new Typo3Version())->getMajorVersion() >= 14) {
    $GLOBALS['TCA']['tt_content']['types']['my_ctype']['columnsOverrides']['pi_flexform']['config']['ds']
        = 'FILE:EXT:my_ext/Configuration/FlexForm/FlexForm.xml';
} else {
    $GLOBALS['TCA']['tt_content']['columns']['pi_flexform']['config']['ds']['*,my_ctype']
        = 'FILE:EXT:my_ext/Configuration/FlexForm/FlexForm.xml';
}
```

---

## Doctrine DBAL

**Validity:** `\PDO::PARAM_INT` removed in v13

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

## Views — never instantiate a view directly

**Validity:** `Extbase\Mvc\View\AbstractView` and `Extbase\Mvc\View\ViewInterface`
removed in v12 · `StandaloneView`, `TemplateView`, `AbstractTemplateView`
deprecated in v13 ([#104773](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.3/Deprecation-104773-CustomFluidViewsAndExtbase.html)),
removed in v14 ([#105377](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-105377-DeprecatedFunctionalityRemoved.html))

> **Stale-knowledge trap:** `GeneralUtility::makeInstance(StandaloneView::class)`
> is the single most common way to build a view in older code and training data.
> It is gone in v14. The ExtensionScanner reports it as a *strong* match.

Inject `ViewFactoryInterface` and call `create()`:

```php
use TYPO3\CMS\Core\View\ViewFactoryInterface;
use TYPO3\CMS\Core\View\ViewFactoryData;

public function __construct(
    private readonly ViewFactoryInterface $viewFactory,
) {}

$view = $this->viewFactory->create(new ViewFactoryData(
    templatePathAndFilename: 'EXT:my_ext/Resources/Private/Templates/Mail.html',
));
```

Template paths belong in `ViewFactoryData`, not in setter calls afterwards.

For a custom view class, implement `TYPO3\CMS\Core\View\ViewInterface`
(namespace `Core\View`, **not** Extbase):

```php
use TYPO3\CMS\Core\View\ViewInterface;

class MyCustomView implements ViewInterface
{
    protected array $variables = [];

    public function assign(string $key, mixed $value): self
    {
        $this->variables[$key] = $value;
        return $this;
    }

    public function assignMultiple(array $values): self
    {
        foreach ($values as $key => $value) {
            $this->assign($key, $value);
        }
        return $this;
    }

    public function render(string $templateFileName = ''): string
    {
        // access assigned variables via $this->variables
    }
}
```

Key details:

- Return type of `assign()`/`assignMultiple()` is `self`, not `static`
- `render()` signature is `render(string $templateFileName = ''): string`
- `$this->variables` must be declared explicitly — it is not inherited

---

## Fluid — argument types

**Validity:** union types in v14+ (Fluid 5) ·
[#108148](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-108148-UnionTypesForViewHelpers.html)
· not supported in v13 (Fluid 4)

```xml
<!-- v14 / Fluid 5 -->
<f:argument name="columns" type="int|array"/>

<!-- v13 / Fluid 4 — one explicit type per argument -->
<f:argument name="columns" type="integer"/>
<f:argument name="breakpoints" type="array"/>
```

In Fluid 4 a union type causes `Cannot cast an array to string` at runtime.
Where multiple types are needed there: use separate arguments, or `type="mixed"`
as a last resort.

---

## Fluid — `f:format.html`

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

## Fluid — template file resolution `.fluid.html`

**Validity:** v14+ ·
[#108166](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-108166-FluidFileExtensionAndTemplateResolving.html)

Fluid 5 natively resolves `{Name}.fluid.{format}` before `{Name}.{format}` for
Templates, Partials and Layouts — see `TemplatePaths::resolveFileInPaths()` in
`typo3fluid/fluid`. No TypoScript or `view.format` configuration is needed.

Prefer naming Fluid template files `*.fluid.html` (e.g. `Default.fluid.html`) in
v14-only extensions — this is the project convention going forward and gives
IDEs unambiguous syntax highlighting for Fluid vs. plain HTML.

---

## `record-transformation` — applied by default in v14

**Validity:** v14+ — verified in
`EXT:fluid_styled_content/Configuration/TypoScript/Helper/ContentElement.typoscript`
(present in v14, absent in v13)

The DataProcessor itself already exists in v13
([#103783](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.2/Feature-103783-RecordTransformationDataProcessor.html)),
but registering it manually there does not give the v13 project what v14
provides: the automatic application plus the surrounding record handling
(`f:render.contentArea` and friends) is what makes it practical. Treat this as a
v14 feature.

```typoscript
# v14 — part of lib.contentElement out of the box
lib.contentElement {
    dataProcessing {
        1770716912 = record-transformation
    }
}
```

Every content element extending `lib.contentElement` therefore gets a `{record}`
variable in Fluid — a `TYPO3\CMS\Core\Domain\Record` object with type-aware
direct property access (`{record.header}`, `{record.uid}`), independent of the
extension's own TypoScript.

For a TCA field of `type => inline` (IRRE/foreign-table relation),
`record-transformation` **resolves the relation automatically** into a
`LazyRecordCollection` of `Record` objects, with the same direct property access
on each child. A manual `database-query` DataProcessor is not needed for this
case.

```html
<!-- No custom dataProcessing needed in TypoScript for this -->
<f:for each="{record.countup_items}" as="item">
    {item.title}: {item.value_end}
</f:for>
```

Caveats:

- Only fields defined in the TCA `columns` for the record's current `type` are
  exposed. A field outside the current type is only reachable via
  `{record.rawRecord}` (untransformed).
- The `Record` API was still marked "to be finalized" in the v13 changelog.
  Treat it as stable enough for v14-only extensions, but verify behaviour for
  field types beyond scalars and `inline` (e.g. `select` with `foreign_table`,
  `category`) before relying on automatic resolution there.

---

## Extension title comes from `composer.json`

**Validity:** v14+ ·
[#108304](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-108304-PopulateExtensionTitleFromComposerJson.html)

The extension title shown in the Extension Manager is derived from
`description` in `composer.json`. The `title` and `description` keys in
`ext_emconf.php` are no longer read automatically.

The core splits on the **first** occurrence of ` - ` (space, dash, space):

```php
// TYPO3\CMS\Core\Package\Package::createPackageMetaData()
$descriptionParts = explode(' - ', $description ?? '', 2);
```

- everything before it becomes the **title**
- the remainder becomes the **description**
- without the separator the whole string is used as the title — that is what
  looks like a missing title in the Extension Manager

```json
// composer.json
"description": "Gallery - Gallery extension for TYPO3 v14."
```

```php
// ext_emconf.php — separate 'title' key, description without the prefix
'title' => 'Gallery',
'description' => 'Gallery extension for TYPO3 v14.',
```

Rules:

- The separator is exactly ` - `. An en dash (` – `) or a hyphen without
  surrounding spaces does not match.
- Only the first occurrence is evaluated, so ` - ` may still appear later inside
  the description text.
- Avoid ` - ` inside the title itself — it would be split at the wrong place.
- Keep `ext_emconf.php` consistent anyway: it is still evaluated in non-Composer
  installations, and its `description` must stay **without** the title prefix,
  otherwise the title appears twice there.

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

When a scanner finding names a changelog number, look it up in the changelog
index instead of guessing the migration — see
`skills/typo3-changelog-harvest/SKILL.md`.

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
