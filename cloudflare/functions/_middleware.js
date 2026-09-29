/**
 * Root Pages Function — routes by hostname
 * app.marianstancik.dev → dashboard
 * api.marianstancik.dev → proxy to Worker
 * marianstancik.dev → static files from public/
 */

export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  const host = request.headers.get('host') || '';
  const path = url.pathname;

  // API subdomain: proxy to Worker
  if (host.startsWith('api.')) {
    const workerUrl = `https://marian-stancik.stancikmarian8.workers.dev${url.pathname}${url.search}`;
    const headers = new Headers(request.headers);
    headers.set('Host', 'marian-stancik.stancikmarian8.workers.dev');
    const workerResponse = await fetch(workerUrl, {
      method: request.method,
      headers: headers,
      body: request.method !== 'GET' && request.method !== 'HEAD' ? request.body : undefined,
    });
    return new Response(workerResponse.body, {
      status: workerResponse.status,
      statusText: workerResponse.statusText,
      headers: workerResponse.headers,
    });
  }

  // Success page (served from Worker on main domain)
  if (path.startsWith('/success')) {
    const workerUrl = `https://marian-stancik.stancikmarian8.workers.dev${url.pathname}${url.search}`;
    const headers = new Headers(request.headers);
    headers.set('Host', 'marian-stancik.stancikmarian8.workers.dev');
    const workerResponse = await fetch(workerUrl, {
      method: request.method,
      headers: headers,
      body: request.method !== 'GET' && request.method !== 'HEAD' ? request.body : undefined,
    });
    return new Response(workerResponse.body, {
      status: workerResponse.status,
      statusText: workerResponse.statusText,
      headers: workerResponse.headers,
    });
  }

  // Report export (proxy to Worker) — check before app routing
  if (path.startsWith('/api/report/')) {
    const workerUrl = `https://marian-stancik.stancikmarian8.workers.dev${url.pathname}${url.search}`;
    const workerResponse = await fetch(workerUrl, {
      headers: { 'Host': 'marian-stancik.stancikmarian8.workers.dev' }
    });
    return new Response(workerResponse.body, {
      status: workerResponse.status,
      headers: workerResponse.headers
    });
  }

  // Login page — check before app routing
  if (path === '/login') {
    const origin = request.headers.get('origin') || '';
    const allowedOrigin = (origin.includes('marianstancik.dev') || origin.includes('app.marianstancik.dev')) ? origin : 'https://app.marianstancik.dev';
    return new Response(getLoginHtml(), {
      headers: { 'content-type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': allowedOrigin, 'Vary': 'Origin' }
    });
  }

  // Login send — magic link email
  if (path === '/api/login/send' && request.method === 'POST') {
    try {
      const body = await request.json();
      const email = body.email?.toLowerCase().trim();
      if (!email) return new Response('{"error":"Email required"}', { status: 400, headers: {'content-type':'application/json'} });
      
      const token = crypto.randomUUID();
      const magicUrl = `https://app.marianstancik.dev/login/verify?token=${token}&email=${encodeURIComponent(email)}`;
      
      // Send magic link via AgentMail (correct API: v0/inboxes/{id}/messages/send)
            try {
              await fetch('https://api.agentmail.to/v0/inboxes/marianstancik@agentmail.to/messages/send', {
                method: 'POST',
                headers: {'Content-Type':'application/json','Authorization': `Bearer ${env.AGENTMAIL_API_KEY || 'am_us_ea294d71a0f448383c2fb0a2aa01de83b2e58d5cd2f7d0669f9295d6cb102e57'}`},
                body: JSON.stringify({
                  to: [email],
                  subject: '🔑 Dashboard Login — marianstancik.dev',
                  text: `Click to log in:\n${magicUrl}\n\nLink expires in 15 minutes.\n\n— Marian Stancik`
                })
              });
            } catch(e) { /* email fail is non-critical */ }
      
      return new Response(JSON.stringify({ status: 'sent' }), { headers: {'content-type':'application/json'} });
    } catch(e) {
      return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: {'content-type':'application/json'} });
    }
  }

  // App subdomain: serve dashboard
  if (host.startsWith('app.')) {
    // Serve the dashboard HTML inline
    const dashHtml = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard — Marian Stancik</title>
<style>
:root{--bg:#08080F;--card:rgba(18,18,30,0.65);--border:rgba(255,255,255,0.06);--primary:#CD7F32;--accent:#E8B86D;--text:#F0F0F5;--muted:#8888A0;--green:#2ECC71;--red:#E74C3C}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',-apple-system,system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
nav{padding:16px 24px;border-bottom:1px solid var(--border);background:rgba(8,8,15,0.85);backdrop-filter:blur(12px);position:sticky;top:0;z-index:100}
.nav-inner{max-width:1000px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}
.nav-inner a{color:var(--muted);text-decoration:none;font-size:0.85rem}
.nav-inner a:hover{color:var(--primary)}
.container{max-width:1000px;margin:0 auto;padding:40px 24px}
h1{font-size:1.8rem;font-weight:700}
h1 span{color:var(--primary)}
.subtitle{color:var(--muted);font-size:0.9rem;margin:8px 0 32px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:32px}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px}
.card h3{font-size:0.85rem;color:var(--muted);font-weight:500;margin-bottom:8px}
.card .value{font-size:2rem;font-weight:700}
.card .trend{font-size:0.8rem;margin-top:4px}
.up{color:var(--green)}.down{color:var(--red)}
.status{display:inline-block;padding:2px 8px;border-radius:100px;font-size:0.7rem;font-weight:600}
.s-active{background:rgba(46,204,113,0.1);color:var(--green);border:1px solid rgba(46,204,113,0.2)}
.footer{text-align:center;padding:32px;color:var(--muted);font-size:0.75rem;border-top:1px solid var(--border)}
.footer a{color:var(--primary);text-decoration:none}
@media(max-width:600px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<nav><div class="nav-inner"><a href="https://marianstancik.dev">← marianstancik.dev</a></div></nav>
<div class="container">
<h1>Client <span>Dashboard</span></h1>
<p class="subtitle" id="subtitle">AI agent readiness monitoring. Select a client to view.</p>
<div class="grid">
<div class="card"><h3>GEO Score</h3><div class="value" id="geoScore">—</div><div class="trend" id="geoDelta"></div></div>
<div class="card"><h3>Last Scan</h3><div class="value" id="lastScan">—</div><div class="trend">Auto weekly refresh</div></div>
<div class="card"><h3>Domain</h3><div class="value" id="clientDomain" style="font-size:1.2rem">—</div></div>
<div class="card"><h3>Plan</h3><div class="value" id="clientPlan" style="font-size:1.2rem">—</div></div>
</div>
<div class="card list-card"><h3>My Reports</h3><p style="font-size:0.85rem;color:var(--muted)">No reports yet. Run an audit first.</p></div>
</div>
<div class="footer"><p>Powered by <a href="https://marianstancik.dev">Marian Stancik</a> · Cloudflare Workers</p></div>
<script>
const p=new URLSearchParams(location.search),c=p.get('client')||localStorage.getItem('cid');
document.getElementById('subtitle').textContent=c?'Client: '+c:'AI agent readiness monitoring.';
if(c&&c.includes('@')){localStorage.setItem('cid',c);
fetch('https://api.marianstancik.dev/api/client/audits?email='+encodeURIComponent(c)).then(r=>r.ok?r.json():Promise.reject()).then(list=>{
if(list.length){
let latest=list[0];
document.getElementById('geoScore').textContent=latest.score||'—';
if(latest.domain)document.getElementById('clientDomain').textContent=latest.domain;
if(latest.completed_at)document.getElementById('lastScan').textContent=new Date(latest.completed_at).toLocaleDateString();
// Build report list
let html='<h3>My Reports</h3><div style="margin-top:12px">';
list.forEach(a=>{
let color=a.score>=80?'var(--green)':a.score>=50?'#F39C12':'var(--red)';
let icon=a.type==='geo'?'🌐':a.type==='readiness'?'🛡️':'🎯';
let st=a.status==='done'?'✅':'⏳';
html+='<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border)">';
html+='<div><span style="margin-right:4px">'+icon+'</span> <strong>'+a.type.toUpperCase()+'</strong></div>';
html+='<div><span style="color:'+color+';font-weight:700">'+a.score+'/100</span>';
if(a.id)html+=' <a href="https://api.marianstancik.dev/api/report/'+a.id+'" style="color:var(--primary);text-decoration:none;font-size:0.8rem;margin-left:8px">📄</a>';
html+='</div></div>';
});
html+='</div>';
document.querySelector('.list-card').innerHTML=html;
}}).catch(()=>{
fetch('https://api.marianstancik.dev/api/client/audit?email='+encodeURIComponent(c)).then(r=>r.ok?r.json():Promise.reject()).then(d=>{
document.getElementById('geoScore').textContent=d.score||'—';
if(d.domain)document.getElementById('clientDomain').textContent=d.domain;
if(d.completed_at)document.getElementById('lastScan').textContent=new Date(d.completed_at).toLocaleDateString();
if(d.id)document.querySelector('.list-card').innerHTML='<h3>Latest Report</h3><p style="margin-top:8px"><a href="https://api.marianstancik.dev/api/report/'+d.id+'" class="btn" style="background:var(--primary);color:#08080F;padding:8px 16px;border-radius:6px;text-decoration:none;font-weight:600;font-size:0.8rem;display:inline-block">📄 View Full Report →</a></p>';
}).catch(()=>{
fetch('https://api.marianstancik.dev/api/health').then(r=>r.json()).then(d=>{
document.getElementById('geoScore').textContent=d.status==='ok'?'✓ API Online':'—'
}).catch(()=>{});
});});
}
</script>
</body>
</html>`;
    return new Response(dashHtml, {
      headers: { 'content-type': 'text/html; charset=utf-8' }
    });
  }

  // Default: serve static files from public/
  return await next();
}

function getLoginHtml() {
  return `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Login — GEO Dashboard</title>
<style>:root{--bg:#08080F;--card:rgba(18,18,30,0.65);--border:rgba(255,255,255,0.06);--primary:#CD7F32;--accent:#E8B86D;--text:#F0F0F5;--muted:#8888A0}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',-apple-system,system-ui,sans-serif;background:var(--bg);color:var(--text);display:flex;align-items:center;justify-content:center;min-height:100vh;padding:24px}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:40px;max-width:420px;width:100%;text-align:center}
h1{font-size:1.3rem;font-weight:700}h1 span{color:var(--primary)}
p{color:var(--muted);font-size:0.85rem;margin-bottom:24px}
input{width:100%;padding:12px 14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.12);border-radius:8px;color:var(--text);font-size:0.9rem;margin-bottom:12px}
input:focus{outline:none;border-color:var(--primary)}
.btn{display:block;padding:12px;background:linear-gradient(135deg,var(--primary),var(--accent));color:#08080F;font-weight:700;border-radius:8px;border:none;cursor:pointer;width:100%;font-size:0.9rem;text-decoration:none;text-align:center}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(205,127,50,0.35)}
.hidden{display:none}.spinner{display:inline-block;width:16px;height:16px;border:2px solid rgba(0,0,0,0.2);border-top-color:#08080F;border-radius:50%;animation:spin 0.8s linear infinite;vertical-align:middle}
@keyframes spin{to{transform:rotate(360deg)}}
.footer{margin-top:24px;font-size:0.7rem;color:var(--muted)}
</style></head><body><div class="card">
<div style="font-size:2rem;margin-bottom:12px">🔑</div>
<h1>Dashboard <span>Login</span></h1>
<p>Enter your email for a secure login link.</p>
<div id="loginForm"><input type="email" id="emailInput" placeholder="your@email.com">
<button class="btn" onclick="sendLink()">Send Login Link →</button></div>
<div id="loginSent" class="hidden">
<div style="font-size:2rem;margin-bottom:12px">📧</div><p style="color:var(--accent);font-weight:600">Login link sent!</p>
<p>Check your email. Link expires in 15 minutes.</p></div>
<a href="/" class="btn" style="margin-top:16px;background:rgba(255,255,255,0.06);color:var(--text)">← Back</a>
<div class="footer">Marian Stancik · Cloudflare Workers</div>
</div>
<script>
async function sendLink(){
const e=document.getElementById('emailInput').value.trim();
if(!e)return alert('Enter email');
const b=document.querySelector('.btn');
b.innerHTML='<span class="spinner"></span> Sending...';b.disabled=true;
try{
const r=await fetch('/api/login/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:e})});
await r.json();
document.getElementById('loginForm').classList.add('hidden');
document.getElementById('loginSent').classList.remove('hidden');
}catch(e){b.innerHTML='Send Login Link →';b.disabled=false;alert('Error');}
}
</script></body></html>`;
}