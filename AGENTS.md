# marian-stancik-web — Personal Brand Website & Autonomous Engineering Hub

**Owner:** Marian Stancik  
**Version:** `v1.0.0` (Production Release)  
**Domain:** https://marianstancik.dev (Production on Vercel)  
**Apex Domain Support:** https://marianstancik.dev & https://www.marianstancik.dev  
**Repo:** https://github.com/Abra7abra7/marian_stancik_dev_web  
**VPS:** 188.245.224.189 (Hetzner Cloud — Caddy + Python WSGI + Hermes Agent)  
**Default Branch:** `main` (Single-branch trunk-based GitOps)

---

## 1. Executive Overview & Mission

This repository represents the official personal brand website, technical knowledge graph, and autonomous agent hub for **Marian Stancik** — AI Agent Developer & Autonomous Systems Builder.

The platform is engineered at the convergence of three foundational pillars:
1. **AI Engineering & Autonomous Multi-Agent Systems:** 24/7 Hermes Agent orchestration, custom Model Context Protocol (MCP) servers, OpenRouter multi-LLM dynamic routing, and an Obsidian persistent memory layer running on dedicated European Hetzner Cloud infrastructure.
2. **Law, EU AI Act & Regulatory Governance (Legal-by-Design):** Practical compliance architectures covering the EU AI Act (risk tiering, GPAI, technical files), GDPR, NIS2 Directive, DORA, EU Data Act, and DSM Copyright Directive (TDM exemptions).
3. **Tactical UAV Systems & Edge Robotics (Hobby Project):** Hand-soldered 1500g carbon quadcopter, ArduPilot Copter autopilot, Raspberry Pi 5 onboard companion computer with real-time edge vision AI, certified EASA A1/A3 with €2.6M Coverdrone insurance.

---

## 2. IDENTITY & ANONYMIZATION RULES (CRITICAL — ZERO TOLERANCE)

> [!CAUTION]
> **Delta Defence is NEVER mentioned by name anywhere on the web, code, blog, schema, or LLM graphs.**  
> Strict security and confidentiality requirement. Only `"Defence Product Manager"` and `"Defence Industry"` are permitted.

- ✅ Hero: `"Defence Product Manager"` / `"AI Agent Developer"`
- ✅ About: `"Defence Product Manager"`
- ✅ JSON-LD: `"name": "Defence Industry (confidential)"`
- ✅ Slovak: `"Defence Product Manager"`
- ✅ `llms.txt`, `llms-full.txt`, blog articles, AUDIT.md, and all HTML files: **ZERO occurrences** of the company name.
- 🛡️ Verified automatically via **L1 Security Sweep** in `scripts/verify_site.py`.

### Name & Visual Identity Standards
- **Name Standard:** Always **Marian Stancik** (strictly without diacritics) in both English and Slovak texts, schemas, metadata, and code.
- **Social / OG Image Standard:** All pages and articles must use Marian's photo (`https://www.marianstancik.dev/profile-big.webp` or `profile.webp`) as `og:image` and `twitter:image` with `width="800" height="800"` and `alt="Marian Stancik"`.
- **Search Snippet & Favicon Standard:** Circular portrait favicon with high-contrast bronze ring border generated from `profile.webp` via `scripts/generate_favicon.py` across all standard resolutions (`favicon.ico`, `favicon-32x32.png`, `favicon-48x48.png`, `apple-touch-icon.png`).

---

## 3. Centralized Configuration & 4-Language i18n Matrix (`EN`, `SK`, `DE`, `PL`)

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

### i18n DOM Mapping Conventions
1. **Element Mapping:** Any element with `id="KEY"` or `data-i18n="KEY"` automatically receives text or HTML from the active locale dictionary.
2. **Protected Containers:** Structural layout tags (`SECTION`, `MAIN`, `NAV`, `HEADER`, `FOOTER`, `BODY`, `HTML`) without explicit `data-i18n` are protected from accidental text overwrites.
3. **Safe Visibility (`.fade-in`):** `.fade-in` elements default to `opacity: 1; transform: translateY(0);` in CSS with progressive enhancement via `initScrollObserver()` so that content is never hidden if JS is delayed.
4. **Client-Side Event Bus:** Language switching triggers a `languageChanged` custom DOM event and stores preference in `localStorage.getItem('ms_lang')`.

