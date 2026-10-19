/**
 * stripe-webhook.js — Stripe → D1 → audit trigger
 * Spracúva Stripe udalosti:
 *   checkout.session.completed → vytvorí client + spustí audit
 *   invoice.paid → predĺži subscription
 *   customer.subscription.deleted → zruší monitoring
 *
 * Vylepšené:
 * - Ak chýba domain → vytvorí clienta s placeholder + alert
 * - Vždy zaloguje platbu, aj keď chýbajú metadata
 * - Notifikuje Maria pri chybe
 */

import { runAudit } from './audit-worker';

async function sendAgentMail(env, to, subject, text, html = null, inboxId = 'marianstancik@agentmail.to') {
  const apiKey = env.AGENTMAIL_API_KEY;
  if (!apiKey) {
    console.warn('AGENTMAIL_API_KEY not configured — skipping email delivery');
    return false;
  }
  try {
    const agentMailUrl = 'https://mcp.agentmail.to/mcp';
    const agentMailHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json, text/event-stream',
      'x-api-key': apiKey
    };
    const initRes = await fetch(agentMailUrl, {
      method: 'POST',
      headers: agentMailHeaders,
      body: JSON.stringify({
        jsonrpc: '2.0', id: '1', method: 'initialize',
        params: { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'stripe-webhook', version: '1.0' } }
      })
    });
    const initText = await initRes.text();
    const sessionMatch = initText.match(/"sessionId"\s*:\s*"([^"]+)"/);
    const sessionId = sessionMatch ? sessionMatch[1] : null;
    const msgHeaders = { ...agentMailHeaders };
    if (sessionId) msgHeaders['Mcp-Session-Id'] = sessionId;

    await fetch(agentMailUrl, {
      method: 'POST',
      headers: msgHeaders,
      body: JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' })
    });

    const args = { inboxId, to: [to], subject, text };
    if (html) args.html = html;

    const msgRes = await fetch(agentMailUrl, {
      method: 'POST',
      headers: msgHeaders,
      body: JSON.stringify({
        jsonrpc: '2.0', id: '2', method: 'tools/call',
        params: { name: 'send_message', arguments: args }
      })
    });
    return msgRes.ok;
  } catch (e) {
    console.error('AgentMail dispatch error:', e.message);
    return false;
  }
}

async function sendAdminAlert(env, subject, message) {
  return await sendAgentMail(env, 'marianstancik@agentmail.to', subject, message);
}

