#!/usr/bin/env python3
"""
Comprehensive Fix & Sync for Multilingual i18n Frontend Engine (EN, SK, DE, PL)
1. Updates js/i18n.js with complete translation dictionaries for all 4 languages.
2. Implements bulletproof window.switchLanguage and generic DOM binding (data-i18n + ID matching).
3. Adds dynamic blog post rendering on blog/index.html and homepage for all 4 languages.
4. Adds missing IDs to index.html and other pages.
5. Updates all <script src="/js/i18n.js"> tags to <script src="/js/i18n.js?v=20260908_v2"> for cache busting.
"""

import os
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load locales
with open(os.path.join(BASE_DIR, 'locales', 'en.json'), 'r', encoding='utf-8') as f:
    loc_en = json.load(f)
with open(os.path.join(BASE_DIR, 'locales', 'sk.json'), 'r', encoding='utf-8') as f:
    loc_sk = json.load(f)
with open(os.path.join(BASE_DIR, 'locales', 'de.json'), 'r', encoding='utf-8') as f:
    loc_de = json.load(f)
with open(os.path.join(BASE_DIR, 'locales', 'pl.json'), 'r', encoding='utf-8') as f:
    loc_pl = json.load(f)

# Define master dictionaries
TRANSLATIONS = {
    "en": {
        "docTitle": "Marian Stancik — AI Agent Developer | Autonomous Agents",
        "docDesc": "Marian Stancik — I build AI agents that run your processes. Custom autonomous agents, AI web audits for the AI search era.",
        "ogTitle": "Marian Stancik — AI Agent Developer | Autonomous Agents",
        "ogDesc": "I build AI agents that run your processes. Autonomous systems on my own infrastructure, built for regulated environments.. Hetzner VPS 24/7.",
        "skipLink": "Skip to main content",
        "navHome": "Home",
        "navAbout": "About",
        "navSkills": "Skills",
        "navDrones": "Drones",
        "navExpertise": "Expertise",
        "navProjects": "Projects",
        "navBlog": "Blog",
        "navContact": "✦ Contact",
        "navProducts": "Products",
        "navServices": "Products",
        "heroBadge": "✦ I build AI agents that run your processes",
        "heroTagline": "I build <strong>AI agents</strong> that run your processes. Autonomous systems, web audits, and custom AI agents for creative founders.",
        "roleAi": "AI Agent Developer",
        "roleUav": "Hardware Engineering (Hobby)",
        "roleDrone": "Drone Pilot (EASA A1/A3)",
        "rolePm": "AI Agent Developer",
        "roleLaw": "Regulatory Awareness (PF UK)",
        "heroEmail": "Email",
        "heroCta": "✦ See Products",
        "heroContact": "Start a Conversation →",
        "scrollText": "Scroll",

        # Homepage Products
        "homeProductsLabel": "✦ Products",
        "homeProductsHeading": "What I Build",
        "homeProductsIntro": "AI agents that audit your web presence and custom autonomous agents for your business.",
        "prodGeoTitle": "AI GEO Audit",
        "prodGeoDesc": "Is your website ready for AI search? Agent checks llms.txt, JSON-LD, robots.txt, and AI visibility.",
        "prodGeoPrice": "€199 →",
        "prodReadinessTitle": "AI Web Readiness Scan",
        "prodReadinessDesc": "Technical check of your website's legal documents. Agent verifies Privacy Policy, GDPR consent, Terms.",
        "prodReadinessPrice": "€200 →",
        "prodFullTitle": "Full Web Audit",
        "prodFullDesc": "Both audits combined. GEO + technical readiness in one comprehensive report with priority matrix.",
        "prodFullPrice": "€300 →",
        "prodCustomTitle": "Custom AI Agent",
        "prodCustomDesc": "A production-grade autonomous agent built for your specific business need. 24/7 operation.",
        "prodCustomPrice": "From €500 →",
        "trustLaw": "⚖️ <strong>Regulatory awareness</strong> — I study EU AI Act, I build for regulated environments",
        "trustUav": "🚁 <strong>Hardware engineering</strong> — Hand-built drone, EASA certified, edge AI",
        "trustPfuk": "🎓 <strong>PF UK</strong> — EU AI Act, GDPR, NIS2",

        # About
        "aboutLabel": "✦ About",
        "aboutHeading": "AI Agent Developer. Building systems that run your processes.",
        "aboutIntro": "I build autonomous AI agents that run business processes — content, CRM, monitoring, and automation. 24/7, on my own infrastructure, without babysitting.",
        "aboutBody": "<p>I build <strong>autonomous AI agents</strong> using the <strong>Hermes Agent</strong> framework (by Nous Research). My core infrastructure runs 24/7 on an enterprise <strong>Hetzner Cloud VPS</strong> in Germany/Finland, orchestrating advanced models via the <strong>OpenRouter API</strong>, with <strong>Obsidian</strong> acting as a persistent memory layer for multi-agent workflows. <em>This website and all its content is built and maintained by my autonomous Hermes Agent.</em></p><p>I build web applications with zero-build <strong>HTML5, Vanilla JS, and modern CSS</strong> — engineered for instant loading (Lighthouse 100), zero layout shifts, and deep discoverability by autonomous AI search crawlers (GEO / LLMO).</p><p>I study the legal and business impacts of AI — primarily the <strong>EU AI Act</strong>, <strong>GDPR</strong>, <strong>NIS2 Directive</strong>, <strong>DORA</strong>, the <strong>EU Data Act</strong>, and the <strong>DSM Copyright Directive</strong>. This regulatory awareness helps me build AI agents that are ready for regulated environments. I share practical regulatory knowledge for educational purposes only, not legal advice.</p><p>On the hardware front, I personally <strong>designed, hand-soldered, and assembled a custom 1500g carbon tactical quadcopter</strong> from bare components into a fully operational flying UAV. Initially flight-tested on <strong>Betaflight</strong>, it now operates on <strong>ArduPilot</strong> for advanced autonomous mission execution.</p>",
        "aboutBodyText": "<p>I build <strong>autonomous AI agents</strong> using the <strong>Hermes Agent</strong> framework. My infrastructure runs 24/7 on an enterprise Hetzner VPS, orchestrating multi-LLM agents for content, CRM, monitoring, and automation. <em>This website and all its content is built and maintained by my autonomous Hermes Agent.</em></p><p>I study law at <strong>PF UK</strong> (Comenius University, Bratislava) — EU AI Act, GDPR, NIS2, and tech regulation. This regulatory awareness means I understand the legal landscape and can build AI agents that are <strong>technically ready for regulated environments</strong>. <strong>I am not a lawyer, I do not provide legal advice.</strong></p><p>I build drones as a <strong>hobby</strong> — hand-soldered 1500g carbon quad with ArduPilot and Raspberry Pi 5 edge AI, EASA A1/A3 certified. It's a showcase of my hardware and edge AI skills, not a product.</p><div class=\"highlight\" style=\"background:rgba(205,127,50,0.08);padding:1.2rem;border-left:3px solid #CD7F32;margin:1.5rem 0;border-radius:6px;font-size:0.88rem;\"><p style=\"margin:0;\"><strong style=\"color:#E8B86D;\">⚠️ Disclaimer:</strong> This is not legal advice. I share regulatory knowledge for educational purposes only. For specific legal questions, consult a qualified attorney.</p></div>",

        # Stats
        "stat1Label": "Active Cron Agents",
        "stat2Label": "Domains Covered",
        "stat3Label": "Years Building",
        "stat4Label": "Drone Insurance",
        "stat5Label": "Open Source Repos",
        "stat6Label": "VPS Agent Runtime",
        "stat1": "Active Cron Agents",
        "stat2": "Engineering Domains",
        "stat3": "Years Building",
        "stat4": "Drone Insurance",
        "stat5": "Open Source Repos",
        "stat6": "24/7 Agent Runtime",

        # Cockpit
        "cockpitStatus": "HERMES C2 // 24/7 AUTONOMOUS RUNTIME ONLINE",
        "cockpitChip": "HETZNER VPS · EU DATA SOVEREIGNTY",
        "cockpitStat1Title": "Autonomous Cron Loops",
        "cockpitStat1Sub": "24/7 background orchestrations for Content, CRM, Sentinel & Health",
        "cockpitStat2Title": "Dynamic OpenRouter Routing",
        "cockpitStat2Sub": "DeepSeek R1/V3 · Claude 3.5 Sonnet · GPT-4o synthesis",
        "cockpitStat3Title": "Persistent Vault Memory",
        "cockpitStat3Sub": "SQLite state + bidirectional Markdown knowledge graph",
        "cockpitStat4Title": "EU AI Act & GDPR Compliant",
        "cockpitStat4Sub": "Art. 50 AI labeling & audit-ready technical files",

        # What I Do / Don't Do
        "whatIDoTitle": "What I do",
        "whatIDoSubtitle": "Job · Context · Hobby — clear separation.",
        "card1Title": "AI Agent Developer (Job)",
        "card1Desc": "I design, build, deploy, and operate autonomous AI agents on client infrastructure or managed VPS. Custom MCP servers, multi-LLM orchestration, 24/7 cron automation, and persistent memory.",
        "card2Title": "Regulatory Context (PF UK)",
        "card2Desc": "PF UK law studies. EU AI Act, GDPR, NIS2 awareness used to build agents ready for regulated environments. Educational sharing only, not legal advice.",
        "card3Title": "Hardware Engineering (Hobby)",
        "card3Desc": "Hand-soldered 1500g carbon quad with ArduPilot and Raspberry Pi 5 edge AI. EASA A1/A3 certified, €2.6M insured. Proof of hardware and embedded engineering skills.",
        "whatIDontDoTitle": "What I don't do",
        "whatIDontDoSubtitle": "Clear boundaries — so you know exactly who you're working with.",
        "dont1Title": "No legal advice",
        "dont1Desc": "I'm a student, not an attorney. I don't provide legal opinions, compliance consulting, or legal services. My agents run technical checks — legal sign-off is for your lawyer.",
        "dont2Title": "No drone services",
        "dont2Desc": "I don't sell drones, do aerial work commercially, or provide drone services. The drone is a hobby that demonstrates edge-AI and systems-engineering skills.",
        "dont3Title": "No agencies / middlemen",
        "dont3Desc": "I build directly with clients. No outsourcing, no white-label, no account management layers. You talk to the engineer who builds your system.",

        # Focus
        "focus1Title": "Process Automation",
        "focus1Desc": "Lead capture, CRM follow-ups, content pipelines, reporting — agents handle workflows that used to eat your team's time.",
        "focus2Title": "AI Web Audits",
        "focus2Desc": "GEO audit (AI-search visibility) and Web Readiness Scan (technical document check) — an agent reviews your web presence.",
        "focus3Title": "Custom AI Agents",
        "focus3Desc": "Your workflow, your data, your infrastructure. An agent built for one job — your job — run 24/7.",
        "focus4Title": "Regulation-Aware Builds",
        "focus4Desc": "Law background means agents are engineered with GDPR/AI-Act awareness from day one — not retrofitted after a problem.",

        # Timeline
        "timelineTitle": "How I got here",
        "timelineSubtitle": "The engineering evolution — from prompt engineering to fully autonomous systems.",
        "t2026Title": "Hermes Agent & Autonomous System (My AI Assistant)",
        "t2026Desc": "Operating a 24/7 autonomous multi-agent infrastructure on Hetzner VPS. 19+ cron orchestrations for content, CRM, and system health. Digital twin automating publishing across platforms, and autonomous Hermes Agent running this website.",
        "t2025Title": "First Autonomous Agents & Model Context Protocol (MCP)",
        "t2025Desc": "Transitioning from passive chatbots to active, tool-using autonomous agents. Implementing custom MCP servers, multi-tool loops, and persistent Obsidian memory architecture. Starting law studies at PF UK (EU AI Act & GDPR focus).",
        "t2024Title": "IDE Antigravity & AI-Augmented Engineering",
        "t2024Desc": "Adopting modern agentic coding workflows in IDE Antigravity. Designing and hand-soldering a 1500g tactical carbon quadcopter with ArduPilot and onboard Raspberry Pi 5 edge vision AI (EASA A1/A3 licensed).",
        "t2023Title": "Inception of AI Chatbots & GPT Experiments",
        "t2023Desc": "First deep dive into LLMs, GPT prompt engineering, and conversational AI bots. Experimenting with API integrations, Python scripting, and discovering the transformative potential of 24/7 autonomous execution.",

        # Skills
        "skillsLabel": "✦ AI Agent Skills",
        "skillsHeading": "Skills & Capabilities",
        "skillsIntro": "Full-stack AI engineering — from LLM orchestration and Hermes Agent loops to cloud infrastructure, regulatory awareness, and hardware engineering.",
        "sk1Title": "Hermes Agent & Multi-Agent Systems",
        "sk1List": "<li><strong>Hermes Agent:</strong> Autonomous execution loops & reflection on 24/7 Hetzner VPS</li><li><strong>MCP Server Design:</strong> Custom Model Context Protocol tools & APIs</li><li><strong>OpenRouter Multi-LLM:</strong> Dynamic routing across DeepSeek, Claude 3.5 & GPT-4o</li><li><strong>Obsidian Memory Layer:</strong> Bi-directional markdown vault for agent memory persistence</li><li><strong>C2 Interfaces:</strong> Interactive command & control via Telegram & WhatsApp bots</li>",
        "sk2Title": "Software, High-Perf Web & Cloud",
        "sk2List": "<li><strong>Python 3 Ecosystem:</strong> FastAPI, Asyncio, Playwright, toolchain automation</li><li><strong>Zero-Build High-Perf Web:</strong> 100% Vanilla HTML5/CSS3/JS, zero framework bloat, PageSpeed 100 & 0ms TBT</li><li><strong>GEO & 3/3 Agentic Browsing:</strong> llmstxt.org v2 standard, Schema.org @graph, optimized for Perplexity & LLM crawlers</li><li><strong>Linux VPS Administration:</strong> Ubuntu Server on Hetzner Cloud (DE/FI), Caddy reverse proxy & SSL</li><li><strong>Production Operations:</strong> 19+ 24/7 cron orchestrations, SQLite persistence & watchdog monitoring</li>",
        "sk3Title": "Regulatory Awareness (EU AI Act, GDPR, NIS2)",
        "sk3List": "<li><strong>EU AI Act:</strong> Risk classification, GPAI governance, and technical documentation files</li><li><strong>GDPR & Privacy:</strong> Training data compliance, automated profiling safeguards</li><li><strong>NIS2 & DORA:</strong> Supply chain cyber resilience & financial tech operational readiness</li><li><strong>EU Data Act:</strong> Data sharing, cloud interoperability, and EU data sovereignty</li><li><strong>DSM Copyright:</strong> Text & Data Mining (TDM) exemptions for AI model training</li>",
        "sk4Title": "Tactical UAV Systems & Edge Robotics",
        "sk4List": "<li><strong>Hardware Build:</strong> Hand-soldered 1500g 8-inch carbon quad from bare components</li><li><strong>Flight Software:</strong> Dual Betaflight dynamics tuning & ArduPilot Copter waypoint missions</li><li><strong>Edge Vision AI:</strong> Raspberry Pi 5 (8GB) + Camera 3 running onboard object detection</li><li><strong>Avionics & Telemetry:</strong> Skystars H7 Dual Gyro FC, AM60 60A ESC, RadioMaster ELRS, GNSS</li><li><strong>Certifications:</strong> EASA A1/A3 licensed drone pilot, €2.6M Coverdrone liability insurance</li>",

        # Drones
        "droneLabel": "✦ UAV Systems",
        "droneHeading": "Hand-Built. Flight-Tested. AI-Augmented.",
        "droneIntro": "Custom 1500g carbon quadcopter hand-soldered from bare components. Initially flown on Betaflight, powered by ArduPilot, with onboard Raspberry Pi 5 edge vision AI in development. EASA A1/A3 certified, €2.6M insured.",
        "dCap1": "20s outdoor compilation — field flight & autonomous waypoint navigation testing",
        "dCap2": "Hand-built 1500g carbon quad — maiden flight & telemetry verification",
        "dCap3": "ArduPilot mission planning — automated multi-waypoint guidance",

        # Expertise
        "expLabel": "✦ Expertise",
        "expHeading": "One focus. Autonomous agents.",
        "expIntro": "One focus: autonomous AI agents that run your processes. Law awareness and hardware engineering are context, not pillars.",
        "exp1Title": "Autonomous Agent Systems",
        "exp1Desc": "I build AI agents using the Hermes Agent framework. 24/7 autonomous systems running on Hetzner VPS with Telegram & WhatsApp C2 interfaces, OpenRouter multi-model routing, and persistent memory.",
        "exp2Title": "EU AI Act & Regulatory Awareness",
        "exp2Desc": "I study EU AI regulation and provide technical context for building auditable systems. Not legal advice — educational regulatory awareness.",
        "exp3Title": "UAV Systems & Edge AI",
        "exp3Desc": "I build drones — from design to flight, with onboard AI. Custom 1500g carbon quadcopters hand-soldered from bare electronics, ArduPilot autonomous missions, Raspberry Pi 5 edge vision. EASA A1/A3 certified.",
        "exp4Title": "Product Manager (Defence)",
        "exp4Desc": "Defence industry background — managing classified hardware and software projects at scale.",

        # Projects
        "projLabel": "✦ Projects",
        "projHeading": "What I'm building.",
        "projIntro": "Production systems, open-source tools, and ambitious experiments.",
        "p1Title": "Prime Agent Masterclass",
        "p1Desc": "8-module video course teaching autonomous AI agents. Stripe-powered, EN/SK, Vercel-hosted.",
        "p2Title": "Autonomous Agent Playground",
        "p2Desc": "Experimental autonomous workflows: AI agent pipelines, regulatory awareness research, and hardware engineering on a Hetzner VPS.",
        "p3Title": "Polymarket Trading Bot",
        "p3Desc": "Production-ready Markov chain trading bot for prediction markets. Docker-deployable.",
        "p4Title": "Hermes Digital Twin",
        "p4Desc": "Autonomous AI agent running 19+ cron jobs on Hetzner VPS — posting X, LinkedIn, blog daily without human touch.",

        # Blog Preview / Index
        "blogSecLabel": "✦ Blog",
        "blogSecHeading": "Latest thoughts.",
        "blogSecIntro": "AI agents, autonomous systems, and building in public.",
        "blogBadge": "✦ Engineering & Thought Log",
        "blogTitle": "Articles & <span>Insights</span>",
        "blogSubtitle": "Autonomous AI agents, legal-by-design frameworks (AI Act & GDPR), and UAV engineering.",
        "blogHomeLink": "← Home",
        "blogAllBtn": "Read all posts →",
        "blogReadPost": "Read post",

        # FAQ
        "faqLabel": "✦ FAQ",
        "faqHeading": "Frequently Asked Questions",
        "faq1q": "Who is Marian Stancik?",
        "faq1a": "<strong>Marian Stancik</strong> builds autonomous AI agents for creative founders and businesses. He specializes in custom AI agent development, AI web audits (GEO and technical readiness), and multi-agent orchestration using the Hermes Agent framework. His law studies inform regulatory awareness for building regulatory-ready systems. Hardware engineering is a hobby that demonstrates edge AI skills.",
        "faq2q": "What does an AI GEO Audit check?",
        "faq2a": "An AI GEO Audit checks if your website is visible to AI search engines like Perplexity, ChatGPT Search, Claude, and Google SGE. It verifies <strong>llms.txt</strong>, <strong>robots.txt</strong>, <strong>JSON-LD</strong> structured data, <strong>OpenGraph</strong> tags, <strong>hreflang</strong>, page speed, and overall AI discoverability. <strong>€199</strong> — one-time audit, report in 48 hours.",
        "faq3q": "What is the AI Web Readiness Scan?",
        "faq3a": "The AI Web Readiness Scan is a <strong>technical check by an AI agent</strong> that verifies whether your website has the required documents and structures — Privacy Policy, GDPR consent, Terms of Service, Disclaimer, AI Act disclosure, and cookie compliance. <strong>This is not legal advice</strong> — just a technical checklist. <strong>€200</strong> — one-time scan, report in 48 hours.",
        "faq4q": "Does Marian provide legal advice?",
        "faq4a": "<strong>No.</strong> Marian studies law, he is not a lawyer. He does not provide legal advice, legal services, or compliance consulting. His AI agents perform <strong>technical checks only</strong> — they verify whether documents and structures exist, not whether they are legally correct. Clients must consult a qualified lawyer for legal matters.",

        # Lead & Contact
        "leadLabel": "✦ Stay in touch",
        "leadHeading": "Get updates from the build.",
        "leadIntro": "AI agent insights, drone builds, law & tech notes — directly to your inbox.",
        "subscribeBtn": "Subscribe",
        "leadNote": "No spam. Unsubscribe anytime. Built with AgentMail.",
        "leadConsentText": "I agree to the <a href=\"/privacy\" style=\"color:#CD7F32;text-decoration:underline;\">Privacy Policy</a> and consent to processing my email for newsletter updates.",
        "connLabel": "✦ Connect",
        "connHeading": "Let's build something.",
        "connIntro": "Follow the build, read the blog, or reach out directly.",
        "connBlogText": "Blog",
        "bookLabel": "✉️ Get in touch",
        "bookHeading": "Let's talk about your project.",
        "bookIntro": "Write to <a href=\"mailto:marianstancik@agentmail.to\">marianstancik@agentmail.to</a>. Calendar booking is not offered — email is the contact channel.",
        "bookCard1Cta": "Email about AI agents",
        "bookCard2Cta": "Email about regulatory checks",
        "bookCard3Cta": "Email about UAV / edge AI",
        "bookNote": "ASCENTIA s.r.o. — <a href=\"mailto:marianstancik@agentmail.to\" style=\"color:#CD7F32;\">marianstancik@agentmail.to</a>.",

        # Footer
        "footerTagline": "I build AI agents that run your processes. Autonomous systems on my own infrastructure.",
        "fCol1Title": "Navigate",
        "fCol2Title": "Projects",
        "fCol3Title": "Contact",
        "fNavHome": "Home",
        "fNavAbout": "About",
        "fNavExp": "Expertise",
        "fNavProj": "Projects",
        "fNavConn": "Connect",
        "fNavBlog": "Blog",
        "fNavSkills": "Skills",
        "fNavServices": "Products",
        "fNavProducts": "Products",
        "fMotto": "Build better. Stay legal.",
        "footerImprint": "<strong>ASCENTIA s.r.o.</strong> · Klincová 37/B, 821 08 Bratislava-Ružinov · IČO: 51858959 · DIČ: 2120816071 · konateľ: Marián Stančík<br>Obchodný register Mestského súdu Bratislava III, oddiel Sro, vložka 130384/B · <a href=\"mailto:marianstancik@agentmail.to\" style=\"color:#CD7F32;\">marianstancik@agentmail.to</a>",
        "footerAiAct": "<strong>⚠️ Disclaimer:</strong> Content is AI-generated or AI-assisted by autonomous agents (Hermes Agent) and is for informational purposes only. It does not constitute professional advice. <strong>No warranty or liability</strong> for reliance on content. ⚖️ EU AI Act Art. 50: AI content labeled accordingly."
    }
}

