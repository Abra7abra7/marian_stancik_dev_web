# AGENTS.md — marianstancik.dev (Single Source of Truth)

Instructions for **every AI & coding agent** (Antigravity, Hermes Agent, OpenBot, Claude, Codex, Jules, OpenCode, …).  
This file + `.agents/product-marketing.md` form the **ONE SINGLE SOURCE OF TRUTH** for who Marian is, what the website does, how it is built, and how the blog and deployments work.

---

## 1. Who I Am, What I Do & Brand Voice (Read First)

Full brand voice & positioning live in [`.agents/product-marketing.md`](.agents/product-marketing.md). Summary:

- **Owner & Operator:** Marián Stančík (brand name in code/metadata without diacritics: **Marian Stancik**), sole trader (živnostník), Brezno, Slovakia (`IČO: 57068917`, `DIČ: 1082585075`, non-VAT payer, ŽR: `630-22847`).
- **What I am:** Builder and manager of practical AI agents using open-source frameworks — primarily **Hermes Agent** and **OpenBot** (open-source alternative to Grok bot). Goal: make life and work easier, win back time, delegate routine tasks, orchestrate workflows, and **measure real results**.
- **Critical view of AI (Key Proof Point):** AI is just a tool, not magic. Real monthly benchmark: **4 billion tokens consumed for ~$200 USD** via DeepSeek on OpenRouter, vs. **~$15,000 USD** on top frontier models.
- **Who I help:** Both **businesses** (founders, managers, SEO/growth leads) and **individuals** who want practical help without hype.
- **What I am NOT (Mandatory Legal & Brand Boundaries):**
  - **NOT a lawyer:** 3rd-year law student (PF UK, Bratislava) interested in privacy (GDPR) and EU AI Act. By law (Act No. 586/2003 Coll.) **does NOT provide legal advice**. All legal/regulatory notes are strictly subjective.
  - **NOT an AI guru:** Zero overnight-miracle claims, zero corporate/IT jargon.
  - **NOT selling products right now:** No Stripe checkout, no fixed-price audit shop on the site. Focus is on clarity, free tools, readers/visits, and direct contact.
- **Automation transparency (EU AI Act Art. 50):** This entire website and the agent email (`marianstancik@agentmail.to`) are operated by AI agents with Marián's human-in-the-loop editorial responsibility.
- **Communication style:**
  - **Slovak (`/sk/`):** **Tykanie**, plain everyday Slovak, short sentences, zero jargon.
  - **English (`/en/`):** Plain, direct, honest English, zero corporate fluff.
- **Official Contact Channels:**
  - **WhatsApp (primary, personal):** `+421 940 377 855` (`https://wa.me/421940377855`)
  - **Agent-managed Email:** `marianstancik@agentmail.to`
  - **Calendar:** `https://calendar.app.google/hu1vx3nqLgK65u5C7` (20-min call)
  - **Socials:** LinkedIn, GitHub (`Abra7abra7`), X (`@marian_s_ai`), YouTube (`@marian_ai`)

---

## 2. Hosting, Deployment & Backend Architecture

- **Production Domain:** `https://www.marianstancik.dev` (apex `https://marianstancik.dev` supported)
- **Hosting:** **Cloudflare Pages** project `marian-stancik` (`marian-stancik.pages.dev`), directly connected to GitHub repo `Abra7abra7/marian_stancik_dev_web` (`main` branch).
  - **Zero Cloudflare build step:** Static generated pages (`en/`, `sk/`, `cs/`, `de/`, `pl/`) are committed directly to git and served from Cloudflare's global edge CDN.
  - Every PR branch gets an automatic Cloudflare Pages preview URL.
- **Edge Functions (`functions/`):**
  - `functions/_middleware.js` — Content negotiation (`Accept: text/markdown` serves clean `.md` twins for AI agents).
  - `functions/api/subscribe.js` + `functions/api/confirm.js` — Strict **GDPR double opt-in** newsletter & Starter Kit delivery via **Gmail API (Google Workspace)** (`functions/api/_gmail.js`), with honeypot + optional Cloudflare Turnstile (`TURNSTILE_SECRET_KEY`).
  - Required Cloudflare Pages Environment Variables (names only — never commit values): `GMAIL_REFRESH_TOKEN` (or `GMAIL_SERVICE_ACCOUNT_JSON`), `OPTIN_SECRET`, `ADMIN_EMAIL` (optional, defaults to `GMAIL_USER`), `TURNSTILE_SECRET_KEY` (optional).