async function verifyStripeSignature(rawBody, header, secret) {
  if (!header || !secret) return false;
  let timestamp = null;
  const signatures = [];
  for (const item of header.split(',')) {
    const parts = item.split('=');
    if (parts.length < 2) continue;
    const k = parts[0].trim();
    const v = parts.slice(1).join('=').trim();
    if (k === 't') timestamp = v;
    else if (k === 'v1') signatures.push(v);
  }
  if (!timestamp || signatures.length === 0) return false;

  // Replay protection: 5 minute tolerance window
  const now = Math.floor(Date.now() / 1000);
  const t = parseInt(timestamp, 10);
  if (isNaN(t) || Math.abs(now - t) > 300) return false;

  const signedPayload = `${timestamp}.${rawBody}`;
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    enc.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const sigBuffer = await crypto.subtle.sign('HMAC', key, enc.encode(signedPayload));
  const expectedSig = Array.from(new Uint8Array(sigBuffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');

  return signatures.includes(expectedSig);
}

export async function handleStripeRequest(request, env) {
  if (request.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 });
  }

  // Verify Stripe signature
  const signature = request.headers.get('stripe-signature');
  if (!signature) {
    return new Response('Missing signature', { status: 401 });
  }

  const rawBody = await request.text();

  if (env.STRIPE_WEBHOOK_SECRET) {
    const isValid = await verifyStripeSignature(rawBody, signature, env.STRIPE_WEBHOOK_SECRET);
    if (!isValid) {
      return new Response(JSON.stringify({ error: 'Invalid webhook signature' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  } else {
    console.warn('STRIPE_WEBHOOK_SECRET not configured — skipping HMAC verification');
  }

  let body;
  try {
    body = JSON.parse(rawBody);
  } catch (e) {
    return new Response('Invalid payload', { status: 400 });
  }

  const event = body.type;
  const data = body.data?.object;

  if (!event || !data) {
    return new Response('Invalid payload', { status: 400 });
  }

  switch (event) {
    case 'checkout.session.completed': {
      const email = data.customer_details?.email || data.customer_email;
      const name = data.customer_details?.name || email?.split('@')[0] || 'Unknown';
      const amount = data.amount_total || 0;
      const currency = data.currency || 'eur';
      const sessionId = data.id;
      
      // Get domain from metadata, custom fields, or client_reference_id
      let domain = data.metadata?.domain;
      if (!domain) {
        try {
          domain = data.custom_fields?.find(f => f.key === 'domain' || f.key === 'website')?.text?.value;
        } catch (e) { /* silent */ }
      }
      if (!domain && data.client_reference_id) {
        domain = data.client_reference_id;
      }

      // Log the event to D1 alerts regardless
      try {
        await env.DB.prepare(
          'INSERT INTO alerts (id, client_id, type, message) VALUES (?, ?, ?, ?)'
        ).bind(
          crypto.randomUUID(),
          'system',
          'stripe_payment',
          `New payment: €${(amount/100).toFixed(2)} from ${email}${domain ? ` for ${domain}` : ' (NO DOMAIN)'} session=${sessionId}`
        ).run();
      } catch (e) { /* db might not be ready */ }

      if (!email) {
        // Critical — no email, no domain
        await sendAdminAlert(env,
          `⚠️ Stripe payment with no email — €${(amount/100).toFixed(2)}`,
          `Session: ${sessionId}\nAmount: €${(amount/100).toFixed(2)}\nMetadata: ${JSON.stringify(data.metadata, null, 2)}\n\nManual action required.`
        );
        return new Response(JSON.stringify({ error: 'Missing email', session: sessionId }), { status: 400 });
      }

      if (!domain) {
        // Payment received but no domain — create pending client, notify Marian
        const clientId = crypto.randomUUID();
        await env.DB.prepare(
          'INSERT INTO clients (id, email, domain, name, plan, status) VALUES (?, ?, ?, ?, ?, ?)'
        ).bind(clientId, email, 'DOMAIN_REQUIRED', name, 'pending_domain', 'pending').run();

        // Store session info for later matching
        await env.DB.prepare(
          'INSERT INTO alerts (id, client_id, type, message) VALUES (?, ?, ?, ?)'
        ).bind(
          crypto.randomUUID(),
          clientId,
          'missing_domain',
          `Client paid €${(amount/100).toFixed(2)} but no domain was submitted. Session: ${sessionId}. Email: ${email}. Ask client for domain.`
        ).run();

        // Alert Marian immediately
        await sendAdminAlert(env,
          `❗ Nová platba bez domény — ${email} zaplatil €${(amount/100).toFixed(2)}`,
          `Klient: ${email}\nČiastka: €${(amount/100).toFixed(2)}\nSession: ${sessionId}\n\nDoplň doménu manuálne v Stripe Dashboard a spusti audit cez:\ncurl -X POST https://api.marianstancik.dev/api/audit/run -H 'Content-Type: application/json' -d '{"domain":"..."}'`
        );

        return new Response(JSON.stringify({
          status: 'pending_domain',
          client_id: clientId,
          note: 'Platform received payment but needs domain to run the audit. Marian has been notified.'
        }), { headers: { 'content-type': 'application/json' } });
      }

      // Normal flow — we have domain + email
      const clientId = crypto.randomUUID();
      await env.DB.prepare(
        'INSERT INTO clients (id, email, domain, name, stripe_customer_id, plan) VALUES (?, ?, ?, ?, ?, ?)'
      ).bind(clientId, email, domain, name, data.customer || sessionId, 'one-time').run();

      // Run the audit
      try {
        await runAudit(domain, 'geo', env, clientId);
        
        // Send client confirmation email with invoice details & audit dashboard
        try {
          const dashUrl = `${env.APP_URL || 'https://app.marianstancik.dev'}?client=${clientId}`;
          const formattedAmount = (amount / 100).toFixed(2);
          const emailSubject = `Potvrdenie platby a faktúra — AI GEO Audit (${domain})`;
          const emailText = `Ahoj ${name},\n\nďakujeme za tvoju platbu €${formattedAmount} za AI GEO Audit pre doménu ${domain}.\n\nPlatba prebehla úspešne cez Stripe (ID relácie: ${sessionId.slice(0, 16)}).\nFaktúru / daňový doklad vystavený k tejto objednávke nájdeš evidovaný v systéme a na Stripe.\n\nSledovanie auditu a výsledky:\n${dashUrl}\n\nV prípade akýchkoľvek otázok stačí odpovedať na tento e-mail.\n\n--\nMarián Stančík (marianstancik.dev)\nIČO: 57068917 · Brezno, Slovensko`;

          await sendAgentMail(env, email, emailSubject, emailText);
        } catch (emailErr) {
          console.error(`Client email failed: ${emailErr.message}`);
        }
      } catch (auditError) {
        // Audit failed, log it
        await env.DB.prepare(
          'INSERT INTO alerts (id, client_id, type, message) VALUES (?, ?, ?, ?)'
        ).bind(crypto.randomUUID(), clientId, 'audit_failed', `Audit for ${domain} failed: ${auditError.message}`).run();
        
        await sendAdminAlert(env,
          `⚠️ Audit failed for ${domain}`, 
          `Client: ${email}\nDomain: ${domain}\nError: ${auditError.message}`
        );
      }

      return new Response(JSON.stringify({ client_id: clientId, status: 'audit_started' }), {
        headers: { 'content-type': 'application/json' }
      });
    }

    case 'invoice.paid': {
      // Subscription renewal
      try {
        const subId = data.subscription;
        const customerId = data.customer;
        const { results } = await env.DB.prepare(
          'SELECT id FROM clients WHERE stripe_customer_id = ?'
        ).bind(customerId).all();

        if (results.length) {
          await env.DB.prepare(
            'UPDATE subscriptions SET next_billing_at = ? WHERE stripe_subscription_id = ?'
          ).bind(
            new Date((data.lines?.data?.[0]?.period?.end || Date.now()/1000) * 1000).toISOString(),
            subId
          ).run();
        } else {
          // Unknown subscription
          await sendAdminAlert(env,
            `⚠️ Subscription renewal from unknown customer`,
            `Customer: ${customerId}\nSubscription: ${subId}\nAmount: €${(data.amount_paid/100).toFixed(2)}`
          );
        }
      } catch (e) {
        console.error(`invoice.paid handler error: ${e.message}`);
      }
      break;
    }

    case 'customer.subscription.deleted': {
      try {
        const subId = data.id;
        await env.DB.prepare(
          'UPDATE subscriptions SET status = ? WHERE stripe_subscription_id = ?'
        ).bind('cancelled', subId).run();
      } catch (e) { /* silent */ }
      break;
    }
  }

  return new Response(JSON.stringify({ received: true }), {
    headers: { 'content-type': 'application/json' }
  });
}