#!/usr/bin/env python3
"""
Hermes Agent — Dual-Language Autonomous Blog Publisher & Indexing Pipeline
Generates synchronized EN + SK articles with hreflang tags, updates sitemap.xml,
manifests (posts.json, llms.txt), and triggers instant IndexNow pings.

Usage:
    python scripts/publish_post.py \\
        --title "Edge AI on Raspberry Pi 5 with ArduPilot" \\
        --title-sk "Edge AI na Raspberry Pi 5 s ArduPilotom" \\
        --excerpt "Deploying neural computer vision models on custom UAVs for real-time target tracking." \\
        --excerpt-sk "Nasadenie neurónových modelov počítačového videnia na UAV drony pre autonómne sledovanie cieľov." \\
        --tags "Drones, Edge AI, Raspberry Pi 5, ArduPilot" \\
        --read-time "5 min read" \\
        --read-time-sk "5 min čítania" \\
        --content-file "path/to/content_en.html" \\
        --content-file-sk "path/to/content_sk.html" \\
        [--push] [--dry-run]
"""

import os
import sys
import json
import argparse
import datetime
import re
import urllib.request
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE_DIR, 'blog', 'posts')
POSTS_SK_DIR = os.path.join(BASE_DIR, 'blog', 'posts', 'sk')
POSTS_DE_DIR = os.path.join(BASE_DIR, 'blog', 'posts', 'de')
POSTS_PL_DIR = os.path.join(BASE_DIR, 'blog', 'posts', 'pl')
POSTS_JSON = os.path.join(BASE_DIR, 'blog', 'posts.json')
SITEMAP_XML = os.path.join(BASE_DIR, 'sitemap.xml')
LLMS_TXT = os.path.join(BASE_DIR, 'llms.txt')
LLMS_FULL_TXT = os.path.join(BASE_DIR, 'llms-full.txt')

HTML_TEMPLATE_EN = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Marian Stancik</title>
<meta name="description" content="{excerpt}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="https://www.marianstancik.dev/blog/posts/{slug}">
<link rel="alternate" hreflang="en" href="https://www.marianstancik.dev/blog/posts/{slug}">
<link rel="alternate" hreflang="sk" href="https://www.marianstancik.dev/blog/posts/sk/{slug}">
<link rel="alternate" hreflang="de" href="https://www.marianstancik.dev/blog/posts/de/{slug}">
<link rel="alternate" hreflang="pl" href="https://www.marianstancik.dev/blog/posts/pl/{slug}">
<link rel="alternate" hreflang="x-default" href="https://www.marianstancik.dev/blog/posts/{slug}">
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
<meta property="og:url" content="https://www.marianstancik.dev/blog/posts/{slug}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://www.marianstancik.dev/profile.webp">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="800">
<meta property="og:image:alt" content="{title}">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="sk_SK">
<meta property="og:locale:alternate" content="de_DE">
<meta property="og:locale:alternate" content="pl_PL">
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
      "headline": "{title}",
      "description": "{excerpt}",
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
      "mainEntityOfPage": "https://www.marianstancik.dev/blog/posts/{slug}",
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
          "name": "Home",
          "item": "https://www.marianstancik.dev/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "https://www.marianstancik.dev/blog"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{title}",
          "item": "https://www.marianstancik.dev/blog/posts/{slug}"
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
</head>
<body>

<nav aria-label="Blog navigation">
  <div class="nav-inner">
    <a href="/" aria-label="Marian Stancik home"><span style="font-size:1.1rem">←</span> Home</a>
    <div style="display:flex;align-items:center;gap:16px;">
      <a href="/blog">Blog</a>
      <div style="display:flex;gap:4px;background:rgba(255,255,255,0.06);padding:2px 4px;border-radius:100px;font-size:0.72rem;font-weight:600;">
        <a href="/blog/posts/{slug}" style="padding:2px 8px;border-radius:100px;color:#CD7F32;background:rgba(205,127,50,0.15);text-decoration:none;">EN</a>
        <a href="/blog/posts/sk/{slug}" style="padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;">SK</a>
        <a href="/blog/posts/de/{slug}" style="padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;">DE</a>
        <a href="/blog/posts/pl/{slug}" style="padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;">PL</a>
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
  <span>By Marian Stancik</span>
