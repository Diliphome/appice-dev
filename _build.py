#!/usr/bin/env python3
"""
Scaffolding generator for the Appice dev portal.

This script emits the static HTML for /index, /sdk/{ios,android,web,react-native}/*,
/api/*, /guides/* — every page shares the same nav, footer, design system and
SEO metadata. To add a page, append it to PAGES below and re-run.

Code samples and API surface are intentionally left as <!-- TODO --> blocks so
engineering can fill verified content; the script does NOT invent SDK signatures.
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent
SITE_URL = "https://dev.appice.ai"
MARKETING_URL = "https://appice.ai"


# ──────────────────────────────────────────────────────────────────────
# CHROME — nav + footer lifted from appice.ai for visual consistency
# ──────────────────────────────────────────────────────────────────────

def nav(rel: str) -> str:
    """Render the top nav. `rel` = relative path prefix to root (e.g. '../')."""
    return f"""<nav class="nav">
  <div class="nav__inner">
    <a href="{rel}index.html" class="nav__logo notranslate" translate="no">
      <img src="{rel}img/appice-logo.png" alt="Appice" style="height:36px;width:auto" loading="eager" decoding="sync" fetchpriority="high">
      <span class="nav__logo-tag">developers</span>
    </a>
    <div class="nav__links">
      <a href="{rel}sdk/index.html">SDKs</a>
      <a href="{rel}api/index.html">API</a>
      <a href="{rel}guides/index.html">Guides</a>
      <a href="{rel}changelog.html">Changelog</a>
    </div>
    <div class="nav__right">
      <a href="{MARKETING_URL}" class="nav__back">← appice.ai</a>
      <button class="nav__search-btn" aria-label="Search documentation">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      </button>
    </div>
    <div class="hamburger"><span></span><span></span><span></span></div>
  </div>
</nav>
<div class="mobile-menu">
  <a href="{rel}sdk/index.html">SDKs</a>
  <a href="{rel}sdk/ios/index.html">— iOS</a>
  <a href="{rel}sdk/android/index.html">— Android</a>
  <a href="{rel}sdk/kotlin/index.html">— Kotlin</a>
  <a href="{rel}sdk/flutter/index.html">— Flutter</a>
  <a href="{rel}sdk/react-native/index.html">— React Native</a>
  <a href="{rel}sdk/web/index.html">— Web</a>
  <a href="{rel}sdk/unity/index.html">— Unity</a>
  <a href="{rel}sdk/cordova/index.html">— Cordova</a>
  <a href="{rel}sdk/ibm-mfp/index.html">— IBM MFP</a>
  <a href="{rel}sdk/kony/index.html">— Kony</a>
  <a href="{rel}api/index.html">API Reference</a>
  <a href="{rel}guides/index.html">Guides</a>
  <a href="{rel}changelog.html">Changelog</a>
  <a href="{MARKETING_URL}">← appice.ai</a>
</div>
<div class="search-overlay" id="searchOverlay">
  <div class="search-box">
    <div class="search-input-row">
      <span class="search-icon-inner"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span>
      <input type="text" class="search-input" placeholder="Search the docs…" autocomplete="off">
      <span class="search-kbd">⌘K</span>
      <button class="search-close-btn" aria-label="Close search"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
    </div>
    <div class="search-results"></div>
  </div>
</div>"""


def footer(rel: str) -> str:
    return f"""<footer class="footer">
  <div class="footer__grid">
    <div class="footer__col footer__brand">
      <a href="{rel}index.html"><img src="{rel}img/appice-logo.png" alt="Appice" class="footer__logo"></a>
      <p class="footer__tagline">Decisioning and execution for regulated enterprises.</p>
      <p class="footer__sub">Developer portal — this is dev.appice.ai.</p>
    </div>
    <div class="footer__col">
      <h4>SDKs</h4>
      <a href="{rel}sdk/ios/index.html">iOS</a>
      <a href="{rel}sdk/android/index.html">Android</a>
      <a href="{rel}sdk/kotlin/index.html">Kotlin</a>
      <a href="{rel}sdk/flutter/index.html">Flutter</a>
      <a href="{rel}sdk/react-native/index.html">React Native</a>
      <a href="{rel}sdk/web/index.html">Web</a>
      <a href="{rel}sdk/unity/index.html">Unity</a>
      <a href="{rel}sdk/cordova/index.html">Cordova</a>
      <a href="{rel}sdk/ibm-mfp/index.html">IBM MFP</a>
      <a href="{rel}sdk/kony/index.html">Kony</a>
    </div>
    <div class="footer__col">
      <h4>API</h4>
      <a href="{rel}api/index.html">Overview</a>
      <a href="{rel}api/authentication.html">Authentication</a>
      <a href="{rel}api/events.html">Events</a>
      <a href="{rel}api/webhooks.html">Webhooks</a>
      <a href="{rel}api/errors.html">Errors</a>
    </div>
    <div class="footer__col">
      <h4>Resources</h4>
      <a href="{rel}guides/index.html">Guides</a>
      <a href="{rel}guides/getting-started.html">Getting started</a>
      <a href="{rel}guides/concepts.html">Concepts</a>
      <a href="{rel}changelog.html">Changelog</a>
      <a href="{MARKETING_URL}">Main site</a>
    </div>
  </div>
  <div class="footer__legal">
    <span>&copy; 2026 Appice</span>
    <a href="{MARKETING_URL}/privacy-policy.html">Privacy</a>
    <a href="{MARKETING_URL}/terms-of-use.html">Terms</a>
    <a href="{MARKETING_URL}/security.html">Security</a>
  </div>
</footer>"""


def head(title: str, description: str, canonical_path: str, rel: str) -> str:
    canonical = f"{SITE_URL}/{canonical_path}".rstrip("/").replace("/index.html", "/")
    breadcrumbs = breadcrumb_jsonld(canonical_path)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/png" href="{rel}img/appice-logo.png">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Appice Developers">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{SITE_URL}/img/og-card.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{SITE_URL}/img/og-card.jpg">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"Appice","url":"{MARKETING_URL}","logo":"{MARKETING_URL}/img/220426_appice_logo.png","sameAs":["https://www.linkedin.com/company/appiceio","https://x.com/appiceio","https://www.youtube.com/@appiceio"]}}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"Appice Developers","url":"{SITE_URL}/"}}</script>
  <script type="application/ld+json">{breadcrumbs}</script>
  <link rel="stylesheet" href="{rel}css/docs.css?v=1">
  <link rel="stylesheet" href="{rel}css/prism.css?v=1">
</head>
<body>"""


