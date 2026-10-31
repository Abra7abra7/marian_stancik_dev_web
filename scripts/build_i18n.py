#!/usr/bin/env python3
"""
build_i18n.py — static multilingual pages for marianstancik.dev

Single source of truth for UI strings: locales/ui/{en,sk,cs,de,pl}.json
Templates (EN source pages): index.html, about.html, skills.html, drones.html,
expertise.html, contact.html, services.html (+ services-sk.html), blog/index.html

Outputs (committed to the repo, Cloudflare Pages serves them as static files):
  /{lang}/index.html, /{lang}/about.html, ... , /{lang}/blog/index.html
  js/i18n.js  -> the `translations` object is regenerated from locales/ui/*.json

Usage:
  python3 scripts/build_i18n.py           # build
  python3 scripts/build_i18n.py --check   # exit 1 if generated files are stale
"""
import argparse
import datetime
import html
import json
import os
import re
import sys

from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.marianstancik.dev'
LANGS = ['en', 'sk', 'cs', 'de', 'pl']
DEFAULT_LANG = 'en'
LOCALES_UI = os.path.join(BASE_DIR, 'locales', 'ui')
POSTS_JSON = os.path.join(BASE_DIR, 'blog', 'posts.json')
I18N_JS = os.path.join(BASE_DIR, 'js', 'i18n.js')

OG_LOCALE = {'en': 'en_US', 'sk': 'sk_SK', 'cs': 'cs_CZ', 'de': 'de_DE', 'pl': 'pl_PL'}
LANG_FIELD = {'en': '', 'sk': 'Sk', 'cs': 'Cs', 'de': 'De', 'pl': 'Pl'}
MONTHS = {
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'sk': ['január', 'február', 'marec', 'apríl', 'máj', 'jún', 'júl', 'august', 'september', 'október', 'november', 'december'],
    'cs': ['ledna', 'února', 'března', 'dubna', 'května', 'června', 'července', 'srpna', 'září', 'října', 'listopadu', 'prosince'],
    'de': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
    'pl': ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia'],
}
READ_TIME = {'en': '{n} min read', 'sk': '{n} min čítania', 'cs': '{n} min čtení', 'de': '{n} Min. Lesezeit', 'pl': '{n} min czytania'}
BLOG_FALLBACK_NOTE = {
    'cs': 'Články zatím vycházejí slovensky a anglicky. České verze připravujeme.',
    'de': 'Die Artikel erscheinen derzeit auf Englisch. Deutsche Versionen folgen.',
    'pl': 'Artykuły ukazują się obecnie po angielsku. Polskie wersje są w przygotowaniu.',
    'sk': 'Články sú zatiaľ v angličtine.',
}
# Fallback language for blog listing / pages that do not exist in a language
CONTENT_FALLBACK = {'cs': 'sk', 'de': 'en', 'pl': 'en', 'sk': 'en', 'en': 'en'}