# German translations
TRANSLATIONS["de"] = {
    **TRANSLATIONS["en"],
    "docTitle": "Marian Stancik — KI-Agenten-Entwickler | Autonome Systeme",
    "docDesc": "Marian Stancik — Ich baue KI-Agenten, die Ihre Prozesse steuern. Maßgeschneiderte autonome Agenten und KI-Web-Audits.",
    "ogTitle": "Marian Stancik — KI-Agenten-Entwickler | Autonome Systeme",
    "ogDesc": "Ich baue KI-Agenten, die Ihre Prozesse steuern. Autonome Systeme auf eigener Infrastruktur, bereit für regulierte Umgebungen. Hetzner VPS 24/7.",
    "skipLink": "Zum Hauptinhalt springen",
    "navHome": "Startseite",
    "navAbout": "Über mich",
    "navSkills": "Fähigkeiten",
    "navDrones": "Drohnen",
    "navExpertise": "Expertise",
    "navProjects": "Projekte",
    "navBlog": "Blog",
    "navContact": "✦ Kontakt",
    "navProducts": "Produkte",
    "navServices": "Produkte",
    "heroBadge": "✦ Ich baue KI-Agenten, die Ihre Prozesse steuern",
    "heroTagline": "Ich baue <strong>KI-Agenten</strong>, die Ihre Prozesse steuern. Autonome Systeme, Web-Audits und maßgeschneiderte KI-Workflows für Gründer.",
    "roleAi": "KI-Agenten-Entwickler",
    "roleUav": "Hardware-Engineering (Hobby)",
    "roleDrone": "Drohnenpilot (EASA A1/A3)",
    "rolePm": "KI-Agenten-Entwickler",
    "roleLaw": "Regulatorische Compliance (PF UK)",
    "heroEmail": "E-Mail",
    "heroCta": "✦ Produkte ansehen",
    "heroContact": "Gespräch beginnen →",
    "scrollText": "Scrollen",

    "homeProductsLabel": "✦ Produkte",
    "homeProductsHeading": "Was ich baue",
    "homeProductsIntro": "KI-Agenten, die Ihre Webpräsenz auditieren, und maßgeschneiderte autonome Agenten für Ihr Unternehmen.",
    "prodGeoTitle": "KI-GEO-Audit",
    "prodGeoDesc": "Ist Ihre Website bereit für KI-Suchen? Überprüfung von llms.txt, JSON-LD, robots.txt und KI-Sichtbarkeit.",
    "prodGeoPrice": "150 € →",
    "prodReadinessTitle": "KI-Web-Readiness-Scan",
    "prodReadinessDesc": "Technischer Compliance-Check: Datenschutzerklärung, DSGVO, AGB, Disclaimer und KI-Kennzeichnung.",
    "prodReadinessPrice": "200 € →",
    "prodFullTitle": "Vollständiges Web-Audit",
    "prodFullDesc": "Beide Audits kombiniert. GEO + technische Compliance in einem umfassenden Bericht mit Prioritätenmatrix.",
    "prodFullPrice": "300 € →",
    "prodCustomTitle": "Individueller KI-Agent",
    "prodCustomDesc": "Ein autonomer Agent in Produktionsqualität, der für Ihre spezifischen Anforderungen gebaut wird.",
    "prodCustomPrice": "Ab 500 € →",
    "trustLaw": "⚖️ <strong>Regulatorische Compliance</strong> — Konform mit EU AI Act & DSGVO",
    "trustUav": "🚁 <strong>Hardware-Engineering</strong> — EASA-zertifizierter Drohnenbau & Edge-KI",
    "trustPfuk": "🎓 <strong>PF UK</strong> — EU AI Act, DSGVO, NIS2",

    "aboutLabel": "✦ Über mich",
    "aboutHeading": "KI-Agenten-Entwickler. Systeme, die Ihre Prozesse steuern.",
    "aboutIntro": "Ich baue autonome KI-Agenten, die Geschäftsprozesse steuern — Content, CRM, Monitoring und Automatisierung. 24/7 auf eigener Infrastruktur.",
    "aboutBody": "<p>Ich baue <strong>autonome KI-Agenten</strong> mit dem <strong>Hermes Agent</strong> Framework. Meine Kerninfrastruktur läuft 24/7 auf einem Enterprise <strong>Hetzner Cloud VPS</strong> in Deutschland/Finnland und orchestriert Modelle über die <strong>OpenRouter API</strong> mit <strong>Obsidian</strong> als persistentem Gedächtnis.</p><p>Ich entwickle Webanwendungen mit <strong>HTML5, Vanilla JS und modernem CSS</strong> — optimiert für sofortiges Laden (Lighthouse 100), null Layout-Verschiebungen und Entdeckung durch KI-Suchcrawler (GEO / LLMO).</p><p>Ich beschäftige mich mit den geschäftlichen Auswirkungen von KI — <strong>EU AI Act, DSGVO, NIS2, DORA</strong>. Dies hilft mir, KI-Agenten für regulierte Umgebungen zu bauen (nur technische Information, keine Rechtsberatung).</p>",
    "aboutBodyText": "<p>Ich baue <strong>autonome KI-Agenten</strong> mit dem <strong>Hermes Agent</strong> Framework. Meine Infrastruktur läuft 24/7 auf einem Hetzner VPS und steuert Multi-Modell-Workflows für Content, CRM, Monitoring und Automation.</p><p>Ich studiere Rechtswissenschaften an der <strong>PF UK</strong> — EU AI Act, DSGVO, NIS2 und Tech-Regulierung. Dieses regulatorische Wissen ermöglicht es mir, technisch auditierbare KI-Systeme zu entwickeln. <strong>Ich bin kein Anwalt und biete keine Rechtsberatung an.</strong></p><p>Drohnen baue ich als <strong>Hobby</strong> — handgelöteter 1500g Carbon-Quad mit ArduPilot und Raspberry Pi 5 Edge-KI, EASA A1/A3 zertifiziert.</p><div class=\"highlight\" style=\"background:rgba(205,127,50,0.08);padding:1.2rem;border-left:3px solid #CD7F32;margin:1.5rem 0;border-radius:6px;font-size:0.88rem;\"><p style=\"margin:0;\"><strong style=\"color:#E8B86D;\">⚠️ Hinweis:</strong> Keine Rechtsberatung. Regulatorische Einblicke dienen ausschließlich Bildungszwecken.</p></div>",

    "stat1Label": "Aktive Cron-Agenten",
    "stat2Label": "Engineering-Bereiche",
    "stat3Label": "Jahre Erfahrung",
    "stat4Label": "Drohnen-Versicherung",
    "stat5Label": "Open-Source Repos",
    "stat6Label": "24/7 Agent-Laufzeit",
    "stat1": "Aktive Cron-Agenten",
    "stat2": "Engineering-Bereiche",
    "stat3": "Jahre Erfahrung",
    "stat4": "Drohnen-Versicherung",
    "stat5": "Open-Source Repos",
    "stat6": "24/7 Agent-Laufzeit",

    "cockpitStatus": "HERMES C2 // 24/7 AUTONOME LAUFZEIT ONLINE",
    "cockpitChip": "HETZNER VPS · EU-DATENSOUVERÄNITÄT",
    "cockpitStat1Title": "Autonome Cron-Schleifen",
    "cockpitStat1Sub": "24/7 Hintergrund-Orchestrierungen für Content, CRM & Health",
    "cockpitStat2Title": "Dynamisches OpenRouter Routing",
    "cockpitStat2Sub": "DeepSeek R1/V3 · Claude 3.5 Sonnet · GPT-4o Synthese",
    "cockpitStat3Title": "Persistenter Vault-Speicher",
    "cockpitStat3Sub": "SQLite-Status + bidirektionaler Markdown-Wissensgraph",
    "cockpitStat4Title": "EU AI Act & DSGVO Konform",
    "cockpitStat4Sub": "Art. 50 KI-Kennzeichnung & auditierbare Dokumentation",

    "whatIDoTitle": "Was ich tue",
    "whatIDoSubtitle": "Beruf · Kontext · Hobby — klare Trennung.",
    "card1Title": "KI-Agenten-Entwickler (Beruf)",
    "card1Desc": "Ich entwerfe, baue und betreibe autonome KI-Agenten auf Kundeninfrastruktur oder Managed VPS. MCP-Server, Multi-LLM-Orchestrierung und 24/7-Cron.",
    "card2Title": "Regulatorischer Kontext (PF UK)",
    "card2Desc": "Rechtsstudium an der PF UK. EU AI Act, DSGVO, NIS2 für den Bau auditierbarer Agenten. Nur technische Information.",
    "card3Title": "Hardware-Engineering (Hobby)",
    "card3Desc": "Handgelöteter 1500g Carbon-Quad mit ArduPilot und Raspberry Pi 5 Edge-KI. EASA A1/A3 lizenziert, 2,6 Mio. € versichert.",
    "whatIDontDoTitle": "Was ich nicht tue",
    "whatIDontDoSubtitle": "Klare Grenzen — damit Sie genau wissen, mit wem Sie arbeiten.",
    "dont1Title": "Keine Rechtsberatung",
    "dont1Desc": "Ich bin Student, kein Anwalt. Meine Agenten führen technische Prüfungen durch — rechtliche Freigaben obliegen Ihrem Anwalt.",
    "dont2Title": "Keine Drohnendienstleistungen",
    "dont2Desc": "Ich verkaufe keine Drohnen und biete keine kommerziellen Flugdienste an. Die Drohne ist ein technisches Hobbyprojekt.",
    "dont3Title": "Keine Agenturen / Zwischenhändler",
    "dont3Desc": "Ich arbeite direkt mit Kunden. Kein Outsourcing. Sie sprechen direkt mit dem Entwickler Ihres Systems.",

    "focus1Title": "Prozessautomatisierung",
    "focus1Desc": "Lead-Generierung, CRM-Follow-ups, Content-Pipelines — Agenten übernehmen zeitraubende Workflows.",
    "focus2Title": "KI-Web-Audits",
    "focus2Desc": "GEO-Audit (KI-Suchsichtbarkeit) und Readiness-Scan (technische Dokumentenprüfung) durch Agenten.",
    "focus3Title": "Individuelle KI-Agenten",
    "focus3Desc": "Ihr Workflow, Ihre Daten, Ihre Infrastruktur. Ein maßgeschneiderter Agent für Ihre Anforderungen.",
    "focus4Title": "Compliance-Bewusste Systeme",
    "focus4Desc": "DSGVO- und AI-Act-Konformität von Tag eins an mitgedacht.",

    "timelineTitle": "Mein Werdegang",
    "timelineSubtitle": "Die technische Evolution — vom Prompt-Engineering zu autonomen Systemen.",
    "t2026Title": "Hermes Agent & Autonomes System",
    "t2026Desc": "Betrieb einer 24/7 autonomen Multi-Agenten-Infrastruktur auf Hetzner VPS mit 19+ Cron-Orchestrierungen.",
    "t2025Title": "Erste autonome Agenten & MCP",
    "t2025Desc": "Übergang zu aktiven, werkzeugnutzenden Agenten mit MCP-Servern und persistenter Obsidian-Architektur.",
    "t2024Title": "IDE Antigravity & KI-gestütztes Engineering",
    "t2024Desc": "Entwicklung moderner Agentic-Coding-Workflows. Bau des 1500g taktischen Quads mit Raspberry Pi 5 Edge-KI.",
    "t2023Title": "Beginn der KI-Chatbots & GPT-Experimente",
    "t2023Desc": "Erste Deep-Dives in LLMs, Prompt-Engineering und 24/7 autonome Skripte.",

    "skillsLabel": "✦ KI-Agenten-Fähigkeiten",
    "skillsHeading": "Fähigkeiten & Kompetenzen",
    "skillsIntro": "Full-Stack-KI-Engineering — von LLM-Orchestrierung und Hermes-Agent-Schleifen bis zu Cloud-Infrastruktur, Compliance und Hardware.",
    "sk1Title": "Hermes Agent & Multi-Agenten-Systeme",
    "sk1List": "<li><strong>Hermes Agent:</strong> Autonome Ausführungsschleifen auf 24/7 Hetzner VPS</li><li><strong>MCP Server Design:</strong> Maßgeschneiderte Model Context Protocol Tools & APIs</li><li><strong>OpenRouter Multi-LLM:</strong> Dynamisches Routing über DeepSeek, Claude 3.5 & GPT-4o</li><li><strong>Obsidian Memory Layer:</strong> Markdown-Vault für persistentes Agentengedächtnis</li><li><strong>C2-Schnittstellen:</strong> Interaktive Steuerung über Telegram- & WhatsApp-Bots</li>",
    "sk2Title": "Software, High-Perf Web & Cloud",
    "sk2List": "<li><strong>Python 3 Ökosystem:</strong> FastAPI, Asyncio, Playwright, Toolchain-Automatisierung</li><li><strong>Zero-Build High-Perf Web:</strong> 100% Vanilla HTML5/CSS3/JS, PageSpeed 100 & 0ms TBT</li><li><strong>GEO & Agentic Browsing:</strong> llmstxt.org v2 Standard, optimiert für Perplexity & LLM-Crawler</li><li><strong>Linux VPS Administration:</strong> Ubuntu Server auf Hetzner Cloud (DE/FI), Caddy & SSL</li><li><strong>Produktionsbetrieb:</strong> 19+ 24/7 Cron-Orchestrierungen, SQLite-Persistenz & Monitoring</li>",
    "sk3Title": "Regulatorische Compliance (EU AI Act, DSGVO, NIS2)",
    "sk3List": "<li><strong>EU AI Act:</strong> Risikoklassifizierung, GPAI-Governance und technische Dokumentation</li><li><strong>DSGVO & Datenschutz:</strong> Trainingsdaten-Compliance, Schutz vor automatisiertem Profiling</li><li><strong>NIS2 & DORA:</strong> Cyber-Resilienz der Lieferkette & finanztechnische Betriebsbereitschaft</li><li><strong>EU Data Act:</strong> Datenaustausch, Cloud-Interoperabilität und EU-Datensouveränität</li><li><strong>DSM-Urheberrecht:</strong> Text- & Data-Mining (TDM) Ausnahmen für KI-Modelltraining</li>",
    "sk4Title": "Taktische UAV-Systeme & Edge-Robotik",
    "sk4List": "<li><strong>Hardware-Bau:</strong> Handgelöteter 1500g 8-Zoll Carbon-Quad aus Einzelkomponenten</li><li><strong>Flugsoftware:</strong> Duale Betaflight-Dynamik & ArduPilot Copter Wegpunkt-Missionen</li><li><strong>Edge Vision KI:</strong> Raspberry Pi 5 (8GB) + Kamera 3 für integrierte Objekterkennung</li><li><strong>Avionik & Telemetrie:</strong> Skystars H7 Dual Gyro FC, AM60 60A ESC, RadioMaster ELRS, GNSS</li><li><strong>Zertifizierungen:</strong> EASA A1/A3 lizenzierter Drohnenpilot, 2,6 Mio. € Coverdrone-Haftpflicht</li>",

    "droneLabel": "✦ UAV-Systeme",
    "droneHeading": "Handgebaut. Flugerprobt. KI-unterstützt.",
    "droneIntro": "Maßgeschneiderter 1500g Carbon-Quadcopter. Ursprünglich auf Betaflight geflogen, betrieben mit ArduPilot, mit Raspberry Pi 5 Edge-Vision-KI. EASA A1/A3 zertifiziert, 2,6 Mio. € versichert (Hobbyprojekt).",
    "dCap1": "20s Outdoor-Zusammenstellung — Feldflug & Wegpunkt-Navigationstests",
    "dCap2": "Handgebauter 1500g Carbon-Quad — Jungfernflug & Telemetrieverifizierung",
    "dCap3": "ArduPilot Missionsplanung — automatisierte Multi-Wegpunkt-Führung",

    "expLabel": "✦ Expertise",
    "expHeading": "Ein Fokus. Autonome Agenten.",
    "expIntro": "Ein Fokus: autonome KI-Agenten, die Ihre Prozesse steuern.",
    "exp1Title": "Autonome Agenten-Systeme",
    "exp1Desc": "Ich baue 24/7 autonome Agenten mit Hermes Agent auf Hetzner VPS mit Telegram & WhatsApp C2, OpenRouter und persistentem Speicher.",
    "exp2Title": "EU AI Act & Compliance",
    "exp2Desc": "Ich analysiere EU-KI-Regulierungen für auditierbare Systeme. Nur technische Compliance, keine Rechtsberatung.",
    "exp3Title": "UAV-Systeme & Edge-KI",
    "exp3Desc": "Handgebauter 1500g Carbon-Quad mit ArduPilot und Raspberry Pi 5 Edge Vision. EASA A1/A3 zertifiziert (Hobby).",
    "exp4Title": "Produktmanager (Defence)",
    "exp4Desc": "Hintergrund in der Verteidigungsindustrie — Leitung klassifizierter Hardware- und Softwareprojekte.",

    "blogSecLabel": "✦ Blog",
    "blogSecHeading": "Aktuelle Beiträge.",
    "blogSecIntro": "KI-Agenten, autonome Systeme und Building in Public.",
    "blogBadge": "✦ Engineering & Gedankenprotokoll",
    "blogTitle": "Artikel & <span>Einblicke</span>",
    "blogSubtitle": "Autonome KI-Agenten, Legal-by-Design-Frameworks (AI Act & DSGVO) und Drohnen-Engineering.",
    "blogHomeLink": "← Startseite",
    "blogAllBtn": "Alle Beiträge lesen →",
    "blogReadPost": "Beitrag lesen",

    "faqLabel": "✦ FAQ",
    "faqHeading": "Häufig gestellte Fragen",
    "faq1q": "Wer ist Marian Stancik?",
    "faq1a": "<strong>Marian Stancik</strong> baut autonome KI-Agenten für Gründer und Unternehmen. Er ist spezialisiert auf Agenten-Entwicklung, KI-Web-Audits (GEO und Compliance) und Multi-Agenten-Orchestrierung mit Hermes Agent.",
    "faq2q": "Was prüft ein KI-GEO-Audit?",
    "faq2a": "Ein KI-GEO-Audit prüft die Sichtbarkeit Ihrer Website für KI-Suchmaschinen wie Perplexity, ChatGPT Search, Claude und Google SGE. <strong>150 €</strong> — einmaliges Audit, Bericht in 48 Stunden.",
    "faq3q": "Was ist der KI-Web-Readiness-Scan?",
    "faq3a": "Eine <strong>technische Prüfung durch einen KI-Agenten</strong> bezüglich erforderlicher rechtlicher Dokumente (Datenschutz, DSGVO, AGB, Disclaimer, AI Act). <strong>200 €</strong> — Bericht in 48 Stunden.",
    "faq4q": "Bietet Marian Rechtsberatung an?",
    "faq4a": "<strong>Nein.</strong> Marian studiert Recht, ist aber kein Anwalt. Seine Agenten führen <strong>nur technische Prüfungen</strong> durch. Rechtsfragen gehören zu einem qualifizierten Anwalt.",

    "leadLabel": "✦ Bleiben Sie informiert",
    "leadHeading": "Updates aus der Entwicklung.",
    "leadIntro": "KI-Agenten-Einblicke, Drohnen-Builds, Tech-Notizen — direkt in Ihr Postfach.",
    "subscribeBtn": "Abonnieren",
    "leadNote": "Kein Spam. Jederzeit abbestellbar. Erstellt mit AgentMail.",
    "leadConsentText": "Ich stimme der <a href=\"/privacy\" style=\"color:#CD7F32;text-decoration:underline;\">Datenschutzerklärung</a> und der Verarbeitung meiner E-Mail-Adresse zu.",
    "connLabel": "✦ Kontakt",
    "connHeading": "Lassen Sie uns etwas bauen.",
    "connIntro": "Folgen Sie dem Projekt, lesen Sie den Blog oder schreiben Sie direkt.",
    "connBlogText": "Blog",
    "bookLabel": "✉️ Kontakt aufnehmen",
    "bookHeading": "Lassen Sie uns über Ihr Projekt sprechen.",
    "bookIntro": "Schreiben Sie an <a href=\"mailto:marianstancik@agentmail.to\">marianstancik@agentmail.to</a>.",
    "bookCard1Cta": "E-Mail über KI-Agenten",
    "bookCard2Cta": "E-Mail über Compliance",
    "bookCard3Cta": "E-Mail über UAV / Edge-KI",
    "bookNote": "ASCENTIA s.r.o. — <a href=\"mailto:marianstancik@agentmail.to\" style=\"color:#CD7F32;\">marianstancik@agentmail.to</a>.",

    "footerTagline": "Ich baue KI-Agenten, die Ihre Prozesse steuern. Autonome Systeme auf eigener Infrastruktur.",
    "fCol1Title": "Navigation",
    "fCol2Title": "Projekte",
    "fCol3Title": "Kontakt",
    "fNavHome": "Startseite",
    "fNavAbout": "Über mich",
    "fNavExp": "Expertise",
    "fNavProj": "Projekte",
    "fNavConn": "Kontakt",
    "fNavBlog": "Blog",
    "fNavSkills": "Fähigkeiten",
    "fNavServices": "Produkte",
    "fNavProducts": "Produkte",
    "fMotto": "Besser bauen. Konform bleiben.",
    "footerImprint": "<strong>ASCENTIA s.r.o.</strong> · Klincová 37/B, 821 08 Bratislava · Geschäftsführer: Marián Stančík · <a href=\"mailto:marianstancik@agentmail.to\" style=\"color:#CD7F32;\">marianstancik@agentmail.to</a>",
    "footerAiAct": "<strong>⚠️ Disclaimer:</strong> Inhalte wurden durch autonome KI-Agenten (Hermes Agent) generiert/unterstützt. ⚖️ EU AI Act Art. 50 konform gekennzeichnet."
}

