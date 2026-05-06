# Contributing to the Appice Developer Portal

Quick guide for filling the scaffold and shipping new pages. Aimed at engineering — keeps churn low and consistency high.

---

## TL;DR for filling a page

1. Open the page in your editor.
2. Find every `⚠ TODO — Engineering` block (yellow box on the rendered page; `<div class="todo">` in the source).
3. Replace each with verified content — code sample, method signature, version number, etc.
4. Delete the `<div class="todo">…</div>` wrapper once filled.
5. Commit with a concrete message: *"iOS SDK quickstart: install + initialize + first event"*.
6. Push to `main` — Netlify deploys automatically to [dev.appice.ai](https://dev.appice.ai).

That's it. **You don't need to touch CSS, JS, the layout, the SEO tags, the search index, or the navigation.** Those are scaffolded and stable.

---

## Where engineering content goes

| Page | What you fill |
|---|---|
| `sdk/<runtime>/quickstart.html` | Install command, initialize snippet, identify-user snippet, first-event snippet, verification steps |
| `sdk/<runtime>/reference.html` | Every public method: signature, parameters, return type, minimal example, deprecation flags |
| `sdk/<runtime>/changelog.html` | Per-version entry: Added / Changed / Fixed / Removed / Deprecated; mark breaking with 🚨 |
| `sdk/<runtime>/index.html` | Latest version, compatibility matrix (min OS / runtime version), source link |
| `api/index.html` | Base URL(s), rate limits, versioning policy, sandbox details |
| `api/authentication.html` | Token format, header name, scopes, rotation/expiry |
| `api/events.html` | Endpoint, request body schema, response, batching, idempotency |
| `api/webhooks.html` | Registration, event types, payload format, signature, retries, delivery model |
| `api/errors.html` | Error response body schema (status codes already filled) |
| `guides/getting-started.html` | API-key issuance flow, live-events / debug view location |
| `guides/concepts.html` | Consent model details |
| `changelog.html` | Most recent release entry across any SDK or API |

---

## Code samples — use the components

### Single-language code block

```html
<pre><code class="language-swift">
import Appice
Appice.start(apiKey: "…")
</code></pre>
```

Supported language classes: `swift`, `objectivec`, `kotlin`, `java`, `javascript`, `typescript`, `json`, `bash`, `http`.

A copy button is added automatically by `js/docs.js` — no markup needed.

### Multi-language tab switcher (Swift/Obj-C, Kotlin/Java, JS/TS)

```html
<div class="tabs" data-tabs>
  <div class="tabs__buttons">
    <button class="tabs__btn is-active" data-tab="swift">Swift</button>
    <button class="tabs__btn" data-tab="objc">Objective-C</button>
  </div>
  <div class="tabs__panel is-active" data-panel="swift">
    <pre><code class="language-swift">// Swift code</code></pre>
  </div>
  <div class="tabs__panel" data-panel="objc">
    <pre><code class="language-objectivec">// Objective-C code</code></pre>
  </div>
</div>
```

The keys (`swift`, `objc`, etc.) are arbitrary — match `data-tab` to `data-panel`.

### Callout boxes

```html
<div class="callout callout--info">  ℹ Note text. </div>
<div class="callout callout--warn">  ⚠ Warning text.</div>
<div class="callout callout--danger">🚨 Breaking change. </div>
```

---

## Adding a new page

1. Create the HTML file at the desired path. Easiest: copy a sibling page and edit.
2. Make sure these are correct in the new page's `<head>`:
   - `<title>` — concise, ≤60 chars, includes "Appice Developers"
   - `<meta name="description">` — 1 sentence, ≤160 chars
   - `<link rel="canonical" href="https://dev.appice.ai/<path>">`
   - `<meta property="og:url">` matches the canonical
   - JSON-LD `BreadcrumbList` updated to reflect the new path
   - Asset paths (`css/`, `js/`, `img/`) use the right number of `../` for the depth
3. Add the page to:
   - `sitemap.xml` — one `<url>` entry
   - `js/search.js` — one row in the `PAGES` array
4. (Optional) Add a sidebar link on related pages.

If this feels like work, run `python3 _build.py` after adding a row to the `PAGES` list in that file — it regenerates all pages with the right chrome.

---

## Updating the search index

Open `js/search.js`, find the `PAGES` array, add a row:

```js
{ title: 'Your page title', url: ROOT + 'path/to/page.html', tags: 'space-separated keywords' }
```

The search is full-text across `title + tags`. Add 5–10 keywords your audience might search for.

---

## Updating the changelog

Per-SDK changelog at `sdk/<runtime>/changelog.html`. Add a new entry at the **top** (reverse-chronological):

```html
<div class="changelog-entry">
  <h2>v1.5.0 <span class="changelog-date">2026-05-15</span></h2>
  <h3>Added</h3>
  <ul><li>Background session merging on Android 14+.</li></ul>
  <h3>Fixed</h3>
  <ul><li>Race condition during cold-start identify().</li></ul>
</div>
```

Mark a breaking release with 🚨 in the heading and a short migration note immediately below the version line.

---

## Conventions

- **Voice**: technical, clipped, no marketing fluff. Assume a senior engineer reading at 2× speed.
- **Code samples**: realistic and complete (will compile) — no `…` placeholders. Use realistic property names (`userId`, `email`, `plan`) not `foo` / `bar`.
- **Version numbers**: pin them. *"Requires iOS 14+"* not *"requires a recent iOS"*.
- **Compliance language**: keep it factual. *"Logs every decision."* not *"100% audit ready 24/7."*
- **Internal links**: relative paths (`../sdk/ios/index.html`), never absolute `https://dev.appice.ai/...` — those break local preview.

---

## What NOT to change without coordinating

- `css/docs.css` — design system. Touch only with brand sign-off.
- `js/docs.js` / `js/search.js` — feature behaviour. Touch only with maintainer review.
- `netlify.toml` — cache + security headers. Touch only when a header policy changes.
- The nav structure (chrome) — must stay consistent across all pages.

---

## Questions

Open an issue on the repo, or grab one of the maintainers in the engineering channel.
