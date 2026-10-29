#!/usr/bin/env python3
"""
Hermes Agent — Multilingual Blog Publisher (EN · SK · CS · DE · PL) with PR-based review

What it does
  1. Writes blog/posts/{slug}.html (EN) and blog/posts/{lang}/{slug}.html for every language in --langs.
     Missing translations are produced through OpenRouter (env OPENROUTER_API_KEY) with a QA check
     (same headings, links, code blocks). Placeholder articles are NEVER published any more.
  2. Updates blog/posts.json, sitemap.xml, llms.txt (scripts/sync_site.py) and the static
     per-language pages incl. blog indexes (scripts/build_i18n.py).
  3. With --pr (or the legacy --push flag) it creates a branch hermes/blog-<slug>, commits,
     pushes the BRANCH and opens a Pull Request for human review. Nothing is pushed to main.
     After the PR is merged and deployed, ping search engines with:  --ping-slug <slug>

Usage (backward compatible with the old EN+SK CLI):
    python3 scripts/publish_post.py \
        --title "Edge AI on Raspberry Pi 5 with ArduPilot" \
        --excerpt "Deploying neural computer vision models on custom UAVs." \
        --title-sk "Edge AI na Raspberry Pi 5 s ArduPilotom" --excerpt-sk "..." \
        --content-file content_en.html --content-file-sk content_sk.html \
        --tags "Drones, Edge AI" --read-time "5 min read" \
        [--langs sk,en,cs,de,pl] [--source-lang en] [--allow-missing] [--pr] [--dry-run]

Environment
    OPENROUTER_API_KEY            required when a language in --langs has no provided text
    HERMES_TRANSLATE_MODEL        OpenRouter model id (default: see DEFAULT_TRANSLATE_MODEL)
    GH_TOKEN / GITHUB_TOKEN       used by `gh pr create` (or by the REST fallback when gh is missing)
"""

import argparse
import datetime
import html as htmlmod
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

SITE = 'https://www.marianstancik.dev'
POSTS_DIR = os.path.join(BASE_DIR, 'blog', 'posts')
POSTS_JSON = os.path.join(BASE_DIR, 'blog', 'posts.json')
REPO_SLUG = 'Abra7abra7/marian_stancik_dev_web'
ALL_LANGS = ['en', 'sk', 'cs', 'de', 'pl']
DEFAULT_LANGS = 'sk,en,cs,de,pl'
DEFAULT_TRANSLATE_MODEL = 'google/gemini-3.5-flash'
SUFFIX = {'en': '', 'sk': 'Sk', 'cs': 'Cs', 'de': 'De', 'pl': 'Pl'}
LANG_NAME = {'en': 'English', 'sk': 'Slovak', 'cs': 'Czech', 'de': 'German', 'pl': 'Polish'}