# Polish translations
TRANSLATIONS["pl"] = {
    **TRANSLATIONS["en"],
    "docTitle": "Marian Stancik — Deweloper Agentów AI | Systemy Autonomiczne",
    "docDesc": "Marian Stancik — Buduję agentów AI, którzy zarządzają Twoimi procesami. Dedykowane agenty autonomiczne i audyty stron AI.",
    "ogTitle": "Marian Stancik — Deweloper Agentów AI | Systemy Autonomiczne",
    "ogDesc": "Buduję agentów AI, którzy zarządzają Twoimi procesami. Systemy autonomiczne na własnej infrastrukturze, gotowe na środowiska regulowane. Hetzner VPS 24/7.",
    "skipLink": "Przejdź do treści głównej",
    "navHome": "Strona główna",
    "navAbout": "O mnie",
    "navSkills": "Umiejętności",
    "navDrones": "Drony",
    "navExpertise": "Ekspertyza",
    "navProjects": "Projekty",
    "navBlog": "Blog",
    "navContact": "✦ Kontakt",
    "navProducts": "Produkty",
    "navServices": "Produkty",
    "heroBadge": "✦ Buduję agentów AI, którzy zarządzają Twoimi procesami",
    "heroTagline": "Buduję <strong>agentów AI</strong>, którzy zarządzają Twoimi procesami. Systemy autonomiczne, audyty sieciowe i dedykowane przepływy pracy dla founderów.",
    "roleAi": "Deweloper Agentów AI",
    "roleUav": "Inżynieria Sprzętowa (Hobby)",
    "roleDrone": "Pilot Drona (EASA A1/A3)",
    "rolePm": "Deweloper Agentów AI",
    "roleLaw": "Świadomość Regulacyjna (PF UK)",
    "heroEmail": "E-mail",
    "heroCta": "✦ Zobacz Produkty",
    "heroContact": "Rozpocznij Rozmowę →",
    "scrollText": "Przewiń",

    "homeProductsLabel": "✦ Produkty",
    "homeProductsHeading": "Co buduję",
    "homeProductsIntro": "Agenci AI audytujący Twoją obecność w sieci oraz dedykowane systemy autonomiczne dla Twojej firmy.",
    "prodGeoTitle": "Audyt AI GEO",
    "prodGeoDesc": "Czy Twoja strona jest gotowa na wyszukiwarki AI? Sprawdzenie llms.txt, JSON-LD, robots.txt i widoczności AI.",
    "prodGeoPrice": "150 € →",
    "prodReadinessTitle": "Skan Gotowości AI",
    "prodReadinessDesc": "Techniczny audyt zgodności: Polityka Prywatności, RODO, Regulamin, Disclaimer i oznaczanie AI.",
    "prodReadinessPrice": "200 € →",
    "prodFullTitle": "Pełny Audyt Strony",
    "prodFullDesc": "Połączenie obu audytów: GEO + gotowość techniczna w jednym kompleksowym raporcie.",
    "prodFullPrice": "300 € →",
    "prodCustomTitle": "Dedykowany Agent AI",
    "prodCustomDesc": "Produkcyjny agent autonomiczny zbudowany pod Twoje specyficzne procesy biznesowe.",
    "prodCustomPrice": "Od 500 € →",
    "trustLaw": "⚖️ <strong>Zgodność Regulacyjna</strong> — Badania nad EU AI Act & RODO",
    "trustUav": "🚁 <strong>Inżynieria Sprzętowa</strong> — Ręcznie budowany dron EASA & Edge AI",
    "trustPfuk": "🎓 <strong>PF UK</strong> — EU AI Act, RODO, NIS2",

    "aboutLabel": "✦ O mnie",
    "aboutHeading": "Deweloper Agentów AI. Systemy, które zarządzają Twoimi procesami.",
    "aboutIntro": "Buduję autonomicznych agentów AI, którzy przejmują procesy biznesowe — content, CRM, monitoring i automatyzację. 24/7 na własnej infrastrukturze.",
    "aboutBody": "<p>Buduję <strong>autonomicznych agentów AI</strong> przy użyciu frameworka <strong>Hermes Agent</strong>. Moja infrastruktura działa 24/7 na <strong>Hetzner Cloud VPS</strong> w Niemczech/Finlandii, orkiestrując modele przez <strong>OpenRouter API</strong> z bazą <strong>Obsidian</strong> jako pamięcią kontekstową.</p><p>Tworzę aplikacje internetowe w technologii zero-build <strong>HTML5, Vanilla JS i nowoczesnym CSS</strong> — zaprojektowane z myślą o natychmiastowym ładowaniu (Lighthouse 100) i widoczności w wyszukiwarkach AI (GEO / LLMO).</p><p>Studiuję prawo na PF UK i analizuję regulacje <strong>EU AI Act, RODO, NIS2, DORA</strong>. Pomaga mi to tworzyć agentów AI gotowych na środowiska regulowane (wyłącznie wiedza techniczna, nie porada prawna).</p>",
    "aboutBodyText": "<p>Buduję <strong>autonomicznych agentów AI</strong> z frameworkiem Hermes Agent. Moja infrastruktura działa 24/7 na Hetzner VPS, zarządzając przepływami pracy dla marketingu, CRM i monitoringu.</p><p>Studiuję prawo na <strong>PF UK</strong> — EU AI Act, RODO, NIS2. Pozwala mi to projektować systemy technicznie przygotowane na wymogi prawne. <strong>Nie jestem prawnikiem i nie świadczę porad prawnych.</strong></p><p>Drony buduję jako <strong>hobby</strong> — 1500g quad węglowy z ArduPilotem i Raspberry Pi 5 Edge AI (licencja EASA A1/A3).</p><div class=\"highlight\" style=\"background:rgba(205,127,50,0.08);padding:1.2rem;border-left:3px solid #CD7F32;margin:1.5rem 0;border-radius:6px;font-size:0.88rem;\"><p style=\"margin:0;\"><strong style=\"color:#E8B86D;\">⚠️ Uwaga:</strong> Brak porad prawnych. Treści mają wyłącznie charakter edukacyjny.</p></div>",

    "stat1Label": "Aktywnych Agentów Cron",
    "stat2Label": "Domeny Inżynieryjne",
    "stat3Label": "Lata Doświadczenia",
    "stat4Label": "Ubezpieczenie Drona",
    "stat5Label": "Repozytoria Open Source",
    "stat6Label": "Czas Pracy 24/7",
    "stat1": "Aktywnych Agentów Cron",
    "stat2": "Domeny Inżynieryjne",
    "stat3": "Lata Doświadczenia",
    "stat4": "Ubezpieczenie Drona",
    "stat5": "Repozytoria Open Source",
    "stat6": "Czas Pracy 24/7",

    "cockpitStatus": "HERMES C2 // 24/7 AUTONOMICZNY RUNTIME ONLINE",
    "cockpitChip": "HETZNER VPS · SUWERENNOŚĆ DANYCH UE",
    "cockpitStat1Title": "Autonomiczne Pętle Cron",
    "cockpitStat1Sub": "24/7 orkiestracja w tle dla Contentu, CRM i Monitoringu",
    "cockpitStat2Title": "Dynamiczny Routing OpenRouter",
    "cockpitStat2Sub": "DeepSeek R1/V3 · Claude 3.5 Sonnet · synteza GPT-4o",
    "cockpitStat3Title": "Trwała Pamięć Vault",
    "cockpitStat3Sub": "Stan SQLite + dwukierunkowy graf wiedzy Markdown",
    "cockpitStat4Title": "Zgodność z EU AI Act i RODO",
    "cockpitStat4Sub": "Oznaczanie AI wg Art. 50 i audytowalna dokumentacja",

    "whatIDoTitle": "Co robię",
    "whatIDoSubtitle": "Praca · Kontekst · Hobby — wyraźny podział.",
    "card1Title": "Deweloper Agentów AI (Praca)",
    "card1Desc": "Projektuję, wdrażam i utrzymuję autonomicznych agentów AI na infrastrukturze klienta lub VPS. Serwery MCP, multi-LLM i automatyzacja cron.",
    "card2Title": "Kontekst Regulacyjny (PF UK)",
    "card2Desc": "Studia prawnicze PF UK. Znajomość EU AI Act, RODO, NIS2 wykorzystywana do budowy audytowalnych agentów.",
    "card3Title": "Inżynieria Sprzętowa (Hobby)",
    "card3Desc": "Ręcznie lutowany quad węglowy 1500g z ArduPilotem i Raspberry Pi 5. Certyfikat EASA A1/A3, ubezpieczenie 2,6 mln €.",
    "whatIDontDoTitle": "Czego nie robię",
    "whatIDontDoSubtitle": "Jasne granice współpracy.",
    "dont1Title": "Brak porad prawnych",
    "dont1Desc": "Jestem studentem, nie adwokatem. Moi agenci wykonują testy techniczne — opinia prawna należy do Twojego radcy.",
    "dont2Title": "Brak usług dronowych",
    "dont2Desc": "Nie sprzedaję dronów ani nie świadczę komercyjnych usług lotniczych. Dron to projekt inżynieryjny.",
    "dont3Title": "Bez agencji i pośredników",
    "dont3Desc": "Pracuję bezpośrednio z klientami. Rozmawiasz z inżynierem budującym Twój system.",

    "focus1Title": "Automatyzacja Procesów",
    "focus1Desc": "Obsługa leadów, CRM, publikacja treści — agenci przejmują czasochłonne zadania zespołu.",
    "focus2Title": "Audyty Stron AI",
    "focus2Desc": "Audyt GEO (widoczność w wyszukiwarkach AI) i skan gotowości technicznej.",
    "focus3Title": "Dedykowani Agenci AI",
    "focus3Desc": "Twój proces, Twoje dane, Twoja infrastruktura. Dedykowany agent działający 24/7.",
    "focus4Title": "Systemy Zgodne z Prawem",
    "focus4Desc": "Architektura projektowana od podstaw z uwzględnieniem RODO i EU AI Act.",

    "timelineTitle": "Moja Droga",
    "timelineSubtitle": "Ewolucja inżynieryjna — od prompt engineeringu do w pełni autonomicznych systemów.",
    "t2026Title": "Hermes Agent & System Autonomiczny",
    "t2026Desc": "Utrzymanie 24/7 infrastruktury wieloagentowej na Hetzner VPS z 19+ zadaniami cron.",
    "t2025Title": "Pierwsze agenty autonomiczne & MCP",
    "t2025Desc": "Przejście do aktywnych agentów narzędziowych z serwerami MCP i pamięcią Obsidian.",
    "t2024Title": "IDE Antigravity & AI Engineering",
    "t2024Desc": "Wdrożenie nowoczesnych przepływów programowania. Budowa quada 1500g z wizją Raspberry Pi 5.",
    "t2023Title": "Początki chatbotów AI & GPT",
    "t2023Desc": "Pierwsze integracje LLM, inżynieria promptów i automatyzacja skryptowa 24/7.",

    "skillsLabel": "✦ Umiejętności Agentów AI",
    "skillsHeading": "Umiejętności i Możliwości",
    "skillsIntro": "Full-stack inżynieria AI — od orkiestracji LLM i pętli Hermes Agent po infrastrukturę chmurową, zgodność prawną i sprzęt.",
    "sk1Title": "Hermes Agent & Systemy Wieloagentowe",
    "sk1List": "<li><strong>Hermes Agent:</strong> Autonomiczne pętle wykonawcze na 24/7 Hetzner VPS</li><li><strong>Projektowanie Serwerów MCP:</strong> Dedykowane narzędzia Model Context Protocol i API</li><li><strong>OpenRouter Multi-LLM:</strong> Dynamiczny routing między DeepSeek, Claude 3.5 i GPT-4o</li><li><strong>Obsidian Memory Layer:</strong> Baza Markdown zapewniająca trwałą pamięć agentów</li><li><strong>Interfejsy C2:</strong> Interaktywna kontrola przez boty Telegram i WhatsApp</li>",
    "sk2Title": "Oprogramowanie, Szybki Web i Chmura",
    "sk2List": "<li><strong>Ekosystem Python 3:</strong> FastAPI, Asyncio, Playwright, automatyzacja narzędzi</li><li><strong>Zero-Build High-Perf Web:</strong> 100% Czysty HTML5/CSS3/JS, PageSpeed 100 i 0ms TBT</li><li><strong>GEO i Agentic Browsing:</strong> Standard llmstxt.org v2, optymalizacja pod Perplexity i roboty LLM</li><li><strong>Administracja Linux VPS:</strong> Ubuntu Server na Hetzner Cloud (DE/FI), Caddy i SSL</li><li><strong>Operacje Produkcyjne:</strong> 19+ zadań cron 24/7, trwałość SQLite i monitoring</li>",
    "sk3Title": "Świadomość Regulacyjna (EU AI Act, RODO, NIS2)",
    "sk3List": "<li><strong>EU AI Act:</strong> Klasyfikacja ryzyka, zarządzanie GPAI i dokumentacja techniczna</li><li><strong>RODO i Prywatność:</strong> Zgodność danych treningowych i ochrona przed profilowaniem</li><li><strong>NIS2 i DORA:</strong> Cyberodporność łańcucha dostaw i gotowość operacyjna fintech</li><li><strong>EU Data Act:</strong> Wymiana danych, interoperacyjność chmur i suwerenność danych UE</li><li><strong>Prawo Autorskie DSM:</strong> Wyjątki Text & Data Mining (TDM) dla treningu modeli AI</li>",
    "sk4Title": "Taktyczne Systemy UAV i Robotyka Brzegowa",
    "sk4List": "<li><strong>Konstrukcja Sprzętowa:</strong> Ręcznie lutowany 1500g 8-calowy quad węglowy</li><li><strong>Oprogramowanie Lotu:</strong> Podwójna dynamika Betaflight i misje waypointów ArduPilot Copter</li><li><strong>Wizja AI Edge:</strong> Raspberry Pi 5 (8GB) + Camera 3 do detekcji obiektów w czasie rzeczywistym</li><li><strong>Awionika i Telemetria:</strong> Skystars H7 Dual Gyro FC, AM60 60A ESC, RadioMaster ELRS, GNSS</li><li><strong>Certyfikaty:</strong> Licencjonowany pilot drona EASA A1/A3, ubezpieczenie OC Coverdrone 2,6 mln €</li>",

    "droneLabel": "✦ Systemy UAV",
    "droneHeading": "Ręcznie zbudowany. Przetestowany w locie. Wspierany przez AI.",
    "droneIntro": "Dedykowany quadcopter węglowy 1500g. Napędzany przez ArduPilot, z pokładową wizją AI Raspberry Pi 5. Certyfikat EASA A1/A3, ubezpieczenie 2,6 mln € (projekt hobbystyczny).",
    "dCap1": "20-sekundowa kompilacja wideo — loty polowe i testy nawigacji waypointów",
    "dCap2": "Ręcznie zbudowany quad węglowy 1500g — dziewiczy lot i weryfikacja telemetrii",
    "dCap3": "Planowanie misji ArduPilot — zautomatyzowane prowadzenie wielopunktowe",

    "expLabel": "✦ Ekspertyza",
    "expHeading": "Jeden cel. Autonomiczni agenci.",
    "expIntro": "Jeden cel: autonomiczni agenci AI, którzy zarządzają Twoimi procesami biznesowymi.",
    "exp1Title": "Systemy Agentów Autonomicznych",
    "exp1Desc": "Buduję agentów 24/7 z Hermes Agent na Hetzner VPS z interfejsami C2 Telegram i WhatsApp oraz dynamicznym routingiem OpenRouter.",
    "exp2Title": "EU AI Act i Zgodność Prawna",
    "exp2Desc": "Analizuję regulacje AI w UE na potrzeby audytowalnych systemów. Wyłącznie kontekst techniczny.",
    "exp3Title": "Systemy UAV i Edge AI",
    "exp3Desc": "Ręcznie budowany quad 1500g z ArduPilotem i Raspberry Pi 5 Edge Vision. Certyfikat EASA A1/A3 (hobby).",
    "exp4Title": "Product Manager (Defence)",
    "exp4Desc": "Doświadczenie w przemyśle obronnym — zarządzanie niejawnymi projektami sprzętowymi i programistycznymi.",

    "blogSecLabel": "✦ Blog",
    "blogSecHeading": "Najnowsze wpisy.",
    "blogSecIntro": "Agenci AI, systemy autonomiczne i budowanie w publiczności.",
    "blogBadge": "✦ Dziennik Inżynieryjny & Myśli",
    "blogTitle": "Artykuły & <span>Wnioski</span>",
    "blogSubtitle": "Autonomiczni agenci AI, ramy legal-by-design (AI Act & RODO) oraz inżynieria dronów.",
    "blogHomeLink": "← Strona główna",
    "blogAllBtn": "Przeczytaj wszystkie wpisy →",
    "blogReadPost": "Przeczytaj artykuł",

    "faqLabel": "✦ FAQ",
    "faqHeading": "Najczęściej Zadawane Pytania",
    "faq1q": "Kim jest Marian Stancik?",
    "faq1a": "<strong>Marian Stancik</strong> buduje autonomicznych agentów AI dla firm i founderów. Specjalizuje się w dedykowanych systemach wieloagentowych, audytach AI (GEO i gotowości) oraz orkiestracji z frameworkiem Hermes Agent.",
    "faq2q": "Co sprawdza Audyt AI GEO?",
    "faq2a": "Audyt AI GEO sprawdza widoczność strony w wyszukiwarkach AI (Perplexity, ChatGPT, Claude, Google SGE). <strong>150 €</strong> — jednorazowy audyt, raport w 48h.",
    "faq3q": "Czym jest Skan Gotowości AI?",
    "faq3a": "Techniczna weryfikacja dokumentów prawnych strony (RODO, regulamin, disclaimer, oznaczanie AI). <strong>200 €</strong> — raport w 48h.",
    "faq4q": "Czy Marian świadczy porady prawne?",
    "faq4a": "<strong>Nie.</strong> Marian studiuje prawo, ale nie jest prawnikiem. Jego agenci wykonują <strong>wyłącznie testy techniczne</strong>.",

    "leadLabel": "✦ Bądź na bieżąco",
    "leadHeading": "Aktualności z procesu budowy.",
    "leadIntro": "Wnioski z AI, budowy dronów i technologii — prosto na Twoją skrzynkę.",
    "subscribeBtn": "Subskrybuj",
    "leadNote": "Brak spamu. Możliwość wypisania się w każdej chwili. Obsługiwane przez AgentMail.",
    "leadConsentText": "Zgadzam się z <a href=\"/privacy\" style=\"color:#CD7F32;text-decoration:underline;\">Polityką Prywatności</a> i wyrażam zgodę na przetwarzanie adresu e-mail.",
    "connLabel": "✦ Kontakt",
    "connHeading": "Zbudujmy coś razem.",
    "connIntro": "Śledź projekt, czytaj bloga lub skontaktuj się bezpośrednio.",
    "connBlogText": "Blog",
    "bookLabel": "✉️ Skontaktuj się",
    "bookHeading": "Porozmawiajmy o Twoim projekcie.",
    "bookIntro": "Napisz na <a href=\"mailto:marianstancik@agentmail.to\">marianstancik@agentmail.to</a>.",
    "bookCard1Cta": "E-mail o agentach AI",
    "bookCard2Cta": "E-mail o zgodności regulacyjnej",
    "bookCard3Cta": "E-mail o UAV / Edge AI",
    "bookNote": "ASCENTIA s.r.o. — <a href=\"mailto:marianstancik@agentmail.to\" style=\"color:#CD7F32;\">marianstancik@agentmail.to</a>.",

    "footerTagline": "Buduję agentów AI, którzy zarządzają Twoimi procesami. Systemy autonomiczne na własnej infrastrukturze.",
    "fCol1Title": "Nawigacja",
    "fCol2Title": "Projekty",
    "fCol3Title": "Kontakt",
    "fNavHome": "Strona główna",
    "fNavAbout": "O mnie",
    "fNavExp": "Ekspertyza",
    "fNavProj": "Projekty",
    "fNavConn": "Kontakt",
    "fNavBlog": "Blog",
    "fNavSkills": "Umiejętności",
    "fNavServices": "Produkty",
    "fNavProducts": "Produkty",
    "fMotto": "Buduj lepiej. Pozostań w zgodzie z prawem.",
    "footerImprint": "<strong>ASCENTIA s.r.o.</strong> · Klincová 37/B, 821 08 Bratislava · Zarząd: Marián Stančík · <a href=\"mailto:marianstancik@agentmail.to\" style=\"color:#CD7F32;\">marianstancik@agentmail.to</a>",
    "footerAiAct": "<strong>⚠️ Disclaimer:</strong> Treść generowana/wspierana przez autonomicznych agentów AI (Hermes Agent). ⚖️ Zgodność z Art. 50 EU AI Act."
}