</div>

<h1>{title}</h1>

<div class="post-content">
{content}
</div>
</article>
</div>

<footer>
  <p>© {year} <a href="/">Marian Stancik</a> — <a href="/">www.marianstancik.dev</a></p>
</footer>
</body>
</html>
"""

HTML_TEMPLATE_SK = """<!DOCTYPE html>
<html lang="sk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_sk} — Marian Stancik</title>
<meta name="description" content="{excerpt_sk}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="https://www.marianstancik.dev/blog/posts/sk/{slug}">
<link rel="alternate" hreflang="en" href="https://www.marianstancik.dev/blog/posts/{slug}">
<link rel="alternate" hreflang="sk" href="https://www.marianstancik.dev/blog/posts/sk/{slug}">
<link rel="alternate" hreflang="de" href="https://www.marianstancik.dev/blog/posts/de/{slug}">
<link rel="alternate" hreflang="pl" href="https://www.marianstancik.dev/blog/posts/pl/{slug}">
<link rel="alternate" hreflang="x-default" href="https://www.marianstancik.dev/blog/posts/{slug}">
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM Knowledge Graph">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="theme-color" content="#08080F">

<!-- Open Graph -->
<meta property="og:title" content="{title_sk} — Marian Stancik">
<meta property="og:description" content="{excerpt_sk}">
<meta property="og:url" content="https://www.marianstancik.dev/blog/posts/sk/{slug}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://www.marianstancik.dev/profile.webp">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="800">
<meta property="og:image:alt" content="{title_sk}">
<meta property="og:locale" content="sk_SK">
<meta property="og:locale:alternate" content="en_US">
<meta property="og:locale:alternate" content="de_DE">
<meta property="og:locale:alternate" content="pl_PL">
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
      "headline": "{title_sk}",
      "description": "{excerpt_sk}",
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
      "mainEntityOfPage": "https://www.marianstancik.dev/blog/posts/sk/{slug}",
      "keywords": {tags_json}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Domov",
          "item": "https://www.marianstancik.dev/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "https://www.marianstancik.dev/blog"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{title_sk}",
          "item": "https://www.marianstancik.dev/blog/posts/sk/{slug}"
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
</head>
<body>

<nav aria-label="Navigácia blogu">
  <div class="nav-inner">
    <a href="/" aria-label="Marian Stancik domov"><span style="font-size:1.1rem">←</span> Domov</a>
    <div style="display:flex;align-items:center;gap:16px;">
      <a href="/blog">Blog</a>
      <div style="display:flex;gap:4px;background:rgba(255,255,255,0.06);padding:2px 4px;border-radius:100px;font-size:0.72rem;font-weight:600;">
        <a href="/blog/posts/{slug}" style="padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;">EN</a>
        <a href="/blog/posts/sk/{slug}" style="padding:2px 8px;border-radius:100px;color:#CD7F32;background:rgba(205,127,50,0.15);text-decoration:none;">SK</a>
        <a href="/blog/posts/de/{slug}" style="padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;">DE</a>
        <a href="/blog/posts/pl/{slug}" style="padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;">PL</a>
      </div>
    </div>
  </div>
</nav>

<div class="container">
<article>
<div class="post-meta">
  <span>{display_date_sk}</span>
  <span class="tag">{primary_tag}</span>
  <span>{read_time_sk}</span>
  <span>Marian Stancik</span>
</div>

<h1>{title_sk}</h1>

<div class="post-content">
{content_sk}
</div>
</article>
</div>

<footer>
  <p>© {year} <a href="/">Marian Stancik</a> — <a href="/">www.marianstancik.dev</a></p>
