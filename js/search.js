/* ===========================================================
   APPICE DEV PORTAL — search.js
   Lightweight in-memory search across all docs pages. The PAGES
   index below is hand-maintained; add a row when you add a page.
   ⌘K / Ctrl+K opens the overlay. / also opens (if not in input).
   =========================================================== */
(function () {
  'use strict';

  // Are we at root, or one/two levels deep?
  var path = window.location.pathname;
  var depth = (path.match(/\//g) || []).length - 1; // / -> 0, /api/ -> 1, /sdk/ios/ -> 2
  var ROOT = depth >= 2 ? '../../' : (depth === 1 ? '../' : '');

  // Page index — title + tags = full-text search corpus.
  var PAGES = [
    { title: 'Developer Portal home',          url: ROOT + 'index.html',                            tags: 'overview home start landing' },
    { title: 'Getting started',                url: ROOT + 'guides/getting-started.html',           tags: 'getting started install first event quickstart pick stack' },
    { title: 'Concepts — Sense Decide Act Learn', url: ROOT + 'guides/concepts.html',               tags: 'concepts sense decide act learn loop privacy consent' },
    { title: 'Guides',                         url: ROOT + 'guides/index.html',                     tags: 'guides walkthroughs how-to' },
    { title: 'SDKs',                           url: ROOT + 'sdk/index.html',                        tags: 'sdks ios android web react native client' },
    { title: 'iOS SDK',                        url: ROOT + 'sdk/ios/index.html',                    tags: 'ios swift objective-c iphone ipad cocoapods spm' },
    { title: 'iOS SDK — Quickstart',           url: ROOT + 'sdk/ios/quickstart.html',               tags: 'ios quickstart install initialize swift' },
    { title: 'iOS SDK — API reference',        url: ROOT + 'sdk/ios/reference.html',                tags: 'ios reference methods api swift objc' },
    { title: 'iOS SDK — Changelog',            url: ROOT + 'sdk/ios/changelog.html',                tags: 'ios changelog release notes' },
    { title: 'Android SDK',                    url: ROOT + 'sdk/android/index.html',                tags: 'android kotlin java gradle' },
    { title: 'Android SDK — Quickstart',       url: ROOT + 'sdk/android/quickstart.html',           tags: 'android quickstart install initialize kotlin gradle' },
    { title: 'Android SDK — API reference',    url: ROOT + 'sdk/android/reference.html',            tags: 'android reference methods kotlin java' },
    { title: 'Android SDK — Changelog',        url: ROOT + 'sdk/android/changelog.html',            tags: 'android changelog release notes' },
    { title: 'Web SDK',                        url: ROOT + 'sdk/web/index.html',                    tags: 'web javascript typescript browser pwa' },
    { title: 'Web SDK — Quickstart',           url: ROOT + 'sdk/web/quickstart.html',               tags: 'web quickstart npm cdn javascript' },
    { title: 'Web SDK — API reference',        url: ROOT + 'sdk/web/reference.html',                tags: 'web reference methods javascript typescript' },
    { title: 'Web SDK — Changelog',            url: ROOT + 'sdk/web/changelog.html',                tags: 'web changelog release notes' },
    { title: 'React Native SDK',               url: ROOT + 'sdk/react-native/index.html',           tags: 'react native cross-platform mobile rn' },
    { title: 'React Native — Quickstart',      url: ROOT + 'sdk/react-native/quickstart.html',      tags: 'react native quickstart install initialize npm' },
    { title: 'React Native — API reference',   url: ROOT + 'sdk/react-native/reference.html',       tags: 'react native reference methods' },
    { title: 'React Native — Changelog',       url: ROOT + 'sdk/react-native/changelog.html',       tags: 'react native changelog release notes' },
    { title: 'Kotlin SDK',                     url: ROOT + 'sdk/kotlin/index.html',                 tags: 'kotlin kmp multiplatform shared module gradle' },
    { title: 'Kotlin SDK — Quickstart',        url: ROOT + 'sdk/kotlin/quickstart.html',            tags: 'kotlin kmp quickstart install gradle multiplatform' },
    { title: 'Kotlin SDK — Reference',         url: ROOT + 'sdk/kotlin/reference.html',             tags: 'kotlin reference methods kmp' },
    { title: 'Kotlin SDK — Changelog',         url: ROOT + 'sdk/kotlin/changelog.html',             tags: 'kotlin changelog release notes' },
    { title: 'Flutter SDK',                    url: ROOT + 'sdk/flutter/index.html',                tags: 'flutter dart pub.dev cross platform' },
    { title: 'Flutter SDK — Quickstart',       url: ROOT + 'sdk/flutter/quickstart.html',           tags: 'flutter quickstart install dart pubspec' },
    { title: 'Flutter SDK — Reference',        url: ROOT + 'sdk/flutter/reference.html',            tags: 'flutter reference methods dart' },
    { title: 'Flutter SDK — Changelog',        url: ROOT + 'sdk/flutter/changelog.html',            tags: 'flutter changelog release notes' },
    { title: 'Unity SDK',                      url: ROOT + 'sdk/unity/index.html',                  tags: 'unity c# upm package manager game ios android webgl' },
    { title: 'Unity SDK — Quickstart',         url: ROOT + 'sdk/unity/quickstart.html',             tags: 'unity quickstart install upm package manager' },
    { title: 'Unity SDK — Reference',          url: ROOT + 'sdk/unity/reference.html',              tags: 'unity reference methods c#' },
    { title: 'Unity SDK — Changelog',          url: ROOT + 'sdk/unity/changelog.html',              tags: 'unity changelog release notes' },
    { title: 'Cordova SDK',                    url: ROOT + 'sdk/cordova/index.html',                tags: 'cordova phonegap plugin javascript hybrid' },
    { title: 'Cordova SDK — Quickstart',       url: ROOT + 'sdk/cordova/quickstart.html',           tags: 'cordova quickstart install plugin add' },
    { title: 'Cordova SDK — Reference',        url: ROOT + 'sdk/cordova/reference.html',            tags: 'cordova reference methods javascript' },
    { title: 'Cordova SDK — Changelog',        url: ROOT + 'sdk/cordova/changelog.html',            tags: 'cordova changelog release notes' },
    { title: 'IBM MFP adapter',                url: ROOT + 'sdk/ibm-mfp/index.html',                tags: 'ibm mobilefirst mfp adapter banking enterprise' },
    { title: 'IBM MFP — Quickstart',           url: ROOT + 'sdk/ibm-mfp/quickstart.html',           tags: 'ibm mfp quickstart install adapter cli' },
    { title: 'IBM MFP — Reference',            url: ROOT + 'sdk/ibm-mfp/reference.html',            tags: 'ibm mfp reference methods adapter' },
    { title: 'IBM MFP — Changelog',            url: ROOT + 'sdk/ibm-mfp/changelog.html',            tags: 'ibm mfp changelog release notes' },
    { title: 'Kony SDK',                       url: ROOT + 'sdk/kony/index.html',                   tags: 'kony temenos quantum ffi module banking' },
    { title: 'Kony SDK — Quickstart',          url: ROOT + 'sdk/kony/quickstart.html',              tags: 'kony quickstart install ffi quantum' },
    { title: 'Kony SDK — Reference',           url: ROOT + 'sdk/kony/reference.html',               tags: 'kony reference methods quantum' },
    { title: 'Kony SDK — Changelog',           url: ROOT + 'sdk/kony/changelog.html',               tags: 'kony changelog release notes' },
    { title: 'REST API',                       url: ROOT + 'api/index.html',                        tags: 'rest api overview server-side base url' },
    { title: 'API — Authentication',           url: ROOT + 'api/authentication.html',               tags: 'api authentication token bearer scope' },
    { title: 'API — Events',                   url: ROOT + 'api/events.html',                       tags: 'api events server-side track post idempotency' },
    { title: 'API — Webhooks',                 url: ROOT + 'api/webhooks.html',                     tags: 'api webhooks signature hmac retry' },
    { title: 'API — Errors',                   url: ROOT + 'api/errors.html',                       tags: 'api errors status codes 400 401 429 500' },
    { title: 'API — Reference (OpenAPI / Redoc)', url: ROOT + 'api/reference.html',                 tags: 'api reference openapi swagger redoc spec endpoints schema' },
    { title: 'API — Rate limits',              url: ROOT + 'api/rate-limits.html',                  tags: 'api rate limits 429 quota throttling per workspace' },
    { title: 'Deprecations',                   url: ROOT + 'deprecations.html',                     tags: 'deprecations sunset removed migration sdk version' },
    { title: 'First decision loop (guide)',    url: ROOT + 'guides/first-decision-loop.html',       tags: 'guide tutorial first decision loop end-to-end signal action' },
    { title: 'Sandbox access',                 url: ROOT + 'sandbox-access.html',                   tags: 'sandbox access trial test workspace api keys' },
    { title: 'Changelog (master)',             url: ROOT + 'changelog.html',                        tags: 'changelog release notes versions' }
  ];

  function ensureOverlay() {
    return document.getElementById('searchOverlay');
  }

  var overlay = ensureOverlay();
  if (!overlay) return;
  var input    = overlay.querySelector('.search-input');
  var results  = overlay.querySelector('.search-results');
  var closeBtn = overlay.querySelector('.search-close-btn');

  function open()  { overlay.classList.add('open');  input.value = ''; results.innerHTML = ''; setTimeout(function () { input.focus(); }, 60); }
  function close() { overlay.classList.remove('open'); input.blur(); }

  document.querySelectorAll('.nav__search-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      overlay.classList.contains('open') ? close() : open();
    });
  });
  if (closeBtn) closeBtn.addEventListener('click', close);
  overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });

  document.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); overlay.classList.contains('open') ? close() : open(); }
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault(); open();
    }
    if (e.key === 'Escape' && overlay.classList.contains('open')) close();
  });

  function esc(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

  function run(q) {
    q = q.trim().toLowerCase();
    results.innerHTML = '';
    if (q.length < 2) return;
    var matches = PAGES.filter(function (p) {
      return p.title.toLowerCase().indexOf(q) !== -1 || p.tags.toLowerCase().indexOf(q) !== -1;
    });
    if (!matches.length) {
      results.innerHTML = '<div style="padding:20px 22px;color:rgba(5,13,31,.45);font-size:14px">No results for “<strong>' + esc(q) + '</strong>”</div>';
      return;
    }
    matches.forEach(function (p) {
      var a = document.createElement('a');
      a.className = 'search-result-item';
      a.href = p.url;
      a.innerHTML =
        '<span style="font-weight:700;font-size:15px;color:#050D1F">' + esc(p.title) + '</span>' +
        '<span style="font-size:12px;color:rgba(5,13,31,.45)">' + esc(p.url.replace(/\.html$/, '').replace(/^\.\.?\//, '/')) + '</span>';
      results.appendChild(a);
    });
  }

  input.addEventListener('input', function () { run(this.value); });
  input.addEventListener('keydown', function (e) {
    var items = results.querySelectorAll('.search-result-item');
    if (!items.length) return;
    if (e.key === 'Enter') { e.preventDefault(); items[0].click(); }
  });
})();