# Slovak translations
TRANSLATIONS["sk"] = {
    **TRANSLATIONS["en"],
    "docTitle": "Marian Stancik — AI Agent Developer | Autonómne Agenty",
    "docDesc": "Marian Stancik — staviam AI agentov, ktorí riadia tvoje procesy. Vlastné autonómne agenty, AI audity webu pre éru AI vyhľadávania.",
    "ogTitle": "Marian Stancik — AI Agent Developer | Autonómne Agenty",
    "ogDesc": "Staviam AI agentov, ktorí riadia tvoje procesy. Autonómne systémy na vlastnej infraštruktúre, ready pre regulované prostredie.. 24/7 runtime na Hetzner VPS.",
    "skipLink": "Preskočiť na hlavný obsah",
    "navHome": "Domov",
    "navAbout": "O mne",
    "navSkills": "Zručnosti",
    "navDrones": "Drony",
    "navExpertise": "Odbornosť",
    "navProjects": "Projekty",
    "navBlog": "Blog",
    "navContact": "✦ Kontakt",
    "navProducts": "Produkty",
    "navServices": "Produkty",
    "heroBadge": "✦ Staviam AI agentov, ktorí riadia tvoje procesy",
    "heroTagline": "Staviam <strong>AI agentov</strong>, ktorí riadia tvoje procesy. Autonómne systémy, web audity a vlastní AI agenti pre kreatívnych founderov.",
    "roleAi": "AI Agent Developer",
    "roleUav": "Hardvérové inžinierstvo (Hobby)",
    "roleDrone": "Pilot dronov (EASA A1/A3)",
    "rolePm": "AI Agent Developer",
    "roleLaw": "Regulačné povedomie (PF UK)",
    "heroEmail": "Email",
    "heroCta": "✦ Pozrieť Produkty",
    "heroContact": "Začať Konverzáciu →",
    "scrollText": "Posunúť",

    "homeProductsLabel": "✦ Produkty",
    "homeProductsHeading": "Čo Staviam",
    "homeProductsIntro": "AI agenti, ktorí auditujú vašu webovú prítomnosť, a zákazkoví autonómni agenti pre vaše podnikanie.",
    "prodGeoTitle": "AI GEO Audit",
    "prodGeoDesc": "Je váš web pripravený pre AI vyhľadávače? Agent preverí llms.txt, JSON-LD, robots.txt a AI viditeľnosť.",
    "prodGeoPrice": "150 € →",
    "prodReadinessTitle": "AI Web Readiness Scan",
    "prodReadinessDesc": "Technická kontrola právnych dokumentov webu. Agent overí Privacy Policy, GDPR súhlas a podmienky.",
    "prodReadinessPrice": "200 € →",
    "prodFullTitle": "Kompletný Web Audit",
    "prodFullDesc": "Oba audity spojené. GEO + technická pripravenosť v jednej komplexnej správe s prioritnou maticou.",
    "prodFullPrice": "300 € →",
    "prodCustomTitle": "Vlastný AI Agent",
    "prodCustomDesc": "Produkčný autonómny agent postavený na mieru pre vašu špecifickú firemnú potrebu. Prevádzka 24/7.",
    "prodCustomPrice": "Od 500 € →",
    "trustLaw": "⚖️ <strong>Regulačné povedomie</strong> — Študujem EU AI Act, staviam pre regulované prostredia",
    "trustUav": "🚁 <strong>Hardvérové inžinierstvo</strong> — Vlastnoručný dron, certifikácia EASA, edge AI",
    "trustPfuk": "🎓 <strong>PF UK</strong> — EU AI Act, GDPR, NIS2",

    "aboutLabel": "✦ O mne",
    "aboutHeading": "AI Agent Developer. Staviam systémy, ktoré riadia vaše procesy.",
    "aboutIntro": "Staviam autonómnych AI agentov, ktorí riadia firemné procesy — obsah, CRM, monitoring a automatizáciu. 24/7, na vlastnej infraštruktúre, bez nutnosti dohľadu.",
    "aboutBody": "<p>Staviam <strong>autonómnych AI agentov</strong> pomocou frameworku <strong>Hermes Agent</strong> (od Nous Research). Moja infraštruktúra beží 24/7 na dedikovanom <strong>Hetzner Cloud VPS</strong> v Nemecku/Fínsku, orchestruje pokročilé modely cez <strong>OpenRouter API</strong> s <strong>Obsidianom</strong> ako perzistentnou pamäťovou vrstvou. <em>Tento web a všetok obsah je tvorený a spravovaný mojím autonómnym Hermes Agentom.</em></p><p>Weby staviam s technológiou zero-build <strong>HTML5, Vanilla JS a moderným CSS</strong> — navrhnuté pre okamžité načítanie (Lighthouse 100) a objaviteľnosť AI vyhľadávačmi (GEO / LLMO).</p><p>Študujem právo na <strong>PF UK</strong> — EU AI Act, GDPR, NIS2, DORA a autorské právo DSM. Toto regulačné povedomie mi umožňuje stavať AI agentov pripravených pre regulované prostredie (edukatívne informácie, nie právne poradenstvo).</p><p>V hardvéri som <strong>vlastnoručne navrhol, pospájkoval a zostavil 1500g karbónový taktický quadcopter</strong> s ArduPilotom a Raspberry Pi 5 palubným počítačovým videním. Certifikácia EASA A1/A3, poistenie Coverdrone 2,6 mil. €.</p>",
    "aboutBodyText": "<p>Staviam <strong>autonómnych AI agentov</strong> pomocou frameworku <strong>Hermes Agent</strong>. Moja infraštruktúra beží 24/7 na Hetzner VPS, kde orchestruje multi-LLM agentov pre obsah, CRM, monitoring a automatizáciu.</p><p>Študujem právo na <strong>PF UK</strong> (Univerzita Komenského v Bratislave) — EU AI Act, GDPR, NIS2 a technologickú reguláciu. Rozumiem právnemu kontextu a viem stavať AI agentov <strong>technicky pripravených na regulované prostredie</strong>. <strong>Nie som advokát, neposkytujem právne poradenstvo.</strong></p><p>Drony staviam ako <strong>hobby</strong> — ručne spájkovaný 1500g karbónový quad s ArduPilotom a Raspberry Pi 5 edge AI (licencia EASA A1/A3).</p><div class=\"highlight\" style=\"background:rgba(205,127,50,0.08);padding:1.2rem;border-left:3px solid #CD7F32;margin:1.5rem 0;border-radius:6px;font-size:0.88rem;\"><p style=\"margin:0;\"><strong style=\"color:#E8B86D;\">⚠️ Upozornenie:</strong> Toto nie je právne poradenstvo. Regulačné poznatky zdieľam výhradne na vzdelávacie a technické účely.</p></div>",

    "stat1Label": "Aktívnych Cron Agentov",
    "stat2Label": "Pokrytých Domén",
    "stat3Label": "Roky Vývoja",
    "stat4Label": "Poistenie Drona",
    "stat5Label": "Open Source Repozitáre",
    "stat6Label": "Runtime Agenta 24/7",
    "stat1": "Aktívnych Cron Agentov",
    "stat2": "Inžinierske Domény",
    "stat3": "Roky Vývoja",
    "stat4": "Poistenie Drona",
    "stat5": "Open Source Repozitáre",
    "stat6": "24/7 Runtime Agenta",

    "cockpitStatus": "HERMES C2 // 24/7 AUTONÓMNY RUNTIME ONLINE",
    "cockpitChip": "HETZNER VPS · DÁTOVÁ SUVERENITA EÚ",
    "cockpitStat1Title": "Autonómne Cron Slučky",
    "cockpitStat1Sub": "24/7 orchestrácia na pozadí pre Obsah, CRM, Sentinel & Monitoring",
    "cockpitStat2Title": "Dynamické OpenRouter Smerovanie",
    "cockpitStat2Sub": "DeepSeek R1/V3 · Claude 3.5 Sonnet · syntéza GPT-4o",
    "cockpitStat3Title": "Perzistentná Pamäť Vaultu",
    "cockpitStat3Sub": "SQLite stav + obojsmerný Markdown vedomostný graf",
    "cockpitStat4Title": "EU AI Act & GDPR Súlad",
    "cockpitStat4Sub": "Čl. 50 AI označovanie & technická dokumentácia pripravená na audit",

    "whatIDoTitle": "Čo robím",
    "whatIDoSubtitle": "Práca · Kontext · Hobby — jasné oddelenie.",
    "card1Title": "AI Agent Developer (Práca)",
    "card1Desc": "Navrhujem, staviam, nasadzujem a prevádzkujem autonómnych AI agentov na klientskej infraštruktúre alebo managed VPS. Vlastné MCP servery, multi-LLM orchestrácia a 24/7 cron automatizácia.",
    "card2Title": "Regulačný Kontext (PF UK)",
    "card2Desc": "Štúdium práva na PF UK. Povedomie o EU AI Act, GDPR, NIS2 využívané na stavbu agentov pripravených pre regulované prostredie. Iba edukatívne zdieľanie.",
    "card3Title": "Hardvérové Inžinierstvo (Hobby)",
    "card3Desc": "Ručne spájkovaný 1500g karbónový quad s ArduPilotom a Raspberry Pi 5 edge AI. Certifikácia EASA A1/A3, poistenie 2,6 mil. €.",
    "whatIDontDoTitle": "Čo nerobím",
    "whatIDontDoSubtitle": "Jasné hranice — aby ste presne vedeli, s kým spolupracujete.",
    "dont1Title": "Žiadne právne poradenstvo",
    "dont1Desc": "Som študent, nie advokát. Neposkytujem právne stanoviská ani advokátske služby. Moji agenti vykonávajú technické kontroly — právne posúdenie patrí vášmu právnikovi.",
    "dont2Title": "Žiadne dronové služby",
    "dont2Desc": "Nepredávam drony ani neposkytujem komerčné letecké práce. Dron je inžinierske hobby demonštrujúce schopnosti edge-AI.",
    "dont3Title": "Žiadne agentúry / sprostredkovatelia",
    "dont3Desc": "Staviam priamo s klientmi. Žiadny outsourcing, žiadny white-label. Komunikujete priamo s inžinierom, ktorý váš systém stavia.",

    "focus1Title": "Automatizácia Procesov",
    "focus1Desc": "Spracovanie leadov, CRM follow-upy, obsahové pipeline, reporting — agenti preberajú procesy, ktoré oberali váš tím o čas.",
    "focus2Title": "AI Audity Webu",
    "focus2Desc": "GEO audit (viditeľnosť v AI vyhľadávaní) a Web Readiness Scan (technická kontrola dokumentov) — agent preverí váš web.",
    "focus3Title": "Zákazkoví AI Agenti",
    "focus3Desc": "Váš proces, vaše dáta, vaša infraštruktúra. Agent postavený presne na jednu úlohu — vašu úlohu — s behom 24/7.",
    "focus4Title": "Regulačne Informovaný Vývoj",
    "focus4Desc": "Právne zázemie znamená, že agenti sú od prvého dňa navrhnutí s ohľadom na GDPR a AI Act.",

    "timelineTitle": "Ako som sa sem dostal",
    "timelineSubtitle": "Inžinierska evolúcia — od prompt engineeringu až po plne autonómne systémy.",
    "t2026Title": "Hermes Agent & Autonómny Systém (Môj AI Asistent)",
    "t2026Desc": "Prevádzka 24/7 autonómnej multi-agentovej infraštruktúry na Hetzner VPS. 19+ cron orchestrácií pre obsah, CRM a zdravie systému.",
    "t2025Title": "Prví autonómni agenti & Model Context Protocol (MCP)",
    "t2025Desc": "Prechod od pasívnych chatbotov k aktívnym autonómnym agentom s nástrojmi MCP a perzistentnou pamäťou Obsidian. Začiatok štúdia práva na PF UK.",
    "t2024Title": "IDE Antigravity & AI-Augmented Engineering",
    "t2024Desc": "Osvojenie moderných postupov agentického programovania. Stavba 1500g taktického quadcoptera s ArduPilotom a Raspberry Pi 5 edge vision AI.",
    "t2023Title": "Začiatok AI chatbotov & experimenty s GPT",
    "t2023Desc": "Prvý ponor do LLM, prompt engineeringu a konverzačných botov. Experimentovanie s API a objavenie potenciálu 24/7 autonómnej exekúcie.",

    "skillsLabel": "✦ AI Agent Zručnosti",
    "skillsHeading": "Zručnosti & Schopnosti",
    "skillsIntro": "Full-stack AI inžinierstvo — od orchestrácie LLM a slučiek Hermes Agenta po cloudovú infraštruktúru, regulačné povedomie a hardvérové inžinierstvo.",
    "sk1Title": "Hermes Agent & Multi-Agentové systémy",
    "sk1List": "<li><strong>Hermes Agent:</strong> Autonómne exekučné slučky & reflexia na 24/7 Hetzner VPS</li><li><strong>MCP Architektúra:</strong> Vlastné Model Context Protocol nástroje a integračné API</li><li><strong>OpenRouter Multi-LLM:</strong> Dynamické smerovanie modelov (DeepSeek, Claude 3.5 & GPT-4o)</li><li><strong>Obsidian Memory Layer:</strong> Obojsmerný markdown vault ako perzistentná pamäť agentov</li><li><strong>C2 Rozhrania:</strong> Interaktívne riadenie a kontrola cez Telegram & WhatsApp botov</li>",
    "sk2Title": "Softvér, Vysokovýkonný Web & Cloud",
    "sk2List": "<li><strong>Python 3 Ekosystém:</strong> FastAPI, Asyncio, Playwright, automatizácia toolchainov</li><li><strong>Zero-Build Web:</strong> 100% Čistý HTML5/CSS3/JS, PageSpeed 100 a 0ms TBT bez frameworkového balastu</li><li><strong>GEO & Agentic Browsing:</strong> Štandard llmstxt.org v2, optimalizácia pre Perplexity a LLM crawlery</li><li><strong>Linux VPS Administrácia:</strong> Ubuntu Server na Hetzner Cloud (DE/FI), Caddy reverzný proxy & SSL</li><li><strong>Produkčné Operácie:</strong> 19+ 24/7 cron orchestrácií, SQLite perzistencia & monitoring</li>",
    "sk3Title": "Regulačné Povedomie (EU AI Act, GDPR, NIS2)",
    "sk3List": "<li><strong>EU AI Act:</strong> Klasifikácia rizík, správa GPAI modelov a technická dokumentácia</li><li><strong>GDPR & Ochrana súkromia:</strong> Súlad trénovacích dát, garancie proti profilovaniu</li><li><strong>NIS2 & DORA:</strong> Kybernetická odolnosť dodávateľského reťazca & fintech pripravenosť</li><li><strong>EU Data Act:</strong> Zdieľanie dát, interoperabilita cloudov a dátová suverenita EÚ</li><li><strong>DSM Autorské právo:</strong> Výnimky pre Text & Data Mining (TDM) pri trénovaní AI modelov</li>",
    "sk4Title": "Taktické UAV Systémy & Edge Robotika",
    "sk4List": "<li><strong>Hardvérová Stavba:</strong> Ručne spájkovaný 1500g 8-palcový karbónový quad z komponentov</li><li><strong>Letový Softvér:</strong> Duálne ladenie dynamiky Betaflight & misie waypointov v ArduPilot Copter</li><li><strong>Edge Vision AI:</strong> Raspberry Pi 5 (8GB) + Camera 3 pre palubnú detekciu objektov</li><li><strong>Avionika & Telemetria:</strong> Skystars H7 Dual Gyro FC, AM60 60A ESC, RadioMaster ELRS, GNSS</li><li><strong>Certifikácie:</strong> Licencovaný pilot dronov EASA A1/A3, poistenie Coverdrone 2,6 mil. €</li>",

    "droneLabel": "✦ UAV Systémy",
    "droneHeading": "Ručne postavené. Otestované v lete. Poháňané AI.",
    "droneIntro": "Vlastný 1500g karbónový quadcopter pospájaný z jednotlivých komponentov. Poháňaný ArduPilotom, s palubným Raspberry Pi 5 edge vision AI. Certifikácia EASA A1/A3, poistenie 2,6 mil. € (hobby projekt).",
    "dCap1": "20s video kompilácia — poľné lety a testy autonómnej navigácie waypointov",
    "dCap2": "Ručne postavený 1500g karbónový quad — zálet a overenie telemetrie",
    "dCap3": "Plánovanie misií v ArduPilot — automatizované multi-waypoint navádzanie",

    "expLabel": "✦ Odbornosť",
    "expHeading": "Jedno zameranie. Autonómne agenty.",
    "expIntro": "Jedno zameranie: autonómni AI agenti, ktorí riadia vaše procesy. Štúdium práva a hardvér tvoria kontext.",
    "exp1Title": "Autonómne Agentové Systémy",
    "exp1Desc": "Staviam AI agentov pomocou frameworku Hermes Agent. 24/7 autonómne systémy na Hetzner VPS s Telegram a WhatsApp rozhraním.",
    "exp2Title": "EU AI Act & Regulačné Povedomie",
    "exp2Desc": "Študujem reguláciu AI v EÚ a poskytujem technický kontext pre stavbu auditovateľných systémov.",
    "exp3Title": "UAV Systémy & Edge AI",
    "exp3Desc": "Staviam drony — od návrhu po let s palubnou AI. Vlastné 1500g karbónové quady, ArduPilot misie a Raspberry Pi 5 edge vision. Certifikácia EASA A1/A3.",
    "exp4Title": "Product Manager (Defence)",
    "exp4Desc": "Zázemie v obrannom priemysle — riadenie utajovaných hardvérových a softvérových projektov.",

    "blogSecLabel": "✦ Blog",
    "blogSecHeading": "Najnovšie myšlienky.",
    "blogSecIntro": "AI agenti, autonómne systémy a building in public.",
    "blogBadge": "✦ Technický & Odborný Blog",
    "blogTitle": "Články & <span>Poznatky</span>",
    "blogSubtitle": "Autonómni AI agenti, legal-by-design rámce (AI Act & GDPR) a inžinierstvo dronov.",
    "blogHomeLink": "← Domov",
    "blogAllBtn": "Čítať všetky články →",
    "blogReadPost": "Čítať článok",

    "faqLabel": "✦ FAQ",
    "faqHeading": "Často kladené otázky",
    "faq1q": "Kto je Marian Stancik?",
    "faq1a": "<strong>Marian Stancik</strong> stavia autonómnych AI agentov pre kreatívnych founderov a firmy. Špecializuje sa na zákazkový vývoj agentov, AI audity webu (GEO a technická pripravenosť) a orchestráciu cez Hermes Agent. Štúdium práva na PF UK mu dáva regulačný prehľad a stavba dronov je technické hobby preukazujúce edge AI zručnosti.",
    "faq2q": "Čo kontroluje AI GEO Audit?",
    "faq2a": "AI GEO Audit overuje viditeľnosť vášho webu pre AI vyhľadávače ako Perplexity, ChatGPT Search, Claude a Google SGE. Kontroluje <strong>llms.txt</strong>, <strong>robots.txt</strong>, <strong>JSON-LD</strong> dáta, <strong>OpenGraph</strong>, <strong>hreflang</strong> a rýchlosť. <strong>150 €</strong> — jednorazový audit, správa do 48 hodín.",
    "faq3q": "Čo je AI Web Readiness Scan?",
    "faq3a": "AI Web Readiness Scan je <strong>technická kontrola AI agentom</strong>, ktorá overí prítomnosť povinných dokumentov — Privacy Policy, GDPR súhlas, Podmienky, Disclaimer, AI Act označenie a cookies. <strong>Nejde o právne poradenstvo</strong> — technický checklist. <strong>200 €</strong> — správa do 48 hodín.",
    "faq4q": "Poskytuje Marian právne poradenstvo?",
    "faq4a": "<strong>Nie.</strong> Marian študuje právo, nie je advokát. Neposkytuje právne poradenstvo ani právne služby. Jeho AI agenti vykonávajú <strong>výhradne technické kontroly</strong>. Pre právne záležitosti sa obráťte na kvalifikovaného advokáta.",

    "leadLabel": "✦ Zostaňte v kontakte",
    "leadHeading": "Získajte novinky z vývoja.",
    "leadIntro": "Poznatky o AI agentoch, stavbe dronov a technológiách — priamo do vašej schránky.",
    "subscribeBtn": "Odoberať",
    "leadNote": "Žiadny spam. Kedykoľvek sa môžete odhlásiť. Beží na AgentMail.",
    "leadConsentText": "Súhlasím so <a href=\"/privacy-sk\" style=\"color:#CD7F32;text-decoration:underline;\">zásadami ochrany osobných údajov</a> a spracovaním e-mailu.",
    "connLabel": "✦ Spojme sa",
    "connHeading": "Poďme niečo postaviť.",
    "connIntro": "Sledujte stavbu, čítajte blog alebo ma kontaktujte priamo.",
    "connBlogText": "Blog",
    "bookLabel": "✉️ Napíšte mi",
    "bookHeading": "Poďme sa porozprávať o projekte.",
    "bookIntro": "Napíšte na <a href=\"mailto:marianstancik@agentmail.to\">marianstancik@agentmail.to</a>. Kalendárové rezervácie neposkytujem — primárnym kanálom je e-mail.",
    "bookCard1Cta": "E-mail o AI agentoch",
    "bookCard2Cta": "E-mail o compliance",
    "bookCard3Cta": "E-mail o UAV / edge AI",
    "bookNote": "ASCENTIA s.r.o. — <a href=\"mailto:marianstancik@agentmail.to\" style=\"color:#CD7F32;\">marianstancik@agentmail.to</a>.",

    "footerTagline": "Staviam AI agentov, ktorí riadia tvoje procesy. Autonómne systémy na vlastnej infraštruktúre.",
    "fCol1Title": "Navigácia",
    "fCol2Title": "Projekty",
    "fCol3Title": "Kontakt",
    "fNavHome": "Domov",
    "fNavAbout": "O mne",
    "fNavServices": "Produkty",
    "fNavProducts": "Produkty",
    "fMotto": "Stavaj lepšie. Zostaň v súlade so zákonom.",
    "footerImprint": "<strong>ASCENTIA s.r.o.</strong> · Klincová 37/B, 821 08 Bratislava-Ružinov · IČO: 51858959 · DIČ: 2120816071 · konateľ: Marián Stančík<br>Obchodný register Mestského súdu Bratislava III, oddiel Sro, vložka 130384/B · <a href=\"mailto:marianstancik@agentmail.to\" style=\"color:#CD7F32;\">marianstancik@agentmail.to</a>",
    "footerAiAct": "<strong>⚠️ Zrieknutie zodpovednosti:</strong> Obsah je generovaný alebo asistovaný autonómnymi AI agentmi (Hermes Agent) na informačné účely. Nepredstavuje právne poradenstvo. ⚖️ EU AI Act Čl. 50: AI obsah je riadne označený."
}

