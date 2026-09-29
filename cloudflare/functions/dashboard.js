/**
 * Dashboard Functions — login + report viewer
 * Routes handled by the root _middleware.js
 */

// ============================================
// MAGIC LINK LOGIN
// ============================================

const MAGIC_LINK_TTL = 15 * 60 * 1000; // 15 minutes

export async function handleMagicLink(request, env) {
  const url = new URL(request.url);
  const path = url.pathname;
  
  // GET /login → show login form
  if (path === '/login' && request.method === 'GET') {
    return new Response(getLoginHtml(), {
      headers: { 'content-type': 'text/html; charset=utf-8' }
    });
  }
  
  // POST /api/login/send → send magic link
  if (path === '/api/login/send' && request.method === 'POST') {
    const body = await request.json();
    const email = body.email?.toLowerCase().trim();
    if (!email) return new Response(JSON.stringify({ error: 'Email required' }), { status: 400 });
    
    // Verify client exists in D1
    const { results } = await env.DB.prepare(
      'SELECT id, email FROM clients WHERE email = ? AND status = ?'
    ).bind(email, 'active').all();
    
    if (!results.length) {
      // Client not found, return generic message (don't reveal if email exists)
      return new Response(JSON.stringify({ status: 'sent' }), {
        headers: { 'content-type': 'application/json' }
      });
    }
    
    const client = results[0];
    const token = crypto.randomUUID();
    const expiresAt = new Date(Date.now() + MAGIC_LINK_TTL).toISOString();
    
    // Store token in D1
    await env.DB.prepare(
      'INSERT INTO alerts (id, client_id, type, message) VALUES (?, ?, ?, ?)'
    ).bind(token, client.id, 'magic_link', `token=${token} expires=${expiresAt}`).run();
    
    // Send magic link email
    const magicUrl = `${env.APP_URL || 'https://app.marianstancik.dev'}/login/verify?token=${token}&client=${client.id}`;
    
    try {
      await fetch('https://api.agentmail.to/v1/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${env.AGENTMAIL_API_KEY || 'am_us_ea294d71a0f448383c2fb0a2aa01de83b2e58d5cd2f7d0669f9295d6cb102e57'}`
        },
        body: JSON.stringify({
          to: email,
          subject: '🔑 Your Dashboard Login Link — marianstancik.dev',
          text: `Click this link to log in to your dashboard:\n${magicUrl}\n\nThis link expires in 15 minutes.\n\nIf you didn't request this, ignore this email.\n\n— Marian Stancik`
        })
      });
    } catch (e) { /* email fail is non-critical */ }
    
    return new Response(JSON.stringify({ status: 'sent' }), {
      headers: { 'content-type': 'application/json' }
    });
  }
  
  // GET /login/verify?token=... → verify magic link
  if (path === '/login/verify' && request.method === 'GET') {
    const token = url.searchParams.get('token');
    const clientId = url.searchParams.get('client');
    
    if (!token || !clientId) {
      return new Response(getLoginHtml('Invalid or expired link.'), {
        headers: { 'content-type': 'text/html; charset=utf-8' }
      });
    }
    
    // Verify token exists in D1
    const { results } = await env.DB.prepare(
      'SELECT message, acknowledged FROM alerts WHERE id = ? AND client_id = ? AND type = ?'
    ).bind(token, clientId, 'magic_link').all();
    
    if (!results.length) {
      return new Response(getLoginHtml('Invalid or expired link. Please request a new one.'), {
        headers: { 'content-type': 'text/html; charset=utf-8' }
      });
    }
    
    // Mark token as used
    await env.DB.prepare(
      'UPDATE alerts SET acknowledged = ? WHERE id = ?'
    ).bind(1, token).run();
    
    // Generate session cookie
    const sessionToken = crypto.randomUUID();
    const response = new Response(null, {
      status: 302,
      headers: {
        'Location': `/dashboard?client=${clientId}&session=${sessionToken}`,
        'Set-Cookie': `session=${sessionToken}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=86400`
      }
    });
    return response;
  }
  
  return null; // Not handled
}

// ============================================
// REPORT GENERATION
// ============================================

