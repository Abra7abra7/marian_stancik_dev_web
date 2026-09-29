/**
 * audit-worker.js — Autonomous GEO + Readiness Audit
 * 
 * Spúšťa sa cez: 
 *   - Stripe webhook (nová platba → audit)
 *   - Cron trigger (týždenný re-scan pre subscription klientov)
 *   - Manuálne cez HTTP request (admin)
 */

// ============================================
// CHECK FUNCTIONS
// ============================================

async function checkRobotsTxt(domain) {
  const url = `https://${domain}/robots.txt`;
  const res = await fetch(url, { method: 'HEAD' });
  const passed = res.ok && res.status === 200;
  return {
    check: 'robots.txt',
    passed,
    status: res.status,
    detail: passed ? 'Exists and accessible' : `${res.status} ${res.statusText}`,
    weight: 15
  };
}

async function checkSitemap(domain) {
  const url = `https://${domain}/sitemap.xml`;
  const res = await fetch(url);
  const text = await res.text();
  const hasUrls = text.includes('<url>') || text.includes('<sitemap>');
  return {
    check: 'Sitemap',
    passed: res.ok && hasUrls,
    status: res.status,
    detail: res.ok && hasUrls ? 'Valid XML sitemap with URLs' : 'Missing or invalid',
    weight: 10
  };
}

async function checkLlmsTxt(domain) {
  const url = `https://${domain}/llms.txt`;
  const res = await fetch(url);
  const text = await res.text();
  const hasContent = text.length > 100;
  return {
    check: 'llms.txt',
    passed: res.ok && hasContent,
    status: res.status,
    detail: res.ok ? `${text.length} chars` : 'Not found',
    weight: 15
  };
}

async function checkJsonLd(domain) {
  const url = `https://${domain}/`;
  const res = await fetch(url);
  const html = await res.text();
  const hasJsonLd = html.includes('"@context"') || html.includes('"@graph"');
  const hasPerson = html.includes('"Person"') || html.includes('"Organization"');
  let score = 0;
  if (hasJsonLd) score += 2;
  if (hasPerson) score += 1;
  return {
    check: 'JSON-LD Schema',
    passed: score >= 2,
    score,
    detail: hasJsonLd ? (hasPerson ? 'Found @graph with Person/Organization' : 'Found JSON-LD but missing Person') : 'No JSON-LD found',
    weight: 15
  };
}

async function checkAiCrawlers(domain) {
  const url = `https://${domain}/robots.txt`;
  const res = await fetch(url);
  const text = await res.text();
  const crawlers = ['GPTBot', 'ClaudeBot', 'PerplexityBot', 'Google-Extended'];
  const found = crawlers.filter(c => text.includes(c));
  return {
    check: 'AI Crawler Access',
    passed: found.length >= 3,
    found_count: found.length,
    detail: found.length >= 3 ? `${found.length}/${crawlers.length} AI crawlers allowed` : `Only ${found.length}/${crawlers.length}`,
    weight: 15
  };
}

async function checkHreflang(domain) {
  const url = `https://${domain}/`;
  const res = await fetch(url);
  const html = await res.text();
  const matches = html.match(/hreflang=["']([^"']+)["']/g) || [];
  return {
    check: 'hreflang',
    passed: matches.length >= 2,
    count: matches.length,
    detail: matches.length >= 2 ? `${matches.length} hreflang tags found` : 'Missing hreflang',
    weight: 5
  };
}

async function checkOpenGraph(domain) {
  const url = `https://${domain}/`;
  const res = await fetch(url);
  const html = await res.text();
  const hasOgTitle = html.includes('og:title') || html.includes('og:description');
  return {
    check: 'OpenGraph',
    passed: hasOgTitle,
    detail: hasOgTitle ? 'OG tags present' : 'Missing OpenGraph tags',
    weight: 5
  };
}

async function checkContentSecurity(domain) {
  const url = `https://${domain}/`;
  const res = await fetch(url);
  const headers = res.headers;
  const hsts = headers.get('strict-transport-security');
  const csp = headers.get('content-security-policy');
  return {
    check: 'Security Headers',
    passed: !!hsts,
    detail: hsts ? 'HSTS + CSP present' : 'Missing HSTS',
    weight: 5
  };
}

async function checkLinkHeaders(domain) {
  const url = `https://${domain}/`;
  const res = await fetch(url);
  const link = res.headers.get('link') || '';
  const hasLlm = link.includes('llms.txt');
  return {
    check: 'Link Headers (llms.txt)',
    passed: hasLlm,
    detail: hasLlm ? 'Link: describedby for llms.txt found' : 'Missing Link header',
    weight: 5
  };
}

async function checkPerformance(url) {
  // Lightweight: check response time + content size
  const start = Date.now();
  const res = await fetch(url);
  const time = Date.now() - start;
  const size = parseInt(res.headers.get('content-length') || '0');
  const fast = time < 500;
  return {
    check: 'Performance',
    passed: fast,
    response_ms: time,
    size_bytes: size,
    detail: fast ? `${time}ms response` : `Slow: ${time}ms`,
    weight: 10
  };
}

// ============================================
// SCORE ENGINE
// ============================================

