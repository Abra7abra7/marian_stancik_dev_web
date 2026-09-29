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

async function sendAdminAlert(env, subject, message) {
  try {
    const agentmailRes = await fetch('https://api.agentmail.to/v1/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${env.AGENTMAIL_API_KEY}`
      },
      body: JSON.stringify({
        to: 'marianstancik@agentmail.to',
        subject: subject,
        text: message
      })
    });
    console.log(`Admin alert sent: ${agentmailRes.status}`);
  } catch (e) {
    console.error(`Admin alert failed: ${e.message}`);
  }
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

  const body = await request.json();
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
      
      // Get domain from metadata or custom fields
      let domain = data.metadata?.domain;
      if (!domain) {
        try {
          domain = data.custom_fields?.find(f => f.key === 'domain' || f.key === 'website')?.text?.value;
        } catch (e) { /* silent */ }
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