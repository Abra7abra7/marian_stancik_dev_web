#!/usr/bin/env python3
"""Regenerate sitemap.xml.

Delegates to scripts/sync_site.py::sync_sitemap so there is ONE sitemap generator:
per-language static pages (/en/, /sk/, /cs/, /de/, /pl/) with hreflang clusters,
legal pages and blog posts (only translations that really exist).
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_site import sync_sitemap, load_config  # noqa: E402

if __name__ == '__main__':
    sync_sitemap(load_config())
    print("✅ Sitemap generated via sync_site.sync_sitemap")
