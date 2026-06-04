# TYPO3 v14 — Developer

Version-specific additions to `docs/guidelines/typo3-developer.md` for TYPO3
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

## Extension Manager — "Extension Title missing"

TYPO3 v14 validates that `description` in `composer.json` and `ext_emconf.php`
are consistent.
A mismatch triggers the **"Extension Title missing"** warning in the backend
Extension Manager.

Rule: always keep both descriptions in sync when updating one of them.

```json
// composer.json
"description": "Gallery - Gallery extension for TYPO3 v13 and v14."
```

```php
// ext_emconf.php
'description' => 'Gallery extension for TYPO3 v13 and v14.',
```

The `composer.json` description follows the convention
`"Title - Description text."`;
`ext_emconf.php` has a separate `'title'` key and uses only the description text
without prefix.
