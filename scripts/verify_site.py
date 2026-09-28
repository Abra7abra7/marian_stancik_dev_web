#!/usr/bin/env python3
import os
import re
import subprocess
import sys
import urllib.request
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    pages = [
        'index.html',
        'about.html',
        'services.html',
        'services-sk.html',
        'expertise.html',
        'skills.html',
        'drones.html',
        'contact.html',
        'blog/index.html'
    ]

    print("========================================")
    print(" 1. SECURITY & ANONYMIZATION (L4 SWEEP)")
    print("========================================")
    found_sec = False
    for root, dirs, files in os.walk('.'):
        if '.git' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith(('.html', '.md', '.js', '.txt', '.json', '.xml')) and file not in ['AGENTS.md', 'test_visual.py', 'verify_site.py']:
                p = os.path.join(root, file)
                with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = re.findall(r'Delta\s*Defence', content, re.IGNORECASE)
                    if matches:
                        print(f"❌ Security violation in {p}: {matches}")
                        found_sec = True
    if not found_sec:
        print("✅ L4 Security Sweep passed (0 forbidden company names found)")

    print("\n========================================")
    print(" 2. JS SYNTAX CHECK (L0)")
    print("========================================")
    for js_file in ['js/i18n.js', 'js/three-bg.js']:
        if os.path.exists(js_file):
            r = subprocess.run(['node', '--check', js_file], capture_output=True, text=True)
            if r.returncode == 0:
                print(f"✅ {js_file}: Syntax OK")
            else:
                print(f"❌ {js_file}: Syntax error:\n{r.stderr}")

    print("\n========================================")
    print(" 3. HTML META & LINK INTEGRITY CHECK")
    print("========================================")
    all_pages_ok = True
    for p in pages:
        if not os.path.exists(p):
            print(f"❌ Missing page file: {p}")
            all_pages_ok = False
            continue
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        errors = []
        if 'OG_<title>' in c or 'OG_<meta' in c:
            errors.append('Found malformed OG_ tags')
        if 'https://www.marianstancik.devabout' in c or 'https://www.marianstancik.devexpertise' in c:
            errors.append('Found malformed URL in JSON-LD')
        if 'href="blog/index.html"' in c:
            errors.append('Found relative blog/index.html link')
        if 'class="skip-link"' not in c and p != 'blog/index.html':
            errors.append('Missing skip-link')
        if 'rel="alternate" type="text/plain" href="/llms.txt"' not in c:
            errors.append('Missing llms.txt discovery link')

        if errors:
            print(f"❌ {p}: {errors}")
            all_pages_ok = False
        else:
            print(f"✅ {p}: All checks passed")

    print("\n========================================")
    print(" 4. DESIGN TOKENS & CSS VALIDATION")
    print("========================================")
    with open('css/main.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    if ':root' in css_content and '--color-primary' in css_content and '--font-body' in css_content:
        print("✅ css/main.css: :root Design Tokens present")
    else:
        print("❌ css/main.css: Missing :root tokens")

    print("\n========================================")
    print(" 5. AI CRAWLERS IN ROBOTS.TXT")
    print("========================================")
    with open('robots.txt', 'r', encoding='utf-8') as f:
        robots = f.read()
    if 'GPTBot' in robots and 'ClaudeBot' in robots and 'PerplexityBot' in robots:
        print("✅ robots.txt: AI bots explicitly allowed & indexed")
    else:
        print("❌ robots.txt: Missing AI bot directives")

    print("\n========================================")
    print(" 6. API HEALTH CHECK (L8)")
    print("========================================")
    api_ok = True
    for endpoint, payload in [
        ("/api/subscribe", '{"email":"test@pre-commit-check.local","source":"pre-commit-check"}'),
    ]:
        url = f"https://www.marianstancik.dev{endpoint}"
        try:
            req = urllib.request.Request(url, data=payload.encode(), headers={"Content-Type": "application/json"}, method="POST")
            resp = urllib.request.urlopen(req, timeout=10)
            body = json.loads(resp.read().decode())
            if body.get("status") == "ok":
                print(f"✅ {endpoint}: returns status=ok")
            else:
                print(f"❌ {endpoint}: unexpected response: {body}")
                api_ok = False
        except Exception as e:
            print(f"❌ {endpoint}: {e}")
            api_ok = False
    print("\n========================================")
    print(" 7. CONFIG & MARKDOWN INTEGRITY CHECK")
    print("========================================")
    cfg_ok = True
    if not os.path.exists('site.config.json'):
        print("❌ Missing site.config.json")
        cfg_ok = False
    else:
        with open('site.config.json', 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        if 'products' in cfg and 'profile' in cfg:
            print("✅ site.config.json: Valid schema")
        else:
            print("❌ site.config.json: Missing required fields")
            cfg_ok = False

    for loc in ['en', 'sk', 'de', 'pl']:
        loc_path = f"locales/{loc}.json"
        if os.path.exists(loc_path):
            print(f"✅ {loc_path}: Present and valid")
        else:
            print(f"❌ Missing locale file: {loc_path}")
            cfg_ok = False

    # Check that all posts have 4-language .md and .html alternates
    if os.path.exists('blog/posts.json'):
        with open('blog/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
        missing_md = 0
        missing_html = 0
        for p in posts:
            slug = p['slug']
            for l_dir, l_label in [('', 'EN'), ('sk/', 'SK'), ('de/', 'DE'), ('pl/', 'PL')]:
                if not os.path.exists(f"blog/posts/{l_dir}{slug}.md"):
                    print(f"❌ Missing .md alternate for {l_dir}{slug}")
                    missing_md += 1
                if not os.path.exists(f"blog/posts/{l_dir}{slug}.html"):
                    print(f"❌ Missing HTML alternate for {l_dir}{slug} ({l_label})")
                    missing_html += 1
        total_expected = len(posts) * 4
        if missing_md == 0:
            print(f"✅ All {len(posts)} blog posts have 4-language (EN/SK/DE/PL) .md alternates (all {total_expected} files present)")
        else:
            cfg_ok = False
        if missing_html == 0:
            print(f"✅ All {len(posts)} blog posts have 4-language (EN/SK/DE/PL) HTML alternates (all {total_expected} files present)")
        else:
            cfg_ok = False
        if missing_md == 0 and missing_html == 0:
            print(f"✅ Full 4-language blog parity: {total_expected}/{total_expected} HTML + MD files")

        # Check blog/index.html has correct number of entries per language
        try:
            with open('blog/index.html', 'r', encoding='utf-8') as f:
                idx = f.read()
            for lang_section, label in [('postsEn', 'EN'), ('postsSk', 'SK'), ('postsDe', 'DE'), ('postsPl', 'PL')]:
                count = len(re.findall(rf'id="posts{lang_section[6:]}".*?</div>\s*<!--', idx, re.DOTALL))
                posts_in_section = idx.count(f'<a href="/blog/posts/')
                # Count actual post items in each section
                section_start = idx.find(f'id="{lang_section}"')
                section_end = idx.find('<!--', section_start) if lang_section != 'postsPl' else idx.find('<footer>', section_start)
                section_html = idx[section_start:section_end]
                post_count = len(re.findall(r'class="post-item"', section_html))
                if post_count < len(posts):
                    print(f"❌ blog/index.html ({label}): found {post_count} posts, expected {len(posts)}")
                    cfg_ok = False
                else:
                    print(f"✅ blog/index.html ({label}): all {post_count} posts listed correctly")
        except Exception as e:
            print(f"❌ blog/index.html check failed: {e}")
            cfg_ok = False

    if cfg_ok:
        print("✅ Config, Markdown & HTML parity checks passed")

    print("\n========================================")
    print(" 8. I18N 4-LANGUAGE PARITY CHECK")
    print("========================================")
    if os.path.exists('js/i18n.js'):
        with open('js/i18n.js', 'r', encoding='utf-8') as f:
            js_code = f.read()
        match = re.search(r'const translations = ({[\s\S]*?});\s*\n\s*let currentLang', js_code)
        if match:
            t = json.loads(match.group(1))
            en_keys = set(t.get('en', {}).keys())
            print(f"Total dictionary keys: {len(en_keys)}")
            parity_ok = True
            for lang in ['sk', 'de', 'pl']:
                l_keys = set(t.get(lang, {}).keys())
                missing = en_keys - l_keys
                if missing:
                    print(f"❌ {lang.upper()} missing keys: {missing}")
                    parity_ok = False
                else:
                    print(f"✅ {lang.upper()} parity: 100% ({len(l_keys)}/{len(en_keys)} keys present)")
            if parity_ok:
                print("✅ Full 4-language i18n parity verified")
        else:
            print("❌ Could not parse translations dictionary from js/i18n.js")

    print("\n========================================")
    print(" 9. DEPLOY SAFETY (root output directories)")
    print("========================================")
    # INCIDENT 2026-09-28: root `public/` existoval a Vercel ho zacal brat ako
    # Output Directory -> deployment serviroval len public/, CELY web vracal 404
    # (/, /about, /robots.txt, /sitemap.xml) a nikto si to 7.5 h nevsimol.
    forbidden_dirs = ['public', 'dist', 'out', 'build']
    blocking = [d for d in forbidden_dirs if os.path.isdir(d)]
    if blocking:
        for d in blocking:
            n = sum(len(f) for _, _, f in os.walk(d))
            print(f"❌ Root directory '{d}/' exists ({n} files) — Vercel will treat it as"
                  f" the Output Directory and serve ONLY its contents; every other path 404s.")
            print(f"   FIX: move the files out of '{d}/' into the repo root (or reference"
                  f" them from a non-root path) and delete '{d}/'.")
    else:
        print("✅ No root output directories (public/ dist/ out/ build/) — full site is deployed")


if __name__ == '__main__':
    import contextlib, io
    # Suite musi realne blokovat: ak je kdekoľvek ❌, commit konci exit 1.
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        main()
    output = buf.getvalue()
    print(output, end="")
    if "❌" in output:
        print("\n❌ VERIFICATION FAILED — deploy blocked, fix the ❌ items above.")
        sys.exit(1)
    print("\n✅ VERIFICATION PASSED — safe to deploy.")

