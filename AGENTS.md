# marian-stancik-web — Personal Brand Website & Autonomous Engineering Hub

**Owner:** Marian Stancik  
**Version:** `v1.2.0` (Production Release — Cloudflare Edge, Hetzner VPS & Sovereign CRM)  
**Domain:** https://marianstancik.dev (Production on Cloudflare Pages)  
**Apex & WWW Support:** https://marianstancik.dev & https://www.marianstancik.dev  
**Cloudflare Pages Project:** `marian-stancik` (`marian-stancik.pages.dev`)  
**Repo:** https://github.com/Abra7abra7/marian_stancik_dev_web  
**Backend VPS:** `188.245.224.189` (Hetzner Cloud — Caddy + Python WSGI + Hermes Agent + Umami)  
**Default Branch:** `main` (Single-branch trunk-based GitOps)

---

## 1. Executive Overview & Mission

This repository represents the official personal brand website, technical knowledge graph, showcase reference architecture, and autonomous agent hub for **Marian Stancik** — AI Agent Developer & Autonomous Systems Builder.

The platform serves both as Marian's personal brand and as a **live production showcase for clients**, demonstrating how modern web engineering, autonomous AI agents, regulatory compliance (Legal-by-Design), and sovereign infrastructure integrate seamlessly without costly SaaS overhead.

The platform operates across three foundational pillars:
1. **AI Engineering & Autonomous Multi-Agent Systems:** 24/7 Hermes Agent orchestration, custom Model Context Protocol (MCP) servers (Google Drive, PostHog, OpenSEO, AgentMail), OpenRouter multi-LLM dynamic routing, and an Obsidian persistent memory layer running on dedicated European Hetzner Cloud infrastructure.
2. **Law, EU AI Act & Regulatory Governance (Legal-by-Design):** Practical compliance architectures covering the EU AI Act (risk tiering, GPAI, technical files, Art. 50 disclosure), GDPR (Art. 7(3) opt-out), NIS2 Directive, DORA, EU Data Act, and statutory consumer protection (Act No. 108/2024 Coll. & Act No. 452/2021 Coll.).
3. **Tactical UAV Systems & Edge Robotics (Hobby Project):** Hand-soldered carbon quadcopter, ArduPilot Copter autopilot, Raspberry Pi 5 onboard companion computer with real-time edge vision AI, certified EASA A1/A3 with €2.6M Coverdrone insurance.

---

## 2. Brand Identity & Quality Standards

### Name & Visual Identity
- **Name Standard:** Always **Marian Stancik** (strictly without diacritics in code, filenames, schemas, and English/Slovak metadata).
- **Professional Title:** **AI Agent Developer & Autonomous Systems Builder** (studying law, building sovereign multi-agent architectures).
- **Social / OG Image Standard:** All pages and articles use Marian's photo (`https://www.marianstancik.dev/profile-big.webp` or `profile.webp`) as `og:image` and `twitter:image` with `width="800" height="800"` and `alt="Marian Stancik"`.
- **Search Snippet & Favicon Standard:** Circular portrait favicon with high-contrast bronze ring border generated from `profile.webp` across standard resolutions (`favicon.ico`, `favicon-32x32.png`, `favicon-48x48.png`, `apple-touch-icon.png`).
- **Design Tokens:** Bronze Neural palette (`#CD7F32` bronze accent, `#08080F` deep dark background, `#E8E8F0` text, glassmorphism cards).

---

## 3. Infrastructure & Hosting Architecture (Cloudflare + Hetzner Hybrid)

