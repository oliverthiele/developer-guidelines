---
title: Record languages — translate, -1, fallback, or no language
scope: typo3
kind: practice
applies_to:
  - "**/Configuration/TCA/**/*.php"
  - "**/Classes/Domain/Repository/**/*.php"
typo3: ["13", "14"]
see_also: ["typo3/developer.md", "typo3/versions.md", "testing.md"]
---

# Record languages — translate, `-1`, fallback, or no language

A **practice guide**, not a rule file. Read it when a table's language handling
is being decided — typically when a multilingual site with `fallbackType: strict`
shows missing records on translated pages after the update to TYPO3 14.3.6. The
rule itself is in [`../developer.md`](../developer.md) → *Extbase and
`fallbackType: strict`*.

Status markers on statements that are not plain facts:

- *(verified)* — reproduced on a TYPO3 14.3.6 installation with a language using
  `fallbackType: strict`, against an Extbase model with a 1:1 relation
- *(core source)* — read in the core source of 14.3.7, not exercised
- *(untested)* — plausible, neither read nor reproduced

## Decision

Decide per table what its records **are**, not what the TCA template generated:

| The data is … | Use |
|---|---|
| content that differs per language — article, news, event | language aware, translated; `strict` is correct |
| language-neutral master data, no translation intended — contact, address | language aware, records set to `-1` — **and their child records and file references as well** |
| maintained in the default language today, translation possible later, with no date for it | language aware, records in `0`, `OVERLAYS_MIXED` for this table only |
| without language by nature — copied from a system that has no languages, pure configuration values | **not** language aware: remove `languageField` from `ctrl` — that entry is the switch, see *Why* |
| a relation whose value must not differ per language — e.g. category assignments a filter depends on | `l10n_mode: exclude` on the relation field |

## When not to

- **Not `-1` when a translation may come later.** `-1` is not a fallback that a
  translation overrides once it exists — see *Why*. Use `0` with
  `OVERLAYS_MIXED` instead.
- **Not `OVERLAYS_MIXED` on content tables, and never globally.** On content,
  `strict` is right: "mixed" shows default-language text on a translated page,
  which is exactly what v13 did and what a site owner chose `strict` to prevent.
- **Not "not language aware" for data editors maintain and may want to
  translate.** Use `0` with `OVERLAYS_MIXED`.
- **Not `l10n_mode: exclude`** when editors deliberately assign different
  relations per language, such as language-specific downloads.

## Why

- **The behaviour changed in a patch release.** From 14.3.6 Extbase honours
  `fallbackType`; untranslated language-0 records vanish from translated pages
  without an error. See `developer.md`.
- **`-1` is not a fallback.** *(verified)* A translation row pointing at a `-1`
  record is ignored: the strict language shows the `-1` record, never the
  translation. The Extbase query only fetches translations whose parent is in
  language `0` (`Typo3DbQueryParser::getLanguageStatement()`), and
  `PageRepository::getRecordOverlay()` returns `-1` records untouched without
  looking for one. The backend never creates that shape either — the list module
  offers no localization for `-1` records (`DatabaseRecordList`), and
  `DataHandler::localize()` does not refuse such a record but writes **no**
  translation parent.

  What comes out of a forced localization is a floating record, and a strict
  language then returns it **next to** the `-1` record — the same entry twice.
  *(verified)*

  Translating later therefore means switching the records back to `0` and
  translating all of them in every strict language at once, or switching to `0`
  with `OVERLAYS_MIXED`.
- **A `-1` parent does not protect its children.** *(verified)* The `-1` record
  itself is returned in every language, but its relations are still overlaid to
  the requested language: a child record or file reference in language `0` is
  dropped, and the relation is `null` on the translated page. Set the children to
  `-1` as well.
- **Imports undo data fixes.** An importer that inserts records without
  `sys_language_uid` creates language `0`. For imported tables, set the language
  in the importer or make the table not language aware.
- **New records default to language `0`.** A TCA `default` of `-1` for
  `type => language` is *(untested)*.