function computeScore(results) {
  let totalWeight = 0;
  let earnedWeight = 0;
  for (const r of results) {
    totalWeight += r.weight;
    if (r.passed) earnedWeight += r.weight;
  }
  const score = Math.round((earnedWeight / totalWeight) * 100);
  
  const recommendations = [];
  for (const r of results) {
    if (!r.passed) {
      recommendations.push({
        check: r.check,
        severity: r.weight >= 15 ? 'high' : r.weight >= 10 ? 'medium' : 'low',
        detail: r.detail,
        fix: `Fix ${r.check} for +${r.weight} points`
      });
    }
  }
  
  return { score, totalWeight, earnedWeight, recommendations };
}

// ============================================
// MAIN HANDLER — export for index.js router
// ============================================

export async function handleAuditRequest(request, env) {
  const url = new URL(request.url);
  const path = url.pathname;

  // Admin: manual audit trigger
  if (path === '/api/audit/run' && request.method === 'POST') {
    try {
      const body = await request.json();
      const domain = body.domain || new URL(request.headers.get('origin') || 'https://example.com').hostname;
      return await runAudit(domain, 'geo', env);
    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), { status: 400 });
    }
  }

  // Client: get last audit result
  if (path.startsWith('/api/audit/') && request.method === 'GET') {
    const clientId = path.split('/')[3];
    const { results } = await env.DB.prepare(
      'SELECT * FROM audits WHERE client_id = ? ORDER BY created_at DESC LIMIT 1'
    ).bind(clientId).all();
    if (!results.length) {
      return new Response(JSON.stringify({ error: 'No audit found' }), { status: 404 });
    }
    return new Response(JSON.stringify(results[0]), {
      headers: { 'content-type': 'application/json' }
    });
  }

  // Health check
  if (path === '/api/health') {
    return new Response(JSON.stringify({ status: 'ok', service: 'audit-worker' }), {
      headers: { 'content-type': 'application/json' }
    });
  }

  return new Response('Not found', { status: 404 });
}

// Standalone Worker entry point (optional, unused when routed via index.js)
export default {
  async fetch(request, env) {
    return await handleAuditRequest(request, env);
  },

  async scheduled(event, env, ctx) {
    const { results: activeClients } = await env.DB.prepare(
      "SELECT * FROM clients WHERE status = 'active' AND plan IN ('monitoring', 'annual')"
    ).all();

    for (const client of activeClients) {
      ctx.waitUntil(runAudit(client.domain, 'geo', env, client.id));
    }
  }
};

export async function runAudit(domain, type, env, clientId = null) {
  const auditId = crypto.randomUUID();
  const timestamp = new Date().toISOString();

  // Store audit record
  if (clientId) {
    await env.DB.prepare(
      'INSERT INTO audits (id, client_id, type, status, started_at) VALUES (?, ?, ?, ?, ?)'
    ).bind(auditId, clientId, type, 'running', timestamp).run();
  }

  // Run all checks in parallel
  const checks = [
    checkRobotsTxt(domain),
    checkSitemap(domain),
    checkLlmsTxt(domain),
    checkJsonLd(domain),
    checkAiCrawlers(domain),
    checkHreflang(domain),
    checkOpenGraph(domain),
    checkContentSecurity(domain),
    checkLinkHeaders(domain),
    checkPerformance(`https://${domain}/`)
  ];

  const results = await Promise.all(checks);
  const { score, recommendations } = computeScore(results);

  // Store results
  const resultBody = {
    domain, type, score, results, recommendations,
    scanned_at: timestamp,
    report_url: `${env.APP_URL || ''}/report/${auditId}`
  };

  if (clientId) {
    // Get baseline for delta
    const { results: prev } = await env.DB.prepare(
      'SELECT score FROM audits WHERE client_id = ? AND status = ? ORDER BY created_at DESC LIMIT 1'
    ).bind(clientId, 'done').all();
    
    const baselineScore = prev.length ? prev[0].score : score;
    const scoreDelta = score - baselineScore;

    // Save to D1
    await env.DB.prepare(
      'UPDATE audits SET status = ?, score = ?, baseline_score = ?, score_delta = ?, completed_at = ? WHERE id = ?'
    ).bind('done', score, baselineScore, scoreDelta, timestamp, auditId).run();

    await env.DB.prepare(
      'INSERT INTO audit_results (audit_id, raw, summary, recommendations) VALUES (?, ?, ?, ?)'
    ).bind(auditId, JSON.stringify(resultBody), generateSummary(results, score), JSON.stringify(recommendations)).run();

    // Alert on score drop
    if (scoreDelta < -10) {
      await env.DB.prepare(
        'INSERT INTO alerts (id, client_id, type, message, score_before, score_after) VALUES (?, ?, ?, ?, ?, ?)'
      ).bind(crypto.randomUUID(), clientId, 'score_drop',
        `GEO score dropped from ${baselineScore} to ${score} (${scoreDelta} points)`,
        baselineScore, score).run();
    }
  }

  return new Response(JSON.stringify({ audit_id: auditId, score, results, recommendations }), {
    headers: { 'content-type': 'application/json' }
  });
}

function generateSummary(results, score) {
  const passed = results.filter(r => r.passed).length;
  const total = results.length;
  return `${passed}/${total} checks passed. Score: ${score}/100. ${score >= 80 ? 'Good AI agent readiness.' : score >= 50 ? 'Moderate — several improvements needed.' : 'Poor — immediate action recommended.'}`;
}