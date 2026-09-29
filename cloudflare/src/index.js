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

      // Route: Success page after Stripe payment
      if (path === '/success') {
        const sessionId = url.searchParams.get('session_id');
        return new Response(getSuccessHtml(sessionId), {
          headers: { 'content-type': 'text/html; charset=utf-8' }
        });
      }

      // Route: Root redirect
      if (path === '/') {
        return Response.redirect('https://marianstancik.dev', 302);
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

async function sendEmail(env, email, subject, text) {
  try {
    await fetch('https://api.agentmail.to/v1/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${env.AGENTMAIL_API_KEY}`
      },
      body: JSON.stringify({
        to: email,
        subject: subject || 'Thanks for subscribing — Marian Stancik',
        text: text || `Welcome! You'll receive updates on AI agent systems, GEO audits, and regulatory insights.\n\n— Marian Stancik\nmarianstancik.dev`
      })
    });
  } catch (e) {
    console.error(`Email send failed: ${e.message}`);
  }
}

function getSuccessHtml(sessionId) {
  return `<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Payment Successful — Marian Stancik</title>
<style>:root{--bg:#08080F;--card:rgba(18,18,30,0.65);--border:rgba(255,255,255,0.06);--primary:#CD7F32;--accent:#E8B86D;--text:#F0F0F5;--muted:#8888A0;--green:#2ECC71}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',-apple-system,system-ui,sans-serif;background:var(--bg);color:var(--text);display:flex;align-items:center;justify-content:center;min-height:100vh;padding:24px}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:48px 40px;max-width:520px;width:100%;text-align:center}
.icon{font-size:3rem;margin-bottom:16px}
h1{font-size:1.5rem;font-weight:700;margin-bottom:8px;color:var(--text)}
h1 span{color:var(--primary)}
p{color:var(--muted);font-size:0.9rem;line-height:1.6;margin-bottom:24px}
.btn{display:inline-block;padding:12px 28px;background:linear-gradient(135deg,var(--primary),var(--accent));color:#08080F;font-weight:700;border-radius:8px;text-decoration:none;font-size:0.9rem;transition:all 0.3s;border:none;cursor:pointer}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(205,127,50,0.35)}
.detail{font-size:0.75rem;color:var(--muted);margin-top:20px;padding-top:20px;border-top:1px solid var(--border)}
</style></head>
<body>
<div class="card">
<div class="icon">✅</div>
<h1>Payment <span>Successful</span></h1>
<p>Your order has been received and is being processed.<br>Your AI GEO audit will begin automatically.<br>You will receive the report within 48 hours.</p>
<a href="https://marianstancik.dev" class="btn">← Back to Home</a>
<div class="detail">Session: ${sessionId || 'completed'}<br>Questions? Email marianstancik@agentmail.to</div>
</div>
</body>
</html>`;

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
        'success_url': `${env.SITE_URL || 'https://marianstancik.dev'}/success?session_id={CHECKOUT_SESSION_ID}`,
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