// Cloudflare Pages Function — Lead & Order capture → AgentMail (branded HTML email templates + admin alerts)
import emailTpl from './email-templates.js';

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
    const apiKey = env.AGENTMAIL_API_KEY;
    if (!apiKey) {
      return new Response(JSON.stringify({ error: 'API key not configured' }), { status: 500, headers: corsHeaders });
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

    const email = (body.email || '').trim().toLowerCase();
    const name = (body.name || '').slice(0, 100);
    const source = (body.source || 'web').slice(0, 50);
    const message = (body.message || '').slice(0, 5000);
    const product = (body.product || '').slice(0, 150);
    const price = (body.price || '').toString().slice(0, 20);
    const website = (body.website || '').slice(0, 200);
    const notes = (body.notes || '').slice(0, 1000);

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return new Response(JSON.stringify({ error: 'Invalid email' }), { status: 400, headers: corsHeaders });
    }

    // Safety guard
    const isTest = source.startsWith('pre-commit') || email.endsWith('.local');
    const isOrder = Boolean(product) || source === 'product_order' || source === 'stripe_checkout_intent';
    const isContact = Boolean(message) || source === 'contact_form';

    if (isTest && !isOrder && !isContact) {
      return new Response(JSON.stringify({ status: 'ok', type: 'test-skip', email, note: 'Test request - email not sent' }), { status: 200, headers: corsHeaders });
    }

    const now = new Date();
    const dateStr = now.toISOString().split('T')[0];
    const timeStr = now.toTimeString().split(' ')[0];

    const agentMailUrl = 'https://mcp.agentmail.to/mcp';
    const agentMailHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json, text/event-stream',
      'x-api-key': apiKey
    };

    async function sendEmail(to, subject, text, html, inboxId = 'marianstancik@agentmail.to') {
      const initBody = JSON.stringify({
        jsonrpc: '2.0', id: '1', method: 'initialize',
        params: { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'hermes-crm', version: '1.0' } }
      });
      const initRes = await fetch(agentMailUrl, { method: 'POST', headers: agentMailHeaders, body: initBody });
      const initText = await initRes.text();
      const sessionMatch = initText.match(/"sessionId"\s*:\s*"([^"]+)"/);
      const sessionId = sessionMatch ? sessionMatch[1] : null;
      const msgHeaders = { ...agentMailHeaders };
      if (sessionId) msgHeaders['Mcp-Session-Id'] = sessionId;

      await fetch(agentMailUrl, { method: 'POST', headers: msgHeaders, body: JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) });

      const args = { inboxId, to: [to], subject, text };
      if (html) args.html = html;

      const sendBody = JSON.stringify({
        jsonrpc: '2.0', id: '2', method: 'tools/call',
        params: { name: 'send_message', arguments: args }
      });
      const msgRes = await fetch(agentMailUrl, { method: 'POST', headers: msgHeaders, body: sendBody });
      const msgText = await msgRes.text();
      if (msgText.includes('"isError":true')) {
        const errMsg = msgText.match(/"message"\s*:\s*"([^"]+)"/)?.[1] || 'Unknown error';
        throw new Error(`AgentMail: ${errMsg}`);
      }
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
      await sendEmail('marianstancik@agentmail.to',
        `[CRM DOWN] Nezapisany lead: ${data.email || entryType}`, alertText, null)
        .catch(e => console.error('Lost-lead alert email failed:', e.message));
      return { ok: false, reason: lastError };
    }

    if (isOrder) {
      const custHtml = emailTpl.orderConfirmation(name || 'zákazník', product, price, website);
      const custText = emailTpl.orderConfirmationText(name || 'zákazník', product, price, website, notes);
      await sendEmail(email, `Potvrdenie objednávky: ${product}`, custText, custHtml);

      const alertBody = `NOVÁ OBJEDNÁVKA\nDatum: ${dateStr} ${timeStr}\nProdukt: ${product}\nCena: €${price}\nZakaznik: ${name || '-'} <${email}>\nWeb: ${website || '-'}\nPoznamky: ${notes || '-'}\nZdroj: ${source}`;
      await sendEmail('marianstancik@agentmail.to', `★ OBJEDNÁVKA: ${product} (€${price}) — ${name || email}`, alertBody, null);

      const crmRes = await crmToSheets('order', { email, name, product, price, website, notes, source, date: dateStr, time: timeStr });
      return new Response(JSON.stringify({ status: 'ok', type: 'order', email, product, crm: crmRes.ok ? 'ok' : 'failed' }), { status: 200, headers: corsHeaders });
    }

    if (isContact) {
      const custHtml = emailTpl.contactConfirmation(name, message);
      const custText = emailTpl.contactConfirmationText(name, message);
      await sendEmail(email, 'Správa prijatá — Marian Stancik', custText, custHtml);

      const alertBody = `NOVÁ SPRÁVA Z KONTAKTNÉHO FORMULÁRA\nDatum: ${dateStr} ${timeStr}\nOdosielatel: ${name || '-'} <${email}>\nSprava:\n${message}\nZdroj: ${source}`;
      await sendEmail('marianstancik@agentmail.to', `✉ SPRÁVA: ${name || email}`, alertBody, null);

      const crmRes = await crmToSheets('contact', { email, name, message, source, date: dateStr, time: timeStr });
      return new Response(JSON.stringify({ status: 'ok', type: 'contact', email, crm: crmRes.ok ? 'ok' : 'failed' }), { status: 200, headers: corsHeaders });
    }

    // Newsletter subscription
    let welcomeSent = false;
    try {
      const welcomeHtml = emailTpl.welcome(name, source);
      const welcomeText = emailTpl.welcomeText();
      await sendEmail(email, 'Vitaj v AI newslettri — Marian Stancik', welcomeText, welcomeHtml);
      welcomeSent = true;
    } catch (e) {
      console.error('Welcome email failed:', e.message);
    }

    await sendEmail('marianstancik@agentmail.to', `✦ Nový odberateľ newslettra: ${email}`, `Nový odberateľ newslettra:\nEmail: ${email}\nZdroj: ${source}\nDátum: ${dateStr} ${timeStr}`, null);
    const crmRes = await crmToSheets('newsletter', { email, source, date: dateStr, time: timeStr });
    return new Response(JSON.stringify({ status: 'ok', type: 'newsletter', email, welcome_sent: welcomeSent, crm: crmRes.ok ? 'ok' : 'failed' }), { status: 200, headers: corsHeaders });

  } catch (err) {
    console.error('Subscribe handler error:', err.message);
    return new Response(JSON.stringify({ error: err.message || 'Internal server error' }), { status: 500, headers: corsHeaders });
  }
}