```mermaid
flowchart TD
    subgraph Global Edge ["Cloudflare Global Network (Anycast CDN & Edge Compute)"]
        DNS[Cloudflare DNS: marianstancik.dev] --> WAF[Cloudflare DDoS / WAF Guard]
        WAF --> EdgeMiddleware["Edge Middleware (_middleware.js)"]
        EdgeMiddleware -->|Accept: text/markdown| MDDirect["Serve *.md endpoints"]
        EdgeMiddleware -->|Accept: text/html| PagesStatic["Cloudflare Pages Static Assets (sub-15ms TTFB)"]
        EdgeMiddleware -->|/api/*| EdgeFunctions["Cloudflare Pages Functions (/functions/api)"]
    end

    subgraph European VPS ["Dedicated Hetzner Cloud VPS (188.245.224.189 - Germany)"]
        Caddy[Caddy 2 Reverse Proxy + Automatic SSL]
        HermesAgent["Hermes Agent Autonomous Runtime (24/7)"]
        HermesCRM["Hermes CRM Dispatcher (/crm/)"]
        Umami["Umami Cookieless Analytics (api.marianstancik.dev)"]
        SQLiteStore[("SQLite Persistent State")]
    end

    subgraph Sovereign Cloud & APIs ["Sovereign Integrations & MCP Services"]
        GoogleDrive["Google Drive & Sheets CRM (hermes-gdrive MCP)"]
        PostHogEU["PostHog Analytics (Frankfurt EU - posthog-mcp)"]
        AgentMail["AgentMail MCP (mcp.agentmail.to)"]
        StripeAPI["Stripe Billing & Checkout"]
        OpenRouter["OpenRouter Multi-LLM Routing"]
        IndexNow["IndexNow API (Bing, Yandex, Seznam)"]
    end

    EdgeFunctions -->|JSON-RPC 2.0| AgentMail
    EdgeFunctions -->|Webhook + X-CRM-Key| HermesCRM
    HermesCRM --> SQLiteStore
    HermesCRM --> GoogleDrive
    PagesStatic -->|Checkout Session| StripeAPI
    PagesStatic -->|Beacon| Umami
    PagesStatic -->|Autocapture & Session Replay| PostHogEU
    HermesAgent -->|LLM Inference| OpenRouter
```

### Hosting Environments & Active Endpoints
1. **Frontend & Edge Hosting (Cloudflare Pages):**
   * **Project Name:** `marian-stancik` (`marian-stancik.pages.dev`).
   * **Custom Domains:** `marianstancik.dev` (Apex) and `www.marianstancik.dev` (CNAME), with full Google Trust Services SSL encryption.
   * **Sub-15ms TTFB:** Vienna (`VIE`) and Frankfurt (`FRA`) edge datacenters with 0ms Total Blocking Time (TBT).
   * **Security Headers:** Strict CSP, HSTS preload, Permissions-Policy, Cache-Control via `_headers`.
   * **Redirects:** Managed via `_redirects` (`/subscribe -> /#leadForm`).
2. **Serverless Edge Functions (Cloudflare Pages Functions):**
   * Located in `functions/api/`:
     * `functions/api/subscribe.js`: Lead capture, honeypot protection, customer confirmation dispatch, admin alert, CRM webhook sync.
     * `functions/api/crm-email.js`: Direct CRM email webhook dispatcher with `x-crm-key` token guard.
     * `functions/api/invoice/[id].js`: Secure HTTPS proxy to backend VPS with `noindex, no-store` headers.
     * `functions/api/email-templates.js`: Branded HTML email templates with GDPR Art. 7(3) and § 116 Act No. 452/2021 Coll. unsubscribe link.
   * Located in `functions/_middleware.js`:
     * Intercepts `Accept: text/markdown` from AI crawlers and routes directly to clean `.md` alternates.
3. **Backend VPS (Hetzner Cloud — Germany):**
   * **IP Address:** `188.245.224.189` (`api.marianstancik.dev`).
   * **Caddy 2 Reverse Proxy:** Reverse proxies internal services, handles SSL termination via Let's Encrypt / ZeroSSL.
   * **Hermes Agent Runtime:** Background autonomous loops handling content publishing, social syndication, sentinel monitoring, and CRM sync.
   * **Hermes CRM Dispatcher:** Receives webhooks at `https://api.marianstancik.dev/crm/`, syncs leads to SQLite and Google Sheets.
   * **Umami Analytics:** Self-hosted cookieless European instance at `https://api.marianstancik.dev/script.js` (Website ID: `ec1c0df8-e51f-4236-9ad0-e3992f0b1637`).

---

## 4. Comprehensive Services & External Integrations Matrix