# Page registry. path = URL path after /{lang}/ ; title_key = nav label used for the <title> of subpages
PAGES = [
    {'id': 'index', 'src': 'index.html', 'path': '', 'out': 'index.html', 'title_key': None, 'priority': '1.0', 'changefreq': 'weekly'},
    {'id': 'about', 'src': 'about.html', 'path': 'about', 'out': 'about.html', 'title_key': 'navAbout', 'priority': '0.9', 'changefreq': 'monthly'},
    {'id': 'services', 'src': {'en': 'services.html', 'sk': 'services-sk.html'}, 'path': 'services', 'out': 'services.html',
     'title_key': 'navProducts', 'langs': ['en', 'sk'], 'priority': '0.9', 'changefreq': 'weekly'},
    {'id': 'expertise', 'src': 'expertise.html', 'path': 'expertise', 'out': 'expertise.html', 'title_key': 'navExpertise', 'priority': '0.7', 'changefreq': 'monthly'},
    {'id': 'skills', 'src': 'skills.html', 'path': 'skills', 'out': 'skills.html', 'title_key': 'navSkills', 'priority': '0.7', 'changefreq': 'monthly'},
    {'id': 'drones', 'src': 'drones.html', 'path': 'drones', 'out': 'drones.html', 'title_key': 'navDrones', 'priority': '0.6', 'changefreq': 'monthly'},
    {'id': 'contact', 'src': 'contact.html', 'path': 'contact', 'out': 'contact.html', 'title_key': 'navContact', 'priority': '0.8', 'changefreq': 'monthly'},
    {'id': 'blog', 'src': 'blog/index.html', 'path': 'blog/', 'out': 'blog/index.html', 'title_key': 'navBlog', 'priority': '0.9', 'changefreq': 'weekly'},
]
PAGE_BY_ID = {p['id']: p for p in PAGES}
LEGACY_PATHS = {
    '/': 'index', '/index.html': 'index', '/about': 'about', '/about.html': 'about',
    '/services': 'services', '/services.html': 'services', '/services-sk': 'services', '/services-sk.html': 'services',
    '/expertise': 'expertise', '/expertise.html': 'expertise', '/skills': 'skills', '/skills.html': 'skills',
    '/drones': 'drones', '/drones.html': 'drones', '/contact': 'contact', '/contact.html': 'contact',
    '/blog': 'blog', '/blog/': 'blog', '/blog/index.html': 'blog',
}
LEGAL = ['privacy', 'terms', 'disclaimer']  # have EN + SK variants (-sk)
PROTECTED_TAGS = {'section', 'main', 'nav', 'header', 'footer', 'body', 'html', 'div', 'article', 'aside'}


def load_strings():
    out = {}
    for lang in LANGS:
        with open(os.path.join(LOCALES_UI, f'{lang}.json'), encoding='utf-8') as f:
            out[lang] = json.load(f)
    keys = set(out['en'])
    for lang in LANGS:
        missing = keys - set(out[lang])
        if missing:
            raise SystemExit(f'locales/ui/{lang}.json is missing keys: {sorted(missing)}')
    return out


def page_langs(page):
    return page.get('langs', LANGS)


def page_url(page, lang):
    return f'/{lang}/{page["path"]}'


def resolved_url(page, lang):
    """URL of the page in `lang`, or of its fallback language when that version does not exist."""
    if lang in page_langs(page):
        return page_url(page, lang)
    fb = CONTENT_FALLBACK.get(lang, DEFAULT_LANG)
    if fb not in page_langs(page):
        fb = DEFAULT_LANG
    return page_url(page, fb)


def strip_label(s):
    return re.sub(r'^[✦\s]+', '', BeautifulSoup(s, 'html.parser').get_text()).strip()


# ---------------------------------------------------------------- blog data
def load_posts():
    if not os.path.exists(POSTS_JSON):
        return []
    with open(POSTS_JSON, encoding='utf-8') as f:
        return json.load(f)


def post_rel(lang, slug):
    return f'blog/posts/{slug}' if lang == 'en' else f'blog/posts/{lang}/{slug}'


def post_exists(lang, slug):
    return os.path.exists(os.path.join(BASE_DIR, post_rel(lang, slug) + '.html'))


def fmt_date(lang, iso):
    try:
        d = datetime.date.fromisoformat(iso)
    except Exception:
        return iso
    m = MONTHS[lang][d.month - 1]
    if lang == 'en':
        return f'{m} {d.day:02d}, {d.year}'
    if lang == 'pl':
        return f'{d.day} {m} {d.year}'
    return f'{d.day}. {m} {d.year}'


def _from_post_file(lang, slug):
    p = os.path.join(BASE_DIR, post_rel(lang, slug) + '.html')
    with open(p, encoding='utf-8') as f:
        s = BeautifulSoup(f.read(), 'html.parser')
    h1 = s.find('h1')
    desc = s.find('meta', attrs={'name': 'description'})
    return (h1.get_text(strip=True) if h1 else ''), (desc.get('content', '') if desc else '')