</footer>
</body>
</html>
"""

HTML_TEMPLATE_DE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_de} — Marian Stancik</title>
<meta name="description" content="{excerpt_de}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="https://www.marianstancik.dev/blog/posts/de/{slug}">
<link rel="alternate" hreflang="en" href="https://www.marianstancik.dev/blog/posts/{slug}">
<link rel="alternate" hreflang="sk" href="https://www.marianstancik.dev/blog/posts/sk/{slug}">
<link rel="alternate" hreflang="de" href="https://www.marianstancik.dev/blog/posts/de/{slug}">
<link rel="alternate" hreflang="pl" href="https://www.marianstancik.dev/blog/posts/pl/{slug}">
<link rel="alternate" hreflang="x-default" href="https://www.marianstancik.dev/blog/posts/{slug}">
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM Knowledge Graph">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="theme-color" content="#08080F">

<!-- Open Graph -->
<meta property="og:title" content="{title_de} — Marian Stancik">
<meta property="og:description" content="{excerpt_de}">
<meta property="og:url" content="https://www.marianstancik.dev/blog/posts/de/{slug}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://www.marianstancik.dev/profile.webp">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="800">
<meta property="og:image:alt" content="{title_de}">
<meta property="og:locale" content="de_DE">
<meta property="og:locale:alternate" content="en_US">
<meta property="og:locale:alternate" content="sk_SK">
<meta property="og:locale:alternate" content="pl_PL">
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
      "headline": "{title_de}",
      "description": "{excerpt_de}",
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
      "mainEntityOfPage": "https://www.marianstancik.dev/blog/posts/de/{slug}",
      "keywords": {tags_json}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Startseite",
          "item": "https://www.marianstancik.dev/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "https://www.marianstancik.dev/blog"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{title_de}",
          "item": "https://www.marianstancik.dev/blog/posts/de/{slug}"
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
</head>
<body>

<nav aria-label="Blog-Navigation">
  <div class="nav-inner">
    <a href="/" aria-label="Marian Stancik Startseite"><span style="font-size:1.1rem">←</span> Startseite</a>
    <div style="display:flex;align-items:center;gap:16px;">
      <a href="/blog">Blog</a>
      <div style="display:flex;gap:4px;background:rgba(255,255,255,0.06);padding:2px 4px;border-radius:100px;font-size:0.72rem;font-weight:600;">
        <a href="/blog/posts/{slug}" style="padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;">EN</a>
        <a href="/blog/posts/sk/{slug}" style="padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;">SK</a>
        <a href="/blog/posts/de/{slug}" style="padding:2px 8px;border-radius:100px;color:#CD7F32;background:rgba(205,127,50,0.15);text-decoration:none;">DE</a>
        <a href="/blog/posts/pl/{slug}" style="padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;">PL</a>
      </div>
    </div>
  </div>
</nav>

<div class="container">
<article>
<div class="post-meta">
  <span>{display_date_de}</span>
  <span class="tag">{primary_tag}</span>
  <span>{read_time_de}</span>
  <span>Marian Stancik</span>
</div>

<h1>{title_de}</h1>

<div class="post-content">
{content_de}
</div>
</article>
</div>

<footer>
  <p>© {year} <a href="/">Marian Stancik</a> — <a href="/">www.marianstancik.dev</a></p>
</footer>
</body>
</html>
"""

