---
name: create-content-block
description: Create a new TYPO3 Content Block in the current project's sitepackage, following the shared Content Block conventions. Use when the user asks to add, create or scaffold a Content Block or a new content element.
---

# Create TYPO3 Content Block

Create a new TYPO3 Content Block in the current project's sitepackage.

## Before you start

1. Read the developer guidelines FIRST (mandatory):
   - `/Users/oliverthiele/PhpstormProjects/developer-guidelines/guidelines/typo3/content-blocks.md` — **primary reference for all CB conventions**
   - `/Users/oliverthiele/PhpstormProjects/developer-guidelines/guidelines/typo3/integrator.md`
   - `/Users/oliverthiele/PhpstormProjects/developer-guidelines/guidelines/xliff/typo3.md` — labels.xlf, SiteSet labels
   - `/Users/oliverthiele/PhpstormProjects/developer-guidelines/guidelines/xliff/keys.md` — key naming
   - `/Users/oliverthiele/PhpstormProjects/developer-guidelines/guidelines/scss.md`
2. Identify the sitepackage: look for a `ContentBlocks/` directory under `packages/*/`
3. Study existing Content Blocks in that directory for project-specific patterns

## Information to gather

Ask the user (only what's not already clear from context):

1. **Name:** PascalCase directory name (e.g., `TechBadges`, `PriceCard`)
2. **Purpose:** One sentence — what does the element display?
3. **Fields:** Which fields are needed? Prefer `useExistingField: true` for standard TYPO3 fields (header, bodytext, header_link, subheader, icon_identifier, assets, image). Only create custom fields when no existing field fits.
4. **Collection fields?** Does this element need repeatable sub-items (IRRE)? If yes, define the sub-fields.
5. **Icon?** Does it use ot-icons? If yes, use the `i:icon` ViewHelper with no hardcoded `iconStyle` (use SiteSet default).
6. **Styling:** Does it need custom CSS? Always create `assets/frontend.css` with portable defaults using the fallback pattern. If the project needs overrides, also create a Build SCSS file.
7. **JavaScript:** Does it need JS? If yes, always create `assets/frontend.js` for portable logic. For substantial library imports, additionally create a Build entry point.
8. **SiteKit groups:** Which groups should it appear in? (group_content_small, group_content_wide, group_cards, group_hero, group_advanced)

## Icon Selector (ot-iconselector)

When `ot_iconselector` is installed, `icon_identifier` fields should use the visual icon picker.

**Top-level fields** (`useExistingField: true`): These inherit the full TCA config from `tt_content.icon_identifier`, including any `renderType` set by a TCA override. Ensure the sitepackage has a TCA override on `tt_content` that applies `renderType: otIconSelector`. Only set `renderType` — never change `type` (TYPO3 derives DB schema from `type`).

```php
// Configuration/TCA/Overrides/tt_content.php
if (ExtensionManagementUtility::isLoaded('ot_iconselector')) {
    $GLOBALS['TCA']['tt_content']['columns']['icon_identifier']['config']['renderType'] = 'otIconSelector';
}
```

**Collection child fields**: `useExistingField: true` is not available inside Collections (separate child table). Create a TCA override file named after the child table (naming pattern: `cb_{blockname}_{field}`):

```php
// Configuration/TCA/Overrides/cb_{blockname}_{field}.php
if (ExtensionManagementUtility::isLoaded('ot_iconselector')) {
    $GLOBALS['TCA']['cb_{blockname}_{field}']['columns']['icon_identifier']['config']['renderType'] = 'otIconSelector';
}
```

## After creation

1. Flush TYPO3 caches: `ddev exec typo3 cache:flush`
2. Check the backend — the new element should appear in the configured SiteKit groups
3. Do NOT run `fe-build` — the file watcher handles SCSS/JS changes automatically
4. Test the element in the frontend — the portable CSS from `assets/frontend.css` should already provide basic styling
5. Test in both dark and light mode
6. If project overrides are needed, create `Build/Default/src/scss/ContentBlocks/_{Name}.scss` and import it in `Main.scss`