---

## 4. Repository Structure & File Topology

```
.
├── index.html                  # Homepage (Hero, Products, About, Dynamic Blog, FAQ, Lead Form)
├── about.html                  # About Marian Stancik + Hermes Runtime Cockpit + Evolution Timeline
├── services.html               # 4 AI Products & Audits (EN) + Stripe Checkout Modals
├── services-sk.html            # 4 AI Products & Audits (SK)
├── skills.html                 # AI & Engineering Capabilities
├── expertise.html              # Core Focus & Domain Architecture
├── drones.html                 # Tactical UAV & Edge Robotics (Hobby Project)
├── contact.html                # Contact Hub & Direct Booking Inquiry
├── privacy.html / privacy-sk   # GDPR & Data Privacy Documentation
├── terms.html / disclaimer.html # Terms of Service & EU AI Act Art. 50 Disclaimers
│
├── api/
│   └── subscribe.js            # Serverless Lead Capture -> AgentMail MCP JSON-RPC 2.0
│
├── blog/
│   ├── index.html              # Blog Archive with Instant 4-Language Switcher
│   ├── posts.json              # Synchronized Article Metadata in 4 Languages
│   └── posts/
│       ├── *.html & *.md       # Standalone English Articles + Markdown Alternates
│       ├── sk/*.html & *.md    # Standalone Slovak Articles + Markdown Alternates
│       ├── de/*.html & *.md    # Standalone German Articles + Markdown Alternates
│       └── pl/*.html & *.md    # Standalone Polish Articles + Markdown Alternates
│
├── css/
│   └── main.css                # Bronze Neural Design Tokens, Responsive Grid & Components
├── js/
│   ├── i18n.js                 # Centralized 4-Language Translation & DOM Switcher
│   └── three-bg.js             # High-Performance Vanilla Three.js Neural Web Background
│
└── scripts/
    ├── publish_post.py         # Autonomous Blog Generator (4 Languages + IndexNow + Sitemap)
    ├── sync_site.py            # Site Config Sync Engine (sitemap.xml, llms.txt, alternates)
    ├── fix_i18n_complete.py    # i18n Engine & HTML Sync Rebuild Script
    ├── verify_site.py          # 8-Tier Automated Production Verification Suite
    └── test_all_channels.py    # Live API & Channel Integration Test Script
```

---

## 5. Autonomous Blog Publishing Pipeline (`scripts/publish_post.py`)

The automated pipeline generates production-ready articles across all 4 active languages:

```mermaid
flowchart TD
    Idea[Topic & Brief] --> Engine[publish_post.py Engine]
    Engine --> EN[blog/posts/{slug}.html + .md]
    Engine --> SK[blog/posts/sk/{slug}.html + .md]
    Engine --> DE[blog/posts/de/{slug}.html + .md]
    Engine --> PL[blog/posts/pl/{slug}.html + .md]
    Engine --> Meta[Update blog/posts.json]
    Engine --> Sitemap[Rebuild sitemap.xml & llms.txt]
    Engine --> IndexNow[Ping IndexNow API: Bing / Yandex / Seznam]
```

### CLI Usage:
```bash
# Publish a new article in all 4 languages simultaneously:
python scripts/publish_post.py "Article Title" --category "AI Agents" --tags "Agents,MCP,Automation"
```

---

## 6. Design System & Tokens (`css/main.css`)

