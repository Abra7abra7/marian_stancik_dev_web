// Cloudflare Pages Middleware — Content Negotiation & Edge Routing

// Best-effort per-isolate rate limit for POST /api/* (form abuse protection, no captcha).
// Combined with the honeypot checks in /api/subscribe and a Cloudflare dashboard
// rate-limiting rule for full coverage. Each isolate holds its own map — good enough
// as a cheap first line; a determined attacker hits the CF rule instead.
const RATE = new Map(); // ip -> { count, reset }
const RATE_MAX = 8;     // POST requests per IP per window
const RATE_WINDOW = 60_000; // 1 minute

function rateLimited(ip) {
  const now = Date.now();
  const e = RATE.get(ip);
  if (!e || now > e.reset) {
    RATE.set(ip, { count: 1, reset: now + RATE_WINDOW });
    if (RATE.size > 10_000) RATE.clear(); // cheap GC for long-lived isolates
    return false;
  }
  e.count += 1;
  return e.count > RATE_MAX;
}

export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);

  // Apex domain redirect to www canonical
  if (url.hostname === 'marianstancik.dev') {
    url.hostname = 'www.marianstancik.dev';
    return Response.redirect(url.toString(), 308);
  }

  // Rate-limit form/API POSTs (skips the markdown negotiation below)
  if (request.method === 'POST' && url.pathname.startsWith('/api/')) {
    const ip = request.headers.get('cf-connecting-ip') || 'unknown';
    if (rateLimited(ip)) {
      return new Response(JSON.stringify({ error: 'Too many requests. Try again in a minute.' }), {
        status: 429,
        headers: { 'Content-Type': 'application/json', 'Retry-After': '60' }
      });
    }
  }

  const accept = request.headers.get('accept') || '';

  // Markdown content negotiation for AI engines (llmstxt / Accept: text/markdown)
  if (accept.includes('text/markdown')) {
    if (url.pathname === '/' || url.pathname === '') {
      return context.env.ASSETS.fetch(new URL('/index.html.md', request.url));
    }
    if (url.pathname === '/blog' || url.pathname === '/blog/') {
      return context.env.ASSETS.fetch(new URL('/blog/index.html.md', request.url));
    }
    if (url.pathname.startsWith('/blog/posts/')) {
      const cleanPath = url.pathname.replace(/\/$/, '');
      if (!cleanPath.endsWith('.md')) {
        return context.env.ASSETS.fetch(new URL(`${cleanPath}.md`, request.url));
      }
    }
  }

  return await next();
}