| Service / Tool | Role / Purpose | Protocol / Auth | Hosting / Region | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Cloudflare Pages** | Static asset delivery, Edge CDN, caching | HTTPS / Edge Cache | Global Anycast (VIE/FRA) | ✅ Active (Production) |
| **Cloudflare Functions** | Serverless API backend (`/api/subscribe`, `/api/crm-email`) | Edge V8 Workers | Global Anycast | ✅ Active |
| **Hetzner Cloud VPS** | 24/7 Hermes runtime, CRM service, Umami analytics | HTTPS / SSH / Caddy | Germany (Nuremberg) | ✅ Active |
| **Google Drive & Sheets CRM** | Double-entry sovereign CRM for leads & client folders | Google Service Account / Sheets API v4 | Sovereign Google Drive | ✅ Active (`hermes-gdrive` MCP) |
| **PostHog Analytics** | Session replays, heatmaps, autocapture & funnel metrics | JavaScript SDK + REST API | Germany (Frankfurt EU Cloud) | ✅ Active (`posthog-mcp`) |
| **AgentMail MCP** | Transactional & notification email sending without SMTP | JSON-RPC 2.0 (`mcp.agentmail.to`) | Cloud API (`x-api-key`) | ✅ Active |
| **Stripe** | Payment processing for 4 audits & 3 subscriptions | Stripe Checkout Links | Global / EU compliant | ✅ Active |
| **OpenRouter** | Multi-LLM dynamic routing (DeepSeek, Claude 3.5, GPT-4o) | REST API (`Bearer ${key}`) | US/EU multi-provider | ✅ Active |
| **Umami Analytics** | Cookieless GDPR-compliant traffic analytics | Lightweight JS Beacon | Hetzner VPS (`api.marianstancik.dev`) | ✅ Active |
| **OpenSEO MCP** | Automated SEO audits, keyword research, gap analysis | MCP JSON-RPC (`app.openseo.so`) | Cloud MCP Server | ✅ Active |
| **IndexNow** | Instant search index pinging (Bing, Yandex, Seznam) | REST HTTP POST | Search engine endpoints | ✅ Active |

### Obsolete / Removed Services (Archived)
- ❌ **Vercel:** Fully decommissioned. The entire site and DNS are hosted on Cloudflare Pages and Hetzner VPS.
- ❌ **Subdomains `app.marianstancik.dev` & `hpi.marianstancik.dev`:** Removed from Cloudflare DNS.
- ❌ **Google Cloud project `pc-work-gemini-cli`:** Deleted in Google Cloud Console; active project is `hermes-agent-desktop-pc-work`.
- ❌ **Delta Defence / Defence Product Manager:** Removed. All personal and professional branding is focused on AI Agent Development, Legal-by-Design, and UAV Robotics.

---

## 5. What the Website Does & Core Features

1. **Autonomous Personal Brand & Client Reference Showroom:** Demonstrates a production-grade, sovereign stack operating without bloated monthly subscriptions.
2. **Product Catalog & Instant Stripe Checkout:**
   * **4 One-Time Audits & Builds:**
     * *AI GEO Audit* (€199): 48h evaluation of AI search visibility (llms.txt, JSON-LD, robots.txt, Perplexity/ChatGPT presence).
     * *AI Web Readiness Scan* (€200): Technical compliance check covering GDPR Privacy Policy, consent, Terms, AI Act disclosures.
     * *Full Web Audit* (€300): Combined GEO + Readiness scan with 30-min strategy call.
     * *Custom Autonomous AI Agent* (From €500 deposit): Custom 24/7 autonomous agent system on dedicated VPS with MCP tooling.
   * **3 Monthly Recurring Subscriptions:**
     * *GEO Monitoring Weekly* (€49/mo): Automated weekly scans & alert reports.
     * *Sentinel Agent 24/7* (€99/mo): Continuous uptime, security & crawler monitor.
     * *Autonomous Ops Retainer* (€249/mo): Managed agent operations & custom tool extensions.