# Generate js/i18n.js
js_content = f"""// Marian Stancik Personal Brand — Centralized Multilingual Engine (EN, SK, DE, PL) v5
// Zero-build, Lighthouse 100, Instant DOM Switching

const translations = {json.dumps(TRANSLATIONS, indent=2, ensure_ascii=False)};

let currentLang = 'en';
try {{
  currentLang = localStorage.getItem('ms_lang') || 'en';
  if (!translations[currentLang]) currentLang = 'en';
}} catch (e) {{
  currentLang = 'en';
}}

function switchLanguage(lang) {{
  if (!translations[lang]) lang = 'en';
  currentLang = lang;
  try {{
    localStorage.setItem('ms_lang', lang);
  }} catch(e) {{}}
  applyTranslations();
  if (typeof loadDynamicPostsHome === 'function') loadDynamicPostsHome();
  if (typeof renderBlogIndexPosts === 'function') renderBlogIndexPosts();
  window.dispatchEvent(new CustomEvent('languageChanged', {{ detail: {{ lang }} }}));
}}

// Expose globally
window.switchLanguage = switchLanguage;
window.applyTranslations = applyTranslations;
window.currentLang = currentLang;

function applyTranslations() {{
  const d = translations[currentLang] || translations.en;
  
  // 1. Update button active classes across any lang switcher
  const langButtons = {{
    'en': document.querySelectorAll('#btnEn, .btn-lang-en, [data-lang-btn="en"]'),
    'sk': document.querySelectorAll('#btnSk, .btn-lang-sk, [data-lang-btn="sk"]'),
    'de': document.querySelectorAll('#btnDe, .btn-lang-de, [data-lang-btn="de"]'),
    'pl': document.querySelectorAll('#btnPl, .btn-lang-pl, [data-lang-btn="pl"]')
  }};
  
  Object.keys(langButtons).forEach(k => {{
    langButtons[k].forEach(b => {{
      if (k === currentLang) b.classList.add('active');
      else b.classList.remove('active');
    }});
  }});

  // 2. Instant blog index pre-rendered post group switcher
  const enGroup = document.getElementById('postsEn');
  const skGroup = document.getElementById('postsSk');
  const deGroup = document.getElementById('postsDe');
  const plGroup = document.getElementById('postsPl');
  if (enGroup && skGroup && deGroup && plGroup) {{
    enGroup.style.display = currentLang === 'en' ? 'block' : 'none';
    skGroup.style.display = currentLang === 'sk' ? 'block' : 'none';
    deGroup.style.display = currentLang === 'de' ? 'block' : 'none';
    plGroup.style.display = currentLang === 'pl' ? 'block' : 'none';
  }}

  document.documentElement.lang = currentLang;
  if (d.docTitle) document.title = d.docTitle;
  
  const descEl = document.querySelector('meta[name="description"]');
  if (descEl && d.docDesc) descEl.setAttribute('content', d.docDesc);
  
  const ogTitleEl = document.querySelector('meta[property="og:title"]');
  if (ogTitleEl && d.ogTitle) ogTitleEl.setAttribute('content', d.ogTitle);
  
  const ogDescEl = document.querySelector('meta[property="og:description"]');
  if (ogDescEl && d.ogDesc) ogDescEl.setAttribute('content', d.ogDesc);

  // 3. Generic Update: any element with data-i18n matching key
  document.querySelectorAll('[data-i18n]').forEach(el => {{
    const key = el.getAttribute('data-i18n');
    if (d[key] !== undefined) {{
      const val = d[key];
      if (typeof val === 'string' && val.includes('<') && val.includes('>')) {{
        el.innerHTML = val;
      }} else {{
        el.textContent = val;
      }}
    }}
  }});

  // 4. Protected Layout Containers List
  const PROTECTED_TAGS = ['SECTION', 'MAIN', 'NAV', 'HEADER', 'FOOTER', 'BODY', 'HTML'];

  // Generic Update: any element with ID matching key in dictionary (skipping structural containers)
  Object.keys(d).forEach(key => {{
    const val = d[key];
    const el = document.getElementById(key);
    if (el) {{
      if (PROTECTED_TAGS.includes(el.tagName) && !el.hasAttribute('data-i18n')) {{
        return;
      }}
      if (typeof val === 'string' && val.includes('<') && val.includes('>')) {{
        el.innerHTML = val;
      }} else {{
        el.textContent = val;
      }}
    }}
  }});
}}

async function loadDynamicPostsHome() {{
  try {{
    const res = await fetch('/blog/posts.json');
    if (!res.ok) return;
    const posts = await res.json();
    if (!Array.isArray(posts) || posts.length === 0) return;
    const container = document.getElementById('homeBlogGrid');
    if (!container) return;
    const d = translations[currentLang] || translations.en;

    container.innerHTML = posts.slice(0, 3).map(p => {{
      let title = p.title;
      let excerpt = p.excerpt;
      let date = p.displayDate;
      let targetUrl = p.url;

      if (currentLang === 'sk') {{
        title = p.titleSk || p.title;
        excerpt = p.excerptSk || p.excerpt;
        date = p.displayDateSk || p.displayDate;
        targetUrl = p.urlSk || p.url;
      }} else if (currentLang === 'de') {{
        title = p.titleDe || p.title;
        excerpt = p.excerptDe || p.excerpt;
        date = p.displayDateDe || p.displayDate;
        targetUrl = p.urlDe || p.url;
      }} else if (currentLang === 'pl') {{
        title = p.titlePl || p.title;
        excerpt = p.excerptPl || p.excerpt;
        date = p.displayDatePl || p.displayDate;
        targetUrl = p.urlPl || p.url;
      }}

      return `
<a href="/${{targetUrl}}" class="blog-card fade-in visible">
  <div class="blog-card-date">${{date}}</div>
  <h3>${{title}}</h3>
  <p>${{excerpt}}</p>
  <div class="blog-card-arrow">${{d.blogReadPost || 'Read post'}} <span>→</span></div>
</a>`;
    }}).join('');
  }} catch(e){{}}
}}

async function renderBlogIndexPosts() {{
  const enGroup = document.getElementById('postsEn');
  const skGroup = document.getElementById('postsSk');
  const deGroup = document.getElementById('postsDe');
  const plGroup = document.getElementById('postsPl');
  if (enGroup && skGroup && deGroup && plGroup) {{
    enGroup.style.display = currentLang === 'en' ? 'block' : 'none';
    skGroup.style.display = currentLang === 'sk' ? 'block' : 'none';
    deGroup.style.display = currentLang === 'de' ? 'block' : 'none';
    plGroup.style.display = currentLang === 'pl' ? 'block' : 'none';
    return;
  }}
  const container = document.getElementById('postContainer');
  if (!container) return;
  try {{
    const res = await fetch('/blog/posts.json');
    if (!res.ok) return;
    const posts = await res.json();
    if (!Array.isArray(posts) || posts.length === 0) return;
    const d = translations[currentLang] || translations.en;

    container.innerHTML = posts.map(p => {{
      let title = p.title;
      let excerpt = p.excerpt;
      let date = p.displayDate;
      let readTime = p.readTime || '5 min read';
      let targetUrl = p.url;

      if (currentLang === 'sk') {{
        title = p.titleSk || p.title;
        excerpt = p.excerptSk || p.excerpt;
        date = p.displayDateSk || p.displayDate;
        readTime = p.readTimeSk || p.readTime;
        targetUrl = p.urlSk || p.url;
      }} else if (currentLang === 'de') {{
        title = p.titleDe || p.title;
        excerpt = p.excerptDe || p.excerpt;
        date = p.displayDateDe || p.displayDate;
        readTime = p.readTimeDe || p.readTime;
        targetUrl = p.urlDe || p.url;
      }} else if (currentLang === 'pl') {{
        title = p.titlePl || p.title;
        excerpt = p.excerptPl || p.excerpt;
        date = p.displayDatePl || p.displayDate;
        readTime = p.readTimePl || p.readTime;
        targetUrl = p.urlPl || p.url;
      }}

      const tagsHtml = (p.tags || []).map(t => `<span>${{t}}</span>`).join('');

      return `
<a href="/${{targetUrl}}" class="post-item fade-in visible" lang="${{currentLang}}">
  <div class="post-top">
    <span class="post-date">${{date}}</span>
    <span class="post-read">${{readTime}}</span>
  </div>
  <h2>${{title}}</h2>
  <p>${{excerpt}}</p>
  <div class="post-tags">${{tagsHtml}}</div>
</a>`;
    }}).join('');
  }} catch(e){{}}
}}

// Scroll / Fade-in Observer
function initScrollObserver() {{
  const elements = document.querySelectorAll('.fade-in');
  elements.forEach(el => el.classList.add('visible'));

  if ('IntersectionObserver' in window) {{
    const observer = new IntersectionObserver((entries) => {{
      entries.forEach(entry => {{
        if (entry.isIntersecting) {{
          entry.target.classList.add('visible');
        }}
      }});
    }}, {{ threshold: 0.05, rootMargin: '0px 0px 50px 0px' }});

    elements.forEach(el => observer.observe(el));

    if (document.body) {{
      const mutObs = new MutationObserver(() => {{
        document.querySelectorAll('.fade-in:not(.visible)').forEach(el => {{
          el.classList.add('visible');
          observer.observe(el);
        }});
      }});
      mutObs.observe(document.body, {{ childList: true, subtree: true }});
    }}
  }}
}}

// Initialize
if (document.readyState === 'loading') {{
  document.addEventListener('DOMContentLoaded', () => {{
    initScrollObserver();
    applyTranslations();
    if ('requestIdleCallback' in window) {{
      requestIdleCallback(loadDynamicPostsHome);
      requestIdleCallback(renderBlogIndexPosts);
    }} else {{
      setTimeout(loadDynamicPostsHome, 50);
      setTimeout(renderBlogIndexPosts, 50);
    }}
  }});
}} else {{
  initScrollObserver();
  applyTranslations();
  if ('requestIdleCallback' in window) {{
    requestIdleCallback(loadDynamicPostsHome);
    requestIdleCallback(renderBlogIndexPosts);
  }} else {{
    setTimeout(loadDynamicPostsHome, 50);
    setTimeout(renderBlogIndexPosts, 50);
  }}
}}

// Mobile nav toggle
document.querySelector('.mobile-toggle')?.addEventListener('click', function() {{
  const nav = document.querySelector('.nav-links');
  const isOpen = nav?.classList.toggle('open');
  this.setAttribute('aria-expanded', isOpen);
}});

document.addEventListener('click', function(e) {{
  const nav = document.querySelector('.nav-links');
  const toggle = document.querySelector('.mobile-toggle');
  if (nav && nav.classList.contains('open') && !nav.contains(e.target) && !toggle?.contains(e.target)) {{
    nav.classList.remove('open');
    toggle?.setAttribute('aria-expanded', 'false');
  }}
}});

// Lead form
document.getElementById('leadForm')?.addEventListener('submit', async function(e) {{
  e.preventDefault();
  const btn = document.getElementById('subscribeBtn');
  const status = document.getElementById('leadStatus');
  const email = document.getElementById('leadEmail')?.value.trim();
  if (!email) return;
  btn.disabled = true;
  btn.textContent = '...';
  status.textContent = '';
  status.className = 'lead-status';
  try {{
    const res = await fetch('/api/subscribe', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ email, source: 'marianstancik.dev' }})
    }});
    const data = await res.json();
    if (res.ok && data.status === 'ok') {{
      status.textContent = currentLang === 'sk' ? '✅ Prihlásené! Skontrolujte si schránku.' : (currentLang === 'de' ? '✅ Abonniert! Prüfen Sie Ihr Postfach.' : (currentLang === 'pl' ? '✅ Zapisano! Sprawdź skrzynkę.' : '✅ Subscribed! Check your inbox.'));
      status.className = 'lead-status lead-success';
      document.getElementById('leadEmail').value = '';
    }} else {{
      status.textContent = '❌ ' + (data.error || 'Error. Try again.');
      status.className = 'lead-status lead-error';
    }}
  }} catch (err) {{
    status.textContent = '❌ Network error.';
    status.className = 'lead-status lead-error';
  }}
  btn.disabled = false;
  btn.textContent = translations[currentLang]?.subscribeBtn || 'Subscribe';
}});
"""

