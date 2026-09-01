# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **Fluid moved out of `guidelines/typo3/` into its own `guidelines/fluid/`
  folder**, split into `README.md` (the `typo3fluid/fluid` engine) and
  `typo3.md` (Fluid as the core ships it). Fluid is an independent package that
  also runs standalone, where its version comes from `composer.json` and is
  unrelated to any TYPO3 release — a rule filed under "TYPO3 Developer" cannot
  state that. The split also makes an inversion visible that a single file hid:
  instantiating a view directly is forbidden in TYPO3 v14 and is the only
  correct way standalone. Same reasoning as the existing `guidelines/xliff/`
  folder. Moved unchanged: `f:format.html`, the backend module `Module` layout,
  ViewHelper argument types, `.fluid.html` resolution. `typo3/developer.md`
  keeps a pointer and drops from 636 to 496 lines.
- `guidelines/xliff/README.md` — a `<trans-unit>` without `<target>` is no longer
  harmless in a translation file. Up to v13 it was skipped and the source
  language answered; from v14 on `XliffLoader` sets the key to an empty string
  regardless, and a present key does not fall through. Left as a "still to
  translate" placeholder it renders the label as nothing at all. Replaces the
  previous line stating that TYPO3 handles the fallback automatically, which was
  true only up to v13. Because nothing fails under v13, these accumulate
  unnoticed and turn blank all at once on the upgrade — with a `grep` pair for
  auditing a file before it happens.

### Added

- `guidelines/xliff/README.md` — `target-language` on the `<file>` element is what
  makes a file a translation. Without it the loader reads `<source>` and ignores
  every `<target>`, so a `de.locallang.xlf` can look fully translated in the
  editor and serve English. Not a v14 change, just easy to miss — and invisible
  in the editor, which is what makes it survive review.
- `guidelines/fluid/README.md` — arbitrary tag attributes are dropped when their
  value is the empty string. `AbstractTagBasedViewHelper::initialize()` filters
  `''` out of `$this->additionalArguments`, so `data-caption=""` produces no
  attribute at all while `data="{caption: ''}"` does. It fails silently and the
  template still looks correct. Matters wherever the attribute is load-bearing:
  a `[data-fancybox]` selector a script binds on, or a marker that switches
  behaviour off.
- `guidelines/fluid/README.md` — the Fluid ↔ TYPO3 version map (v13.1 → 2.11,
  v13.2 → 2.12, v13.3 → 4.0, v14.0 → 5.0) and the rule that in a TYPO3 project
  the TYPO3 major is enough. The 2 → 4 jump in v13 carried no breaking changes,
  which is why the Fluid number never has to be looked up there. Standalone is
  the exception: only `composer.json` answers it.
- `guidelines/fluid/README.md` — `getTemplatePaths()` is gone from the view in
  Fluid 5 and lives only on the `RenderingContext`. Verified against
  `AbstractTemplateView` in 2.15.0 (line 96) and its absence in 5.3.1, whose
  view exposes only `getRenderingContext()`, `setRenderingContext()`,
  `assign()`, `assignMultiple()`, `render()`, `renderSection()` and
  `renderPartial()`. Affects standalone wrapper classes on upgrade;
  `new TemplateView()` itself stays correct, since `TYPO3Fluid\Fluid\View\
  TemplateView` is a different class from the core one v14 removed.
- `guidelines/playwright.md` — how to read a run's result. The line reporter
  prints failed test titles after the counts, so `tail -n` shows test names and
  a pass count while the `failed` line scrolls away, and a red run reads exactly
  like a green one. Says what to grep for instead, and that "N passed" alone
  proves nothing.

## [2.5.0] — 2026-08-25

### Added

- `guidelines/typo3/developer.md` — deletions and updates go through
  `QueryBuilder`, never through `Connection`. `Connection::delete()` and
  `update()` take `$types` as their last argument, not further conditions, and
  `expr()` sits on `QueryBuilder`. Mixing the two up reads plausibly, fails with
  an `Error`, and becomes an unbounded `DELETE` or `UPDATE` the moment someone
  repairs only the `Error`. With the rules that follow: share the criteria
  between the counting and the writing path, guard against the column default,
  and make `--dry-run` report rather than merely warn
- `guidelines/php.md` — a PHPStan baseline is not neutral debt. It freezes
  whatever is in it, including code that cannot run. The identifiers reporting
  runtime failures (`method.notFound`, `method.nonObject`, `class.notFound`,
  `binaryOp.invalid`, `foreach.nonIterable`, `return.type`) must be fixed rather
  than frozen. `class.notFound` is listed separately: a missing `use` makes
  `instanceof` silently `false`, so the guard rejects everything and the endpoint
  behind it stops answering without an error anywhere
