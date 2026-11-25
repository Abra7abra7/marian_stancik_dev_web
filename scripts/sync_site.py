#!/usr/bin/env python3
"""
Sync Site Engine — Single Source of Truth Orchestration
Reads site.config.json + locales/{en,sk,de,pl}.json (+ per-language pages from build_i18n.py) and automatically:
1. Generates clean .md markdown alternates for all blog posts (fixing 404 on Link headers).
2. Generates updated llms.txt & llms-full.txt (with all 6 articles + products).
3. Generates complete sitemap.xml with proper hreflang alternate tags.
4. Synchronizes i18n dictionaries and ensures all metadata remains consistent.
"""

import os
import re
import json
import datetime
from html.parser import HTMLParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'site.config.json')
LOCALES_DIR = os.path.join(BASE_DIR, 'locales')
POSTS_DIR = os.path.join(BASE_DIR, 'blog', 'posts')
POSTS_SK_DIR = os.path.join(BASE_DIR, 'blog', 'posts', 'sk')
POSTS_JSON = os.path.join(BASE_DIR, 'blog', 'posts.json')
LLMS_TXT = os.path.join(BASE_DIR, 'llms.txt')
LLMS_FULL_TXT = os.path.join(BASE_DIR, 'llms-full.txt')
SITEMAP_XML = os.path.join(BASE_DIR, 'sitemap.xml')

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_locales():
    locales = {}
    for code in ['en', 'sk', 'de', 'pl']:
        p = os.path.join(LOCALES_DIR, f"{code}.json")
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                locales[code] = json.load(f)
    return locales

class HTMLToMarkdownExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_article = False
        self.in_script = False
        self.in_style = False
        self.text_parts = []
        
    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style', 'nav', 'footer', 'header']:
            self.in_script = True
        if tag == 'article' or (tag == 'div' and ('class', 'post-body') in attrs):
            self.in_article = True
        if self.in_article:
            if tag in ['h1', 'h2', 'h3', 'h4']:
                self.text_parts.append(f"\n\n### ")
            elif tag == 'p':
                self.text_parts.append("\n\n")
            elif tag == 'li':
                self.text_parts.append("\n- ")
            elif tag == 'pre' or tag == 'code':
                self.text_parts.append("\n```\n")

    def handle_endtag(self, tag):
        if tag in ['script', 'style', 'nav', 'footer', 'header']:
            self.in_script = False
        if tag == 'article':
            self.in_article = False
        if self.in_article:
            if tag == 'pre' or tag == 'code':
                self.text_parts.append("\n```\n")

    def handle_data(self, data):
        if not self.in_script and self.in_article:
            self.text_parts.append(data)

def extract_markdown_from_html(html_content, title, date, excerpt):
    parser = HTMLToMarkdownExtractor()
    parser.feed(html_content)
    raw_text = "".join(parser.text_parts).strip()
    
    # Clean excessive whitespace
    clean_body = re.sub(r'\n{3,}', '\n\n', raw_text)
    
    md_content = f"""# {title}

> **Published:** {date}  
> **Author:** Marian Stancik  
> **Summary:** {excerpt}

---

{clean_body}

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
"""
    return md_content

