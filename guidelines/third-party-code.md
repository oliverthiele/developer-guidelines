---
title: Third-party code and license comments
scope: frontend
applies_to:
  - "**/webpack.config.js"
  - "**/build.mjs"
  - "**/composer.json"
  - "**/Resources/Public/**/*.js"
  - "**/Resources/Public/**/*.css"
  - "**/Resources/Private/**/*.scss"
  - "**/Build/**/src/**/*.js"
  - "**/Build/**/src/**/*.scss"
  - "**/*.LICENSE.txt"
see_also: ["javascript.md", "scss.md", "documentation.md"]
---
# Third-party code and license comments

How to carry a third-party license through copying, building and minifying. Most
permissive licenses (MIT, BSD, ISC, Apache-2.0) have one condition that matters
here: the copyright and license notice must stay with every copy — including the
minified bundle a website delivers.

## The rule, whatever the tool

Every license notice that is in the source must arrive in what is delivered:
either in the built file itself, or in a license file deployed next to it that
the built file names.

- Mark the notice so that every tool recognises it — `/*! … */`, see below
- Never configure a build step to drop license comments
- **Check the built files, not the configuration.** A correct configuration is
  not enough: a minifier can still lose a notice (see *Terser drops notices on
  inlined code* below)

This holds for any build tool, including one this file does not list. For a tool
not listed here, find out how it treats license comments and check its output
before relying on it.

## `/*!` marks a comment as a license comment

**Basis:** verified against terser-webpack-plugin 5.6.1 (terser 5.51.2),
esbuild 0.28.2, sass 1.105.1 and postcss-discard-comments 7.0.8
(cssnano-preset-default 7.0.17)

A block comment that starts with `/*!` is a "loud" or "important" comment. The
build tools keep it by default:

| Tool | Default |
|---|---|
| Sass, any output style | keeps `/*! … */`; `compressed` drops `/* … */`; `//` never reaches the CSS |
| cssnano (`discardComments`) | keeps `/*! … */`, drops all other comments |
| Terser via terser-webpack-plugin | moves license comments into `[name].js.LICENSE.txt` and puts a `/*! For license information please see … */` banner on top of the bundle |
| esbuild, JS and CSS (`legalComments`) | keeps license comments in the file — inline without `bundle`, at the end of the file with `bundle: true` |

In JavaScript, Terser and esbuild also treat `//!`, `// @license` and
`/* @preserve */` as license comments. In Sass, every `//` comment disappears in
the first compile. Write `/*!` everywhere: it is the one form all four tools
keep, so a notice survives when a file moves from JavaScript to a stylesheet
build or to another tool.

## Build configuration — never strip license comments

**Basis:** verified against terser-webpack-plugin 5.6.1 (terser 5.51.2),
esbuild 0.28.2 and postcss-discard-comments 7.0.8 (cssnano-preset-default 7.0.17)

webpack:

```js
// Correct
new TerserPlugin({
  terserOptions: {
    format: {
      comments: false,
    },
  },
  // Move license comments (/*! … */, @license, @preserve) into
  // [name].js.LICENSE.txt next to the bundle, referenced by a banner
  extractComments: true,
}),
new CssMinimizerPlugin({
  minimizerOptions: {
    preset: [
      'default',
      {
        // removeAll: false keeps /*! … */ license comments, drops all others
        discardComments: {removeAll: false},
      },
    ],
  },
}),
```

```js
// Wrong — removes every license notice from the delivered files
extractComments: false,
terserOptions: {format: {comments: false}},
// …
discardComments: {removeAll: true},
```

esbuild (the `build.mjs` setup from `javascript.md` and `scss.md`):

```js
// Correct — no legalComments option: notices stay in the built file
await build({
  entryPoints: ['Resources/Private/JavaScript/CountUp.ts'],
  outfile: 'Resources/Public/JavaScript/CountUp.min.js',
  minify: true,
});
```

```js
// Wrong — removes every license notice
legalComments: 'none',
// Wrong unless the .LEGAL.txt is deployed — moves the notices into
// [name].LEGAL.txt and leaves no reference in the built file
legalComments: 'external',
```

Rules:

- A minifier used without license-related options (`new TerserPlugin()`,
  `new CssMinimizerPlugin()`, esbuild without `legalComments`) already behaves
  correctly — leave it that way
- `comments: false` in `terserOptions.format` is fine **only together with**
  `extractComments: true`; with `extractComments: false` it drops the notices
- `extractComments: false` alone keeps the notices inline — allowed, but it
  changes the default for no gain
- esbuild `legalComments: 'linked'` is fine: it writes `[name].LEGAL.txt` and a
  `/*! For license information please see … */` banner, like Terser's extraction