- `guidelines/php.md` — ordered chains: normalise before inspecting. Encoding
  checks and type narrowing belong ahead of any regex, and `preg_*` returns
  `null`/`false` on a PCRE error, which `/u` makes reachable with ordinary user
  input
- `guidelines/php.md` — declared shapes are promises. An `array{…}` annotation is
  read as a guarantee by callers and by PHPStan; one the code does not keep is
  worse than `array<string, mixed>`, because it stops people from checking

## [2.4.0] — 2026-08-21

### Added

- `guidelines/git.md` — verify the active branch immediately before every
  commit, not just once at the start of a session; `main` is off-limits for
  any commit other than the release-merge commit itself
- `guidelines/shell.md` — bash 3.2 (macOS default) vs. bash 4.4+/5.x
  (DDEV, Live/Staging) compatibility rules: guard `"${array[@]}"` expansions
  under `set -u` against empty arrays, and prefer `ddev exec bash <script>`
  over running non-DDEV-orchestrating scripts directly on the host
- `guidelines/typo3/developer.md` — a Backend Module template rendered through
  `ModuleTemplate::renderResponse()` without an `f:layout` declaration still
  renders, silently dropping the module-body wrapper, the DocHeader partial,
  and every queued flash message. Requires the `Module` layout in module
  templates

## [2.3.2] — 2026-08-14

### Fixed

- `skills/guidelines-upgrade/upgrade.py` — every reference was resolved against
  `guidelines/`, so `../developer-guidelines/AGENTS.md` was checked for as
  `guidelines/AGENTS.md` and reported as missing. Since 2.2.0 that reference is
  the prescribed entry point, so every correctly set up project reported the
  same false alarm. References naming the repository root now resolve against
  it; `skills/…` was affected the same way
- `skills/guidelines-upgrade/upgrade.py` — `--grant-read` wrote the pre-2.3.0
  permission `Read(../developer-guidelines/guidelines/**)`, which does not cover
  the entry point it is granted for. It now writes
  `Read(../developer-guidelines/**)`, as does the check's hint text
- `skills/guidelines-upgrade/SKILL.md` — documents the widened grant and how a
  reference is resolved

## [2.3.1] — 2026-08-13

### Changed

- `AGENTS.md` — the read order said "only that one file", which contradicted the
  `see_also` mechanism two lines below it and left a task spanning two areas
  without a correct move. It is now one file per work area the task actually
  touches
- `AGENTS.md` — "never read the changelog index whole" carries its reason and
  the size that causes it. A bare prohibition is followed less reliably than one
  that states the cost
- `AGENTS.md` — lists the four document types, so practice guides are reachable
  from the entry point. They were only discoverable by browsing into
  `guidelines/typo3/`, where they read as a TYPO3 detail rather than as the
  place architecture decisions are settled

## [2.3.0] — 2026-08-13

### Changed

- `guidelines/README.md` — the read permission a project grants is now
  `Read(../developer-guidelines/**)` instead of `Read(.../guidelines/**)`.
  `AGENTS.md` sits in the repository root and `skills/` outside `guidelines/`,
  so the narrower pattern prompted on exactly the two files a project reads
  first. Existing projects should widen the pattern in their
  `.claude/settings.json`
- `guidelines/README.md` — the `CLAUDE.md` template for a project now routes
  through `AGENTS.md` and carries the missing-rule protocol, and says how to
  use it in a project that has no `Guidelines/` folder

## [2.2.1] — 2026-08-13

### Fixed

- `README.md` — the skills table listed only `typo3-changelog-harvest` and had
  been stale since three further skills were added. It now matches
  `skills/README.md`

## [2.2.0] — 2026-08-13

### Added

- `guidelines/README.md` — what to do when no rule covers the case: look it up
  in the changelog index or the surrounding project code, ask when that does
  not settle it, and never invent a fallback. The index said how to follow the
  rules that exist but was silent on the gaps, and silence reads as permission
  to guess — which is where the expensive errors come from
- `AGENTS.md` — entry point for AI assistants that read that filename but not a
  personal `CLAUDE.md`: read order, routing to the index, and the missing-rule
  protocol. It restates no rule, so nothing in it can drift out of sync

## [2.1.1] — 2026-08-13

### Changed

- `guidelines/README.md` — only the sibling relationship between a project and
  this repository is binding, not the name of the parent directory. The setup
  tree happens to be called `PhpstormProjects/`, which read as a requirement.
  A shared location within a team belongs in that team's project guidelines, so
  onboarding commands can be copied verbatim
- `guidelines/README.md` — projects read this clone's working tree, not a
  release tag: whichever branch is checked out is what every project sees, so
  the clone belongs on `main` outside of work on the guidelines themselves

## [2.1.0] — 2026-08-13

### Added

