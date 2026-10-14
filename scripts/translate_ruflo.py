#!/usr/bin/env python3
import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN_HTML = os.path.join(BASE_DIR, 'blog', 'posts', '2026-10-14-ruflo-queen-led-agent-swarms.html')
DE_HTML = os.path.join(BASE_DIR, 'blog', 'posts', 'de', '2026-10-14-ruflo-queen-led-agent-swarms.html')
PL_HTML = os.path.join(BASE_DIR, 'blog', 'posts', 'pl', '2026-10-14-ruflo-queen-led-agent-swarms.html')
POSTS_JSON = os.path.join(BASE_DIR, 'blog', 'posts.json')

with open(EN_HTML, 'r', encoding='utf-8') as f:
    en_content = f.read()

# Generate DE version
de_content = en_content
de_content = re.sub(r'<html lang="en">', '<html lang="de">', de_content)
de_content = re.sub(
    r'<title>.*? — Marian Stancik</title>',
    '<title>Ruflo, 74K Stars in 24 Stunden: Was Queen-Led Agent Swarms für Multi-Agenten-Architektur bedeuten — Marian Stancik</title>',
    de_content
)
de_content = re.sub(
    r'<meta name="description" content=".*?">',
    '<meta name="description" content="Cognitum One veröffentlichte Ruflo am 13. Oktober 2026 — 74.000 GitHub-Stars in 24 Stunden, 314 MCP-Tools, Queen-Led-Agentenschwärme. Architekturanalyse.">',
    de_content
)
de_content = re.sub(
    r'<link rel="canonical" href="https://www.marianstancik.dev/blog/posts/2026-10-14-ruflo-queen-led-agent-swarms">',
    '<link rel="canonical" href="https://www.marianstancik.dev/blog/posts/de/2026-10-14-ruflo-queen-led-agent-swarms">',
    de_content
)
de_content = re.sub(r'en_US', 'de_DE', de_content)
de_content = re.sub(r'11 min read', '11 Min. Lesezeit', de_content)
de_content = re.sub(r'October 14, 2026', '14. Oktober 2026', de_content)

with open(DE_HTML, 'w', encoding='utf-8') as f:
    f.write(de_content)

# Generate PL version
pl_content = en_content
pl_content = re.sub(r'<html lang="en">', '<html lang="pl">', pl_content)
pl_content = re.sub(
    r'<title>.*? — Marian Stancik</title>',
    '<title>Ruflo, 74 tys. gwiazdek w 24 godziny: Co roje agentów pod przywództwem królowej oznaczają dla architektury multi-agent — Marian Stancik</title>',
    pl_content
)
pl_content = re.sub(
    r'<meta name="description" content=".*?">',
    '<meta name="description" content="Cognitum One wydało Ruflo 13 października 2026 — 74 000 gwiazdek GitHub w 24 godziny, 314 narzędzi MCP, roje agentów sterowane przez królową. Analiza architektury.">',
    pl_content
)
pl_content = re.sub(
    r'<link rel="canonical" href="https://www.marianstancik.dev/blog/posts/2026-10-14-ruflo-queen-led-agent-swarms">',
    '<link rel="canonical" href="https://www.marianstancik.dev/blog/posts/pl/2026-10-14-ruflo-queen-led-agent-swarms">',
    pl_content
)
pl_content = re.sub(r'en_US', 'pl_PL', pl_content)
pl_content = re.sub(r'11 min read', '11 min czytania', pl_content)
pl_content = re.sub(r'October 14, 2026', '14 października 2026', pl_content)

with open(PL_HTML, 'w', encoding='utf-8') as f:
    f.write(pl_content)

# Update posts.json
with open(POSTS_JSON, 'r', encoding='utf-8') as f:
    posts = json.load(f)

for p in posts:
    if p["slug"] == "2026-10-14-ruflo-queen-led-agent-swarms":
        p["urlDe"] = "blog/posts/de/2026-10-14-ruflo-queen-led-agent-swarms"
        p["urlPl"] = "blog/posts/pl/2026-10-14-ruflo-queen-led-agent-swarms"
        p["blogUrlDe"] = "posts/de/2026-10-14-ruflo-queen-led-agent-swarms"
        p["blogUrlPl"] = "posts/pl/2026-10-14-ruflo-queen-led-agent-swarms"
        p["displayDateDe"] = "14. Oktober 2026"
        p["displayDatePl"] = "14 października 2026"
        p["titleDe"] = "Ruflo, 74K Stars in 24 Stunden: Was Queen-Led Agent Swarms für Multi-Agenten-Architektur bedeuten"
        p["titlePl"] = "Ruflo, 74 tys. gwiazdek w 24 godziny: Co roje agentów pod przywództwem królowej oznaczają dla architektury multi-agent"
        p["excerptDe"] = "Cognitum One veröffentlichte Ruflo am 13. Oktober 2026 — 74.000 GitHub-Stars in 24 Stunden, 314 MCP-Tools, Queen-Led-Agentenschwärme. Architekturanalyse."
        p["excerptPl"] = "Cognitum One wydało Ruflo 13 października 2026 — 74 000 gwiazdek GitHub w 24 godziny, 314 narzędzi MCP, roje agentów sterowane przez królową. Analiza architektury."
        p["readTimeDe"] = "11 Min. Lesezeit"
        p["readTimePl"] = "11 min czytania"
        break

with open(POSTS_JSON, 'w', encoding='utf-8') as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

print("Generated DE and PL versions successfully!")
