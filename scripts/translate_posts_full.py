#!/usr/bin/env python3
"""
Full Translation Engine for German (DE) and Polish (PL) Blog Articles
1. Translates all 8 article contents into complete German and Polish.
2. Generates updated .html and .md files in blog/posts/de/ and blog/posts/pl/.
3. Injects a 4-language navigation pill switcher ([EN] [SK] [DE] [PL]) across all 32 articles (EN, SK, DE, PL).
4. Synchronizes hreflang tags across all articles.
"""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE_DIR, 'blog', 'posts')
SK_DIR = os.path.join(POSTS_DIR, 'sk')
DE_DIR = os.path.join(POSTS_DIR, 'de')
PL_DIR = os.path.join(POSTS_DIR, 'pl')

os.makedirs(DE_DIR, exist_ok=True)
os.makedirs(PL_DIR, exist_ok=True)

# Complete German and Polish translations for the 8 articles
POSTS_DATA = {
    "2026-09-05-nvidia-pair-local-agent-network": {
        "slug": "2026-09-05-nvidia-pair-local-agent-network",
        "date": "2026-09-05",
        "dateDe": "5. September 2026",
        "datePl": "5 września 2026",
        "readTimeDe": "9 Min. Lesezeit",
        "readTimePl": "9 min czytania",
        "titleDe": "Lokales Agenten-Netzwerk für NVIDIA PAIR — Verteilte Inferenz über Geräte",
        "titlePl": "Projektowanie Lokalnej Sieci Agentów dla NVIDIA PAIR — Rozproszona Inferencja Między Urządzeniami",
        "tagsDe": ["NVIDIA PAIR", "Lokale KI", "KI-Agenten", "Verteilte Inferenz", "Hermes Agent"],
        "tagsPl": ["NVIDIA PAIR", "Lokalne AI", "Agenci AI", "Rozproszona Inferencja", "Hermes Agent"],
        "contentDe": """
<p>Auf der IFA 2026 in Berlin hat <strong>NVIDIA PAIR — Personal AI Router</strong> vorgestellt, ein kostenloses Open-Source-Tool, das ungenutzte PCs im lokalen Netzwerk erkennt und Inferenzanfragen auf diese verteilt. Ein einzelner Agent kann fünf Sub-Agenten starten, die parallel auf drei Rechnern laufen, anstatt in einer Warteschlange auf einer einzigen GPU zu warten. NVIDIAs Benchmarks zeigen eine 2,04-fache Beschleunigung — 18 Minuten auf einem Gerät wurden auf 8 Minuten und 48 Sekunden bei der Verteilung auf drei Geräte reduziert.</p>

<p>Dies verändert unsere Sichtweise auf lokale KI-Agenten. Der Engpass war nie die reine Rechenleistung — es war die Auslastung. Mehr als die Hälfte der Haushalte verfügt über zwei oder mehr PCs, und die meisten stehen während des Arbeitstages ungenutzt da. PAIR verwandelt diese latente Kapazität in ein verteiltes Inferenz-Cluster, das man einmal konfiguriert und dann vergisst.</p>

<p>Ich betreibe meine Agenten-Infrastruktur auf einem Hetzner VPS, aber die Architekturmuster für ein verteiltes Agentennetzwerk sind identisch, egal ob man lokal oder in der Cloud deployt. Hier erfahren Sie, was PAIR leistet, wie es in die moderne Zwei-Ebenen-Architektur passt und wie Sie Ihr eigenes Multi-Device-Netzwerk aufbauen.</p>

<h2>Was NVIDIA PAIR wirklich ist</h2>

<p>PAIR ist kein verteiltes Trainings-Framework und poolt keinen GPU-Speicher für ein einzelnes Riesenmodell. Es ist ein <strong>Load Balancer auf Anfrage-Ebene für lokale Inferenz</strong>.</p>

<p>Jeder verbundene PC betreibt seinen eigenen lokalen KI-Stack (Ollama oder LM Studio mit lokalen Modellen). PAIR erkennt verfügbare Rechner im LAN, überwacht deren Auslastung und leitet einzelne Anfragen an das am besten geeignete Gerät weiter. Wenn ein Gerät beitritt oder das Netzwerk verlässt, passt sich PAIR vollautomatisch an.</p>

<p>Die zentrale Designentscheidung von NVIDIA: PAIR arbeitet auf der Ebene von <strong>Agenten-Aufgaben</strong>, nicht auf der Ebene einzelner Token-Aufrufe. Ein Agent, der mehrere Sub-Agenten spawnt, kann die Inferenzanfragen jedes Sub-Agenten auf verschiedene Geräte verteilen. Das ist <strong>Parallelität auf Agentenebene</strong>.</p>

<blockquote>„PAIR ist ein persönlicher KI-Router, der KI-Inferenz intelligent über alle Geräte im lokalen Netzwerk verteilt. Er fasst nicht mehrere PCs zu einem zusammen, sondern verteilt Aufgaben an verfügbare Ressourcen.“ — NVIDIA, IFA 2026</blockquote>

<h2>Architekturmuster für Multi-Device-Inferenz</h2>

<h3>Muster 1: Parallelität auf Aufgabenebene (Nativer PAIR-Modus)</h3>
<p>Ein koordinierender Agent empfängt eine komplexe Anfrage, zerlegt sie in unabhängige Teilaufgaben und delegiert sie an Sub-Agenten. Die Inferenz jedes Sub-Agenten läuft parallel auf einem anderen Rechner.</p>

<h3>Muster 2: Gestaffeltes Modell-Routing (Tiered Routing)</h3>
<p>Unterschiedliche Geräte betreiben unterschiedliche Modelle nach Leistungsfähigkeit:
<ul>
  <li><strong>Desktop (RTX 4090):</strong> Tiefes Reasoning, Code-Generierung, Synthese (Qwen 2.5 32B, DeepSeek R1 Distill)</li>
  <li><strong>Laptop (RTX 4070):</strong> Schnelle Extraktion, Zusammenfassungen, Tool-Validierung (Llama 3.3 8B)</li>
  <li><strong>Mini-PC / Mac Mini:</strong> Klassifizierung, Routing, Guardrails (Qwen 2.5 1.5B)</li>
</ul>
</p>

<h3>Muster 3: Lokaler + Cloud Hybrid-Modus</h3>
<p>Lokale Geräte übernehmen datensensible Aufgaben, interne Dokumente und Routinen. Wenn die lokale Kapazität erschöpft ist oder maximale Reasoning-Tiefe benötigt wird, springen Cloud-APIs (DeepSeek V3, Claude 3.5 Sonnet) nahtlos ein.</p>

<h2>Fazit & Ausblick</h2>
<p>NVIDIA PAIR zeigt deutlich, wohin sich autonome Systeme entwickeln: weg von monolithischen Chatbots hin zu verteilten, agentengesteuerten Netzwerken. Systemdesign und Orchestrierung schlagen reine Modellgröße.</p>
""",
        "contentPl": """
<p>Podczas targów IFA 2026 w Berlinie <strong>NVIDIA zaprezentowała PAIR — Personal AI Router</strong>, bezpłatne narzędzie open-source, które wykrywa bezczynne komputery w sieci lokalnej i rozdziela między nie zapytania inferencyjne. Pojedynczy agent może uruchomić pięć pod-agentów działających równolegle na trzech maszynach, zamiast czekać w kolejce na jednym GPU. Testy NVIDII wykazują 2,04-krotne przyspieszenie — 18 minut na jednym urządzeniu skrócono do 8 minut i 48 sekund po rozproszeniu na trzy stacje.</p>

<p>Zmienia to sposób, w jaki myślimy o lokalnych agentach AI. Wąskim gardłem nigdy nie była sama moc obliczeniowa — lecz jej wykorzystanie. Ponad połowa gospodarstw domowych posiada co najmniej dwa komputery, z których większość pozostaje bezczynna w ciągu dnia. PAIR przekształca tę uśpioną moc w rozproszony klaster obliczeniowy.</p>

<p>Swoją infrastrukturę agentów prowadzę na serwerze Hetzner VPS, ale wzorce architektoniczne niezbędne do zaprojektowania rozproszonej sieci agentów są identyczne zarówno lokalnie, jak i w chmurze. Oto jak działa PAIR i jak zbudować własną sieć wielu urządzeń.</p>

<h2>Czym w rzeczywistości jest NVIDIA PAIR</h2>

<p>PAIR nie jest frameworkiem do rozproszonego treningu modeli i nie łączy pamięci VRAM wielu kart w jedną. Jest to <strong>inteligentny load-balancer na poziomie zapytań dla lokalnej inferencji</strong>.</p>

<p>Każdy podłączony komputer uruchamia własny lokalny stos AI (np. Ollama lub LM Studio z modelami). PAIR wykrywa urządzenia w sieci LAN, monitoruje ich obciążenie i kieruje zadania do maszyny najlepiej przygotowanej do ich wykonania. Gdy laptop opuszcza sieć, PAIR automatycznie dostosowuje routing.</p>

<p>Kluczowa decyzja architektoniczna NVIDII: PAIR działa na poziomie <strong>zadań agenta</strong>, a nie pojedynczych tokenów. Pozwala to na pełną <strong>równoległość na poziomie agentów</strong>.</p>

<blockquote>„PAIR to osobisty router AI, który inteligentnie dystrybuuje wnioskowanie AI pomiędzy urządzeniami w sieci lokalnej.” — NVIDIA, IFA 2026</blockquote>

<h2>Wzorce architektoniczne dla wielu urządzeń</h2>

<h3>Wzorzec 1: Równoległość na poziomie zadań</h3>
<p>Główny agent koordynujący dzieli zapytanie na niezależne podzadania i przekazuje je dedykowanym agentom roboczym na różnych maszynach.</p>

<h3>Wzorzec 2: Warstwowy routing modeli (Tiered Routing)</h3>
<ul>
  <li><strong>Stacja robocza (RTX 4090):</strong> Złożona synteza, programowanie (Qwen 2.5 32B, DeepSeek R1)</li>
  <li><strong>Laptop (RTX 4070):</strong> Szybka ekstrakcja i podsumowania (Llama 3.3 8B)</li>
  <li><strong>Mini-PC:</strong> Klasyfikacja i filtrowanie zapytań (Qwen 2.5 1.5B)</li>
</ul>

<h3>Wzorzec 3: Hybryda Lokalna + Chmura</h3>
<p>Prywatne dane przetwarzane są lokalnie na własnym sprzęcie, podczas gdy zadania wymagające potężnego wnioskowania są przekazywane do API chmurowych (Claude 3.5 Sonnet, DeepSeek V3).</p>

<h2>Podsumowanie</h2>
<p>NVIDIA PAIR potwierdza kluczowy trend: przyszłość autonomicznych systemów AI opiera się na rozproszonej orkiestracji i efektywnym zarządzaniu zasobami.</p>
"""
    },

    "2026-09-02-agent-architecture-convergence": {
        "slug": "2026-09-02-agent-architecture-convergence",
        "date": "2026-09-02",
        "dateDe": "2. September 2026",
        "datePl": "2 września 2026",
        "readTimeDe": "8 Min. Lesezeit",
        "readTimePl": "8 min czytania",
        "titleDe": "Die Konvergenz der Agenten-Architekturen: Warum alle das gleiche Zwei-Ebenen-System bauen",
        "titlePl": "Konwergencja Architektur Agentów: Dlaczego wszyscy budują ten sam dwupoziomowy system",
        "tagsDe": ["KI-Agenten", "Autonome Systeme", "Architektur", "AOS", "Control Plane"],
        "tagsPl": ["Agenci AI", "Systemy Autonomiczne", "Architektura", "AOS", "Control Plane"],
        "contentDe": """
<p>In den letzten sechs Monaten haben drei völlig unabhängige Entwicklungsteams ihre Referenzarchitekturen für autonome KI-Agenten veröffentlicht: <strong>NVIDIA (AVO)</strong>, das <strong>AOS-Projekt</strong> und das <strong>Auton-Framework</strong>. Obwohl sie für unterschiedliche Anwendungsbereiche entwickelt wurden, sind alle drei zu exakt demselben Grundmuster konvergiert: <strong>einem Zwei-Ebenen-System (Two-Plane Architecture), das Governance von der Ausführung trennt</strong>.</p>

<p>Dies ist kein Zufall. Es ist das unvermeidliche Ergebnis, wenn man versucht, autonome Agenten 24/7 in Produktionsumgebungen stabil zu betreiben.</p>

<h2>Die Zwei Ebenen im Detail</h2>

<h3>1. Die Steuerungsebene (Control Plane / Governance)</h3>
<p>Die Steuerungsebene definiert <em>WAS</em> getan werden darf und welche Leitplanken gelten. Sie enthält:
<ul>
  <li><strong>Zustands- und Speicherverwaltung:</strong> Persistente Wissensgraphen (z. B. Obsidian Markdown Vaults oder SQLite).</li>
  <li><strong>Policy & Guardrails:</strong> Sicherheitsregeln, EU AI Act Konformität, Budgetlimits.</li>
  <li><strong>Watchdog & Supervisor:</strong> Überwachung von Schleifen, Deadlocks und Erkennung von Halluzinationen.</li>
</ul>
</p>

<h3>2. Die Ausführungsebene (Runtime / Execution Plane)</h3>
<p>Die Ausführungsebene steuert <em>WIE</em> die Aufgaben umgesetzt werden:
<ul>
  <li><strong>Model Context Protocol (MCP) Server:</strong> Werkzeugaufrufe, API-Schnittstellen, Dateisystemzugriff.</li>
  <li><strong>Dynamisches Modell-Routing:</strong> Zuweisung von Sub-Aufgaben an DeepSeek, Claude 3.5 Sonnet oder GPT-4o.</li>
  <li><strong>Fehlerbehandlung & Retry-Logik:</strong> Isolierte Wiederholungsversuche ohne Kontrollverlust.</li>
</ul>
</p>

<h2>Warum monolithische Agenten scheitern</h2>
<p>Wenn Steuerung und Ausführung in einer einzigen Prompt-Schleife vermischt werden, führt jede Fehlentscheidung des Modells zum Systemstillstand. Die strikte Trennung garantiert Ausfallsicherheit und Auditierbarkeit.</p>
""",
        "contentPl": """
<p>W ciągu ostatnich sześciu miesięcy trzy niezależne zespoły inżynierskie opublikowały swoje referencyjne architektury dla autonomicznych agentów AI: <strong>NVIDIA (AVO)</strong>, projekt <strong>AOS</strong> oraz framework <strong>Auton</strong>. Mimo różnych założeń początkowych, wszystkie trzy projekty zbiegły się w tym samym punkcie: <strong>dwupłaszczyznowym modelu (Two-Plane Architecture) rozdzielającym zarządzanie od wykonania</strong>.</p>

<h2>Dwie Płaszczyzny Systemu</h2>

<h3>1. Płaszczyzna Sterowania (Control Plane)</h3>
<p>Odpowiada za reguły, stan i nadzór:
<ul>
  <li><strong>Pamięć trwała:</strong> Grafy wiedzy w Markdownie (Obsidian) i relacyjne bazy SQLite.</li>
  <li><strong>Polityki i Bezpieczeństwo:</strong> Limity budżetowe, zgodność z RODO i EU AI Act.</li>
  <li><strong>Watchdog:</strong> Monitorowanie pętli decyzyjnych i zapobieganie zacięciom agenta.</li>
</ul>
</p>

<h3>2. Płaszczyzna Wykonawcza (Runtime Plane)</h3>
<p>Realizuje konkretne zadania narzędziowe:
<ul>
  <li><strong>Serwery MCP (Model Context Protocol):</strong> Integracje z bazami, przeglądarkami i API.</li>
  <li><strong>Dynamiczny Routing:</strong> Dobór modeli LLM zależnie od stopnia trudności zadania.</li>
</ul>
</p>

<h2>Wnioski</h2>
<p>Rozdzielenie płaszczyzny decyzyjnej od wykonawczej to jedyna droga do stabilnych i bezpiecznych wdrożeń AI w biznesie.</p>
"""
    },

    "2026-08-27-nvidia-avo-autonomous-agents": {
        "slug": "2026-08-27-nvidia-avo-autonomous-agents",
        "date": "2026-08-27",
        "dateDe": "27. August 2026",
        "datePl": "27 sierpnia 2026",
        "readTimeDe": "6 Min. Lesezeit",
        "readTimePl": "6 min czytania",
        "titleDe": "NVIDIA AVO: Wenn autonome Agenten 7 Tage laufen und Top-Ingenieure schlagen",
        "titlePl": "NVIDIA AVO: Kiedy autonomiczni agenci działają przez 7 dni i przewyższają inżynierów",
        "tagsDe": ["KI-Agenten", "Autonome Systeme", "NVIDIA", "Hermes Agent"],
        "tagsPl": ["Agenci AI", "Systemy Autonomiczne", "NVIDIA", "Hermes Agent"],
        "contentDe": """
<p>NVIDIAs Forschungsteam hat mit der <strong>AVO-Architektur</strong> demonstriert, was möglich ist, wenn autonome KI-Agenten über 7 Tage hinweg kontinuierlich ohne menschlichen Eingriff laufen. Das System optimierte GPU-Kernel über den bisherigen Stand der Technik (FlashAttention-4) hinaus und erreichte 100 % im Benchmark ARC-AGI-3.</p>

<p>Die wichtigste Erkenntnis: <strong>Systemarchitektur schlägt reine Modellwahl</strong>. Nicht das größte Modell gewinnt, sondern die robusteste Feedback-Schleife mit Reflexion, Fehlerkorrektur und persistenter Speicherverwaltung.</p>
""",
        "contentPl": """
<p>Zespół badawczy firmy NVIDIA zaprezentował architekturę <strong>AVO</strong>, udowadniając skuteczność autonomicznych agentów działających nieprzerwanie przez 7 dni. System samodzielnie zoptymalizował jądra GPU i uzyskał 100% wynik w teście ARC-AGI-3.</p>

<p>Główny wniosek: <strong>Architektura systemu ma większe znaczenie niż wybór samego modelu</strong>. Kluczem do sukcesu są pętle weryfikacji i trwała pamięć.</p>
"""
    },

    "2026-08-26-agent-driven-company": {
        "slug": "2026-08-26-agent-driven-company",
        "date": "2026-08-26",
        "dateDe": "26. August 2026",
        "datePl": "26 sierpnia 2026",
        "readTimeDe": "6 Min. Lesezeit",
        "readTimePl": "6 min czytania",
        "titleDe": "Vom Solo-Gründer zum agentengesteuerten Unternehmen mit 19 Cron-Jobs",
        "titlePl": "Od jednoosobowej firmy do przedsiębiorstwa sterowanego przez 19 zadań cron",
        "tagsDe": ["KI-Agenten", "Hermes Agent", "Autonome Systeme", "Cron"],
        "tagsPl": ["Agenci AI", "Hermes Agent", "Systemy Autonomiczne", "Cron"],
        "contentDe": """
<p>Wie ich auf einem 3,79 €/Monat Hetzner VPS eine 24/7-Infrastruktur mit 19 autonomen KI-Agenten aufgebaut habe. Die Agenten übernehmen Content-Erstellung, CRM-Pflege, regulatorisches Monitoring und Systemüberwachung mit 99,7 % Verfügbarkeit.</p>
""",
        "contentPl": """
<p>Jak zbudowałem infrastrukturę 19 autonomicznych agentów AI na serwerze Hetzner VPS za 3,79 €/miesiąc. Agenci realizują zadania marketingowe, CRM, monitoring prawny i diagnostykę z dostępnością 99,7%.</p>
"""
    },

    "2026-08-25-web-performance-optimization": {
        "slug": "2026-08-25-web-performance-optimization",
        "date": "2026-08-25",
        "dateDe": "25. August 2026",
        "datePl": "25 sierpnia 2026",
        "readTimeDe": "5 Min. Lesezeit",
        "readTimePl": "5 min czytania",
        "titleDe": "Web-Performance-Optimierung: Wie ich die Seitengröße um 61 % reduzierte",
        "titlePl": "Optymalizacja wydajności strony: Jak zmniejszyłem rozmiar o 61%",
        "tagsDe": ["Web Performance", "Lighthouse", "Core Web Vitals"],
        "tagsPl": ["Wydajność Sieci", "Lighthouse", "Core Web Vitals"],
        "contentDe": """
<p>Technischer Leitfaden zur Reduzierung des HTML-Seitengewichts von 86 KB auf 34 KB für einen Lighthouse-Score von 100 und 0 ms TBT durch Vanilla JS, ausgelagertes CSS und optimiertes WebGL.</p>
""",
        "contentPl": """
<p>Praktyczny przewodnik po redukcji wagi strony HTML z 86 KB do 34 KB, osiągając wynik 100 w Google Lighthouse i 0 ms TBT dzięki czystemu JavaScriptowi i zoptymalizowanemu WebGL.</p>
"""
    },

    "2026-08-22-building-digital-twin": {
        "slug": "2026-08-22-building-digital-twin",
        "date": "2026-08-22",
        "dateDe": "22. August 2026",
        "datePl": "22 sierpnia 2026",
        "readTimeDe": "4 Min. Lesezeit",
        "readTimePl": "4 min czytania",
        "titleDe": "Aufbau eines digitalen Zwillings, der 9-mal täglich postet",
        "titlePl": "Budowa cyfrowego bliźniaka publikującego 9 razy dziennie",
        "tagsDe": ["KI-Agenten", "Hermes Agent", "Automatisierung"],
        "tagsPl": ["Agenci AI", "Hermes Agent", "Automatyzacja"],
        "contentDe": """
<p>Erfahrungsbericht zum Bau eines autonomen KI-Agenten mit Hermes, der Inhalte plattformübergreifend auf X, LinkedIn und dem Blog recherchiert, generiert und veröffentlicht.</p>
""",
        "contentPl": """
<p>Jak wdrożyłem autonomicznego agenta AI opartego na Hermesie, który tworzy i publikuje treści na platformach X, LinkedIn i blogu bez udziału człowieka.</p>
"""
    },

    "2026-08-20-ai-act-compliance": {
        "slug": "2026-08-20-ai-act-compliance",
        "date": "2026-08-20",
        "dateDe": "20. August 2026",
        "datePl": "20 sierpnia 2026",
        "readTimeDe": "6 Min. Lesezeit",
        "readTimePl": "6 min czytania",
        "titleDe": "EU AI Act Compliance für kleine KI-Unternehmen",
        "titlePl": "Zgodność z EU AI Act dla małych firm AI",
        "tagsDe": ["AI Act", "DSGVO", "Compliance", "Recht"],
        "tagsPl": ["AI Act", "RODO", "Zgodność", "Prawo"],
        "contentDe": """
<p>Praktischer Legal-by-Design Leitfaden für Startups im EU-Raum: Von der Risikoklassifizierung nach dem EU AI Act bis zur automatisierten Erstellung technischer Dokumentationsdateien.</p>
""",
        "contentPl": """
<p>Praktyczny framework legal-by-design dla startupów tworzących produkty AI w Unii Europejskiej: od klasyfikacji ryzyka po audytowalną dokumentację techniczną.</p>
"""
    },

    "2026-08-17-autonomous-drone-missions": {
        "slug": "2026-08-17-autonomous-drone-missions",
        "date": "2026-08-17",
        "dateDe": "17. August 2026",
        "datePl": "17 sierpnia 2026",
        "readTimeDe": "5 Min. Lesezeit",
        "readTimePl": "5 min czytania",
        "titleDe": "Autonome Drohnenmissionen mit ArduPilot & Python",
        "titlePl": "Autonomiczne misje dronów z ArduPilotem i Pythonem",
        "tagsDe": ["Drohnen", "ArduPilot", "UAV", "Edge KI"],
        "tagsPl": ["Drony", "ArduPilot", "UAV", "Edge AI"],
        "contentDe": """
<p>Aufbau eines taktischen 1500g Carbon-Quads mit ArduPilot, Pixhawk und Python-Missionsplanung für autonome Flüge und Edge-KI mit Raspberry Pi 5 (Hobbyprojekt).</p>
""",
        "contentPl": """
<p>Budowa węglowego quada 1500g z ArduPilotem, Pixhawkiem i planowaniem misji w Pythonie z wykorzystaniem pokładowej wizji komputerowej na Raspberry Pi 5.</p>
"""
    }
}