def post_card(post, lang):
    sfx = LANG_FIELD[lang]
    slug = post['slug']
    title = post.get('title' + sfx) or ''
    excerpt = post.get('excerpt' + sfx) or ''
    if lang != 'en' and (not title or not excerpt or (title == post.get('title') and lang != 'en')):
        t2, e2 = _from_post_file(lang, slug)
        title = title if (title and title != post.get('title')) else (t2 or title)
        excerpt = excerpt if (excerpt and excerpt != post.get('excerpt')) else (e2 or excerpt)
    date = post.get('displayDate' + sfx) or fmt_date(lang, post.get('date', ''))
    rt = post.get('readTime' + sfx)
    if not rt:
        n = re.search(r'\d+', post.get('readTime', '5'))
        rt = READ_TIME[lang].format(n=n.group(0) if n else '5')
    tags = ''.join(f'<span>{html.escape(t)}</span>' for t in post.get('tags', []))
    return (f'\n      <a href="/{post_rel(lang, slug)}" class="post-item" lang="{lang}">\n'
            f'        <div class="post-top"><span class="post-date">{html.escape(date)}</span><span class="post-read">{html.escape(rt)}</span></div>\n'
            f'        <h2>{html.escape(title)}</h2>\n'
            f'        <p>{html.escape(excerpt)}</p>\n'
            f'        <div class="post-tags">{tags}</div>\n'
            f'      </a>')


def blog_langs(posts):
    """Languages that have at least one published post (these get an indexable blog index)."""
    return [l for l in LANGS if any(post_exists(l, p['slug']) for p in posts)]


# ---------------------------------------------------------------- rendering
def set_html(el, val):
    el.clear()
    if isinstance(val, str) and '<' in val and '>' in val:
        frag = BeautifulSoup(val, 'html.parser')
        for c in list(frag.contents):
            el.append(c)
    else:
        el.string = val


INLINE_TAGS = {'strong', 'em', 'b', 'i', 'a', 'span', 'br', 'code', 'small'}


def container_replaceable(el, val, lang):
    """Structural containers (div, section, …) are replaced only when that cannot break layout:
    plain-text content, the same inner tag structure as the translation, or (non-EN) only inline formatting."""
    if lang == DEFAULT_LANG:
        return False  # EN keeps the hand-written template text (same as the old client-side engine)
    inner = [t.name for t in el.find_all(True)]
    if not inner:
        return True
    if inner == [t.name for t in BeautifulSoup(val, 'html.parser').find_all(True)]:
        return True
    return lang != 'en' and set(inner) <= INLINE_TAGS


def translate_dom(soup, d, lang):
    for el in soup.select('[data-i18n]'):
        k = el.get('data-i18n')
        if k in d:
            set_html(el, d[k])
    for k, val in d.items():
        el = soup.find(id=k)
        if el is None:
            continue
        if el.name in PROTECTED_TAGS and not el.has_attr('data-i18n') and not container_replaceable(el, val, lang):
            continue
        set_html(el, val)


def rewrite_links(soup, lang):
    for a in soup.find_all('a', href=True):
        href = a['href']
        if not href.startswith('/') or href.startswith('//'):
            continue
        path, _, frag = href.partition('#')
        path, _, query = path.partition('?')
        new = None
        if path in LEGACY_PATHS:
            new = resolved_url(PAGE_BY_ID[LEGACY_PATHS[path]], lang)
        else:
            for lp in LEGAL:
                if path in (f'/{lp}', f'/{lp}-sk', f'/{lp}.html', f'/{lp}-sk.html'):
                    new = f'/{lp}-sk' if lang in ('sk', 'cs') else f'/{lp}'
        if new is None:
            continue
        a['href'] = new + (('?' + query) if query else '') + (('#' + frag) if frag else '')


def build_switcher(soup, page, lang):
    for sw in soup.select('.lang-switcher'):
        # the mobile copy inside the nav menu must not repeat the desktop ids
        mobile_copy = 'lang-switcher-mobile' in (sw.get('class') or [])
        sw.clear()
        for l in LANGS:
            a = soup.new_tag('a', href=resolved_url(page, l))
            a['class'] = ['lang-btn'] + (['active'] if l == lang else [])
            if not mobile_copy:
                a['id'] = 'btn' + l.capitalize()
            a['hreflang'] = l
            a['lang'] = l
            a['data-lang-btn'] = l
            if l == lang:
                a['aria-current'] = 'true'
            a.string = l.upper()
            sw.append(a)