- A separate license file (`.LICENSE.txt`, `.LEGAL.txt`) has to be deployed. A
  deployment that copies single files instead of the asset folder has to include
  it
- CSS has no extraction step in webpack; the `/*! */` comments stay inline. That
  is the normal case and costs a few hundred bytes

### Terser drops notices on inlined code

**Basis:** verified against terser-webpack-plugin 5.6.1 (terser 5.51.2)

Terser attaches a comment to the code that follows it. When the minifier inlines
or removes that code — a small helper function called once is enough — the
comment goes with it. No `.LICENSE.txt` is written and no banner is set; the
configuration is correct and the notice is still gone. esbuild 0.28.2 kept the
notice in the same case.

When the check below finds a notice missing, add it back as a banner on the
bundle and keep the header in the vendored file. webpack's `BannerPlugin` wraps
its text in `/*! … */`, and Terser then extracts it into the `.LICENSE.txt` like
any other notice. With esbuild, pass the comment itself:
`banner: {js: '/*! … */'}`.

### Check the built files

Search the built files for each copyright holder from the vendored headers, not
only for `/*!` — a count of license comments does not show which one is missing:

```bash
grep -l 'Jane Doe' path/to/Assets/JavaScript/* path/to/Assets/Styles/*
```

Every vendored file must show up — in the bundle, or in its `.LICENSE.txt` or
`.LEGAL.txt`.

## Copying a third-party file into a package or project

Applies to a vendored script, a copied stylesheet, and an SCSS file derived from
one — anything not installed through npm or Composer, where the license would
travel with the package.

1. **Header as a `/*! */` comment** at the top of the file, containing:
   - the name and the source URL
   - the version, tag or commit it was taken from
   - the copyright line
   - for short licenses (MIT, BSD, ISC): the full license text; for long ones
     (Apache-2.0, MPL-2.0): the SPDX identifier and the path of the license file
2. **License file next to it**, verbatim from upstream: `Name.LICENSE.txt` beside
   `Name.js`. It documents the license for the package; the header carries it
   into the bundle.
3. **Say whether it was changed.** "unchanged below this comment" or a short list
   of what differs. Keep a verbatim copy byte-identical below the header, so a
   `diff` against upstream stays empty.
4. **Do not invent the copyright holder.** Some upstream `LICENSE` files leave the
   name empty. Take it from upstream's `package.json` (`author`) or its `dist`
   header. If upstream names nobody, write the copyright line as upstream has it.

The header has to be a comment the build keeps, so that the notice reaches the
bundle; the license file is what a reader of the package finds. Both are needed
because the bundle does not ship the license file and the package does not
ship the bundle.

```js
/*!
 * Some Library - what it does
 * https://github.com/acme/some-library
 * src/js/some-library.js at commit 1a2b3c4, unchanged below this comment.
 *
 * MIT License
 *
 * Copyright (c) 2018 Jane Doe
 *
 * Permission is hereby granted, free of charge, …
 * (full MIT text)
 */
```

A file that already carries its notice in its own syntax — an SVG icon with
`<!--! … -->` — keeps it. Do not strip it when optimising the file.

## Composer `license` and the README

**Basis:** documented — [Composer schema: `license`](https://getcomposer.org/doc/04-schema.md#license)

- **Do not add the third-party license to `composer.json`.** Several entries in
  `license` mean *the user may choose one of them* (disjunctive), not *both apply*.
  `["GPL-2.0-or-later", "MIT"]` would offer the whole package under MIT.
  MIT, BSD and ISC code may be part of a GPL package; the package license stays.
- **Name the third-party parts in the README**, below the package license — see
  `documentation.md` → *License section*:

  ```markdown
  ## License

  GPL-2.0-or-later — see [LICENSE](LICENSE)

  Third-party parts:

  | Files | Source | License |
  |---|---|---|
  | `Resources/Public/JavaScript/SomeLibrary.js` | [acme/some-library](https://github.com/acme/some-library), © 2018 Jane Doe | MIT — see [SomeLibrary.LICENSE.txt](Resources/Public/JavaScript/SomeLibrary.LICENSE.txt) |
  ```

## Shipped SCSS must not reference files by relative path

**Basis:** verified against webpack 5.107.2 and sass-loader 17.0.0

An SCSS file that an extension ships for projects to load with `@use` must build
from any entry point. A relative `url('../../Public/Icons/arrow.svg')` is
resolved against the **importing** build, not the extension, so the build breaks
with `Cannot find module` — and the error may only show with webpack's error
stats.

- Small icons: embed them as a data URI
- Larger assets: a `!default` variable for the base path, which the project sets

Note the origin of an embedded icon in a comment, and its license in the file
header when it is third-party.
