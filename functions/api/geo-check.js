// Cloudflare Pages Function — Free AI-visibility snapshot (3 of 12 audit checks)
// GET /api/geo-check?domain=example.com
// Checks: llms.txt presence, AI crawlers in robots.txt, JSON-LD structured data on the homepage.
// The full 12-check audit is a paid product (€199) — this endpoint is intentionally a teaser.

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': 'https://www.marianstancik.dev',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}

const AI_CRAWLERS = [
  'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot',
  'anthropic-ai', 'PerplexityBot', 'Perplexity-User', 'Google-Extended',
  'CCBot', 'Bytespider', 'Amazonbot', 'Applebot-Extended', 'FacebookBot', 'Meta-ExternalAgent',
];

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
  });
}

function normalizeDomain(raw) {
  if (!raw) return null;
  let d = String(raw).trim().toLowerCase();
  d = d.replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/\/.*$/, '').replace(/[:?#].*$/, '');
  if (!/^[a-z0-9]([a-z0-9-]*\.)+[a-z]{2,24}$/.test(d)) return null;
  if (d.length > 253) return null;
  // block localhost / private / IP literals
  if (/^(localhost|.*\.local|.*\.test|.*\.example|.*\.invalid|127\.|10\.|192\.168\.|169\.254\.|0\.|\[?::1)/.test(d)) return null;
  if (/^\d{1,3}(\.\d{1,3}){3}$/.test(d)) return null;
  return d;
}

async function fetchLimited(url, { timeoutMs = 7000, maxBytes = 400_000, accept = 'text/*' } = {}) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      redirect: 'follow',
      signal: ctrl.signal,
      headers: { 'User-Agent': 'MarianStancikDev-FreeCheck/1.0 (+https://www.marianstancik.dev/services)', 'Accept': accept },
    });
    const reader = res.body?.getReader();
    if (!reader) return { status: res.status, text: '' };
    const chunks = [];
    let size = 0;
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
      size += value.length;
      if (size > maxBytes) { await reader.cancel(); break; }
    }
    const text = new TextDecoder('utf-8', { fatal: false }).decode(
      new Uint8Array(chunks.reduce((a, c) => [...a, ...c], []))
    );
    return { status: res.status, text };
  } catch {
    return { status: 0, text: '' };
  } finally {
    clearTimeout(timer);
  }
}

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const domain = normalizeDomain(url.searchParams.get('domain'));
  if (!domain) {
    return json({ error: 'invalid_domain' }, 400);
  }
  const base = 'https://' + domain;

  // 1) llms.txt
  const llms = await fetchLimited(base + '/llms.txt', { maxBytes: 100_000 });
  const llmsOk = llms.status === 200 && llms.text.trim().length > 24;

  // 2) robots.txt — how many known AI crawlers are addressed
  const robots = await fetchLimited(base + '/robots.txt', { maxBytes: 100_000 });
  const found = AI_CRAWLERS.filter((c) => robots.text.toLowerCase().includes(c.toLowerCase()));
  const crawlersOk = robots.status === 200 && found.length >= 2;

  // 3) JSON-LD structured data on the homepage
  const home = await fetchLimited(base + '/', { maxBytes: 400_000, accept: 'text/html' });
  const schemaOk =
    home.status === 200 &&
    /<script[^>]+type=["']application\/ld\+json["']/i.test(home.text);

  const checks = [
    { id: 'llms', pass: llmsOk, detail: llmsOk ? 'found' : 'missing' },
    { id: 'crawlers', pass: crawlersOk, detail: robots.status === 200 ? found.length + ' named' : 'no robots.txt' },
    { id: 'schema', pass: schemaOk, detail: schemaOk ? 'found' : 'missing' },
  ];
  const score = checks.filter((c) => c.pass).length;

  return json({ domain, checks, score, of: 3, ts: Date.now() });
}