with open(os.path.join(BASE_DIR, 'js', 'i18n.js'), 'w', encoding='utf-8') as f:
    f.write(js_content)
print("[+] Successfully wrote js/i18n.js")

# Fix index.html IDs
with open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

# Fix hero buttons
html = html.replace('<a href="/services" class="btn-primary hero-cta">✦ See Products</a>', '<a href="/services" class="btn-primary hero-cta" id="heroCta">✦ See Products</a>')
html = html.replace('<a href="/contact">Start a Conversation →</a>', '<a href="/contact" id="heroContact">Start a Conversation →</a>')

# Fix FAQ IDs
faq_old = """<!-- === FAQ === -->
<section id="faq" aria-label="Frequently Asked Questions">
  <div class="container">
    <div class="section-label fade-in">✦ FAQ</div>
    <h2 class="fade-in">Frequently Asked Questions</h2>

    <div class="faq-list fade-in">
      <details class="faq-item" open>
        <summary class="faq-question"><span>Who is Marian Stancik?</span><div class="faq-icon">+</div></summary>
        <div class="faq-answer">
          <strong>Marian Stancik</strong> builds autonomous AI agents for creative founders and businesses. He specializes in custom AI agent development, AI web audits (GEO and technical readiness), and multi-agent orchestration using the Hermes Agent framework. He also studies law at PF UK and builds drones as a hobby.
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question"><span>What does an AI GEO Audit check?</span><div class="faq-icon">+</div></summary>
        <div class="faq-answer">
          An AI GEO Audit checks if your website is visible to AI search engines like Perplexity, ChatGPT Search, Claude, and Google SGE. It verifies <strong>llms.txt</strong>, <strong>robots.txt</strong>, <strong>JSON-LD</strong> structured data, <strong>OpenGraph</strong> tags, <strong>hreflang</strong>, page speed, and overall AI discoverability. <strong>€199</strong> — one-time audit, report in 48 hours.
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question"><span>What is the AI Web Readiness Scan?</span><div class="faq-icon">+</div></summary>
        <div class="faq-answer">
          The AI Web Readiness Scan is a <strong>technical check by an AI agent</strong> that verifies whether your website has the required documents and structures — Privacy Policy, GDPR consent, Terms of Service, Disclaimer, AI Act disclosure, and cookie compliance. <strong>This is not legal advice</strong> — just a technical checklist. <strong>€200</strong> — one-time scan, report in 48 hours.
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question"><span>Does Marian provide legal advice?</span><div class="faq-icon">+</div></summary>
        <div class="faq-answer">
          <strong>No.</strong> Marian studies law, he is not a lawyer. He does not provide legal advice, legal services, or compliance consulting. His AI agents perform <strong>technical checks only</strong> — they verify whether documents and structures exist, not whether they are legally correct. Clients must consult a qualified lawyer for legal matters.
        </div>
      </details>
    </div>
  </div>
</section>"""

