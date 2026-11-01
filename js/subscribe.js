// Blog subscribe forms — CSP-safe replacement for the (never-defined) inline
// onsubmit="handleBlogSubscribe(...)". Forms declare data-subscribe-lang="en|sk|…".
// Posts to /api/subscribe (honeypot + per-IP throttle handled server-side).
(function () {
  'use strict';

  var T = {
    en: { ok: '✅ Subscribed! Check your inbox to confirm.', bad: 'Please enter a valid email.', err: '❌ Error. Try again later.' },
    sk: { ok: '✅ Prihlásené! Potvrďte si prosím e-mail v schránke.', bad: 'Zadajte prosím platný e-mail.', err: '❌ Chyba. Skúste prosím neskôr.' },
    cs: { ok: '✅ Přihlášeno! Potvrďte prosím e-mail ve schránce.', bad: 'Zadejte prosím platný e-mail.', err: '❌ Chyba. Zkuste prosím později.' },
    de: { ok: '✅ Abonniert! Bitte bestätige die E-Mail in deinem Postfach.', bad: 'Bitte eine gültige E-Mail-Adresse eingeben.', err: '❌ Fehler. Bitte später erneut versuchen.' },
    pl: { ok: '✅ Zapisano! Potwierdź proszę e-mail w skrzynce.', bad: 'Podaj proszę prawidłowy adres e-mail.', err: '❌ Błąd. Spróbuj proszę później.' }
  };

  var renderedAt = Date.now();

  document.addEventListener('submit', function (e) {
    var form = e.target.closest ? e.target.closest('form[data-subscribe-lang]') : null;
    if (!form) return;
    e.preventDefault();

    var lang = form.getAttribute('data-subscribe-lang') || 'en';
    var m = T[lang] || T.en;
    var status = form.parentElement ? form.parentElement.querySelector('.blog-sub-status') : null;
    var emailEl = form.querySelector('input[type="email"]');
    var hpEl = form.querySelector('input[name="hp"]');
    var email = emailEl ? String(emailEl.value).trim() : '';

    function say(msg) { if (status) status.textContent = msg; }

    // Bot signals: honeypot filled, or the form was submitted under 2s after load.
    if (hpEl && hpEl.value) { say(m.ok); form.reset(); return; }
    if (Date.now() - renderedAt < 2000) { say(m.ok); form.reset(); return; }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { say(m.bad); return; }

    say('…');
    fetch('/api/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, source: 'blog_subscribe', lang: lang, hp: '' })
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d && (d.status === 'ok' || d.type === 'bot_dropped')) { say(m.ok); form.reset(); }
        else { say(m.err); }
      })
      .catch(function () { say(m.err); });
  });
})();
