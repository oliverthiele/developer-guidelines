# Playwright Guidelines

Patterns and conventions for Playwright tests in TYPO3 projects.

For QA workflow, tool detection, and execution order see `testing.md`.

---

## Directory structure

```
tests/
  functional/          functional tests — no screenshots
  visual/              visual regression tests — screenshots committed to git
  helpers/             shared utilities imported by all specs
    fixtures.ts        custom test fixture (window.__playwright injection)
    page-setup.ts      overlay hiding helpers
    urls.ts            URL map with DDEV/Live environment handling
    errors.ts          expectNoError() for TYPO3/PHP error detection
```

Always import `test` and `expect` from `helpers/fixtures.ts`, not directly from
`@playwright/test`. The custom fixture injects `window.__playwright` before any
page script runs.

---

## Custom fixture — `window.__playwright`

```typescript
// helpers/fixtures.ts
export const test = base.extend({
    page: async ({page}, use) => {
        await page.addInitScript(() => {
            (window as unknown as Record<string, unknown>)['__playwright'] = true;
        });
        await use(page);
    },
});
```

The flag is injected via `addInitScript()` — it is present before any page
JavaScript executes. Frontend components check this flag to suppress UI elements
that interfere with visual snapshots (scroll-to-top buttons, modals, etc.):

```javascript
// In the component JS:
if (!window.__playwright) {
    showScrollToTopButton();
}
```

Use `window.__playwright` for suppression at the source. Use CSS `display: none`
via `page.evaluate()` only for third-party elements where source access is not
possible (e.g. cookie banners).

---

## Hiding overlays before screenshots

Two helper functions handle different screenshot scopes:

```typescript
// helpers/page-setup.ts

// Use for full-page screenshots — hides cookie banner AND footer
hideOverlays(page)

// Use for element-scoped screenshots — hides only cookie banner
// (so the element under test is not accidentally hidden)
hideFloatingElements(page)
```

Rule: always call the appropriate helper between `page.goto()` and
`expect(page).toHaveScreenshot()`. Never skip it — overlays will cause false
positives on every run.

---

## Visual regression tests

```typescript
import {test, expect} from '../helpers/fixtures';
import {hideOverlays} from '../helpers/page-setup';

test.describe('Homepage', () => {
    test('English — full page', async ({page}) => {
        await page.goto('/', {waitUntil: 'networkidle'});
        await hideOverlays(page);
        await expect(page).toHaveScreenshot('home-en.png', {fullPage: true});
    });
});
```

Rules:

- Always use `waitUntil: 'networkidle'` for pages with AJAX-driven components
  (Vue apps, lazy-loaded content). Without it, the screenshot is taken before
  rendering is complete.
- On static pages without AJAX, prefer `waitUntil: 'domcontentloaded'` or wait
  for a specific locator (`page.locator('...').waitFor()`) — `networkidle` can
  cause flaky tests on CI when external resources (fonts, tracking) respond slowly.
- Always use `{ fullPage: true }` for full-page screenshots.
- Omit `{ fullPage: true }` for element-scoped screenshots (the locator already
  defines the crop area).

### Element screenshot (isolation)

Test unstable elements (SVGs, complex CSS) in isolation as element screenshots
rather than full-page. This avoids false positives in unrelated tests while
still
catching regressions in the element itself.

```typescript
import {hideFloatingElements} from '../helpers/page-setup';

test('Footer — element screenshot', async ({page}) => {
    await page.goto('/', {waitUntil: 'networkidle'});
    await hideFloatingElements(page);    // not hideOverlays — footer must stay visible

    const footer = page.locator('#pagefooter');
    await expect(footer).toHaveScreenshot('footer.png');
});
```

### State isolation before screenshots

Clear persistent state (localStorage, sessionStorage, cookies) before tests that
involve components retaining state across runs:

```typescript
test('Initial state — no filters selected', async ({page}) => {
    await page.addInitScript(() => localStorage.clear());

    await page.goto('/product-selector', {waitUntil: 'networkidle'});
    await hideOverlays(page);
    await expect(page).toHaveScreenshot('product-selector-initial.png', {fullPage: true});
});
```

### Reference screenshots

Reference screenshots are stored in `*.spec.ts-snapshots/` next to the spec file
and committed to Git.

Filename pattern: `{name}-{viewport-project}-{os}.png`
Example: `home-de-Desktop-Chrome-darwin.png`

Regenerate references after intentional visual changes:

```bash
npm run test:update
```

Commit the updated snapshots together with the code change that caused them.

---

## Functional tests

Functional tests verify behavior without screenshots. Always call
`expectNoError()`
after `page.goto()` to catch TYPO3 and PHP error pages before the actual
assertion.

```typescript
import {test, expect} from '../helpers/fixtures';
import {url} from '../helpers/urls';
import {expectNoError} from '../helpers/errors';

test.describe('Product detail', () => {
    test('Detail page — heading and key data are present', async ({page}) => {
        await page.goto(url('productDetail'), {waitUntil: 'networkidle'});

        await expectNoError(page);

        await expect(page.locator('h1')).toContainText('Expected heading');
        await expect(page.locator('[data-js="productSerialNumber"]')).toBeVisible();
    });
});
```

### 404 and error status tests

Test error responses explicitly via the return value of `page.goto()`:

```typescript
test('Unknown record — returns 404 without PHP exception', async ({page}) => {
    const response = await page.goto('/record/00000000-0000-0000-0000-000000000000');

    expect(response?.status()).toBe(404);
    await expectNoError(page);    // confirms no PHP exception is shown on the error page
});
```