def breadcrumb_jsonld(canonical_path: str) -> str:
    """Build a BreadcrumbList JSON-LD from a path like 'sdk/ios/quickstart.html'."""
    parts = canonical_path.replace("index.html", "").strip("/").split("/")
    parts = [p for p in parts if p]
    items = [{"@type": "ListItem", "position": 1, "name": "Developers", "item": f"{SITE_URL}/"}]
    cum = SITE_URL
    for i, p in enumerate(parts):
        cum = f"{cum}/{p}"
        name = p.replace(".html", "").replace("-", " ").title()
        # Friendly names
        if name == "Sdk":
            name = "SDKs"
        elif name == "Api":
            name = "API"
        elif name == "Ios":
            name = "iOS"
        elif name == "React Native":
            name = "React Native"
        items.append({"@type": "ListItem", "position": i + 2, "name": name, "item": cum})
    import json
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})


# Page tail (footer + scripts)
def tail(rel: str) -> str:
    return f"""{footer(rel)}
<script src="{rel}js/docs.js?v=1"></script>
<script src="{rel}js/search.js?v=1"></script>
<script src="{rel}js/prism.js?v=1"></script>
</body>
</html>
"""


# ──────────────────────────────────────────────────────────────────────
# PAGE BODIES
# ──────────────────────────────────────────────────────────────────────

def todo(label: str) -> str:
    """A clearly-marked TODO block engineering must fill."""
    return f"""<div class="todo">
  <div class="todo__label">⚠ TODO — Engineering</div>
  <div class="todo__text">{label}</div>
</div>"""


def home_body() -> str:
    HOME_SDK_ORDER = ["ios","android","kotlin","flutter","react-native","web","unity","cordova","ibm-mfp","kony"]
    pills = "\n      ".join([f'<a href="sdk/{s}/quickstart.html" class="hero__pill">{SDK_META[s]["name"]}</a>' for s in HOME_SDK_ORDER])
    cards = "\n      ".join([
        f'<a href="sdk/{s}/quickstart.html" class="sdk-card">'
        f'<div class="sdk-card__icon">{SDK_META[s]["icon"]}</div>'
        f'<div class="sdk-card__tag">{SDK_META[s]["tag"]}</div>'
        f'<h3 class="sdk-card__name">{SDK_META[s]["name"]}</h3>'
        f'<p class="sdk-card__desc">{SDK_META[s]["blurb"]}</p>'
        f'<span class="sdk-card__cta">Start →</span>'
        f'</a>'
        for s in HOME_SDK_ORDER
    ])
    return f"""<main class="hero hero--dark">
  <div class="hero__inner hero__inner--center">
    <span class="eyebrow eyebrow--light">Appice Developers</span>
    <h1 class="hero__h1 hero__h1--big">Pick your stack. Ship your first decision in 30 minutes.</h1>
    <p class="hero__sub hero__sub--light">SDKs for the apps your customers use. A REST API for the systems behind them. End-to-end guides that connect signal to decision to action.</p>
    <div class="hero__pills">
      {pills}
    </div>
  </div>
</main>

<section class="grid-section">
  <div class="inner">
    <p class="section-eyebrow">SDK Quickstarts — 10 platforms supported</p>
    <div class="sdk-grid">
      {cards}
    </div>
  </div>
</section>

<section class="grid-section grid-section--alt">
  <div class="inner">
    <h2 class="section-title">REST API</h2>
    <p class="section-sub">Send events, identify users and receive webhooks server-side. Pair with the SDKs or use standalone for backend integrations.</p>
    <div class="card-grid card-grid--3">
      <a href="api/authentication.html" class="card">
        <h3 class="card__title">Authentication</h3>
        <p class="card__desc">How to authenticate API requests.</p>
      </a>
      <a href="api/events.html" class="card">
        <h3 class="card__title">Events</h3>
        <p class="card__desc">Send behavioural events server-side.</p>
      </a>
      <a href="api/webhooks.html" class="card">
        <h3 class="card__title">Webhooks</h3>
        <p class="card__desc">Receive real-time decisions and outcomes.</p>
      </a>
    </div>
  </div>
</section>

<section class="grid-section">
  <div class="inner inner--narrow">
    <h2 class="section-title">Need a primer first?</h2>
    <p class="section-sub">If you're new to Appice, start with concepts and the architecture overview before wiring up a SDK.</p>
    <div class="card-grid card-grid--2">
      <a href="guides/concepts.html" class="card">
        <h3 class="card__title">Concepts</h3>
        <p class="card__desc">Sense → Decide → Act → Learn — the vocabulary every Appice integration uses.</p>
      </a>
      <a href="guides/getting-started.html" class="card">
        <h3 class="card__title">Getting started</h3>
        <p class="card__desc">Pick your stack and walk through your first event end-to-end.</p>
      </a>
    </div>
  </div>
</section>"""