HTML_TEMPLATE_PL = """<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_pl} — Marian Stancik</title>
<meta name="description" content="{excerpt_pl}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="https://www.marianstancik.dev/blog/posts/pl/{slug}">
<link rel="alternate" hreflang="en" href="https://www.marianstancik.dev/blog/posts/{slug}">
<link rel="alternate" hreflang="sk" href="https://www.marianstancik.dev/blog/posts/sk/{slug}">
<link rel="alternate" hreflang="de" href="https://www.marianstancik.dev/blog/posts/de/{slug}">
<link rel="alternate" hreflang="pl" href="https://www.marianstancik.dev/blog/posts/pl/{slug}">
<link rel="alternate" hreflang="x-default" href="https://www.marianstancik.dev/blog/posts/{slug}">
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM Knowledge Graph">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="theme-color" content="#08080F">

<!-- Open Graph -->
<meta property="og:title" content="{title_pl} — Marian Stancik">
<meta property="og:description" content="{excerpt_pl}">
<meta property="og:url" content="https://www.marianstancik.dev/blog/posts/pl/{slug}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://www.marianstancik.dev/profile.webp">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="800">
<meta property="og:image:alt" content="{title_pl}">
<meta property="og:locale" content="pl_PL">
<meta property="og:locale:alternate" content="en_US">
<meta property="og:locale:alternate" content="sk_SK">
<meta property="og:locale:alternate" content="de_DE">
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
      "headline": "{title_pl}",
      "description": "{excerpt_pl}",
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
      "mainEntityOfPage": "https://www.marianstancik.dev/blog/posts/pl/{slug}",
      "keywords": {tags_json}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Strona główna",
          "item": "https://www.marianstancik.dev/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "https://www.marianstancik.dev/blog"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{title_pl}",
          "item": "https://www.marianstancik.dev/blog/posts/pl/{slug}"
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
</head>
<body>

<nav aria-label="Nawigacja bloga">
  <div class="nav-inner">
    <a href="/" aria-label="Marian Stancik Strona główna"><span style="font-size:1.1rem">←</span> Strona główna</a>
    <div style="display:flex;align-items:center;gap:16px;">
      <a href="/blog">Blog</a>
      <div style="display:flex;gap:4px;background:rgba(255,255,255,0.06);padding:2px 4px;border-radius:100px;font-size:0.72rem;font-weight:600;">
        <a href="/blog/posts/{slug}" style="padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;">EN</a>
        <a href="/blog/posts/sk/{slug}" style="padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;">SK</a>
        <a href="/blog/posts/de/{slug}" style="padding:2px 8px;border-radius:100px;color:#8888A0;text-decoration:none;">DE</a>
        <a href="/blog/posts/pl/{slug}" style="padding:2px 8px;border-radius:100px;color:#CD7F32;background:rgba(205,127,50,0.15);text-decoration:none;">PL</a>
      </div>
    </div>
  </div>
</nav>

<div class="container">
<article>
<div class="post-meta">
  <span>{display_date_pl}</span>
  <span class="tag">{primary_tag}</span>
  <span>{read_time_pl}</span>
  <span>Marian Stancik</span>
</div>

<h1>{title_pl}</h1>

<div class="post-content">
{content_pl}
</div>
</article>
</div>

<footer>
  <p>© {year} <a href="/">Marian Stancik</a> — <a href="/">www.marianstancik.dev</a></p>
</footer>
</body>
</html>
"""

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    return re.sub(r'[\s-]+', '-', text).strip('-')