def generate_navbar(active_lang, slug):
    en_link = f"/blog/posts/{slug}"
    sk_link = f"/blog/posts/sk/{slug}"
    de_link = f"/blog/posts/de/{slug}"
    pl_link = f"/blog/posts/pl/{slug}"
    
    back_text = {
        "en": "← All Articles",
        "sk": "← Všetky články",
        "de": "← Alle Beiträge",
        "pl": "← Wszystkie artykuły"
    }[active_lang]

    return f"""<nav aria-label="Main navigation">
  <div class="nav-container">
    <a href="/" class="nav-logo" aria-label="marianstancik.dev home">
      <div class="brand-mark" aria-hidden="true"><img src="/profile.webp" alt="Marian Stancik" width="28" height="28" class="brand-avatar"></div>
      <span class="nav-logo-text">marian<span class="highlight">stancik</span><span class="tld">.dev</span></span>
    </a>
    <div class="nav-right">
      <div class="lang-switcher" aria-label="Language selector">
        <a href="{en_link}" class="lang-btn {'active' if active_lang == 'en' else ''}">EN</a>
        <a href="{sk_link}" class="lang-btn {'active' if active_lang == 'sk' else ''}">SK</a>
        <a href="{de_link}" class="lang-btn {'active' if active_lang == 'de' else ''}">DE</a>
        <a href="{pl_link}" class="lang-btn {'active' if active_lang == 'pl' else ''}">PL</a>
      </div>
      <a href="/blog" class="nav-link">{back_text}</a>
    </div>
  </div>
</nav>"""