export async function handleReportExport(request, env) {
  const url = new URL(request.url);
  const path = url.pathname;
  
  // GET /api/report/{auditId} → return audit report as printable HTML
  if (path.startsWith('/api/report/') && request.method === 'GET') {
    const auditId = path.split('/')[3];
    if (!auditId) return new Response('Missing audit ID', { status: 400 });
    
    const { results } = await env.DB.prepare(
      'SELECT a.*, ar.raw, ar.summary, ar.recommendations, c.email, c.domain ' +
      'FROM audits a ' +
      'LEFT JOIN audit_results ar ON a.id = ar.audit_id ' +
      'LEFT JOIN clients c ON a.client_id = c.id ' +
      'WHERE a.id = ?'
    ).bind(auditId).all();
    
    if (!results.length) return new Response('Audit not found', { status: 404 });
    
    const audit = results[0];
    const data = typeof audit.raw === 'string' ? JSON.parse(audit.raw) : audit.raw;
    const recs = typeof audit.recommendations === 'string' ? JSON.parse(audit.recommendations) : (audit.recommendations || []);
    
    return new Response(generateReportHtml(audit, data, recs), {
      headers: {
        'content-type': 'text/html; charset=utf-8',
        'Content-Disposition': `inline; filename="geo-audit-${audit.domain}-${audit.completed_at?.slice(0,10) || 'report'}.html"`
      }
    });
  }
  
  return null;
}

// ============================================
// HTML GENERATORS
// ============================================