LANG_META = {
    'en': {'og': 'en_US', 'home': 'Home', 'home_aria': 'Marian Stancik home', 'nav_aria': 'Blog navigation', 'by': 'By Marian Stancik',
           'read': '{n} min read', 'fallback_read': '4 min read'},
    'sk': {'og': 'sk_SK', 'home': 'Domov', 'home_aria': 'Marian Stancik domov', 'nav_aria': 'Navigácia blogu', 'by': 'Marian Stancik',
           'read': '{n} min čítania', 'fallback_read': '4 min čítania'},
    'cs': {'og': 'cs_CZ', 'home': 'Domů', 'home_aria': 'Marian Stancik domů', 'nav_aria': 'Navigace blogu', 'by': 'Marian Stancik',
           'read': '{n} min čtení', 'fallback_read': '4 min čtení'},
    'de': {'og': 'de_DE', 'home': 'Startseite', 'home_aria': 'Marian Stancik Startseite', 'nav_aria': 'Blog-Navigation', 'by': 'Von Marian Stancik',
           'read': '{n} Min. Lesezeit', 'fallback_read': '4 Min. Lesezeit'},
    'pl': {'og': 'pl_PL', 'home': 'Strona główna', 'home_aria': 'Marian Stancik strona główna', 'nav_aria': 'Nawigacja bloga', 'by': 'Marian Stancik',
           'read': '{n} min czytania', 'fallback_read': '4 min czytania'},
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Marian Stancik</title>
<meta name="description" content="{excerpt}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="{url}">
{hreflang_links}
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM Knowledge Graph">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="theme-color" content="#08080F">

<!-- Open Graph -->
<meta property="og:title" content="{title} — Marian Stancik">
<meta property="og:description" content="{excerpt}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://www.marianstancik.dev/profile.webp">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="800">
<meta property="og:image:alt" content="{title}">
<meta property="og:locale" content="{og_locale}">
{og_locale_alts}
<meta property="og:site_name" content="Marian Stancik">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@marian_s_ai">
<meta name="twitter:creator" content="@marian_s_ai">
<meta name="twitter:image" content="https://www.marianstancik.dev/profile.webp">

<meta name="ai-generated-content" content="true">

<!-- JSON-LD Structured Data with BreadcrumbList -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BlogPosting",
      "headline": {title_json},
      "description": {excerpt_json},
      "datePublished": "{date}",
      "dateModified": "{date}",
      "author": {{
        "@type": "Person",
        "name": "Marian Stancik",
        "url": "https://www.marianstancik.dev"
      }},
      "publisher": {{
        "@type": "Person",
        "name": "Marian Stancik"
      }},
      "mainEntityOfPage": "{url}",
      "keywords": {tags_json},
      "isBasedOn": "https://schema.org/AIGeneratedContent",
      "creativeWorkStatus": "AIGenerated"
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "{home_label}",
          "item": "https://www.marianstancik.dev/{lang}/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "https://www.marianstancik.dev/{lang}/blog/"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": {title_json},
          "item": "{url}"
        }}
      ]
    }}
  ]
}}
</script>