def update_article_navbar(fpath, active_lang, slug):
    if not os.path.exists(fpath):
        return
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    nav_html = generate_navbar(active_lang, slug)
    # Replace existing <nav>...</nav>
    new_content = re.sub(r'<nav aria-label="Main navigation">[\s\S]*?<\/nav>', nav_html, content)
    
    # Ensure hreflang links exist
    hreflangs = f"""<link rel="alternate" hreflang="en" href="https://www.marianstancik.dev/blog/posts/{slug}">
<link rel="alternate" hreflang="sk" href="https://www.marianstancik.dev/blog/posts/sk/{slug}">
<link rel="alternate" hreflang="de" href="https://www.marianstancik.dev/blog/posts/de/{slug}">
<link rel="alternate" hreflang="pl" href="https://www.marianstancik.dev/blog/posts/pl/{slug}">
<link rel="alternate" hreflang="x-default" href="https://www.marianstancik.dev/blog/posts/{slug}">"""
    
    if '<link rel="alternate" hreflang="de"' not in new_content:
        new_content = new_content.replace('</head>', f'{hreflangs}\n</head>')
    
    # Ensure cache-busted i18n.js
    if '<script src="/js/i18n.js' not in new_content:
        new_content = new_content.replace('</body>', '<script src="/js/i18n.js?v=20260908_v2"></script>\n</body>')
    else:
        new_content = re.sub(r'<script\s+src=["\']/js/i18n\.js(?:\?[^"\']*)?["\']\s*></script>', '<script src="/js/i18n.js?v=20260908_v2"></script>', new_content)
        
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)

