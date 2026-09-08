# marian-stancik-web — Personal Brand Website & Autonomous Engineering Hub

**Owner:** Marian Stancik  
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

## 3. Centralized Configuration Engine (`site.config.json` & `locales/`)

All site metadata, product definitions, Stripe pricing, social handles, and multilingual dictionaries are managed centrally from a **Single Source of Truth**:

- **Central Config:** [`site.config.json`](file:///site.config.json)
  - `site`: Base domain, contact email, default language, active language matrix (`en`, `sk`, `de`, `pl`).
  - `profile`: Identity, localized roles, taglines, social channels, and geographic coordinates.
  - `products`: 4 core products (AI GEO Audit €150, Web Readiness Scan €200, Full Web Audit €300, Custom Autonomous Agent €500 deposit) with Stripe test and live links.
- **Modular Locales:** [`locales/`](file:///locales/)
  - `locales/en.json` (English — primary international)
  - `locales/sk.json` (Slovak — native domestic)
  - `locales/de.json` (German — DACH market)
  - `locales/pl.json` (Polish — CEE market)
- **Synchronization Engine:** [`scripts/sync_site.py`](file:///scripts/sync_site.py) reads the configuration, syncs markdown alternates, rebuilds `llms.txt`, `llms-full.txt`, and generates `sitemap.xml`.

---

## 4. Site Architecture & Page Topology

**Navigation:** Home | About | Products | Blog | Contact.  
(Drones marked as hobby engineering project. Expertise and Skills accessible via footer/About).

| Page | URL | Purpose & Core Content |
|:-----|:----|:-----------------------|
| **Home** | `/` (`index.html`) | Hero: "I build AI agents that run your processes" + 4 products + dynamic blog preview + lead capture |
| **About** | `/about` (`about.html`) | Bio: AI agent developer + Hermes Autonomous Agent Runtime Cockpit widget + 4-layer stack timeline |
| **Products** | `/services` (`services.html`) | 4 products with instant Stripe checkout & Schema.org `Service`/`Offer` JSON-LD |
| **Products SK** | `/services-sk` (`services-sk.html`) | Slovak localized products page with Stripe checkout modal & direct invoice ordering |
| **Blog** | `/blog` (`blog/index.html`) | Static blog archive + dynamic JSON client fetching + real-time language switcher |
| **Blog Posts (EN)** | `/blog/posts/*.html` | 6 standalone technical articles + synchronized `.md` markdown alternates |
| **Blog Posts (SK)** | `/blog/posts/sk/*.html` | 6 synchronized Slovak translations + bidirectional hreflang links + `.md` alternates |
| **Drones** | `/drones` (`drones.html`) | Hobby project — build specs + hobby disclaimer. Not a commercial product. |
| **Contact** | `/contact` (`contact.html`) | Lead capture + social links + order inquiry handoff |
| **Privacy / Terms** | `/privacy`, `/terms`, `/disclaimer` | GDPR, Terms of Service, and compliance documentation |

---

## 5. Design System & Tokens (`css/main.css`)

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

### Spacing & Layout Tokens
- Spacing: `--space-xs: 4px;` | `--space-sm: 8px;` | `--space-md: 16px;` | `--space-lg: 24px;` | `--space-xl: 48px;` | `--space-2xl: 90px;`
- Radius: `--radius-sm: 6px;` | `--radius-md: 12px;` | `--radius-lg: 18px;` | `--radius-full: 9999px;`
- Accessibility: `--min-tap-target: 44px;` for all mobile buttons and interactive anchors.

---

## 6. Generative Engine Optimization (GEO) & LLMO Blueprint

To guarantee instant, authoritative discovery and citations across AI engines (**Perplexity, ChatGPT Search, Claude, Google SGE, Grok**):

### 1. `llms.txt` & `llms-full.txt` Knowledge Graphs (llmstxt.org v2 Standard)
* Root files strictly following the [llmstxt.org](https://llmstxt.org/) specification.
* Every single resource is a valid Markdown link: `- [Title](https://domain/path): Description`.
* Contains all 6 technical articles, core pages, and detailed product/service descriptions.

### 2. Dual-Language Markdown Alternates (`.md` Endpoints)
* Every HTML page and blog post provides a clean markdown version (`index.html.md`, `blog/posts/*.md`, `blog/posts/sk/*.md`).
* Advertised via HTTP Link header: `Link: </blog/posts/$1.md>; rel="alternate"; type="text/markdown"` and `Link: </llms.txt>; rel="describedby"`.

### 3. Comprehensive AI Crawler Access in `robots.txt`
* Explicitly white-lists all production and experimental AI search spiders (GPTBot, ChatGPT-User, ClaudeBot, anthropic-ai, PerplexityBot, Google-Extended, Applebot-Extended, CCBot, Bravebot, Meta-ExternalAgent, Cohere-ai, Diffbot, OAI-SearchBot).

### 4. Schema.org JSON-LD Hierarchy
* **`Person` & `Organization` Schemas:** Rich `sameAs` array, `knowsAbout`, `jobTitle`, `image`.
* **`Service` & `Offer` Schemas:** Embedded on `/services` and `/services-sk` with precise EUR pricing (€150, €200, €300, €500).
* **`FAQPage` Schema:** Structured Question/Answer pairs embedded directly on key pages.

---

## 7. Backend Architecture & Security (`/api/subscribe`)

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

## 8. Automated Verification Matrix

Run the 7-tier verification script before any deployment:
```bash
python scripts/verify_site.py
```

### Test Tiers
1. **L0 — Syntax & Modules:** `node --check js/i18n.js` and `node --check js/three-bg.js`.
2. **L1 — Security & Anonymization Sweep:** Regex scan ensuring zero confidential company names.
3. **L2 — HTML & Link Integrity:** Validates root-relative links, OpenGraph tags, and JSON-LD syntax across all pages.
4. **L3 — Design Token Adherence:** Checks `:root` token presence in `css/main.css`.
5. **L4 — AI Discovery & GEO:** Validates `<link rel="alternate" href="/llms.txt">` and AI crawler permissions in `robots.txt`.
6. **L5 — API Health Check:** Validates live HTTP 200 response from `/api/subscribe`.
7. **L6 — Config, Locales & Markdown Integrity:** Validates `site.config.json`, all 4 `locales/*.json` files, and guarantees zero missing `.md` blog alternates.

### Live Channel Integration Test
To run a live test of all email channels, lead capture, and Stripe payment links:
```bash
python scripts/test_all_channels.py
```