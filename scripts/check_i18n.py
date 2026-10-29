#!/usr/bin/env python3
"""
check_i18n.py — validation of the static multilingual site (no network).

  1. generated /{lang}/ pages are up to date (build_i18n.py --check)
  2. every generated page: <html lang>, self-canonical, hreflang cluster with x-default,
     every hreflang target exists and links back (reciprocity)
  3. every internal link in generated pages resolves to a file or a _redirects rule
  4. every sitemap <loc> and xhtml:link alternate resolves
  5. every blog post hreflang target exists

Exit code 1 on any ❌.
"""
import glob
import os
import re
import subprocess
import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.marianstancik.dev'
LANGS = ['en', 'sk', 'cs', 'de', 'pl']
errors, warnings = [], []


def redirect_sources():
    src = set()
    p = os.path.join(BASE, '_redirects')
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            line = line.strip()
            if line and not line.startswith('#'):
                src.add(line.split()[0])
    return src


REDIRECTS = redirect_sources()


def resolve(path):
    """Return True when a URL path is served by a static file or a redirect rule."""
    path = path.split('#')[0].split('?')[0]
    if path in REDIRECTS:
        return True
    for r in REDIRECTS:
        if r.endswith('*') and path.startswith(r[:-1]):
            return True
        if ':slug' in r and re.fullmatch(r.replace(':slug', '[^/]+'), path):
            return True
    rel = path.lstrip('/')
    cands = [rel, rel + '.html', os.path.join(rel, 'index.html')] if rel else ['index.html']
    if path.endswith('/'):
        cands = [os.path.join(rel, 'index.html')]
    return any(os.path.isfile(os.path.join(BASE, c)) for c in cands)


def url_to_path(u):
    return urlparse(u).path or '/'


def load(path):
    with open(path, encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')


def page_url(file_rel):
    rel = file_rel.replace(os.sep, '/')
    if rel.endswith('index.html'):
        rel = rel[:-len('index.html')]
    elif rel.endswith('.html'):
        rel = rel[:-5]
    return SITE + '/' + rel


def main():
    print('── 1. build_i18n --check')
    r = subprocess.run([sys.executable, os.path.join(BASE, 'scripts', 'build_i18n.py'), '--check'], cwd=BASE, capture_output=True, text=True)
    print('   ' + (r.stdout.strip() or r.stderr.strip()).replace('\n', '\n   '))
    if r.returncode != 0:
        errors.append('generated pages are stale')

    print('── 2. hreflang / canonical on generated pages')
    gen = sorted(f for l in LANGS for f in glob.glob(os.path.join(BASE, l, '**', '*.html'), recursive=True))
    clusters = {}
    for f in gen:
        rel = os.path.relpath(f, BASE)
        lang = rel.split(os.sep)[0]
        s = load(f)
        me = page_url(rel)
        if s.html.get('lang') != lang:
            errors.append(f'{rel}: <html lang="{s.html.get("lang")}"> != {lang}')
        robots = (s.find('meta', attrs={'name': 'robots'}) or {}).get('content', '')
        canon = s.find('link', rel='canonical')
        alts = {l['hreflang']: l['href'] for l in s.find_all('link', rel='alternate') if l.get('hreflang')}
        if 'noindex' in robots:
            if alts:
                errors.append(f'{rel}: noindex page must not carry hreflang')
            continue
        if not canon or canon['href'] != me:
            errors.append(f'{rel}: canonical {canon["href"] if canon else None} != {me}')
        if 'x-default' not in alts:
            errors.append(f'{rel}: missing hreflang x-default')
        if alts.get(lang) != me:
            errors.append(f'{rel}: hreflang="{lang}" does not point to itself')
        for hl, href in alts.items():
            if not resolve(url_to_path(href)):
                errors.append(f'{rel}: hreflang {hl} -> {href} does not exist')
        clusters[me] = alts
        if not s.find('a', class_='skip-link') and 'blog' not in rel:
            errors.append(f'{rel}: missing skip-link')
        if not s.find('link', attrs={'href': '/llms.txt', 'type': 'text/plain'}):
            errors.append(f'{rel}: missing llms.txt discovery link')
    for me, alts in clusters.items():
        for hl, href in alts.items():
            if hl == 'x-default' or href == me:
                continue
            back = clusters.get(href)
            if back is None or me not in back.values():
                errors.append(f'hreflang not reciprocal: {me} -> {href}')
    print(f'   checked {len(gen)} generated pages, {len(clusters)} indexable')

    print('── 3. internal links on generated pages')
    broken = set()
    for f in gen:
        s = load(f)
        for a in s.find_all('a', href=True):
            h = a['href']
            if h.startswith('/') and not h.startswith('//') and not resolve(h):
                broken.add((os.path.relpath(f, BASE), h))
    for rel, h in sorted(broken):
        errors.append(f'{rel}: broken internal link {h}')
    print(f'   {len(broken)} broken')

    print('── 4. sitemap.xml')
    sm = open(os.path.join(BASE, 'sitemap.xml'), encoding='utf-8').read()
    locs = re.findall(r'<loc>([^<]+)</loc>', sm)
    hrefs = set(re.findall(r'xhtml:link rel="alternate" hreflang="[^"]+" href="([^"]+)"', sm))
    for u in locs + sorted(hrefs):
        if not resolve(url_to_path(u)):
            errors.append(f'sitemap: {u} does not resolve')
        elif url_to_path(u) in REDIRECTS:
            errors.append(f'sitemap: {u} is a redirect, list the target instead')
    print(f'   {len(locs)} URLs, {len(hrefs)} alternates')

    print('── 5. blog post hreflang targets')
    posts = glob.glob(os.path.join(BASE, 'blog', 'posts', '*.html')) + glob.glob(os.path.join(BASE, 'blog', 'posts', '*', '*.html'))
    bad = 0
    for f in posts:
        txt = open(f, encoding='utf-8').read()
        for hl, href in re.findall(r'hreflang="([^"]+)" href="([^"]+)"', txt):
            if href.startswith(SITE) and not resolve(url_to_path(href)):
                bad += 1
                warnings.append(f'{os.path.relpath(f, BASE)}: hreflang {hl} -> missing {href}')
    print(f'   {len(posts)} posts, {bad} missing targets (warning, pre-existing posts)')

    for w in warnings[:20]:
        print('⚠️ ', w)
    for e in errors:
        print('❌', e)
    if errors:
        print(f'❌ i18n checks failed ({len(errors)} errors)')
        sys.exit(1)
    print('✅ i18n checks passed' + (f' ({len(warnings)} warnings)' if warnings else ''))


if __name__ == '__main__':
    main()
