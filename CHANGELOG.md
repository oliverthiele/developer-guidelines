# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `guidelines/README.md` — "How a rule is backed": a `**Basis:**` line per
  section says whether its statements are verified against a named package
  version, documented in a changelog, or only observed in a project. Observed
  rules yield to contradicting code; new sections carry the line, existing ones
  get it when next changed. The v14 upgrade sections carry it already
- `guidelines/typo3/developer.md` — "Upgrading to v14 — changes that fail
  silently": base TCA files must `return` their array (the file name becomes the
  table name, `$GLOBALS['TCA']` writes are discarded);
  `ExtensionManagementUtility::addPlugin()` takes two arguments and a stale
  `'CType'` becomes the FlexForm data structure; the fifth argument of
  `configurePlugin()` is required in v13.4 and unused in v14; a leftover
  `IconRegistry` in `ext_localconf.php` stops the boot; `absoluteUri: true`
  breaks `f:image`; `errorMessage` → `message` on `RegularExpressionValidator`;
  which Rector sets to use and what to undo after the run. Plus the "Fetch of
  property data" ExtensionScanner false positive
- `guidelines/fluid/README.md` — `renderStatic()` → `render()`: without
  `getContentArgumentName()` a value passed as argument is lost silently, while
  the inline chain keeps working
- `guidelines/fluid/typo3.md` — global ViewHelper namespaces in
  `Configuration/Fluid/Namespaces.php`, `typo3 fluid:namespaces`; an `xmlns` with
  backslashes or `https` throws in Fluid 5
- `guidelines/typo3/integrator.md` — `allowedContentTypes` /
  `disallowedContentTypes` per backend layout column replace
  EXT:content_defender except `maxitems`; an escaped `\/` in a TypoScript
  `matches` pattern makes the condition throw on every evaluation
- `guidelines/playwright.md` — a plugin spec needs a positive assertion besides
  `expectNoError()`
- `guidelines/typo3/versions.md` — rows for all of the above
- `guidelines/fluid/README.md` — a component's `default` is not cast to the
  declared type. A passed value is, an omitted one is not: `default="false"`
  arrives as the string `"false"`, and `!{argument}` is therefore always false.
  `{argument}` alone is right because `convertToBoolean()` special-cases that
  string, so the defect only shows on the negation. Holds in Fluid 4 and 5 alike
- `guidelines/fluid/typo3.md`, `guidelines/xliff/typo3.md` — `f:translate`
  arguments must be a list. From v14.2 `array_is_list()` decides between
  `vsprintf` and ICU; an array starting at 1 takes the ICU branch and leaves
  `%1$s` standing in the page. v13 ignored the keys, so this breaks silently on
  upgrade — no exception, no deprecation

### Fixed

