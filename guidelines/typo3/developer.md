---
title: TYPO3 Developer
scope: typo3
applies_to:
    - "**/Classes/**/*.php"
    - "**/Configuration/TCA/**/*.php"
    - "**/ext_localconf.php"
    - "**/ext_tables.php"
typo3: [ "13", "14" ]
see_also: [ "typo3/integrator.md", "typo3/versions.md", "fluid/typo3.md", "php.md" ]
---

# TYPO3 Developer Guidelines

TYPO3 conventions for extension development: PHP, TCA, database access.

For integrator conventions (SiteSets, TypoScript, backend configuration), see
`integrator.md`. For Fluid templates, see [`../fluid/`](../fluid/README.md).

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

### System columns come from `ctrl` — do not write them by hand

**Validity:** v13.3+ ·
[#104311](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.3/Feature-104311-AutoCreatedSystemTCAColumns.html)

A `ctrl` entry creates the matching `columns` definition: `languageField`,
`transOrigPointerField`, `transOrigDiffSourceField`, `enablecolumns`,
`descriptionColumn`, `editlock`. Extensions can drop that boilerplate — keeping
a hand-written copy means maintaining a definition the core already ships.

`columns` definitions do **not** make a table language aware; `ctrl` does. When
only `languageField` is set, the core adds `transOrigPointerField` on its own.
Whether a table should be language aware at all is a design decision — see
[`practices/record-languages.md`](practices/record-languages.md).

The core does not add the fields to `types` or `palettes`. Placing them in
`showitem`, and setting the access permissions, stays with the extension.

The database side follows the same route: columns are created from the TCA
definition since v13
([#101553](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.0/Feature-101553-Auto-createDBFieldsFromTCAColumns.html)),
so `ext_tables.sql` only needs what TCA does not describe. A column that loses
its TCA definition is no longer managed, and the schema compare offers to drop
it — a separate decision from removing the definition.

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
[#107789](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-107789-CoreTCATabLabelsUseShortFormReferences.html)
· longform still valid in v14, required in v13

```php
// v14 — shortform
'--div--;core.form.tabs:access'

// v13 and v14 — longform
'--div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access'
```

Do not use shortform in extensions that still support v13.

### `cropVariants` — every variant needs a `cropArea`

**Validity:** reproduced on v14 · not checked on v13

```php
'cropVariants' => [
    'free' => [
        'title' => 'Free',
        'cropArea' => ['x' => 0, 'y' => 0, 'width' => 1, 'height' => 1],
        'allowedAspectRatios' => [
            'free' => ['title' => 'Free', 'value' => 0.0],
        ],
    ],
],
```

The image manipulation element fills in a missing `cropArea`, so the mistake is
invisible where the configuration is usually checked. The `OtherLanguageThumbnails`
field wizard does not: editing a **translated** record with an image raises
`Undefined array key "cropArea"` and shows no preview thumbnails.

---

## FlexForm data structure registration

**Validity:** `columnsOverrides` required in v14 · pointer-key approach required
in v13 · `ExtensionManagementUtility::addPiFlexFormValue()` deprecated in v14
([#107047](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Deprecation-107047-ExtensionManagementUtilityAddPiFlexFormValue.html)),
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

## Deleting and updating — use `QueryBuilder`, never `Connection`

**Validity:** all versions. This is an API-shape trap, not a version change.

`Connection::delete()` and `Connection::update()` take **types** as their last
argument, not further conditions:

```php
public function delete(string $tableName, array $identifier = [], array $types = []): int
public function update(string $tableName, array $data, array $identifier = [], array $types = []): int
```

And `expr()` sits on `QueryBuilder`, not on `Connection`. Code that mixes the
two up looks plausible and is silently catastrophic:

```php
// WRONG — three defects in five lines
$connection->delete(
    'fe_users',
    ['disable' => 1],                                  // the only real criterion
    [$connection->expr()->lt('token_expires', time())] // lands in $types, and
);                                                     // expr() does not exist here
```

`expr()` raises an `Error`, so the statement never runs. Repairing only that
error turns the query into "delete every disabled user" — the expression was
never part of the WHERE clause. The same shape with `update()` and an empty
`$identifier` produces an `UPDATE` across the whole table.

**Rules:**

1. Write deletions and updates through `QueryBuilder`, where a condition cannot
   end up in a parameter meant for something else.
2. Put the criteria in **one** private method that the counting path and the
   writing path share, so a dry run cannot diverge from the real run.
3. Guard against the column default. `int` columns default to `0` or `NULL`, so
   `expires < time()` matches every row that never carried a value. Require the
   column to be set as well.
4. For a cleanup that can delete a lot, add a count method and let the command's
   `--dry-run` report what it would remove. A `--dry-run` that only prints a
   warning and does nothing is worse than none: it looks like a safety net.

```php
// Correct
private function expiredConstraints(QueryBuilder $queryBuilder, int $maxAge): array
{
    return [
        $queryBuilder->expr()->eq('disable', $queryBuilder->createNamedParameter(1, Connection::PARAM_INT)),
        $queryBuilder->expr()->gt('token_expires', $queryBuilder->createNamedParameter(0, Connection::PARAM_INT)),
        $queryBuilder->expr()->lt('token_expires', $queryBuilder->createNamedParameter(time(), Connection::PARAM_INT)),
    ];
}
```

Whether a cleanup deletes hard or sets `deleted = 1` is a data protection
decision, not a habit. Records that exist to prove something once — an
unconfirmed registration, a verification code — have no basis for retention once
that purpose is spent, and a soft delete would keep the personal data
indefinitely. A record a person or editor may want back is the opposite case.

---

## `$GLOBALS['TSFE']` is gone — read request attributes

**Validity:** `TypoScriptFrontendController` deprecated in v13
([#105230](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.4/Deprecation-105230-TypoScriptFrontendControllerAndGLOBALSTSFE.html)),
removed in v14
([#107831](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-107831-RemovedTypoScriptFrontendController.html))
· members already internal or read-only in v13
([#102621](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.0/Breaking-102621-MostTSFEMembersMarkedInternalOrRead-only.html))

> **Stale-knowledge trap:** `$GLOBALS['TSFE']->id`, `->page`, `->fe_user` and
> friends appear in fifteen years of TYPO3 examples and dominate training data.
> The object does not exist in v14. Anything generated from memory here is
> wrong.

Frontend state is carried on the PSR-7 request as attributes:

```php
// Correct — v13 and v14
$pageInformation = $request->getAttribute('frontend.page.information');
$pageId = $pageInformation->getId();
$pageRecord = $pageInformation->getPageRecord();

$frontendUser = $request->getAttribute('frontend.user');
$typoScript = $request->getAttribute('frontend.typoscript');

// Wrong — removed in v14
$pageId = $GLOBALS['TSFE']->id;
$pageRecord = $GLOBALS['TSFE']->page;
```

Rules:

- Inject or pass the `ServerRequestInterface`; never reach for `$GLOBALS`
- In an EventListener, take the request from the event (`$event->getRequest()`)
  rather than from a global
- In Fluid, the data a template needs comes from the DataProcessor or the
  controller, not from a TSFE lookup in a ViewHelper

For the exact replacement of a specific member, look up
[#102621](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.0/Breaking-102621-MostTSFEMembersMarkedInternalOrRead-only.html)
in the changelog index — it lists every property with its substitution.

---

## Extbase and `fallbackType: strict` — untranslated records disappear

**Validity:** v14 **from 14.3.6**
([#88886](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.3.x/Important-88886-ExtbasePersistenceRespectsLanguageOverlayType.html))
· v13 and v14 up to 14.3.5 always overlay with "mixed" semantics · related:
`setIgnoreEnableFields()` now reveals hidden translations
([#100638](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.3.x/Important-100638-ExtbaseIgnoreEnableFieldsAppliesToTranslations.html))

> **Stale-knowledge trap:** up to 14.3.5, Extbase returned the default-language
> record whenever no translation existed, regardless of the site's
> `fallbackType`. Existing extensions and nearly every example rely on it. The
> change arrived in a patch release, classified as Important rather than
> Breaking, and no tool can see it: no signature changes, only results.
> `hideNonTranslated` is not a way back — it is the legacy name of
> `OVERLAYS_ON` and `OVERLAYS_ON_WITH_FLOATING`, the strict behaviour itself.
> `Typo3QuerySettings::setLanguageOverlayMode()` does not exist.

| `fallbackType` | Overlay type | Untranslated record in language 0 |
|---|---|---|
| `strict` | `OVERLAYS_ON_WITH_FLOATING` | **dropped** — aggregate roots and related objects |
| `fallback` | `OVERLAYS_MIXED` | default-language record, unchanged |
| `free` | `OVERLAYS_OFF` | no overlay; `findByUid()` still resolves with "mixed" semantics |

What `strict` does to relations on a translated page:

| Relation | Effect |
|---|---|
| 1:1 (`select`, value field) | property is `null` |
| 1:n, m:n, file references | items missing from the collection, no error |
| child of a parent **without** a language field | dropped as well — children are overlaid to the requested language |
| child of a parent with `sys_language_uid = -1` | dropped as well, unless the child is `-1` itself or translated |

Kept: records with `-1`, and translated records without a translation parent
("floating"). Records created through Extbase in the frontend are stored in
language `0` unless a language is assigned, and are therefore invisible in
strict languages until translated.

Rules:

1. **Nullable getters for 1:1 relations.** A required TCA field does not
   guarantee an object in every language.

   ```php
   // Correct
   protected ?Contact $contact = null;

   public function getContact(): ?Contact
   {
       return $this->contact;
   }

   // Wrong — TypeError on a translated page when the contact is not translated
   public function getContact(): Contact
   ```

   Guard the template block (`<f:if condition="{event.contact}">`) — as a
   consequence of the nullable getter, never as the fix. A guard alone renders
   the page without the record and reports nothing.
2. **No property validators on models that are only displayed.** A
   `#[Validate(validator: 'NotEmpty')]` on a relation of an object passed as
   action argument fails argument validation when the related record is dropped;
   the page answers HTTP 400. Validators belong on objects that are submitted.

   Where a validator does belong, put the attribute **on the parameter**, not on
   the method with an argument name — `#[Validate(param: …)]` and
   `#[IgnoreValidation(argumentName: …)]` are deprecated in v14 and stop working
   in v15
   ([#108227](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Deprecation-108227-UsageOfIgnoreValidationAndValidateAttributesForParametersAtMethodLevel.html)):

   ```php
   // Correct — v14
   public function updateAction(
       #[IgnoreValidation]
       Event $event,
       #[Validate(validator: 'NotEmpty')]
       string $comment,
   ): ResponseInterface {

   // Deprecated in v14, removed in v15
   #[IgnoreValidation(argumentName: 'event')]
   #[Validate(param: 'comment', validator: 'NotEmpty')]
   public function updateAction(Event $event, string $comment): ResponseInterface {
   ```

   Only the parameter-naming properties are affected. An attribute on the method
   that applies to the whole method, and `#[Validate]` on a model property, stay
   valid.
3. **Decide per table what the data is** — translate, `-1`, `0` with a fallback,
   or not language aware. See
   [`practices/record-languages.md`](practices/record-languages.md). Never
   restore "mixed" globally.
4. **Change languages through the backend or DataHandler, never with SQL.** A
   translation consists of `l10n_parent`, `l10n_source`, `l10n_state`, its own
   file references and the reference index; a partial SQL fix can make the
   frontend look right while the backend's localization view is broken.
5. **Third-party extensions:** do not patch them. Fix the data, or add a
   project-level listener. They may set their own `LanguageAspect`, so compare
   the rendered output per language instead of trusting the configuration.
6. **Test translated pages before updating to 14.3.6 or later** — see
   [`../testing.md`](../testing.md) → *Multilingual Sites*.

---

## Views — never instantiate a view directly

**Validity:** `Extbase\Mvc\View\AbstractView` and
`Extbase\Mvc\View\ViewInterface`
removed in v12 · `StandaloneView`, `TemplateView`, `AbstractTemplateView`
deprecated in v13
([#104773](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.3/Deprecation-104773-CustomFluidViewsAndExtbase.html)),
removed in v14
([#105377](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-105377-DeprecatedFunctionalityRemoved.html))

> **Stale-knowledge trap:**
> `GeneralUtility::makeInstance(StandaloneView::class)`
> is the single most common way to build a view in older code and training data.
> It is gone in v14. The ExtensionScanner reports it as a *strong* match.

Inject `ViewFactoryInterface` and call `create()`:

```php
use TYPO3\CMS\Core\View\ViewFactoryData;
use TYPO3\CMS\Core\View\ViewFactoryInterface;

public function __construct(
    private readonly ViewFactoryInterface $viewFactory,
) {}

$view = $this->viewFactory->create(new ViewFactoryData(
    templateRootPaths: ['EXT:my_ext/Resources/Private/Templates/'],
    partialRootPaths: ['EXT:my_ext/Resources/Private/Partials/'],
    layoutRootPaths: ['EXT:my_ext/Resources/Private/Layouts/'],
    request: $request,
));
$view->assign('order', $order);
$html = $view->render('Mail/OrderConfirmation');
```

Rules, taken from the best-practice block in `ViewFactoryData` itself (read in
core 14.3.7):

- **Root paths, not `templatePathAndFilename`.** The core names it as the thing
  to avoid. Root paths keep partials and layouts resolvable and let a project
  override the template by adding its own path to the array — a single file name
  cannot be overridden. Reserve `templatePathAndFilename` for a template that
  genuinely lives outside any root path structure.
- **`render()` takes the template name without extension**, relative to
  `templateRootPaths` — `'Mail/OrderConfirmation'`, not a path with `.html`.
- **Hand over the request** whenever the code has one. Core lists that first;
  ViewHelpers that need it read it from the rendering context. Code without a
  request — a CLI command, a scheduler task — passes none.
- Template paths belong in `ViewFactoryData`, not in setter calls afterwards.

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

## Fluid

Fluid rules live in [`../fluid/`](../fluid/README.md), not here — the engine is
its own package and also runs standalone.

| | |
|---|---|
| [../fluid/README.md](../fluid/README.md) | syntax, ViewHelper arguments, tag attributes, `.fluid.html` resolution |
| [../fluid/typo3.md](../fluid/typo3.md) | `f:format.html`, backend module `Module` layout, core ViewHelpers |

---

## `record-transformation` — applied by default in v14

**Validity:** available since v13.2
([#103783](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.2/Feature-103783-RecordTransformationDataProcessor.html)),
**recommended from v14**, where `lib.contentElement` applies it by default —
verified in
`EXT:fluid_styled_content/Configuration/TypoScript/Helper/ContentElement.typoscript`
(present in v14, absent in v13) · TCA values are transformed for record objects
since v13.3
([#103581](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.3/Feature-103581-AutomaticallyTransformTCAFieldValuesForRecordObjects.html))

The DataProcessor exists in v13 and can be registered manually there — the
recommendation is about practice, not availability. What v13 lacks is the
automatic application plus the surrounding record handling
(`f:render.contentArea` and friends), which is what makes it worth using. So:
usable in v13 if a project wants it, the default from v14 on.

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
producing a "weak" match. Unlike PHPStan baselines, the ExtensionScanner has no
way to mark a finding as reviewed/dismissed — it resurfaces every time the scan
runs.

Avoid generic names for properties/methods we define ourselves when they collide
with a removed/deprecated core pattern:

| Avoid                               | Collides with (removed TYPO3 v14)               | Prefer instead                                    |
|-------------------------------------|-------------------------------------------------|---------------------------------------------------|
| `$config`                           | `TypoScriptFrontendController::$config`         | specific name, e.g. `$apiConfiguration`           |
| `$data`                             | `TypoScriptFrontendController::$data`           | specific name, e.g. `$articleData`                |
| `error()` (custom method we define) | any core class with a same-named removed method | specific name, e.g. `logError()`, `reportError()` |

This only applies to properties/methods **we name ourselves**. It does not apply
to calls on external interfaces we don't control — e.g.
`LoggerInterface::error()` (PSR-3) is the prescribed method name and must be
called as-is. The resulting scanner false positive there is unavoidable and not
worth working around.

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