function getLoginHtml(error = '') {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login — GEO Dashboard</title>
<style>
:root{--bg:#08080F;--card:rgba(18,18,30,0.65);--border:rgba(255,255,255,0.06);--primary:#CD7F32;--accent:#E8B86D;--text:#F0F0F5;--muted:#8888A0}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',-apple-system,system-ui,sans-serif;background:var(--bg);color:var(--text);display:flex;align-items:center;justify-content:center;min-height:100vh;padding:24px}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:40px;max-width:420px;width:100%;text-align:center}
h1{font-size:1.3rem;font-weight:700;margin-bottom:8px}
h1 span{color:var(--primary)}
p{color:var(--muted);font-size:0.85rem;line-height:1.5;margin-bottom:24px}
.error{color:#E74C3C;font-size:0.8rem;margin-bottom:16px;padding:8px 12px;background:rgba(231,76,60,0.1);border:1px solid rgba(231,76,60,0.2);border-radius:8px}
input{width:100%;padding:12px 14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.12);border-radius:8px;color:var(--text);font-size:0.9rem;margin-bottom:12px;box-sizing:border-box}
input:focus{outline:none;border-color:var(--primary);background:rgba(255,255,255,0.06)}
.btn{display:inline-block;padding:12px 28px;background:linear-gradient(135deg,var(--primary),var(--accent));color:#08080F;font-weight:700;border-radius:8px;text-decoration:none;font-size:0.9rem;transition:all 0.3s;border:none;cursor:pointer;width:100%}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(205,127,50,0.35)}
.hidden{display:none}
.spinner{display:inline-block;width:16px;height:16px;border:2px solid rgba(0,0,0,0.2);border-top-color:#08080F;border-radius:50%;animation:spin 0.8s linear infinite;vertical-align:middle;margin-right:8px}
@keyframes spin{to{transform:rotate(360deg)}}
.footer{margin-top:24px;font-size:0.7rem;color:var(--muted)}
</style>
</head>
<body>
<div class="card">
  <div style="font-size:2rem;margin-bottom:12px">🔑</div>
  <h1>Dashboard <span>Login</span></h1>
  <p>Enter your email to receive a secure login link. No password needed.</p>
  ${error ? `<div class="error">${error}</div>` : ''}
  <div id="loginForm">
    <input type="email" id="emailInput" placeholder="your@email.com" autocomplete="email">
    <button class="btn" onclick="sendMagicLink()">Send Login Link →</button>
  </div>
  <div id="loginSent" class="hidden">
    <div style="font-size:2rem;margin-bottom:12px">📧</div>
    <p style="color:var(--accent);font-weight:600">Login link sent!</p>
    <p>Check your email. The link expires in 15 minutes.</p>
  </div>
  <div class="footer">Powered by Marian Stancik · Cloudflare Workers</div>
</div>
<script>
async function sendMagicLink() {
  const email = document.getElementById('emailInput').value.trim();
  if (!email) return alert('Please enter your email');
  const btn = document.querySelector('.btn');
  btn.innerHTML = '<span class="spinner"></span> Sending...';
  btn.disabled = true;
  try {
    const r = await fetch('/api/login/send', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({email})
    });
    const d = await r.json();
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('loginSent').classList.remove('hidden');
  } catch(e) {
    btn.innerHTML = 'Send Login Link →';
    btn.disabled = false;
    alert('Error: ' + e.message);
  }
}
</script>
</body>
</html>`;
}

function generateReportHtml(audit, data, recommendations) {
  const score = audit.score || data?.score || 0;
  const domain = audit.domain || data?.domain || '?';
  const date = audit.completed_at ? new Date(audit.completed_at).toLocaleDateString() : 'Today';
  const results = data?.results || [];
  const passed = results.filter(r => r.passed).length;
  const total = results.length;
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GEO Audit Report — ${domain}</title>
<style>
:root{--bg:#08080F;--card:rgba(18,18,30,0.65);--border:rgba(255,255,255,0.06);--primary:#CD7F32;--accent:#E8B86D;--text:#F0F0F5;--muted:#8888A0;--green:#2ECC71;--red:#E74C3C}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',-apple-system,system-ui,sans-serif;background:var(--bg);color:var(--text);padding:40px 24px;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.header{text-align:center;margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid var(--border)}
h1{font-size:1.6rem;font-weight:700}
h1 span{color:var(--primary)}
.meta{color:var(--muted);font-size:0.85rem;margin-top:8px}
.score-box{display:inline-block;padding:12px 24px;border-radius:12px;font-size:2rem;font-weight:700;margin:16px 0;background:rgba(46,204,113,0.1);border:2px solid var(--green);color:var(--green)}
.section{margin-bottom:28px}
h2{font-size:1rem;font-weight:600;color:var(--accent);margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--border)}
table{width:100%;border-collapse:collapse;font-size:0.85rem}
th{text-align:left;padding:8px 12px;color:var(--muted);font-weight:500;border-bottom:1px solid var(--border)}
td{padding:8px 12px;border-bottom:1px solid rgba(255,255,255,0.03);color:#B0B0C8}
.pass{color:var(--green)}
.fail{color:var(--red)}
.rec-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:12px 16px;margin-bottom:8px}
.rec-card h3{font-size:0.85rem;font-weight:600;margin-bottom:4px;color:var(--accent)}
.rec-card p{font-size:0.8rem;color:var(--muted)}
.rec-high{border-left:3px solid var(--red)}
.rec-med{border-left:3px solid #F39C12}
@media print{body{background:#fff;color:#333;padding:20px}.card,.score-box{background:#f5f5f5;border-color:#ddd;}h1 span{color:#CD7F32}.meta{color:#666}.section h2{color:#CD7F32}.rec-card{background:#f9f9f9;border-color:#eee}}
</style>
</head>
<body>
<div class="header">
  <h1>GEO <span>Audit Report</span></h1>
  <div class="meta">
    <div><strong>Domain:</strong> ${domain}</div>
    <div><strong>Date:</strong> ${date}</div>
    <div><strong>Type:</strong> ${audit.type || 'geo'}</div>
    <div><strong>Client:</strong> ${audit.email || '?'}</div>
  </div>
  <div class="score-box">${score}/100</div>
  <div class="meta">${passed}/${total} checks passed</div>
</div>

<div class="section">
  <h2>📋 Check Results</h2>
  <table>
    <tr><th>Check</th><th>Status</th><th>Detail</th><th>Weight</th></tr>
    ${results.map(r => `<tr>
      <td>${r.check}</td>
      <td class="${r.passed ? 'pass' : 'fail'}">${r.passed ? '✅ Pass' : '❌ Fail'}</td>
      <td>${r.detail || '—'}</td>
      <td>${r.weight || '—'}</td>
    </tr>`).join('')}
  </table>
</div>

${recommendations?.length ? `
<div class="section">
  <h2>🎯 Recommendations</h2>
  ${recommendations.map(r => `
    <div class="rec-card ${r.severity === 'high' ? 'rec-high' : 'rec-med'}">
      <h3>${r.check}</h3>
      <p><strong>Severity:</strong> ${r.severity || 'medium'}</p>
      <p>${r.detail || ''}</p>
      <p style="margin-top:4px;color:var(--accent)">${r.fix || ''}</p>
    </div>
  `).join('')}
</div>` : ''}

<div class="section" style="margin-top:32px;padding-top:20px;border-top:1px solid var(--border)">
  <div class="meta" style="text-align:center">
    <p>Generated by Hermes Agent · Cloudflare Workers · Marian Stancik</p>
    <p style="margin-top:4px">marianstancik.dev · EU AI Act Art. 50: AI-generated content</p>
    <p style="margin-top:8px"><button onclick="window.print()" style="padding:8px 20px;background:var(--primary);color:#08080F;border:none;border-radius:6px;cursor:pointer;font-weight:600">🖨️ Print / Save PDF</button></p>
  </div>
</div>
</body>
</html>`;
}