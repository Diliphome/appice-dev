# dev.appice.ai — CTO Hand-off

**Last updated:** 6 May 2026
**Author:** Dilip Mistry
**Owner:** Engineering (CTO)
**Goal:** ship `dev.appice.ai` so it's a believable developer portal — and lift the Appice competitive benchmark on Developer / API from 4 → 5.

---

## What's already done (in this repo)

A complete starter for the dev portal is in `Appice/02-dev-portal/`. Every file listed below is commit-ready static HTML, YAML, or JSON. **No build step required** — Netlify serves the repo root as-is.

Final shipped scope from the marketing/strategy side:

- Portal landing (`index.html`) — "Pick your stack" with cards for the four SDK platforms, the API reference, the Postman collection, the first-decision-loop guide, and a sandbox CTA. Uses the same design system as `help.appice.ai` (same `main-nav.css` and `styles.css`, copied in).
- 4 quickstart pages (~5-min onboarding each): iOS, Android, Web, React Native.
- 4 SDK reference shell pages — one per platform — listing the public surface and pointing to where the auto-generated DocC / Dokka / TypeDoc reference will appear.
- API reference page (`api/reference.html`) embedding **Redoc** to render the OpenAPI spec.
- OpenAPI 3 spec (`openapi/appice-api.yaml`) — full draft with 12 endpoints across Ingest, Inform, Webhooks, Segments, Campaigns, Allyvate.
- Postman collection (`postman/appice-api.postman_collection.json`) — generated to match the OpenAPI, ready to "Run in Postman".
- Auth + rate-limits explainer pages.
- 30-minute end-to-end walkthrough (`guides/first-decision-loop.html`) tying SDK → Allyvate → in-app → Inform → webhook into one runnable recipe.
- Sandbox-access form (`sandbox-access.html`) using **Netlify Forms** — no backend needed for v1.
- Changelog and Deprecations pages with policy text.
- 4 GitHub Actions workflow templates (`ci-templates/build-*-docs.yml`) for auto-generating SDK reference HTML from the SDK source repos and committing back to this portal repo.
- 404 page, sitemap.xml, robots.txt, site.webmanifest, _redirects, netlify.toml.

**Recurring cost:** $0 / month.

---

## Open items for engineering

The work below is what remains to make the portal real and self-updating. Items are grouped by where they happen.

---

### A · Repo + Netlify + DNS (1 hour)

