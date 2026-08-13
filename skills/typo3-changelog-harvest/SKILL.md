---
name: typo3-changelog-harvest
description: Build and query the TYPO3 changelog index. Use when an ExtensionScanner or PHPStan finding names a changelog number or a removed/deprecated class, when checking whether a TYPO3 API is still valid in a given version, or when the index needs to be regenerated after a core update.
---

# TYPO3 Changelog Harvest

Turns the reStructuredText changelogs shipped with the TYPO3 core into a
grep-optimised index, and defines how to query it.

This is **level 3** of the guidelines architecture: never read as a whole, only
entered through a changelog number or a symbol name. See
`guidelines/typo3/README.md` for how the three levels relate.

## Querying (the common case)

Do **not** read the index files. Grep them.

```bash
# Entry point: a changelog number from an ExtensionScanner or PHPStan finding
grep -h '^104773' ../developer-guidelines/guidelines/typo3/changelog-index/v1*.tsv

# Entry point: a class or method name
grep -h 'StandaloneView' ../developer-guidelines/guidelines/typo3/changelog-index/v1*.tsv

# Entry point: an area, via the tag column
grep -h 'TypoScript' ../developer-guidelines/guidelines/typo3/changelog-index/v14.tsv
```

### Writing forward-compatible code

`v15.tsv` is indexed even though no project runs v15 yet. Knowing what the next
major removes makes it possible to write v14 code today that survives the
upgrade — cheaper than migrating later.

```bash
# Does the API I am about to use disappear in the next major?
grep -P '\tBreaking\t' .../changelog-index/v15.tsv | grep -i 'formengine'
```

Use this when choosing between two working approaches in a v13/v14 project. Do
**not** use it to write code that only works on v15 — those entries are
`provisional` and the project still has to run on its installed version.

Columns, tab-separated:

| # | Column | Notes |
|---|---|---|
| 1 | number | changelog issue number |
| 2 | type | `Breaking`, `Deprecation`, `Feature` |
| 3 | version | e.g. `13.4` |
| 4 | title | from the entry heading |
| 5 | tags | from the entry's `.. index::` directive (`TCA`, `TypoScript`, `NotScanned`, `ext:core`, …) |
| 6 | symbols | short class/method names, capped at 30 (`+N-more-see-rst` marks the cut) |
| 7 | migration-gist | one-line summary of the `Migration` section |
| 8 | note | `note` = a curated note exists, see below |
| 9 | source | `local:14.3.x` or `provisional` |
| 10 | path | relative to the core's `Documentation/Changelog/` |

### How far to trust each column

1. **`note` column says `note`** → read `changelog-index/notes/{number}.md` first.
   It is hand-written, outranks everything else, and usually records a mistake
   that was already made once.
2. **`type` is `Deprecation` or `Feature`** → the migration gist is normally
   enough to act on.
3. **`type` is `Breaking`** → read the full `.rst` before writing code. The gist
   is mechanically extracted and lossy; being wrong about a breaking change is
   expensive.

Read the full entry from the cache next to the index. Column 10 of the index is
the path, and it resolves inside `changelog-index/cache/`:

```bash
sed -n '/^Migration/,$p' \
  ../developer-guidelines/guidelines/typo3/changelog-index/cache/13.3/Deprecation-104773-CustomFluidViewsAndExtbase.rst
```

The cache covers **every indexed version, not just the one installed**. That is
the point: a v13 project has no `14.x` folder in its vendor directory, so
without the cache a v14 entry could be found but not opened. The same path also
resolves against `vendor/typo3/cms-core/Documentation/Changelog/` when the
installed core happens to cover that version.

## Writing a note

When a changelog entry was handled **wrongly** and the correct handling is not
obvious from the `.rst` alone, record it:

```markdown
# #104773 — Custom Fluid views and Extbase

**Antipattern:** `GeneralUtility::makeInstance(StandaloneView::class)` als
Ersatz für den entfernten Konstruktoraufruf.

**Correct:** `ViewFactoryInterface` injizieren, `ViewFactoryData` bauen,
`create()` aufrufen. Die Template-Pfade gehören in `ViewFactoryData`,
nicht in nachträgliche Setter.
```

Notes live in `changelog-index/notes/{number}.md`, are **never** touched by the
harvest, and survive every regeneration. Nothing else in `changelog-index/` is
hand-editable.

A note is not the same as a guideline. It stays a note as long as it concerns
one changelog entry. It is promoted into a guideline file (with a `Validity:`
line and a `Stale-knowledge trap:` block) only when the same class of mistake
shows up repeatedly — see the inclusion criterion in `guidelines/README.md`.

## Regenerating the index

Needed after a core update, or when a version should be indexed for the first
time.

```bash
python3 skills/typo3-changelog-harvest/harvest.py \
  --changelog-dir ~/PhpstormProjects/<project>/vendor/typo3/cms-core/Documentation/Changelog \
  --major 13 --major 14 --cache-local
```

`--cache-local` copies the source `.rst` files into `changelog-index/cache/`.
Always pass it: released changelogs never change, so this is a one-time cost,
and it is what makes a v14 entry readable from inside a v13 project. The files
compress well — several hundred entries add well under a megabyte to the
repository.

Pick a project whose installed core is **at least** as new as the highest
version to index — the changelog folder only contains versions up to the
installed core. Only `Breaking`, `Deprecation` and `Feature` are indexed;
`Important` is dropped. Versions below 13.0 are out of scope.

### Write protection — maintainer only

Generated files must never appear as uncommitted changes in someone else's
clone; that produces `git pull` conflicts for every collaborator.

- `.maintainer` present in the repository root → writes into
  `guidelines/typo3/changelog-index/`
- `.maintainer` missing → read-only mode, writes to `~/.claude/typo3-changelog/`
  and says so

`.maintainer` is gitignored and exists only in the maintainer's checkout.
Collaborators grep the committed index but never regenerate it.

### Unreleased versions

For a version that is not installed anywhere yet (preparing for v15 while the
core is still v14), harvest from the TYPO3 core repository instead of `vendor/`.
The file name already carries type, number and title, so a directory listing
produces most columns without downloading a single file; the symbol column is
filled lazily for entries that are actually consulted, and those `.rst` files
are cached under `changelog-index/cache/main/`.

```bash
python3 skills/typo3-changelog-harvest/harvest.py --remote main --major 15
```

`--remote` implies `--provisional`. Entries from an unreleased branch can still
be reclassified or dropped, so they must **not** become a `Validity:` line in a
guideline without that caveat.

The cached `.rst` files are a snapshot of a moving branch. Re-run the command
every few months to pick up new entries, and re-harvest from `vendor/` once the
version is released — a local core is authoritative, a branch is not.
