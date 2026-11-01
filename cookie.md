# Cookie a úložisková politika — SK


Pre webovú stránku https://marianstancik.dev

## 1. Právny základ (ePrivacy)

Podľa § 109 ods. 8 zákona č. 452/2021 Z. z. (v platnom znení; transpozícia čl. 5 ods. 3 smernice 2002/58/ES) je každý, kto ukladá alebo získava prístup k informáciám uloženým v koncovom zariadení užívateľa, oprávnený na to **iba so súhlasom užívateľa**. To nebráni **technickému uloženiu údajov alebo prístupu k nim**, ktorých jediným účelom je prenos alebo uľahčenie prenosu správy, alebo ktoré je **bezpodmienečne potrebné na poskytovanie služby informačnej spoločnosti, ktorú si užívateľ výslovne vyžiadal** (výnimka pre technicky nevyhnutné ukladanie).

## 2. Čo web reálne používa (overené v implementácii)

### A. Technicky nevyhnutné ukladanie (bez súhlasu — výnimka § 109 ods. 8)

| Úložisko | Účel | Doba |
| :--- | :--- | :--- |
| LocalStorage: jazyk (SK/EN/DE/PL), svetlý/tmavý režim | Uloženie zvolených preferencií | Do vymazania používateľom |
| LocalStorage: `ms_consent_analytics` | Zapamätanie vášho rozhodnutia o analytických cookies | 12 mesiacov |
| Session storage / token: **Cloudflare Turnstile** | Ochrana formulára Starter Kit proti spamu/botom (bez sledovania, bez marketingu) | Krátkodobo, pri odoslaní formulára |
| Ochrana proti spamu (honeypot polia) | Filtrovanie botov | Neukladá sa do prehliadača |

### B. Analytika — **len po súhlase (opt-in)**

- Po kliknutí na „Súhlasím“ (dialog „Cookies a analytika“ v pätičke) sa načíta **PostHog EU Cloud (Frankfurt, Nemecko)** s persistence `localStorage+cookie` a začne sa zaznamenávať návštevnosť (page views, udalosti používania nástrojov).
- **Bez súhlasu sa nič neukladá ani sa neposiela žiadny request na PostHog** (overené v js/posthog.js: pred opt-inom nie je vytvorený žiadny ph_* cookie ani localStorage záznam).
- Nesťa sa žiadne krížové sledovanie medzi webmi ani remarketing.
- Súhlas môžete kedykoľvek zmeniť cez „Nastavenia cookies“ (odhlásenie = opt-out, ďalšie zaznamenávanie sa zastaví).

### C. Čo web NEPOUŽÍVA

- Žiadne reklamné, remarketingové ani sledovacie cookies tretích strán (Meta Pixel, Google Ads a pod.).
- Žiadne newsletter cookies; odber je založený na e-mailovom súhlase (viď Zásady ochrany osobných údajov), nie na cookies.

## 3. Záver pre banner

- Technicky nevyhnutné ukladanie nespadá pod povinnosť súhlasu → nie je potrebný banner pre túto kategóriu.
- Analytika (PostHog) je implementovaná ako **opt-in** → spĺňa požiadavku aktívneho súhlasu; pasívny banner („pokračovaním súhlasíte“) sa nepoužíva.
- Pokiaľ by sa v budúcnosti pridala analytika s predvolenými cookies alebo marketingové nástroje, je potrebná novelizácia tejto politiky a súhlasu.

## 4. Ako uložené dáta zrušiť

LocalStorage a cookies môžete kedykoľvek vymazať v prehliadači (Nastavenia → Súkromie a bezpečnosť → Vymazať údaje prehliadania), prípadne cez „Nastavenia cookies“ v pätičke webu.

---
*Zdroj: § 109 ods. 8 zákona č. 452/2021 Z. z., aktuálne znenie (overené na Slov-Lex 1. 11. 2026, verzia účinná od 18. 8. 2026).*