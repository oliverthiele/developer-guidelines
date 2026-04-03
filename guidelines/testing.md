# Testing & Quality Guidelines

Quality assurance rules for TYPO3 projects.

These rules are mandatory unless explicitly overridden.

## Purpose

Ensure consistent code quality and prevent regressions by enforcing
project-aware validation before committing changes.

## Core Principles

- Always inspect the current project first
- Prefer project-defined Composer scripts over direct binary calls
- Prefer the most targeted useful validation scope
- Use full validation only when broader impact is likely
- Stop on first failing required step
- Do not invent missing tools, scripts, or workflows

## Project Detection

Before running any quality checks, inspect the current project setup.

Always check at least:

- root `composer.json`
- available Composer scripts in `composer.json`
- `require-dev` entries in `composer.json`
- relevant config files, such as:
    - `phpstan.neon`
    - `phpstan.neon.dist`
    - `phpunit.xml`
    - `phpunit.xml.dist`
    - `playwright.config.*`
    - `package.json`

## Detection Rules

- Use only tools that are actually installed in the current project
- Do not assume that `phpstan`, `phpunit`, `php-cs-fixer`, `phpcs`, `phpcbf`, `rector`, or `playwright` are available
- If a project provides package-specific scripts, prefer the most targeted script for the affected package
- If a project has no frontend tooling, do not invent a frontend validation workflow
- If Playwright configuration is missing, do not assume Playwright is available
- If a tool is missing, report that clearly instead of silently skipping it

## Execution Context

- PHP, TYPO3, Composer, and most backend-related checks must run via `ddev`, unless the project explicitly defines
  otherwise
- Frontend and E2E tooling may run either via `ddev` or on the host system, depending on the project setup
- Playwright often runs on the host system in local development, but this must be verified per project
- Always follow the current project setup instead of assuming a default environment

## Command Selection Rules

Always prefer project-defined Composer scripts over direct binary calls.

Reasons:

- project-specific configuration stays versioned in Git
- other developers can run the same checks more easily
- the project remains the single source of truth for validation commands
- scripts may already include the correct config files, scopes, or package-specific targets

Use direct binary calls only when:

- no suitable Composer script exists
- a more targeted project-approved command is explicitly needed
- the task requires a narrower scope than the default script provides

## Execution Order

Use the following order when the corresponding tools are available and relevant:

1. Auto-fix and formatting
2. Static analysis
3. Unit / Functional Tests
4. Frontend build or frontend validation
5. E2E tests such as Playwright

## Validation Order (PHP)

For PHP-related validation, use this fixed execution order:

1. php-cs-fixer--dry-run
2. php-codesniffer
3. phpstan

This order is authoritative and must not be overridden in tools or automation.

The PHP validation order applies within the "Auto-fix and formatting" and "Static analysis" steps of the execution order.

All required steps (when applicable) must pass before committing changes.

If any step fails:

- stop execution immediately
- fix the issue before continuing
- do not run subsequent checks

## Validation Scope

### Fast Path

Use for small, isolated changes during development.

Examples:

- run targeted PHPStan for the affected package
- run a package-specific PHPUnit suite
- run one targeted Playwright spec
- run only the relevant frontend build or validation step

### Full Validation

Use before merging, releasing, or after larger refactorings.

Examples:

- run all required formatting and autofix steps
- run project-wide static analysis
- run all relevant PHPUnit suites
- run the relevant frontend build
- run the relevant E2E test suite

## Preferred Workflow

### Step 1: Inspect the project

Identify:

- available Composer scripts
- installed dev tools
- PHP-related config files
- frontend-related config files
- whether the project is a monorepo or package-based setup
- whether the change affects backend logic, frontend behavior, or both

### Step 2: Choose the most targeted checks

Prefer the smallest useful validation scope.

Examples:

- one changed package -> use package-specific static analysis and tests if available
- TYPO3 backend-only change -> usually no Playwright unless UI behavior is affected
- SCSS / JavaScript / Fluid change -> consider frontend build and Playwright if relevant

### Step 3: Escalate when needed

Use broader checks when:

- multiple packages are affected
- shared base packages are changed
- project-wide configuration changes
- release preparation
- previous targeted checks indicate wider impact

## Common Tool Categories

The following categories are common, but not guaranteed to exist in every project.

### Formatting / Autofix

Typical tools:

- `php-cs-fixer`
- `phpcbf`

### Static Analysis

Typical tools:

- `phpstan`
- `phpcs`
- `rector` in analysis or migration workflows

### Tests

Typical tools:

- `phpunit`
- TYPO3 testing framework suites
- project-specific test suites

### Frontend Validation

Typical tools:

- build scripts from `package.json`
- analysis or lint scripts from `package.json`

### E2E Validation

Typical tools:

- `playwright`

## Fallback Behavior

- If a tool is not installed, report it clearly
- If a script is missing, look for an explicit alternative in the project configuration
- If no suitable validation exists for a change type, say so explicitly
- Do not invent missing commands, scripts, or config files
- Do not silently skip validation that should normally happen

## Example Detection Questions

Before running checks, clarify internally:

- Does the root `composer.json` define a script for this tool?
- Is the tool installed in `require-dev`?
- Is there a package-specific script that is more precise?
- Does the project use `ddev` for this command?
- Does the project have a `package.json` or Playwright config?
- Is the current change backend-only, frontend-only, or mixed?

## Do

- Inspect the project before running checks
- Use the most specific available script
- Keep validation proportional to the actual change
- Report clearly what was checked and what was not available
- Stop on first failing required step

## Don't

- Do not assume that every TYPO3 project has the same QA setup
- Do not run generic commands when the project defines a better script
- Do not assume Playwright, PHPUnit, or PHPStan are present
- Do not silently skip missing tools
- Do not install or configure missing tooling without explicit approval
