#!/usr/bin/env python3
"""Smoke test for the AI redesign branch (feature/ai-redesign).

Checks:
 1. All key pages exist and render 200 on a local static server.
 2. Deleted pages are really gone.
 3. Every _redirects target resolves to an existing static file.
 4. No internal href in any generated page points to a deleted path that is NOT covered by _redirects.
 5. sitemap.xml contains the new structure and no deleted URLs; every <loc> exists as a file.
 6. llms.txt core pages exist.
 7. Blog bylines link to /how-it-works (not /about).
 8. JSON-LD on Home has no Product/Offer; no inline event handlers (CSP) on new pages.
 9. Prompt Library has 15 prompt cards with copy buttons.
"""
import http.server
import json
import os
import re
import socketserver
import subprocess
import sys
import threading
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
os.chdir(BASE)
LANGS = ['en', 'sk', 'cs', 'de', 'pl']
FAILS = []
OKS = []

def ok(msg): OKS.append(msg); print(f'  ✅ {msg}')
def fail(msg): FAILS.append(msg); print(f'  ❌ {msg}')

def path_for(url):
    """Map a URL path to the static file that Cloudflare Pages would serve."""
    p = url.split('?')[0].split('#')[0]
    if p in ('/', ''):
        p = '/index.html'
    p = p.lstrip('/')
    if p.endswith('/'):
        p += 'index.html'
    if not os.path.exists(p) and not p.endswith('.html'):
        if os.path.exists(p + '.html'):
            p += '.html'
        else:
            p2 = os.path.join(p, 'index.html')
            if os.path.exists(p2):
                p = p2
    return p

# ---- redirect targets -------------------------------------------------------
print('1) _redirects targets')
redirect_rules = []
for line in (BASE / '_redirects').read_text().splitlines():
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    parts = line.split()
    if len(parts) >= 2:
        if ':' in parts[0] or '*' in parts[0]:
            continue  # Cloudflare splat/placeholder rule — cannot be verified statically
        redirect_rules.append((parts[0], parts[1]))
bad = []
for src, dst in redirect_rules:
    dst_clean = dst.split('#')[0]
    if dst_clean in ('/', '') :
        f = 'index.html'
    else:
        f = path_for(dst_clean)
    if not os.path.exists(f):
        bad.append(f'{src} -> {dst} (missing {f})')
if bad:
    for b in bad: fail('redirect target missing: ' + b)
else:
    ok(f'all {len(redirect_rules)} redirect targets resolve to existing files')

# ---- HTTP checks ------------------------------------------------------------
class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

    def translate_path(self, path):
        # mimic Cloudflare Pages: extensionless URLs -> .html or dir/index.html
        clean = path.split('?')[0].split('#')[0]
        if clean.endswith('/'):
            clean += 'index.html'
        elif not os.path.splitext(clean)[1] and os.path.exists(super().translate_path(clean + '.html')):
            clean += '.html'
        return super().translate_path(clean)

