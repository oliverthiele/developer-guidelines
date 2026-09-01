---
title: Fluid Components — when to use them
scope: typo3
kind: practice
applies_to:
  - "**/Resources/Private/Components/**"
  - "**/Configuration/Fluid/ComponentCollections.php"
  - "**/Configuration/Fluid/Namespaces.php"
typo3: ["13", "14"]
see_also: ["fluid/README.md", "fluid/typo3.md", "typo3/versions.md", "scss.md"]
---

# Fluid Components — when to use them

A **practice guide**, not a rule file. Read it when starting an implementation
that could be a component, not on every Fluid change. It answers which approach
to pick and when deliberately not to — the changelog answers neither.

## Decision

**New markup that has a defined interface and is used more than once becomes a
component.** Structure it along Atomic Design: `Atom`, `Molecule`, `Organism`.

This applies to **newly generated code only**. Existing templates and partials
stay as they are — see [Migration](#migration).

Components are built for **our own code**. Third-party extensions are left
alone, with one exception: if a third-party extension already ships components,
use and extend those instead of building parallel structures.

## When not to

A partial remains the right tool. Do not build a component for:

- structure that only breaks up a single template and appears nowhere else
- fragments that live off ambient context (`{data}`, a specific record) instead
  of explicit arguments
- markup from a third-party extension that does not use components — unless the
  partial is being overridden anyway, in which case own atoms may be used inside
  the override
- anything TypoScript paths point at, as long as nothing else forces the change
- working code that is not being touched for other reasons

The last two are not laziness. Template paths are configured in TypoScript
across many installations; moving a file can break a site that nobody is
currently working on.

## Why

The problem components solve is **one element, defined once, across
extensions**. The failure mode without them is visible in older projects: the
same visual element drifts apart between templates although it should look
identical, because each template carries its own copy of the markup.

Before components existed, the workaround was `<f:section>` plus
`<f:render section="…">` inside one template. That keeps a single template
consistent with itself, but it cannot be reused anywhere else — which is exactly
why such sections are the strongest conversion candidates.

## v13 vs v14

Components exist in both. What differs is the registration effort and the file
naming.

| | v13 (Fluid 4.3+) | v14.1+ |
|---|---|---|
| Registration | custom PHP class extending `AbstractComponentCollection` | `Configuration/Fluid/ComponentCollections.php` |
| Cross-extension | each extension needs its own class and namespace | an extension can add template paths to another extension's collection |
| Template file | `Name/Name.html` | `Name/Name.fluid.html` |

**Validity:** component support since Fluid 4.3 (shipped with v13.4) ·
configuration-based collections since 14.1
([#108508](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.1/Feature-108508-FluidComponentsIntegration.html))
· IDE autocompletion via XSD since 14.2
([#109114](https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/14.2/Feature-109114-AutocompleteForComponentsViaXSDSchema.html))

In a v13 project, keep the existing PHP collection class and its namespace. Do
not migrate namespaces during a version upgrade — that is a separate,
instructed step, because every template referencing the namespace changes with
it.

```php
// v13 — Classes/Components/ComponentCollection.php
final class ComponentCollection extends AbstractComponentCollection
{
    public function getTemplatePaths(): TemplatePaths
    {
        $templatePaths = new TemplatePaths();
        $templatePaths->setTemplateRootPaths([
            ExtensionManagementUtility::extPath(
                'my_theme',
                'Resources/Private/Components/Bootstrap5/'
            ),
        ]);
        return $templatePaths;
    }
}
```

```php
// v14.1+ — Configuration/Fluid/ComponentCollections.php
return [
    'MyVendor\\MyTheme\\Components' => [
        'templatePaths' => [
            10 => 'EXT:my_theme/Resources/Private/Components/Bootstrap5/',
        ],
    ],
];
```

In a v14 project, one collection belongs to the project's sitepackage or theme,
and other extensions add their paths to it. A **distributed** extension is the
exception — it owns its collection, because it cannot depend on a project that
may not exist.

## Conventions

**Folder structure** — flavor folder first, then the Atomic Design level in
**singular**, then one folder per component:

```
Resources/Private/Components/Bootstrap5/
    Atom/Figure/Figure.fluid.html
    Atom/Navbar/Toggler/Toggler.fluid.html
    Molecule/LanguageMenu/LanguageMenu.fluid.html
    Organism/PageHeader/PageHeader.fluid.html
```

The `Bootstrap5/` flavor folder follows the same rule as template root paths in
`../integrator.md` — a single folder name switches the whole set. One folder per
component is Fluid's default and leaves room for a matching CSS or JS file next
to the template.

**Namespace alias** — the integrator decides it per project, and it should be
recognisable at a glance. The established scheme derives the alias from the
source and appends `c` for the component collection: SiteKit's ViewHelpers are
`sk`, its components `skc`. Register it globally so templates need no `xmlns`:

```php
// Configuration/Fluid/Namespaces.php
return [
    'skc' => ['OliverThiele\\OtSitekitbase\\Components'],
];
```

**Arguments are explicit.** A component gets a fresh variable scope containing
only what was passed — variables of the calling template are not visible inside.
Keep the strict API: declare every argument with `<f:argument>` and do not set
`additionalArgumentsAllowed`, which would silently accept undeclared arguments.

**`settings` is the one exception.** Fluid copies `settings` into the component
scope if the parent has it and it was not passed explicitly
(`StandardVariableProvider::getScopeCopy()`). So `{settings}` is available
without being declared. Declaring it anyway is fine and makes the dependency
visible — but never assume the same for any other variable.

## Variants — SiteKit pattern, not a general one

A component with configurable variants can dispatch on a setting and delegate to
sibling components:

```html
<!-- Atom/Navbar/Toggler/Toggler.fluid.html -->
<f:argument name="targetId" type="string" optional="{true}" default="navbarMain"/>
<f:argument name="settings" type="array" optional="{true}" default="{}"/>

<f:switch expression="{settings.sitekit.menus.main.toggler.variant}">
    <f:case value="Animated">
        <skc:atom.navbar.toggler.animated targetId="{targetId}"/>
    </f:case>
    <f:defaultCase>
        <skc:atom.navbar.toggler.default targetId="{targetId}"/>
    </f:defaultCase>
</f:switch>
```

This belongs to **SiteKit**, which is a construction kit meant to produce
different variants of a site from the same base. In a normal customer project it
is usually unnecessary — there, the calling template picks the component
directly. The exception is a deliberate feature switch, e.g. moving to a new
layout behind a setting.

Do not introduce a dispatcher just because a component has two forms. Introduce
it when a **site** should be able to choose between them without touching
templates.

## Converting an existing partial

Signals that a partial or section wants to be a component:

- an `<f:section>` rendered repeatedly via `<f:render section="…">` in the same
  template — it is already a component in everything but name
- the same visual element looks different across templates although it should
  look identical
- the same markup exists in two or more extensions
- a partial that is called with the same four arguments every time

Apply these to extensions in `packages/` of a normal customer instance. In a
monorepo holding many of our own extensions, "the same markup in two extensions"
is expected and not by itself a reason to convert.

Propose conversions, do not perform them unasked. The signals above exist so
that the proposal can be argued rather than felt.

## Migration

Existing partials stay. There is no project-wide conversion, and especially none
while larger construction sites are open.

Convert when a file is being reworked anyway, when one of the signals above
applies, and when nothing in TypoScript depends on the old path.
