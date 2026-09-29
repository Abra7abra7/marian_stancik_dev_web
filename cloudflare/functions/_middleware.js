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
<div class="card"><h3>AI Crawler Access</h3>
<p style="font-size:0.85rem;color:#B0B0C8">GPTBot <span class="status s-active">✓</span> · ClaudeBot <span class="status s-active">✓</span> · PerplexityBot <span class="status s-active">✓</span> · Google-Extended <span class="status s-active">✓</span> · CCBot <span class="status s-active">✓</span></p>
</div>
</div>
<div class="footer"><p>Powered by <a href="https://marianstancik.dev">Marian Stancik</a> · Cloudflare Workers</p></div>
<script>
const p=new URLSearchParams(location.search),c=p.get('client')||localStorage.getItem('cid');
if(c){localStorage.setItem('cid',c);
fetch('https://api.marianstancik.dev/api/health').then(r=>r.json()).then(d=>{
document.getElementById('geoScore').textContent=d.status==='ok'?'✓ Online':'—'
}).catch(()=>{});
fetch('https://api.marianstancik.dev/api/audit/'+c).then(r=>r.json()).then(d=>{
if(d.score!==undefined)document.getElementById('geoScore').textContent=d.score;
if(d.completed_at)document.getElementById('lastScan').textContent=new Date(d.completed_at).toLocaleDateString();
if(d.score_delta!==null&&d.score_delta!==undefined)
document.getElementById('geoDelta').innerHTML=d.score_delta>=0?'<span class=up>▲ +'+d.score_delta+'</span>':'<span class=down>▼ '+d.score_delta+'</span>';
}).catch(()=>{});
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