with socketserver.TCPServer(('127.0.0.1', 0), Handler) as httpd:
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()

    def get(url):
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}{url}', timeout=10) as r:
                return r.status, r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            return e.code, ''

    print('2) key pages 200')
    key_pages = ['/en/', '/sk/', '/cs/', '/de/', '/pl/']
    for l in LANGS:
        key_pages += [f'/{l}/tools/', f'/{l}/tools/prompt-library', f'/{l}/tools/starter-kit',
                      f'/{l}/tools/mission-planner', f'/{l}/how-it-works', f'/{l}/contact', f'/{l}/blog/']
    key_pages += ['/privacy', '/terms', '/disclaimer', '/impressum', '/cookie',
                  '/llms.txt', '/sitemap.xml', '/robots.txt', '/rss.xml']
    for u in key_pages:
        code, _ = get(u)
        (ok if code == 200 else fail)(f'{u} -> {code}')

    print('3) deleted pages 404')
    for u in ['/about.html', '/services.html', '/drones.html', '/skills.html',
              '/expertise.html', '/audit-report.html', '/en/about', '/sk/services']:
        code, _ = get(u)
        (ok if code == 404 else fail)(f'{u} -> {code} (expected 404 pre-redirect)')

    # ---- internal hrefs ----
    print('4) internal hrefs')
    deleted_paths = {'/about', '/services', '/services-sk', '/drones', '/skills', '/expertise', '/audit-report'}
    covered = {src for src, _ in redirect_rules} | {src.rstrip('/') for src, _ in redirect_rules} | \
              {src + '.html' for src, _ in redirect_rules} | {src.rstrip('/') + '.html' for src, _ in redirect_rules}
    gen_files = []
    for l in LANGS:
        gen_files += [f'{l}/index.html', f'{l}/tools/index.html', f'{l}/tools/prompt-library.html',
                      f'{l}/tools/starter-kit.html', f'{l}/tools/mission-planner.html',
                      f'{l}/how-it-works.html', f'{l}/contact.html', f'{l}/blog/index.html']
    gen_files += ['index.html', 'contact.html', 'tools/index.html', 'tools/prompt-library.html',
                  'tools/starter-kit.html', 'tools/starter-kit-sk.html', 'tools/mission-planner.html', 'how-it-works.html']
    href_re = re.compile(r'href="(/[^"]*)"')
    dead = []
    for f in gen_files:
        if not os.path.exists(f):
            continue
        html = open(f, encoding='utf-8').read()
        for m in href_re.finditer(html):
            href = m.group(1).split('#')[0].split('?')[0]
            if not href or href.startswith('//'):
                continue
            if href in deleted_paths or href.rstrip('/') in deleted_paths:
                # covered by _redirects? then acceptable only if intentionally kept (none kept)
                dead.append(f'{f}: {href}')
                continue
            target = path_for(href)
            if href.startswith('/blog/posts') and not os.path.exists(target):
                dead.append(f'{f}: {href} (missing file)')
            elif not href.startswith('/blog/posts') and not os.path.exists(target) and not href.startswith('/api'):
                dead.append(f'{f}: {href} (missing file)')
    if dead:
        for d_ in sorted(set(dead))[:20]: fail('dead href: ' + d_)
    else:
        ok('no dead internal hrefs in templates + generated pages')

    # blog posts byline
    print('5) blog bylines')
    posts = list((BASE / 'blog' / 'posts').rglob('*.html'))
    bad_byline = [str(p.relative_to(BASE)) for p in posts
                  if 'href="/about"' in p.read_text(encoding='utf-8', errors='replace')]
    (ok if not bad_byline else fail)(f'{len(posts)} post files checked; /about bylines remaining: {len(bad_byline)}')

    # sitemap consistency
    print('6) sitemap')
    sm = open('sitemap.xml', encoding='utf-8').read()
    locs = re.findall(r'<loc>(.*?)</loc>', sm)
    deleted_in_sm = [l for l in locs if any(x in l for x in ['/about', '/services', '/drones', '/skills', '/expertise', '/audit-report'])]
    new_in_sm = [l for l in locs if '/tools/' in l or '/how-it-works' in l]
    (ok if not deleted_in_sm else fail)(f'deleted URLs in sitemap: {len(deleted_in_sm)}')
    (ok if new_in_sm else fail)(f'new URLs in sitemap: {len(new_in_sm)}')
    missing_sm = []
    for l in locs:
        p = l.replace('https://www.marianstancik.dev', '')
        f = path_for(p)
        if not os.path.exists(f) and '/blog/posts' not in p:
            missing_sm.append(p)
    (ok if not missing_sm else fail)(f'sitemap locs missing as files: {missing_sm[:5]}')

    # llms.txt
    print('7) llms.txt')
    ll = open('llms.txt', encoding='utf-8').read()
    ll_bad = [x for x in ['/about', '/services', '/drones'] if f'marianstancik.dev{x}' in ll]
    ll_new = all(x in ll for x in ['/tools/', '/tools/prompt-library', '/tools/starter-kit', '/how-it-works'])
    (ok if not ll_bad else fail)(f'llms.txt references deleted pages: {ll_bad}')
    (ok if ll_new else fail)('llms.txt lists new core pages')

    # JSON-LD + CSP on home
    print('8) JSON-LD / CSP')
    idx = open('en/index.html', encoding='utf-8').read()
    (ok if '"Product"' not in idx and '"Offer"' not in idx else fail)('no Product/Offer in Home JSON-LD')
    new_pages = ['index.html', 'tools/index.html', 'tools/prompt-library.html',
                 'tools/starter-kit.html', 'tools/mission-planner.html', 'how-it-works.html']
    inline = []
    for f in new_pages:
        html = open(f, encoding='utf-8').read()
        if re.search(r'\son(click|change|submit|load)\s*=', html, re.I):
            inline.append(f)
    (ok if not inline else fail)(f'no inline event handlers on new pages: {inline}')

    # prompt library cards
    print('9) prompt library')
    pl = open('tools/prompt-library.html', encoding='utf-8').read()
    n_cards = len(re.findall(r'class="prompt-card fade-in"', pl))
    n_copy = pl.count('copy-btn')
    (ok if n_cards == 15 else fail)(f'prompt cards: {n_cards}/15')
    (ok if n_copy >= 15 else fail)(f'copy buttons: {n_copy}')
    (ok if '/js/tools.min.js' in pl or '/js/tools.js' in pl else fail)('tools.js referenced')

    httpd.shutdown()

print()
if FAILS:
    print(f'❌ SMOKE TEST FAILED: {len(FAILS)} problem(s)')
    sys.exit(1)
print(f'✅ SMOKE TEST PASSED ({len(OKS)} checks)')
