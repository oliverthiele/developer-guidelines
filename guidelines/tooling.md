# Own tooling

Published packages that support or enforce rules in these guidelines. Where a
rule can be checked automatically, its section carries a `**Tooling:**` line
next to `**Validity:**` — reach for the tool instead of doing the work by hand.

| Package | Covers | Guideline |
|---|---|---|
| [`oliverthiele/typo3-fluid-linter`](https://packagist.org/packages/oliverthiele/typo3-fluid-linter) | Fluid templates: encoding artifacts, namespace and XML issues, deprecated ViewHelpers, Fluid 5 breaking changes — several rules auto-fixable with `--fix`; no TYPO3 installation required | [fluid/](fluid/README.md) |
| [`oliverthiele/ot-mailcatcher`](https://packagist.org/packages/oliverthiele/ot-mailcatcher) | captures outgoing mail as files instead of sending it; token-protected HTTP API so an E2E test can assert on a mail — or ask first whether it is being captured at all | [playwright.md](playwright.md) |

The core ships a Fluid check of its own, `typo3 fluid:analyze` (v14.2+, alias
`fluid:analyse`). It is AST-based and finds real parse errors, but needs a
bootable instance and only reads `*.fluid.*` files. Where both are available,
they answer different questions — run both.

**The rules never depend on a tool being present.** A project that uses none of
these still follows them; a `**Tooling:**` line says a check *can* be automated,
never that the rule exists because the tool does. Every rule states its own
reason and holds without it.