### Bug regression tests

Link every regression test to its origin in the file-level comment block:

```typescript
/**
 * Regression for bug #1234567: MyAction threw PageNotFoundException
 * ("No configuration specified.") when no `config` argument was present.
 */
```

This makes it possible to trace why a test exists and whether it can be removed
if the underlying code is later refactored.

---

## TYPO3/PHP error detection — `expectNoError()`

```typescript
// helpers/errors.ts
const ERROR_PATTERNS = [
    'Oops, an error occurred!',
    'Uncaught TYPO3 Exception',
    'TYPO3 Exception',
    'PHP Fatal error',
    'PHP Warning:',
    'PHP Notice:',
    '500 Internal Server Error',
] as const;

export async function expectNoError(page: Page): Promise<void> {
    for (const pattern of ERROR_PATTERNS) {
        await expect(page.locator('body'), `Page must not contain: "${pattern}"`).not.toContainText(pattern);
    }
}
```

Call `expectNoError()` in every test after `page.goto()` — both in functional
and in visual tests where rendering depends on backend data.

TYPO3 Admin Panel: disable it for the test user via TSconfig (`admPanel = 0`).
If active, TYPO3 injects additional markup and styles that break visual
regression tests.

---

## URL management — `helpers/urls.ts`

Centralise all test URLs in `helpers/urls.ts`. Never hardcode paths inside spec
files.

```typescript
const paths = {
    home: '/',
    productList: '/products',
    productDetail: '/products/example-product',
} satisfies Record<string, PathEntry>;

export function url(key: keyof typeof paths): string { ...
}
```

When DDEV and Live use different slugs (e.g. after a slug migration), use the
object form:

```typescript
productDetail: {
    ddev: '/products/example-product',
    live: '/en/products/example-product',
}
```

Default to a plain string — only use the object form when paths actually differ.

---

## Test naming

```
test.describe('Component or page name', () => {
    test('Subject — variant or state', ...)
})
```

Examples:

- `'English — full page'`
- `'Footer — element screenshot'`
- `'Detail page — heading and key data are present'`
- `'Unknown record — returns 404 without PHP exception'`

The describe label names the feature. The test label names the specific case and
distinguishes it from sibling tests in the same describe block.

---

## Playwright config

Key settings in `playwright.config.ts`:

| Setting             | Value             | Reason                                                     |
|---------------------|-------------------|------------------------------------------------------------|
| `fullyParallel`     | `true`            | each spec file runs in its own worker                      |
| `retries`           | `1`               | catches cold-start timeouts; a real regression fails twice |
| `workers`           | `1` local, `2` CI | easier to follow locally                                   |
| `screenshot`        | `only-on-failure` | shows exactly what the browser saw                         |
| `video`             | `on-first-retry`  | helps diagnose transient failures                          |
| `maxDiffPixelRatio` | `0.002`           | tolerates sub-pixel rendering differences                  |

`baseURL` is read from `process.env.BASE_URL`, defaulting to the DDEV hostname.
Run against Live by passing the environment variable:

```bash
BASE_URL=https://example.com npm test
```

### Viewport projects

Two viewports are defined by default:

| Project        | Config                                  |
|----------------|-----------------------------------------|
| Desktop Chrome | `Desktop Chrome`, viewport `1440 × 900` |
| Mobile Safari  | `iPhone 13` (devices preset)            |

Reference screenshots are generated and stored per project and OS:
`home-en-Desktop-Chrome-darwin.png`, `home-en-Mobile-Safari-darwin.png`.

---

## Login for access-protected pages

Authenticate once in a global setup routine and reuse the browser state via
`storageState`. Do not re-authenticate before every test.

```typescript
// helpers/global-setup.ts
import {chromium, FullConfig} from '@playwright/test';

async function globalSetup(config: FullConfig) {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    await page.goto(process.env['BASE_URL'] + '/login');
    await page.locator('[data-js="username"]').fill(process.env['TEST_USERNAME'] ?? '');
    await page.locator('[data-js="password"]').fill(process.env['TEST_PASSWORD'] ?? '');
    await page.locator('[data-js="submitLogin"]').click();

    await page.context().storageState({path: 'tests/helpers/auth-state.json'});
    await browser.close();
}

export default globalSetup;
```

Register the setup in `playwright.config.ts`:

```typescript
export default defineConfig({
    globalSetup: './tests/helpers/global-setup.ts',
});
```

Use in protected spec files:

```typescript
test.use({storageState: 'tests/helpers/auth-state.json'});

test('Protected page — content is visible', async ({page}) => {
    await page.goto('/members-area', {waitUntil: 'networkidle'});
    await expectNoError(page);
    await expect(page.locator('h1')).toBeVisible();
});
```

Never hardcode credentials. Always read them from environment variables.
Add `tests/helpers/auth-state.json` to `.gitignore`.

---

## Masking dynamic content

TYPO3 pages often include dynamic elements (news teasers, timestamps, random
items) that change between runs and cause false positives in visual tests. Mask
these elements instead of hiding them:

```typescript
test('Homepage — full page with masked dynamic elements', async ({page}) => {
    await page.goto('/', {waitUntil: 'networkidle'});
    await hideOverlays(page);

    await expect(page).toHaveScreenshot('home.png', {
        fullPage: true,
        mask: [
            page.locator('[data-js="latestNews"]'),
            page.locator('[data-js="currentDate"]'),
        ],
    });
});
```

Masked areas are replaced with a solid colour in the snapshot — the surrounding
layout is still compared. Use `mask` instead of `display: none` so the layout
impact of the element is preserved in the test.