def sdk_index_body(sdk_name: str, slug: str, intro: str) -> str:
    return f"""<main class="docs-page">
  <aside class="docs-sidebar">
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">{sdk_name}</div>
      <a href="index.html" class="is-active">Overview</a>
      <a href="quickstart.html">Quickstart</a>
      <a href="reference.html">API reference</a>
      <a href="changelog.html">Changelog</a>
    </div>
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">Other SDKs</div>
      <a href="../ios/index.html">iOS</a>
      <a href="../android/index.html">Android</a>
      <a href="../web/index.html">Web</a>
      <a href="../react-native/index.html">React Native</a>
    </div>
  </aside>
  <article class="docs-body">
    <span class="docs-eyebrow">SDK</span>
    <h1>{sdk_name} SDK</h1>
    <p class="docs-lede">{intro}</p>

    <div class="version-row">
      <span class="version-badge">Latest</span>
      {todo(f"Replace with the latest published version of the {sdk_name} SDK (e.g. <code>v1.4.2</code>) and link to release notes.")}
    </div>

    <h2>Quick links</h2>
    <div class="card-grid card-grid--3">
      <a href="quickstart.html" class="card">
        <h3 class="card__title">Quickstart</h3>
        <p class="card__desc">Install, initialize and send your first event in under 10 minutes.</p>
      </a>
      <a href="reference.html" class="card">
        <h3 class="card__title">API reference</h3>
        <p class="card__desc">Every public method, parameter and return type.</p>
      </a>
      <a href="changelog.html" class="card">
        <h3 class="card__title">Changelog</h3>
        <p class="card__desc">Releases, breaking changes and migration notes.</p>
      </a>
    </div>

    <h2>Compatibility</h2>
    {todo(f"Fill the minimum supported {sdk_name} runtime version (and any deprecated versions) here. Use a small table: Runtime / Min version / Notes.")}

    <h2>Privacy &amp; consent</h2>
    <p>Appice is built for regulated, data-sensitive environments. The {sdk_name} SDK respects user-level consent flags and supports deferred initialization until consent is captured.</p>
    <p>See <a href="../../guides/concepts.html#privacy">privacy &amp; consent in concepts</a> for the model used across all SDKs.</p>

    <h2>Source &amp; releases</h2>
    {todo(f"Link to the GitHub repository (or registry listing) for the {sdk_name} SDK and the canonical release-notes URL.")}
  </article>
</main>"""


def sdk_quickstart_body(sdk_name: str, slug: str, install_hint: str, init_hint: str) -> str:
    return f"""<main class="docs-page">
  <aside class="docs-sidebar">
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">{sdk_name}</div>
      <a href="index.html">Overview</a>
      <a href="quickstart.html" class="is-active">Quickstart</a>
      <a href="reference.html">API reference</a>
      <a href="changelog.html">Changelog</a>
    </div>
  </aside>
  <article class="docs-body">
    <span class="docs-eyebrow">{sdk_name} SDK</span>
    <h1>Quickstart</h1>
    <p class="docs-lede">Install the {sdk_name} SDK, initialize it once at app start, and send your first event.</p>

    <h2>1. Install</h2>
    <p>{install_hint}</p>
    {todo(f"Paste the install command(s) for the {sdk_name} SDK. Include the package manager (CocoaPods, SPM, Gradle, npm, yarn, etc.) and the latest version pin.")}

    <h2>2. Initialize</h2>
    <p>{init_hint}</p>
    {todo("Paste the initialization snippet. Include the API key parameter name, region/endpoint parameter, and any required runtime callbacks. If the SDK supports multiple languages on this runtime (Swift+Obj-C, Kotlin+Java, JS+TS), wrap each in a <code>&lt;div class='tab'&gt;</code> — the tab switcher in <code>js/docs.js</code> handles the rest.")}

    <h2>3. Identify a user</h2>
    {todo("Paste a user-identify snippet showing how to attach a user identifier and basic user properties (email, plan, locale). Note any privacy considerations (PII handling, hashed IDs).")}

    <h2>4. Send your first event</h2>
    {todo("Paste an event-tracking snippet. Use a realistic example event (e.g. <code>app_opened</code> or <code>checkout_started</code>) with 1-2 properties.")}

    <h2>5. Verify</h2>
    {todo(f"Tell the developer how to verify the {sdk_name} SDK is connected — link to the live-events view in the panel, mention the typical 1-2 second latency, and what 'success' looks like.")}

    <h2>Next steps</h2>
    <ul>
      <li><a href="reference.html">Full API reference</a> — every public method.</li>
      <li><a href="../../api/events.html">Server-side events</a> — for backend integrations.</li>
      <li><a href="../../guides/concepts.html">Concepts</a> — Sense / Decide / Act / Learn.</li>
    </ul>
  </article>
</main>"""


def sdk_reference_body(sdk_name: str, slug: str) -> str:
    sections = [
        ("initialization", "Initialization", f"All initialization options the {sdk_name} SDK exposes — API key, region, debug logging, opt-in/opt-out behaviour."),
        ("user-identity", "User identity", "Identifying users, anonymous IDs, alias, logout."),
        ("events", "Events", "Tracking custom events with properties; system events captured by default."),
        ("screens", "Screen tracking", "Automatic vs. manual screen tracking; naming conventions."),
        ("push", "Push notifications", "Registering for pushes; handling rich payloads; deep links."),
        ("inapp", "In-app messages", "Triggering, rendering, and instrumenting in-app campaigns."),
        ("attributes", "User attributes", "Setting profile attributes; supported types; reserved keys."),
        ("consent", "Consent &amp; privacy", "Deferred initialization, opt-out, consent flags, GDPR/DPDP support."),
    ]
    nav_links = "\n      ".join([f'<a href="#{anchor}">{title}</a>' for anchor, title, _ in sections])
    body_sections = "\n\n".join([f'<h2 id="{anchor}">{title}</h2>\n<p>{desc}</p>\n{todo(f"Document every public method in the <em>{title}</em> section. Include the method signature, parameters with types, return type, and a minimal code example. Mark deprecated methods with a callout box.")}' for anchor, title, desc in sections])
    return f"""<main class="docs-page">
  <aside class="docs-sidebar">
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">{sdk_name}</div>
      <a href="index.html">Overview</a>
      <a href="quickstart.html">Quickstart</a>
      <a href="reference.html" class="is-active">API reference</a>
      <a href="changelog.html">Changelog</a>
    </div>
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">On this page</div>
      {nav_links}
    </div>
  </aside>
  <article class="docs-body">
    <span class="docs-eyebrow">{sdk_name} SDK</span>
    <h1>API reference</h1>
    <p class="docs-lede">Every public method exposed by the {sdk_name} SDK. Method signatures use the canonical language for the runtime; toggle between languages with the tab switcher where applicable.</p>

    {body_sections}
  </article>
</main>"""