All visual interfaces adhere strictly to the design system tokens defined in [`css/main.css`](file:///css/main.css):

### Color Tokens (Bronze Neural Theme)
```css
:root {
  --color-bg: #08080F;              /* Deep dark canvas */
  --color-bg-secondary: #0D0D18;    /* Elevated surface */
  --color-bg-card: rgba(18, 18, 30, 0.65); /* Glassmorphic card */
  --color-bg-card-hover: rgba(26, 26, 42, 0.85);
  --color-primary: #CD7F32;         /* Metallic Bronze */
  --color-accent: #E8B86D;          /* Warm Gold / Amber Accent */
  --color-glow: rgba(205, 127, 50, 0.2); /* Ambient glow */
  --color-border: rgba(255, 255, 255, 0.06);
  --color-border-hover: rgba(205, 127, 50, 0.35);
  --color-text: #F0F0F5;            /* High contrast text */
  --color-text-muted: #8888A0;      /* Secondary reading text */
}
```

### Spacing & Accessibility Tokens
- Spacing: `--space-xs: 4px;` | `--space-sm: 8px;` | `--space-md: 16px;` | `--space-lg: 24px;` | `--space-xl: 48px;` | `--space-2xl: 90px;`
- Radius: `--radius-sm: 6px;` | `--radius-md: 12px;` | `--radius-lg: 18px;` | `--radius-full: 9999px;`
- Accessibility: `--min-tap-target: 44px;` for all mobile buttons and interactive anchors.

---

## 7. Generative Engine Optimization (GEO) & LLMO Blueprint

To guarantee instant, authoritative discovery and citations across AI engines (**Perplexity, ChatGPT Search, Claude, Google SGE, Grok**):

1. **`llms.txt` & `llms-full.txt` (llmstxt.org v2 Standard):** Clean Markdown links with summaries of all articles, products, and pages.
2. **Dual-Language Markdown Alternates (`.md` Endpoints):** Every HTML page and blog post provides a clean markdown version (`*.md`) advertised via HTTP Link headers.
3. **AI Crawler White-Listing (`robots.txt`):** Explicitly grants access to GPTBot, ChatGPT-User, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended, CCBot, Bravebot, Meta-ExternalAgent, Cohere-ai, Diffbot, and OAI-SearchBot.
4. **Schema.org JSON-LD Hierarchy:** Rich `@graph` containing `Person`, `Organization`, `WebSite`, `Service`, `Offer`, and `FAQPage` schemas with precise pricing (€199, €200, €300, €500).

---

## 8. Backend Architecture & Security (`/api/subscribe`)

The serverless API is deployed on Vercel and connects directly to **AgentMail MCP** for asynchronous processing:

```mermaid
flowchart LR
    Visitor[Client Web Form] -->|POST /api/subscribe| VercelAPI[Vercel Serverless Function]
    VercelAPI -->|Honeypot & Rate Check| SecurityGuard[Spam & Origin Filter]
    SecurityGuard -->|JSON-RPC 2.0 MCP| AgentMail[mcp.agentmail.to MCP Session]
    AgentMail -->|User Confirmation| CustomerEmail[Customer Inbox]
    AgentMail -->|Urgent Admin Alert| MarianInbox[marianstancik@agentmail.to]
```

- **Dynamic CORS:** Supports `https://www.marianstancik.dev`, `https://marianstancik.dev`, and preview endpoints.
- **Honeypot Protection:** Silently drops automated spam bots without consuming AgentMail API quota.
- **Payload Routing:**
  1. `product_order` / `stripe_checkout_intent` ➔ Sends detailed order recap + admin notification.
  2. `contact_form` ➔ Sends receipt confirmation + instant admin alert.
  3. `newsletter` ➔ Sends welcome guide + subscriber notification.

---

## 9. Automated Verification Suite (`scripts/verify_site.py`)

Run the 8-tier verification script before any deployment:
```bash
python scripts/verify_site.py
```

### Test Tiers
1. **L0 — JS Syntax Check:** `node --check js/i18n.js` and `node --check js/three-bg.js`.
2. **L1 — Security & Anonymization Sweep:** Regex scan ensuring zero confidential company names.
3. **L2 — HTML Meta & Link Integrity:** Validates root-relative links, OpenGraph tags, and JSON-LD syntax across all pages.
4. **L3 — Design Tokens & CSS Validation:** Checks `:root` token presence in `css/main.css`.
5. **L4 — AI Discovery & GEO:** Validates `<link rel="alternate" href="/llms.txt">` and AI crawler permissions in `robots.txt`.
6. **L5 — API Health Check:** Validates live HTTP 200 response from `/api/subscribe`.
7. **L6 — Config, Locales & Markdown Integrity:** Validates `site.config.json`, all 4 `locales/*.json` files, and guarantees zero missing `.md` blog alternates.
8. **L7 — 4-Language Parity Check:** Verifies 100% dictionary key parity across `en.json`, `sk.json`, `de.json`, and `pl.json`.

---

## 10. GitOps & Release Procedures

- **Branching Model:** Trunk-based GitOps on `main`.
- **Production Tag:** `v1.0.0`
- **Deployment Trigger:** Every push to `main` triggers automatic Vercel build & edge deployment.