faq_new = """<!-- === FAQ === -->
<section id="faq" aria-label="Frequently Asked Questions">
  <div class="container">
    <div class="section-label fade-in" id="faqLabel">✦ FAQ</div>
    <h2 class="fade-in" id="faqHeading">Frequently Asked Questions</h2>

    <div class="faq-list fade-in">
      <details class="faq-item" open>
        <summary class="faq-question"><span id="faq1q">Who is Marian Stancik?</span><div class="faq-icon">+</div></summary>
        <div class="faq-answer" id="faq1a">
          <strong>Marian Stancik</strong> builds autonomous AI agents for creative founders and businesses. He specializes in custom AI agent development, AI web audits (GEO and technical readiness), and multi-agent orchestration using the Hermes Agent framework. His law studies inform regulatory awareness for building regulatory-ready systems. Hardware engineering is a hobby that demonstrates edge AI skills.
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question"><span id="faq2q">What does an AI GEO Audit check?</span><div class="faq-icon">+</div></summary>
        <div class="faq-answer" id="faq2a">
          An AI GEO Audit checks if your website is visible to AI search engines like Perplexity, ChatGPT Search, Claude, and Google SGE. It verifies <strong>llms.txt</strong>, <strong>robots.txt</strong>, <strong>JSON-LD</strong> structured data, <strong>OpenGraph</strong> tags, <strong>hreflang</strong>, page speed, and overall AI discoverability. <strong>€199</strong> — one-time audit, report in 48 hours.
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question"><span id="faq3q">What is the AI Web Readiness Scan?</span><div class="faq-icon">+</div></summary>
        <div class="faq-answer" id="faq3a">
          The AI Web Readiness Scan is a <strong>technical check by an AI agent</strong> that verifies whether your website has the required documents and structures — Privacy Policy, GDPR consent, Terms of Service, Disclaimer, AI Act disclosure, and cookie compliance. <strong>This is not legal advice</strong> — just a technical checklist. <strong>€200</strong> — one-time scan, report in 48 hours.
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question"><span id="faq4q">Does Marian provide legal advice?</span><div class="faq-icon">+</div></summary>
        <div class="faq-answer" id="faq4a">
          <strong>No.</strong> Marian studies law, he is not a lawyer. He does not provide legal advice, legal services, or compliance consulting. His AI agents perform <strong>technical checks only</strong> — they verify whether documents and structures exist, not whether they are legally correct. Clients must consult a qualified lawyer for legal matters.
        </div>
      </details>
    </div>
  </div>
</section>"""