def sdk_changelog_body(sdk_name: str) -> str:
    return f"""<main class="docs-page">
  <aside class="docs-sidebar">
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">{sdk_name}</div>
      <a href="index.html">Overview</a>
      <a href="quickstart.html">Quickstart</a>
      <a href="reference.html">API reference</a>
      <a href="changelog.html" class="is-active">Changelog</a>
    </div>
  </aside>
  <article class="docs-body">
    <span class="docs-eyebrow">{sdk_name} SDK</span>
    <h1>Changelog</h1>
    <p class="docs-lede">Reverse-chronological log of {sdk_name} SDK releases. Format below: version, date, additions, fixes, breaking changes (if any), migration notes (if breaking).</p>

    <div class="changelog-entry">
      <h2>vX.Y.Z <span class="changelog-date">YYYY-MM-DD</span></h2>
      {todo(f"Replace this template entry with the most recent {sdk_name} SDK release. Use the bullet structure below — Added / Changed / Fixed / Removed / Deprecated. Mark breaking changes with a 🚨 emoji and link to a migration note if needed.")}
      <h3>Added</h3>
      <ul><li>TODO</li></ul>
      <h3>Changed</h3>
      <ul><li>TODO</li></ul>
      <h3>Fixed</h3>
      <ul><li>TODO</li></ul>
    </div>

    <p class="changelog-footer">For releases prior to the start of this changelog, see the <a href="#">GitHub releases page</a>. <em>(TODO: replace with real link.)</em></p>
  </article>
</main>"""


def sdk_index_intro(sdk: str) -> str:
    intros = {
        "ios": "Lightweight Swift and Objective-C client for iOS apps. Captures behavioural events, manages user identity, registers for pushes and renders in-app campaigns.",
        "android": "Lightweight Kotlin and Java client for Android apps. Captures behavioural events, manages user identity, registers for FCM pushes and renders in-app campaigns.",
        "web": "JavaScript and TypeScript client for browsers and progressive web apps. Tracks page views, custom events and user identity; supports web push.",
        "react-native": "Cross-platform React Native client with full behavioural-event parity to the native iOS and Android SDKs. Single API surface, two native runtimes.",
        "kotlin": "Kotlin Multiplatform module that shares the Appice client across iOS, Android and JVM targets from one codebase. Reuses logic, ships native artifacts.",
        "flutter": "Dart package for Flutter apps. Wraps the native iOS and Android runtimes and exposes a single Dart API for tracking, identity, push and in-app.",
        "unity": "C# package for Unity games and apps, distributed via Unity Package Manager. Supports iOS, Android and WebGL build targets.",
        "cordova": "Cordova / PhoneGap plugin that bridges JavaScript calls to the native Appice runtimes on iOS and Android.",
        "ibm-mfp": "IBM MobileFirst Platform adapter — purpose-built for banking-grade MFP deployments. Plugs into the existing MFP runtime and delivery channels.",
        "kony": "Kony / Temenos Quantum module for Indian-bank legacy stacks. FFI bridge into Quantum apps, with per-channel decisioning hooks.",
    }
    return intros[sdk]


def sdk_install_hint(sdk: str) -> str:
    hints = {
        "ios": "Recommended via Swift Package Manager; CocoaPods is also supported.",
        "android": "Recommended via Gradle; minimum Android API level is configured in the SDK's manifest.",
        "web": "Available via npm / yarn for bundled apps; a CDN snippet is also published for static sites.",
        "react-native": "Install via npm or yarn alongside the React Native peer dependency. Native iOS and Android components are linked automatically.",
        "kotlin": "Distributed as a Kotlin Multiplatform Maven artifact. Add the dependency to your shared module's <code>build.gradle.kts</code>.",
        "flutter": "Distributed via <code>pub.dev</code>. Add the package to <code>pubspec.yaml</code>; native iOS and Android components link automatically.",
        "unity": "Distributed via Unity Package Manager (UPM). Import via the package URL in <strong>Window → Package Manager → Add package from git URL</strong>.",
        "cordova": "Distributed via npm as a Cordova plugin. Install with <code>cordova plugin add</code>.",
        "ibm-mfp": "Distributed via the IBM MFP CLI. Install through the MFP adapter mechanism on your MFP server.",
        "kony": "Distributed as a Kony FFI module. Import into your Quantum project via the standard module-add flow.",
    }
    return hints[sdk]


def sdk_init_hint(sdk: str) -> str:
    hints = {
        "ios": "Initialize the SDK once in your <code>AppDelegate</code> (UIKit) or <code>App</code> entry point (SwiftUI), before any tracking calls.",
        "android": "Initialize the SDK once in your <code>Application</code> subclass, before any tracking calls.",
        "web": "Initialize the SDK as early as possible — typically in the &lt;head&gt; for synchronous initialization, or after consent is captured for opt-in flows.",
        "react-native": "Initialize the SDK in your root component's <code>useEffect</code> or in <code>index.js</code>, before any tracking calls.",
        "kotlin": "Initialize the SDK in your shared module's startup function, after platform-specific platform handles are wired up.",
        "flutter": "Initialize the SDK in <code>main()</code> after <code>WidgetsFlutterBinding.ensureInitialized()</code> and before <code>runApp()</code>.",
        "unity": "Initialize the SDK in a bootstrap <code>MonoBehaviour</code> with <code>RuntimeInitializeOnLoadMethod</code>, or in your first scene's <code>Awake</code>.",
        "cordova": "Initialize the SDK in your <code>onDeviceReady</code> handler in <code>www/js/index.js</code>.",
        "ibm-mfp": "Configure the Appice adapter through the standard MFP adapter flow; no client-side init required for backend-driven decisioning.",
        "kony": "Initialize the SDK in your Quantum app's <code>preAppInit</code> or first form's <code>preShow</code> event.",
    }
    return hints[sdk]


