# Privacy Policy — EN

> **DRAFT – requires attorney review before publication.**
> Version 3.0 (draft dated 1 November 2026). Publish only after Marián's final approval and attorney review. Replaces privacy.md v2.0. (Slovak version prevails.)

For website https://marianstancik.dev

## 1. Data Controller

The Controller pursuant to Article 4(7) of Regulation (EU) 2016/679 (GDPR) and Section 22 of Act No. 18/2018 Coll. on Personal Data Protection is:

- **Controller:** Marian Stancik — Sole Proprietor (fyzická osoba – podnikateľ)
- **Place of Business:** Černákova 2046/8, 977 01 Brezno, Slovak Republic
- **Business ID (IČO):** 57068917 | **Tax ID (DIČ):** 1082585075 | Non-VAT payer
- **Trade Register:** District Office Brezno, No. 630-22847
- **GDPR Contact:** marianstancik@agentmail.to
- **Web:** https://marianstancik.dev

## 2. What Personal Data We Process and Why

This website sells no products or services and collects personal data at **one place only** (see below). The blog and the prompt library do not collect personal data.

### 2.1 Single collection point: #leadForm on /tools/starter-kit/

| Purpose | Categories of Data | Lawful Basis | Retention |
| :--- | :--- | :--- | :--- |
| Sending the free "Starter Kit" (prompt pack, playbook, checklist) and optional updates by e-mail | E-mail address, optionally name, date/time of submission, source tag ("starter-kit") | **Consent** — Art. 6(1)(a) GDPR; § 13 of Act No. 18/2018 Coll. (mandatory checkbox + double opt-in) | Until consent withdrawal (1-click unsubscribe); consent evidence (double opt-in record) max. 6 months after withdrawal to demonstrate compliance under Art. 5(2) GDPR |

Double opt-in mechanism: after submitting the form (with a mandatory GDPR consent checkbox and spam protection via Turnstile/honeypot), the subscriber confirms the subscription by clicking a verification link in an e-mail; without confirmation the address is not activated for updates. *(Note: verify in implementation before publication — see open questions in the change summary.)*

### 2.2 Operational and security logs

| Purpose | Categories of Data | Lawful Basis | Retention |
| :--- | :--- | :--- | :--- |
| Security and infrastructure protection (Cloudflare) | IP address, timestamp, user agent, HTTP status | Legitimate interest — Art. 6(1)(f) GDPR (cybersecurity, form-abuse prevention) | Up to 90 days in rotating logs (proposed) |

### 2.3 What we DO NOT process

- No payment data (the website accepts no payments).
- No marketing, tracking or advertising cookies without consent (see Cookie Policy; PostHog EU analytics runs **only after an explicit opt-in consent**).
- No profiling or automated decision-making within the meaning of Article 22 GDPR.
- Children's data: the website is not directed at persons under 16 (Art. 8 GDPR; § 20 of Act No. 18/2018 Coll.); we do not request consent or data from such persons.

## 3. Recipients and Processors

| Provider | Role | Country / Transfer |
| :--- | :--- | :--- |
| **Cloudflare, Inc.** | Hosting (Cloudflare Pages), CDN, security headers, form verification (Turnstile) | USA — EU-US Data Privacy Framework certified + SCCs |
| **AgentMail** | Transactional e-mail (confirmation, welcome, unsubscribe) | Storage and transfer mechanism **to be verified before publication** (see open questions) |
| **Hetzner Online GmbH** | CRM relay webhook (lead recording) | Germany (EU) |
| **Google** (Google Sheets) | Lead list storage | Depending on account setup — **to be verified before publication** (see open questions) |
| **PostHog** (EU Cloud, Frankfurt) | Traffic analytics **only after opt-in consent** | Germany (EU), no marketing cookies |

Data processing agreements (Art. 28 GDPR) are or will be concluded, or standard contractual clauses apply where the provider is not covered by applicable EU transfer mechanisms.

## 4. Rights of Data Subjects

Under Articles 15–22 GDPR and Act No. 18/2018 Coll. (§§ 28–48), you have in particular:

- right of access (Art. 15),
- rectification (Art. 16) and erasure (Art. 17),
- restriction of processing (Art. 18),
- data portability (Art. 20),
- the right to object (Art. 21) and to withdraw consent at any time (without affecting the lawfulness of processing before withdrawal),
- the right to lodge a complaint with a supervisory authority.

Requests: **marianstancik@agentmail.to** (answered within 30 days).

**Supervisory Authority:** Office for Personal Data Protection of the Slovak Republic, Hraničná 12, 820 07 Bratislava 27, https://dataprotection.gov.sk

## 5. Security of Processing

Pursuant to Article 32 GDPR: TLS 1.3, strict security headers (HSTS), form spam protection (Turnstile + honeypot), least-privilege access, European infrastructure.

## 6. Changes to this Policy

Material changes are announced on this page; for consent-based processing, changes require new consent where the scope requires it.

---
*Applicable law: Regulation (EU) 2016/679 (GDPR) — effective 25 May 2018; Act No. 18/2018 Coll. as amended; § 109 of Act No. 452/2021 Coll. (end-device storage, see Cookie Policy); Regulation (EU) 2024/1689 (AI Act), Art. 50 — applicable from 2 August 2026 (AI content transparency).*