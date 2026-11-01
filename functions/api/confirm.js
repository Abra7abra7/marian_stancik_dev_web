// Cloudflare Pages Function — Double opt-in CONFIRMATION endpoint (legal v3.0.1).
// E-mails via Gmail (Google Workspace) — Legacy third-party inbox provider removed from the personal-data flow.
// TODO(Marián — Google Workspace Admin konzola, mimo repozitára): Data Region = Europe (Sheets + Gmail).
// GET /api/confirm?token=<payload>.<hmac>
//  - verifies the signed token (HMAC-SHA256, 30-day validity)
//  - flips the contact to status=confirmed in the CRM (Sheets)
//  - sends the welcome email with the AI Agent Starter Kit
//  - redirects the subscriber back to the Starter Kit page
import { sendGmail } from './_gmail.js';

const SITE = 'https://www.marianstancik.dev';

function b64urlDecode(s) {
  s = s.replace(/-/g, '+').replace(/_/g, '/');
  while (s.length % 4) s += '=';
  return atob(s);
}

async function hmacSign(data, secretStr) {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey('raw', enc.encode(secretStr), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, enc.encode(data));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('');
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const token = (url.searchParams.get('token') || '').trim();

  const secret = env.OPTIN_SECRET || env.CRM_WEBHOOK_KEY || env.GMAIL_CLIENT_SECRET;
  if (!secret) {
    // never verify against a default/fallback secret — require explicit configuration
    return new Response('Opt-in signing secret not configured', { status: 500 });
  }

  const fail = (lang, code) => Response.redirect(`${SITE}/${lang}/tools/starter-kit?confirmed=${code}`, 302);

  if (!env.GMAIL_REFRESH_TOKEN && !env.GMAIL_SERVICE_ACCOUNT_JSON) {
    return new Response('Gmail credentials not configured', { status: 500 });
  }
  if (!token || !token.includes('.')) return fail('en', 0);

  const dot = token.lastIndexOf('.');
  const payloadB64 = token.slice(0, dot);
  const sig = token.slice(dot + 1);

  let payload;
  try {
    payload = JSON.parse(b64urlDecode(payloadB64));
  } catch (e) {
    return fail('en', 0);
  }
  if (!payload || !payload.e) return fail('en', 0);

  const expected = await hmacSign(payloadB64, secret);
  if (expected !== sig) return fail(payload.l || 'en', 0);

  // 30-day validity
  if (!payload.t || Date.now() - payload.t > 30 * 24 * 3600 * 1000) return fail(payload.l || 'en', 2);

  const email = String(payload.e).toLowerCase();
  const lang = payload.l === 'sk' ? 'sk' : 'en';
  const source = String(payload.s || 'web').slice(0, 50);

  const now = new Date();
  const dateStr = now.toISOString().split('T')[0];
  const timeStr = now.toTimeString().split(' ')[0];

  const CRM_URL = env.CRM_WEBHOOK_URL || 'https://api.marianstancik.dev/crm/';
  const CRM_KEY = env.CRM_WEBHOOK_KEY || '';
  async function crmToSheets(entryType, data) {
    if (!CRM_KEY) return { ok: false, reason: 'CRM_WEBHOOK_KEY missing' };
    try {
      const res = await fetch(CRM_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CRM-Key': CRM_KEY },
        body: JSON.stringify({ type: entryType, ...data }),
      });
      return res.ok ? { ok: true } : { ok: false, reason: `HTTP ${res.status}` };
    } catch (e) {
      return { ok: false, reason: e.message };
    }
  }

  // 1. Flip status to confirmed in the CRM (Sheets)
  const crmRes = await crmToSheets('newsletter_confirm', { email, source, status: 'confirmed', date: dateStr, time: timeStr });

  // 2. Welcome email with the Starter Kit (sent ONLY now, after the confirmed click)
  const kitLink = `${SITE}/tools/prompt-library`;
  const howLink = `${SITE}/how-it-works`;
  const subject = lang === 'sk' ? 'Tvoj AI Agent Starter Kit' : 'Your AI Agent Starter Kit';
  const text = lang === 'sk'
    ? `Ahoj,\n\npotvrdenie prišlo — tu je AI Agent Starter Kit:\n\n1. Prompt Library (15 promptov vo formáte prompt → vstup → výstup → zlyhania):\n   ${kitLink}\n\n2. Ako funguje tím 14 agentov (príbeh a pravidlá):\n   ${howLink}\n\nTri tipy na začiatok:\n- Nečítaj všetko naraz. Začni orkestrátorom a pravidlom formátu.\n- Každý prompt má vypísané známe zlyhania — prečítaj si ich skôr, než prompt použiješ.\n- Najčastejšia chyba začiatočníkov je agent „na všetko“. Daj mu jednu rolu.\n\nAk niečo nebude jasné, odpovedaj na tento e-mail.\n\n— Marian Stancik`
    : `Hi,\n\nconfirmation received — here is your AI Agent Starter Kit:\n\n1. Prompt Library (15 prompts in the prompt → input → output → known failures format):\n   ${kitLink}\n\n2. How the 14-agent team works (the story and the rules):\n   ${howLink}\n\nThree tips to start:\n- Don't read everything at once. Start with the orchestrator and the format rule.\n- Every prompt lists its known failures — read them before you use the prompt.\n- The most common beginner mistake is the "does everything" agent. Give it one role.\n\nIf anything is unclear, just reply to this email.\n\n— Marian Stancik`;
  const html = `<!DOCTYPE html><html><body style="font-family:Arial,Helvetica,sans-serif;max-width:560px;margin:0 auto;color:#222;">
    <h2 style="color:#CD7F32;">${lang === 'sk' ? 'Tvoj AI Agent Starter Kit' : 'Your AI Agent Starter Kit'}</h2>
    <p>${lang === 'sk' ? 'Potvrdenie prišlo — tu je Kit:' : 'Confirmation received — here is the Kit:'}</p>
    <p><a href="${kitLink}" style="display:inline-block;background:#CD7F32;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:bold;">${lang === 'sk' ? 'Otvoriť Prompt Library' : 'Open the Prompt Library'}</a></p>
    <p>${lang === 'sk'
      ? 'Ďalej: <a href="' + howLink + '">ako funguje tím 14 agentov</a>. Tri tipy: začni orkestrátorom, čítaj známe zlyhania skôr než prompt použiješ, a nedaj agentovi „všetko“ — jednu rolu.'
      : 'Also: <a href="' + howLink + '">how the 14-agent team works</a>. Three tips: start with the orchestrator, read the known failures before using a prompt, and never give an agent "everything" — one role.'}</p>
    <p style="font-size:0.8rem;color:#888;">${lang === 'sk' ? 'Toto je druhý a posledný e-mail z tejto sekvencie.' : 'This is the second and last email of this sequence.'}</p>
  </body></html>`;

  try {
    await sendGmail(env, email, subject, text, html);
  } catch (e) {
    console.error('Welcome email failed:', e.message);
    // status is already confirmed; the kit email can be re-sent manually — still redirect as success
  }

  await sendGmail(env, env.ADMIN_EMAIL || env.GMAIL_USER || 'stancikmarian8@gmail.com', `✅ Opt-in POTVRDENÝ: ${email}`,
    `Opt-in potvrdený (status=confirmed), kit odoslaný:\nEmail: ${email}\nZdroj: ${source}\nDátum: ${dateStr} ${timeStr}\nCRM: ${crmRes.ok ? 'ok' : 'FAILED — zapis rucne'}`)
    .catch(e => console.error('Admin notify failed:', e.message));

  return Response.redirect(`${SITE}/${lang}/tools/starter-kit?confirmed=1`, 302);
}