# Per-SDK metadata for the home page card grid.
SDK_META = {
    "ios":          {"icon": "📱",  "tag": "iOS · SPM/CocoaPods",       "name": "iOS",            "blurb": "Native iOS SDK. Swift / Objective-C."},
    "android":      {"icon": "🤖",  "tag": "Java/Kotlin · Gradle",       "name": "Android",        "blurb": "Native Android SDK. Kotlin / Java."},
    "web":          {"icon": "🌐",  "tag": "JavaScript · npm / CDN",     "name": "Web",            "blurb": "Browser SDK. JS / TS."},
    "react-native": {"icon": "⚛️",  "tag": "TypeScript · npm",            "name": "React Native",   "blurb": "Wraps native SDKs. RN 0.71+ autolinked."},
    "kotlin":       {"icon": "🅺",   "tag": "KMP · multiplatform",         "name": "Kotlin",         "blurb": "KMP shared module. Reuse logic across iOS &amp; Android."},
    "flutter":      {"icon": "🦋",  "tag": "Dart · pub.dev",              "name": "Flutter",        "blurb": "Dart package. iOS &amp; Android via platform channels."},
    "unity":        {"icon": "🎮",  "tag": "C# · UPM",                    "name": "Unity",          "blurb": "Unity Package Manager. iOS, Android, WebGL."},
    "cordova":      {"icon": "📦",  "tag": "JavaScript · plugin",         "name": "Cordova",        "blurb": "Cordova / PhoneGap plugin. JS bridge to natives."},
    "ibm-mfp":      {"icon": "🏦",  "tag": "Adapter · MFP CLI",           "name": "IBM MFP",        "blurb": "IBM MobileFirst Platform adapter. Banking-grade."},
    "kony":         {"icon": "🛡️",  "tag": "FFI module · Quantum",        "name": "Kony",           "blurb": "Kony / Temenos Quantum module. Indian-bank legacy stack."},
}


# API pages
def api_overview_body() -> str:
    return f"""<main class="docs-page">
  <aside class="docs-sidebar">
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">API</div>
      <a href="index.html" class="is-active">Overview</a>
      <a href="authentication.html">Authentication</a>
      <a href="events.html">Events</a>
      <a href="webhooks.html">Webhooks</a>
      <a href="errors.html">Errors</a>
    </div>
  </aside>
  <article class="docs-body">
    <span class="docs-eyebrow">REST API</span>
    <h1>API overview</h1>
    <p class="docs-lede">Server-side REST API for sending events, identifying users, and receiving real-time decisions via webhooks. Pair with the SDKs for client-side capture, or use standalone for backend integrations.</p>

    <h2>Base URL</h2>
    {todo("Document the base URL(s) for the Appice REST API. List per-region endpoints if the deployment is regional (IN / SEA / MENA / LatAm). Include both the production and any staging URLs.")}

    <h2>Format</h2>
    <p>All requests and responses use <code>application/json</code>. All timestamps are ISO 8601 in UTC unless otherwise noted.</p>

    <h2>Authentication</h2>
    <p>All endpoints require authentication. See <a href="authentication.html">Authentication</a> for details.</p>

    <h2>Rate limits</h2>
    {todo("Document the per-token / per-endpoint rate limits. Include the response headers (<code>X-RateLimit-*</code>) and what happens on exceed (HTTP 429 — link to <a href='errors.html'>Errors</a>).")}

    <h2>Versioning</h2>
    {todo("Document the versioning policy. Include where the version is communicated (URL path, header, or implicit), what counts as a breaking change, and the deprecation notice window.")}

    <h2>Sandbox</h2>
    {todo("If a sandbox/test environment is offered, document how to access it, how it differs from production, and any sandbox-only limitations.")}
  </article>
</main>"""


def api_authentication_body() -> str:
    return f"""<main class="docs-page">
  <aside class="docs-sidebar">
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">API</div>
      <a href="index.html">Overview</a>
      <a href="authentication.html" class="is-active">Authentication</a>
      <a href="events.html">Events</a>
      <a href="webhooks.html">Webhooks</a>
      <a href="errors.html">Errors</a>
    </div>
  </aside>
  <article class="docs-body">
    <span class="docs-eyebrow">REST API</span>
    <h1>Authentication</h1>
    <p class="docs-lede">How API tokens are issued, scoped and presented on requests.</p>

    <h2>Token format</h2>
    {todo("Document the API token format. Is it a JWT? An opaque string? How is it presented — <code>Authorization: Bearer ...</code>, a custom header, or a query parameter? Include a worked example with a placeholder value.")}

    <h2>Issuing tokens</h2>
    {todo("Where do customers issue API tokens — the Appice panel, an admin API call, both? Document the steps and any required role/permission to do so.")}

    <h2>Scopes</h2>
    {todo("Document the scopes / permissions a token can carry. Include the minimum-privilege scope for common operations (write events, read users, manage webhooks).")}

    <h2>Rotation &amp; expiry</h2>
    {todo("Document token rotation: are tokens long-lived or short-lived? Is there a refresh flow? What's the recommended rotation cadence? What happens when a token expires (HTTP 401 — link to <a href='errors.html'>Errors</a>)?")}

    <h2>Storing tokens</h2>
    <p>Never embed an API token in client-side code (mobile binaries, web bundles, public repos). Use the SDKs for client-side capture; reserve the REST API for server-to-server calls.</p>
  </article>
</main>"""


def api_events_body() -> str:
    return f"""<main class="docs-page">
  <aside class="docs-sidebar">
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">API</div>
      <a href="index.html">Overview</a>
      <a href="authentication.html">Authentication</a>
      <a href="events.html" class="is-active">Events</a>
      <a href="webhooks.html">Webhooks</a>
      <a href="errors.html">Errors</a>
    </div>
  </aside>
  <article class="docs-body">
    <span class="docs-eyebrow">REST API</span>
    <h1>Events</h1>
    <p class="docs-lede">Send behavioural events server-side. Use this when capture happens outside a SDK runtime — backend services, batch loaders, server-rendered web, or third-party webhooks you want to relay into Appice.</p>

    <h2>Endpoint</h2>
    {todo("Document the HTTP method and path of the events endpoint (e.g. <code>POST /v1/events</code>). Include the full URL with the base.")}

    <h2>Request body</h2>
    {todo("Schema of the request body. Field-by-field: name, type, required, description, constraints. Use a JSON example. Cover: event name, user identifier, properties map, timestamp, idempotency key.")}

    <h2>Response</h2>
    {todo("Schema of the success response. Include the status code, response body fields, and what 'accepted' vs 'enqueued' vs 'processed' means in the context of the decisioning pipeline.")}

    <h2>Batching</h2>
    {todo("Document the batch endpoint (if separate). Include the maximum batch size, payload size limit, and recommended batching strategy for high-volume backends.")}

    <h2>Idempotency</h2>
    {todo("Document how idempotency works for events. Is there an <code>Idempotency-Key</code> header? How long are idempotency keys remembered? What happens on conflict?")}

    <h2>Errors</h2>
    <p>See <a href="errors.html">Errors</a> for the full status-code reference and error response format.</p>
  </article>
</main>"""


