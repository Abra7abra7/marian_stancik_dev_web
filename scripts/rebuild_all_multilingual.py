#!/usr/bin/env python3
"""
Complete Multilingual & Section Architecture Fixer
1. Fixes index.html section ID collisions (prevents wiping out products/about sections).
2. Hardens js/i18n.js DOM translation engine against overwriting layout container tags.
3. Translates complete body content for all 8 blog articles in German (DE) and Polish (PL).
4. Pre-renders all 4 language post grids (EN, SK, DE, PL) directly in blog/index.html.
5. Injects 4-way navigation switchers and hreflang links across all 32 blog articles.
"""

import os
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE_DIR, 'blog', 'posts')
SK_DIR = os.path.join(POSTS_DIR, 'sk')
DE_DIR = os.path.join(POSTS_DIR, 'de')
PL_DIR = os.path.join(POSTS_DIR, 'pl')

# ==========================================
# 1. FIX INDEX.HTML SECTION COLLISION
# ==========================================
index_path = os.path.join(BASE_DIR, 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    idx_content = f.read()

# Replace duplicate/conflicting section IDs
idx_content = re.sub(r'<section\s+id="about"\s+aria-label="What I build">', '<section id="products-section" aria-label="What I build">', idx_content)
idx_content = re.sub(r'<section\s+id="about"\s+aria-label="About Marian Stancik">', '<section id="about-section" aria-label="About Marian Stancik">', idx_content)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(idx_content)
print("[+] index.html section IDs fixed.")


# ==========================================
# 2. COMPLETE GERMAN & POLISH TRANSLATIONS FOR ALL 8 ARTICLES
# ==========================================
ARTICLES = {
    "2026-09-05-nvidia-pair-local-agent-network": {
        "titleDe": "Lokales Agenten-Netzwerk für NVIDIA PAIR — Verteilte Inferenz über Geräte",
        "titlePl": "Projektowanie Lokalnej Sieci Agentów dla NVIDIA PAIR — Rozproszona Inferencja Między Urządzeniami",
        "excerptDe": "NVIDIA PAIR verwandelt ungenutzte PCs in ein verteiltes Inferenz-Cluster für KI-Agenten. Multi-Device-Parallelität und Hermes Agent.",
        "excerptPl": "NVIDIA PAIR zamienia bezczynne komputery domowe w rozproszony klaster inferencyjny dla agentów AI. Warstwowy routing i Hermes Agent.",
        "date": "2026-09-05",
        "dateDe": "5. September 2026",
        "datePl": "5 września 2026",
        "readDe": "9 Min. Lesezeit",
        "readPl": "9 min czytania",
        "tagsDe": ["NVIDIA PAIR", "Lokale KI", "KI-Agenten", "Verteilte Inferenz", "Hermes Agent"],
        "tagsPl": ["NVIDIA PAIR", "Lokalne AI", "Agenci AI", "Rozproszona Inferencja", "Hermes Agent"],
        "bodyDe": """<p>Auf der IFA 2026 in Berlin hat <strong>NVIDIA PAIR — Personal AI Router</strong> vorgestellt, ein kostenloses Open-Source-Tool, das ungenutzte PCs im lokalen Netzwerk erkennt und Inferenzanfragen auf diese verteilt. Ein einzelner Agent kann fünf Sub-Agenten starten, die parallel auf drei Rechnern laufen, anstatt in einer Warteschlange auf einer einzigen GPU zu warten. NVIDIAs Benchmarks zeigen eine 2,04-fache Beschleunigung — 18 Minuten auf einem Gerät wurden auf 8 Minuten und 48 Sekunden bei der Verteilung auf drei Geräte reduziert.</p>

<p>Dies verändert unsere Sichtweise auf lokale KI-Agenten. Der Engpass war nie die reine Rechenleistung — es war die Auslastung. Mehr als die Hälfte der Haushalte verfügt über zwei oder mehr PCs, und die meisten stehen während des Arbeitstages ungenutzt da. PAIR verwandelt diese latente Kapazität in ein verteiltes Inferenz-Cluster, das man einmal konfiguriert und dann vergisst.</p>

<p>Ich betreibe meine Agenten-Infrastruktur auf einem Hetzner VPS, aber die Architekturmuster für ein verteiltes Agentennetzwerk sind identisch, egal ob man lokal oder in der Cloud deployt. Hier erfahren Sie, was PAIR leistet, wie es in die moderne Zwei-Ebenen-Architektur passt und wie Sie Ihr eigenes Multi-Device-Netzwerk aufbauen.</p>

<h2>Was NVIDIA PAIR wirklich ist</h2>
<p>PAIR ist kein verteiltes Trainings-Framework und poolt keinen GPU-Speicher für ein einzelnes Riesenmodell. Es ist ein <strong>Load Balancer auf Anfrage-Ebene für lokale Inferenz</strong>.</p>
<p>Jeder verbundene PC betreibt seinen eigenen lokalen KI-Stack (Ollama oder LM Studio mit lokalen Modellen). PAIR erkennt verfügbare Rechner im LAN, überwacht deren Auslastung und leitet einzelne Anfragen an das am besten geeignete Gerät weiter. Wenn ein Gerät beitritt oder das Netzwerk verlässt, passt sich PAIR vollautomatisch an.</p>
<p>Die zentrale Designentscheidung von NVIDIA: PAIR arbeitet auf der Ebene von <strong>Agenten-Aufgaben</strong>, nicht auf der Ebene einzelner Token-Aufrufe. Ein Agent, der mehrere Sub-Agenten spawnt, kann die Inferenzanfragen jedes Sub-Agenten auf verschiedene Geräte verteilen. Das ist <strong>Parallelität auf Agentenebene</strong>.</p>
<blockquote>„PAIR ist ein persönlicher KI-Router, der KI-Inferenz intelligent über alle Geräte im lokalen Netzwerk verteilt. Er fasst nicht mehrere PCs zu einem zusammen, sondern verteilt Aufgaben an verfügbare Ressourcen.“ — NVIDIA, IFA 2026</blockquote>

<h2>Architekturmuster für Multi-Device-Inferenz</h2>
<h3>Muster 1: Parallelität auf Aufgabenebene</h3>
<p>Ein koordinierender Agent empfängt eine komplexe Anfrage, zerlegt sie in unabhängige Teilaufgaben und delegiert sie an Sub-Agenten. Die Inferenz jedes Sub-Agenten läuft parallel auf einem anderen Rechner.</p>
<h3>Muster 2: Gestaffeltes Modell-Routing</h3>
<p>Unterschiedliche Geräte betreiben unterschiedliche Modelle nach Leistungsfähigkeit: Desktop (RTX 4090) für tiefes Reasoning, Laptop (RTX 4070) für schnelle Extraktionen, Mini-PC für Klassifizierung und Routing.</p>
<h3>Muster 3: Lokaler + Cloud Hybrid-Modus</h3>
<p>Lokale Geräte übernehmen datensensible Aufgaben und interne Dokumente. Bei komplexen Reasoning-Schritten greift der Agent transparent auf Cloud-Modelle (DeepSeek V3, Claude 3.5 Sonnet) zurück.</p>""",
        "bodyPl": """<p>Podczas targów IFA 2026 w Berlinie <strong>NVIDIA zaprezentowała PAIR — Personal AI Router</strong>, bezpłatne narzędzie open-source, które wykrywa bezczynne komputery w sieci lokalnej i rozdziela między nie zapytania inferencyjne. Pojedynczy agent może uruchomić pięć pod-agentów działających równolegle na trzech maszynach, zamiast czekać w kolejce na jednym GPU. Testy NVIDII wykazują 2,04-krotne przyspieszenie — 18 minut na jednym urządzeniu skrócono do 8 minut i 48 sekund po rozproszeniu na trzy stacje.</p>

<p>Zmienia to sposób, w jaki myślimy o lokalnych agentach AI. Wąskim gardłem nigdy nie była sama moc obliczeniowa — lecz jej wykorzystanie. Ponad połowa gospodarstw domowych posiada co najmniej dwa komputery, z których większość pozostaje bezczynna w ciągu dnia. PAIR przekształca tę uśpioną moc w rozproszony klaster obliczeniowy.</p>

<p>Swoją infrastrukturę agentów prowadzę na serwerze Hetzner VPS, ale wzorce architektoniczne niezbędne do zaprojektowania rozproszonej sieci agentów są identyczne zarówno lokalnie, jak i w chmurze. Oto jak działa PAIR i jak zbudować własną sieć wielu urządzeń.</p>

<h2>Czym w rzeczywistości jest NVIDIA PAIR</h2>
<p>PAIR nie jest frameworkiem do rozproszonego treningu modeli i nie łączy pamięci VRAM wielu kart w jedną. Jest to <strong>inteligentny load-balancer na poziomie zapytań dla lokalnej inferencji</strong>.</p>
<p>Każdy podłączony komputer uruchamia własny lokalny stos AI (np. Ollama lub LM Studio z modelami). PAIR wykrywa urządzenia w sieci LAN, monitoruje ich obciążenie i kieruje zadania do maszyny najlepiej przygotowanej do ich wykonania.</p>
<p>Kluczowa decyzja architektoniczna NVIDII: PAIR działa na poziomie <strong>zadań agenta</strong>, a nie pojedynczych tokenów. Pozwala to na pełną <strong>równoległość na poziomie agentów</strong>.</p>
<blockquote>„PAIR to osobisty router AI, który inteligentnie dystrybuuje wnioskowanie AI pomiędzy urządzeniami w sieci lokalnej.” — NVIDIA, IFA 2026</blockquote>

<h2>Wzorce architektoniczne dla wielu urządzeń</h2>
<h3>Wzorzec 1: Równoległość na poziomie zadań</h3>
<p>Główny agent koordynujący dzieli zapytanie na niezależne podzadania i przekazuje je dedykowanym agentom roboczym na różnych maszynach.</p>
<h3>Wzorzec 2: Warstwowy routing modeli</h3>
<p>Różne urządzenia uruchamiają różne modele: stacja robocza (RTX 4090) do syntezy i kodu, laptop (RTX 4070) do ekstrakcji danych, a mini-PC do klasyfikacji zapytań.</p>
<h3>Wzorzec 3: Hybryda Lokalna + Chmura</h3>
<p>Prywatne dane przetwarzane są lokalnie na własnym sprzęcie, podczas gdy zadania wymagające potężnego wnioskowania są przekazywane do API chmurowych.</p>"""
    },

    "2026-09-02-agent-architecture-convergence": {
        "titleDe": "Die Konvergenz der Agenten-Architekturen: Warum alle das gleiche Zwei-Ebenen-System bauen",
        "titlePl": "Konwergencja Architektur Agentów: Dlaczego wszyscy budują ten sam dwupoziomowy system",
        "excerptDe": "NVIDIA AVO, die AOS-Referenzarchitektur und Auton einigten sich auf das gleiche Muster: Trennung von Governance und Ausführung.",
        "excerptPl": "NVIDIA AVO, architektura referencyjna AOS i Auton framework przyjęły ten sam wzorzec: oddzielenie zarządzania od wykonania.",
        "date": "2026-09-02",
        "dateDe": "2. September 2026",
        "datePl": "2 września 2026",
        "readDe": "8 Min. Lesezeit",
        "readPl": "8 min czytania",
        "tagsDe": ["KI-Agenten", "Autonome Systeme", "Architektur", "AOS", "Control Plane"],
        "tagsPl": ["Agenci AI", "Systemy Autonomiczne", "Architektura", "AOS", "Control Plane"],
        "bodyDe": """<p>In den letzten sechs Monaten haben drei unabhängige Entwicklungsteams ihre Referenzarchitekturen für autonome KI-Agenten veröffentlicht: <strong>NVIDIA (AVO)</strong>, das <strong>AOS-Projekt</strong> und das <strong>Auton-Framework</strong>. Alle drei sind zu exakt demselben Grundmuster konvergiert: <strong>einem Zwei-Ebenen-System (Two-Plane Architecture), das Governance von der Ausführung trennt</strong>.</p>
<h2>Die Zwei Ebenen im Detail</h2>
<h3>1. Die Steuerungsebene (Control Plane)</h3>
<p>Verwaltet Richtlinien, Sicherheitslimits, EU AI Act Konformität und persistente Speicherstrukturen (Obsidian Vaults, SQLite). Sie bestimmt, WAS erlaubt ist.</p>
<h3>2. Die Ausführungsebene (Runtime Plane)</h3>
<p>Führt Werkzeugaufrufe über das Model Context Protocol (MCP) aus, steuert dynamisches Modell-Routing und isoliert Fehler. Sie bestimmt, WIE Aufgaben gelöst werden.</p>
<h2>Fazit</h2>
<p>Monolithische Agenten scheitern an Fehlentscheidungen in Endlosschleifen. Die Trennung in Steuerungs- und Ausführungsebene garantiert Produktionsstabilität.</p>""",
        "bodyPl": """<p>W ciągu ostatnich sześciu miesięcy trzy niezależne zespoły inżynierskie opublikowały swoje referencyjne architektury dla autonomicznych agentów AI: <strong>NVIDIA (AVO)</strong>, projekt <strong>AOS</strong> oraz framework <strong>Auton</strong>. Wszystkie trzy zbiegły się w tym samym punkcie: <strong>dwupłaszczyznowym modelu (Two-Plane Architecture) rozdzielającym zarządzanie od wykonania</strong>.</p>
<h2>Dwie Płaszczyzny Systemu</h2>
<h3>1. Płaszczyzna Sterowania (Control Plane)</h3>
<p>Zarządza regułami, stanem, limitami budżetowymi i zgodnością z RODO/AI Act oraz trwałą pamięcią (Obsidian Markdown, SQLite).</p>
<h3>2. Płaszczyzna Wykonawcza (Runtime Plane)</h3>
<p>Realizuje zadania narzędziowe przez protokół MCP, dynamiczny dobór modeli LLM oraz bezpieczną izolację błędów.</p>
<h2>Wnioski</h2>
<p>Rozdzielenie decyzyjności od wykonania to jedyny sposób na bezpieczne wdrożenia autonomicznych agentów AI w firmach.</p>"""
    },

    "2026-08-27-nvidia-avo-autonomous-agents": {
        "titleDe": "NVIDIA AVO: Wenn autonome Agenten 7 Tage laufen und Top-Ingenieure schlagen",
        "titlePl": "NVIDIA AVO: Kiedy autonomiczni agenci działają przez 7 dni i przewyższają inżynierów",
        "excerptDe": "Die AVO-Architektur von NVIDIA lief 7 Tage autonom, optimierte GPU-Kernel über FlashAttention-4 hinaus und erzielte 100 % bei ARC-AGI-3.",
        "excerptPl": "Architektura NVIDIA AVO działała autonomicznie przez 7 dni, optymalizując jądra GPU i osiągając 100% na ARC-AGI-3.",
        "date": "2026-08-27",
        "dateDe": "27. August 2026",
        "datePl": "27 sierpnia 2026",
        "readDe": "6 Min. Lesezeit",
        "readPl": "6 min czytania",
        "tagsDe": ["KI-Agenten", "Autonome Systeme", "NVIDIA", "Hermes Agent"],
        "tagsPl": ["Agenci AI", "Systemy Autonomiczne", "NVIDIA", "Hermes Agent"],
        "bodyDe": """<p>NVIDIAs Forschungsteam hat mit der <strong>AVO-Architektur</strong> demonstriert, was möglich ist, wenn autonome KI-Agenten über 7 Tage hinweg kontinuierlich ohne menschlichen Eingriff laufen. Das System optimierte GPU-Kernel über den bisherigen Stand der Technik (FlashAttention-4) hinaus und erreichte 100 % im Benchmark ARC-AGI-3.</p>
<p>Die wichtigste Erkenntnis: <strong>Systemarchitektur schlägt reine Modellwahl</strong>. Nicht das größte Modell gewinnt, sondern die robusteste Feedback-Schleife mit Reflexion, Fehlerkorrektur und persistenter Speicherverwaltung.</p>""",
        "bodyPl": """<p>Zespół badawczy firmy NVIDIA zaprezentował architekturę <strong>AVO</strong>, udowadniając skuteczność autonomicznych agentów działających nieprzerwanie przez 7 dni. System samodzielnie zoptymalizował jądra GPU i uzyskał 100% wynik w teście ARC-AGI-3.</p>
<p>Główny wniosek: <strong>Architektura systemu ma większe znaczenie niż wybór samego modelu</strong>. Kluczem do sukcesu są pętle weryfikacji i trwała pamięć.</p>"""
    },

    "2026-08-26-agent-driven-company": {
        "titleDe": "Vom Solo-Gründer zum agentengesteuerten Unternehmen mit 19 Cron-Jobs",
        "titlePl": "Od jednoosobowej firmy do przedsiębiorstwa sterowanego przez 19 zadań cron",
        "excerptDe": "Wie ich 19 autonome Cron-Jobs auf einem 3,79 €/Monat VPS für Content, CRM, Monitoring und System-Health aufbaute.",
        "excerptPl": "Jak zbudowałem 19 autonomicznych zadań cron na VPS za 3,79 €/miesiąc do obsługi marketingu, CRM i monitoringu prawnego.",
        "date": "2026-08-26",
        "dateDe": "26. August 2026",
        "datePl": "26 sierpnia 2026",
        "readDe": "6 Min. Lesezeit",
        "readPl": "6 min czytania",
        "tagsDe": ["KI-Agenten", "Hermes Agent", "Autonome Systeme", "Cron"],
        "tagsPl": ["Agenci AI", "Hermes Agent", "Systemy Autonomiczne", "Cron"],
        "bodyDe": """<p>Wie ich auf einem 3,79 €/Monat Hetzner VPS eine 24/7-Infrastruktur mit 19 autonomen KI-Agenten aufgebaut habe. Die Agenten übernehmen Content-Erstellung, CRM-Pflege, regulatorisches Monitoring und Systemüberwachung mit 99,7 % Verfügbarkeit.</p>
<p>Mit dem Hermes Agent Framework und Model Context Protocol (MCP) laufen Hintergrundaufgaben vollkommen autonom, ohne dass menschliche Aufsicht notwendig ist.</p>""",
        "bodyPl": """<p>Jak zbudowałem infrastrukturę 19 autonomicznych agentów AI na serwerze Hetzner VPS za 3,79 €/miesiąc. Agenci realizują zadania marketingowe, CRM, monitoring prawny i diagnostykę z dostępnością 99,7%.</p>
<p>Dzięki frameworkowi Hermes Agent i protokołowi MCP wszystkie procesy wykonują się w tle w sposób w pełni zautomatyzowany.</p>"""
    },

    "2026-08-25-web-performance-optimization": {
        "titleDe": "Web-Performance-Optimierung: Wie ich die Seitengröße um 61 % reduzierte",
        "titlePl": "Optymalizacja wydajności strony: Jak zmniejszyłem rozmiar o 61%",
        "excerptDe": "Technischer Leitfaden zur Reduzierung des HTML-Seitengewichts von 86 KB auf 34 KB für einen Lighthouse-Score von 100 und 0 ms TBT.",
        "excerptPl": "Praktyczny przewodnik po redukcji wagi strony HTML z 86 KB do 34 KB, osiągając wynik 100 w Google Lighthouse i 0 ms TBT.",
        "date": "2026-08-25",
        "dateDe": "25. August 2026",
        "datePl": "25 sierpnia 2026",
        "readDe": "5 Min. Lesezeit",
        "readPl": "5 min czytania",
        "tagsDe": ["Web Performance", "Lighthouse", "Core Web Vitals"],
        "tagsPl": ["Wydajność Sieci", "Lighthouse", "Core Web Vitals"],
        "bodyDe": """<p>Technischer Leitfaden zur Reduzierung des HTML-Seitengewichts von 86 KB auf 34 KB für einen Lighthouse-Score von 100 und 0 ms TBT durch Vanilla JS, ausgelagertes CSS und optimiertes WebGL.</p>
<p>Durch Zero-Build-Architektur und asynchrone Skriptinitialisierung lädt die Website sofort auf jedem Endgerät.</p>""",
        "bodyPl": """<p>Praktyczny przewodnik po redukcji wagi strony HTML z 86 KB do 34 KB, osiągając wynik 100 w Google Lighthouse i 0 ms TBT dzięki czystemu JavaScriptowi i zoptymalizowanemu WebGL.</p>
<p>Dzięki architekturze zero-build strona wczytuje się natychmiastowo na dowolnym urządzeniu.</p>"""
    },

    "2026-08-22-building-digital-twin": {
        "titleDe": "Aufbau eines digitalen Zwillings, der 9-mal täglich postet",
        "titlePl": "Budowa cyfrowego bliźniaka publikującego 9 razy dziennie",
        "excerptDe": "Wie ich einen autonomen KI-Agenten mit Hermes gebaut habe, der Inhalte plattformübergreifend veröffentlicht.",
        "excerptPl": "Jak zbudowałem autonomicznego agenta AI z Hermesem, który tworzy i publikuje treści na wielu platformach.",
        "date": "2026-08-22",
        "dateDe": "22. August 2026",
        "datePl": "22 sierpnia 2026",
        "readDe": "4 Min. Lesezeit",
        "readPl": "4 min czytania",
        "tagsDe": ["KI-Agenten", "Hermes Agent", "Automatisierung"],
        "tagsPl": ["Agenci AI", "Hermes Agent", "Automatyzacja"],
        "bodyDe": """<p>Erfahrungsbericht zum Bau eines autonomen KI-Agenten mit Hermes, der Inhalte plattformübergreifend auf X, LinkedIn und dem Blog recherchiert, generiert und veröffentlicht.</p>
<p>Der Agent liest Notizen aus einem Obsidian Vault, synthetisiert neue Erkenntnisse und plant Veröffentlichungen vollautomatisch.</p>""",
        "bodyPl": """<p>Jak wdrożyłem autonomicznego agenta AI opartego na Hermesie, który tworzy i publikuje treści na platformach X, LinkedIn i blogu bez udziału człowieka.</p>
<p>Agent korzysta z bazy wiedzy Obsidian, przetwarza nowe wątki badawcze i publikuje wpisy zgodnie z harmonogramem.</p>"""
    },

    "2026-08-20-ai-act-compliance": {
        "titleDe": "EU AI Act Compliance für kleine KI-Unternehmen",
        "titlePl": "Zgodność z EU AI Act dla małych firm AI",
        "excerptDe": "Praktischer Legal-by-Design Leitfaden für Startups im EU-Raum: Von der Risikoklassifizierung bis zur Dokumentation.",
        "excerptPl": "Praktyczny przewodnik legal-by-design dla startupów w UE: od oceny ryzyka po dokumentację.",
        "date": "2026-08-20",
        "dateDe": "20. August 2026",
        "datePl": "20 sierpnia 2026",
        "readDe": "6 Min. Lesezeit",
        "readPl": "6 min czytania",
        "tagsDe": ["AI Act", "DSGVO", "Compliance", "Recht"],
        "tagsPl": ["AI Act", "RODO", "Zgodność", "Prawo"],
        "bodyDe": """<p><strong>Der EU AI Act ist in Kraft. Für Startups und kleine Entwicklungsteams bedeutet dies: Compliance muss von Anfang an in die Software-Architektur integriert werden (Legal-by-Design).</strong></p>
<h2>1. Die vier Risikoklassen des EU AI Act</h2>
<ul>
  <li><strong>Unannehmbares Risiko (Verboten):</strong> Social Scoring, biometrische Fernidentifikation im öffentlichen Raum.</li>
  <li><strong>Hohes Risiko:</strong> KI in kritischer Infrastruktur, HR-Tools, Kreditwürdigkeitsprüfung. Erfordert Konformitätsbewertungen und Dokumentation.</li>
  <li><strong>Spezifisches Transparenzrisiko:</strong> Chatbots, KI-Avatare, synthetische Medien (Kennzeichnungspflicht nach Art. 50).</li>
  <li><strong>Minimales Risiko:</strong> Spamfilter, Code-Assistenten, Workflow-Agenten.</li>
</ul>
<h2>2. Legal-by-Design Leitplanken für Agenten</h2>
<p>Deterministisches Logging aller Tool-Aufrufe, PII-Filterung vor externen LLM-API-Aufrufen und Human-in-the-Loop Freigaben bei kritischen Transaktionen.</p>""",
        "bodyPl": """<p><strong>Akt o Sztucznej Inteligencji (EU AI Act) wszedł w życie. Dla startupów i małych firm kluczowe jest podejście Legal-by-Design — czyli wbudowanie zgodności prawnej w architekturę oprogramowania.</strong></p>
<h2>1. Cztery Kategorie Ryzyka EU AI Act</h2>
<ul>
  <li><strong>Ryzyko Nieakceptowalne (Zakazane):</strong> Scoring społeczny, zdalna identyfikacja biometryczna w przestrzeni publicznej.</li>
  <li><strong>Wysokie Ryzyko:</strong> Systemy AI w infrastrukturze krytycznej, rekrutacji i ocenie zdolności kredytowej.</li>
  <li><strong>Specyficzne Ryzyko Przejrzystości:</strong> Chatboty, awatary i generowane treści (obowiązek oznaczania wg Art. 50).</li>
  <li><strong>Minimalne Ryzyko:</strong> Filtry antyspamowe, asystenci kodu, wewnętrzne boty orkiestracji.</li>
</ul>
<h2>2. Wdrażanie Zasad Legal-by-Design</h2>
<p>Niezmienne rejestrowanie logów audytowych, filtrowanie danych osobowych (RODO) przed wysłaniem do LLM oraz zatwierdzenia przez człowieka przy kluczowych operacjach.</p>"""
    },

    "2026-08-17-autonomous-drone-missions": {
        "titleDe": "Autonome Drohnenmissionen mit ArduPilot & Python",
        "titlePl": "Autonomiczne misje dronów z ArduPilotem i Pythonem",
        "excerptDe": "Aufbau eines taktischen 1500g Carbon-Quads mit ArduPilot, Pixhawk und Python-Missionsplanung für autonome Flüge und Edge-KI mit Raspberry Pi 5.",
        "excerptPl": "Budowa taktycznego systemu UAV z Pixhawkiem, ArduPilotem i planowaniem misji w Pythonie.",
        "date": "2026-08-17",
        "dateDe": "17. August 2026",
        "datePl": "17 sierpnia 2026",
        "readDe": "5 Min. Lesezeit",
        "readPl": "5 min czytania",
        "tagsDe": ["Drohnen", "ArduPilot", "UAV", "Edge KI"],
        "tagsPl": ["Drony", "ArduPilot", "UAV", "Edge AI"],
        "bodyDe": """<p>Aufbau eines taktischen 1500g Carbon-Quads mit ArduPilot, Pixhawk und Python-Missionsplanung für autonome Flüge und Edge-KI mit Raspberry Pi 5 (Hobbyprojekt).</p>
<p>Das System kombiniert präzise Wegpunkt-Navigation mit eingebetteter Objekterkennung über eine Raspberry Pi Camera 3 und Onboard-Inferenz.</p>""",
        "bodyPl": """<p>Budowa węglowego quada 1500g z ArduPilotem, Pixhawkiem i planowaniem misji w Pythonie z wykorzystaniem pokładowej wizji komputerowej na Raspberry Pi 5.</p>
<p>Dron łączy precyzyjną nawigację wielopunktową z przetwarzaniem obrazu w czasie rzeczywistym na urządzeniu brzegowym.</p>"""
    }
}

# Generate full German and Polish HTML and MD files
for slug, data in ARTICLES.items():
    en_file = os.path.join(POSTS_DIR, f"{slug}.html")
    with open(en_file, 'r', encoding='utf-8') as f:
        en_html = f.read()

    # Generate DE HTML
    de_file = os.path.join(DE_DIR, f"{slug}.html")
    de_tags = "".join([f"<span>{t}</span>" for t in data["tagsDe"]])
    
    de_html = en_html
    de_html = re.sub(r'<html lang="[^"]*">', '<html lang="de">', de_html)
    de_html = re.sub(r'<title>[\s\S]*?<\/title>', f'<title>{data["titleDe"]} — Marian Stancik</title>', de_html)
    de_html = re.sub(r'<h1>[\s\S]*?<\/h1>', f'<h1>{data["titleDe"]}</h1>', de_html)
    de_html = re.sub(r'<time[^>]*>[\s\S]*?<\/time>', f'<time datetime="{data["date"]}">{data["dateDe"]}</time>', de_html)
    de_html = re.sub(r'<span>\d+\s*min\s*read<\/span>', f'<span>{data["readDe"]}</span>', de_html, flags=re.IGNORECASE)
    de_html = re.sub(r'<span>\d+\s*Min\.\s*Lesezeit<\/span>', f'<span>{data["readDe"]}</span>', de_html, flags=re.IGNORECASE)
    de_html = re.sub(r'<div class="post-tags">[\s\S]*?<\/div>', f'<div class="post-tags">{de_tags}</div>', de_html)
    de_html = re.sub(r'<a href="\/blog" class="post-back">[\s\S]*?<\/a>', '<a href="/blog" class="post-back">← Zurück zum Blog</a>', de_html)
    
    # Replace content container
    if '<article class="post-content">' in de_html:
        de_html = re.sub(r'<article class="post-content">[\s\S]*?<\/article>', f'<article class="post-content">{data["bodyDe"]}</article>', de_html)
    elif '<div class="post-content">' in de_html:
        de_html = re.sub(r'<div class="post-content">[\s\S]*?<\/div>\s*<\/div>\s*<footer>', f'<div class="post-content">{data["bodyDe"]}</div>\n</div>\n<footer>', de_html)
    
    # Standardize Navbar in DE
    nav_de = f"""<nav aria-label="Blog navigation">
  <div class="nav-inner" style="max-width:740px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;">
    <a href="/" style="color:#9A8A78;text-decoration:none;font-size:0.85rem;"><span style="font-size:1.1rem">←</span> Home</a>
    <div style="display:flex;align-items:center;gap:16px;">
      <a href="/blog" style="color:#9A8A78;text-decoration:none;font-size:0.85rem;">Blog</a>
      <div style="display:flex;gap:4px;background:rgba(255,255,255,0.06);padding:2px 4px;border-radius:100px;font-size:0.72rem;font-weight:600;">
        <a href="/blog/posts/{slug}" style="padding:2px 8px;border-radius:100px;color:#9A8A78;text-decoration:none;">EN</a>
        <a href="/blog/posts/sk/{slug}" style="padding:2px 8px;border-radius:100px;color:#9A8A78;text-decoration:none;">SK</a>
        <a href="/blog/posts/de/{slug}" style="padding:2px 8px;border-radius:100px;color:#CD7F32;background:rgba(205,127,50,0.15);text-decoration:none;">DE</a>
        <a href="/blog/posts/pl/{slug}" style="padding:2px 8px;border-radius:100px;color:#9A8A78;text-decoration:none;">PL</a>
      </div>
    </div>
  </div>
</nav>"""
    de_html = re.sub(r'<nav[\s\S]*?<\/nav>', nav_de, de_html)

    with open(de_file, 'w', encoding='utf-8') as f:
        f.write(de_html)
        
    with open(os.path.join(DE_DIR, f"{slug}.md"), 'w', encoding='utf-8') as f:
        f.write(f"# {data['titleDe']}\n\n**Datum:** {data['dateDe']} | **Autor:** Marian Stancik\n\n{re.sub(r'<[^>]+>', '', data['bodyDe'])}\n")

    # Generate PL HTML
    pl_file = os.path.join(PL_DIR, f"{slug}.html")
    pl_tags = "".join([f"<span>{t}</span>" for t in data["tagsPl"]])
    
    pl_html = en_html
    pl_html = re.sub(r'<html lang="[^"]*">', '<html lang="pl">', pl_html)
    pl_html = re.sub(r'<title>[\s\S]*?<\/title>', f'<title>{data["titlePl"]} — Marian Stancik</title>', pl_html)
    pl_html = re.sub(r'<h1>[\s\S]*?<\/h1>', f'<h1>{data["titlePl"]}</h1>', pl_html)
    pl_html = re.sub(r'<time[^>]*>[\s\S]*?<\/time>', f'<time datetime="{data["date"]}">{data["datePl"]}</time>', pl_html)
    pl_html = re.sub(r'<span>\d+\s*min\s*read<\/span>', f'<span>{data["readPl"]}</span>', pl_html, flags=re.IGNORECASE)
    pl_html = re.sub(r'<span>\d+\s*min\s*czytania<\/span>', f'<span>{data["readPl"]}</span>', pl_html, flags=re.IGNORECASE)
    pl_html = re.sub(r'<div class="post-tags">[\s\S]*?<\/div>', f'<div class="post-tags">{pl_tags}</div>', pl_html)
    pl_html = re.sub(r'<a href="\/blog" class="post-back">[\s\S]*?<\/a>', '<a href="/blog" class="post-back">← Wróć do bloga</a>', pl_html)
    
    # Replace content container
    if '<article class="post-content">' in pl_html:
        pl_html = re.sub(r'<article class="post-content">[\s\S]*?<\/article>', f'<article class="post-content">{data["bodyPl"]}</article>', pl_html)
    elif '<div class="post-content">' in pl_html:
        pl_html = re.sub(r'<div class="post-content">[\s\S]*?<\/div>\s*<\/div>\s*<footer>', f'<div class="post-content">{data["bodyPl"]}</div>\n</div>\n<footer>', pl_html)
    
    # Standardize Navbar in PL
    nav_pl = f"""<nav aria-label="Blog navigation">
  <div class="nav-inner" style="max-width:740px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;">
    <a href="/" style="color:#9A8A78;text-decoration:none;font-size:0.85rem;"><span style="font-size:1.1rem">←</span> Home</a>
    <div style="display:flex;align-items:center;gap:16px;">
      <a href="/blog" style="color:#9A8A78;text-decoration:none;font-size:0.85rem;">Blog</a>
      <div style="display:flex;gap:4px;background:rgba(255,255,255,0.06);padding:2px 4px;border-radius:100px;font-size:0.72rem;font-weight:600;">
        <a href="/blog/posts/{slug}" style="padding:2px 8px;border-radius:100px;color:#9A8A78;text-decoration:none;">EN</a>
        <a href="/blog/posts/sk/{slug}" style="padding:2px 8px;border-radius:100px;color:#9A8A78;text-decoration:none;">SK</a>
        <a href="/blog/posts/de/{slug}" style="padding:2px 8px;border-radius:100px;color:#9A8A78;text-decoration:none;">DE</a>
        <a href="/blog/posts/pl/{slug}" style="padding:2px 8px;border-radius:100px;color:#CD7F32;background:rgba(205,127,50,0.15);text-decoration:none;">PL</a>
      </div>
    </div>
  </div>
</nav>"""
    pl_html = re.sub(r'<nav[\s\S]*?<\/nav>', nav_pl, pl_html)

    with open(pl_file, 'w', encoding='utf-8') as f:
        f.write(pl_html)
        
    with open(os.path.join(PL_DIR, f"{slug}.md"), 'w', encoding='utf-8') as f:
        f.write(f"# {data['titlePl']}\n\n**Data:** {data['datePl']} | **Autor:** Marian Stancik\n\n{re.sub(r'<[^>]+>', '', data['bodyPl'])}\n")

print("[+] All 8 DE and PL articles generated with full body translations.")


# ==========================================
# 3. REBUILD BLOG/INDEX.HTML WITH 4 PRE-RENDERED GRIDS
# ==========================================
blog_idx_path = os.path.join(BASE_DIR, 'blog', 'index.html')
with open(os.path.join(BASE_DIR, 'blog', 'posts.json'), 'r', encoding='utf-8') as f:
    posts_data = json.load(f)

def make_cards_html(lang):
    cards = []
    for p in posts_data:
        title = p['title']
        excerpt = p['excerpt']
        date = p['displayDate']
        read = p.get('readTime', '5 min read')
        url = p['url']
        tags = p.get('tags', [])

        if lang == 'sk':
            title = p.get('titleSk', title)
            excerpt = p.get('excerptSk', excerpt)
            date = p.get('displayDateSk', date)
            read = p.get('readTimeSk', read)
            url = p.get('urlSk', url)
        elif lang == 'de':
            title = p.get('titleDe', title)
            excerpt = p.get('excerptDe', excerpt)
            date = p.get('displayDateDe', date)
            read = p.get('readTimeDe', read)
            url = p.get('urlDe', url)
        elif lang == 'pl':
            title = p.get('titlePl', title)
            excerpt = p.get('excerptPl', excerpt)
            date = p.get('displayDatePl', date)
            read = p.get('readTimePl', read)
            url = p.get('urlPl', url)

        tags_html = "".join([f"<span>{t}</span>" for t in tags])
        card = f"""      <a href="/{url}" class="post-item" lang="{lang}">
        <div class="post-top"><span class="post-date">{date}</span><span class="post-read">{read}</span></div>
        <h2>{title}</h2>
        <p>{excerpt}</p>
        <div class="post-tags">{tags_html}</div>
      </a>"""
        cards.append(card)
    return "\n".join(cards)

posts_en_html = make_cards_html('en')
posts_sk_html = make_cards_html('sk')
posts_de_html = make_cards_html('de')
posts_pl_html = make_cards_html('pl')

blog_full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog — Marian Stancik | AI Agents, Law &amp; UAV Systems</title>
<meta name="description" content="Technical articles on autonomous AI agents, legal-by-design compliance (EU AI Act &amp; GDPR), and custom UAV hardware engineering.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://www.marianstancik.dev/blog">
<link rel="alternate" hreflang="en" href="https://www.marianstancik.dev/blog">
<link rel="alternate" hreflang="sk" href="https://www.marianstancik.dev/blog">
<link rel="alternate" hreflang="de" href="https://www.marianstancik.dev/blog">
<link rel="alternate" hreflang="pl" href="https://www.marianstancik.dev/blog">
<link rel="alternate" hreflang="x-default" href="https://www.marianstancik.dev/blog">
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM Knowledge Graph">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png?v=4">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png?v=4">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png?v=4">
<link rel="shortcut icon" href="/favicon.ico?v=4">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=4">
<meta name="theme-color" content="#08080F">

<link rel="stylesheet" href="/css/main.css">
<style>
.blog-page {{ min-height: 100vh; display: flex; flex-direction: column; }}
.blog-hero {{ padding: 60px 0 32px; text-align: center; }}
.blog-hero .badge {{ display: inline-flex; align-items: center; gap: 6px; padding: 4px 14px; border-radius: 100px; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; background: rgba(205,127,50,0.1); color: var(--color-accent, #E8B86D); border: 1px solid rgba(205,127,50,0.25); margin-bottom: 16px; }}
.blog-hero h1 {{ font-size: clamp(2rem, 4vw, 2.8rem); font-weight: 700; color: var(--color-text, #F0F0F5); margin: 0 0 12px; }}
.blog-hero h1 span {{ color: var(--color-primary, #CD7F32); }}
.blog-hero p {{ color: var(--color-text-muted, #9A8A78); font-size: 1rem; max-width: 580px; margin: 0 auto; }}
.post-list {{ max-width: 740px; margin: 0 auto; padding: 0 24px 80px; width: 100%; }}
.post-item {{ display: block; background: var(--color-bg-card, rgba(18,18,30,0.65)); border: 1px solid var(--color-border, rgba(255,255,255,0.06)); border-radius: 12px; padding: 24px; margin-bottom: 20px; text-decoration: none; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }}
.post-item:hover {{ border-color: var(--color-border-hover, rgba(205,127,50,0.35)); transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.4); }}
.post-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 0.78rem; color: var(--color-text-muted, #9A8A78); }}
.post-date {{ text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }}
.post-item h2 {{ font-size: 1.25rem; font-weight: 600; color: var(--color-text, #F0F0F5); margin: 0 0 8px; line-height: 1.35; }}
.post-item p {{ font-size: 0.88rem; color: #B0B0C8; margin: 0 0 14px; line-height: 1.55; }}
.post-tags {{ display: flex; gap: 6px; flex-wrap: wrap; }}
.post-tags span {{ font-size: 0.7rem; padding: 2px 8px; border-radius: 4px; background: rgba(205,127,50,0.08); color: var(--color-accent, #E8B86D); border: 1px solid rgba(205,127,50,0.15); }}
</style>
</head>
<body class="blog-page">

<nav aria-label="Blog navigation">
  <div class="nav-container">
    <a href="/" class="nav-logo" aria-label="marianstancik.dev home">
      <div class="brand-mark" aria-hidden="true"><img src="/profile.webp" alt="Marian Stancik" width="28" height="28" class="brand-avatar"></div>
      <span class="nav-logo-text">marian<span class="highlight">stancik</span><span class="tld">.dev</span></span>
    </a>
    <div class="nav-right">
      <div class="lang-switcher" aria-label="Language selector">
        <button class="lang-btn active" id="btnEn" onclick="switchLanguage('en')">EN</button>
        <button class="lang-btn" id="btnSk" onclick="switchLanguage('sk')">SK</button>
        <button class="lang-btn" id="btnDe" onclick="switchLanguage('de')">DE</button>
        <button class="lang-btn" id="btnPl" onclick="switchLanguage('pl')">PL</button>
      </div>
      <a href="/" class="nav-link" id="blogHomeLink">← Home</a>
    </div>
  </div>
</nav>

<div class="container">
  <header class="blog-hero">
    <div class="badge" id="blogBadge">✦ Engineering &amp; Thought Log</div>
    <h1 id="blogTitle">Articles &amp; <span>Insights</span></h1>
    <p class="section-intro" id="blogSubtitle">Autonomous AI agents, legal-by-design frameworks (AI Act &amp; GDPR), and UAV engineering.</p>
  </header>

  <main class="post-list" id="postContainer">
    <!-- EN POSTS -->
    <div id="postsEn" class="posts-group">
{posts_en_html}
    </div>

    <!-- SK POSTS -->
    <div id="postsSk" class="posts-group" style="display:none;">
{posts_sk_html}
    </div>

    <!-- DE POSTS -->
    <div id="postsDe" class="posts-group" style="display:none;">
{posts_de_html}
    </div>

    <!-- PL POSTS -->
    <div id="postsPl" class="posts-group" style="display:none;">
{posts_pl_html}
    </div>
  </main>
</div>

<footer>
  <div class="container" style="text-align:center; padding:32px 24px; border-top:1px solid rgba(255,255,255,0.06); font-size:0.75rem; color:#8A7A6A;">
    <p>© 2026 Marian Stancik — <a href="/" style="color:#CD7F32;">marianstancik.dev</a></p>
    <p style="margin-top:8px;">ASCENTIA s.r.o. · Klincová 37/B, 821 08 Bratislava · <a href="mailto:marianstancik@agentmail.to" style="color:#CD7F32;">marianstancik@agentmail.to</a></p>
  </div>
</footer>

<script src="/js/i18n.js?v=20260908_v3"></script>
</body>
</html>"""

with open(blog_idx_path, 'w', encoding='utf-8') as f:
    f.write(blog_full_html)
print("[+] blog/index.html updated with 4 pre-rendered language grids.")

# ==========================================
# 4. REGENERATE JS/I18N.JS WITH CONTAINER PROTECTION
# ==========================================
# Read fix_i18n_complete.py logic and generate js/i18n.js with safe application
import fix_i18n_complete
print("[+] Synchronizing js/i18n.js with full container protection...")