- **`ctrl['languageField']` is the switch, not the `columns` definitions.**
  *(core source)* Since v13.3
  ([#104311](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.3/Feature-104311-AutoCreatedSystemTCAColumns.html))
  `TcaEnrichment` creates the `columns` entries for the language fields whenever
  `ctrl['languageField']` is set and they are not defined by hand — and it adds
  `transOrigPointerField => 'l10n_parent'` to `ctrl` on its own when only
  `languageField` is there. Removing the hand-written `columns` definitions
  therefore makes a table no less language aware; removing `languageField` does.
  Conversely, a table that stays language aware needs none of that boilerplate
  in its TCA any more.
- **The identity map separates languages since v14.2**
  ([#93765](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Important-93765-ExtbaseIdentityMapNowLanguageAware.html)).
  Its key carries `contentId`, overlay type and fallback chain, so the same
  record fetched under two language aspects comes back as **two distinct
  objects**. Code comparing objects with `===` across language contexts breaks.
  *(verified)*
- **Relations without `l10n_mode: exclude` are stored per language**, with their
  own MM rows per translation. Editors change one language and forget the other;
  filters then behave differently per language.

## v13 vs v14

v13 and v14 up to 14.3.5 hide all of this: untranslated related records come
back in the default language. The decision table can be applied **before** the
update — `-1`, `OVERLAYS_MIXED` and removing language awareness change nothing in
the output of an older core and keep working afterwards. Audit before updating to
14.3.6, not after go-live.

## Restoring "mixed" for one table

On a query the table's own repository builds *(verified — the fallback applies to
the records and to their relations)*:

```php
use TYPO3\CMS\Core\Context\LanguageAspect;

$querySettings = $query->getQuerySettings();
$languageAspect = $querySettings->getLanguageAspect();
$querySettings->setLanguageAspect(new LanguageAspect(
    $languageAspect->getId(),
    $languageAspect->getContentId(),
    LanguageAspect::OVERLAYS_MIXED,
    $languageAspect->getFallbackChain(),
));
```

`DataMapper::getPreparedQuery()` hands the overlay type of the parent query on to
relations, so this also covers relations loaded through that query.

When the table is reached as a relation of models you do not own, use
`ModifyQueryBeforeFetchingObjectDataEvent` *(verified)*. It is dispatched in
`Backend::getObjectDataByQuery()` for every Extbase query, relation queries
included, after `DataMapper` has set their language aspect:

```php
use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\Context\LanguageAspect;
use TYPO3\CMS\Extbase\Event\Persistence\ModifyQueryBeforeFetchingObjectDataEvent;

#[AsEventListener]
final readonly class FallBackToDefaultLanguageForGroups
{
    public function __invoke(ModifyQueryBeforeFetchingObjectDataEvent $event): void
    {
        $query = $event->getQuery();
        if ($query->getType() !== Group::class) {
            return;
        }
        $querySettings = $query->getQuerySettings();
        $languageAspect = $querySettings->getLanguageAspect();
        $querySettings->setLanguageAspect(new LanguageAspect(
            $languageAspect->getId(),
            $languageAspect->getContentId(),
            LanguageAspect::OVERLAYS_MIXED,
            $languageAspect->getFallbackChain(),
        ));
    }
}
```

The listener changes the relation's records only, while the aggregate root stays
strict — verified with a translated parent whose untranslated child came back
through the listener alone.

Three gaps:

- **File references cannot be addressed by type.** Every file relation of every
  table arrives as `TYPO3\CMS\Extbase\Domain\Model\FileReference`, so
  `getType()` cannot tell one table's images from another's. Either accept the
  fallback for all of them or read the query's source instead.
- `findByUid()` returns an object already held by the persistence session without
  running a query, so no event is dispatched for it.
- `count()` runs through the separate `ModifyQueryBeforeFetchingObjectCountEvent`
  ([#106510](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.0/Feature-106510-AddedPSR-14EventsToExtbaseBackendgetObjectCountByQueryMethod.html)).

## Migration

1. **Find affected relations.** Build the relation list from
   `DataMapFactory::buildDataMap()` for every model class — Extbase's own view,
   including parents without a language field — and generate one read-only SQL
   query per relation: value field, `foreign_field`, MM. Report related records
   in language `0` without a visible translation in the target language. Run it
   against a copy of production data. `DataMapFactory` is `@internal`: fine for a
   one-off audit script, not for extension code.
2. **Classify each finding** with the decision table; fix code (nullable getters,
   validators) and data — through the backend or DataHandler.
3. **Compare rendered data per language.** For JavaScript apps fed by JSON (data
   attributes, APIs), diff the default and the translated JSON structurally —
   list lengths, `null` vs. set, identifiers; ignore translated strings. This also
   finds editorial divergence the relation audit cannot see.
4. **Switching a relation to `l10n_mode: exclude`:** translations stop showing the
   field but keep their old rows until the **default record is saved** — then
   DataHandler copies the assignment to all translations. Before saving, add
   assignments that existed only in a translation and are correct, or they are
   lost. *(verified)*
5. **Checking the behaviour in your own project.** A CLI script is enough and
   answers in seconds what a click-through cannot answer reliably: bootstrap
   TYPO3 (`SystemEnvironmentBuilder::run()` plus `Bootstrap::init()`), set an
   admin backend user so DataHandler works, create the records through
   DataHandler, then set the language aspect on the singleton `Context` from
   `LanguageAspectFactory::createFromSiteLanguage()` and run the repository query
   once per language. Overriding the overlay type on the aspect shows the "mixed"
   result in the same run.

   On v14.2 and later no `PersistenceManager::clearState()` is needed between the
   languages — the identity map keys on the language aspect and answers each run
   separately *(verified)*. On v13 it is, or the second query is answered from
   the first run's objects.
6. **Removing language awareness from the TCA** leaves the database columns; the
   schema compare then only proposes dropping the language index. Decide the
   column drop separately. *(verified)*