def api_webhooks_body() -> str:
    return f"""<main class="docs-page">
  <aside class="docs-sidebar">
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">API</div>
      <a href="index.html">Overview</a>
      <a href="authentication.html">Authentication</a>
      <a href="events.html">Events</a>
      <a href="webhooks.html" class="is-active">Webhooks</a>
      <a href="errors.html">Errors</a>
    </div>
  </aside>
  <article class="docs-body">
    <span class="docs-eyebrow">REST API</span>
    <h1>Webhooks</h1>
    <p class="docs-lede">Receive real-time decisions and outcomes from Appice at an HTTPS endpoint you control. Use webhooks to wire decisioning into downstream systems — call centres, RM alerts, partner channels, or your own backends.</p>

    <h2>Registering a webhook</h2>
    {todo("Document how to register a webhook destination — UI in the Appice panel, REST endpoint, or both. Include required fields (URL, events to subscribe to, signing secret).")}

    <h2>Event types</h2>
    {todo("List the webhook event types Appice emits. Group by category (decision.*, outcome.*, system.*) and link each to its payload schema.")}

    <h2>Payload format</h2>
    {todo("Document the canonical webhook payload shape. Common envelope fields (id, type, created_at), then the event-specific data block.")}

    <h2>Signature verification</h2>
    {todo("Document the signature header (e.g. <code>X-Appice-Signature</code>), the signing algorithm (HMAC-SHA256 typical), and provide a verification snippet in 1-2 common server languages.")}

    <h2>Retries</h2>
    {todo("Document retry behaviour: which status codes trigger a retry, the backoff curve, the maximum retry duration, and how to detect a redelivery (e.g. an attempt counter in the headers).")}

    <h2>Delivery guarantees</h2>
    {todo("Document the delivery model — at-least-once vs exactly-once. Recommend the consumer pattern (idempotent handler keyed by event id).")}
  </article>
</main>"""


def api_errors_body() -> str:
    return f"""<main class="docs-page">
  <aside class="docs-sidebar">
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">API</div>
      <a href="index.html">Overview</a>
      <a href="authentication.html">Authentication</a>
      <a href="events.html">Events</a>
      <a href="webhooks.html">Webhooks</a>
      <a href="errors.html" class="is-active">Errors</a>
    </div>
  </aside>
  <article class="docs-body">
    <span class="docs-eyebrow">REST API</span>
    <h1>Errors</h1>
    <p class="docs-lede">HTTP status codes and error response format. The codes below are universal; the response body fields are Appice-specific.</p>

    <h2>Status codes</h2>
    <table class="docs-table">
      <thead><tr><th>Code</th><th>Meaning</th><th>Common causes</th></tr></thead>
      <tbody>
        <tr><td><code>200</code></td><td>OK</td><td>Request succeeded.</td></tr>
        <tr><td><code>201</code></td><td>Created</td><td>Resource created.</td></tr>
        <tr><td><code>202</code></td><td>Accepted</td><td>Event accepted for asynchronous processing.</td></tr>
        <tr><td><code>400</code></td><td>Bad Request</td><td>Malformed JSON, missing required field, invalid type.</td></tr>
        <tr><td><code>401</code></td><td>Unauthorized</td><td>Missing, invalid or expired API token.</td></tr>
        <tr><td><code>403</code></td><td>Forbidden</td><td>Token does not carry the required scope.</td></tr>
        <tr><td><code>404</code></td><td>Not Found</td><td>Resource does not exist.</td></tr>
        <tr><td><code>409</code></td><td>Conflict</td><td>Idempotency key collision with a different payload.</td></tr>
        <tr><td><code>422</code></td><td>Unprocessable Entity</td><td>Schema-valid but business-rule-rejected.</td></tr>
        <tr><td><code>429</code></td><td>Too Many Requests</td><td>Rate limit exceeded — see <code>Retry-After</code> header.</td></tr>
        <tr><td><code>500</code></td><td>Internal Server Error</td><td>Server-side failure — retry with exponential backoff.</td></tr>
        <tr><td><code>503</code></td><td>Service Unavailable</td><td>Brief unavailability — retry.</td></tr>
      </tbody>
    </table>

    <h2>Error response body</h2>
    {todo("Document the canonical error response shape. Common pattern: <code>{ error: { code, message, request_id, details } }</code>. Include a worked example for a 400 and a 401.")}

    <h2>Retry strategy</h2>
    <p>For 5xx and 429 responses, retry with exponential backoff. Recommended: initial delay 1s, multiplier 2x, max delay 30s, max attempts 5. Honor the <code>Retry-After</code> header on 429 responses if present.</p>
  </article>
</main>"""


# Guides
def guides_index_body() -> str:
    return f"""<main class="docs-page">
  <aside class="docs-sidebar">
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">Guides</div>
      <a href="index.html" class="is-active">Overview</a>
      <a href="getting-started.html">Getting started</a>
      <a href="concepts.html">Concepts</a>
    </div>
  </aside>
  <article class="docs-body">
    <span class="docs-eyebrow">Guides</span>
    <h1>Guides</h1>
    <p class="docs-lede">Conceptual walkthroughs and end-to-end workflows. Start here if you're new to Appice; jump to the SDK or API reference once you know what you need.</p>

    <div class="card-grid card-grid--2">
      <a href="getting-started.html" class="card">
        <h3 class="card__title">Getting started</h3>
        <p class="card__desc">Pick your stack, install a SDK, send your first event, see it appear in the panel.</p>
      </a>
      <a href="concepts.html" class="card">
        <h3 class="card__title">Concepts</h3>
        <p class="card__desc">Sense → Decide → Act → Learn — the model every Appice integration assumes.</p>
      </a>
    </div>
  </article>
</main>"""