<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Inter',-apple-system,BlinkMacSystemFont,system-ui,sans-serif;background:#08080F;color:#E8E8F0;line-height:1.8;-webkit-font-smoothing:antialiased}}
.container{{max-width:740px;margin:0 auto;padding:0 24px}}
nav{{padding:16px 24px;border-bottom:1px solid rgba(255,255,255,0.04);background:rgba(8,8,15,0.85);backdrop-filter:blur(12px);position:sticky;top:0;z-index:100}}
.nav-inner{{max-width:740px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}}
.nav-inner a{{color:#8888A0;text-decoration:none;font-size:0.85rem;transition:color 0.3s}}
.nav-inner a:hover{{color:#CD7F32}}
article{{padding:48px 0 80px}}
.post-meta{{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:32px;font-size:0.78rem;color:#9090A8}}
.post-meta .tag{{background:rgba(205,127,50,0.08);color:#E8B86D;padding:3px 10px;border-radius:100px;font-size:0.65rem;border:1px solid rgba(205,127,50,0.15)}}
h1{{font-size:clamp(1.6rem,4vw,2.4rem);font-weight:700;color:#F0F0F5;line-height:1.25;letter-spacing:-0.02em;margin-bottom:8px}}
h2{{font-size:1.3rem;font-weight:600;color:#F0F0F5;margin:36px 0 12px;line-height:1.35}}
h3{{font-size:1.05rem;font-weight:600;color:#D0D0E0;margin:24px 0 8px}}
p{{color:#B0B0C8;margin-bottom:16px;font-size:0.95rem}}
a{{color:#E8B86D;transition:color 0.3s}}
a:hover{{color:#CD7F32}}
ul,ol{{padding-left:20px;margin-bottom:16px;color:#B0B0C8;font-size:0.95rem}}
li{{margin-bottom:6px}}
code{{background:rgba(255,255,255,0.04);padding:2px 6px;border-radius:4px;font-size:0.85rem;color:#E8B86D;font-family:'Fira Code','Cascadia Code','JetBrains Mono',monospace}}
pre{{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:20px;overflow-x:auto;margin-bottom:20px;font-size:0.82rem;line-height:1.5}}
pre code{{background:none;padding:0;color:#C8C8D8}}
.callout{{background:rgba(205,127,50,0.06);border-left:3px solid #CD7F32;border-radius:0 8px 8px 0;padding:16px 20px;margin:24px 0;color:#E8E8F0}}
footer{{padding:36px 24px;text-align:center;color:#9090A8;font-size:0.75rem;border-top:1px solid rgba(255,255,255,0.04)}}
footer a{{color:#8888A0;text-decoration:none}}
footer a:hover{{color:#CD7F32}}
@media(max-width:600px){{article{{padding:32px 0 60px}}}}
</style>
<script defer src="https://api.marianstancik.dev/script.js" data-website-id="ec1c0df8-e51f-4236-9ad0-e3992f0b1637"></script>
<script defer src="/js/posthog.js"></script>
</head>
<body>

<nav aria-label="{nav_aria}">
  <div class="nav-inner">
    <a href="/{lang}/" aria-label="{home_aria}"><span style="font-size:1.1rem">←</span> {home_label}</a>
    <div style="display:flex;align-items:center;gap:16px;">
      <a href="/{lang}/blog/">Blog</a>
      <div style="display:flex;gap:4px;background:rgba(255,255,255,0.06);padding:2px 4px;border-radius:100px;font-size:0.72rem;font-weight:600;">
{switcher}
      </div>
    </div>
  </div>
</nav>

<div class="container">
<article>
<div class="post-meta">
  <span>{display_date}</span>
  <span class="tag">{primary_tag}</span>
  <span>{read_time}</span>
  <span>{by_label}</span>
</div>

<h1>{title}</h1>

<div class="post-content">
{content}
</div>
</article>
</div>

<footer>
  <p>© {year} <a href="/{lang}/">Marian Stancik</a> — <a href="/{lang}/">www.marianstancik.dev</a></p>
</footer>
</body>
</html>
"""

# ----------------------------------------------------------------------------- helpers
def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    return re.sub(r'[\s-]+', '-', text).strip('-')


def post_rel(lang, slug):
    return f'blog/posts/{slug}' if lang == 'en' else f'blog/posts/{lang}/{slug}'


def post_path(lang, slug):
    return os.path.join(BASE_DIR, post_rel(lang, slug) + '.html')


def display_date(lang, dt):
    from build_i18n import fmt_date
    if lang == 'en':
        return dt.strftime('%B %d, %Y')
    return fmt_date(lang, dt.strftime('%Y-%m-%d'))


def read_time_for(lang, args_value, en_value):
    if args_value:
        return args_value
    n = re.search(r'\d+', en_value or '')
    return LANG_META[lang]['read'].format(n=n.group(0) if n else '4')


class TranslationError(RuntimeError):
    pass


def _openrouter_chat(system, user, model):
    key = os.environ.get('OPENROUTER_API_KEY')
    if not key:
        raise TranslationError('OPENROUTER_API_KEY is not set')
    payload = json.dumps({
        'model': model,
        'temperature': 0.2,
        'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
    }).encode('utf-8')
    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions', data=payload,
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json',
                 'HTTP-Referer': SITE, 'X-Title': 'Hermes blog translator'})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read().decode('utf-8'))
    try:
        return data['choices'][0]['message']['content'].strip()
    except Exception:
        raise TranslationError(f'Unexpected OpenRouter response: {str(data)[:300]}')


def _chunks(content, limit=12000):
    """Split HTML on block boundaries so each request stays small."""
    parts = re.split(r'(?<=</p>)|(?<=</h2>)|(?<=</h3>)|(?<=</ul>)|(?<=</ol>)|(?<=</pre>)|(?<=</div>)|(?<=</table>)', content)
    out, cur = [], ''
    for p in parts:
        if len(cur) + len(p) > limit and cur:
            out.append(cur)
            cur = ''
        cur += p
    if cur:
        out.append(cur)
    return out


def translate(text, src, tgt, kind, model):
    """kind: 'title' | 'excerpt' | 'html'"""
    system = (f'You are a professional technical translator. Translate the user text from {LANG_NAME[src]} to {LANG_NAME[tgt]}. '
              'Keep meaning, tone and technical terms (product names, model names, code, numbers, dates, URLs) exactly. '
              'Preserve every HTML tag and attribute unchanged; translate only human-readable text. '
              'Never add commentary, notes or Markdown fences. Output ONLY the translation.')
    if kind == 'title':
        system += ' The text is an article title: return a single line.'
    if kind != 'html':
        out = _openrouter_chat(system, text, model).strip()
        if len(out) > 1 and out[0] == out[-1] and out[0] in '"„“':
            out = out[1:-1].strip()
        return out
    return ''.join(_openrouter_chat(system, chunk, model) for chunk in _chunks(text))


def qa_html(src_html, out_html):
    """Structural QA: same number of headings/links/code blocks and identical link targets."""
    problems = []
    for tag in ['h2', 'h3', 'pre', 'code', 'li', 'table']:
        a = len(re.findall(rf'<{tag}[\s>]', src_html))
        b = len(re.findall(rf'<{tag}[\s>]', out_html))
        if a != b:
            problems.append(f'<{tag}> count {a} -> {b}')
    hrefs_a = sorted(re.findall(r'href="([^"]+)"', src_html))
    hrefs_b = sorted(re.findall(r'href="([^"]+)"', out_html))
    if hrefs_a != hrefs_b:
        problems.append('link targets differ')
    if out_html.lstrip().startswith('```'):
        problems.append('markdown fence in output')
    return problems


def read_content(file_arg, html_arg):
    if file_arg:
        if not os.path.exists(file_arg):
            raise SystemExit(f'Content file not found: {file_arg}')
        with open(file_arg, 'r', encoding='utf-8') as f:
            return f.read()
    return html_arg or ''


def build_alternates(slug, langs):
    order = [l for l in ALL_LANGS if l in langs]
    links = [f'<link rel="alternate" hreflang="{l}" href="{SITE}/{post_rel(l, slug)}">' for l in order]
    xdef = 'en' if 'en' in order else order[0]
    links.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/{post_rel(xdef, slug)}">')
    return '\n'.join(links)


def build_switcher(slug, langs, active):
    out = []
    for l in [l for l in ALL_LANGS if l in langs]:
        style = ('padding:2px 8px;border-radius:100px;color:#CD7F32;background:rgba(205,127,50,0.15);text-decoration:none;'
                 if l == active else 'padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;')
        out.append(f'        <a href="/{post_rel(l, slug)}" hreflang="{l}" lang="{l}" style="{style}">{l.upper()}</a>')
    return '\n'.join(out)


def render_post(lang, slug, langs, title, excerpt, content, date_iso, disp_date, read_time, tags, year):
    meta = LANG_META[lang]
    url = f'{SITE}/{post_rel(lang, slug)}'
    alts = '\n'.join(f'<meta property="og:locale:alternate" content="{LANG_META[l]["og"]}">'
                     for l in ALL_LANGS if l in langs and l != lang)
    return HTML_TEMPLATE.format(
        lang=lang, url=url, slug=slug,
        title=htmlmod.escape(title, quote=True), excerpt=htmlmod.escape(excerpt, quote=True),
        title_json=json.dumps(title, ensure_ascii=False), excerpt_json=json.dumps(excerpt, ensure_ascii=False),
        hreflang_links=build_alternates(slug, langs), og_locale=meta['og'], og_locale_alts=alts,
        home_label=meta['home'], home_aria=meta['home_aria'], nav_aria=meta['nav_aria'], by_label=meta['by'],
        switcher=build_switcher(slug, langs, lang), date=date_iso, display_date=disp_date, read_time=read_time,
        primary_tag=htmlmod.escape(tags[0] if tags else 'AI & Technology'), tags_json=json.dumps(tags, ensure_ascii=False),
        content=content, year=year)


def ping_search_engines(urls):
    """IndexNow ping (Bing, Seznam, Yandex…). Run only after the PR is merged and deployed."""
    print('[*] Triggering IndexNow ping...')
    try:
        payload = json.dumps({
            'host': 'www.marianstancik.dev',
            'key': '47a47bfd9de94eb79d5cbf3f33a254ba',
            'keyLocation': 'https://www.marianstancik.dev/47a47bfd9de94eb79d5cbf3f33a254ba.txt',
            'urlList': urls,
        }).encode('utf-8')
        req = urllib.request.Request('https://api.indexnow.org/indexnow', data=payload,
                                     headers={'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'MarianStancik-Publisher/2.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f'    [+] IndexNow OK ({response.status})')
    except Exception as e:
        print(f'    [!] IndexNow notice: {e}')


def git(*cmd, check=True, capture=False):
    r = subprocess.run(['git', *cmd], cwd=BASE_DIR, check=check, text=True,
                       stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None)
    return r.stdout.strip() if capture else r


def prepare_branch(branch):
    if git('status', '--porcelain', capture=True):
        raise SystemExit('[!] Working tree is not clean — commit/stash local changes before publishing with --pr.')
    git('fetch', 'origin', 'main')
    git('checkout', '-B', branch, 'origin/main')


def open_pull_request(branch, title, body):
    git('push', '-u', 'origin', branch)
    if shutil.which('gh'):
        r = subprocess.run(['gh', 'pr', 'create', '--repo', REPO_SLUG, '--base', 'main', '--head', branch,
                            '--title', title, '--body', body], cwd=BASE_DIR, text=True, capture_output=True)
        if r.returncode == 0:
            return r.stdout.strip()
        print(f'[!] gh pr create failed: {r.stderr.strip()}')
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        raise SystemExit(f'[!] Branch {branch} pushed, but no gh CLI / GH_TOKEN to open the PR. Open it manually.')
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO_SLUG}/pulls',
        data=json.dumps({'title': title, 'head': branch, 'base': 'main', 'body': body}).encode('utf-8'),
        headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json', 'User-Agent': 'hermes-publisher'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8')).get('html_url', '')


# ----------------------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser(description='Hermes Agent multilingual blog publisher (EN, SK, CS, DE, PL) — opens a PR for review')
    p.add_argument('--langs', default=DEFAULT_LANGS, help=f'comma-separated languages to publish (default: {DEFAULT_LANGS})')
    p.add_argument('--source-lang', default='en', choices=ALL_LANGS, help='language of the original text (default: en)')
    for l in ALL_LANGS:
        sfx = '' if l == 'en' else f'-{l}'
        name = LANG_NAME[l]
        p.add_argument(f'--title{sfx}', help=f'Article title ({name})')
        p.add_argument(f'--excerpt{sfx}', help=f'Article excerpt ({name})')
        p.add_argument(f'--read-time{sfx}', help=f'Read time ({name}), e.g. "{LANG_META[l]["fallback_read"]}"')
        p.add_argument(f'--content-file{sfx}', help=f'Path to {name} HTML content snippet')
        p.add_argument(f'--content-html{sfx}', help=f'Raw {name} HTML content string')
    p.add_argument('--tags', default='AI Agents, Tech', help='Comma-separated tags')
    p.add_argument('--date', help='Publish date YYYY-MM-DD (defaults to today)')
    p.add_argument('--translate-model', default=os.environ.get('HERMES_TRANSLATE_MODEL', DEFAULT_TRANSLATE_MODEL),
                   help='OpenRouter model used for missing translations')
    p.add_argument('--no-translate', action='store_true', help='never call OpenRouter; missing languages are an error (or skipped with --allow-missing)')
    p.add_argument('--allow-missing', action='store_true', help='skip languages that cannot be produced instead of failing')
    p.add_argument('--pr', action='store_true', help='commit to a new branch and open a Pull Request (never pushes to main)')
    p.add_argument('--push', action='store_true', help='DEPRECATED alias of --pr (kept for backward compatibility; no longer pushes to main)')
    p.add_argument('--ping-slug', help='only send the IndexNow ping for an already deployed post slug, then exit')
    p.add_argument('--dry-run', action='store_true', help='simulate the run without writing files or calling git')
    args = p.parse_args()
    a = vars(args)

    if args.ping_slug:
        slug = args.ping_slug
        langs = [l for l in ALL_LANGS if os.path.exists(post_path(l, slug))]
        ping_search_engines([f'{SITE}/{post_rel(l, slug)}' for l in langs])
        return

    def arg(field, lang):
        key = field.replace('-', '_') + ('' if lang == 'en' else f'_{lang}')
        return a.get(key)

    langs = [l.strip() for l in args.langs.split(',') if l.strip()]
    bad = [l for l in langs if l not in ALL_LANGS]
    if bad:
        raise SystemExit(f'Unsupported languages: {bad}. Supported: {ALL_LANGS}')
    src = args.source_lang
    if src not in langs:
        langs.insert(0, src)
    if not arg('title', src) or not arg('excerpt', src):
        raise SystemExit(f'--title/--excerpt for the source language ({src}) are required')
    if args.push and not args.pr:
        print('[i] --push is deprecated: opening a Pull Request instead of pushing to main.')
        args.pr = True

    pub_date = args.date or datetime.date.today().strftime('%Y-%m-%d')
    dt = datetime.datetime.strptime(pub_date, '%Y-%m-%d')
    tags = [t.strip() for t in args.tags.split(',') if t.strip()]

    src_title, src_excerpt = arg('title', src), arg('excerpt', src)
    src_content = read_content(arg('content-file', src), arg('content-html', src))
    if not src_content:
        raise SystemExit(f'Content for the source language ({src}) is required (--content-file / --content-html).')

    data, translated, skipped = {}, [], []
    for lang in langs:
        title, excerpt = arg('title', lang), arg('excerpt', lang)
        content = read_content(arg('content-file', lang), arg('content-html', lang))
        need = [k for k, v in (('title', title), ('excerpt', excerpt), ('content', content)) if not v]
        if need and lang != src:
            if args.no_translate or args.dry_run:
                msg = f'{lang}: missing {need} and translation disabled' + (' (dry run)' if args.dry_run else '')
                if args.allow_missing or args.dry_run:
                    print(f'[!] Skipping {msg}')
                    skipped.append(lang)
                    continue
                raise SystemExit(f'[!] {msg}. Provide the texts, enable translation or use --allow-missing.')
            try:
                print(f'[*] Translating {src} -> {lang} via OpenRouter ({args.translate_model}) …')
                title = title or translate(src_title, src, lang, 'title', args.translate_model)
                excerpt = excerpt or translate(src_excerpt, src, lang, 'excerpt', args.translate_model)
                if not content:
                    content = translate(src_content, src, lang, 'html', args.translate_model)
                    problems = qa_html(src_content, content)
                    if problems:
                        raise TranslationError('QA failed: ' + '; '.join(problems))
                translated.append(lang)
            except Exception as e:
                if args.allow_missing:
                    print(f'[!] Skipping {lang}: {e}')
                    skipped.append(lang)
                    continue
                raise SystemExit(f'[!] Translation to {lang} failed: {e}')
        data[lang] = {'title': title, 'excerpt': excerpt, 'content': content}

    published = [l for l in ALL_LANGS if l in data]
    en_title = data['en']['title'] if 'en' in data else translate(src_title, src, 'en', 'title', args.translate_model) if not args.no_translate else src_title
    slug = f'{pub_date}-{slugify(en_title)}'
    branch = f'hermes/blog-{slug}'

    entry = {'slug': slug, 'date': pub_date, 'tags': tags, 'langs': published}
    for l in ALL_LANGS:
        s = SUFFIX[l]
        d = data.get(l)
        entry['url' + s] = post_rel(l, slug) if d else ''
        entry['blogUrl' + s] = post_rel(l, slug).replace('blog/', '', 1) if d else ''
        entry['displayDate' + s] = display_date(l, dt) if d else ''
        entry['title' + s] = d['title'] if d else ''
        entry['excerpt' + s] = d['excerpt'] if d else ''
        entry['readTime' + s] = read_time_for(l, arg('read-time', l), arg('read-time', 'en') or '4 min read') if d else ''

    print(f'[*] Article {slug}: languages {published}' + (f', translated {translated}' if translated else '') + (f', skipped {skipped}' if skipped else ''))
    if args.dry_run:
        print('[!] DRY RUN — no files written, no git.')
        print(json.dumps(entry, indent=2, ensure_ascii=False))
        return

    if args.pr:
        prepare_branch(branch)

    for l in published:
        d = data[l]
        out = render_post(l, slug, published, d['title'], d['excerpt'], d['content'], pub_date,
                          entry['displayDate' + SUFFIX[l]], entry['readTime' + SUFFIX[l]], tags, str(dt.year))
        os.makedirs(os.path.dirname(post_path(l, slug)), exist_ok=True)
        with open(post_path(l, slug), 'w', encoding='utf-8') as f:
            f.write(out)
        print(f'[+] Wrote {post_rel(l, slug)}.html')
        try:
            from sync_site import extract_markdown_from_html
            with open(post_path(l, slug)[:-5] + '.md', 'w', encoding='utf-8') as f:
                f.write(extract_markdown_from_html(out, d['title'], pub_date, d['excerpt']))
        except Exception as e:
            print(f'[!] Markdown alternate for {l} failed: {e}')

    posts = []
    if os.path.exists(POSTS_JSON):
        with open(POSTS_JSON, 'r', encoding='utf-8') as f:
            try:
                posts = json.load(f)
            except Exception:
                posts = []
    posts = [x for x in posts if x.get('slug') != slug]
    posts.insert(0, entry)
    with open(POSTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print(f'[+] Updated blog/posts.json ({len(posts)} posts)')

    from sync_site import main as run_site_sync
    run_site_sync()                       # sitemap.xml (+hreflang), llms.txt, .md alternates
    subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, 'build_i18n.py')], cwd=BASE_DIR, check=True)  # blog indexes per language

    urls = [f'{SITE}/{post_rel(l, slug)}' for l in published]
    if not args.pr:
        print('[+] Files written locally. Review, then publish with --pr (opens a Pull Request).')
        return

    git('add', 'blog', 'sitemap.xml', 'llms.txt', 'llms-full.txt', *[l for l in ALL_LANGS if os.path.isdir(os.path.join(BASE_DIR, l))], 'js/i18n.js')
    title = f'📝 Blog: {en_title} ({"+".join(x.upper() for x in published)})'
    git('commit', '-m', title)
    body = '\n'.join([
        'Automatický návrh článku od Hermes Agenta — **čaká na kontrolu človekom**.',
        '',
        f'- Slug: `{slug}`',
        f'- Jazyky: {", ".join(x.upper() for x in published)}',
        f'- Preložené cez OpenRouter ({args.translate_model}): {", ".join(x.upper() for x in translated) or "nič"}',
        f'- Vynechané: {", ".join(x.upper() for x in skipped) or "nič"}',
        '',
        '**Kontrola pred merge:** fakty a zdroje, tón, preklady (nadpisy, odkazy, kód), náhľad Cloudflare Pages.',
        '',
        f'Po merge a nasadení: `python3 scripts/publish_post.py --ping-slug {slug}` (IndexNow).',
        '',
        'URL po nasadení:',
        *[f'- {u}' for u in urls],
    ])
    pr_url = open_pull_request(branch, title, body)
    git('checkout', 'main', check=False)
    print(f'[+] Pull Request opened for review: {pr_url}')


if __name__ == '__main__':
    main()
