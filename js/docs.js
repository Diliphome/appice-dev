/* ===========================================================
   APPICE DEV PORTAL — docs.js
   Hamburger menu, sidebar active-link, code-block copy buttons,
   and tab switcher (Swift/Obj-C, Kotlin/Java, JS/TS, etc).
   =========================================================== */
(function () {
  'use strict';

  // ── Hamburger toggle ─────────────────────────────────────
  var hamburger = document.querySelector('.hamburger');
  var mobileMenu = document.querySelector('.mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', function () {
      mobileMenu.classList.toggle('open');
      hamburger.classList.toggle('active');
    });
    document.addEventListener('click', function (e) {
      if (!mobileMenu.contains(e.target) && !hamburger.contains(e.target)) {
        mobileMenu.classList.remove('open');
        hamburger.classList.remove('active');
      }
    });
  }

  // ── Wrap every <pre> in a .code-block with a copy button ──
  document.querySelectorAll('.docs-body pre').forEach(function (pre) {
    if (pre.parentElement && pre.parentElement.classList.contains('code-block')) return;
    var wrap = document.createElement('div');
    wrap.className = 'code-block';
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);
    var btn = document.createElement('button');
    btn.className = 'code-copy';
    btn.type = 'button';
    btn.textContent = 'Copy';
    btn.addEventListener('click', function () {
      var text = pre.innerText;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          btn.textContent = 'Copied';
          btn.classList.add('copied');
          setTimeout(function () { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 1500);
        });
      }
    });
    wrap.appendChild(btn);
  });

  // ── Tab switcher ──────────────────────────────────────────
  // Markup convention:
  //   <div class="tabs" data-tabs>
  //     <div class="tabs__buttons">
  //       <button class="tabs__btn is-active" data-tab="swift">Swift</button>
  //       <button class="tabs__btn" data-tab="objc">Objective-C</button>
  //     </div>
  //     <div class="tabs__panel is-active" data-panel="swift">...</div>
  //     <div class="tabs__panel" data-panel="objc">...</div>
  //   </div>
  document.querySelectorAll('[data-tabs]').forEach(function (group) {
    var btns = group.querySelectorAll('.tabs__btn');
    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var key = btn.getAttribute('data-tab');
        group.querySelectorAll('.tabs__btn').forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        group.querySelectorAll('.tabs__panel').forEach(function (p) {
          p.classList.toggle('is-active', p.getAttribute('data-panel') === key);
        });
      });
    });
  });

  // ── Sidebar: highlight current page link ──────────────────
  // (Already done at build time via class="is-active", but also handle
  //  hash-anchor changes within long reference pages.)
  var hashLinks = document.querySelectorAll('.docs-sidebar a[href^="#"]');
  function syncHash() {
    var hash = window.location.hash;
    hashLinks.forEach(function (a) {
      a.classList.toggle('is-active', a.getAttribute('href') === hash);
    });
  }
  if (hashLinks.length) {
    window.addEventListener('hashchange', syncHash);
    syncHash();
  }
})();
