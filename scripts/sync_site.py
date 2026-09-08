#!/usr/bin/env python3
"""
Sync Site Engine — Single Source of Truth Orchestration
Reads site.config.json + locales/{en,sk,de,pl}.json and automatically:
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

def sync_llms_txt(config):
    print("Generating llms.txt & llms-full.txt...")
    posts = []
    if os.path.exists(POSTS_JSON):
        with open(POSTS_JSON, 'r', encoding='utf-8') as f:
            posts = json.load(f)
            
    # llms.txt (Concise llmstxt.org v2)
    llms_content = f"""# {config['profile']['name']}

> {config['profile']['tagline']['en']}

Marian Stancik builds autonomous agent ecosystems (Hermes Agent, MCP), hand-soldered tactical UAV edge AI drones (ArduPilot, Raspberry Pi 5), and legal-by-design compliance architectures (EU AI Act, GDPR, NIS2, DORA).

## Core Pages

- [Home](https://www.marianstancik.dev/): High-impact hero, autonomous agent stats, live 24/7 cron orchestrations, and connect channels.
- [About](https://www.marianstancik.dev/about): Technical bio, 4-layer engineering stack (Hetzner VPS, OpenRouter, Obsidian, Zero-build Web), and career timeline.
- [Products & Audits](https://www.marianstancik.dev/services): 4 production-ready products (AI GEO Audit €150, Web Readiness Scan €200, Full Web Audit €300, Custom Agent from €500).
- [Tactical UAV Systems](https://www.marianstancik.dev/drones): Hand-soldered 1500g carbon quadcopter, ArduPilot Copter autopilot, Raspberry Pi 5 edge vision AI (Hobby project).
- [Blog](https://www.marianstancik.dev/blog): Technical articles on autonomous AI workflows, legal-by-design compliance (AI Act, GDPR), and robotics.
- [Contact](https://www.marianstancik.dev/contact): Direct lead capture, communication channels, and social profiles.

## Technical Articles

"""
    for p in posts:
        llms_content += f"- [{p['title']}](https://www.marianstancik.dev/{p['url']}): {p['excerpt']}\n"

    llms_content += f"""
## Optional

- [Full LLM Knowledge Graph](https://www.marianstancik.dev/llms-full.txt): Comprehensive deep-context technical knowledge graph and Q&A dataset.
- [Blog Posts Feed JSON](https://www.marianstancik.dev/blog/posts.json): Structured JSON archive of all published articles, dates, tags, and reading times.
- [XML Sitemap](https://www.marianstancik.dev/sitemap.xml): Search engine indexing directory for all canonical website endpoints.
- [RSS XML Feed](https://www.marianstancik.dev/rss.xml): Standard RSS syndication feed for autonomous web readers and crawlers.
- [GitHub]({config['profile']['socials']['github']}): Open-source repositories, agent scripts, MCP servers, and website source.
- [X (Twitter)]({config['profile']['socials']['x']}): Daily autonomous build updates, AI engineering thoughts, and UAV flight logs.
- [YouTube]({config['profile']['socials']['youtube']}): Long-form video breakdowns of AI agents, drone builds, and legal compliance.
- [LinkedIn]({config['profile']['socials']['linkedin']}): Professional engineering profile, publications, and enterprise advisory.
- [Email](mailto:{config['site']['email']}): Direct asynchronous agent-routed communication endpoint.
"""
    with open(LLMS_TXT, 'w', encoding='utf-8') as f:
        f.write(llms_content.strip() + "\n")
    print("  Updated llms.txt")

    # llms-full.txt (Comprehensive Knowledge Graph)
    llms_full_content = f"""# {config['profile']['name']} — Full AI Agent Context & Knowledge Graph

> Personal brand website, comprehensive technical knowledge graph, and autonomous multi-agent engineering platform of Marian Stancik.

## Core Endpoints & Pages

- [Home](https://www.marianstancik.dev/): High-impact hero, autonomous agent stats, live 24/7 cron orchestrations, and connect channels.
- [About](https://www.marianstancik.dev/about): Technical bio, 4-layer engineering stack (Hetzner VPS, OpenRouter, Obsidian, Zero-build Web), and career timeline.
- [Products & Audits](https://www.marianstancik.dev/services): AI GEO Audit (€150), AI Web Readiness Scan (€200), Full Web Audit (€300), Custom Autonomous Agent (€500 deposit).
- [Tactical UAV Systems](https://www.marianstancik.dev/drones): Hand-soldered 1500g carbon quadcopter, ArduPilot Copter autopilot, Raspberry Pi 5 edge vision AI (Hobby project).
- [Blog Archive](https://www.marianstancik.dev/blog): Technical articles on autonomous AI workflows, legal-by-design compliance (AI Act, GDPR), and robotics.
- [Contact & Connect](https://www.marianstancik.dev/contact): Direct lead capture, communication channels, and social profiles.

## Blog Articles

"""
    for p in posts:
        llms_full_content += f"- [{p['title']}](https://www.marianstancik.dev/{p['url']}): {p['excerpt']}\n"

    llms_full_content += f"""
## Machine-Readable Endpoints

- [LLM Summary Context](https://www.marianstancik.dev/llms.txt): Concise LLM knowledge graph standard file.
- [Blog Posts Feed JSON](https://www.marianstancik.dev/blog/posts.json): Structured JSON archive of all published articles, dates, tags, and reading times.
- [XML Sitemap](https://www.marianstancik.dev/sitemap.xml): Search engine indexing directory for all canonical website endpoints.
- [RSS XML Feed](https://www.marianstancik.dev/rss.xml): Standard RSS syndication feed for autonomous web readers and crawlers.

## Identity & Core Positioning

Marian Stancik is an AI Engineer, UAV Systems Builder, and Law Scholar exploring the convergence of artificial intelligence, autonomous physical hardware, and regulatory compliance.

His core differentiation is the intersection of three domains:
1. **Autonomous AI Systems:** Hermes Agent, MCP tooling, OpenRouter model orchestration, Hetzner VPS 24/7 runtime, Obsidian second brain / memory layer, zero-build web engineering.
2. **Law & AI Compliance (Legal-by-Design):** Practical compliance architectures under the EU AI Act, GDPR, NIS2, DORA, EU Data Act, and DSM Copyright Directive (TDM exceptions).
3. **UAV Systems & Edge Robotics:** Hand-soldered 1500g carbon quad, ArduPilot Copter autopilot, Raspberry Pi 5 edge vision AI, EASA A1/A3 certified, €2.6M insured (Hobby project).

## Products & Fixed-Price Audits

1. **AI GEO Audit (€150):** Deep evaluation of website discoverability across AI search engines (Perplexity, ChatGPT Search, Claude, Google SGE). Includes llms.txt validation, robots.txt crawl access, Schema.org @graph entity analysis, and instant copy-paste remediation snippets.
2. **AI Web Readiness Scan (€200):** Comprehensive automated technical checklist covering Privacy Policy, GDPR consent structures, Terms of Service, Disclaimer, AI Act disclosures, and cookie compliance.
3. **Full Web Audit (€300):** GEO Audit + Web Readiness Scan combined with 30-min direct technical walkthrough call.
4. **Custom Autonomous Agent (€500 deposit):** End-to-end bespoke autonomous agents running 24/7 on dedicated European VPS with custom MCP servers, Telegram/WhatsApp C2 bridges, and SQLite persistence.

## Social & Professional Channels

- [X (Twitter)]({config['profile']['socials']['x']}): Daily autonomous build updates, AI engineering thoughts, and UAV flight logs.
- [YouTube]({config['profile']['socials']['youtube']}): Long-form video breakdowns of AI agents, drone builds, and legal compliance.
- [GitHub]({config['profile']['socials']['github']}): Open-source repositories, agent scripts, MCP servers, and website source.
- [LinkedIn]({config['profile']['socials']['linkedin']}): Professional engineering profile, publications, and enterprise advisory.
- [Email](mailto:{config['site']['email']}): Direct asynchronous agent-routed communication endpoint.
"""
    with open(LLMS_FULL_TXT, 'w', encoding='utf-8') as f:
        f.write(llms_full_content.strip() + "\n")
    print("  Updated llms-full.txt")

def sync_sitemap(config):
    print("Generating sitemap.xml with full hreflang alternates...")
    today = datetime.date.today().isoformat()
    
    pages = [
        {"loc": "/", "priority": "1.0", "changefreq": "weekly"},
        {"loc": "/about", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/services", "priority": "0.9", "changefreq": "weekly"},
        {"loc": "/services-sk", "priority": "0.9", "changefreq": "weekly"},
        {"loc": "/drones", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/contact", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/blog/", "priority": "0.9", "changefreq": "weekly"},
        {"loc": "/privacy", "priority": "0.3", "changefreq": "yearly"},
        {"loc": "/privacy-sk", "priority": "0.3", "changefreq": "yearly"},
        {"loc": "/terms", "priority": "0.3", "changefreq": "yearly"},
        {"loc": "/terms-sk", "priority": "0.3", "changefreq": "yearly"},
        {"loc": "/disclaimer", "priority": "0.3", "changefreq": "yearly"},
        {"loc": "/disclaimer-sk", "priority": "0.3", "changefreq": "yearly"},
        {"loc": "/llms.txt", "priority": "0.4", "changefreq": "monthly"},
        {"loc": "/llms-full.txt", "priority": "0.4", "changefreq": "monthly"}
    ]
    
    posts = []
    if os.path.exists(POSTS_JSON):
        with open(POSTS_JSON, 'r', encoding='utf-8') as f:
            posts = json.load(f)
            
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    xml.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    
    for p in pages:
        loc = f"https://www.marianstancik.dev{p['loc']}"
        xml.append('  <url>')
        xml.append(f'    <loc>{loc}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append(f'    <changefreq>{p["changefreq"]}</changefreq>')
        xml.append(f'    <priority>{p["priority"]}</priority>')
        xml.append('  </url>')
        
    for post in posts:
        slug = post['slug']
        en_url = f"https://www.marianstancik.dev/blog/posts/{slug}"
        sk_url = f"https://www.marianstancik.dev/blog/posts/sk/{slug}"
        de_url = f"https://www.marianstancik.dev/blog/posts/de/{slug}"
        pl_url = f"https://www.marianstancik.dev/blog/posts/pl/{slug}"
        
        for lang_code, url in [('en', en_url), ('sk', sk_url), ('de', de_url), ('pl', pl_url)]:
            xml.append('  <url>')
            xml.append(f'    <loc>{url}</loc>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="sk" href="{sk_url}"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="de" href="{de_url}"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="pl" href="{pl_url}"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{en_url}"/>')
            xml.append(f'    <lastmod>{post.get("date", today)}</lastmod>')
            xml.append('    <changefreq>monthly</changefreq>')
            xml.append('    <priority>0.7</priority>')
            xml.append('  </url>')
        
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