def sync_blog_markdown_files():
    print("Generating .md markdown alternates for blog posts...")
    if not os.path.exists(POSTS_JSON):
        return
    with open(POSTS_JSON, 'r', encoding='utf-8') as f:
        posts = json.load(f)
        
    for p in posts:
        slug = p['slug']
        en_html = os.path.join(POSTS_DIR, f"{slug}.html")
        en_md = os.path.join(POSTS_DIR, f"{slug}.md")
        sk_html = os.path.join(POSTS_SK_DIR, f"{slug}.html")
        sk_md = os.path.join(POSTS_SK_DIR, f"{slug}.md")
        de_html = os.path.join(POSTS_DIR, 'de', f"{slug}.html")
        de_md = os.path.join(POSTS_DIR, 'de', f"{slug}.md")
        pl_html = os.path.join(POSTS_DIR, 'pl', f"{slug}.html")
        pl_md = os.path.join(POSTS_DIR, 'pl', f"{slug}.md")
        
        if os.path.exists(en_html):
            with open(en_html, 'r', encoding='utf-8') as f:
                content = f.read()
            md = extract_markdown_from_html(content, p['title'], p['date'], p['excerpt'])
            with open(en_md, 'w', encoding='utf-8') as f:
                f.write(md)
            print(f"  [EN] Created {slug}.md")
            
        if os.path.exists(sk_html):
            with open(sk_html, 'r', encoding='utf-8') as f:
                content = f.read()
            md = extract_markdown_from_html(content, p.get('titleSk', p['title']), p['date'], p.get('excerptSk', p['excerpt']))
            with open(sk_md, 'w', encoding='utf-8') as f:
                f.write(md)
            print(f"  [SK] Created sk/{slug}.md")

        if os.path.exists(de_html):
            with open(de_html, 'r', encoding='utf-8') as f:
                content = f.read()
            md = extract_markdown_from_html(content, p.get('titleDe', p['title']), p['date'], p.get('excerptDe', p['excerpt']))
            with open(de_md, 'w', encoding='utf-8') as f:
                f.write(md)
            print(f"  [DE] Created de/{slug}.md")

        if os.path.exists(pl_html):
            with open(pl_html, 'r', encoding='utf-8') as f:
                content = f.read()
            md = extract_markdown_from_html(content, p.get('titlePl', p['title']), p['date'], p.get('excerptPl', p['excerpt']))
            with open(pl_md, 'w', encoding='utf-8') as f:
                f.write(md)
            print(f"  [PL] Created pl/{slug}.md")

        cs_html = os.path.join(POSTS_DIR, 'cs', f"{slug}.html")
        if os.path.exists(cs_html):
            with open(cs_html, 'r', encoding='utf-8') as f:
                content = f.read()
            md = extract_markdown_from_html(content, p.get('titleCs') or p['title'], p['date'], p.get('excerptCs') or p['excerpt'])
            with open(os.path.join(POSTS_DIR, 'cs', f"{slug}.md"), 'w', encoding='utf-8') as f:
                f.write(md)
            print(f"  [CS] Created cs/{slug}.md")

