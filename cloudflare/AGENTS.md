# Cloudflare Architecture — Marian Stancik

## Prehľad

Celý systém beží na **Cloudflare** (jediný provider). Web je na Verceli (nezmenený).
API, databáza, dashboard, cron, a klientské služby sú na Cloudflare.

```
┌─────────────────────────────────────────────────┐
│ Vercel (web)                                    │
│   marianstancik.dev — statický web              │
│   (nezmenený, ostáva na Verceli)               │
├─────────────────────────────────────────────────┤
│ Cloudflare (API + data + dashboard)             │
│                                                  │
│  api.marianstancik.dev ──── CNAME ────┐         │
│  app.marianstancik.dev ──── CNAME ────┤         │
│                                        ▼         │
│  Cloudflare Pages (marian-stancik)     │         │
│    ├── _middleware.js (router)         │         │
│    │   ├── api.* → proxy na Worker    │         │
│    │   └── app.* → dashboard HTML     │         │
│    └── public/ (statické súbory)      │         │
│                                        │         │
│  Cloudflare Worker (marian-stancik)    │         │
│    ├── /api/audit/*      → GEO scan   │         │
│    ├── /api/stripe/*     → platby     │         │
│    ├── /api/subscribe    → newsletter │         │
│    ├── /api/crm-email    → CRM        │         │
│    ├── /api/health       → health     │         │
│    └── /api/invoice      → invoice    │         │
│                                        │         │
│  D1 databáza (marian-stancik-db)      │         │
│    clients → audity → alerts → subskripcie     │
│                                        │         │
│  R2 bucket (marian-stancik-reports)    │         │
│    report-{id}.html                    │         │
│                                        │         │
│  Cron Triggers                         │         │
│    Pondelok 06:00 → týždenný re-scan  │         │
│    Každý deň 12:00 → compliance check │         │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│ Stripe (test mode)                              │
│   Webhook → api.marianstancik.dev/api/stripe    │
├─────────────────────────────────────────────────┤
│ AgentMail                                       │
│   Notifikácie, leady, reporty                   │
└─────────────────────────────────────────────────┘
```

---

## Služby a produkty

### Stripe produkty (test mode)

| Produkt | Cena | Stripe Price ID |
|---------|------|-----------------|
| AI GEO Audit | €199 one-time | `price_1UKvSSQQHUoXC9gsqOaR96Su` |
| AI Web Readiness Scan | €200 one-time | `price_1UKvSSQQHUoXC9gsqij0bs56` |
| Full Web Audit (Combo) | €300 one-time | `price_1UKvSTQQHUoXC9gsJ9k2KXI4` |
| GEO Monitoring | €49/mesiac | `price_1UKvSUQQHUoXC9gsJbb9ETha` |
| Compliance Watch | €29/mesiac | `price_1UKvSUQQHUoXC9gsH8fXihf2` |
| Full Monitoring Suite | €69/mesiac | `price_1UKvSVQQHUoXC9gs53kRK05k` |

### Ako funguje GEO Audit

```
1. Klient klikne "Buy" na marianstancik.dev/services
   → Stripe checkout session
2. Stripe → Webhook → api.marianstancik.dev/api/stripe/webhook
   → Vytvorí client v D1
   → Spustí audit-worker
3. audit-worker skontroluje:
   - robots.txt (existuje? sú AI crawleri povolení?)
   - sitemap.xml (existuje? validný?)
   - llms.txt & llms-full.txt (existujú? obsah?)
   - JSON-LD Schema (Person, Organization, @graph?)
   - AI Crawlers (GPTBot, ClaudeBot, PerplexityBot?)
   - hreflang (EN/SK/DE/PL?)
   - OpenGraph (og:title, og:description?)
   - Security Headers (HSTS, CSP?)
   - Link Headers (llms.txt describedby?)
   - Performance (response time?)
4. Výsledok → D1 (audit_results) + R2 (report HTML)
5. Klient dostane link na dashboard
```

### D1 Databáza

```sql
-- clients: evidencia všetkých klientov
CREATE TABLE clients (id, email, domain, name, plan, stripe_customer_id, status, created_at);

-- audits: história auditov
CREATE TABLE audits (id, client_id, type, status, score, baseline_score, score_delta, report_url, started_at, completed_at);

-- audit_results: JSON s kompletnými výsledkami
CREATE TABLE audit_results (audit_id, raw JSON, summary, recommendations);

-- alerts: alerty pri zmene skóre
CREATE TABLE alerts (id, client_id, type, message, score_before, score_after, acknowledged);

-- subscriptions: predplatné
CREATE TABLE subscriptions (id, client_id, plan, stripe_subscription_id, amount_cents, status, next_billing_at);
```

---

## Endpointy

| Endpoint | Metóda | Čo robí |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/audit/run` | POST `{domain}` | Spustí GEO audit |
| `/api/audit/{clientId}` | GET | Vráti posledný audit |
| `/api/stripe/webhook` | POST | Stripe udalosti |
| `/api/stripe/create-checkout` | POST `{priceId,domain,email}` | Vytvorí Stripe checkout |
| `/api/subscribe` | POST `{email}` | Newsletter |
| `/api/crm-email` | POST `{to,subject,message}` | CRM dispatcher (Auth: Bearer) |
| `/api/invoice?id=...` | GET | Invoice proxy |

---

## Ako to rozbehať (pre klienta)

1. Klient zaplatí na marianstancik.dev/services
2. Stripe webhook zachytí platbu
3. Worker vytvorí clienta + spustí audit
4. Výsledok v D1 + R2
5. Klient vidí dashboard na app.marianstancik.dev?client={id}
6. Pri subscription: každý pondelok automatický re-scan

---

## Upozornenia

- ⚠️ **workers.dev subdomain** sa vypína pri každom `wrangler deploy` — treba re-enable:
  ```bash
  curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/{account}/workers/scripts/marian-stancik/subdomain" \
    -H "Authorization: Bearer {token}" \
    -H "Content-Type: application/json" \
    -d '{"enabled":true}'
  ```
- ⚠️ **DNS je na Verceli** — CNAME záznamy pre `api` a `app` smerujú na `marian-stancik.pages.dev`
- ⚠️ **Main web (marianstancik.dev) ostáva na Verceli** — nemeniť
- ⚠️ **Stripe je v test mode** — pred produkciou treba prepnúť na live keys

---

## Cloudflare Secrets (nastavené)

| Secret | Hodnota |
|--------|---------|
| `AGENTMAIL_API_KEY` | ✅ Nastavený |
| `STRIPE_SECRET_KEY` | ✅ Test key |
| `STRIPE_WEBHOOK_SECRET` | ✅ Nastavený v Cloudflare Secrets |
| `CRM_WEBHOOK_KEY` | ✅ Random |

## Customizácia

- **Dashboard** — uprav `functions/_middleware.js`, HTML v `dashHtml`
- **Audit checky** — uprav `src/audit-worker.js` (pridať/odobrať check funkcie)
- **Cron harmonogram** — uprav `wrangler.toml` → `triggers.crons`
- **Stripe produkty** — Stripe Dashboard (aktuálne test mode)
- **Ceny** — Stripe Dashboard / API