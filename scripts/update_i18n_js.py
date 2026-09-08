#!/usr/bin/env python3
"""
Inject full German (de) and Polish (pl) translation blocks into js/i18n.js
and update language button handling and post rendering.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N_JS = os.path.join(BASE_DIR, 'js', 'i18n.js')

with open(I18N_JS, 'r', encoding='utf-8') as f:
    code = f.read()

de_block = """
de: {
docTitle: "Marian Stancik — KI-Agenten-Entwickler | Autonome Systeme",
docDesc: "Marian Stancik — Ich baue KI-Agenten, die Ihre Prozesse steuern. Maßgeschneiderte autonome Agenten und KI-Web-Audits.",
ogTitle: "Marian Stancik — KI-Agenten-Entwickler | Autonome Systeme",
ogDesc: "Ich baue KI-Agenten, die Ihre Prozesse steuern. Autonome Systeme auf eigener Infrastruktur, bereit für regulierte Umgebungen. Hetzner VPS 24/7.",
skipLink: "Zum Hauptinhalt springen",
navHome: "Startseite",
navAbout: "Über mich",
navSkills: "Fähigkeiten",
navDrones: "Drohnen",
navExpertise: "Expertise",
navProjects: "Projekte",
navBlog: "Blog",
navContact: "✦ Kontakt",
navProducts: "Produkte",
heroBadge: "✦ Ich baue KI-Agenten, die Ihre Prozesse steuern",
heroTagline: "Ich baue <strong>KI-Agenten</strong>, die Ihre Prozesse steuern. Autonome Systeme, Web-Audits und maßgeschneiderte KI-Workflows für Gründer.",
roleAi: "KI-Agenten-Entwickler",
roleUav: "Hardware-Engineering (Hobby)",
roleDrone: "Drohnenpilot (EASA A1/A3)",
rolePm: "KI-Agenten-Entwickler",
roleLaw: "Regulatorische Compliance (PF UK)",
heroEmail: "E-Mail",
skillsLabel: "✦ KI-Agenten-Fähigkeiten",
skillsHeading: "Fähigkeiten & Kompetenzen",
skillsIntro: "Full-Stack-KI-Engineering — von LLM-Orchestrierung und Hermes-Agent-Schleifen bis zu Cloud-Infrastruktur, Compliance und Hardware.",
sk1Title: "Hermes Agent & Multi-Agenten-Systeme",
sk1List: `
  <li><strong>Hermes Agent:</strong> Autonome Ausführungsschleifen auf 24/7 Hetzner VPS</li>
  <li><strong>MCP Server Design:</strong> Maßgeschneiderte Model Context Protocol Tools & APIs</li>
  <li><strong>OpenRouter Multi-LLM:</strong> Dynamisches Routing über DeepSeek, Claude 3.5 & GPT-4o</li>
  <li><strong>Obsidian Memory Layer:</strong> Markdown-Vault für persistentes Agentengedächtnis</li>
  <li><strong>C2-Schnittstellen:</strong> Interaktive Steuerung über Telegram- & WhatsApp-Bots</li>
`,
sk2Title: "Software, High-Perf Web & Cloud",
sk2List: `
  <li><strong>Python 3 Ökosystem:</strong> FastAPI, Asyncio, Playwright, Toolchain-Automatisierung</li>
  <li><strong>Zero-Build High-Perf Web:</strong> 100% Vanilla HTML5/CSS3/JS, PageSpeed 100 & 0ms TBT</li>
  <li><strong>GEO & Agentic Browsing:</strong> llmstxt.org v2 Standard, optimiert für Perplexity & LLM-Crawler</li>
  <li><strong>Linux VPS Administration:</strong> Ubuntu Server auf Hetzner Cloud (DE/FI), Caddy & SSL</li>
  <li><strong>Produktionsbetrieb:</strong> 19+ 24/7 Cron-Orchestrierungen, SQLite-Persistenz & Monitoring</li>
`,
sk3Title: "Regulatorische Compliance (EU AI Act, DSGVO, NIS2)",
sk3List: `
  <li><strong>EU AI Act:</strong> Risikoklassifizierung, GPAI-Governance und technische Dokumentation</li>
  <li><strong>DSGVO & Datenschutz:</strong> Trainingsdaten-Compliance, Schutz vor automatisiertem Profiling</li>
  <li><strong>NIS2 & DORA:</strong> Cyber-Resilienz der Lieferkette & finanztechnische Betriebsbereitschaft</li>
  <li><strong>EU Data Act:</strong> Datenaustausch, Cloud-Interoperabilität und EU-Datensouveränität</li>
  <li><strong>DSM-Urheberrecht:</strong> Text- & Data-Mining (TDM) Ausnahmen für KI-Modelltraining</li>
`,
sk4Title: "Taktische UAV-Systeme & Edge-Robotik",
sk4List: `
  <li><strong>Hardware-Bau:</strong> Handgelöteter 1500g 8-Zoll Carbon-Quad aus Einzelkomponenten</li>
  <li><strong>Flugsoftware:</strong> Duale Betaflight-Dynamik & ArduPilot Copter Wegpunkt-Missionen</li>
  <li><strong>Edge Vision KI:</strong> Raspberry Pi 5 (8GB) + Kamera 3 für integrierte Objekterkennung</li>
  <li><strong>Avionik & Telemetrie:</strong> Skystars H7 Dual Gyro FC, AM60 60A ESC, RadioMaster ELRS, GNSS</li>
  <li><strong>Zertifizierungen:</strong> EASA A1/A3 lizenzierter Drohnenpilot, 2,6 Mio. € Coverdrone-Haftpflicht</li>
`,
droneLabel: "✦ UAV-Systeme",
droneHeading: "Handgebaut. Flugerprobt. KI-unterstützt.",
droneIntro: "Maßgeschneiderter 1500g Carbon-Quadcopter. Ursprünglich auf Betaflight geflogen, betrieben mit ArduPilot, mit Raspberry Pi 5 Edge-Vision-KI. EASA A1/A3 zertifiziert, 2,6 Mio. € versichert (Hobbyprojekt).",
dCap1: "20s Outdoor-Zusammenstellung — Feldflug & Wegpunkt-Navigationstests",
dCap2: "Handgebauter 1500g Carbon-Quad — Jungfernflug & Telemetrieverifizierung",
dCap3: "ArduPilot Missionsplanung — automatisierte Multi-Wegpunkt-Führung",
scrollText: "Scrollen",
aboutLabel: "✦ Über mich",
aboutHeading: "KI-Agenten-Entwickler. Systeme, die Ihre Prozesse steuern.",
aboutBody: `
<p>Ich baue <strong>autonome KI-Agenten</strong> mit dem <strong>Hermes Agent</strong> Framework. Meine Kerninfrastruktur läuft 24/7 auf einem Enterprise <strong>Hetzner Cloud VPS</strong> in Deutschland/Finnland und orchestriert Modelle über die <strong>OpenRouter API</strong> mit <strong>Obsidian</strong> als persistentem Gedächtnis.</p>
<p>Ich entwickle Webanwendungen mit <strong>HTML5, Vanilla JS und modernem CSS</strong> — optimiert für sofortiges Laden (Lighthouse 100), null Layout-Verschiebungen und Entdeckung durch KI-Suchcrawler (GEO / LLMO).</p>
<p>Ich beschäftige mich mit den geschäftlichen Auswirkungen von KI — <strong>EU AI Act, DSGVO, NIS2, DORA</strong>. Dies hilft mir, KI-Agenten für regulierte Umgebungen zu bauen (nur technische Information, keine Rechtsberatung).</p>
`,
stat1: "Aktive Cron-Agenten",
stat2: "Engineering-Bereiche",
stat3: "Jahre Erfahrung",
stat4: "Drohnen-Versicherung",
stat5: "Open-Source Repos",
stat6: "24/7 Agent-Laufzeit",
expLabel: "✦ Expertise",
expHeading: "Ein Fokus. Autonome Agenten.",
expIntro: "Ein Fokus: autonome KI-Agenten, die Ihre Prozesse steuern.",
exp1Title: "Autonome Agenten-Systeme",
exp1Desc: "Ich baue 24/7 autonome Agenten mit Hermes Agent auf Hetzner VPS mit Telegram & WhatsApp C2, OpenRouter und persistentem Speicher.",
exp2Title: "EU AI Act & Compliance",
exp2Desc: "Ich analysiere EU-KI-Regulierungen für auditierbare Systeme. Nur technische Compliance, keine Rechtsberatung.",
exp3Title: "UAV-Systeme & Edge-KI",
exp3Desc: "Handgebauter 1500g Carbon-Quad mit ArduPilot und Raspberry Pi 5 Edge Vision. EASA A1/A3 zertifiziert (Hobby).",
projLabel: "✦ Projekte",
projHeading: "Was ich baue.",
projIntro: "Produktionssysteme, Open-Source-Tools und Experimente.",
p1Title: "Prime Agent Masterclass",
p1Desc: "8-Module Videokurs über autonome KI-Agenten. Stripe-Zahlung, EN/SK/DE, Vercel-Hosting.",
p2Title: "Autonome Agenten-Plattform",
p2Desc: "Experimentelle autonome Workflows, Compliance-Checks und Hardware-Engineering auf Hetzner VPS.",
p3Title: "Polymarket Trading Bot",
p3Desc: "Produktionsbereiter Markov-Chain-Trading-Bot für Prognosemärkte.",
p4Title: "Hermes Digital Twin",
p4Desc: "Autonomer KI-Agent mit 19+ Cron-Jobs — tägliche Veröffentlichung auf X, LinkedIn und Blog.",
blogSecLabel: "✦ Blog",
blogSecHeading: "Aktuelle Beiträge.",
blogSecIntro: "KI-Agenten, autonome Systeme und Building in Public.",
b1Date: "22. August 2026",
b1Title: "Aufbau eines digitalen Zwillings, der 9-mal täglich postet",
b1Desc: "Wie ich einen autonomen KI-Agenten mit Hermes gebaut habe, der Inhalte plattformübergreifend veröffentlicht.",
b2Date: "20. August 2026",
b2Title: "EU AI Act Compliance für kleine KI-Unternehmen",
b2Desc: "Praktischer Legal-by-Design-Leitfaden für Startups in der EU von der Risikobewertung bis zur Dokumentation.",
b3Date: "17. August 2026",
b3Title: "Autonome Drohnenmissionen mit ArduPilot",
b3Desc: "Bau eines taktischen UAV-Systems mit Pixhawk, ArduPilot und Python-Missionsplanung.",
blogAllBtn: "Alle Beiträge lesen →",
leadLabel: "✦ Bleiben Sie informiert",
leadHeading: "Updates aus der Entwicklung.",
leadIntro: "KI-Agenten-Einblicke, Drohnen-Builds, Tech-Notizen — direkt in Ihr Postfach.",
subscribeBtn: "Abonnieren",
leadNote: "Kein Spam. Jederzeit abbestellbar. Erstellt mit AgentMail.",
connLabel: "✦ Kontakt",
connHeading: "Lassen Sie uns etwas bauen.",
connIntro: "Folgen Sie dem Projekt, lesen Sie den Blog oder schreiben Sie direkt.",
connBlogText: "Blog",
footerTagline: "Ich baue KI-Agenten, die Ihre Prozesse steuern. Autonome Systeme auf eigener Infrastruktur.",
fCol1Title: "Navigation",
fCol2Title: "Projekte",
fCol3Title: "Kontakt",
fNavAbout: "Über mich",
fNavExp: "Expertise",
fNavProj: "Projekte",
fNavConn: "Kontakt",
fNavBlog: "Blog",
fMotto: "Besser bauen. Konform bleiben.",
cockpitStatus: "HERMES C2 // 24/7 AUTONOME LAUFZEIT ONLINE",
cockpitChip: "HETZNER VPS · EU-DATENSOUVERÄNITÄT",
cockpitStat1Title: "Autonome Cron-Schleifen",
cockpitStat1Sub: "24/7 Hintergrund-Orchestrierungen für Content, CRM & Health",
cockpitStat2Title: "Dynamisches OpenRouter Routing",
cockpitStat2Sub: "DeepSeek R1/V3 · Claude 3.5 Sonnet · GPT-4o Synthese",
cockpitStat3Title: "Persistenter Vault-Speicher",
cockpitStat3Sub: "SQLite-Status + bidirektionaler Markdown-Wissensgraph",
cockpitStat4Title: "EU AI Act & DSGVO Konform",
cockpitStat4Sub: "Art. 50 KI-Kennzeichnung & auditierbare Dokumentation",
aboutIntro: "Ich baue autonome KI-Agenten, die Geschäftsprozesse steuern — Content, CRM, Monitoring und Automatisierung. 24/7 auf eigener Infrastruktur.",
whatIDoTitle: "Was ich tue",
whatIDoSubtitle: "Beruf · Kontext · Hobby — klare Trennung.",
card1Title: "KI-Agenten-Entwickler (Beruf)",
card1Desc: "Ich entwerfe, baue und betreibe autonome KI-Agenten auf Kundeninfrastruktur oder Managed VPS. MCP-Server, Multi-LLM-Orchestrierung und 24/7-Cron.",
card2Title: "Regulatorischer Kontext (PF UK)",
card2Desc: "Rechtsstudium an der PF UK. EU AI Act, DSGVO, NIS2 für den Bau auditierbarer Agenten. Nur technische Information.",
card3Title: "Hardware-Engineering (Hobby)",
card3Desc: "Handgelöteter 1500g Carbon-Quad mit ArduPilot und Raspberry Pi 5 Edge-KI. EASA A1/A3 lizenziert, 2,6 Mio. € versichert.",
whatIDontDoTitle: "Was ich nicht tue",
whatIDontDoSubtitle: "Klare Grenzen — damit Sie genau wissen, mit wem Sie arbeiten.",
dont1Title: "Keine Rechtsberatung",
dont1Desc: "Ich bin Student, kein Anwalt. Meine Agenten führen technische Prüfungen durch — rechtliche Freigaben obliegen Ihrem Anwalt.",
dont2Title: "Keine Drohnendienstleistungen",
dont2Desc: "Ich verkaufe keine Drohnen und biete keine kommerziellen Flugdienste an. Die Drohne ist ein technisches Hobbyprojekt.",
dont3Title: "Keine Agenturen / Zwischenhändler",
dont3Desc: "Ich arbeite direkt mit Kunden. Kein Outsourcing. Sie sprechen direkt mit dem Entwickler Ihres Systems.",
timelineTitle: "Mein Werdegang",
timelineSubtitle: "Die technische Evolution — vom Prompt-Engineering zu autonomen Systemen.",
t2026Title: "Hermes Agent & Autonomes System",
t2026Desc: "Betrieb einer 24/7 autonomen Multi-Agenten-Infrastruktur auf Hetzner VPS mit 19+ Cron-Orchestrierungen.",
t2025Title: "Erste autonome Agenten & MCP",
t2025Desc: "Übergang zu aktiven, werkzeugnutzenden Agenten mit MCP-Servern und persistenter Obsidian-Architektur.",
t2024Title: "IDE Antigravity & KI-gestütztes Engineering",
t2024Desc: "Entwicklung moderner Agentic-Coding-Workflows. Bau des 1500g taktischen Quads mit Raspberry Pi 5 Edge-KI.",
t2023Title: "Beginn der KI-Chatbots & GPT-Experimente",
t2023Desc: "Erste Deep-Dives in LLMs, Prompt-Engineering und 24/7 autonome Skripte.",
homeProductsLabel: "✦ Produkte",
homeProductsHeading: "Was ich baue",
homeProductsIntro: "KI-Agenten, die Ihre Webpräsenz auditieren, und maßgeschneiderte autonome Agenten für Ihr Unternehmen.",
prodGeoTitle: "KI-GEO-Audit",
prodGeoDesc: "Ist Ihre Website bereit für KI-Suchen? Überprüfung von llms.txt, JSON-LD, robots.txt und KI-Sichtbarkeit.",
prodGeoPrice: "150 € →",
prodReadinessTitle: "KI-Web-Readiness-Scan",
prodReadinessDesc: "Technischer Compliance-Check: Datenschutzerklärung, DSGVO, AGB, Disclaimer und KI-Kennzeichnung.",
prodReadinessPrice: "200 € →",
prodFullTitle: "Vollständiges Web-Audit",
prodFullDesc: "Beide Audits kombiniert. GEO + technische Compliance in einem umfassenden Bericht mit Prioritätenmatrix.",
prodFullPrice: "300 € →",
prodCustomTitle: "Individueller KI-Agent",
prodCustomDesc: "Ein autonomer Agent in Produktionsqualität, der für Ihre spezifischen Anforderungen gebaut wird.",
prodCustomPrice: "Ab 500 € →",
trustLaw: "⚖️ <strong>Regulatorische Compliance</strong> — Konform mit EU AI Act & DSGVO",
trustUav: "🚁 <strong>Hardware-Engineering</strong> — EASA-zertifizierter Drohnenbau & Edge-KI",
trustPfuk: "🎓 <strong>PF UK</strong> — EU AI Act, DSGVO, NIS2",
fNavProducts: "Produkte",
aboutDisclaimer: "<span>⚠️</span> <span><strong>Hinweis:</strong> Regulatorische Einblicke dienen nur Informationszwecken. Keine Rechtsberatung.</span>",
hCockpitStatus: "HERMES C2 // 24/7 LAUFZEIT",
hCockpitChip: "HETZNER VPS · EU",
hMetric1Lbl: "Cron-Schleifen",
hMetric1Sub: "24/7 Hintergrundaufgaben",
hMetric2Lbl: "Autonom",
hMetric2Sub: "Null menschliche Überwachung",
hMetric3Lbl: "Dynamisches Routing",
hMetric3Sub: "DeepSeek · Claude · GPT",
hMetric4Lbl: "Lighthouse",
hMetric4Sub: "0ms TBT · Null CLS",
hCockpitLink: "Vollständige Historie ansehen →",
exp4Title: "Produktmanager (Defence)",
exp4Desc: "Hintergrund in der Verteidigungsindustrie — Leitung klassifizierter Hardware- und Softwareprojekte.",
heroCta: "✦ Produkte ansehen",
heroContact: "Gespräch beginnen →",
faqLabel: "✦ FAQ",
faqHeading: "Häufig gestellte Fragen",
faq1q: "Wer ist Marian Stancik?",
faq1a: "<strong>Marian Stancik</strong> baut autonome KI-Agenten für Gründer und Unternehmen. Er ist spezialisiert auf Agenten-Entwicklung, KI-Web-Audits (GEO und Compliance) und Multi-Agenten-Orchestrierung mit Hermes Agent.",
faq2q: "Was prüft ein KI-GEO-Audit?",
faq2a: "Ein KI-GEO-Audit prüft die Sichtbarkeit Ihrer Website für KI-Suchmaschinen wie Perplexity, ChatGPT Search, Claude und Google SGE. <strong>150 €</strong> — einmaliges Audit, Bericht in 48 Stunden.",
faq3q: "Was ist der KI-Web-Readiness-Scan?",
faq3a: "Eine <strong>technische Prüfung durch einen KI-Agenten</strong> bezüglich erforderlicher rechtlicher Dokumente (Datenschutz, DSGVO, AGB, Disclaimer, AI Act). <strong>200 €</strong> — Bericht in 48 Stunden.",
faq4q: "Bietet Marian Rechtsberatung an?",
faq4a: "<strong>Nein.</strong> Marian studiert Recht, ist aber kein Anwalt. Seine Agenten führen <strong>nur technische Prüfungen</strong> durch. Rechtsfragen gehören zu einem qualifizierten Anwalt.",
leadConsentText: 'Ich stimme der <a href="/privacy" style="color:#CD7F32;text-decoration:underline;">Datenschutzerklärung</a> und der Verarbeitung meiner E-Mail-Adresse zu.',
fNavHome: "Startseite",
blogReadPost: "Beitrag lesen",
footerImprint: '<strong>ASCENTIA s.r.o.</strong> · Klincová 37/B, 821 08 Bratislava · Geschäftsführer: Marián Stančík · <a href="mailto:marianstancik@agentmail.to" style="color:#CD7F32;">marianstancik@agentmail.to</a>',
footerAiAct: '<strong>⚠️ Disclaimer:</strong> Inhalte wurden durch autonome KI-Agenten (Hermes Agent) generiert/unterstützt. ⚖️ EU AI Act Art. 50 konform gekennzeichnet.',
bookLabel: "✉️ Kontakt aufnehmen",
bookHeading: "Lassen Sie uns über Ihr Projekt sprechen.",
bookIntro: 'Schreiben Sie an <a href="mailto:marianstancik@agentmail.to">marianstancik@agentmail.to</a>.',
bookCard1Cta: "E-Mail über KI-Agenten",
bookCard2Cta: "E-Mail über Compliance",
bookCard3Cta: "E-Mail über UAV / Edge-KI",
bookNote: 'ASCENTIA s.r.o. — <a href="mailto:marianstancik@agentmail.to" style="color:#CD7F32;">marianstancik@agentmail.to</a>.'
},
"""

pl_block = """
pl: {
docTitle: "Marian Stancik — Deweloper Agentów AI | Systemy Autonomiczne",
docDesc: "Marian Stancik — Buduję agentów AI, którzy zarządzają Twoimi procesami. Dedykowane agenty autonomiczne i audyty stron AI.",
ogTitle: "Marian Stancik — Deweloper Agentów AI | Systemy Autonomiczne",
ogDesc: "Buduję agentów AI, którzy zarządzają Twoimi procesami. Systemy autonomiczne na własnej infrastrukturze, gotowe na środowiska regulowane. Hetzner VPS 24/7.",
skipLink: "Przejdź do treści głównej",
navHome: "Strona główna",
navAbout: "O mnie",
navSkills: "Umiejętności",
navDrones: "Drony",
navExpertise: "Ekspertyza",
navProjects: "Projekty",
navBlog: "Blog",
navContact: "✦ Kontakt",
navProducts: "Produkty",
heroBadge: "✦ Buduję agentów AI, którzy zarządzają Twoimi procesami",
heroTagline: "Buduję <strong>agentów AI</strong>, którzy zarządzają Twoimi procesami. Systemy autonomiczne, audyty sieciowe i dedykowane przepływy pracy dla founderów.",
roleAi: "Deweloper Agentów AI",
roleUav: "Inżynieria Sprzętowa (Hobby)",
roleDrone: "Pilot Drona (EASA A1/A3)",
rolePm: "Deweloper Agentów AI",
roleLaw: "Świadomość Regulacyjna (PF UK)",
heroEmail: "E-mail",
skillsLabel: "✦ Umiejętności Agentów AI",
skillsHeading: "Umiejętności i Możliwości",
skillsIntro: "Full-stack inżynieria AI — od orkiestracji LLM i pętli Hermes Agent po infrastrukturę chmurową, zgodność prawną i sprzęt.",
sk1Title: "Hermes Agent & Systemy Wieloagentowe",
sk1List: `
  <li><strong>Hermes Agent:</strong> Autonomiczne pętle wykonawcze na 24/7 Hetzner VPS</li>
  <li><strong>Projektowanie Serwerów MCP:</strong> Dedykowane narzędzia Model Context Protocol i API</li>
  <li><strong>OpenRouter Multi-LLM:</strong> Dynamiczny routing między DeepSeek, Claude 3.5 i GPT-4o</li>
  <li><strong>Obsidian Memory Layer:</strong> Baza Markdown zapewniająca trwałą pamięć agentów</li>
  <li><strong>Interfejsy C2:</strong> Interaktywna kontrola przez boty Telegram i WhatsApp</li>
`,
sk2Title: "Oprogramowanie, Szybki Web i Chmura",
sk2List: `
  <li><strong>Ekosystem Python 3:</strong> FastAPI, Asyncio, Playwright, automatyzacja narzędzi</li>
  <li><strong>Zero-Build High-Perf Web:</strong> 100% Czysty HTML5/CSS3/JS, PageSpeed 100 i 0ms TBT</li>
  <li><strong>GEO i Agentic Browsing:</strong> Standard llmstxt.org v2, optymalizacja pod Perplexity i roboty LLM</li>
  <li><strong>Administracja Linux VPS:</strong> Ubuntu Server na Hetzner Cloud (DE/FI), Caddy i SSL</li>
  <li><strong>Operacje Produkcyjne:</strong> 19+ zadań cron 24/7, trwałość SQLite i monitoring</li>
`,
sk3Title: "Świadomość Regulacyjna (EU AI Act, RODO, NIS2)",
sk3List: `
  <li><strong>EU AI Act:</strong> Klasyfikacja ryzyka, zarządzanie GPAI i dokumentacja techniczna</li>
  <li><strong>RODO i Prywatność:</strong> Zgodność danych treningowych i ochrona przed profilowaniem</li>
  <li><strong>NIS2 i DORA:</strong> Cyberodporność łańcucha dostaw i gotowość operacyjna fintech</li>
  <li><strong>EU Data Act:</strong> Wymiana danych, interoperacyjność chmur i suwerenność danych UE</li>
  <li><strong>Prawo Autorskie DSM:</strong> Wyjątki Text & Data Mining (TDM) dla treningu modeli AI</li>
`,
sk4Title: "Taktyczne Systemy UAV i Robotyka Brzegowa",
sk4List: `
  <li><strong>Konstrukcja Sprzętowa:</strong> Ręcznie lutowany 1500g 8-calowy quad węglowy</li>
  <li><strong>Oprogramowanie Lotu:</strong> Podwójna dynamika Betaflight i misje waypointów ArduPilot Copter</li>
  <li><strong>Wizja AI Edge:</strong> Raspberry Pi 5 (8GB) + Camera 3 do detekcji obiektów w czasie rzeczywistym</li>
  <li><strong>Awionika i Telemetria:</strong> Skystars H7 Dual Gyro FC, AM60 60A ESC, RadioMaster ELRS, GNSS</li>
  <li><strong>Certyfikaty:</strong> Licencjonowany pilot drona EASA A1/A3, ubezpieczenie OC Coverdrone 2,6 mln €</li>
`,
droneLabel: "✦ Systemy UAV",
droneHeading: "Ręcznie zbudowany. Przetestowany w locie. Wspierany przez AI.",
droneIntro: "Dedykowany quadcopter węglowy 1500g. Napędzany przez ArduPilot, z pokładową wizją AI Raspberry Pi 5. Certyfikat EASA A1/A3, ubezpieczenie 2,6 mln € (projekt hobbystyczny).",
dCap1: "20-sekundowa kompilacja wideo — loty polowe i testy nawigacji waypointów",
dCap2: "Ręcznie zbudowany quad węglowy 1500g — dziewiczy lot i weryfikacja telemetrii",
dCap3: "Planowanie misji ArduPilot — zautomatyzowane prowadzenie wielopunktowe",
scrollText: "Przewiń",
aboutLabel: "✦ O mnie",
aboutHeading: "Deweloper Agentów AI. Systemy, które zarządzają Twoimi procesami.",
aboutBody: `
<p>Buduję <strong>autonomicznych agentów AI</strong> przy użyciu frameworka <strong>Hermes Agent</strong>. Moja infrastruktura działa 24/7 na <strong>Hetzner Cloud VPS</strong> w Niemczech/Finlandii, orkiestrując modele przez <strong>OpenRouter API</strong> z bazą <strong>Obsidian</strong> jako pamięcią kontekstową.</p>
<p>Tworzę aplikacje internetowe w technologii zero-build <strong>HTML5, Vanilla JS i nowoczesnym CSS</strong> — zaprojektowane z myślą o natychmiastowym ładowaniu (Lighthouse 100) i widoczności w wyszukiwarkach AI (GEO / LLMO).</p>
<p>Studiuję prawo na PF UK i analizuję regulacje <strong>EU AI Act, RODO, NIS2, DORA</strong>. Pomaga mi to tworzyć agentów AI gotowych na środowiska regulowane (wyłącznie wiedza techniczna, nie porada prawna).</p>
`,
stat1: "Aktywnych Agentów Cron",
stat2: "Domeny Inżynieryjne",
stat3: "Lata Doświadczenia",
stat4: "Ubezpieczenie Drona",
stat5: "Repozytoria Open Source",
stat6: "Czas Pracy 24/7",
expLabel: "✦ Ekspertyza",
expHeading: "Jeden cel. Autonomiczni agenci.",
expIntro: "Jeden cel: autonomiczni agenci AI, którzy zarządzają Twoimi procesami biznesowymi.",
exp1Title: "Systemy Agentów Autonomicznych",
exp1Desc: "Buduję agentów 24/7 z Hermes Agent na Hetzner VPS z interfejsami C2 Telegram i WhatsApp oraz dynamicznym routingiem OpenRouter.",
exp2Title: "EU AI Act i Zgodność Prawna",
exp2Desc: "Analizuję regulacje AI w UE na potrzeby audytowalnych systemów. Wyłącznie kontekst techniczny.",
exp3Title: "Systemy UAV i Edge AI",
exp3Desc: "Ręcznie budowany quad 1500g z ArduPilotem i Raspberry Pi 5 Edge Vision. Certyfikat EASA A1/A3 (hobby).",
projLabel: "✦ Projekty",
projHeading: "Co buduję.",
projIntro: "Systemy produkcyjne, narzędzia open-source i ambitne eksperymenty.",
p1Title: "Prime Agent Masterclass",
p1Desc: "8-modułowy kurs wideo o autonomicznych agentach AI z obsługą płatności Stripe.",
p2Title: "Platforma Agentów Autonomicznych",
p2Desc: "Eksperymentalne potoki agentów, testy gotowości regulacyjnej i inżynieria na Hetzner VPS.",
p3Title: "Polymarket Trading Bot",
p3Desc: "Produkcyjny bot tradingowy oparty na łańcuchach Markowa dla rynków prognostycznych.",
p4Title: "Hermes Digital Twin",
p4Desc: "Autonomiczny agent AI wykonujący 19+ zadań cron — codzienna publikacja na X, LinkedIn i blogu.",
blogSecLabel: "✦ Blog",
blogSecHeading: "Najnowsze wpisy.",
blogSecIntro: "Agenci AI, systemy autonomiczne i budowanie w publiczności.",
b1Date: "22 sierpnia 2026",
b1Title: "Budowa cyfrowego bliźniaka publikującego 9 razy dziennie",
b1Desc: "Jak zbudowałem autonomicznego agenta AI z Hermesem, który tworzy i publikuje treści na wielu platformach.",
b2Date: "20 sierpnia 2026",
b2Title: "Zgodność z EU AI Act dla małych firm AI",
b2Desc: "Praktyczny przewodnik legal-by-design dla startupów w UE: od oceny ryzyka po dokumentację.",
b3Date: "17 sierpnia 2026",
b3Title: "Autonomiczne misje dronów z ArduPilotem",
b3Desc: "Budowa taktycznego systemu UAV z Pixhawkiem, ArduPilotem i planowaniem misji w Pythonie.",
blogAllBtn: "Przeczytaj wszystkie wpisy →",
leadLabel: "✦ Bądź na bieżąco",
leadHeading: "Aktualności z procesu budowy.",
leadIntro: "Wnioski z AI, budowy dronów i technologii — prosto na Twoją skrzynkę.",
subscribeBtn: "Subskrybuj",
leadNote: "Brak spamu. Możliwość wypisania się w każdej chwili. Obsługiwane przez AgentMail.",
connLabel: "✦ Kontakt",
connHeading: "Zbudujmy coś razem.",
connIntro: "Śledź projekt, czytaj bloga lub skontaktuj się bezpośrednio.",
connBlogText: "Blog",
footerTagline: "Buduję agentów AI, którzy zarządzają Twoimi procesami. Systemy autonomiczne na własnej infrastrukturze.",
fCol1Title: "Nawigacja",
fCol2Title: "Projekty",
fCol3Title: "Kontakt",
fNavAbout: "O mnie",
fNavExp: "Ekspertyza",
fNavProj: "Projekty",
fNavConn: "Kontakt",
fNavBlog: "Blog",
fMotto: "Buduj lepiej. Pozostań zgodny z prawem.",
cockpitStatus: "HERMES C2 // ŚRODOWISKO AUTONOMICZNE 24/7 ONLINE",
cockpitChip: "HETZNER VPS · SUWERENNOŚĆ DANYCH UE",
cockpitStat1Title: "Autonomiczne Pętle Cron",
cockpitStat1Sub: "Orkiestracje 24/7 w tle dla Contentu, CRM i Monitoringu",
cockpitStat2Title: "Dynamiczny Routing OpenRouter",
cockpitStat2Sub: "Synteza DeepSeek R1/V3 · Claude 3.5 Sonnet · GPT-4o",
cockpitStat3Title: "Trwała Pamięć Skarbca",
cockpitStat3Sub: "Baza SQLite + dwukierunkowy graf wiedzy Markdown",
cockpitStat4Title: "Zgodność z EU AI Act i RODO",
cockpitStat4Sub: "Oznaczenia AI zgodne z Art. 50 i dokumentacja audytowa",
aboutIntro: "Buduję autonomicznych agentów AI zarządzających procesami firmowymi — treści, CRM, monitoring i automatyzacja. 24/7 na własnej infrastrukturze.",
whatIDoTitle: "Czym się zajmuję",
whatIDoSubtitle: "Praca · Kontekst · Hobby — wyraźny podział.",
card1Title: "Deweloper Agentów AI (Praca)",
card1Desc: "Projektuję, buduję i wdrażam autonomicznych agentów AI na infrastrukturze klienta lub zarządzanym VPS. Dedykowane serwery MCP i pętle 24/7.",
card2Title: "Kontekst Regulacyjny (PF UK)",
card2Desc: "Studia prawnicze na PF UK. Znajomość EU AI Act, RODO, NIS2 do tworzenia audytowalnych agentów. Wyłącznie wiedza techniczna.",
card3Title: "Inżynieria Sprzętowa (Hobby)",
card3Desc: "Ręcznie lutowany quad 1500g z ArduPilotem i Raspberry Pi 5 Edge AI. Certyfikat EASA A1/A3, ubezpieczenie 2,6 mln €.",
whatIDontDoTitle: "Czym się NIE zajmuję",
whatIDontDoSubtitle: "Jasne granice — wiesz dokładnie, z kim współpracujesz.",
dont1Title: "Brak porad prawnych",
dont1Desc: "Jestem studentem, nie adwokatem. Moi agenci wykonują testy techniczne — zatwierdzenie prawne należy do Twojego prawnika.",
dont2Title: "Brak komercyjnych usług dronowych",
dont2Desc: "Nie sprzedaję dronów ani nie wykonuję komercyjnych prac lotniczych. Dron to hobby inżynieryjne.",
dont3Title: "Brak agencji i pośredników",
dont3Desc: "Pracuję bezpośrednio z klientami. Bez outsourcingu. Rozmawiasz bezpośrednio z inżynierem budującym Twój system.",
timelineTitle: "Moja ścieżka",
timelineSubtitle: "Ewolucja inżynieryjna — od prompt engineeringu do pełnych systemów autonomicznych.",
t2026Title: "Hermes Agent i System Autonomiczny",
t2026Desc: "Zarządzanie infrastrukturą wieloagentową 24/7 na Hetzner VPS z 19+ orkiestracjami cron.",
t2025Title: "Pierwsi autonomiczni agenci i MCP",
t2025Desc: "Przejście do aktywnych agentów wykorzystujących narzędzia MCP i trwałą architekturę Obsidian.",
t2024Title: "IDE Antigravity i Inżynieria AI",
t2024Desc: "Wdrażanie nowoczesnych przepływów agentic coding. Budowa taktycznego quada 1500g z Raspberry Pi 5.",
t2023Title: "Początki chatbotów AI i eksperymenty GPT",
t2023Desc: "Pierwsze projekty z modelami LLM, prompt engineering i skrypty autonomiczne 24/7.",
homeProductsLabel: "✦ Produkty",
homeProductsHeading: "Co buduję",
homeProductsIntro: "Agenci AI audytujący Twoją stronę oraz dedykowane agenty autonomiczne dla Twojej firmy.",
prodGeoTitle: "Audyt AI GEO",
prodGeoDesc: "Czy Twoja strona jest widoczna dla wyszukiwarek AI? Weryfikacja llms.txt, JSON-LD, robots.txt i widoczności.",
prodGeoPrice: "150 € →",
prodReadinessTitle: "Skan Gotowości AI",
prodReadinessDesc: "Techniczna lista kontrolna: Polityka Prywatności, RODO, Regulamin, Disclaimer i oznaczenia AI.",
prodReadinessPrice: "200 € →",
prodFullTitle: "Pełny Audyt Sieciowy",
prodFullDesc: "Połączenie obu audytów. GEO + gotowość techniczna w jednym raporcie z macierzą priorytetów.",
prodFullPrice: "300 € →",
prodCustomTitle: "Dedykowany Agent AI",
prodCustomDesc: "Autonomiczny agent produkcyjnej jakości zbudowany pod Twoje specyficzne potrzeby.",
prodCustomPrice: "Od 500 € →",
trustLaw: "⚖️ <strong>Świadomość regulacyjna</strong> — Zgodność z EU AI Act i RODO",
trustUav: "🚁 <strong>Inżynieria sprzętowa</strong> — Certyfikat EASA, ręcznie budowany dron i Edge AI",
trustPfuk: "🎓 <strong>PF UK</strong> — EU AI Act, RODO, NIS2",
fNavProducts: "Produkty",
aboutDisclaimer: "<span>⚠️</span> <span><strong>Uwaga:</strong> Informacje regulacyjne mają charakter wyłącznie edukacyjny i techniczny. Nie stanowią porady prawnej.</span>",
hCockpitStatus: "HERMES C2 // ŚRODOWISKO 24/7",
hCockpitChip: "HETZNER VPS · UE",
hMetric1Lbl: "Pętle Cron",
hMetric1Sub: "Zadania w tle 24/7",
hMetric2Lbl: "Autonomia",
hMetric2Sub: "Zero nadzoru człowieka",
hMetric3Lbl: "Dynamiczny Routing",
hMetric3Sub: "DeepSeek · Claude · GPT",
hMetric4Lbl: "Lighthouse",
hMetric4Sub: "0ms TBT · Zero CLS",
hCockpitLink: "Zobacz pełną historię →",
exp4Title: "Product Manager (Defence)",
exp4Desc: "Doświadczenie w branży obronnej — zarządzanie niejawnymi projektami sprzętowymi i programistycznymi.",
heroCta: "✦ Zobacz produkty",
heroContact: "Rozpocznij rozmowę →",
faqLabel: "✦ FAQ",
faqHeading: "Często zadawane pytania",
faq1q: "Kim jest Marian Stancik?",
faq1a: "<strong>Marian Stancik</strong> buduje autonomicznych agentów AI dla przedsiębiorców i firm. Specjalizuje się w tworzeniu agentów, audytach stron (GEO i zgodność) oraz orkiestracji Hermes Agent.",
faq2q: "Co sprawdza Audyt AI GEO?",
faq2a: "Audyt AI GEO sprawdza widoczność strony w wyszukiwarkach AI (Perplexity, ChatGPT Search, Claude, Google SGE). <strong>150 €</strong> — jednorazowy audyt, raport w 48 godzin.",
faq3q: "Czym jest Skan Gotowości Sieciowej AI?",
faq3a: "<strong>Techniczne sprawdzenie przez agenta AI</strong> obecności wymaganych dokumentów (Prywatność, RODO, Regulamin, AI Act). <strong>200 €</strong> — raport w 48 godzin.",
faq4q: "Czy Marian świadczy porady prawne?",
faq4a: "<strong>Nie.</strong> Marian studiuje prawo, nie jest adwokatem. Agenci wykonują <strong>wyłącznie kontrole techniczne</strong>.",
leadConsentText: 'Zgadzam się z <a href="/privacy" style="color:#CD7F32;text-decoration:underline;">Polityką Prywatności</a> i przetwarzaniem mojego adresu e-mail.',
fNavHome: "Strona główna",
blogReadPost: "Czytaj wpis",
footerImprint: '<strong>ASCENTIA s.r.o.</strong> · Klincová 37/B, 821 08 Bratysława · Członek zarządu: Marián Stančík · <a href="mailto:marianstancik@agentmail.to" style="color:#CD7F32;">marianstancik@agentmail.to</a>',
footerAiAct: '<strong>⚠️ Disclaimer:</strong> Treści generowane lub wspomagane przez autonomicznych agentów AI (Hermes Agent). ⚖️ Oznaczone zgodnie z EU AI Act Art. 50.',
bookLabel: "✉️ Skontaktuj się",
bookHeading: "Porozmawiajmy o Twoim projekcie.",
bookIntro: 'Napisz na <a href="mailto:marianstancik@agentmail.to">marianstancik@agentmail.to</a>.',
bookCard1Cta: "E-mail o agentach AI",
bookCard2Cta: "E-mail o zgodności regulacyjnej",
bookCard3Cta: "E-mail o UAV / Edge AI",
bookNote: 'ASCENTIA s.r.o. — <a href="mailto:marianstancik@agentmail.to" style="color:#CD7F32;">marianstancik@agentmail.to</a>.'
},
"""

# Inject de_block and pl_block into translations object before closing };
if 'de: {' not in code:
    code = code.replace('sk: {', f'{de_block}\n{pl_block}\nsk: {{')

# Update switchLanguage and applyTranslations button toggling
btn_toggle_code = """document.getElementById('btnEn')?.classList.toggle('active', currentLang === 'en');
document.getElementById('btnSk')?.classList.toggle('active', currentLang === 'sk');
document.getElementById('btnDe')?.classList.toggle('active', currentLang === 'de');
document.getElementById('btnPl')?.classList.toggle('active', currentLang === 'pl');"""

code = re.sub(
    r"document\.getElementById\('btnEn'\)\.classList\.toggle\('active', currentLang === 'en'\);\s*document\.getElementById\('btnSk'\)\.classList\.toggle\('active', currentLang === 'sk'\);",
    btn_toggle_code,
    code
)

# Update post dynamic loader in js/i18n.js
post_loader_code = """async function loadDynamicPostsHome() {
try {
const res = await fetch('blog/posts.json');
if (!res.ok) return;
const posts = await res.json();
if (!Array.isArray(posts) || posts.length === 0) return;
const container = document.getElementById('homeBlogGrid');
if (!container) return;
const d = translations[currentLang] || translations.en;

container.innerHTML = posts.slice(0, 3).map(p => {
let title = p.title;
let excerpt = p.excerpt;
let date = p.displayDate;
let targetUrl = p.url;

if (currentLang === 'sk') {
  title = p.titleSk || p.title;
  excerpt = p.excerptSk || p.excerpt;
  date = p.displayDateSk || p.displayDate;
  targetUrl = p.urlSk || p.url;
} else if (currentLang === 'de') {
  title = p.titleDe || p.title;
  excerpt = p.excerptDe || p.excerpt;
  date = p.displayDateDe || p.displayDate;
  targetUrl = p.urlDe || p.url;
} else if (currentLang === 'pl') {
  title = p.titlePl || p.title;
  excerpt = p.excerptPl || p.excerpt;
  date = p.displayDatePl || p.displayDate;
  targetUrl = p.urlPl || p.url;
}

return `
<a href="${targetUrl}" class="blog-card fade-in visible">
  <div class="blog-card-date">${date}</div>
  <h3>${title}</h3>
  <p>${excerpt}</p>
  <div class="blog-card-arrow">${d.blogReadPost || 'Read post'} <span>→</span></div>
</a>`;
}).join('');
} catch(e){}
}"""

code = re.sub(
    r"async function loadDynamicPostsHome\(\)[\s\S]*?const observer = new IntersectionObserver",
    f"{post_loader_code}\nconst observer = new IntersectionObserver",
    code
)

# Update initial load button state
init_state_code = """
document.getElementById('btnEn')?.classList.toggle('active', currentLang === 'en');
document.getElementById('btnSk')?.classList.toggle('active', currentLang === 'sk');
document.getElementById('btnDe')?.classList.toggle('active', currentLang === 'de');
document.getElementById('btnPl')?.classList.toggle('active', currentLang === 'pl');
applyTranslations();
"""

code = re.sub(
    r"if \(currentLang === 'sk'\) \{[\s\S]*?document\.getElementById\('btnSk'\)\?\.classList\.remove\('active'\);\s*\}",
    init_state_code.strip(),
    code
)

with open(I18N_JS, 'w', encoding='utf-8') as f:
    f.write(code)

print("[+] js/i18n.js updated with complete 4-language support!")