def guides_getting_started_body() -> str:
    return f"""<main class="docs-page">
  <aside class="docs-sidebar">
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">Guides</div>
      <a href="index.html">Overview</a>
      <a href="getting-started.html" class="is-active">Getting started</a>
      <a href="concepts.html">Concepts</a>
    </div>
  </aside>
  <article class="docs-body">
    <span class="docs-eyebrow">Guides</span>
    <h1>Getting started</h1>
    <p class="docs-lede">Install a SDK, send your first event, and verify it lands in the Appice panel — in under 15 minutes.</p>

    <h2>1. Get your API key</h2>
    {todo("Document where customers get their API key — the Appice panel URL, the menu path (Settings → API keys → Create), and any role required to issue keys. Include a screenshot if helpful.")}

    <h2>2. Pick your stack</h2>
    <p>Appice ships SDKs for the four runtimes most enterprise apps use today.</p>
    <div class="card-grid card-grid--4">
      <a href="../sdk/ios/quickstart.html" class="card"><h3 class="card__title">iOS</h3><p class="card__desc">Swift / Objective-C</p></a>
      <a href="../sdk/android/quickstart.html" class="card"><h3 class="card__title">Android</h3><p class="card__desc">Kotlin / Java</p></a>
      <a href="../sdk/web/quickstart.html" class="card"><h3 class="card__title">Web</h3><p class="card__desc">JS / TS</p></a>
      <a href="../sdk/react-native/quickstart.html" class="card"><h3 class="card__title">React Native</h3><p class="card__desc">Cross-platform</p></a>
    </div>
    <p>Server-side? Use the <a href="../api/index.html">REST API</a> directly.</p>

    <h2>3. Send your first event</h2>
    <p>Each SDK quickstart walks you through install, initialize, and a first event. Pick the one that matches your stack above.</p>

    <h2>4. Verify it landed</h2>
    {todo("Document the live-events / debug view in the Appice panel. Include the menu path, what fields show up, and the typical end-to-end latency a developer should see during testing.")}

    <h2>5. What next</h2>
    <ul>
      <li><a href="concepts.html">Concepts</a> — the Sense → Decide → Act → Learn loop your events feed into.</li>
      <li><a href="../api/webhooks.html">Webhooks</a> — receive real-time decisions back at your endpoint.</li>
      <li><a href="../api/index.html">REST API</a> — server-side capture and admin operations.</li>
    </ul>
  </article>
</main>"""


def guides_concepts_body() -> str:
    return f"""<main class="docs-page">
  <aside class="docs-sidebar">
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">Guides</div>
      <a href="index.html">Overview</a>
      <a href="getting-started.html">Getting started</a>
      <a href="concepts.html" class="is-active">Concepts</a>
    </div>
    <div class="docs-sidebar__group">
      <div class="docs-sidebar__head">On this page</div>
      <a href="#sense">Sense</a>
      <a href="#decide">Decide</a>
      <a href="#act">Act</a>
      <a href="#learn">Learn</a>
      <a href="#privacy">Privacy &amp; consent</a>
    </div>
  </aside>
  <article class="docs-body">
    <span class="docs-eyebrow">Guides</span>
    <h1>Concepts</h1>
    <p class="docs-lede">Appice is structured around a four-stage real-time loop. Every SDK call, API request and webhook fires somewhere in this loop.</p>

    <h2 id="sense">Sense</h2>
    <p>Capture every customer signal as it happens — app opens, transactions, drop-offs, support contacts, partner channel events. The SDKs handle client-side capture; the REST API handles server-side capture; both feed the same pipeline.</p>

    <h2 id="decide">Decide</h2>
    <p>The decisioning engine evaluates each signal against rules, segments and propensity models in milliseconds, under your governance policies. Every decision is logged and explainable.</p>

    <h2 id="act">Act</h2>
    <p>Decisions execute across every channel — push, in-app, SMS, WhatsApp, email, web, call centre, RM alerts, partner channels — under 100ms. Webhooks fan out to your downstream systems.</p>

    <h2 id="learn">Learn</h2>
    <p>Outcomes feed back into the decisioning layer. Conversion, engagement and retention metrics improve every decision that follows.</p>

    <h2 id="privacy">Privacy &amp; consent</h2>
    <p>Appice is built for regulated, data-sensitive environments. SDKs support deferred initialization until consent is captured. The REST API supports per-user opt-out and consent flags. Audit-ready logging is on by default.</p>
    {todo("Document the consent model in detail. Cover: how consent flags are passed to the SDKs/API, what happens to events sent before consent, the panel-side controls for managing consented vs. unconsented data, and the supported regulatory frameworks (GDPR, DPDP, CCPA, etc).")}
  </article>
</main>"""


def changelog_body() -> str:
    return f"""<main class="docs-page docs-page--full">
  <article class="docs-body docs-body--wide">
    <span class="docs-eyebrow">Changelog</span>
    <h1>Master changelog</h1>
    <p class="docs-lede">Combined release log across all SDKs and the REST API. Each entry links to the full release notes. For per-SDK changelogs see the SDK-specific pages.</p>

    <div class="changelog-entry">
      <h2>SDK · vX.Y.Z <span class="changelog-date">YYYY-MM-DD</span></h2>
      {todo("Replace this placeholder with the most recent release across any SDK or the API. Use the format: <code>Stack · vX.Y.Z — Date</code>, then a short summary, then a link to the full notes on the SDK-specific changelog page.")}
    </div>

    <p>Per-SDK changelogs:</p>
    <ul>
      <li><a href="sdk/ios/changelog.html">iOS</a></li>
      <li><a href="sdk/android/changelog.html">Android</a></li>
      <li><a href="sdk/web/changelog.html">Web</a></li>
      <li><a href="sdk/react-native/changelog.html">React Native</a></li>
    </ul>
  </article>
</main>"""