#### A1. Create the GitHub repo
- [ ] Create empty repo `Diliphome/appice-dev` (or whatever you'd like to name it — I assumed `appice-dev`, change if needed)
- [ ] **Visibility:** public is fine — there's nothing secret in here. Public also makes it easier for OpenAPI consumers to PR fixes
- [ ] **Default branch:** `main`

#### A2. Push the starter
From your Mac (the agent environment is firewalled from github.com; you push):
```bash
cd "/Users/home/Documents/Claude/Projects/Appice/02-dev-portal"
git init
git remote add origin git@github.com:Diliphome/appice-dev.git
git checkout -b main
git add .
git commit -m "Initial commit — dev portal starter"
git push -u origin main
```

#### A3. Connect Netlify
- [ ] Netlify dashboard → **Add new site → Import from Git**
- [ ] Pick the `Diliphome/appice-dev` repo
- [ ] **Build command:** leave blank
- [ ] **Publish directory:** `.`  (root)
- [ ] Click **Deploy site**
- [ ] Site name: anything — I suggest `appice-dev` so the placeholder URL is `appice-dev.netlify.app` while DNS is pending
- [ ] Wait for the first deploy to complete (should be ~30s)
- [ ] Visit the placeholder URL and confirm the landing page renders

#### A4. Point dev.appice.ai at Netlify
- [ ] Netlify → Site → **Domain management → Add custom domain → `dev.appice.ai`**
- [ ] Netlify will tell you a CNAME target like `<site>.netlify.app`
- [ ] In **GoDaddy DNS** for `appice.ai`:
  - [ ] Add record: type `CNAME`, name `dev`, value `<site>.netlify.app` (whatever Netlify gave you), TTL 1 hour
- [ ] Wait for DNS to propagate (~5–60 minutes — check with `dig dev.appice.ai`)
- [ ] Netlify auto-provisions a Let's Encrypt cert as soon as the CNAME resolves
- [ ] Visit `https://dev.appice.ai` — landing page should render with valid SSL

#### A5. Enable Netlify Forms (for sandbox-access)
- [ ] Netlify → Site → **Forms**. The `sandbox-request` form will appear automatically after the first submission (Netlify auto-detects forms with `data-netlify="true"`)
- [ ] Configure email notifications: Site settings → Forms → Form notifications → **Add notification → Email** → recipient `dev@appice.ai` (or whatever address you want sandbox requests to land in)
- [ ] Optional: add reCAPTCHA via Netlify's form spam-protection setting

---

### B · OpenAPI spec — backend team validation (1–2 weeks elapsed; ~3 dev-days actual work)

The OpenAPI spec at `openapi/appice-api.yaml` is a **draft I wrote based on what I know about the platform**. Your backend team needs to validate it against the actual Node Express implementation. Two ways to do this:

#### B1. Quick path — manual reconciliation
Backend lead reads the spec, lists every discrepancy from the actual implementation. ~1 day.

Specific things to verify:
- [ ] Endpoint paths — I assumed `/v1/events`, `/v1/users`, `/v1/inform/trigger`, etc. Map to actual routes
- [ ] Header names — confirm `X-Appice-Workspace` is the actual header (vs alternatives like `X-Workspace-Id`)
- [ ] Authentication — confirm Bearer-token model is what's actually implemented
- [ ] Region routing — confirm regional hostnames match what's deployed
- [ ] Error codes — verify the actual error response shape matches the `Error` schema
- [ ] Response shapes — sample 1 real response from each endpoint and diff against the spec

#### B2. Better path — generate the spec from code (recommended)
Add `express-jsdoc-swagger` to the Node Express backend so the spec is generated from JSDoc comments on the existing routes. The spec then **stays in sync forever** because it's source-of-truth.

```bash
# in your Node Express repo
npm install express-jsdoc-swagger --save-dev
```

```javascript
// in your Express app entry
const expressJSDocSwagger = require('express-jsdoc-swagger');

expressJSDocSwagger(app)({
  info: { title: 'Appice REST API', version: '5.0.0' },
  baseDir: __dirname,
  filesPattern: './routes/**/*.js',
  swaggerUIPath: '/api-docs',     // for internal preview
  exposeApiDocs: true,
  apiDocsPath: '/openapi.json'    // machine-readable
});
```

Then add JSDoc blocks to every route. Example:

```javascript
/**
 * POST /v1/events
 * @summary Ingest server-side events
 * @tags Ingest
 * @param {EventBatch} request.body.required - Events to ingest
 * @return {IngestResult} 202 - Accepted for processing
 * @return {Error} 400 - Validation failure
 * @return {Error} 401 - Unauthorized
 * @return {Error} 429 - Rate limited
 */
app.post('/v1/events', async (req, res) => { ... });
```

Then export the JSON, convert to YAML, and replace `openapi/appice-api.yaml` in this repo. CI to keep them in sync is straightforward.

- [ ] Decide between B1 (manual, 1 day) and B2 (express-jsdoc-swagger, 2-3 days but durable)
- [ ] Implement
- [ ] Replace `openapi/appice-api.yaml` with the validated/generated version
- [ ] Regenerate the Postman collection from the corrected spec (Postman → Import → OpenAPI URL)

---

### C · SDK reference auto-generation (one-time setup per SDK repo, ~1 day per SDK)

Goal: every release tag of every SDK auto-publishes its reference HTML to `dev.appice.ai/sdk/<platform>/reference/`.

#### C1. iOS SDK repo (`appice-ios`)
- [ ] Confirm the SDK source has DocC-compatible doc comments (`///` triple-slash blocks). If not, add them — minimum on every public type and method
- [ ] Add the workflow file: copy `ci-templates/build-ios-docs.yml` into `.github/workflows/build-ios-docs.yml` of the `appice-ios` repo
- [ ] Add the secret: SDK repo → Settings → Secrets → `APPICE_DEV_PUSH_TOKEN` (fine-grained PAT scoped to `Diliphome/appice-dev` only, `Contents: write`)
- [ ] Run a test build locally: `xcodebuild docbuild -scheme Appice ...`
- [ ] Tag a test release (`v5.0.0-test1`); confirm CI runs and commits to `appice-dev`
- [ ] Verify `https://dev.appice.ai/sdk/ios/reference/` renders the DocC HTML

#### C2. Android SDK repo (`appice-android`)
- [ ] Add Dokka plugin to `build.gradle.kts`:
  ```kotlin
  plugins { id("org.jetbrains.dokka") version "1.9.20" }
  ```
- [ ] Confirm KDoc comments exist on public API
- [ ] Copy `ci-templates/build-android-docs.yml` into `.github/workflows/`
- [ ] Add the same secret
- [ ] Test: `./gradlew :appice-android:dokkaHtml` locally
- [ ] Tag a test release; verify reference HTML lands in `appice-dev`
- [ ] Verify rendering at `https://dev.appice.ai/sdk/android/reference/`

#### C3. Web SDK repo (`appice-web`)
- [ ] Add typedoc as a dev dependency: `npm install --save-dev typedoc`
- [ ] Add `typedoc.json` config to repo root:
  ```json
  {
    "entryPoints": ["src/index.ts"],
    "out": "out-typedoc",
    "name": "Appice Web SDK",
    "navigationLinks": { "Portal": "https://dev.appice.ai" }
  }
  ```
- [ ] Confirm TSDoc comments on public API
- [ ] Copy `ci-templates/build-web-docs.yml` into `.github/workflows/`
- [ ] Add the secret
- [ ] Test: `npx typedoc` locally
- [ ] Tag a release; verify
- [ ] Verify rendering at `https://dev.appice.ai/sdk/web/reference/`

#### C4. React Native SDK repo (`appice-react-native`)
- [ ] Same setup as Web (TypeDoc-based)
- [ ] Copy `ci-templates/build-rn-docs.yml`
- [ ] Verify rendering at `https://dev.appice.ai/sdk/react-native/reference/`

#### C5. (Optional, if you ship them) Other SDKs
For each additional SDK platform you support, create a similar workflow:
- [ ] Flutter — `dart doc` → static HTML
- [ ] Unity — Doxygen → static HTML
- [ ] Server-side Node — TypeDoc (same as web)
- [ ] Python — Sphinx → static HTML

---

### D · Sandbox provisioning workflow (manual at first, automate later)

The sandbox-access form lands as a Netlify Forms submission. v1 workflow is **manual provisioning**; v2 can automate.

#### D1. v1 manual workflow (Week 1)
- [ ] Designate an owner of inbound sandbox requests (DevRel? Solutions? Sales?)
- [ ] Owner receives Netlify Forms email → manually creates a workspace in `panel.appice.io` → emails the requester back with credentials
- [ ] Target turnaround: same business day for verified business addresses
- [ ] Internal SLA tracking — append to a Google Sheet with: timestamp, requester, time-to-credentials, sandbox tier issued

#### D2. v2 self-serve sandbox (Week 4–8)
- [ ] Add a `/api/internal/provision-sandbox` endpoint to the Node Express backend that creates a sandboxed workspace with sample data and emails credentials
- [ ] Hook the Netlify Form submission to that endpoint via Netlify Function
- [ ] Add automated email-domain verification (block free-email TLDs)
- [ ] Result: sandbox credentials in inbox within 60 seconds of form submission

---

### E · Initial backfill of SDK reference HTML (1 hour, before launch)

Until you tag a release of each SDK, the `sdk/<platform>/reference/` folders are empty. To pre-populate:

- [ ] iOS: locally build DocC, copy output into `appice-dev/sdk/ios/reference/`, commit
- [ ] Android: locally build Dokka, same flow
- [ ] Web: locally `npx typedoc`, same flow
- [ ] RN: same as web
- [ ] Push once → portal is fully populated for launch

After the backfill, the CI workflows take over.

---

### F · Optional polish (ship as time allows)

- [ ] **Search** — wire client-side search (Lunr.js or Algolia DocSearch free tier for OSS docs)
- [ ] **Code copy buttons** — single shared JS that adds a copy-icon to every `<pre class="code">` block
- [ ] **Syntax highlighting** — Prism.js via CDN, lazy-loaded
- [ ] **Light analytics** — Plausible (privacy-respecting) or Cloudflare Analytics (free tier) on the portal
- [ ] **Internal preview** — `*.netlify.app` deploy previews on every PR are already enabled by default; consider enabling Netlify Drawer Comments for review
- [ ] **OG image** — generate a portal-specific OG card (different from main site) so when devs share links the preview shows "Appice Developers"

---

### G · Launch checklist (final review before announcing)

- [ ] All four quickstarts walk-through-tested by an engineer who isn't on the SDK team — they should hit zero blockers
- [ ] OpenAPI spec validated against actual implementation (per item B)
- [ ] All 4 SDK reference folders populated (per item E)
- [ ] Sandbox-access form delivers email reliably (test with 3 different email domains)
- [ ] Postman collection imports cleanly and at least 3 endpoints work end-to-end against the sandbox
- [ ] First-decision-loop guide — at least one engineer has run the full 30-minute walkthrough and reports it works
- [ ] All internal `https://appice.ai/...` links from the portal still resolve
- [ ] Lighthouse audit on the portal landing — should score 95+ on Performance, 100 on Accessibility, 100 on Best Practices, 100 on SEO
- [ ] Submit `https://dev.appice.ai/sitemap.xml` to Google Search Console
- [ ] Add `dev.appice.ai` to the main site mega-menu (Resources → Developers) — single line edit in `appice-site` repo
- [ ] Announce on LinkedIn + add to the next sales enablement update

---

## Cost summary

| Item | Cost |
|---|---|
| Domain (already owned) | — |
| Netlify static hosting (free tier) | $0 / month |
| GitHub Actions (free tier covers all 4 SDK doc-gens) | $0 / month |
| Netlify Forms (free tier: 100 submissions/month) | $0 / month |
| Redoc (MIT-licensed, CDN) | $0 / month |
| Apple DocC, Dokka, TypeDoc (open source) | $0 / month |
| **Total recurring** | **$0 / month** |

Upgrade triggers (if/when you hit them):
- Netlify Forms exceeded → Netlify Pro ($19/site/mo) covers 1000 submissions
- Need search → Algolia DocSearch (free for OSS) or self-host MeiliSearch
- Need traffic analytics → Plausible self-hosted ($0) or Cloudflare Analytics ($0)

---

## Reporting

What I'd like to see in the next status update from engineering (in 7 days):

1. URL of the GitHub repo + first commit SHA
2. URL of the Netlify deploy (placeholder + custom domain)
3. Status of OpenAPI validation (spec has been reviewed yes/no; what discrepancies if any)
4. Status of CI workflow setup per SDK (how many of 4 are running)
5. Status of initial reference HTML backfill (how many of 4 are populated)
6. First sandbox request received? (Yes confirms the form is wired end-to-end)

After that, expect re-benchmark to lift the Developer / API dimension from 4 → 5 and overall score from 4.43 → 4.50.

---

## Questions for me

If anything in here is unclear or you'd like to push back on choices (Redoc vs other tools, manual vs auto sandbox, etc.), reply to this doc with comments. I'm available.