def head_tags(soup, page, lang, alt_langs, indexable):
    head = soup.head
    for sel in ['link[rel="canonical"]', 'link[rel="alternate"][hreflang]', 'meta[property="og:url"]',
                'meta[property="og:locale"]', 'meta[property="og:locale:alternate"]', 'meta[name="robots"]']:
        for el in head.select(sel):
            el.decompose()
    anchor = head.find('title')
    new = []
    robots = 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1' if indexable else 'noindex, follow'
    new.append(soup.new_tag('meta', attrs={'name': 'robots', 'content': robots}))
    canonical_lang = lang if indexable else CONTENT_FALLBACK.get(lang, DEFAULT_LANG)
    new.append(soup.new_tag('link', attrs={'rel': 'canonical', 'href': SITE + page_url(page, canonical_lang)}))
    if indexable:
        for l in alt_langs:
            new.append(soup.new_tag('link', attrs={'rel': 'alternate', 'hreflang': l, 'href': SITE + page_url(page, l)}))
        new.append(soup.new_tag('link', attrs={'rel': 'alternate', 'hreflang': 'x-default', 'href': SITE + page_url(page, DEFAULT_LANG)}))
    new.append(soup.new_tag('meta', attrs={'property': 'og:url', 'content': SITE + page_url(page, canonical_lang)}))
    new.append(soup.new_tag('meta', attrs={'property': 'og:locale', 'content': OG_LOCALE[lang]}))
    for l in alt_langs:
        if l != lang:
            new.append(soup.new_tag('meta', attrs={'property': 'og:locale:alternate', 'content': OG_LOCALE[l]}))
    style = soup.new_tag('style')
    style['data-i18n-build'] = '1'
    style.string = 'a.lang-btn{text-decoration:none;display:inline-block;line-height:1.4}'
    new.append(style)
    for el in reversed(new):
        anchor.insert_after(el)
        anchor.insert_after('\n')


def set_meta(soup, name=None, prop=None, value=None):
    el = soup.head.find('meta', attrs={'name': name} if name else {'property': prop})
    if el is not None and value:
        el['content'] = value


