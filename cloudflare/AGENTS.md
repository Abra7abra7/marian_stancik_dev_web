# Cloudflare Architecture — Marian Stancik

## Prehľad

Celý systém beží na **Cloudflare** (jediný provider pre API a dáta).
Web (marianstancik.dev) je na Verceli — nezmenený.

```
┌──────────────────────────────────────────────────────┐
│ Vercel (web)                                         │
│   marianstancik.dev — statický HTML web              │
│   services.html — 7 produktov so Stripe checkout     │
├──────────────────────────────────────────────────────┤
│ Cloudflare (API + data + dashboard + login)          │
│                                                       │
│  DNS (Vercel):                                       │
│    api.marianstancik.dev → CNAME → Worker (priamo)   │
│    app.marianstancik.dev → CNAME → Pages             │
│                                                       │
│  Cloudflare Pages (marian-stancik)                    │
│    └── functions/_middleware.js                       │
│        ├── app.* subdomena → dashboard HTML           │
│        │   └── JS načíta audit dáta z API             │
│        ├── /login → HTML login formular               │
│        ├── /api/login/send → magic link email         │
│        └── /api/report/{id} → proxy na Worker         │
│                                                       │
│  Cloudflare Worker (marian-stancik)                   │
│    ├── /api/health           → health check           │
│    ├── /api/audit/run        → spustí audit           │
│    ├── /api/client/audit     → posledný audit klienta │
│    ├── /api/client/audits    → všetky audity klienta  │
│    ├── /api/report/{id}      → HTML report s PDF      │
│    ├── /api/stripe/webhook   → Stripe udalosti        │
│    ├── /api/stripe/create-checkout → checkout session │
│    ├── /api/subscribe        → newsletter             │
│    ├── /api/crm-email        → CRM dispatcher         │
│    ├── /api/compliance/check → compliance kontrola    │
│    └── /api/invoice?id=...   → invoice proxy          │
│                                                       │
│  D1 databáza (marian-stancik-db)                      │
│    clients → audits → audit_results → alerts          │
│                                                       │
│  Cron Triggers                                        │
│    Pondelok 06:00 → týždenný GEO re-scan              │
│    Každý deň 12:00 → compliance check                 │
└──────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────┐
│ Stripe (test mode)                                    │
│   7 produktov: GEO, Readiness, Full, 3 monitoringy   │
│   Webhook → api.marianstancik.dev/api/stripe/webhook │
├──────────────────────────────────────────────────────┤
│ AgentMail                                             │
│   marianstancik@agentmail.to — notifikácie, reporty  │
│   ascentia@agentmail.to — CRM                        │
└──────────────────────────────────────────────────────┘
```

---

## Služby a produkty

| # | Produkt | Cena | Typ |
|---|---------|:----:|:----:|
| 1 | AI GEO Audit | €199 | One-time |
| 2 | AI Web Readiness Scan | €200 | One-time |
| 3 | Full Web Audit (Combo) | €300 | One-time |
| 4 | GEO Monitoring | €49/mo | Recurring |
| 5 | Compliance Watch | €29/mo | Recurring |
| 6 | Full Monitoring Suite | €69/mo | Recurring |
| 7 | Custom AI Agent | od €500 | One-time |

### Stripe Price IDs (test mode)

| Produkt | Price ID |
|---------|----------|
| GEO Audit | `price_1UKvSSQQHUoXC9gsqOaR96Su` |
| Readiness | `price_1UKvSSQQHUoXC9gsqij0bs56` |
| Full Combo | `price_1UKvSTQQHUoXC9gsJ9k2KXI4` |
| GEO Monitoring | `price_1UKvSUQQHUoXC9gsJbb9ETha` |
| Compliance Watch | `price_1UKvSUQQHUoXC9gsH8fXihf2` |
| Full Suite | `price_1UKvSVQQHUoXC9gs53kRK05k` |

---

## Kompletný flow — čo sa stane keď klient kúpi audit

```
1. Klient na marianstancik.dev/services klikne "Buy"
   → Stripe Checkout session (create-checkout endpoint)

2. Stripe → Webhook POST → api.marianstancik.dev/api/stripe/webhook
   → Vytvorí client záznam v D1 (clients tabuľka)
   → Spustí audit-worker pre daný domain

3. audit-worker:
   a) Vytvorí audit záznam v D1 (audits tabuľka)
   b) Spustí všetky checky (10 GEO + 8 Readiness)
   c) Uloží kompletné výsledky do audit_results
   d) Pošle email klientovi cez AgentMail
   e) Ak skóre kleslo >10 bodov → alert v D1

4. Klient dostane email:
   - Link na dashboard: app.marianstancik.dev?client={email}
   - Link na report: api.marianstancik.dev/api/report/{auditId}

5. Dashboard (app.marianstancik.dev):
   - Zobrazí všetky audity klienta (typ, skóre, stav)
   - Každý audit má odkaz na plný HTML report
   - Magic link login (email → AgentMail → login link)

6. Pri subscription produktoch:
   - Pondelok 06:00 → automatický re-scan
   - Denná kontrola alive + alerty
```
