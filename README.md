# Appice Developer Portal

Source for **dev.appice.ai** — the developer-facing site covering Appice's SDKs (iOS, Android, Web, React Native), REST API and integration guides.

Static HTML/CSS/JS — no build step. Deploys to Netlify on push to `main`.

---

## Repo layout

```
.
├── index.html              # Landing page
├── changelog.html          # Master changelog (combined)
├── sdk/
│   ├── index.html          # SDKs overview
│   ├── ios/                # iOS SDK pages
│   ├── android/            # Android SDK pages
│   ├── web/                # Web SDK pages
│   └── react-native/       # React Native SDK pages
│   (each: index, quickstart, reference, changelog)
├── api/
│   ├── index.html          # REST API overview
│   ├── authentication.html
│   ├── events.html
│   ├── webhooks.html
│   └── errors.html
├── guides/
│   ├── index.html
│   ├── getting-started.html
│   └── concepts.html
├── css/
│   ├── docs.css            # Main stylesheet
│   └── prism.css           # Code-block syntax-highlight theme
├── js/
│   ├── docs.js             # Hamburger, copy-button, tab switcher
│   ├── search.js           # Search overlay (⌘K)
│   └── prism.js            # Syntax highlighter
├── img/
│   ├── appice-logo.png     # Brand logo (favicon + nav + footer)
│   └── og-card.jpg         # Open Graph / Twitter share image
├── netlify.toml            # Build, cache, and security headers
├── sitemap.xml
├── robots.txt
├── _build.py               # Page-scaffold generator (rerun after adding a page)
├── CONTRIBUTING.md         # How to fill the TODOs and ship a page
└── README.md
```

## Local preview

Any static file server works. The simplest:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Status

This is a **scaffold**. Every SDK page, API page and guide is structured with the right sections in the right order — but actual API surface, code samples, and version numbers are marked **`⚠ TODO — Engineering`** and need to be filled in by the team. See [CONTRIBUTING.md](./CONTRIBUTING.md) for the workflow and conventions.

## Deploy

Pushes to `main` auto-deploy to [https://dev.appice.ai](https://dev.appice.ai) via Netlify (project: `appice-dev`).