def render_page(page, lang, strings, posts):
    src = page['src'][lang] if isinstance(page['src'], dict) else page['src']
    with open(os.path.join(BASE_DIR, src), encoding='utf-8') as f:
        soup = BeautifulSoup(f.read().replace('\r\n', '\n'), 'html.parser')
    d = strings[lang]
    soup.html['lang'] = lang
    soup.html['data-i18n-static'] = lang

    # services has hand-written EN and SK sources; only shared chrome (nav/footer) is translated there
    translate_dom(soup, d, lang)
    # legal links (privacy, terms, cookies, impressum) as a separate localized line under the footer disclaimer
    ai_act = soup.find(id='footerAiAct')
    if ai_act is not None and soup.find(id='footerLegalLinks') is None:
        legal = soup.new_tag('p', id='footerLegalLinks', style='margin:8px 0 0 0;')
        set_html(legal, d['footerLegalLinks'])
        ai_act.insert_after(legal)

    # <title> / description
    title_el = soup.head.find('title')
    desc_el = soup.head.find('meta', attrs={'name': 'description'})
    if page['id'] == 'index':
        title, desc = d['docTitle'], d['docDesc']
    elif lang == 'en' or isinstance(page['src'], dict):
        title = title_el.get_text() if title_el else d['docTitle']
        desc = desc_el.get('content') if desc_el else d['docDesc']
    else:
        tagline = d['docTitle'].split('|')[-1].strip() if '|' in d['docTitle'] else d['roleAi']
        title = f"{strip_label(d[page['title_key']])} — Marian Stancik | {tagline}"
        # per-page description: unikatna, 50-158 znakov
        label = strip_label(d[page['title_key']])
        base = d['docDesc']
        cand = f"{label} — {base}"
        if len(cand) > 158:
            cand = cand[:155].rsplit(' ', 1)[0] + '…'
        desc = cand
    if title_el is not None:
        title_el.string = title
    if desc_el is not None:
        desc_el['content'] = desc
    for n in ['twitter:title']:
        set_meta(soup, name=n, value=title)
    for n in ['twitter:description']:
        set_meta(soup, name=n, value=desc)
    set_meta(soup, prop='og:title', value=title)
    set_meta(soup, prop='og:description', value=desc)

    indexable = True
    alt_langs = page_langs(page)
    if page['id'] == 'blog':
        langs_with_posts = blog_langs(posts)
        alt_langs = langs_with_posts
        show_lang = lang if lang in langs_with_posts else CONTENT_FALLBACK.get(lang, 'en')
        indexable = lang in langs_with_posts
        main = soup.find(id='postContainer')
        main['id'] = 'postContainerStatic'
        main.clear()
        cards = ''.join(post_card(p, show_lang) for p in posts if post_exists(show_lang, p['slug']))
        note = '' if indexable else f'\n    <p class="section-intro" style="margin-bottom:1.5rem;">{html.escape(BLOG_FALLBACK_NOTE.get(lang, ""))}</p>'
        grp = BeautifulSoup(f'{note}\n    <div id="posts{show_lang.capitalize()}" class="posts-group" lang="{show_lang}">{cards}\n    </div>\n  ', 'html.parser')
        for c in list(grp.contents):
            main.append(c)

    head_tags(soup, page, lang, alt_langs, indexable)
    rewrite_links(soup, lang)
    build_switcher(soup, page, lang)
    out = str(soup)
    if not out.lstrip().lower().startswith('<!doctype'):
        out = '<!DOCTYPE html>\n' + out
    banner = f'<!-- GENERATED by scripts/build_i18n.py from {src} + locales/ui/{lang}.json — do not edit by hand -->\n'
    return out.replace('<!DOCTYPE html>\n', '<!DOCTYPE html>\n' + banner, 1) if out.startswith('<!DOCTYPE html>\n') else banner + out


def render_i18n_js(strings):
    with open(I18N_JS, encoding='utf-8') as f:
        js = f.read()
    start = js.index('const translations = {')
    end = js.index('\n};', start) + 3
    block = 'const translations = ' + json.dumps({l: strings[l] for l in LANGS}, ensure_ascii=False, indent=2) + ';'
    js = js[:start] + block + js[end:]
    return js


def outputs():
    strings = load_strings()
    posts = load_posts()
    files = {}
    for page in PAGES:
        for lang in LANGS:
            if lang not in page_langs(page):
                continue
            files[os.path.join(lang, page['out'])] = render_page(page, lang, strings, posts)
    files[os.path.relpath(I18N_JS, BASE_DIR)] = render_i18n_js(strings)
    return files


def sitemap_page_entries():
    """[(loc, {lang: url}, priority, changefreq)] for all generated, indexable pages."""
    posts = load_posts()
    entries = []
    for page in PAGES:
        langs = blog_langs(posts) if page['id'] == 'blog' else page_langs(page)
        alts = {l: SITE + page_url(page, l) for l in langs}
        alts['x-default'] = SITE + page_url(page, DEFAULT_LANG)
        for l in langs:
            entries.append((SITE + page_url(page, l), alts, page['priority'], page['changefreq']))
    return entries


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='fail if generated files are out of date')
    args = ap.parse_args()
    files = outputs()
    stale = []
    for rel, content in files.items():
        p = os.path.join(BASE_DIR, rel)
        cur = open(p, encoding='utf-8').read() if os.path.exists(p) else None
        if cur != content:
            stale.append(rel)
            if not args.check:
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(content)
    if args.check:
        if stale:
            print('❌ Generated i18n files are stale (run python3 scripts/build_i18n.py):')
            for s in stale:
                print('   -', s)
            sys.exit(1)
        print(f'✅ i18n build up to date ({len(files)} files)')
    else:
        print(f'✅ i18n build: {len(files)} files, {len(stale)} updated')


if __name__ == '__main__':
    main()
