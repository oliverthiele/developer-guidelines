---
title: TYPO3 deployment
scope: typo3
applies_to:
  - "deploy.php"
  - "composer.json"
typo3: ["13", "14"]
see_also: ["typo3/developer.md", "git.md", "shell.md"]
---

# TYPO3 Deployment

What a deploy of a TYPO3 project — and an import of the live database — has to
account for. Not a runbook: the traps, each with the reason it is one. How to
switch a server's branch and why deploy steps are not chained with `&&`:
[git.md → Git on servers](../git.md#git-on-servers).

## Schema: update, flush, update again

**Basis:** verified against TYPO3 14.3.7 and `helhum/typo3-console` 9.0.1

```bash
vendor/bin/typo3 database:updateschema "*.add"
vendor/bin/typo3 cache:flush
vendor/bin/typo3 database:updateschema "*.add"   # must report nothing left to add
```

Run it on **every** deploy and after **every** import of a database, also when
nothing seems to touch the schema — a dependency update can bring columns
nobody noticed. With nothing to add it costs nothing.

**Why twice.** Since TYPO3 13, columns are created from the TCA
([#101553](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/13.0/Feature-101553-Auto-createDBFieldsFromTCAColumns.html),
*Auto-create DB fields from TCA columns*). `database:updateschema` — a command of
`helhum/typo3-console`, not of the core — boots with caching allowed and reads
the TCA from the cache. Right after a deploy that cache still holds the old
TCA, so the first run adds only part of the new columns, or stops:

- **Silently:** it reports what it added and leaves out the new columns. The
  next command that needs one fails with `Unknown column`.
- **Hard:** a new table whose index refers to a column that comes from the new
  TCA aborts with `InvalidIndexDefinitionException` — a Content Block
  `Collection` is the usual case, see
  [content-blocks.md → A new Collection on deploy](content-blocks.md#a-new-collection-on-deploy).

The flush rebuilds the TCA; the second run then does the remaining work. After
an import it is the other way round — the first run creates what the dump left
out, and only then can the flush run. One sequence covers both.

**Never chain the first run with `&&`.** That it may fail is expected, and the
flush has to run anyway.

### A dropped column: flush right after

**Basis:** observed

Until the cache is flushed, the cached schema still lists a column that a
script has just dropped, and any request that builds its field list from it
fails with `Unknown column`. Run `cache:flush` as the very next command, with
nothing in between.

### A major upgrade: delete the cache, do not flush it

**Basis:** observed

The compiled DI container, the TCA and TypoScript under `var/cache/code/`
survive `composer install`, and `cache:flush` itself needs a working container.
On a major upgrade remove the directory instead:

```bash
rm -rf var/cache/*
```

## Upgrade wizards

**Basis:** verified against `helhum/typo3-console` 9.0.1

- **Name every wizard.** `upgrade:run all` — or an interactive `upgrade:run`
  without an argument, which offers *all* as its default — also runs the wizards
  that were left out on purpose. One of them migrates form definitions from
  files to the database and removes the files.
- **Confirm with `--confirm`, never by piping `yes`:**

  ```bash
  vendor/bin/typo3 upgrade:run myWizard --confirm myWizard
  ```

  A wizard that asks for confirmation takes the default answer under
  `--no-interaction`. When that default is "no", the wizard does nothing — and
  if its confirmation is not marked as required, the console reports
  `Skipped wizard "…" and marked as executed`. It is then never offered again.
- **Check the result in the data**, not in the exit code: the table the wizard
  writes to, or `upgrade:list` afterwards.
- **A wizard whose class moved namespace is offered again**, because its old
  `sys_registry` marker no longer matches. **Basis: observed.** Read what it
  would do before treating it as new work.
- **A rehearsal's wizard list is not the live one.** A staging copy synced
  without `--delete`, or missing a directory, hides wizards that live needs, or
  shows ones live does not. **Basis: observed.**

## Composer on the server

**Basis:** observed

- **A Composer plugin the deploy relies on belongs in `require`**, not in
  `require-dev`. Servers run `composer install --no-dev`; a patch plugin such as
  `cweagans/composer-patches` in `require-dev` is not installed there, and the
  patches silently do not apply.
- **`installed.json` is not evidence.** An aborted `composer install` has
  already written it, so the next run can report "Nothing to install" while the
  files on disk are wrong. Check the files.
- **On a major TYPO3 switch `composer install` can fail once** inside the
  `typo3/class-alias-loader` plugin, because Composer runs the plugin from the
  vendor tree it is replacing (`Class "TYPO3\ClassAliasLoader\…" not found`). Do
  not delete `vendor/`; repair the one package:

  ```bash
  composer reinstall typo3/class-alias-loader --no-plugins --no-scripts
  composer install
  ```

- **Build output inside a Composer package is replaced with the package.** When
  the frontend build writes into `vendor/<package>/Resources/Public/`, a deploy
  that changes that package's version replaces the directory — and the site has
  no CSS and JavaScript until the build runs again. A deploy without a version
  change leaves it alone.

## `SYS/setMemoryLimit` overrides `php.ini`

**Basis:** verified against TYPO3 14.3.7

TYPO3 applies `$GLOBALS['TYPO3_CONF_VARS']['SYS']['setMemoryLimit']` with
`ini_set('memory_limit', …)` during bootstrap, for the CLI and for PHP-FPM
alike. When a process runs out of memory, raising `memory_limit` in `php.ini`
has no effect while this setting is lower — change the setting.

## Data changes

**Basis:** observed

The live database is the master. It flows downwards only — into the local
environment and onto staging — and every import replaces what was changed
there.

- **Record values and content** are maintained in the live backend. A local
  change is a trial, not a delivery.
- **Tables and columns** belong in `ext_tables.sql` or the TCA of the
  extension, and arrive through the schema step above.
- **A change that has to be scripted** — too many records, values derived from
  other data, a structural change — is a script that belongs to its feature:
  - every statement is idempotent
  - it names the schema change it depends on
  - it records the query it uses, and why that query is the right one
  - it runs locally after every import until the feature is deployed, then
    once on live with the deploy
  - it is deleted in the cleanup after that deploy; the history keeps it