- `skills/changelog-audit/` — compares the guidelines against the changelog
  index and ranks entries that touch a subject the guidelines cover but do not
  cite. Uses a triage log (`changelog-index/reviewed.tsv`) so every entry is
  either cited, judged, or shown — without it an audit reports hundreds of
  candidates once and is never read again
- `guidelines/typo3/developer.md` — `$GLOBALS['TSFE']` and
  `TypoScriptFrontendController` are gone in v14; frontend state is read from
  PSR-7 request attributes. Found by the first audit run: the guidelines had no
  word on it, and seven of twenty-four candidates were facets of that one change

- `guidelines/typo3/practices/` — decision guides, a fourth document type next
  to rule files, version table and changelog index. They answer which approach
  to choose and when deliberately not, which neither the rules nor the changelog
  cover — some shifts (menus from `HMENU` to DataProcessor plus Fluid) have no
  changelog entry at all
- `guidelines/typo3/practices/fluid-components.md` — component or partial,
  Atomic Design levels, the strict argument API and the `settings` exception,
  v13 PHP collection class vs. v14.1 configuration, and the variant dispatcher
  as a SiteKit pattern rather than a general one

## [2.0.0] — 2026-08-13

Breaking for consumers: guideline files moved. Every project, skill or
`CLAUDE.md` referencing the old paths must be updated — there are no
compatibility stubs.

### Changed

- **All TYPO3 rules moved to `guidelines/typo3/`**: `typo3-integrator.md` →
  `typo3/integrator.md`, `typo3-developer.md` → `typo3/developer.md`,
  `sitekit/sitekit.md` → `typo3/sitekit.md`
- **All XLIFF rules moved to `guidelines/xliff/`** and split by purpose:
  `README.md` (format, attributes, ICU), `keys.md` (key naming and lifecycle),
  `typo3.md` (LLL references, SiteSet `labels.xlf`, enum labels). A task needing
  only key naming no longer loads 533 lines
- **Version model replaced.** A rule now lives once, in its topic file, and
  states its validity inline:
  `**Validity:** deprecated in v13 · removed in v14 · [#105171](…)`. The previous
  per-version overlay folders encoded *"introduced in"* but were read as
  *"applies only to"* — four of five rules in the former `v13/integrator.md`
  were current rules that hold in v14 unchanged
- `guidelines/typo3/v13/` and `v14/` removed; every difference is clearer as one
  rule showing both variants. `typo3/README.md` documents the criterion for
  reintroducing a version folder
- `guidelines/README.md` — the `UpperCamelCase` file naming rule now explicitly
  applies to project source trees, not to documentation repositories
- Validity is stated in **major versions only** and dated by practical
  usability, not by first appearance in the core. Live sites are updated at LTS
  releases, so every site runs the latest minor of its major and the minor
  version changes no decision. The exact minor stays in the changelog index

### Added

- `skills/guidelines-upgrade/` — checks a project against the current guidelines
  release: are they reachable, is `Read(../developer-guidelines/guidelines/**)`
  pre-granted, and do the referenced files still exist. Rewrites moved paths
  from a cumulative `path-map.tsv`, so a project that skipped releases is still
  carried forward. Reports by default, writes only with `--apply`, never commits