- **Decommissioned / Offline Services:**
  - Legacy Hetzner CRM webhook & Umami analytics (`api.marianstancik.dev`) were removed/taken offline; lead notifications go via Gmail API.
  - Vercel, `app.marianstancik.dev`, `hpi.marianstancik.dev`, and Stripe product pages are decommissioned.

---

## 3. Repository Structure & Single Sources of Truth

```
.agents/product-marketing.md     # SINGLE SOURCE OF TRUTH for brand voice, positioning & proof points
AGENTS.md                        # SINGLE SOURCE OF TRUTH for agent rules, architecture & workflows
css/main.css                     # Readable design system source (Midnight Navy #0A111C + Bronze Gold #CD7F32 / #EBC37D)
css/main.min.css                 # GENERATED minified CSS served in production (via node scripts/minify_js.mjs)
js/three-bg.js (+ .min.js)       # Zero-CDN 2D <canvas> ambient background (mobile-disabled, pauses on hidden tab)
_headers                         # Cloudflare Pages security headers + 30-day image cache + 1-year CSS/JS immutable cache
index.html                       # EN source template for homepage (root / 302 -> /en/)
how-it-works.html, how-it-works-sk.html
tools/index.html, tools/prompt-library*.html, tools/starter-kit*.html, tools/mission-planner.html
contact.html                     # Unified direct contact (WhatsApp + agent email + calendar)
blog/index.html                  # Blog index template (unified 5-link nav)
blog/writer-rules.md             # SINGLE SOURCE OF TRUTH for automated blog writing logic, tone & structure
blog/topics.json                 # Editable queue of pending/done blog topics for the auto-blog generator
blog/posts.json                  # SINGLE SOURCE OF TRUTH for blog metadata & archive
blog/posts/{slug}.{html,md}      # EN blog posts (+ Markdown twins)
blog/posts/{lang}/{slug}.{html,md}  # Translated blog posts (sk, cs, de, pl)
locales/ui/{en,sk,cs,de,pl}.json # SINGLE SOURCE OF TRUTH for UI strings (100% 5-lang parity required)
en/ sk/ cs/ de/ pl/              # GENERATED by scripts/build_i18n.py — DO NOT hand-edit
llms.txt, llms-full.txt          # GEO / AI-agent knowledge graph (auto-synced by scripts/sync_site.py)
robots.txt, sitemap.xml, rss.xml # SEO & AI crawler discovery (all AI search bots allowed)
privacy*.html, disclaimer*.html, terms*.html, cookie.html, impressum*.html  # Legal pages
functions/                       # Cloudflare Pages Functions (edge API + Markdown negotiation)
scripts/                         # dev_server.py, build_i18n.py, check_i18n.py, verify_site.py, minify_js.mjs, sync_site.py, publish_post.py, generate_blog_draft.py
.github/workflows/               # auto-blog.yml (Mon/Thu + manual PR generator), indexnow-on-merge.yml (auto Bing/Seznam/Yandex ping)
```

---

## 4. Blog Governance: How It Works, Auto-Generation & Responsibility

1. **Single Sources of Truth:**
   - **Writing logic & tone:** `blog/writer-rules.md` (edit directly on GitHub to steer future posts without touching Python).
   - **Topic queue:** `blog/topics.json` (`pending` / `done` items; or pass a custom topic in GitHub Actions `Run workflow`).
   - **Published metadata:** `blog/posts.json`.
   - **Post content:** `blog/posts/{slug}.{html,md}` (EN) and `blog/posts/{lang}/{slug}.{html,md}` (SK, CS, DE, PL).
   - Language blog indexes (`/{lang}/blog/index.html`), `sitemap.xml`, `llms.txt`, and `llms-full.txt` are generated automatically by `scripts/sync_site.py` + `scripts/build_i18n.py` — never hand-edit generated `/en`, `/sk`, `/cs`, `/de`, `/pl` files.