3. **Autonomous Multilingual Technical Blog:**
   * 19 in-depth technical essays on production agent infrastructure, enterprise AgenticOps, MCP, and AI governance.
   * Multi-language parity: 76 synchronized articles (all 19 available in `EN`, `SK`, `DE`, `PL` both as `.html` and `.md`).
   * Interactive inline newsletter subscription card right inside each post with instant AJAX feedback.
4. **Lead Capture & Customer Onboarding:**
   * High-conversion homepage form + in-article forms submitting to `/api/subscribe`.
   * Automated double-send: instant branded HTML confirmation to client + instant alert to Marian.
   * Real-time sync into Google Sheets CRM (`1mcVQxHMu1SavnoJussw9KCpleT-qhFs8FJMe4F8h5PM`) and Hetzner SQLite.

---

## 6. Centralized Configuration & 4-Language i18n Matrix (`EN`, `SK`, `DE`, `PL`)

All site metadata, product definitions, Stripe pricing, social handles, and multilingual dictionaries are managed centrally:

```
├── site.config.json            # Central Single Source of Truth
├── locales/
│   ├── en.json                 # English (Primary International)
│   ├── sk.json                 # Slovak (Native Domestic)
│   ├── de.json                 # German (DACH Market)
│   └── pl.json                 # Polish (CEE Market)
└── js/i18n.js                  # Zero-build High-Performance i18n Client Engine
```

### i18n Routing & DOM Conventions
1. **Dynamic DOM Translation:** Any element with `id="KEY"` or `data-i18n="KEY"` automatically receives translated text or HTML from `locales/*.json` via `js/i18n.js`.
2. **Intelligent URL Subpage Router:**
   * When on `/services` and clicking `SK` → automatically navigates to `/services-sk`.
   * When on `/services-sk` and clicking `EN`, `DE`, or `PL` → automatically navigates to `/services`.
   * Similarly for paired legal subpages: `/privacy` <-> `/privacy-sk`, `/terms` <-> `/terms-sk`, `/disclaimer` <-> `/disclaimer-sk`.
   * In blog articles: clicking language buttons routes cleanly between `/blog/posts/{slug}`, `/blog/posts/sk/{slug}`, `/blog/posts/de/{slug}`, and `/blog/posts/pl/{slug}`.
3. **Dynamic Navigation Link Rewriting:**
   * When `currentLang === 'sk'`, navigation links (`#navProducts`, `#navServices`, `.home-prod-card`) dynamically point to `/services-sk`.
   * When `currentLang !== 'sk'`, they point to `/services`.
4. **Client-Side Event Bus:** Language switching triggers a `languageChanged` custom DOM event and stores preference in `localStorage.getItem('ms_lang')`.

---

## 7. Generative Engine Optimization (GEO) & AI Discovery (LLMO)

To guarantee instant, authoritative discovery and citations across AI engines (**Perplexity, ChatGPT Search, Claude, Google SGE, Grok**) as well as standard search engines:

1. **100/100 Core Web Vitals:** Mobile & Desktop performance (sub-15ms TTFB, LCP < 400ms, CLS = 0). Zero render-blocking resources, externalized minified CSS/JS, and asynchronous Three.js canvas.
2. **`llms.txt` & `llms-full.txt` (llmstxt.org v2 Standard):** Clean Markdown links with summaries of all articles, products, and pages.
3. **4-Language Markdown Alternates & Content Negotiation:** Every HTML page and blog post provides a clean markdown version (`*.md`). `functions/_middleware.js` intercepts requests with `Accept: text/markdown` and transparently routes AI agents directly to `.md` endpoints (`Vary: Accept`).
4. **AI Crawler White-Listing & Content-Signals (`robots.txt`):** Explicitly grants access to GPTBot, ChatGPT-User, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended, CCBot, Bravebot, Meta-ExternalAgent, Cohere-ai, Diffbot, and OAI-SearchBot while defining modern content licensing signals:
   ```text
   Content-Signal: ai-train=no, search=yes, ai-input=yes
   ```
5. **Schema.org JSON-LD Hierarchy:** Rich `@graph` containing `Person`, `Organization`, `WebSite`, `Service`, `Offer`, and `FAQPage` schemas with precise pricing (€199, €200, €300, €500).

---