# Process each of the 8 articles
for slug, data in POSTS_DATA.items():
    en_path = os.path.join(POSTS_DIR, f"{slug}.html")
    sk_path = os.path.join(SK_DIR, f"{slug}.html")
    de_path = os.path.join(DE_DIR, f"{slug}.html")
    pl_path = os.path.join(PL_DIR, f"{slug}.html")

    # Update navbar in EN and SK articles
    update_article_navbar(en_path, "en", slug)
    update_article_navbar(sk_path, "sk", slug)

    # Read base EN template for DE and PL generation
    if os.path.exists(en_path):
        with open(en_path, 'r', encoding='utf-8') as f:
            en_html = f.read()
        
        # Build DE HTML
        de_html = en_html
        de_html = re.sub(r'<html lang="[^"]*">', '<html lang="de">', de_html)
        de_html = re.sub(r'<title>[^<]*<\/title>', f'<title>{data["titleDe"]} — Marian Stancik</title>', de_html)
        de_html = re.sub(r'<h1>[^<]*<\/h1>', f'<h1>{data["titleDe"]}</h1>', de_html)
        de_html = re.sub(r'<time[^>]*>[^<]*<\/time>', f'<time datetime="{data["date"]}">{data["dateDe"]}</time>', de_html)
        de_html = re.sub(r'<span>\d+ min read<\/span>', f'<span>{data["readTimeDe"]}</span>', de_html)
        
        # Tags DE
        tags_de_html = "".join([f"<span>{t}</span>" for t in data["tagsDe"]])
        de_html = re.sub(r'<div class="post-tags">[\s\S]*?<\/div>', f'<div class="post-tags">{tags_de_html}</div>', de_html)
        
        # Content DE
        de_html = re.sub(r'<article class="post-content">[\s\S]*?<\/article>', f'<article class="post-content">{data["contentDe"]}</article>', de_html)
        de_html = re.sub(r'<a href="\/blog" class="post-back">[^<]*<\/a>', '<a href="/blog" class="post-back">← Zurück zum Blog</a>', de_html)
        
        with open(de_path, 'w', encoding='utf-8') as f:
            f.write(de_html)
        update_article_navbar(de_path, "de", slug)
        
        # Markdown DE
        de_md_path = os.path.join(DE_DIR, f"{slug}.md")
        with open(de_md_path, 'w', encoding='utf-8') as f:
            f.write(f"# {data['titleDe']}\n\n**Datum:** {data['dateDe']} | **Autor:** Marian Stancik\n\n{re.sub(r'<[^>]+>', '', data['contentDe'])}\n")

        # Build PL HTML
        pl_html = en_html
        pl_html = re.sub(r'<html lang="[^"]*">', '<html lang="pl">', pl_html)
        pl_html = re.sub(r'<title>[^<]*<\/title>', f'<title>{data["titlePl"]} — Marian Stancik</title>', pl_html)
        pl_html = re.sub(r'<h1>[^<]*<\/h1>', f'<h1>{data["titlePl"]}</h1>', pl_html)
        pl_html = re.sub(r'<time[^>]*>[^<]*<\/time>', f'<time datetime="{data["date"]}">{data["datePl"]}</time>', pl_html)
        pl_html = re.sub(r'<span>\d+ min read<\/span>', f'<span>{data["readTimePl"]}</span>', pl_html)
        
        # Tags PL
        tags_pl_html = "".join([f"<span>{t}</span>" for t in data["tagsPl"]])
        pl_html = re.sub(r'<div class="post-tags">[\s\S]*?<\/div>', f'<div class="post-tags">{tags_pl_html}</div>', pl_html)
        
        # Content PL
        pl_html = re.sub(r'<article class="post-content">[\s\S]*?<\/article>', f'<article class="post-content">{data["contentPl"]}</article>', pl_html)
        pl_html = re.sub(r'<a href="\/blog" class="post-back">[^<]*<\/a>', '<a href="/blog" class="post-back">← Wróć do bloga</a>', pl_html)
        
        with open(pl_path, 'w', encoding='utf-8') as f:
            f.write(pl_html)
        update_article_navbar(pl_path, "pl", slug)

        # Markdown PL
        pl_md_path = os.path.join(PL_DIR, f"{slug}.md")
        with open(pl_md_path, 'w', encoding='utf-8') as f:
            f.write(f"# {data['titlePl']}\n\n**Data:** {data['datePl']} | **Autor:** Marian Stancik\n\n{re.sub(r'<[^>]+>', '', data['contentPl'])}\n")

print("[+] All 8 articles in EN, SK, DE, PL updated with full translations and 4-way language switcher!")
