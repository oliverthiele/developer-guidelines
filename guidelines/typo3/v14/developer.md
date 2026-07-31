# TYPO3 v14 — Developer

Version-specific additions to `guidelines/typo3-developer.md` for TYPO3
v14 / Fluid 5.

---

## Fluid 5 — Argument types

Union types in `<f:argument>` are supported from Fluid 5 / TYPO3 v14 onwards.

```xml
<!-- Valid in TYPO3 v14 (Fluid 5) -->
<f:argument name="columns" type="int|array"/>

    <!-- In TYPO3 v13 (Fluid 4) this causes "Cannot cast an array to string" — use single types there -->
```

---

## FlexForm DS registration

In TYPO3 v14, the FlexForm data structure must be registered via
`columnsOverrides`, not via the pointer-key approach on `columns`:

```php
// v14 — correct
$GLOBALS['TCA']['tt_content']['types']['my_ctype']['columnsOverrides']['pi_flexform']['config']['ds']
    = 'FILE:EXT:my_ext/Configuration/FlexForm/FlexForm.xml';

// v13 — still needed there (pointer-key approach)
$GLOBALS['TCA']['tt_content']['columns']['pi_flexform']['config']['ds']['*,my_ctype']
    = 'FILE:EXT:my_ext/Configuration/FlexForm/FlexForm.xml';
```

`ExtensionManagementUtility::addPiFlexFormValue()` is deprecated in v14 and will
be removed in v15.
It internally uses `columnsOverrides` — use it directly instead.

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

## TCA showitem — shortform label references

In v14, core tab labels in `showitem` can be written in shortform:

```php
// v14 — shortform (new)
'--div--;core.form.tabs:access'

// v13 and v14 — longform (still valid in v14, required in v13)
'--div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access'
```

Do not use shortform in extensions that still support v13.

---

## Extension title comes from `composer.json`

Since TYPO3 v14 the extension title shown in the Extension Manager is derived
from the `description` in `composer.json`. The `title` and `description` keys in
`ext_emconf.php` are no longer read automatically
([Breaking-108304](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Breaking-108304-PopulateExtensionTitleFromComposerJson.html)).

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

## `record-transformation` is applied by default — and resolves IRRE relations

Since TYPO3 v14, `lib.contentElement` (the base TypoScript object every
`FLUIDTEMPLATE`-based content element extends via `=< lib.contentElement`)
already applies the `record-transformation` DataProcessor to the element's own
data by default:

```typoscript
# EXT:fluid_styled_content/Configuration/TypoScript/Helper/ContentElement.typoscript
lib.contentElement {
    dataProcessing {
        1770716912 = record-transformation
    }
}
```

This means every content element based on `lib.contentElement` automatically
gets a `{record}` variable in Fluid — a `TYPO3\CMS\Core\Domain\Record` object
with clean, type-aware, direct property access (`{record.header}`,
`{record.uid}`), independent of whatever the extension's own TypoScript adds.

Confirmed by testing: for a TCA field of `type => inline` (an IRRE/foreign-table
relation, e.g. `countup_items` in `ot_countup`), `record-transformation`
**automatically resolves the relation** into a `LazyRecordCollection` of
`Record` objects — with the same clean, direct property access on each child
(`{item.title}`, `{item.value_end}`, no `.data.` wrapper). A manual
`database-query` DataProcessor to fetch IRRE child records is **not** needed
for this case.

```html
<!-- No custom dataProcessing needed in TypoScript for this -->
<f:for each="{record.countup_items}" as="item">
    {item.title}: {item.value_end}
</f:for>
```

Caveats:

- Only fields defined in the TCA `columns` for the record's current `type`
  are exposed. A field not in the current type's `showitem`/columns is only
  reachable via `{record.rawRecord}` (untransformed).
- The core changelog for this feature (`Feature-103783`) explicitly notes the
  `Record` API "is still to be finalized" as of v13 LTS — treat it as stable
  enough to build on for v14-only extensions, but verify behavior for field
  types beyond scalars and `inline` (e.g. `select` with `foreign_table`,
  `category`) before relying on automatic resolution there too.

---

## Fluid 5 template file resolution — `.fluid.html` convention

Fluid 5 (TYPO3 v14) natively resolves `{Name}.fluid.{format}` before
`{Name}.{format}` for Templates, Partials, and Layouts — see
`TemplatePaths::resolveFileInPaths()` in `typo3fluid/fluid`. No TypoScript
or `view.format` configuration is needed; it works as a same-directory,
same-basename fallback out of the box.

Official reference:
[Feature-108166 — Fluid file extension and template resolving](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-108166-FluidFileExtensionAndTemplateResolving.html)

Prefer naming Fluid template files `*.fluid.html` (e.g. `Default.fluid.html`)
instead of plain `*.html` — this is the project convention going forward and
gives IDEs unambiguous syntax highlighting for Fluid vs. plain HTML.
