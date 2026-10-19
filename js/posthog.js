// Analytics consent (opt-in) + PostHog EU Cloud (Frankfurt)
// Marian Stancik (marianstancik.dev)
//
// Legal basis: § 109 ods. 8 zák. 452/2021 Z. z. / Art. 5(3) ePrivacy, Art. 6(1)(a) + Art. 7 GDPR.
// - Before consent PostHog is NOT loaded at all: no request to posthog.com, no ph_* cookie,
//   no ph_* localStorage entry.
// - "Accept" -> PostHog is loaded with persistence 'localStorage+cookie' and capturing is opted in.
// - "Reject" -> nothing from PostHog is loaded or stored. Only the choice itself is remembered
//   (strictly necessary preference, key ms_consent_analytics, 12 months).
// - Consent can be changed any time via the "Cookie settings" link in the footer
//   (or any element with [data-ms-consent-open]) or window.msConsent.open().
(function () {
  'use strict';
  if (window.msConsent) return;

  var PH_KEY = 'phc_ohdWxCxN8vuoPk9GysrYash3ZTSKc7Y7XFLFztLTv4kX';
  var PH_HOST = 'https://eu.i.posthog.com';
  var STORE_KEY = 'ms_consent_analytics';
  var CONSENT_VERSION = 1;
  var MAX_AGE_MS = 365 * 24 * 60 * 60 * 1000; // re-ask after 12 months

  var TEXT = {
    sk: {
      title: 'Súbory cookies a analytika',
      body: 'S vaším súhlasom použijeme analytiku PostHog (EÚ, Frankfurt), ktorá ukladá cookies a údaje v prehliadači, aby sme pochopili, ako sa web používa, a mohli ho zlepšovať. Bez súhlasu sa nič také neukladá. Súhlas môžete kedykoľvek zmeniť cez „Nastavenia cookies“ v pätičke.',
      more: 'Viac o cookies',
      accept: 'Súhlasím',
      reject: 'Odmietnuť',
      settings: 'Nastavenia cookies',
      privacy: '/privacy-sk'
    },
    en: {
      title: 'Cookies & analytics',
      body: 'With your consent we use PostHog analytics (EU, Frankfurt), which stores cookies and data in your browser so we can understand how the site is used and improve it. Without consent nothing of the kind is stored. You can change your choice any time via “Cookie settings” in the footer.',
      more: 'More about cookies',
      accept: 'Accept',
      reject: 'Reject',
      settings: 'Cookie settings',
      privacy: '/privacy'
    },
    de: {
      title: 'Cookies & Analyse',
      body: 'Mit Ihrer Einwilligung nutzen wir PostHog-Analyse (EU, Frankfurt), die Cookies und Daten in Ihrem Browser speichert, damit wir verstehen, wie die Website genutzt wird. Ohne Einwilligung wird nichts dergleichen gespeichert. Sie können Ihre Wahl jederzeit über „Cookie-Einstellungen“ in der Fußzeile ändern.',
      more: 'Mehr zu Cookies',
      accept: 'Akzeptieren',
      reject: 'Ablehnen',
      settings: 'Cookie-Einstellungen',
      privacy: '/privacy'
    },
    pl: {
      title: 'Pliki cookie i analityka',
      body: 'Za Twoją zgodą używamy analityki PostHog (UE, Frankfurt), która zapisuje pliki cookie i dane w przeglądarce, abyśmy mogli zrozumieć, jak korzystasz z witryny. Bez zgody nic takiego nie jest zapisywane. Wybór możesz zmienić w każdej chwili w „Ustawieniach cookie” w stopce.',
      more: 'Więcej o cookie',
      accept: 'Akceptuję',
      reject: 'Odrzuć',
      settings: 'Ustawienia cookie',
      privacy: '/privacy'
    }
  };

  function lang() {
    var l = '';
    try { l = localStorage.getItem('ms_lang') || ''; } catch (e) {}
    if (!l) l = (document.documentElement.lang || 'en');
    l = String(l).toLowerCase().slice(0, 2);
    return TEXT[l] ? l : 'en';
  }
  function t() { return TEXT[lang()]; }

  // ---------- consent storage ----------
  function readConsent() {
    try {
      var raw = localStorage.getItem(STORE_KEY);
      if (!raw) return null;
      var c = JSON.parse(raw);
      if (!c || c.v !== CONSENT_VERSION) return null;
      if (c.status !== 'granted' && c.status !== 'denied') return null;
      if (!c.ts || (Date.now() - c.ts) > MAX_AGE_MS) return null;
      return c.status;
    } catch (e) { return null; }
  }
  function writeConsent(status) {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify({ v: CONSENT_VERSION, status: status, ts: Date.now() }));
    } catch (e) {}
  }

  // ---------- PostHog cleanup (for visitors with ph_* data from the previous version) ----------
  function purgePostHogStorage() {
    try {
      var host = location.hostname;
      var parts = host.split('.');
      var domains = ['', host, '.' + host];
      if (parts.length >= 2) domains.push('.' + parts.slice(-2).join('.'));
      document.cookie.split(';').forEach(function (c) {
        var name = c.split('=')[0].trim();
        if (name.indexOf('ph_') === 0 || name.indexOf('__ph') === 0) {
          domains.forEach(function (d) {
            document.cookie = name + '=; Max-Age=0; path=/' + (d ? '; domain=' + d : '') + '; SameSite=Lax';
          });
        }
      });
    } catch (e) {}
    [window.localStorage, window.sessionStorage].forEach(function (s) {
      try {
        var del = [];
        for (var i = 0; i < s.length; i++) {
          var k = s.key(i);
          if (k && (k.indexOf('ph_') === 0 || k.indexOf('__ph') === 0)) del.push(k);
        }
        del.forEach(function (k) { s.removeItem(k); });
      } catch (e) {}
    });
  }

  // ---------- PostHog loader (only after consent) ----------
  var phLoaded = false;
  function loadPostHog() {
    if (phLoaded) {
      try { window.posthog.set_config({ persistence: 'localStorage+cookie' }); window.posthog.opt_in_capturing(); } catch (e) {}
      return;
    }
    phLoaded = true;
    !function(t,e){var o,n,p,r;e.__SV||(window.posthog && window.posthog.__loaded)||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}p||((p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",p.onerror=function(){p=null},(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r));var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],Object.defineProperty(u,"toString",{configurable:!0,enumerable:!0,writable:!0,value:function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e}}),Object.defineProperty(u.people,"toString",{configurable:!0,enumerable:!0,writable:!0,value:function(){return u.toString(1)+".people (stub)"}}),o="du fu pu gu bu init Vu Gu zu Uu Ku el Wu Xu qu rc oc ac lc uc cc capture getExtension Qu cu fc calculateEventProperties dc register register_once register_for_session unregister unregister_for_session bc Bu gc getFeatureFlag getFeatureFlagPayload getFeatureFlagResult getAllFeatureFlags isFeatureEnabled reloadFeatureFlags updateFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSurveysLoaded onSessionId getSurveys getActiveMatchingSurveys onActiveMatchingSurveysChanged renderSurvey displaySurvey cancelPendingSurvey canRenderSurvey canRenderSurveyAsync identify setPersonProperties unsetPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset wc shutdown setIdentity clearIdentity get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException addExceptionStep captureLog startExceptionAutocapture stopExceptionAutocapture loadToolbar get_property getSessionProperty mc ec createPersonProfile setInternalOrTestUser yc Su wu opt_in_capturing opt_out_capturing ku has_opted_in_capturing has_opted_out_capturing get_explicit_consent_status is_capturing clear_opt_in_out_capturing Yu debug il Os getPageViewId captureTraceFeedback captureTraceMetric Ou".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
    window.posthog.init(PH_KEY, {
      api_host: PH_HOST,
      defaults: '2026-05-30',
      persistence: 'localStorage+cookie',
      opt_out_capturing_by_default: true,
      person_profiles: 'identified_only',
      capture_pageview: true,
      capture_pageleave: true,
      autocapture: true,
      disable_session_recording: true
    });
    window.posthog.opt_in_capturing();
  }

  function stopPostHog() {
    if (phLoaded && window.posthog) {
      try { window.posthog.opt_out_capturing(); } catch (e) {}
      try { window.posthog.reset(); } catch (e) {}
      try { window.posthog.set_config({ persistence: 'memory' }); } catch (e) {}
    }
    purgePostHogStorage();
    // posthog may write asynchronously; sweep once more
    setTimeout(purgePostHogStorage, 300);
  }

  // ---------- UI ----------
  var STYLE_ID = 'ms-consent-style';
  function injectStyle() {
    if (document.getElementById(STYLE_ID)) return;
    var css = '' +
      '.ms-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483000;max-width:640px;margin:0 auto;' +
      'background:var(--color-bg-secondary,#0B1320);color:var(--color-text,#E8EEF5);border:1px solid var(--color-border-hover,rgba(205,127,50,.42));' +
      'border-radius:16px;padding:20px 22px;box-shadow:0 18px 50px rgba(0,0,0,.55),0 0 24px var(--color-glow,rgba(205,127,50,.18));' +
      'font-family:inherit;font-size:14px;line-height:1.55;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}' +
      '.ms-consent[hidden]{display:none}' +
      '.ms-consent h2{margin:0 0 6px;font-size:16px;font-weight:600;color:var(--color-accent,#CD7F32);letter-spacing:.01em;border:0;padding:0}' +
      '.ms-consent p{margin:0 0 14px;color:var(--color-text-muted,#B4C0CF);font-size:13.5px}' +
      '.ms-consent a{color:var(--color-accent,#CD7F32);text-decoration:underline}' +
      '.ms-consent-actions{display:flex;gap:10px;flex-wrap:wrap}' +
      '.ms-consent-btn{flex:1 1 140px;min-height:42px;padding:10px 16px;border-radius:10px;cursor:pointer;font:inherit;font-size:14px;font-weight:600;' +
      'background:transparent;color:var(--color-text,#E8EEF5);border:1px solid var(--color-accent,#CD7F32);transition:background .2s,color .2s}' +
      '.ms-consent-btn:hover{background:var(--color-accent,#CD7F32);color:var(--color-bg,#002147)}' +
      '.ms-consent-btn:focus-visible{outline:2px solid var(--color-accent,#CD7F32);outline-offset:2px}' +
      '.ms-consent-link{background:none;border:0;padding:0;margin:0;font:inherit;color:inherit;text-decoration:underline;cursor:pointer}' +
      '.ms-consent-link:hover{color:var(--color-primary,#CD7F32)}' +
      '.ms-consent-footer{margin:8px 0 0;text-align:center;font-size:.75rem}' +
      '@media (max-width:480px){.ms-consent{left:10px;right:10px;bottom:10px;padding:16px}}';
    var s = document.createElement('style');
    s.id = STYLE_ID;
    s.textContent = css;
    document.head.appendChild(s);
  }

  var banner = null;
  function render() {
    var x = t();
    banner.innerHTML =
      '<h2 id="ms-consent-title"></h2>' +
      '<p id="ms-consent-desc"><span></span> <a href="/cookie"></a></p>' +
      '<div class="ms-consent-actions">' +
        '<button type="button" class="ms-consent-btn" data-ms-consent="reject"></button>' +
        '<button type="button" class="ms-consent-btn" data-ms-consent="accept"></button>' +
      '</div>';
    banner.querySelector('h2').textContent = x.title;
    banner.querySelector('p span').textContent = x.body;
    banner.querySelector('p a').textContent = x.more;
    banner.querySelector('[data-ms-consent="reject"]').textContent = x.reject;
    banner.querySelector('[data-ms-consent="accept"]').textContent = x.accept;
  }

  function ensureBanner() {
    if (banner) return banner;
    injectStyle();
    banner = document.createElement('div');
    banner.className = 'ms-consent';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-modal', 'false');
    banner.setAttribute('aria-labelledby', 'ms-consent-title');
    banner.setAttribute('aria-describedby', 'ms-consent-desc');
    banner.hidden = true;
    render();
    banner.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-ms-consent]');
      if (!b) return;
      decide(b.getAttribute('data-ms-consent') === 'accept' ? 'granted' : 'denied');
    });
    document.body.appendChild(banner);
    return banner;
  }

  function open(focus) {
    ensureBanner();
    render();
    banner.hidden = false;
    // Focus only when opened on request (keyboard users); on first visit neither button is pre-selected.
    var first = focus === true && banner.querySelector('[data-ms-consent]');
    if (first) try { first.focus({ preventScroll: true }); } catch (e) {}
  }
  function close() { if (banner) banner.hidden = true; }

  function decide(status) {
    writeConsent(status);
    close();
    if (status === 'granted') loadPostHog(); else stopPostHog();
    try { window.dispatchEvent(new CustomEvent('ms:consent', { detail: { analytics: status } })); } catch (e) {}
  }

  function addFooterLink() {
    if (document.getElementById('ms-consent-settings')) return;
    var host = document.querySelector('footer .footer-bottom') || document.querySelector('footer .container') || document.querySelector('footer');
    if (!host) return;
    var p = document.createElement('p');
    p.className = 'ms-consent-footer';
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'ms-consent-settings';
    btn.className = 'ms-consent-link';
    btn.setAttribute('data-ms-consent-open', '');
    btn.textContent = t().settings;
    p.appendChild(btn);
    host.appendChild(p);
  }

  function relabel() {
    var b = document.getElementById('ms-consent-settings');
    if (b) b.textContent = t().settings;
    if (banner && !banner.hidden) render();
  }

  document.addEventListener('click', function (ev) {
    var el = ev.target.closest && ev.target.closest('[data-ms-consent-open]');
    if (el) { ev.preventDefault(); open(true); }
  });
  window.addEventListener('languageChanged', relabel);

  window.msConsent = {
    open: function () { open(true); },
    get: readConsent,
    accept: function () { decide('granted'); },
    reject: function () { decide('denied'); }
  };

  function boot() {
    injectStyle();
    addFooterLink();
    var c = readConsent();
    if (c === 'granted') {
      loadPostHog();
    } else {
      purgePostHogStorage(); // remove ph_* left by the previous (non-consent) setup
      if (c !== 'denied') open();
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
