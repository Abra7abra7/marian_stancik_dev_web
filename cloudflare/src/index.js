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

import { handleAuditRequest, runAudit, runComplianceCheck } from './audit-worker';
import { handleStripeRequest } from './stripe-webhook';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS pre všetky API endpoints
    if (request.method === 'OPTIONS') {
      const origin = request.headers.get('origin') || '';
      const allowedOrigin = (origin.includes('marianstancik.dev') || origin.includes('app.marianstancik.dev') || origin.includes('localhost'))
        ? origin : 'https://marianstancik.dev';
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': allowedOrigin,
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization, Stripe-Signature',
          'Access-Control-Max-Age': '86400'
        }
      });
    }

    try {
      const origin = request.headers.get('origin') || '';
      const allowedOrigin = (origin.includes('marianstancik.dev') || origin.includes('app.marianstancik.dev'))
        ? origin : 'https://marianstancik.dev';
      const corsHeaders = {
        'Access-Control-Allow-Origin': allowedOrigin,
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Vary': 'Origin'
      };

      // Route: Audit
      if (path.startsWith('/api/audit')) {
        return await handleAuditRequest(request, env);
      }

      // Route: Compliance check (for cron + manual trigger)
      if (path === '/api/compliance/check' && request.method === 'POST') {
        return await handleComplianceCheck(request, env);
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

      // Route: Report export
      if (path.startsWith('/api/report/') && request.method === 'GET') {
        return await handleReportExport(request, env);
      }

      // Route: Get latest audit by client email
      if (path === '/api/client/audit' && request.method === 'GET') {
        const email = url.searchParams.get('email');
        if (!email) return new Response(JSON.stringify({ error: 'email required' }), { status: 400, headers: {'content-type':'application/json',...corsHeaders} });
        // Try 1: JOIN by email → get latest audit
        let { results } = await env.DB.prepare(
          'SELECT a.id, a.score, a.type, a.status, a.completed_at, a.baseline_score, a.score_delta, ar.summary, ar.recommendations, c.domain, c.plan, c.email ' +
          'FROM audits a ' +
          'LEFT JOIN audit_results ar ON a.id = ar.audit_id ' +
          'LEFT JOIN clients c ON a.client_id = c.id ' +
          'WHERE c.email = ? ORDER BY a.completed_at DESC LIMIT 1'
        ).bind(email).all();
        if (!results.length) {
          const { results: r2 } = await env.DB.prepare(
            'SELECT a.id, a.score, a.type, a.status, a.completed_at, a.baseline_score, a.score_delta, ar.summary, ar.recommendations ' +
            'FROM audits a LEFT JOIN audit_results ar ON a.id = ar.audit_id ' +
            'WHERE a.client_id = ? ORDER BY a.completed_at DESC LIMIT 1'
          ).bind(email).all();
          results = r2;
        }
        if (!results.length) return new Response(JSON.stringify({ error: 'No audit found for this email' }), { status: 404, headers: {'content-type':'application/json',...corsHeaders} });
        return new Response(JSON.stringify(results[0]), { headers: {'content-type':'application/json',...corsHeaders} });
      }

      // Route: Get all audits for a client
      if (path === '/api/client/audits' && request.method === 'GET') {
        const email = url.searchParams.get('email');
        if (!email) return new Response(JSON.stringify({ error: 'email required' }), { status: 400, headers: {'content-type':'application/json',...corsHeaders} });
        let { results } = await env.DB.prepare(
                  'SELECT a.id, a.score, a.type, a.status, a.completed_at, ar.summary ' +
                  'FROM audits a ' +
                  'LEFT JOIN audit_results ar ON a.id = ar.audit_id ' +
                  'WHERE a.client_id IN (SELECT id FROM clients WHERE email = ?) ' +
                  'ORDER BY a.completed_at DESC'
                ).bind(email).all();
        if (!results.length) {
          const { results: r2 } = await env.DB.prepare(
            'SELECT a.id, a.score, a.type, a.status, a.completed_at, ar.summary ' +
            'FROM audits a LEFT JOIN audit_results ar ON a.id = ar.audit_id ' +
            'WHERE a.client_id = ? ORDER BY a.completed_at DESC'
          ).bind(email).all();
          results = r2;
        }
        if (!results.length) return new Response(JSON.stringify({ error: 'No audits found for this email' }), { status: 404, headers: {'content-type':'application/json',...corsHeaders} });
        return new Response(JSON.stringify(results), { headers: {'content-type':'application/json',...corsHeaders} });
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

      // Success page redirect (handled by main web)
      if (path === '/success') {
        return Response.redirect('https://marianstancik.dev/success?session_id=' + (url.searchParams.get('session_id') || ''), 302);
      }

      // Route: Root redirect
      if (path === '/') {
        return Response.redirect('https://marianstancik.dev', 302);
      }

      return new Response('Not found', { status: 404 });

    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), { 
        status: 500,
        headers: { 'content-type': 'application/json', ...corsHeaders }
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

// Compliance check handler
async function handleComplianceCheck(request, env) {
  try {
    const body = await request.json();
    const { domain, clientId } = body;
    if (!domain) return new Response(JSON.stringify({ error: 'Domain required' }), { status: 400 });
    const result = await runComplianceCheck(domain, env, clientId);
    return new Response(JSON.stringify(result), { headers: { 'content-type': 'application/json' } });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: { 'content-type': 'application/json' } });
  }
}

// Report export handler
async function handleReportExport(request, env) {
  const url = new URL(request.url);
  const auditId = url.pathname.split('/')[3];
  if (!auditId) return new Response('Missing audit ID', { status: 400 });
  
  try {
    const { results } = await env.DB.prepare(
      'SELECT a.id, a.score, a.type, a.status, a.completed_at, a.baseline_score, a.score_delta, ' +
      'ar.raw, ar.summary, ar.recommendations, c.email, c.domain ' +
      'FROM audits a ' +
      'LEFT JOIN audit_results ar ON a.id = ar.audit_id ' +
      'LEFT JOIN clients c ON a.client_id = c.id ' +
      'WHERE a.id = ?'
    ).bind(auditId).all();
    
    if (!results.length) return new Response('Audit not found', { status: 404 });
    
    const audit = results[0];
    const data = typeof audit.raw === 'string' ? JSON.parse(audit.raw) : (audit.raw || {});
    const recs = typeof audit.recommendations === 'string' ? JSON.parse(audit.recommendations) : (audit.recommendations || []);
    const score = audit.score || data.score || 0;
    const resultsList = data.results || [];
    const passed = resultsList.filter(r => r.passed).length;
    const domain = audit.domain || data.domain || '?';
    
    return new Response(generateReportHtml(audit, data, recs, score, resultsList, passed, domain), {
      headers: {
        'content-type': 'text/html; charset=utf-8',
        'Content-Disposition': `inline; filename="geo-audit-${domain}.html"`
      }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: { 'content-type': 'application/json' } });
  }
}

function generateReportHtml(audit, data, recommendations, score, results, passed, domain) {
  const date = audit.completed_at ? new Date(audit.completed_at).toLocaleDateString() : 'Today';
  const total = results.length;
  
  return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>GEO Audit Report</title>' +
  '<style>:root{--bg:#08080F;--card:rgba(18,18,30,0.65);--border:rgba(255,255,255,0.06);--primary:#CD7F32;--accent:#E8B86D;--text:#F0F0F5;--muted:#8888A0;--green:#2ECC71;--red:#E74C3C}' +
  '*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;background:var(--bg);color:var(--text);padding:40px 24px;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}' +
  '.header{text-align:center;margin-bottom:32px;padding-bottom:20px;border-bottom:1px solid var(--border)}h1{font-size:1.6rem;font-weight:700}h1 span{color:var(--primary)}' +
  '.meta{color:var(--muted);font-size:0.85rem}.score-box{display:inline-block;padding:12px 24px;border-radius:12px;font-size:2rem;font-weight:700;margin:16px 0;background:rgba(46,204,113,0.1);border:2px solid var(--green);color:var(--green)}' +
  'h2{font-size:1rem;font-weight:600;color:var(--accent);margin:24px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--border)}' +
  'table{width:100%;border-collapse:collapse;font-size:0.85rem}th{text-align:left;padding:8px 12px;color:var(--muted);font-weight:500;border-bottom:1px solid var(--border)}' +
  'td{padding:8px 12px;border-bottom:1px solid rgba(255,255,255,0.03);color:#B0B0C8}.pass{color:var(--green)}.fail{color:var(--red)}' +
  '.rec-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:12px 16px;margin-bottom:8px}' +
  '.rec-card h3{font-size:0.85rem;font-weight:600;color:var(--accent)}.rec-card p{font-size:0.8rem;color:var(--muted)}' +
  '.btn{display:inline-block;padding:8px 20px;background:var(--primary);color:#08080F;border:none;border-radius:6px;cursor:pointer;font-weight:600;margin-top:16px}' +
  '.footer{text-align:center;margin-top:32px;padding-top:16px;border-top:1px solid var(--border);font-size:0.75rem;color:var(--muted)}' +
  '@media print{body{background:#fff;color:#333}.score-box{background:#f5f5f5;border-color:#ddd}h1 span{color:#CD7F32}}</style></head><body>' +
  '<div class="header"><h1>GEO <span>Audit Report</span></h1>' +
  '<div class="meta"><div><strong>Domain:</strong> ' + domain + '</div><div><strong>Date:</strong> ' + date + '</div>' +
  '<div><strong>Type:</strong> ' + (audit.type || 'geo') + '</div><div><strong>Score:</strong> ' + score + '/100</div></div>' +
  '<div class="score-box">' + score + '/100</div><div class="meta">' + passed + '/' + total + ' checks passed</div></div>' +
  '<h2>Check Results</h2><table><tr><th>Check</th><th>Status</th><th>Detail</th><th>Weight</th></tr>' +
  results.map(r => '<tr><td>' + r.check + '</td><td class="' + (r.passed ? 'pass' : 'fail') + '">' + (r.passed ? '✅' : '❌') + '</td><td>' + (r.detail || '—') + '</td><td>' + (r.weight || '—') + '</td></tr>').join('') +
  '</table>' +
  (recommendations?.length ? '<h2>Recommendations</h2>' + recommendations.map(r =>
    '<div class="rec-card"><h3>' + r.check + '</h3><p><strong>Severity:</strong> ' + (r.severity || 'medium') + '</p><p>' + (r.detail || '') + '</p></div>'
  ).join('') : '') +
  '<div class="footer"><p>Generated by Hermes Agent · Marian Stancik · Cloudflare Workers</p>' +
  '<p><button class="btn" onclick="window.print()">🖨 Print / Save PDF</button></p></div>' +
  '</body></html>';
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