def sync_llms_txt(config):
    print("Generating llms.txt & llms-full.txt...")
    posts = []
    if os.path.exists(POSTS_JSON):
        with open(POSTS_JSON, 'r', encoding='utf-8') as f:
            posts = json.load(f)

    # llms.txt (Concise llmstxt.org v2 — synced with AGENTS.md & .agents/product-marketing.md)
    llms_content = f"""# {config['profile']['name']}

> I build and manage AI agents (Hermes Agent, OpenBot) to save time, delegate routine work, orchestrate tasks, and measure real results — without the AI hype.

## Identity (Who I Am & Who I Am NOT)

- **Who I am:** Builder and manager of practical AI agents using open-source frameworks (**Hermes Agent** and **OpenBot**, an open-source alternative to Grok bot). Focused on delegating routine work, orchestrating workflows, and keeping token costs under control for both businesses and individuals.
- **Real numbers (not hype):** AI is just a tool. In one month my agents consumed **4 billion tokens for ~$200 USD** using DeepSeek via OpenRouter — the same workload on top frontier models would have cost **~$15,000 USD**.
- **Law & Privacy:** 3rd-year law student (Comenius University, Bratislava) interested in GDPR and the EU AI Act.
- **Who I am NOT:** Not a lawyer — by law I **do not provide legal advice**. Everything on this site is my subjective view. Not an "AI guru", and not running an e-shop or selling packaged products right now.
- **Automation transparency (EU AI Act Art. 50):** This entire website and my professional email (`marianstancik@agentmail.to`) are managed by autonomous AI agents with human editorial oversight.

## Direct Contact

- **WhatsApp (fastest, personal):** [+421 940 377 855](https://wa.me/421940377855)
- **Agent-managed Email:** [marianstancik@agentmail.to](mailto:marianstancik@agentmail.to)
- **20-min Online Call:** [Google Calendar](https://calendar.app.google/hu1vx3nqLgK65u5C7)

## Core Pages (Available in EN, SK, CS, DE, PL)

- [Home (EN)](https://www.marianstancik.dev/en/): Plain-language overview, real token cost numbers (4B tokens / ~$200 vs $15k), "What I am / What I am NOT", newsletter signup, and direct WhatsApp.
- [Home (SK)](https://www.marianstancik.dev/sk/): Slovenská verzia hlavnej stránky.
- [How it works](https://www.marianstancik.dev/en/how-it-works): How a 14-agent team splits roles, what one normal day looks like, and where a human still decides.
- [Free Tools](https://www.marianstancik.dev/en/tools/): Prompt Library, AI Agent Starter Kit, and upcoming Mission Planner — free, no hype.
- [Prompt Library](https://www.marianstancik.dev/en/tools/prompt-library): 15 field-tested agent prompts (prompt → input → output → known failures). Free, no sign-up.
- [AI Agent Starter Kit](https://www.marianstancik.dev/en/tools/starter-kit): 15 prompts, 3-step first-agent playbook, and guardrails checklist — free by double opt-in email.
- [Blog](https://www.marianstancik.dev/en/blog/): Build log and technical notes on AI agents, token economics, guardrails, GEO, and EU AI Act reflections.
- [Contact](https://www.marianstancik.dev/en/contact): Direct WhatsApp (+421 940 377 855), agent-managed email (`marianstancik@agentmail.to`), and 20-min call booking.

## Technical Articles

"""
    for p in posts:
        llms_content += f"- [{p['title']}](https://www.marianstancik.dev/{p['url']}): {p['excerpt']}\n"

    llms_content += f"""
## Machine-Readable Feeds & Profiles

- [Full LLM Knowledge Graph](https://www.marianstancik.dev/llms-full.txt): Extended context and Q&A for AI search engines and autonomous agents.
- [Blog Posts Feed JSON](https://www.marianstancik.dev/blog/posts.json): Complete JSON archive of all published articles.
- [XML Sitemap](https://www.marianstancik.dev/sitemap.xml): Canonical URL index across all 5 languages (EN, SK, CS, DE, PL).
- [RSS Feed](https://www.marianstancik.dev/rss.xml): Standard RSS syndication feed.
- [GitHub]({config['profile']['socials']['github']}): Open-source repositories and website source.
- [LinkedIn]({config['profile']['socials']['linkedin']}): Professional profile.
- [X (Twitter)]({config['profile']['socials']['x']}): Build updates and AI agent notes.
- [YouTube]({config['profile']['socials']['youtube']}): Video breakdowns.
"""
    with open(LLMS_TXT, 'w', encoding='utf-8') as f:
        f.write(llms_content.strip() + "\n")
    print("  Updated llms.txt")

    # llms-full.txt (Comprehensive Knowledge Graph — synced with AGENTS.md)
    llms_full_content = f"""# {config['profile']['name']} — Full AI Agent Context & Knowledge Graph

> Practical AI agents without the hype: open-source orchestration (Hermes Agent, OpenBot), real token-cost economics, free tools, and transparent human-in-the-loop automation.

## Quick Facts for AI Search Engines & Agents

- **Name:** Marian Stancik (legal operator name: Marián Stančík, Sole Proprietor / Živnostník, Brezno, Slovakia, IČO: 57068917, DIČ: 1082585075, non-VAT payer)
- **Website:** https://www.marianstancik.dev (hosted on Cloudflare Pages, global edge CDN, static 5-language HTML + Markdown alternates via `Accept: text/markdown`)
- **Languages:** English (`/en/`), Slovak (`/sk/`), Czech (`/cs/`), German (`/de/`), Polish (`/pl/`)
- **Primary Focus:** Building, delegating to, orchestrating, and measuring practical AI agents using open-source frameworks (**Hermes Agent** and **OpenBot**, an open-source alternative to Grok bot).
- **Target Audience:** Both businesses (founders, managers, SEO/growth teams) and individuals who want to save time and cut repetitive work without AI hype or vendor lock-in.
- **Business Model:** No e-shop or packaged products sold on the site right now. Free tools, open build logs, and direct conversations via WhatsApp.
- **Direct Contact (Personal):** WhatsApp `+421 940 377 855` (`https://wa.me/421940377855`)
- **Agent-Managed Email:** `marianstancik@agentmail.to` (read, triaged, and drafted by an AI agent)
- **Calendar:** `https://calendar.app.google/hu1vx3nqLgK65u5C7` (20-min free call)

## Proof Points & Real Numbers

- **Token Economics:** 4 billion tokens consumed in one month across live autonomous agents for approximately **$200 USD** using DeepSeek via OpenRouter — compared to roughly **$15,000 USD** for the same volume on top frontier models.
- **Philosophy:** AI is strictly a tool, not magic. System architecture, clear rules, model routing, and measurable ROI matter more than chasing the most expensive model.
- **Full Automation Disclosure:** This website and its agent inbox (`marianstancik@agentmail.to`) are operated by AI agents under human editorial responsibility (EU AI Act Art. 50).

## Strict Boundaries (What Marian Stancik Is NOT)

- **NOT a lawyer / NO legal advice:** Marian is a 3rd-year law student (Faculty of Law, Comenius University in Bratislava) interested in privacy (GDPR) and the EU AI Act. By Slovak law (Act No. 586/2003 Coll. on Advocacy), he does **not** provide legal advice. All regulatory content on this site represents subjective educational notes only.
- **NOT an AI guru:** No overnight miracle claims, no paid hype courses, no "set and forget" autonomy without human oversight.
- **NO active online store:** Legacy paid audit packages and Stripe links have been removed; visitors get free tools, prompts, and direct contact.

## Blog Articles

"""
    for p in posts:
        llms_full_content += f"- [{p['title']}](https://www.marianstancik.dev/{p['url']}): {p['excerpt']}\n"

    llms_full_content += f"""
## Core Machine-Readable Endpoints

- `https://www.marianstancik.dev/llms.txt` — Concise LLM summary
- `https://www.marianstancik.dev/llms-full.txt` — Full knowledge graph (this file)
- `https://www.marianstancik.dev/blog/posts.json` — Complete blog posts archive
- `https://www.marianstancik.dev/sitemap.xml` — Full multilingual XML sitemap
- `https://www.marianstancik.dev/rss.xml` — RSS feed
- `Accept: text/markdown` — Supported on HTML pages via Cloudflare Edge Middleware (`functions/_middleware.js`)

## Social & Professional Channels

- [WhatsApp](https://wa.me/421940377855): +421 940 377 855 (fastest personal channel)
- [Email](mailto:marianstancik@agentmail.to): Agent-managed inbox
- [GitHub]({config['profile']['socials']['github']}): Open-source repositories and website source
- [LinkedIn]({config['profile']['socials']['linkedin']}): Professional profile
- [X (Twitter)]({config['profile']['socials']['x']}): Build updates and AI agent notes
- [YouTube]({config['profile']['socials']['youtube']}): Video breakdowns
"""
    with open(LLMS_FULL_TXT, 'w', encoding='utf-8') as f:
        f.write(llms_full_content.strip() + "\n")
    print("  Updated llms-full.txt")