- `xliff/README.md` — whitespace and `xml:space`: from v14 the parser follows
  the XML specification, so indentation in a label collapses instead of being
  kept. Includes when `xml:space="preserve"` is warranted and why it should not
  be set by default ([#70867](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Important-70867-XLIFFWhitespaceHandlingNowRespectsXmlSpaceAttribute.html))
- `Important` changelog entries are now indexed as well (67 additional entries
  for v13 and v14). They change how existing code behaves without being
  classified as breaking, which is exactly what gets overlooked — the XLIFF
  whitespace change above was found this way
- `guidelines/typo3/versions.md` — validity table with changelog references,
  the entry point when unsure whether a rule still applies
- `guidelines/typo3/changelog-index/` — one line per core changelog entry for
  v13, v14 and v15, with affected symbols and a one-line migration hint.
  Searched with `grep`, never read whole
- `guidelines/typo3/changelog-index/cache/` — the source `.rst` for every
  indexed entry. A v13 project has no `14.x` folder in its vendor directory, so
  without this a v14 entry could be found but not opened. Released changelogs
  never change, so the copy never goes stale
- `guidelines/typo3/changelog-index/notes/` — hand-written notes on individual
  changelog entries, never touched by regeneration
- `skills/` — `typo3-changelog-harvest` (build and query the index) and
  `create-content-block` (moved in from a personal commands folder)
- YAML frontmatter in every guideline file (`applies_to`, `typo3`, `see_also`)
- `guidelines/README.md` — inclusion criterion: a rule earns its place only if
  the mistake actually happened and is not derivable from surrounding project
  code. Plus an expiry rule for versions leaving support

### Fixed

- `StandaloneView`, `TemplateView` and `AbstractTemplateView` are deprecated in
  v13 (`#104773`) and **removed in v14** (`#105377`). The replacement via
  `ViewFactoryInterface` is now documented as a rule instead of being absent
- `record-transformation` is documented as a v14 feature. The DataProcessor
  exists in v13, but only v14 applies it automatically and ships the surrounding
  record handling that makes it usable — dating it v13 would be accurate and
  misleading at once

## [1.1.0] — 2026-08-13

### Added

- `guidelines/README.md` — "Project-specific guidelines": rules that hold for a
  single project live in a `Guidelines/` folder in that project's root and are
  evaluated before the shared files; on conflict the project file wins. Shared
  rules are never copied into a project, and the repository is never vendored
  into one (no submodule) so that a single `git pull` updates every project
- `guidelines/README.md` — "Setting up a project": three-step onboarding with
  copy-paste blocks for the project's `CLAUDE.md` and for a committed
  `.claude/settings.json` granting read access to the shared guidelines
- `scss.md` — a project may define a short CSS prefix scheme
  (`my_productfinder` → `mp-`) instead of the extension-key default, provided the
  assignment is documented per extension in that project's `Guidelines/` and
  applied consistently
- `scss.md` — table of reserved prefixes that must never be assigned to an
  extension: `bs-`, `sk-`, `cb-`/`--cb-`, `is-`/`has-`, `tx-`. `sk-` is reserved
  in every project, not only in SiteKit projects
- `git.md` — "No customer data in public repositories": public repositories must
  never contain customer names, project names, domains, real extension keys or
  server data, examples included; use neutral placeholders

### Changed

- Replaced the extension-key examples in `scss.md` and `typo3-integrator.md` with
  neutral placeholders

### Fixed

- `php.md` — `code-quality` example now defines all three referenced scripts and
  states that unresolved `@`-references abort the chain; corrected "Both must
  pass" to "All three must pass"
- `typo3-developer.md` — added the v14 row to the version-specific file table
- `typo3-integrator.md` — noted that no v14 integrator file exists yet and how to
  read the v13 one in a v14 project; moved the `xliff.md` pointer to the end of
  the translation section
- `typo3/v13/developer.md`, `typo3/v13/integrator.md`, `typo3/v14/developer.md` —
  corrected the non-existent `docs/guidelines/` path in the header line
- `git.md` — the Co-Authored-By ban now applies to all repositories, matching the
  GitKraken instructions further down the file
- `README.md`, `guidelines/README.md` — aligned the XLIFF and SCSS topic
  descriptions with the actual file contents

## [1.0.0] — 2026-07-31

First tagged release of the guideline set.

### Added

- `guidelines/typo3/content-blocks.md` — Content Block conventions: directory
  structure, two-layer CSS architecture with the portable fallback pattern,
  asset loading via `cb:assetPath()`, `config.yaml` and `SiteKit.yaml`
  conventions, per-block README structure
- `git.md` — first push on a new repository: push `main` before `develop` so
  GitHub picks the correct default branch
- `javascript.md` — TypeScript vs. plain JavaScript decision rule, including a
  minimal esbuild + `tsc --noEmit` reference setup
- `scss.md` — when to introduce actual Sass compilation for standalone
  extensions
- `typo3-developer.md` — ExtensionScanner false positives caused by
  property/method naming; rule against guessing the current TYPO3 minor version
- `typo3-integrator.md` — frontend framework folder structure for SiteKit-based
  and standalone extensions; `f:translate` `extensionName` must be
  UpperCamelCase
- `typo3/v13/integrator.md` — `@import` instead of the deprecated
  `<INCLUDE_TYPOSCRIPT:`; New Content Element wizard auto-registration via TCA
  and wizard group selection
- `typo3/v14/developer.md` — `record-transformation` applied by default
  including automatic IRRE relation resolving; Fluid 5 `.fluid.html` file
  resolution

### Changed

- `typo3/v14/developer.md` — replaced the "Extension Title missing" section with
  the actual v14 behavior: the extension title is derived from the
  `composer.json` description, split on the first ` - `

### Fixed

- Added `guidelines/typo3/content-blocks.md` to the file index in both
  `README.md` and `guidelines/README.md`, and refreshed the outdated topic
  descriptions for the version-specific files
- Removed cross-references to sections that do not exist and corrected the claim
  that `templateRootPaths` can override shipped `Resources/Public` assets — it
  resolves Fluid templates only
- Added missing final newlines in `guidelines/php.md`,
  `guidelines/typo3-integrator.md` and `sitekit/sitekit.md` as required by
  `.editorconfig`
