#!/usr/bin/env python3
"""Regenerate sitemap.xml — www domain, all pages, SK variants"""
import os
import sys
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DOMAIN = "https://www.marianstancik.dev"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def page(url, lastmod, changefreq="monthly", priority=0.7):
    return f"""  <url>
    <loc>{DOMAIN}{url}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""

def get_lastmod(filepath):
    stat = os.stat(filepath)
    dt = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d")

pages = []

# Core pages
pages.append(page("/", get_lastmod(f"{ROOT}/index.html"), "weekly", 1.0))
pages.append(page("/blog", get_lastmod(f"{ROOT}/blog/index.html"), "weekly", 0.9))
pages.append(page("/about", get_lastmod(f"{ROOT}/about.html"), "monthly", 0.8))
pages.append(page("/expertise", get_lastmod(f"{ROOT}/expertise.html"), "monthly", 0.8))
pages.append(page("/skills", get_lastmod(f"{ROOT}/skills.html"), "monthly", 0.8))
pages.append(page("/services", get_lastmod(f"{ROOT}/services.html"), "monthly", 0.8))
pages.append(page("/services-sk", get_lastmod(f"{ROOT}/services-sk.html"), "monthly", 0.8))
pages.append(page("/drones", get_lastmod(f"{ROOT}/drones.html"), "monthly", 0.8))
pages.append(page("/contact", get_lastmod(f"{ROOT}/contact.html"), "monthly", 0.7))
pages.append(page("/privacy", get_lastmod(f"{ROOT}/privacy.html"), "yearly", 0.3))
pages.append(page("/disclaimer", get_lastmod(f"{ROOT}/disclaimer.html"), "yearly", 0.3))
pages.append(page("/disclaimer-sk", get_lastmod(f"{ROOT}/disclaimer-sk.html"), "yearly", 0.3))
pages.append(page("/privacy-sk", get_lastmod(f"{ROOT}/privacy-sk.html"), "yearly", 0.3))
pages.append(page("/terms", get_lastmod(f"{ROOT}/terms.html"), "yearly", 0.5))
pages.append(page("/terms-sk", get_lastmod(f"{ROOT}/terms-sk.html"), "yearly", 0.5))

# Blog posts EN
posts_dir = f"{ROOT}/blog/posts"
for fname in sorted(os.listdir(posts_dir), reverse=True):
    if fname.endswith(".html") and not fname.startswith("."):
        slug = fname.replace(".html", "")
        pages.append(page(f"/blog/posts/{slug}", get_lastmod(f"{posts_dir}/{fname}"), "monthly", 0.7))

# Blog posts SK
sk_dir = f"{ROOT}/blog/posts/sk"
for fname in sorted(os.listdir(sk_dir), reverse=True):
    if fname.endswith(".html") and not fname.startswith("."):
        slug = fname.replace(".html", "")
        pages.append(page(f"/blog/posts/sk/{slug}", get_lastmod(f"{sk_dir}/{fname}"), "monthly", 0.7))

# AI assets
pages.append(page("/llms.txt", get_lastmod(f"{ROOT}/llms.txt"), "monthly", 0.3))
pages.append(page("/llms-full.txt", get_lastmod(f"{ROOT}/llms-full.txt"), "monthly", 0.3))

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(pages)}
</urlset>
"""

with open(f"{ROOT}/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"✅ Sitemap generated: {len(pages)} URLs")
print(f"   Domain: {DOMAIN}")
for p in pages:
    loc = p.split("<loc>")[1].split("</loc>")[0] if "<loc>" in p else "?"
    print(f"   - {loc}")