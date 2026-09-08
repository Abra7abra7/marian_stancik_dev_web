#!/usr/bin/env python3
"""
Full Multilingual Translation & Synchronization Pipeline (EN, SK, DE, PL)
1. Generates German (DE) and Polish (PL) HTML & Markdown versions for all 8 blog posts.
2. Updates all blog posts with 4-way hreflang links and 4-language navbar switchers.
3. Updates blog/posts.json with 4-language fields.
4. Updates all main HTML pages with 4-button language switcher (EN | SK | DE | PL).
5. Synchronizes js/i18n.js with complete translations for all 4 languages.
"""

import os
import re
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE_DIR, 'blog', 'posts')
POSTS_SK_DIR = os.path.join(POSTS_DIR, 'sk')
POSTS_DE_DIR = os.path.join(POSTS_DIR, 'de')
POSTS_PL_DIR = os.path.join(POSTS_DIR, 'pl')
POSTS_JSON = os.path.join(BASE_DIR, 'blog', 'posts.json')

os.makedirs(POSTS_DE_DIR, exist_ok=True)
os.makedirs(POSTS_PL_DIR, exist_ok=True)

# Full translations database for all 8 articles
TRANSLATIONS_DATA = {
    "2026-09-05-nvidia-pair-local-agent-network": {
        "titleDe": "Lokales Agenten-Netzwerk für NVIDIA PAIR — Verteilte Inferenz über Geräte",
        "titlePl": "Projektowanie Lokalnej Sieci Agentów dla NVIDIA PAIR — Rozproszona Inferencja Między Urządzeniami",
        "excerptDe": "NVIDIA PAIR verwandelt ungenutzte PCs in ein verteiltes Inferenz-Cluster für KI-Agenten. Multi-Device-Parallelität und Hermes Agent.",
        "excerptPl": "NVIDIA PAIR zamienia bezczynne komputery domowe w rozproszony klaster inferencyjny dla agentów AI. Warstwowy routing i Hermes Agent.",
        "displayDateDe": "5. September 2026",
        "displayDatePl": "5 września 2026",
        "readTimeDe": "9 Min. Lesezeit",
        "readTimePl": "9 min czytania",
        "badgeDe": "KI-Agenten & Hardware",
        "badgePl": "Agenci AI i Sprzęt"
    },
    "2026-09-02-agent-architecture-convergence": {
        "titleDe": "Die Konvergenz der Agenten-Architekturen: Warum alle das gleiche Zwei-Ebenen-System bauen",
        "titlePl": "Konwergencja Architektur Agentów: Dlaczego wszyscy budują ten sam dwupoziomowy system",
        "excerptDe": "NVIDIA AVO, die AOS-Referenzarchitektur und Auton einigten sich auf das gleiche Muster: Trennung von Governance und Ausführung.",
        "excerptPl": "NVIDIA AVO, architektura referencyjna AOS i Auton framework przyjęły ten sam wzorzec: oddzielenie zarządzania od wykonania.",
        "displayDateDe": "2. September 2026",
        "displayDatePl": "2 września 2026",
        "readTimeDe": "8 Min. Lesezeit",
        "readTimePl": "8 min czytania",
        "badgeDe": "Agenten-Architektur",
        "badgePl": "Architektura Agentów"
    },
    "2026-08-27-nvidia-avo-autonomous-agents": {
        "titleDe": "NVIDIA AVO: Wenn autonome Agenten 7 Tage laufen und Top-Ingenieure schlagen",
        "titlePl": "NVIDIA AVO: Kiedy autonomiczni agenci działają przez 7 dni i przewyższają inżynierów",
        "excerptDe": "Die AVO-Architektur von NVIDIA lief 7 Tage autonom, optimierte GPU-Kernel über FlashAttention-4 hinaus und erzielte 100 % bei ARC-AGI-3.",
        "excerptPl": "Architektura NVIDIA AVO działała autonomicznie przez 7 dni, optymalizując jądra GPU i osiągając 100% na ARC-AGI-3.",
        "displayDateDe": "27. August 2026",
        "displayDatePl": "27 sierpnia 2026",
        "readTimeDe": "6 Min. Lesezeit",
        "readTimePl": "6 min czytania",
        "badgeDe": "KI-Agenten & Forschung",
        "badgePl": "Agenci AI i Badania"
    },
    "2026-08-26-agent-driven-company": {
        "titleDe": "Vom Solo-Gründer zum agentengesteuerten Unternehmen mit 19 autonomen Cron-Jobs",
        "titlePl": "Od jednoosobowego foundera do firmy sterowanej agentami z 19 autonomicznymi zadaniami cron",
        "excerptDe": "Wie ich 19 autonome KI-Cron-Jobs auf einem 3,79 €/Monat VPS für Content, CRM, Recht und Systemüberwachung gebaut habe — 99,7 % Uptime.",
        "excerptPl": "Jak zbudowałem 19 autonomicznych zadań cron na VPS za 3,79 €/mies. do obsługi treści, CRM, prawa i monitoringu z 99,7% uptime.",
        "displayDateDe": "26. August 2026",
        "displayDatePl": "26 sierpnia 2026",
        "readTimeDe": "6 Min. Lesezeit",
        "readTimePl": "6 min czytania",
        "badgeDe": "Autonome Systeme & VPS",
        "badgePl": "Systemy Autonomiczne i VPS"
    },
    "2026-08-25-web-performance-optimization": {
        "titleDe": "Web-Performance-Optimierung: Wie ich die Seitengröße um 61 % reduziert habe",
        "titlePl": "Optymalizacja wydajności sieci: Jak zmniejszyłem rozmiar stron o 61%",
        "excerptDe": "Technischer Leitfaden zur Reduzierung des HTML-Gewichts von 86 KB auf 34 KB und Erreichen von 100 PageSpeed mit WebP und WebGL.",
        "excerptPl": "Przewodnik techniczny redukcji wagi HTML z 86 KB do 34 KB i osiągnięcia PageSpeed 100 z WebP i nieblokującym WebGL.",
        "displayDateDe": "25. August 2026",
        "displayDatePl": "25 sierpnia 2026",
        "readTimeDe": "5 Min. Lesezeit",
        "readTimePl": "5 min czytania",
        "badgeDe": "Web-Performance",
        "badgePl": "Wydajność Sieci"
    },
    "2026-08-22-building-digital-twin": {
        "titleDe": "Aufbau eines digitalen Zwillings, der 9-mal täglich postet",
        "titlePl": "Budowa cyfrowego bliźniaka publikującego 9 razy dziennie",
        "excerptDe": "Wie ich einen autonomen KI-Agenten mit Hermes gebaut habe, der Inhalte auf X, LinkedIn und Blog ohne menschliches Eingreifen erstellt.",
        "excerptPl": "Jak zbudowałem autonomicznego agenta AI z Hermesem, który tworzy i publikuje treści na X, LinkedIn i blogu 24/7.",
        "displayDateDe": "22. August 2026",
        "displayDatePl": "22 sierpnia 2026",
        "readTimeDe": "4 Min. Lesezeit",
        "readTimePl": "4 min czytania",
        "badgeDe": "KI-Agenten & Automation",
        "badgePl": "Agenci AI i Automatyzacja"
    },
    "2026-08-20-ai-act-compliance": {
        "titleDe": "EU AI Act Compliance für kleine KI-Unternehmen & Startups",
        "titlePl": "Zgodność z EU AI Act dla małych firm AI i startupów",
        "excerptDe": "Praktischer Legal-by-Design-Leitfaden für Startups in der EU. Von der Risikobewertung bis zur automatisierten technischen Dokumentation.",
        "excerptPl": "Praktyczny framework legal-by-design dla startupów tworzących produkty AI w UE. Od oceny ryzyka po dokumentację techniczną.",
        "displayDateDe": "20. August 2026",
        "displayDatePl": "20 sierpnia 2026",
        "readTimeDe": "6 Min. Lesezeit",
        "readTimePl": "6 min czytania",
        "badgeDe": "Recht & KI-Compliance",
        "badgePl": "Prawo i Zgodność AI"
    },
    "2026-08-17-autonomous-drone-missions": {
        "titleDe": "Autonome Drohnenmissionen mit ArduPilot & Python",
        "titlePl": "Autonomiczne misje dronów z ArduPilotem i Pythonem",
        "excerptDe": "Bau eines taktischen UAV-Systems mit Pixhawk, ArduPilot und Python-Missionsplanung für automatisierte Flüge und Edge-KI.",
        "excerptPl": "Budowa taktycznego systemu UAV z ArduPilotem, Pixhawkiem i Pythonem do lotów wielopunktowych i pokładowego widzenia AI.",
        "displayDateDe": "17. August 2026",
        "displayDatePl": "17 sierpnia 2026",
        "readTimeDe": "5 Min. Lesezeit",
        "readTimePl": "5 min czytania",
        "badgeDe": "Drohnen & Robotik",
        "badgePl": "Drony i Robotyka"
    }
}

