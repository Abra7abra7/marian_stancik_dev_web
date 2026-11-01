import { sendGmail } from './_gmail.js';

// Cloudflare Pages Function — Lead capture with STRICT double opt-in (legal v3.0.1).
// Transactional e-mails go through Gmail (Google Workspace) via functions/api/_gmail.js —
// AgentMail is fully removed from the personal-data flow.
// TODO(Marián — Google Workspace Admin konzola, mimo repozitára): Data Region = Europe (Sheets + Gmail).
// The welcome/kit email is sent from functions/api/confirm.js AFTER the confirmation link click.
export async function onRequestOptions(context) {
  const origin = context.request.headers.get('origin') || '';
  return new Response(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': origin || 'https://www.marianstancik.dev',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    }
  });
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const origin = request.headers.get('origin') || '';
  const allowedOrigins = [
    'https://www.marianstancik.dev',
    'https://marianstancik.dev',
    'http://localhost:3000',
    'http://localhost:5000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5500'
  ];

  const corsHeaders = {
    'Access-Control-Allow-Origin': (allowedOrigins.includes(origin) || origin.endsWith('.marianstancik.dev')) ? origin : 'https://www.marianstancik.dev',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
  };

  try {
    if (!env.GMAIL_REFRESH_TOKEN && !env.GMAIL_SERVICE_ACCOUNT_JSON) {
      return new Response(JSON.stringify({ error: 'Gmail credentials not configured' }), { status: 500, headers: corsHeaders });
    }

    let body = {};
    try {
      body = await request.json();
    } catch (e) {
      body = {};
    }

    // Honeypot spam protection
    if (body.hp || body.honeypot || body.website_url_hp) {
      console.warn('Honeypot triggered, silently dropping bot request');
      return new Response(JSON.stringify({ status: 'ok', type: 'bot_dropped' }), { status: 200, headers: corsHeaders });
    }

    // Cloudflare Turnstile verification — active ONLY when TURNSTILE_SECRET_KEY is configured.
    // While the env var is unset the form works as before (honeypot-only), so deploying this
    // code does not change behaviour until Marián adds the secret key in Cloudflare Pages settings.
    if (env.TURNSTILE_SECRET_KEY) {
      const turnstileToken = body.turnstile || body['cf-turnstile-response'] || '';
      if (!turnstileToken) {
        return new Response(JSON.stringify({ error: 'Captcha verification missing. Please retry.' }), { status: 403, headers: corsHeaders });
      }
      try {
        const verifyRes = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            secret: env.TURNSTILE_SECRET_KEY,
            response: turnstileToken,
            remoteip: request.headers.get('cf-connecting-ip') || ''
          })
        });
        const verify = await verifyRes.json();
        if (!verify.success) {
          console.warn('Turnstile verification failed', verify['error-codes'] || []);
          return new Response(JSON.stringify({ error: 'Captcha verification failed. Please retry.' }), { status: 403, headers: corsHeaders });
        }
      } catch (e) {
        console.error('Turnstile verification error', e);
        return new Response(JSON.stringify({ error: 'Captcha verification error. Please retry.' }), { status: 502, headers: corsHeaders });
      }
    }

    const email = (body.email || '').trim().toLowerCase();
    const source = (body.source || 'web').slice(0, 50);

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return new Response(JSON.stringify({ error: 'Invalid email' }), { status: 400, headers: corsHeaders });
    }

    // Safety guard
    const isTest = source.startsWith('pre-commit') || email.endsWith('.local');

    if (isTest) {
      return new Response(JSON.stringify({ status: 'ok', type: 'test-skip', email, note: 'Test request - email not sent' }), { status: 200, headers: corsHeaders });
    }

    const now = new Date();
    const dateStr = now.toISOString().split('T')[0];
    const timeStr = now.toTimeString().split(' ')[0];

    // E-mail sending via Gmail (Google Workspace) — see functions/api/_gmail.js
    const ADMIN_EMAIL = env.ADMIN_EMAIL || env.GMAIL_USER || 'stancikmarian8@gmail.com';
    async function notifyAdmin(subject, text) {
      await sendGmail(env, ADMIN_EMAIL, subject, text, null)
        .catch(e => console.error('Admin notify failed:', e.message));
    }

    // CRM forward to Hetzner VPS webhook
    const CRM_URL = env.CRM_WEBHOOK_URL || 'https://api.marianstancik.dev/crm/';
    const CRM_KEY = env.CRM_WEBHOOK_KEY || '';
    async function crmToSheets(entryType, data) {
      if (!CRM_KEY) {
        return { ok: false, reason: 'CRM_WEBHOOK_KEY missing' };
      }
      let lastError = 'unknown';
      for (let attempt = 1; attempt <= 2; attempt++) {
        try {
          const res = await fetch(CRM_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CRM-Key': CRM_KEY },
            body: JSON.stringify({ type: entryType, ...data }),
          });
          if (res.ok) return { ok: true };
          lastError = `HTTP ${res.status}`;
        } catch (e) {
          lastError = e.message;
        }
        if (attempt === 1) await new Promise(r => setTimeout(r, 400));
      }

      const alertText = `LEAD NEZAPISANY DO CRM - webhook ${lastError}\n`
        + `Typ: ${entryType}\nDatum: ${dateStr} ${timeStr}\n`
        + `Lead: ${data.name || '-'} <${data.email || '-'}>\n`
        + (data.message ? `Sprava: ${data.message}\n` : '')
        + (data.product ? `Produkt: ${data.product} ${data.price ? '(' + data.price + ')' : ''}\n` : '')
        + (data.website ? `Web: ${data.website}\n` : '')
        + `Zdroj: ${data.source || '-'}\n\n`
        + `Tento lead sa NEDOSTAL do CRM Sheets - zapis ho rucne.\n`;
      await notifyAdmin(`[CRM DOWN] Nezapisany lead: ${data.email || entryType}`, alertText)
        .catch(e => console.error('Lost-lead alert email failed:', e.message));
      return { ok: false, reason: lastError };
    }

    // ---- Lead capture: STRICT double opt-in (legal v3.0) ----
    // Step 1: store the contact as "pending". NO welcome email and NO kit here —
    // the kit is sent only after the subscriber clicks the confirmation link
    // (see functions/api/confirm.js).

    async function hmacSign(data, secretStr) {
      const enc = new TextEncoder();
      const key = await crypto.subtle.importKey('raw', enc.encode(secretStr), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
      const sig = await crypto.subtle.sign('HMAC', key, enc.encode(data));
      return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('');
    }

    const crmRes = await crmToSheets('newsletter', { email, source, status: 'pending', date: dateStr, time: timeStr });

    const optinSecret = env.OPTIN_SECRET || env.CRM_WEBHOOK_KEY || env.GMAIL_CLIENT_SECRET;
    if (!optinSecret) {
      // signing secret is required for the opt-in token — never sign with an empty/default key
      return new Response(JSON.stringify({ error: 'Opt-in signing secret not configured (set OPTIN_SECRET)' }), { status: 500, headers: corsHeaders });
    }
    const lang = (body.lang === 'sk') ? 'sk' : 'en';
    const payload = btoa(JSON.stringify({ e: email, s: source, l: lang, t: Date.now() }))
      .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
    const sig = await hmacSign(payload, optinSecret);
    const token = `${payload}.${sig}`;
    const confirmUrl = `https://www.marianstancik.dev/api/confirm?token=${encodeURIComponent(token)}`;

    const confSubject = lang === 'sk'
      ? 'Potvrď prihlásenie — AI Agent Starter Kit'
      : 'Confirm your subscription — AI Agent Starter Kit';
    const confText = lang === 'sk'
      ? `Ahoj,\n\nraz si požiadal(a) o AI Agent Starter Kit na marianstancik.dev.\n\nPosledný krok: potvrď prihlásenie kliknutím na tento odkaz:\n${confirmUrl}\n\nBez potvrdenia ti nič nepošleme. Odkaz platí 30 dní.\n\nAk si o to nepožiadal(a), tento e-mail ignoruj a nič sa nestane.\n\n— Marian Stancik`
      : `Hi,\n\nyou requested the AI Agent Starter Kit on marianstancik.dev.\n\nOne last step: confirm your subscription by clicking this link:\n${confirmUrl}\n\nNothing gets sent without confirmation. The link is valid for 30 days.\n\nIf you did not request this, ignore this email and nothing happens.\n\n— Marian Stancik`;
    const confHtml = `<!DOCTYPE html><html><body style="font-family:Arial,Helvetica,sans-serif;max-width:560px;margin:0 auto;color:#222;">
      <h2 style="color:#CD7F32;">${lang === 'sk' ? 'Potvrď prihlásenie' : 'Confirm your subscription'}</h2>
      <p>${lang === 'sk'
        ? 'Raz si požiadal(a) o AI Agent Starter Kit. Posledný krok: klikni na potvrdzovacie tlačidlo nižšie. Bez potvrdenia ti nič nepošleme.'
        : 'You requested the AI Agent Starter Kit. One last step: click the confirmation button below. Nothing gets sent without confirmation.'}</p>
      <p><a href="${confirmUrl}" style="display:inline-block;background:#CD7F32;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:bold;">${lang === 'sk' ? 'Potvrdiť prihlásenie' : 'Confirm subscription'}</a></p>
      <p style="font-size:0.8rem;color:#888;">${lang === 'sk' ? 'Odkaz platí 30 dní. Ak si o to nepožiadal(a), ignoruj tento e-mail.' : 'The link is valid for 30 days. If you did not request this, ignore this email.'}</p>
    </body></html>`;

    try {
      await sendGmail(env, email, confSubject, confText, confHtml);
    } catch (e) {
      console.error('Confirmation email failed:', e.message);
      return new Response(JSON.stringify({ error: 'Confirmation email could not be sent. Try again later.' }), { status: 502, headers: corsHeaders });
    }

    await notifyAdmin(`✦ Nový PENDING opt-in: ${email}`, `Nový pending opt-in (čaká na potvrdenie):\nEmail: ${email}\nZdroj: ${source}\nDátum: ${dateStr} ${timeStr}\nCRM: ${crmRes.ok ? 'ok' : 'FAILED — zapis rucne'}`, null)
      .catch(e => console.error('Admin notify failed:', e.message));

    return new Response(JSON.stringify({ status: 'ok', type: 'newsletter', double_optin: 'pending', email, crm: crmRes.ok ? 'ok' : 'failed' }), { status: 200, headers: corsHeaders });

  } catch (err) {
    console.error('Subscribe handler error:', err.message);
    return new Response(JSON.stringify({ error: err.message || 'Internal server error' }), { status: 500, headers: corsHeaders });
  }
}
