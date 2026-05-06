# CTO Action Plan — `dev.appice.ai`

**Generated:** 7 May 2026
**Owner:** CTO (this is the doc that gets handed to you)
**Status of `dev.appice.ai`:** scaffold deployed, ready for engineering to fill verified content.

---

## 1. State today

**Live:** [https://dev.appice.ai](https://dev.appice.ai). 51 HTML pages. Marketing site at appice.ai now claims **10 GA SDKs** to match the dev portal.

### Already done (no engineering effort needed)

- 51 pages structured in canonical shape (overview / quickstart / reference / changelog per SDK; auth / events / webhooks / errors / rate-limits / OpenAPI for the API).
- Full chrome — nav, footer, search overlay (⌘K), copy buttons, tab switcher (Swift/Obj-C, Kotlin/Java), syntax highlighting (Bash, JSON, JS/TS, HTTP, Swift, Kotlin, Java, Obj-C).
- SEO stack — canonical URLs, OG / Twitter cards, JSON-LD per page (Organization, WebSite, BreadcrumbList), sitemap.xml, robots.txt.
- Cache + security headers via `netlify.toml`.
- 301 redirects from legacy URL patterns to canonical.
- OpenAPI 3 spec at `/openapi/appice-api.yaml`, rendered live at `/api/reference.html` via Redoc.
- Postman collection at `/postman/appice-api.postman_collection.json`.
- 4 reference CI workflows in `/ci-templates/` for SDK-doc generation.
- Three pages with real factual content: `/api/authentication.html`, `/api/rate-limits.html`, `/deprecations.html`.

### What needs engineering effort

Every page has yellow `⚠ TODO — Engineering` callouts marking exact spots that need verified content. Replace each callout's content, delete the callout div, commit.

---

## 2. Risk to mitigate first (within 7 days)

`dev.appice.ai` and `appice.ai` now publicly claim **all 10 SDKs are GA**: iOS, Android, Kotlin (KMP), Flutter, React Native, Web, Unity, Cordova, IBM MFP, Kony.

**If any are not actually GA**, a regulated buyer (IDBI, GIB, MENA banks, SAMA-overseen FIs) will hit a quickstart, ask sales for a release version, and the gap becomes a credibility issue mid-deal.

### Action 0 — CTO sign-off, in writing, per SDK

| SDK | Truly GA? | Last tested release | Maintainer | If not GA, real status |
|---|---|---|---|---|
| iOS | | | | |
| Android | | | | |
| Kotlin (KMP) | | | | |
| Flutter | | | | |
| React Native | | | | |
| Web | | | | |
| Unity | | | | |
| Cordova | | | | |
| IBM MFP | | | | |
| Kony / Quantum | | | | |

If any SDKs are partner-only / beta / pre-GA, drop them from `dev.appice.ai` and `appice.ai` immediately — don't wait for engineering to fill the docs. Contact the dev portal maintainer; this is a 10-minute change.

---

## 3. Action 1 — Fill the 4 customer-facing SDKs first

**Owner:** SDK leads (iOS, Android, Web, RN). **Effort:** 30–45 min/SDK paste-work assuming internal docs already exist.

**Order:** iOS → Android → Web → React Native. These are the SDKs your existing customers (banks, telcos, fintechs serving 10M–200M end users) actually run.

For each, on `/sdk/<name>/`:

| Page | What to fill |
|---|---|
| `index.html` | Latest version pin, min OS / runtime version, source repo / registry link |
| `quickstart.html` | Install command (1 line), initialize snippet, identify-user snippet, first-event snippet, "how to verify in the panel" |
| `reference.html` | Method-list table, paste from internal API docs. Use the `data-tabs` switcher for multi-language (e.g., Swift + Obj-C in one block) |
| `changelog.html` | Last 3–5 releases. Format spec is on the page already |

**Definition of done:** zero `⚠ TODO` callouts on these 4 SDK page sets.

**Time-box:** 1 working day per SDK lead, in parallel = **5 working days**.

---

## 4. Action 2 — Decide and document the other 6 SDKs

**Owner:** CTO + product. **Decision needed first; documentation second.**

For each of: Kotlin (KMP), Flutter, Unity, Cordova, IBM MFP, Kony — pick one of:

- **(A) Promote** — write the docs same as Action 1. Add to all CI templates.
- **(B) Mark partner-only** — keep the page, add a banner *"Partner-managed — contact your account team."* Hide from the public quickstart cards.
- **(C) Mark beta** — keep the page, prefix every method with a beta callout, optionally put behind a sign-in.
- **(D) Remove** — drop from `dev.appice.ai` home, `appice.ai`, sitemap. Engineering cleanup commit takes 10 minutes.

**Recommend timing:** same week as Action 0. Blocking other docs work on this.

---

## 5. Action 3 — Fill the API surface (parallel to Action 1)

**Owner:** Backend / platform lead. **Effort:** 1–2 days total.

The OpenAPI spec is already rendered at `/api/reference.html`. **Confirm or update** the spec at `openapi/appice-api.yaml`.

**Source-of-truth question** — is the YAML in the repo authoritative, or generated from the codebase upstream? If upstream exists, wire CI to publish it on every release (see `ci-templates/`).

Pages to fill:

- `/api/index.html` — base URL(s), regional endpoints, sandbox details, versioning policy.
- `/api/events.html` — request body schema, batching, idempotency.
- `/api/webhooks.html` — registration flow, event types, signature header, retry behaviour.
- `/api/errors.html` — error-response body shape (status codes table is already filled).

---

## 6. Action 4 — Wire CI to keep docs current

**Owner:** DevOps / platform. **Effort:** 1 day.

`ci-templates/` has 4 reference workflows. Pick one pattern per SDK:

- **Push-on-release** — SDK release pipeline emits a changelog entry → opens a PR on `Diliphome/appice-dev` → auto-merges if CI green. **Recommended for the top 4 SDKs.**
- **Weekly sync** — cron pulls latest version metadata from npm / Maven / SPM / UPM and updates the version badges. Recommended for low-churn SDKs.
- **Manual** — engineering opens PRs by hand. Acceptable only for very-low-traffic SDKs (Cordova, Kony if kept).

---

## 7. Action 5 — Owner per surface (write it down)

Without explicit owners the docs go stale within 2 sprints. CTO fills the right column:

| Surface | Owner |
|---|---|
| iOS SDK docs | |
| Android SDK docs | |
| Web SDK docs | |
| React Native SDK docs | |
| Kotlin / Flutter / Unity / Cordova SDK docs | |
| IBM MFP / Kony SDK docs | |
| REST API + OpenAPI spec | |
| Guides + Concepts | |
| Master changelog | |
| Dev portal infrastructure (Netlify, Cloudflare, repo) | |

---

## 8. Action 6 — Process for adding/removing an SDK

`CONTRIBUTING.md` documents the per-page workflow. Add to it:

- **PR review SLA:** 2 business days max.
- **Public-claim discipline:** the 10-SDK list on `dev.appice.ai` and `appice.ai` is the single source of truth. Adding/removing an SDK requires CTO sign-off on a tracked issue, not a freeform PR.
- **Deprecation gate:** removing a published SDK follows the policy at `/deprecations.html` (12 months for SDKs, 6 months for REST endpoints).

---

## 9. Action 7 — Engineering rituals

**Owner:** SDK leads. **Frequency:** every sprint / quarter as noted.

- **Per-release docs gate** (every release) — a SDK release does not ship without its changelog entry merged on `dev.appice.ai`.
- **Quarterly factual audit** (~1 hour per SDK) — walk every SDK page; verify version, install command, initialise snippet still match the latest release.
- **Quarterly link audit** (~10 min) — `npx broken-link-checker https://dev.appice.ai`. Fix red.

---

## 10. Critical-path Gantt (3-week target)

```
Week 1 (now):
  Mon  CTO signs off on which SDKs are truly GA  (Action 0)        [BLOCKING]
  Tue  Drop / hide any non-GA SDKs from public surfaces            [BLOCKING]
  Wed  Assign owners (Action 5)
  Thu–Fri  Top-4 SDK leads start filling /sdk/<name>/ (Action 1)

Week 2:
  Mon–Wed  iOS / Android / Web / RN docs filled (Action 1)
  Wed–Thu  API surface filled (Action 3, parallel to Action 1)
  Fri  CI integration shipped for top-4 SDKs (Action 4)

Week 3:
  Mon–Thu  Decisions on remaining 6 SDKs (Action 2) acted on
  Fri  Quarterly audit ritual added to engineering ops (Action 7)
```

**End state at end of week 3:** dev portal is factually accurate, CI keeps it current automatically for the top 4 SDKs, the rest are explicitly classified, and there is a written process for any future SDK changes.

---

## 11. What CTO cannot delegate

1. **The GA / not-GA decision in Action 0.** Engineering can't unilaterally say *"yes Kony ships"* — that's a public-claim decision and needs the CTO's name on it.
2. **Per-SDK ownership in Action 5.** Without explicit owners the docs rot.
3. **The "what gets dropped from public" call in Action 2.** Otherwise marketing and sales will keep selling against pages that don't have content.

Everything else can flow down.

---

## 12. References

- Live dev portal: [https://dev.appice.ai](https://dev.appice.ai)
- Repo: [https://github.com/Diliphome/appice-dev](https://github.com/Diliphome/appice-dev)
- Deploy logs: Netlify project `appice-dev`
- OpenAPI spec: `/openapi/appice-api.yaml`
- Postman collection: `/postman/appice-api.postman_collection.json`
- CI templates: `/ci-templates/`
- Per-page contribution guide: `CONTRIBUTING.md`
- Original handoff doc (out of date — pre-10-SDK expansion): `CTO_TODO_LIST.md`

---

*This document is generated alongside a PDF copy at `CTO_ACTION_PLAN.pdf`. Both are committed to the repo.*
