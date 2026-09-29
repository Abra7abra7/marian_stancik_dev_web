/**
 * Main router — spája všetky Workers do jedného
 * Routes:
 *   /api/audit/*    → audit-worker
 *   /api/stripe/*   → stripe-webhook
 *   /api/subscribe  → subscribe handler (newsletter)
 *   /api/crm-email  → CRM dispatcher
 *   /api/health     → health check
 *   /dashboard/*    → client dashboard (static)
 */

import { handleAuditRequest, runAudit } from './audit-worker';
import { handleStripeRequest } from './stripe-webhook';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS pre všetky API endpoints
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': 'https://marianstancik.dev',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization, Stripe-Signature',
          'Access-Control-Max-Age': '86400'
        }
      });
    }

    try {
      // Route: Audit
      if (path.startsWith('/api/audit')) {
        return await handleAuditRequest(request, env);
      }

      // Route: Stripe webhook
      if (path === '/api/stripe/webhook') {
        return await handleStripeRequest(request, env);
      }

      // Route: Subscribe (newsletter)
      if (path === '/api/subscribe' && request.method === 'POST') {
        const body = await request.json();
        const email = body.email;
        if (!email) return new Response(JSON.stringify({ error: 'Email required' }), { status: 400 });
        
        // Store to D1
        try {
          await env.DB.prepare(
            'INSERT INTO clients (id, email, domain, name, plan) VALUES (?, ?, ?, ?, ?)'
          ).bind(crypto.randomUUID(), email, 'newsletter', email.split('@')[0], 'newsletter').run();
        } catch (e) {
          // Duplicate is OK
        }

        // Notify via AgentMail
        try {
          await sendEmail(env, email);
        } catch (e) {
          // Email failure is non-critical
        }

        return new Response(JSON.stringify({ status: 'ok' }), {
          headers: { 'content-type': 'application/json' }
        });
      }

      // Route: CRM email
      if (path === '/api/crm-email' && request.method === 'POST') {
        const key = request.headers.get('x-crm-key') || 
                    request.headers.get('authorization')?.replace('Bearer ', '');
        if (key !== env.CRM_WEBHOOK_KEY) {
          return new Response('Unauthorized', { status: 401 });
        }
        
        const body = await request.json();
        // Forward to AgentMail
        const agentmailRes = await fetch('https://api.agentmail.to/v1/send', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${env.AGENTMAIL_API_KEY}`
          },
          body: JSON.stringify({
            to: body.to || 'marianstancik@agentmail.to',
            subject: body.subject,
            text: body.message
          })
        });

        return new Response(JSON.stringify({ status: agentmailRes.ok ? 'sent' : 'failed' }), {
          headers: { 'content-type': 'application/json' }
        });
      }

      // Route: Invoice proxy
      if (path === '/api/invoice' && request.method === 'GET') {
        const invoiceId = url.searchParams.get('id');
        if (!invoiceId) {
          return new Response('Missing invoice id', { status: 400 });
        }
        // Proxy to VPS backend (temporary, will be replaced with R2)
        const invoiceRes = await fetch(`https://api.marianstancik.dev/invoice/${invoiceId}`);
        const invoiceData = await invoiceRes.text();
        return new Response(invoiceData, {
          headers: {
            'content-type': 'application/pdf',
            'X-Robots-Tag': 'noindex, nofollow, noarchive',
            'Cache-Control': 'private, no-store'
          }
        });
      }

      // Route: Create Stripe checkout session
      if (path === '/api/stripe/create-checkout' && request.method === 'POST') {
        return await handleCreateCheckout(request, env);
      }

      // Route: Health
      if (path === '/api/health') {
        return new Response(JSON.stringify({ 
          status: 'ok', 
          service: 'marian-stancik-workers',
          region: 'weur',
          timestamp: new Date().toISOString()
        }), { headers: { 'content-type': 'application/json' } });
      }

      return new Response('Not found', { status: 404 });

    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), { 
        status: 500,
        headers: { 'content-type': 'application/json' }
      });
    }
  },

  // Cron triggers
  async scheduled(event, env, ctx) {
    if (event.cron === '0 6 * * MON') {
      // Weekly re-scan for subscription clients
      const { results: activeClients } = await env.DB.prepare(
        "SELECT * FROM clients WHERE status = 'active' AND plan IN ('monitoring', 'annual')"
      ).all();
      
      for (const client of activeClients) {
        ctx.waitUntil(runAudit(client.domain, 'geo', env, client.id));
      }
    }

    if (event.cron === '0 12 * * *') {
      // Daily compliance check
      const { results: activeClients } = await env.DB.prepare(
        "SELECT * FROM clients WHERE status = 'active' AND plan IN ('monitoring', 'annual', 'compliance_watch')"
      ).all();
      
      for (const client of activeClients) {
        // Lightweight check: just robots.txt + sitemap exist
        const res = await fetch(`https://${client.domain}/robots.txt`);
        if (!res.ok) {
          await env.DB.prepare(
            'INSERT INTO alerts (id, client_id, type, message) VALUES (?, ?, ?, ?)'
          ).bind(crypto.randomUUID(), client.id, 'site_down',
            `${client.domain} robots.txt returned ${res.status}`).run();
        }
      }
    }
  }
};

async function sendEmail(env, email) {
  try {
    await fetch('https://api.agentmail.to/v1/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${env.AGENTMAIL_API_KEY}`
      },
      body: JSON.stringify({
        to: email,
        subject: 'Thanks for subscribing — Marian Stancik',
        text: `Welcome! You'll receive updates on AI agent systems, GEO audits, and regulatory insights.\n\n— Marian Stancik\nmarianstancik.dev`
      })
    });
  } catch (e) {
    // Silent fail
  }
}

// Stripe checkout session creation
async function handleCreateCheckout(request, env) {
  try {
    const body = await request.json();
    const { priceId, domain, email, name } = body;

    if (!priceId || !domain || !email) {
      return new Response(JSON.stringify({ error: 'Missing required fields: priceId, domain, email' }), {
        status: 400,
        headers: { 'content-type': 'application/json' }
      });
    }

    // Create Stripe checkout session
    const stripeRes = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.STRIPE_SECRET_KEY}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        'mode': body.recurring ? 'subscription' : 'payment',
        'success_url': `${env.APP_URL || 'https://app.marianstancik.dev'}/success?session_id={CHECKOUT_SESSION_ID}`,
        'cancel_url': `${env.SITE_URL || 'https://marianstancik.dev'}/services`,
        'line_items[0][price]': priceId,
        'line_items[0][quantity]': '1',
        'customer_email': email,
        'metadata[domain]': domain,
        'metadata[name]': name || email.split('@')[0]
      })
    });

    const session = await stripeRes.json();

    if (!stripeRes.ok) {
      return new Response(JSON.stringify({ error: session.error?.message || 'Stripe error' }), {
        status: 400,
        headers: { 'content-type': 'application/json' }
      });
    }

    return new Response(JSON.stringify({ url: session.url, session_id: session.id }), {
      headers: { 'content-type': 'application/json' }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), {
      status: 500,
      headers: { 'content-type': 'application/json' }
    });
  }
}