- `guidelines/typo3/versions.md`, `guidelines/typo3/developer.md`,
  `guidelines/xliff/README.md`, `guidelines/typo3/practices/record-languages.md`
  — four changelog links pointed at file names that do not exist on
  docs.typo3.org (#107047, #107789, #107710, #106510)

## [2.8.1] — 2026-09-16

### Changed

- `guidelines/typo3/versions.md`, `guidelines/typo3/README.md` — the
  `record-transformation` row and the version model now say the same as the rule
  itself: available since v13.2 and registrable by hand there, applied by default
  and recommended from v14. The row read "usable in practice: no" for v13, so the
  answer depended on which file was opened
- `guidelines/README.md`, `AGENTS.md`, `guidelines/setup.md` — for a reusable
  extension, the installed core is only half the answer: `composer.json` says
  which range it must support, and an API confirmed in the installed v14 proves
  nothing about the v13 the extension also declares

## [2.8.0] — 2026-09-16

### Added

- `guidelines/typo3/developer.md` — Extbase honours `fallbackType` from TYPO3
  14.3.6 on (#88886). On `strict` languages, untranslated records disappear —
  aggregate roots and related objects, including children of parents without a
  language field and of `-1` parents. Up to 14.3.5 Extbase always fell back to
  the default language, and the change came in a patch release without any
  signature change, so neither ExtensionScanner nor PHPStan can see it. Rules:
  nullable getters for 1:1 relations, no validators on display-only models, a
  per-table decision instead of a global fallback, language changes through
  DataHandler, and translated pages tested before the update
- `guidelines/typo3/practices/record-languages.md` — decision guide: translate,
  `-1`, `0` with `OVERLAYS_MIXED`, not language aware, or `l10n_mode: exclude`.
  Records from the core source that `-1` is not a fallback — a translation of a
  `-1` record is never loaded — and shows how to restore "mixed" for a single
  table, including relations of models you do not own
- `changelog-index/notes/88886.md` — the template guard, `-1` on the parent only,
  and SQL fixes as antipatterns
- `guidelines/typo3/practices/record-languages.md` — how to check the behaviour
  in a project: a CLI script that creates records through DataHandler and runs
  the repository query once per language against the singleton `Context`
- `guidelines/typo3/versions.md` — row for #88886
- `guidelines/git.md` — customer data leaks into a public repository at one
  specific moment: when a rule is promoted out of the project where the mistake
  happened, because there the project's names and numbers are simply the material
  the fix was made of. Promotion is therefore its own step — write a sanitised
  draft in the project, check it while the context is still open, then apply it
  from the draft rather than from the diff or the transcript
- `guidelines/testing.md` — multilingual sites: pages that render records are
  tested in at least one translated language as well, preferably a strict one.
  Translation state is data, and the default language never runs an overlay, so
  it cannot show what is missing. Compare structure rather than text, use a copy
  of production content, and repeat after every core update, patch releases
  included
- `guidelines/playwright.md` — one generated test per language, and a count
  comparison for content that is meant to be identical across languages
- `guidelines/typo3/developer.md` — every `cropVariants` entry needs a
  `cropArea`. The image manipulation element fills a missing one in; the
  `OtherLanguageThumbnails` wizard does not and raises a warning when a
  translated record with an image is edited

- `guidelines/typo3/developer.md` — TCA system columns come from `ctrl`, not from
  hand-written `columns` definitions (#104311): the core creates them, adds
  `transOrigPointerField` on its own when only `languageField` is set, and
  creates the database columns from TCA (#101553). Removing the `columns`
  boilerplate does not make a table less language aware — removing
  `languageField` does

- `guidelines/fluid/typo3.md` — the request in a ViewHelper comes from
  `getAttribute(ServerRequestInterface::class)`. `RenderingContext->getRequest()`
  was removed in v14 and the ExtensionScanner deliberately does not look for it,
  because the method name is too common to scan — so nothing warns before the
  fatal error (#104684)
- `guidelines/typo3/developer.md` — a validator attribute belongs on the
  parameter. `#[Validate(param: …)]` and `#[IgnoreValidation(argumentName: …)]`
  are deprecated in v14 and stop working in v15; attributes applying to a whole
  method and `#[Validate]` on a property are unaffected (#108227)
- `guidelines/typo3/versions.md` — rows for both

### Changed

- `guidelines/README.md` — the lookup path now names the two steps it skipped:
  establish which TYPO3 version the project runs, and read the installed source
  in `vendor/`. A changelog says what changed, not how an API is used, and the
  published documentation defaults to another version
- `guidelines/README.md` — expiry distinguishes instructions from warnings. The
  end of a version's support removes a rule about how to do something there; a
  warning about a removed pattern stays while the pattern is still produced,
  because support ends on a schedule and training data does not
- `guidelines/typo3/developer.md` — the `ViewFactoryData` example uses root paths
  and `render('Mail/OrderConfirmation')` and hands over the request, following
  the best-practice block in the core class, which names
  `templatePathAndFilename` as the thing to avoid. Root paths are also what makes
  a template overridable by a project
- `guidelines/typo3/developer.md`, `guidelines/typo3/versions.md` — where
  availability and recommendation differ, both are named: `record-transformation`
  is available since v13.2 and recommended from v14. A bare "v14" reads as "does
  not exist before v14"
- `guidelines/README.md` — setup and tooling moved to `guidelines/setup.md` and
  `guidelines/tooling.md`, leaving pointers. Both are read once per project, not
  per task; the mandatory entry file drops from 275 to 171 lines
- `guidelines/typo3/practices/record-languages.md` — the Extbase identity map
  keys on the language aspect since v14.2 (#93765), so a second query in another
  language needs no `clearState()` and returns a distinct object. The migration
  step said the opposite, which held for v13
- `guidelines/typo3/versions.md`, `guidelines/typo3/README.md` — exception to
  "major versions only": a behaviour change shipped in a patch release names that
  release in full, because the patch update is the moment it breaks
- `changelog-index/` — regenerated from core 14.3.7, adding the Important entries
  of the 13.4.x and 14.3.x patch releases; v15 re-harvested from `main`
- `skills/changelog-audit/SKILL.md`, `changelog-index/reviewed.tsv` — a
  `not-relevant` reason now names the mechanism that already covers the entry —
  ExtensionScanner, PHPStan, PHP itself, or a grep in the index — instead of the
  current project inventory. A verdict decides only whether an entry deserves a
  rule; the index stays complete, and "we do not use it" is wrong the day a
  project from another developer arrives

## [2.7.0] — 2026-09-01

### Added

- `guidelines/README.md` — a `**Tooling:**` line may sit next to `**Validity:**`
  on any rule that can be checked automatically, plus an index of the packages
  that do it. The point is that nobody — a person or an assistant — starts doing
  by hand what a linter already fixes. The rules stay independent of the tools:
  a `**Tooling:**` line says a check can be automated, never that the rule
  exists because the tool does
- `guidelines/fluid/README.md` — CDATA no longer comments code out. Fluid used
  to strip `<![CDATA[ ]]>` before parsing, which is what made
  `<f:comment><![CDATA[ … ]]></f:comment>` safe for invalid Fluid. Fluid 5 stops
  stripping it, so the construct comments nothing out and writes a deprecation
  on every render from TYPO3 13.4.21 on. A plain `<f:comment>` suffices since
  v13.3, where it began ignoring Fluid syntax errors on its own
- `guidelines/fluid/README.md` — CDATA is not gone but reassigned: inside a
  section `{…}` is ignored and `{{{…}}}` accesses variables, so that inline CSS
  and JavaScript stop colliding with Fluid's braces. Noted with the core's own
  caveat that inline CSS/JS in a template remains bad practice
- `guidelines/fluid/README.md` — the namespace URI is `http://`, never
  `https://`. It is an identifier, not an address; the https form throws a
  runtime exception, and "fixing" the scheme is a plausible-looking wrong move
- `guidelines/fluid/typo3.md` — `f:render.contentArea` renders a content area
  from the `page-content` DataProcessor, with `recordAs` replacing the `f:for`.
  The established `f:cObject` / `f:for` pattern does not fail, which is why it
  survives review — but it emits no `ModifyRenderedContentAreaEvent`, so the
  extension point other extensions rely on is silently absent
- `guidelines/playwright.md` — a test that triggers mail must ask whether mail
  is being captured **before** it submits, and skip when it is not. On a staging
  system cloned from live those recipients are real people. The check has to be
  answerable while capturing is off, which is what a catcher that merely
  intercepts cannot report

## [2.6.0] — 2026-09-01

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
- `guidelines/git.md` — the rule against customer data in public repositories now
  covers the vocabulary of a project (product and article names, article numbers,
  category and tag names, project-specific CSS classes, JS variables and
  `data-js` values) and quantities (defect counts, language counts, record
  counts). Quantities are the part that slips through, because a number reads as
  neutral: it describes one specific project, it combines with other details into
  a fingerprint that identifies the customer without naming them, and it reads as
  if the author had built the defects rather than inherited them. State the
  mechanism, not the measurement.

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