def sdk_index_root_body() -> str:
    HOME_SDK_ORDER = ["ios","android","kotlin","flutter","react-native","web","unity","cordova","ibm-mfp","kony"]
    cards = "\n      ".join([
        f'<a href="{s}/index.html" class="sdk-card">'
        f'<div class="sdk-card__icon">{SDK_META[s]["icon"]}</div>'
        f'<div class="sdk-card__tag">{SDK_META[s]["tag"]}</div>'
        f'<h3 class="sdk-card__name">{SDK_META[s]["name"]}</h3>'
        f'<p class="sdk-card__desc">{SDK_META[s]["blurb"]}</p>'
        f'<span class="sdk-card__cta">Open →</span>'
        f'</a>'
        for s in HOME_SDK_ORDER
    ])
    return f"""<main class="docs-page docs-page--full">
  <article class="docs-body docs-body--wide">
    <span class="docs-eyebrow">SDKs</span>
    <h1>Client SDKs</h1>
    <p class="docs-lede">Ten production SDKs covering native mobile, cross-platform, web and the enterprise-banking runtimes our regulated customers run today. All expose the same conceptual API surface — method names differ to match each language's idioms.</p>

    <div class="sdk-grid">
      {cards}
    </div>

    <h2>Choosing the right SDK</h2>
    <ul>
      <li><strong>Native iOS / Android</strong> — single-platform apps or maximum performance.</li>
      <li><strong>Kotlin Multiplatform</strong> — sharing client logic across iOS &amp; Android from one Kotlin codebase.</li>
      <li><strong>Flutter / React Native</strong> — cross-platform Dart or JS codebases. Both have native-parity event capture.</li>
      <li><strong>Web</strong> — browser surfaces (marketing sites, web apps, PWAs). Don't embed inside a native WebView; use a native SDK there.</li>
      <li><strong>Unity</strong> — games and 3D apps. Supports iOS, Android and WebGL build targets.</li>
      <li><strong>Cordova</strong> — legacy hybrid apps that already use the Cordova plugin model.</li>
      <li><strong>IBM MFP / Kony</strong> — banking-grade platforms. Use these only if your stack is already on MobileFirst Platform or Kony / Temenos Quantum.</li>
    </ul>

    <h2>Compatibility and version matrix</h2>
    {todo("Single combined matrix: SDK / latest version / minimum runtime version / supported targets / notes. Engineering owns this — keep it on this page so docs readers can compare without clicking through ten SDK pages.")}
  </article>
</main>"""


# ──────────────────────────────────────────────────────────────────────
# PAGE LIST
# ──────────────────────────────────────────────────────────────────────

PAGES = []  # list of (path, title, description, body_html_fn, rel)

PAGES.append(("index.html",
              "Appice Developers — SDKs, API, Guides",
              "Developer documentation for the Appice real-time decisioning platform. iOS, Android, Web and React Native SDKs, REST API and integration guides.",
              home_body, ""))

PAGES.append(("changelog.html",
              "Changelog — Appice Developers",
              "Release log across all Appice SDKs and the REST API.",
              changelog_body, ""))

PAGES.append(("sdk/index.html",
              "SDKs — Appice Developers",
              "Ten production SDKs across mobile, cross-platform, web and enterprise banking runtimes.",
              sdk_index_root_body, "../"))

# Per-SDK pages — order matches the home-page card grid below.
SDK_LIST = [
    ("ios",          "iOS"),
    ("android",      "Android"),
    ("kotlin",       "Kotlin"),
    ("flutter",      "Flutter"),
    ("react-native", "React Native"),
    ("web",          "Web"),
    ("unity",        "Unity"),
    ("cordova",      "Cordova"),
    ("ibm-mfp",      "IBM MFP"),
    ("kony",         "Kony"),
]
for slug, name in SDK_LIST:
    PAGES.append((f"sdk/{slug}/index.html",
                  f"{name} SDK — Appice Developers",
                  f"Appice {name} SDK overview, compatibility and quick links.",
                  (lambda n=name, s=slug: sdk_index_body(n, s, sdk_index_intro(s))),
                  "../../"))
    PAGES.append((f"sdk/{slug}/quickstart.html",
                  f"{name} SDK Quickstart — Appice Developers",
                  f"Install, initialize and send your first event with the Appice {name} SDK.",
                  (lambda n=name, s=slug: sdk_quickstart_body(n, s, sdk_install_hint(s), sdk_init_hint(s))),
                  "../../"))
    PAGES.append((f"sdk/{slug}/reference.html",
                  f"{name} SDK API reference — Appice Developers",
                  f"Complete API reference for the Appice {name} SDK.",
                  (lambda n=name, s=slug: sdk_reference_body(n, s)),
                  "../../"))
    PAGES.append((f"sdk/{slug}/changelog.html",
                  f"{name} SDK Changelog — Appice Developers",
                  f"Release log for the Appice {name} SDK.",
                  (lambda n=name: sdk_changelog_body(n)),
                  "../../"))

# API pages
PAGES.append(("api/index.html",
              "REST API — Appice Developers",
              "Server-side REST API for sending events, identifying users and receiving webhooks.",
              api_overview_body, "../"))
PAGES.append(("api/authentication.html",
              "API Authentication — Appice Developers",
              "How API tokens are issued, scoped and presented on Appice REST API requests.",
              api_authentication_body, "../"))
PAGES.append(("api/events.html",
              "API Events — Appice Developers",
              "Send behavioural events server-side via the Appice REST API.",
              api_events_body, "../"))
PAGES.append(("api/webhooks.html",
              "API Webhooks — Appice Developers",
              "Receive real-time decisions and outcomes from Appice via webhooks.",
              api_webhooks_body, "../"))
PAGES.append(("api/errors.html",
              "API Errors — Appice Developers",
              "HTTP status codes and error response format for the Appice REST API.",
              api_errors_body, "../"))

# Guides
PAGES.append(("guides/index.html",
              "Guides — Appice Developers",
              "Conceptual walkthroughs and end-to-end workflows for the Appice platform.",
              guides_index_body, "../"))
PAGES.append(("guides/getting-started.html",
              "Getting started — Appice Developers",
              "Install a SDK, send your first event, see it appear in the Appice panel.",
              guides_getting_started_body, "../"))
PAGES.append(("guides/concepts.html",
              "Concepts — Appice Developers",
              "Sense, Decide, Act, Learn — the model every Appice integration assumes.",
              guides_concepts_body, "../"))


# ──────────────────────────────────────────────────────────────────────
# EMIT
# ──────────────────────────────────────────────────────────────────────

def emit():
    for path, title, desc, body_fn, rel in PAGES:
        full_path = ROOT / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        body = body_fn()
        html = head(title, desc, path, rel) + nav(rel) + "\n" + body + "\n" + tail(rel)
        full_path.write_text(html)
        print(f"  + {path}")
    print(f"\n✅ Wrote {len(PAGES)} HTML pages.")


if __name__ == "__main__":
    emit()