## 8. Lead Capture, Newsletter Lifecycle & Legal Compliance

```mermaid
flowchart LR
    Visitor[Client Web Form] -->|POST /api/subscribe| EdgeFunction[Cloudflare Pages Function]
    EdgeFunction -->|Honeypot Check| SpamDrop[Silently drop bots]
    EdgeFunction -->|JSON-RPC 2.0| AgentMail[mcp.agentmail.to]
    AgentMail -->|Branded HTML + Unsubscribe| CustomerInbox[Customer Inbox]
    AgentMail -->|Instant Alert| MarianInbox[marianstancik@agentmail.to]
    EdgeFunction -->|POST /crm/ Webhook| HetznerCRM[api.marianstancik.dev]
    HetznerCRM -->|Storage| Sheets[(Google Sheets CRM)]
    EdgeFunction -.->|Failover Alert| DownAlert["[CRM DOWN] Alert Email"]
```

### Statutory Compliance & Consumer Protection
1. **Statutory Digital Content Waiver (§ 19 Act No. 108/2024 Coll.):**
   * Before redirecting to Stripe, clients purchasing digital audits must confirm:
     > *"I explicitly consent to the commencement of digital service provision before the expiry of the statutory 14-day withdrawal period, and I acknowledge that by granting this consent, I lose the right of withdrawal under § 19 of Act No. 108/2024 Coll. once the service is fully provided."*
2. **Statutory Unsubscribe & Consent Withdrawal (GDPR Art. 7(3) & § 116 Act No. 452/2021 Coll.):**
   * Every outgoing email generated by `functions/api/email-templates.js` contains full sender identification (Marián Stančík, IČO: 57068917, DIČ: 1082585075), Art. 50 AI disclosure, and a direct, free, one-click opt-out link:
     > *"Tento e-mail ste dostali na základe udeleného súhlasu na marianstancik.dev. Odber môžete kedykoľvek bezplatne zrušiť: [Odhlásiť sa z odberu](mailto:marianstancik@agentmail.to?subject=Unsubscribe%20Newsletter)."*
3. **Cookieless EU Privacy Architecture:**
   * 100% cookieless analytics via self-hosted Umami on European infrastructure (`api.marianstancik.dev`).
   * Zero third-party cookies, no tracking pixels, fully compliant with GDPR Art. 6(1)(f) and the ePrivacy Directive without intrusive cookie consent banners.

---

## 9. Automated Verification Suite (`scripts/verify_site.py`)

Run the 9-tier verification script before any deployment:
```bash
python scripts/verify_site.py
```

### Test Tiers
1. **Tier 1 — Security & Quality Sweep:** Scan ensuring clean metadata and zero unauthorized secrets.
2. **Tier 2 — JS Syntax Check (L0):** `node --check js/i18n.js` and `node --check js/three-bg.js`.
3. **Tier 3 — HTML Meta & Link Integrity:** Validates root-relative links, OpenGraph tags, and JSON-LD syntax across all pages.
4. **Tier 4 — Design Tokens & CSS Validation:** Checks `:root` token presence in `css/main.css`.
5. **Tier 5 — AI Discovery & GEO:** Validates `<link rel="alternate" href="/llms.txt">` and AI crawler permissions in `robots.txt`.
6. **Tier 6 — API Health Check (L8):** Validates live HTTP 200 response from `/api/subscribe`.
7. **Tier 7 — Config, Locales & Markdown Integrity:** Validates `site.config.json`, all 4 `locales/*.json` files, and guarantees 76/76 `.html` and `.md` blog alternates.
8. **Tier 8 — 4-Language Parity Check:** Verifies 100% dictionary key parity across `en.json`, `sk.json`, `de.json`, and `pl.json`.
9. **Tier 9 — Deploy Safety Check:** Verifies no unwanted output directories before deploying.

---

## 10. GitOps & Release Procedures

- **Branching Model:** Trunk-based GitOps on `main`.
- **Production Tag:** `v1.2.0`
- **Git Push Trigger:** Every push to GitHub `main` synchronizes trunk-based changes and keeps remote repository in lockstep with Cloudflare Pages edge.