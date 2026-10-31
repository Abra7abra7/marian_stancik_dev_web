// Stripe checkout modal — services pages (en + sk source templates, and their generated copies).
// CSP-safe replacement for the former inline <script> + onclick/onsubmit handlers
// (script-src 'self' without 'unsafe-inline').
//
// Buttons declare: data-checkout-key="geo-audit" data-price="199" data-title="AI GEO Audit"
// The overlay/close/form are bound here, not in HTML.
(function () {
  'use strict';

  var lang = document.documentElement.getAttribute('data-i18n-static')
    || (document.documentElement.getAttribute('lang') || 'en').split('-')[0];
  var sl = (lang === 'sk' || lang === 'cs');
  var MSG = sl
    ? { order: 'Objednávka s povinnosťou platby', redirect: 'Presmerovávam na bezpečnú platbu…', fill: 'Vyplňte prosím e-mail a adresu webu.' }
    : { order: 'Order with obligation to pay', redirect: 'Redirecting to secure checkout...', fill: 'Please fill in email and website URL.' };

  // Single source of truth for payment links. Keys match data-checkout-key on the buttons.
  // Fixes the former mismatch where monitoring/compliance/suite buttons passed keys
  // ('geo-monitoring', 'compliance-watch', 'full-suite') that the old PRODUCTS map did
  // not contain, silently redirecting those orders to the generic fallback link.
  var PRODUCTS = {
    'geo-audit':        { stripeUrl: 'https://buy.stripe.com/test_3cI9AT73SaTmfsKcTE1Fe00' },
    'readiness':        { stripeUrl: 'https://buy.stripe.com/test_4gMdR93RG9Pi2FYf1M1Fe01' },
    'full-audit':       { stripeUrl: 'https://buy.stripe.com/test_fZu9ATbk8bXq4O6dXI1Fe02' },
    'geo-monitoring':   { stripeUrl: 'https://buy.stripe.com/test_cNi8wPdsg5z2fsK1aW1Fe04' },
    'compliance-watch': { stripeUrl: 'https://buy.stripe.com/test_7sYaEXag4d1ugwO7zk1Fe05' },
    'full-suite':       { stripeUrl: 'https://buy.stripe.com/test_4gM3cv87W3qU80i9Hs1Fe06' },
    'custom-agent':     { stripeUrl: 'https://buy.stripe.com/test_eVq5kD0Fu7Ha1BU7zk1Fe03' },
    'agent-deposit':    { stripeUrl: 'https://buy.stripe.com/test_eVq5kD0Fu7Ha1BU7zk1Fe03' }
  };
  var FALLBACK_URL = 'https://buy.stripe.com/test_5kQ28t4Sk94S74pgBD28800';

  var currentTitle = '';
  var currentPrice = 199;
  var currentKey = '';

  function openStripeCheckout(title, price, key) {
    currentTitle = title;
    currentPrice = price;
    currentKey = key || '';
    var stepForm = document.getElementById('modalStepForm');
    var titleEl = document.getElementById('modalProductTitle');
    var priceEl = document.getElementById('modalPriceVal');
    var btn = document.getElementById('modalSubmitBtn');
    if (stepForm) stepForm.style.display = 'block';
    if (titleEl) titleEl.textContent = title;
    if (priceEl) priceEl.textContent = '€' + price;
    if (btn) {
      btn.innerHTML = MSG.order + ' (<span id="modalPriceVal">€' + price + '</span>) →';
      btn.disabled = false;
    }
    var modal = document.getElementById('stripeModal');
    if (modal) modal.style.display = 'flex';
  }

  function closeStripeModal() {
    var modal = document.getElementById('stripeModal');
    var stepForm = document.getElementById('modalStepForm');
    var btn = document.getElementById('modalSubmitBtn');
    if (modal) modal.style.display = 'none';
    if (stepForm) stepForm.style.display = 'block';
    if (btn) btn.disabled = false;
  }

  async function handleStripeRedirect(e) {
    e.preventDefault();
    var emailEl = document.getElementById('stripeEmail');
    var urlEl = document.getElementById('stripeUrl');
    var notesEl = document.getElementById('stripeNotes');
    var email = emailEl ? emailEl.value.trim() : '';
    var url = urlEl ? urlEl.value.trim() : '';
    var notes = notesEl ? notesEl.value.trim() : '';
    var prod = PRODUCTS[currentKey] || { stripeUrl: FALLBACK_URL };

    if (!email || !url) { alert(MSG.fill); return; }

    var btn = document.getElementById('modalSubmitBtn');
    if (btn) {
      btn.textContent = MSG.redirect;
      btn.disabled = true;
    }

    try {
      // Lead capture & order notification (AgentMail + CRM) — best effort
      await fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email,
          source: 'product_order',
          product: currentTitle,
          price: String(currentPrice),
          website: url,
          notes: notes,
          consent_terms: true,
          consent_withdrawal_waiver: true
        })
      });
    } catch (err) {
      console.warn('Lead capture notification notice:', err);
    }

    // Redirect to the Stripe Payment Link with prefilled email + target domain
    var cleanDomain = url.trim().toLowerCase().replace(/^https?:\/\//, '').replace(/\/.*$/, '');
    var baseLink = prod.stripeUrl || FALLBACK_URL;
    var sep = baseLink.indexOf('?') === -1 ? '?' : '&';
    window.location.href = baseLink + sep + 'prefilled_email=' + encodeURIComponent(email) +
      '&client_reference_id=' + encodeURIComponent(cleanDomain);
  }

  // --- Delegated listeners (replaces inline onclick/onsubmit) ---
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-checkout-key]');
    if (btn) {
      openStripeCheckout(
        btn.getAttribute('data-title') || btn.textContent.trim(),
        parseInt(btn.getAttribute('data-price'), 10) || 199,
        btn.getAttribute('data-checkout-key')
      );
      return;
    }
    if (e.target.closest('.stripe-modal-close')) { closeStripeModal(); return; }
    var overlay = e.target.closest('.stripe-modal-overlay');
    if (overlay && !e.target.closest('.stripe-modal')) closeStripeModal();
  });

  var form = document.getElementById('stripeCheckoutForm');
  if (form) form.addEventListener('submit', handleStripeRedirect);

  // Kept for backwards compatibility with any legacy callers.
  window.openStripeCheckout = openStripeCheckout;
  window.closeStripeModal = closeStripeModal;
})();