def sync_sitemap(config):
    """sitemap.xml: per-language static pages (from build_i18n) + legal pages + blog posts.
    Only URLs that really exist are listed, and every hreflang cluster lists only existing translations."""
    print("Generating sitemap.xml with full hreflang alternates...")
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from build_i18n import sitemap_page_entries, LANGS, post_exists, post_rel, SITE

    today = datetime.date.today().isoformat()
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    xml.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')

    def add(loc, alts, lastmod, changefreq, priority):
        xml.append('  <url>')
        xml.append(f'    <loc>{loc}</loc>')
        for hl, href in (alts or {}).items():
            xml.append(f'    <xhtml:link rel="alternate" hreflang="{hl}" href="{href}"/>')
        xml.append(f'    <lastmod>{lastmod}</lastmod>')
        xml.append(f'    <changefreq>{changefreq}</changefreq>')
        xml.append(f'    <priority>{priority}</priority>')
        xml.append('  </url>')

    for loc, alts, priority, changefreq in sitemap_page_entries():
        add(loc, alts, today, changefreq, priority)

    legal = [
        ("/impressum", None), ("/impressum-en", None), ("/cookie", None),
        ("/privacy", "/privacy-sk"), ("/terms", "/terms-sk"), ("/disclaimer", "/disclaimer-sk"),
    ]
    for en_path, sk_path in legal:
        if sk_path:
            alts = {'en': SITE + en_path, 'sk': SITE + sk_path, 'x-default': SITE + en_path}
            add(SITE + en_path, alts, today, 'monthly', '0.5')
            add(SITE + sk_path, alts, today, 'monthly', '0.5')
        else:
            add(SITE + en_path, None, today, 'monthly', '0.5')
    for extra in ["/llms.txt", "/llms-full.txt"]:
        add(SITE + extra, None, today, 'monthly', '0.5')

    posts = []
    if os.path.exists(POSTS_JSON):
        with open(POSTS_JSON, 'r', encoding='utf-8') as f:
            posts = json.load(f)
    for post in posts:
        slug = post['slug']
        langs = [l for l in LANGS if post_exists(l, slug)]
        if not langs:
            continue
        alts = {l: f"{SITE}/{post_rel(l, slug)}" for l in langs}
        alts['x-default'] = alts.get('en', alts[langs[0]])
        for l in langs:
            add(alts[l], alts, post.get("date", today), 'monthly', '0.7')

    xml.append('</urlset>')
    with open(SITEMAP_XML, 'w', encoding='utf-8') as f:
        f.write("\n".join(xml) + "\n")
    print("  Updated sitemap.xml")

def main():
    print("=== STARTING SITE SYNC ENGINE ===")
    config = load_config()
    sync_blog_markdown_files()
    sync_llms_txt(config)
    sync_sitemap(config)
    print("=== SITE SYNC COMPLETE (100% OK) ===")

if __name__ == '__main__':
    main()
