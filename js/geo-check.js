// Free AI-visibility snapshot — client for /api/geo-check (hero lead magnet)
// Renders the 3 free checks + CTA into the full audit. Also owns the
// One-time / Ongoing segment toggle in the products section.
(function () {
  'use strict';

  var lang = document.documentElement.getAttribute('data-i18n-static') || 'en';
  // translations arrive via a lazy-locale chunk — read at call time, not parse time
  function txt(id, fallback) {
    var t = (typeof translations !== 'undefined' && translations[lang]) || {};
    return t[id] || fallback;
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // Localize the domain input placeholder (attributes are not covered by the i18n engine)
  var domainInput = document.getElementById('geoDomain');
  if (domainInput && txt('heroInputPlaceholder')) domainInput.placeholder = txt('heroInputPlaceholder');

  var CHECK_LABELS = { llms: 'heroCheckLlms', crawlers: 'heroCheckCrawlers', schema: 'heroCheckSchema' };

  var form = document.getElementById('geoCheckForm');
  var btn = document.getElementById('heroRunCheck');
  var box = document.getElementById('geoResult');

  function showError(msg) {
    if (!box) return;
    box.hidden = false;
    box.className = 'hero-check-result is-error';
    box.innerHTML = '<p>' + msg + '</p>';
  }

  function render(data) {
    var items = (data.checks || []).map(function (c) {
      var cls = c.pass ? 'ok' : 'bad';
      var icon = c.pass
        ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21.8 10A10 10 0 1 1 17 3.34"/><path d="m9 11 3 3L22 4"/></svg>'
        : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>';
      return '<li class="' + cls + '">' + icon + esc(txt(CHECK_LABELS[c.id], c.id)) +
        '<span class="geo-state">' + esc(c.pass ? txt('heroCheckYes', 'pass') : txt('heroCheckNo', 'missing')) + '</span></li>';
    }).join('');

    var good = data.score >= 2;
    var servicesHref = (lang === 'sk' || lang === 'cs') ? '/services-sk' : '/services';
    var summary = data.score + '/3';
    var verdict = good
      ? txt('heroResultsOk', 'All 3 checks passed. Keep your lead — get the full 12-check audit.')
      : txt('heroResultsBad', 'AI search engines may not see your site. Get the full audit.');

    box.hidden = false;
    box.className = 'hero-check-result is-done';
    box.innerHTML =
      '<h4>' + esc(txt('heroResultsTitle', 'Free AI-visibility snapshot')) + ' — ' + esc(data.domain) + '</h4>' +
      '<ul class="geo-checks">' + items + '</ul>' +
      '<p class="geo-score"><strong>' + esc(summary) + '</strong> ' + esc(verdict) + '</p>' +
      '<a class="btn-primary" href="' + servicesHref + '#geo">' + esc(txt('heroResultsCta', 'Get the full audit — €199 →')) + '</a>';
  }

  if (form && btn && domainInput) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var raw = domainInput.value.trim();
      if (!raw) { domainInput.focus(); return; }
      var domain = raw.replace(/^https?:\/\//i, '').replace(/^www\./i, '').replace(/\/.*$/, '').toLowerCase();
      if (!/^[a-z0-9]([a-z0-9-]*\.)+[a-z]{2,24}$/.test(domain)) {
        showError(txt('heroCheckInvalid', 'Please enter a valid domain, e.g. your-domain.com'));
        return;
      }
      btn.disabled = true;
      var orig = btn.textContent;
      btn.textContent = '…';
      if (box) { box.hidden = false; box.className = 'hero-check-result'; box.innerHTML = '<p class="geo-score">…</p>'; }
      fetch('/api/geo-check?domain=' + encodeURIComponent(domain), { headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error('bad status ' + r.status);
          return r.json();
        })
        .then(function (d) {
          render(d);
          if (window.posthog && window.posthog.capture) {
            window.posthog.capture('geo_free_check', { domain: d.domain, score: d.score });
          }
        })
        .catch(function () {
          showError(txt('heroCheckError', 'The check failed to run. Try again, or write to me directly.'));
        })
        .finally(function () {
          btn.disabled = false;
          btn.textContent = orig;
        });
    });
  }

  // --- Products: One-time / Ongoing segment toggle ---
  var segOne = document.getElementById('segmentOneTime');
  var segOngoing = document.getElementById('segmentOngoing');
  var oneTime = document.getElementById('prodOneTime');
  var ongoing = document.getElementById('prodOngoing');

  function pick(on) {
    if (segOne) {
      segOne.classList.toggle('active', !on);
      segOne.setAttribute('aria-pressed', String(!on));
    }
    if (segOngoing) {
      segOngoing.classList.toggle('active', on);
      segOngoing.setAttribute('aria-pressed', String(on));
    }
    if (oneTime) oneTime.hidden = on;
    if (ongoing) ongoing.hidden = !on;
    if (window.posthog && window.posthog.capture) {
      window.posthog.capture('prod_segment_toggle', { segment: on ? 'ongoing' : 'one_time' });
    }
  }
  if (segOne && segOngoing) {
    segOne.addEventListener('click', function () { pick(false); });
    segOngoing.addEventListener('click', function () { pick(true); });
  }
})();
