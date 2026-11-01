// tools.js — CSP-safe interactions for the Free Tools pages (no inline handlers).
// 1. Copy button on prompt cards (Clipboard API + fallback).
// 2. Category filter on the Prompt Library.
(function () {
  'use strict';

  function copyText(text, btn) {
    var done = function () {
      var label = btn.querySelector('[data-i18n]') || btn;
      var original = label.textContent;
      btn.classList.add('copied');
      label.textContent = '✓';
      setTimeout(function () {
        btn.classList.remove('copied');
        label.textContent = original;
      }, 1200);
    };
    var fail = function () {
      // Fallback for non-secure contexts / older browsers
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); done(); } catch (e) { /* noop */ }
      document.body.removeChild(ta);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fail);
    } else {
      fail();
    }
  }

  document.addEventListener('click', function (e) {
    var btn = e.target && e.target.closest ? e.target.closest('.copy-btn') : null;
    if (btn) {
      var target = document.getElementById(btn.getAttribute('data-copy-target'));
      if (target) copyText(target.textContent, btn);
      return;
    }

    var filter = e.target && e.target.closest ? e.target.closest('.filter-btn') : null;
    if (filter) {
      var f = filter.getAttribute('data-filter');
      var row = filter.closest('.filter-row');
      if (row) {
        row.querySelectorAll('.filter-btn').forEach(function (b) {
          var active = b === filter;
          b.classList.toggle('active', active);
          b.setAttribute('aria-pressed', active ? 'true' : 'false');
        });
      }
      document.querySelectorAll('.prompt-card').forEach(function (card) {
        var show = f === 'all' || card.getAttribute('data-category') === f;
        card.hidden = !show;
      });
      var grid = document.querySelector('.prompt-grid');
      var visible = grid ? grid.querySelectorAll('.prompt-card:not([hidden])').length : 0;
      var empty = document.getElementById('plEmpty');
      if (empty) empty.hidden = visible !== 0;
    }
  });
})();