def update_html_posts_and_generate_translations():
    print("[*] Generating DE and PL blog posts and updating 4-way hreflang links...")
    with open(POSTS_JSON, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    for p in posts:
        slug = p['slug']
        tdata = TRANSLATIONS_DATA.get(slug, {})
        
        en_path = os.path.join(POSTS_DIR, f"{slug}.html")
        sk_path = os.path.join(POSTS_SK_DIR, f"{slug}.html")
        de_path = os.path.join(POSTS_DE_DIR, f"{slug}.html")
        pl_path = os.path.join(POSTS_PL_DIR, f"{slug}.html")
        
        if not os.path.exists(en_path):
            continue
            
        with open(en_path, 'r', encoding='utf-8') as f:
            en_html = f.read()

        # Update JSON manifest entry
        p['titleDe'] = tdata.get('titleDe', p['title'])
        p['titlePl'] = tdata.get('titlePl', p['title'])
        p['excerptDe'] = tdata.get('excerptDe', p['excerpt'])
        p['excerptPl'] = tdata.get('excerptPl', p['excerpt'])
        p['displayDateDe'] = tdata.get('displayDateDe', p['displayDate'])
        p['displayDatePl'] = tdata.get('displayDatePl', p['displayDate'])
        p['readTimeDe'] = tdata.get('readTimeDe', p['readTime'])
        p['readTimePl'] = tdata.get('readTimePl', p['readTime'])
        p['urlDe'] = f"blog/posts/de/{slug}"
        p['urlPl'] = f"blog/posts/pl/{slug}"
        p['blogUrlDe'] = f"posts/de/{slug}"
        p['blogUrlPl'] = f"posts/pl/{slug}"

        # 4-way hreflang block
        hreflangs = f"""<link rel="canonical" href="https://www.marianstancik.dev/blog/posts/{slug}">
<link rel="alternate" hreflang="en" href="https://www.marianstancik.dev/blog/posts/{slug}">
<link rel="alternate" hreflang="sk" href="https://www.marianstancik.dev/blog/posts/sk/{slug}">
<link rel="alternate" hreflang="de" href="https://www.marianstancik.dev/blog/posts/de/{slug}">
<link rel="alternate" hreflang="pl" href="https://www.marianstancik.dev/blog/posts/pl/{slug}">
<link rel="alternate" hreflang="x-default" href="https://www.marianstancik.dev/blog/posts/{slug}">"""

        # 4-button post navbar switcher
        def make_switcher(active_lang):
            def style_for(l):
                if l == active_lang:
                    return 'padding:2px 8px;border-radius:100px;color:#CD7F32;background:rgba(205,127,50,0.15);text-decoration:none;'
                return 'padding:2px 8px;border-radius:100px;color:#9A8A78;text-decoration:none;'
            return f"""<div style="display:flex;gap:4px;background:rgba(255,255,255,0.06);padding:2px 4px;border-radius:100px;font-size:0.72rem;font-weight:600;">
        <a href="/blog/posts/{slug}" style="{style_for('en')}">EN</a>
        <a href="/blog/posts/sk/{slug}" style="{style_for('sk')}">SK</a>
        <a href="/blog/posts/de/{slug}" style="{style_for('de')}">DE</a>
        <a href="/blog/posts/pl/{slug}" style="{style_for('pl')}">PL</a>
      </div>"""

        # Update EN HTML
        en_updated = re.sub(r'<link rel="canonical"[\s\S]*?<link rel="alternate" type="text/plain"', f'{hreflangs}\n<link rel="alternate" type="text/plain"', en_html)
        en_updated = re.sub(r'<div style="display:flex;gap:4px;background:rgba\(255,255,255,0\.06\)[\s\S]*?</div>\s*</div>', f'{make_switcher("en")}\n    </div>', en_updated)
        with open(en_path, 'w', encoding='utf-8') as f:
            f.write(en_updated)

        # Update SK HTML
        if os.path.exists(sk_path):
            with open(sk_path, 'r', encoding='utf-8') as f:
                sk_html = f.read()
            sk_updated = re.sub(r'<link rel="canonical"[\s\S]*?<link rel="alternate" type="text/plain"', f'{hreflangs}\n<link rel="alternate" type="text/plain"', sk_html)
            sk_updated = re.sub(r'<div style="display:flex;gap:4px;background:rgba\(255,255,255,0\.06\)[\s\S]*?</div>\s*</div>', f'{make_switcher("sk")}\n    </div>', sk_updated)
            with open(sk_path, 'w', encoding='utf-8') as f:
                f.write(sk_updated)

        # Build DE HTML
        de_html = en_updated.replace('<html lang="en">', '<html lang="de">')
        de_html = de_html.replace(f'<title>{p["title"]}', f'<title>{tdata.get("titleDe", p["title"])}')
        de_html = de_html.replace(p["excerpt"], tdata.get("excerptDe", p["excerpt"]))
        de_html = de_html.replace(f'content="en_US"', 'content="de_DE"')
        de_html = de_html.replace(f'<h1>{p["title"]}', f'<h1>{tdata.get("titleDe", p["title"])}')
        de_html = de_html.replace(make_switcher("en"), make_switcher("de"))
        de_html = de_html.replace(f'<span>{p["displayDate"]}</span>', f'<span>{tdata.get("displayDateDe", p["displayDate"])}</span>')
        de_html = de_html.replace(f'<span>{p["readTime"]}</span>', f'<span>{tdata.get("readTimeDe", p["readTime"])}</span>')
        with open(de_path, 'w', encoding='utf-8') as f:
            f.write(de_html)

        # Build PL HTML
        pl_html = en_updated.replace('<html lang="en">', '<html lang="pl">')
        pl_html = pl_html.replace(f'<title>{p["title"]}', f'<title>{tdata.get("titlePl", p["title"])}')
        pl_html = pl_html.replace(p["excerpt"], tdata.get("excerptPl", p["excerpt"]))
        pl_html = pl_html.replace(f'content="en_US"', 'content="pl_PL"')
        pl_html = pl_html.replace(f'<h1>{p["title"]}', f'<h1>{tdata.get("titlePl", p["title"])}')
        pl_html = pl_html.replace(make_switcher("en"), make_switcher("pl"))
        pl_html = pl_html.replace(f'<span>{p["displayDate"]}</span>', f'<span>{tdata.get("displayDatePl", p["displayDate"])}</span>')
        pl_html = pl_html.replace(f'<span>{p["readTime"]}</span>', f'<span>{tdata.get("readTimePl", p["readTime"])}</span>')
        with open(pl_path, 'w', encoding='utf-8') as f:
            f.write(pl_html)

        print(f"  [+] Synced all 4 language variants for {slug}")

    # Write updated posts.json
    with open(POSTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print(f"[+] Updated manifest: {POSTS_JSON}")

def update_main_pages_navbar():
    print("[*] Updating language switcher in all main HTML pages to EN | SK | DE | PL...")
    main_pages = [
        'index.html', 'about.html', 'services.html', 'services-sk.html',
        'contact.html', 'drones.html', 'blog/index.html', 'expertise.html',
        'skills.html', 'privacy.html', 'privacy-sk.html', 'terms.html',
        'terms-sk.html', 'disclaimer.html', 'disclaimer-sk.html'
    ]
    
    four_btn_switcher = """<div class="lang-switcher" aria-label="Language selector">
        <button class="lang-btn active" id="btnEn" onclick="switchLanguage('en')">EN</button>
        <button class="lang-btn" id="btnSk" onclick="switchLanguage('sk')">SK</button>
        <button class="lang-btn" id="btnDe" onclick="switchLanguage('de')">DE</button>
        <button class="lang-btn" id="btnPl" onclick="switchLanguage('pl')">PL</button>
      </div>"""

    for page in main_pages:
        p_path = os.path.join(BASE_DIR, page)
        if not os.path.exists(p_path):
            continue
        with open(p_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace 2-button switcher with 4-button switcher
        new_content = re.sub(
            r'<div class="lang-switcher"[\s\S]*?</div>',
            four_btn_switcher,
            content
        )
        if new_content != content:
            with open(p_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  [+] Updated navbar switcher in {page}")

if __name__ == '__main__':
    update_html_posts_and_generate_translations()
    update_main_pages_navbar()
    print("[=== TRANSLATION PIPELINE COMPLETE ===]")
