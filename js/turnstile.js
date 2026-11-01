// turnstile.js — Cloudflare Turnstile for the Starter Kit / lead forms.
// CSP-safe (external script, no inline handlers).
//
// Activation is key-driven and intentionally inert by default:
//  - The form contains <div class="cf-turnstile" data-sitekey="" ...></div>.
//  - While data-sitekey is empty, this script does NOTHING and the form
//    behaves exactly as before (honeypot-only protection).
//  - Once Marián provides the site key from the Cloudflare dashboard,
//    set data-sitekey="0x..." on the .cf-turnstile element and set the
//    TURNSTILE_SECRET_KEY environment variable for the /api/subscribe
//    Pages Function — verification then becomes mandatory server-side.
(function () {
  'use strict';

  function activate(widget) {
    var key = (widget.getAttribute('data-sitekey') || '').trim();
    if (!key || widget.getAttribute('data-turnstile-ready') === 'true') return;
    widget.setAttribute('data-turnstile-ready', 'true');

    var script = document.createElement('script');
    script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
    script.async = true;
    script.onload = function () {
      if (!window.turnstile || typeof window.turnstile.render !== 'function') return;
      widget.removeAttribute('hidden');
      window.turnstile.render(widget, {
        sitekey: key,
        theme: widget.getAttribute('data-theme') || 'dark',
        callback: function (token) { window.__turnstileToken = token; },
        'expired-callback': function () { window.__turnstileToken = ''; },
        'error-callback': function () { window.__turnstileToken = ''; }
      });
    };
    document.head.appendChild(script);
  }

  function boot() {
    var form = document.getElementById('leadForm') || document.getElementById('contactForm');
    if (!form) return;
    var widget = form.querySelector('.cf-turnstile');
    if (widget) activate(widget);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