2. **Automated Publishing Pipeline (GitHub Actions — replaces legacy Hetzner Hermes VPS):**
   - **Workflow:** `.github/workflows/auto-blog.yml` (Node 24 native `actions/checkout@v7` + `actions/setup-python@v7`) runs every **Monday & Thursday at 08:00 UTC** or manually via **Run workflow**.
   - **Required GitHub repo setup:** Secret `OPENROUTER_API_KEY` + Settings → Actions → General → *Read and write permissions* + *Allow GitHub Actions to create and approve pull requests*.
   - **Execution (`scripts/generate_blog_draft.py` → `scripts/publish_post.py --langs sk,en,cs,de,pl --allow-missing --pr`):**
     1. Reads `blog/writer-rules.md`, `AGENTS.md`, and `.agents/product-marketing.md`, then picks the next `pending` topic from `blog/topics.json` (or custom `--topic`).
     2. Generates EN + SK drafts and translates CS/DE/PL via OpenRouter (`OPENROUTER_API_KEY`) using the preferred model order: **`deepseek/deepseek-v4.1-flash-1017`** (primary) → **`openai/gpt-6-luna`** (fallback), with automatic `429`/`5xx` exponential backoff retries and HTML structure QA.
     3. Runs `scripts/sync_site.py` (updates `.md` twins, `llms.txt`, `llms-full.txt`, `sitemap.xml`) and `scripts/build_i18n.py` (rebuilds all 5 language blog indexes).
     4. Creates branch `hermes/blog-<slug>`, marks the topic `done` on that branch, and opens a **Pull Request** for human review. Never pushes directly to `main`.
   - **Auto-Indexing after Merge (`.github/workflows/indexnow-on-merge.yml`):**
     - When Marián reviews and merges the PR into `main`, Cloudflare Pages deploys automatically and `indexnow-on-merge.yml` submits the new post URLs + `sitemap.xml` to **IndexNow** (`api.indexnow.org` & `www.bing.com/indexnow`) for instant Bing/Seznam/Yandex indexing.
3. **Who Is Responsible:**
   - **Drafting & technical publishing:** Autonomous GitHub Actions pipeline + OpenRouter models (`scripts/generate_blog_draft.py` & `scripts/publish_post.py`).
   - **Final editorial & legal responsibility:** **Marián Stančík** (human-in-the-loop). No blog post goes live without Marián's explicit PR merge. Every post carries EU AI Act Art. 50 disclosure (`<meta name="ai-generated-content" content="true">`) and a clear non-legal-advice notice.

---

## 5. Essential Commands

```bash
python3 scripts/dev_server.py 8080        # Local dev server with clean URLs (npm run dev)
node scripts/minify_js.mjs                # Minify js/*.js + js/i18n/*.js + css/main.css -> css/main.min.css
python3 scripts/build_i18n.py             # Rebuild /en /sk /cs /de /pl + js/i18n chunks
python3 scripts/build_i18n.py --check     # Fails if generated pages are stale
python3 scripts/check_i18n.py             # Checks hreflang, canonical, internal links, sitemap
python3 scripts/sync_site.py              # Regenerate blog .md twins, llms.txt, llms-full.txt, sitemap.xml
python3 scripts/verify_site.py            # Full 10-tier verification suite (must pass 100%)
```

- **Never run `npm run deploy`** without explicit instruction — production deploys happen via GitHub → Cloudflare Pages.

---

## 6. Mandatory Working Rules for Every Agent

1. **Branch + Pull Request by default** (`feat/…`, `fix/…`, `docs/…`, `seo/…`). Only push directly to `main` if Marián explicitly asks for it in the current conversation.
2. **No secrets in git.** Never commit `.env*`, API keys, tokens, passwords, private keys, or VPS IPs. Reference secrets by environment variable name only.
3. **GDPR & EU AI Act first.** Keep double opt-in intact, never add unapproved trackers/cookies, keep Art. 50 disclosure and the 3rd-year law student non-legal-advice boundary visible everywhere.
4. **Single source of truth.** When updating UI text, edit the template + all 5 `locales/ui/{en,sk,cs,de,pl}.json` files (100% key parity), then run `python3 scripts/build_i18n.py` and `python3 scripts/verify_site.py`.
5. **Invent nothing.** Never fabricate prices, metrics, legal claims, or testimonials. If something is unconfirmed, mark `TODO: confirm`.
6. **Keep it simple.** Plain language, Midnight Navy + Bronze Gold (`css/main.css`), no page-level `<style>` blocks, no e-shop clutter, WhatsApp (`+421 940 377 855`) always easy to find.