def ping_search_engines(urls):
    """Pings Google Sitemap & IndexNow API for instant crawl and indexing."""
    print("[*] Triggering instant indexing pings...")
    
    # 1. Google Sitemap Ping
    try:
        sitemap_url = "https://www.marianstancik.dev/sitemap.xml"
        google_ping = f"https://www.google.com/ping?sitemap={sitemap_url}"
        req = urllib.request.Request(google_ping, headers={'User-Agent': 'MarianStancik-Publisher/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"    [+] Google Sitemap Ping OK ({response.status})")
    except Exception as e:
        print(f"    [!] Google Ping notice: {e}")

    # 2. IndexNow API Ping (Bing, Perplexity, Seznam, Yandex)
    try:
        indexnow_payload = json.dumps({
            "host": "www.marianstancik.dev",
            "key": "marianstancik-indexnow-key",
            "urlList": urls
        }).encode('utf-8')
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=indexnow_payload,
            headers={'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'MarianStancik-Publisher/1.0'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"    [+] IndexNow API Ping OK ({response.status})")
    except Exception as e:
        print(f"    [!] IndexNow notice: {e}")

def update_sitemap(slug):
    """Adds 4-language post entries to sitemap.xml if not present."""
    if not os.path.exists(SITEMAP_XML):
        return
    with open(SITEMAP_XML, 'r', encoding='utf-8') as f:
        content = f.read()

    en_loc = f"<loc>https://www.marianstancik.dev/blog/posts/{slug}</loc>"
    if en_loc in content:
        return

    today = datetime.date.today().strftime('%Y-%m-%d')
    new_entry = f"""  <url>
    <loc>https://www.marianstancik.dev/blog/posts/{slug}</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.marianstancik.dev/blog/posts/{slug}"/>
    <xhtml:link rel="alternate" hreflang="sk" href="https://www.marianstancik.dev/blog/posts/sk/{slug}"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://www.marianstancik.dev/blog/posts/de/{slug}"/>
    <xhtml:link rel="alternate" hreflang="pl" href="https://www.marianstancik.dev/blog/posts/pl/{slug}"/>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://www.marianstancik.dev/blog/posts/sk/{slug}</loc>
    <xhtml:link rel="alternate" hreflang="sk" href="https://www.marianstancik.dev/blog/posts/sk/{slug}"/>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.marianstancik.dev/blog/posts/{slug}"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://www.marianstancik.dev/blog/posts/de/{slug}"/>
    <xhtml:link rel="alternate" hreflang="pl" href="https://www.marianstancik.dev/blog/posts/pl/{slug}"/>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://www.marianstancik.dev/blog/posts/de/{slug}</loc>
    <xhtml:link rel="alternate" hreflang="de" href="https://www.marianstancik.dev/blog/posts/de/{slug}"/>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.marianstancik.dev/blog/posts/{slug}"/>
    <xhtml:link rel="alternate" hreflang="sk" href="https://www.marianstancik.dev/blog/posts/sk/{slug}"/>
    <xhtml:link rel="alternate" hreflang="pl" href="https://www.marianstancik.dev/blog/posts/pl/{slug}"/>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://www.marianstancik.dev/blog/posts/pl/{slug}</loc>
    <xhtml:link rel="alternate" hreflang="pl" href="https://www.marianstancik.dev/blog/posts/pl/{slug}"/>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.marianstancik.dev/blog/posts/{slug}"/>
    <xhtml:link rel="alternate" hreflang="sk" href="https://www.marianstancik.dev/blog/posts/sk/{slug}"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://www.marianstancik.dev/blog/posts/de/{slug}"/>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>"""

    content = content.replace("</urlset>", new_entry)
    with open(SITEMAP_XML, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[+] Updated sitemap.xml with 4-language endpoints for: {slug}")

def main():
    parser = argparse.ArgumentParser(description="Hermes Agent 4-Language Blog Publisher")
    parser.add_argument('--title', required=True, help="Article title (English)")
    parser.add_argument('--title-sk', help="Article title (Slovak)")
    parser.add_argument('--title-de', help="Article title (German)")
    parser.add_argument('--title-pl', help="Article title (Polish)")
    parser.add_argument('--excerpt', required=True, help="Article excerpt (English)")
    parser.add_argument('--excerpt-sk', help="Article excerpt (Slovak)")
    parser.add_argument('--excerpt-de', help="Article excerpt (German)")
    parser.add_argument('--excerpt-pl', help="Article excerpt (Polish)")
    parser.add_argument('--tags', default="AI Agents, Tech", help="Comma-separated tags")
    parser.add_argument('--read-time', default="4 min read", help="Read time EN")
    parser.add_argument('--read-time-sk', default="4 min čítania", help="Read time SK")
    parser.add_argument('--read-time-de', default="4 Min. Lesezeit", help="Read time DE")
    parser.add_argument('--read-time-pl', default="4 min czytania", help="Read time PL")
    parser.add_argument('--content-file', help="Path to English HTML/MD content snippet")
    parser.add_argument('--content-file-sk', help="Path to Slovak HTML/MD content snippet")
    parser.add_argument('--content-file-de', help="Path to German HTML/MD content snippet")
    parser.add_argument('--content-file-pl', help="Path to Polish HTML/MD content snippet")
    parser.add_argument('--content-html', help="Raw English HTML content string")
    parser.add_argument('--content-html-sk', help="Raw Slovak HTML content string")
    parser.add_argument('--content-html-de', help="Raw German HTML content string")
    parser.add_argument('--content-html-pl', help="Raw Polish HTML content string")
    parser.add_argument('--date', help="Publish date YYYY-MM-DD (defaults to today)")
    parser.add_argument('--push', action='store_true', help="Automatically git commit and push to main")
    parser.add_argument('--dry-run', action='store_true', help="Simulate run without writing files")

    args = parser.parse_args()

    pub_date = args.date or datetime.date.today().strftime('%Y-%m-%d')
    dt = datetime.datetime.strptime(pub_date, '%Y-%m-%d')
    display_date = dt.strftime('%B %d, %Y')
    
    sk_months = {
        1: 'január', 2: 'február', 3: 'marec', 4: 'apríl',
        5: 'máj', 6: 'jún', 7: 'júl', 8: 'august',
        9: 'september', 10: 'október', 11: 'november', 12: 'december'
    }
    de_months = {
        1: 'Januar', 2: 'Februar', 3: 'März', 4: 'April',
        5: 'Mai', 6: 'Juni', 7: 'Juli', 8: 'August',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Dezember'
    }
    pl_months = {
        1: 'stycznia', 2: 'lutego', 3: 'marca', 4: 'kwietnia',
        5: 'maja', 6: 'czerwca', 7: 'lipca', 8: 'sierpnia',
        9: 'września', 10: 'października', 11: 'listopada', 12: 'grudnia'
    }

    display_date_sk = f"{dt.day}. {sk_months[dt.month]} {dt.year}"
    display_date_de = f"{dt.day}. {de_months[dt.month]} {dt.year}"
    display_date_pl = f"{dt.day} {pl_months[dt.month]} {dt.year}"
    year = str(dt.year)

    title_sk = args.title_sk or args.title
    title_de = args.title_de or args.title
    title_pl = args.title_pl or args.title

    excerpt_sk = args.excerpt_sk or args.excerpt
    excerpt_de = args.excerpt_de or args.excerpt
    excerpt_pl = args.excerpt_pl or args.excerpt

    title_slug = slugify(args.title)
    slug = f"{pub_date}-{title_slug}"
    html_filename = f"{slug}.html"
    
    html_filepath_en = os.path.join(POSTS_DIR, html_filename)
    html_filepath_sk = os.path.join(POSTS_SK_DIR, html_filename)
    html_filepath_de = os.path.join(POSTS_DE_DIR, html_filename)
    html_filepath_pl = os.path.join(POSTS_PL_DIR, html_filename)
    
    relative_url_en = f"blog/posts/{slug}"
    relative_url_sk = f"blog/posts/sk/{slug}"
    relative_url_de = f"blog/posts/de/{slug}"
    relative_url_pl = f"blog/posts/pl/{slug}"

    tags = [t.strip() for t in args.tags.split(',') if t.strip()]
    primary_tag = tags[0] if tags else "AI & Technology"

    # English content
    content_en = ""
    if args.content_file and os.path.exists(args.content_file):
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content_en = f.read()
    elif args.content_html:
        content_en = args.content_html
    else:
        content_en = f"<p><strong>{args.excerpt}</strong></p><p>Full technical analysis and implementation details.</p>"

    # Slovak content
    content_sk = ""
    if args.content_file_sk and os.path.exists(args.content_file_sk):
        with open(args.content_file_sk, 'r', encoding='utf-8') as f:
            content_sk = f.read()
    elif args.content_html_sk:
        content_sk = args.content_html_sk
    else:
        content_sk = f"<p><strong>{excerpt_sk}</strong></p><p>Kompletná technická analýza a detaily implementácie.</p>"

    # German content
    content_de = ""
    if args.content_file_de and os.path.exists(args.content_file_de):
        with open(args.content_file_de, 'r', encoding='utf-8') as f:
            content_de = f.read()
    elif args.content_html_de:
        content_de = args.content_html_de
    else:
        content_de = f"<p><strong>{excerpt_de}</strong></p><p>Vollständige technische Analyse und Implementierungsdetails.</p>"

    # Polish content
    content_pl = ""
    if args.content_file_pl and os.path.exists(args.content_file_pl):
        with open(args.content_file_pl, 'r', encoding='utf-8') as f:
            content_pl = f.read()
    elif args.content_html_pl:
        content_pl = args.content_html_pl
    else:
        content_pl = f"<p><strong>{excerpt_pl}</strong></p><p>Pełna analiza techniczna i szczegóły wdrożenia.</p>"

    html_out_en = HTML_TEMPLATE_EN.format(
        title=args.title,
        excerpt=args.excerpt,
        slug=slug,
        date=pub_date,
        display_date=display_date,
        read_time=args.read_time,
        primary_tag=primary_tag,
        tags_json=json.dumps(tags),
        content=content_en,
        year=year
    )

    html_out_sk = HTML_TEMPLATE_SK.format(
        title_sk=title_sk,
        excerpt_sk=excerpt_sk,
        slug=slug,
        date=pub_date,
        display_date_sk=display_date_sk,
        read_time_sk=args.read_time_sk,
        primary_tag=primary_tag,
        tags_json=json.dumps(tags),
        content_sk=content_sk,
        year=year
    )

    html_out_de = HTML_TEMPLATE_DE.format(
        title_de=title_de,
        excerpt_de=excerpt_de,
        slug=slug,
        date=pub_date,
        display_date_de=display_date_de,
        read_time_de=args.read_time_de,
        primary_tag=primary_tag,
        tags_json=json.dumps(tags),
        content_de=content_de,
        year=year
    )

    html_out_pl = HTML_TEMPLATE_PL.format(
        title_pl=title_pl,
        excerpt_pl=excerpt_pl,
        slug=slug,
        date=pub_date,
        display_date_pl=display_date_pl,
        read_time_pl=args.read_time_pl,
        primary_tag=primary_tag,
        tags_json=json.dumps(tags),
        content_pl=content_pl,
        year=year
    )

    new_post_entry = {
        "slug": slug,
        "url": relative_url_en,
        "urlSk": relative_url_sk,
        "urlDe": relative_url_de,
        "urlPl": relative_url_pl,
        "blogUrl": f"posts/{slug}",
        "blogUrlSk": f"posts/sk/{slug}",
        "blogUrlDe": f"posts/de/{slug}",
        "blogUrlPl": f"posts/pl/{slug}",
        "date": pub_date,
        "displayDate": display_date,
        "displayDateSk": display_date_sk,
        "displayDateDe": display_date_de,
        "displayDatePl": display_date_pl,
        "title": args.title,
        "titleSk": title_sk,
        "titleDe": title_de,
        "titlePl": title_pl,
        "excerpt": args.excerpt,
        "excerptSk": excerpt_sk,
        "excerptDe": excerpt_de,
        "excerptPl": excerpt_pl,
        "tags": tags,
        "readTime": args.read_time,
        "readTimeSk": args.read_time_sk,
        "readTimeDe": args.read_time_de,
        "readTimePl": args.read_time_pl
    }

    print(f"[*] Preparing 4-language article: {slug}")
    print(f"    - Title (EN): {args.title}")
    print(f"    - Title (SK): {title_sk}")
    print(f"    - Title (DE): {title_de}")
    print(f"    - Title (PL): {title_pl}")

    if args.dry_run:
        print("[!] DRY RUN mode — no files written.")
        print(f"JSON preview:\n{json.dumps(new_post_entry, indent=2, ensure_ascii=False)}")
        return

    if args.push and not args.dry_run:
        print("[*] Pulling latest changes from origin/main before publishing...")
        try:
            subprocess.run(["git", "pull", "origin", "main", "--rebase"], cwd=BASE_DIR, check=True)
        except Exception as e:
            print(f"[!] Warning: git pull failed: {e}")

    # 1. Write HTML article files in all 4 language directories
    os.makedirs(POSTS_DIR, exist_ok=True)
    os.makedirs(POSTS_SK_DIR, exist_ok=True)
    os.makedirs(POSTS_DE_DIR, exist_ok=True)
    os.makedirs(POSTS_PL_DIR, exist_ok=True)
    
    with open(html_filepath_en, 'w', encoding='utf-8') as f:
        f.write(html_out_en)
    print(f"[+] Created EN article: {html_filepath_en}")

    with open(html_filepath_sk, 'w', encoding='utf-8') as f:
        f.write(html_out_sk)
    print(f"[+] Created SK article: {html_filepath_sk}")

    with open(html_filepath_de, 'w', encoding='utf-8') as f:
        f.write(html_out_de)
    print(f"[+] Created DE article: {html_filepath_de}")

    with open(html_filepath_pl, 'w', encoding='utf-8') as f:
        f.write(html_out_pl)
    print(f"[+] Created PL article: {html_filepath_pl}")

    # Generate .md markdown alternates
    try:
        from sync_site import extract_markdown_from_html
        md_en = extract_markdown_from_html(html_out_en, args.title, pub_date, args.excerpt)
        with open(os.path.join(POSTS_DIR, f"{slug}.md"), 'w', encoding='utf-8') as f:
            f.write(md_en)
        md_sk = extract_markdown_from_html(html_out_sk, title_sk, pub_date, excerpt_sk)
        with open(os.path.join(POSTS_SK_DIR, f"{slug}.md"), 'w', encoding='utf-8') as f:
            f.write(md_sk)
        md_de = extract_markdown_from_html(html_out_de, title_de, pub_date, excerpt_de)
        with open(os.path.join(POSTS_DE_DIR, f"{slug}.md"), 'w', encoding='utf-8') as f:
            f.write(md_de)
        md_pl = extract_markdown_from_html(html_out_pl, title_pl, pub_date, excerpt_pl)
        with open(os.path.join(POSTS_PL_DIR, f"{slug}.md"), 'w', encoding='utf-8') as f:
            f.write(md_pl)
        print(f"[+] Created .md markdown alternates for all 4 languages: {slug}")
    except Exception as e:
        print(f"[!] Warning: Could not generate markdown alternates: {e}")

    # 2. Update blog/posts.json
    posts = []
    if os.path.exists(POSTS_JSON):
        with open(POSTS_JSON, 'r', encoding='utf-8') as f:
            try:
                posts = json.load(f)
            except Exception:
                posts = []
    
    posts = [p for p in posts if p.get('slug') != slug]
    posts.insert(0, new_post_entry)

    with open(POSTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print(f"[+] Updated manifest: {POSTS_JSON} ({len(posts)} total posts)")

    # 3. Update sitemap.xml
    update_sitemap(slug)

    # 4. Trigger full 4-language sync
    try:
        from sync_site import main as run_site_sync
        run_site_sync()
        print("[+] Triggered automatic 4-language sync and sitemap update")
    except Exception as e:
        print(f"[!] Warning: Site sync failed: {e}")

    # 5. Instant IndexNow Ping
    published_urls = [
        f"https://www.marianstancik.dev/{relative_url_en}",
        f"https://www.marianstancik.dev/{relative_url_sk}",
        f"https://www.marianstancik.dev/{relative_url_de}",
        f"https://www.marianstancik.dev/{relative_url_pl}"
    ]
    ping_search_engines(published_urls)

    # 6. Optional Git Commit & Push
    if args.push:
        print("[*] Executing git push to main...")
        subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)
        commit_msg = f"📝 auto(blog): publish 4-language {slug}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, check=True)
        print("[+] Published and deployed live (EN + SK + DE + PL) to origin/main.")
    else:
        print("[+] Files written locally. Ready for git push.")

if __name__ == '__main__':
    main()