if faq_old in html:
    html = html.replace(faq_old, faq_new)

html = html.replace('<span>I agree to the <a href="/privacy" style="color:#CD7F32;text-decoration:underline;">Privacy Policy</a> and consent to processing my email for newsletter updates.</span>',
                    '<span id="leadConsentText">I agree to the <a href="/privacy" style="color:#CD7F32;text-decoration:underline;">Privacy Policy</a> and consent to processing my email for newsletter updates.</span>')

with open(os.path.join(BASE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html)
print("[+] Successfully updated index.html IDs")

# Update all HTML files with cache-busted <script src="/js/i18n.js?v=20260908_v6">
CACHE_BUST_SCRIPT = '<script src="/js/i18n.js?v=20260908_v6"></script>'

for root, dirs, files in os.walk(BASE_DIR):
    if '.git' in root or '.system_generated' in root:
        continue
    for fname in files:
        if fname.endswith('.html'):
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Replace any /js/i18n.js occurrences
            new_content = re.sub(r'<script\s+src=["\']/js/i18n\.js(?:\?[^"\']*)?["\']\s*></script>', CACHE_BUST_SCRIPT, content)
            
            # On blog/index.html, ensure it includes /js/i18n.js?v=20260908_v2
            if fname == 'index.html' and 'blog' in root:
                if CACHE_BUST_SCRIPT not in new_content:
                    new_content = new_content.replace('</body>', f'{CACHE_BUST_SCRIPT}\n</body>')
                # Remove obsolete inline i18n script in blog/index.html
                new_content = re.sub(r'<script>\s*const i18n = \{[\s\S]*?<\/script>', '', new_content)
                
            if new_content != content:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"[+] Updated i18n script cache bust in: {os.path.relpath(fpath, BASE_DIR)}")

    print("\n[+] All i18n components synchronized successfully!")
