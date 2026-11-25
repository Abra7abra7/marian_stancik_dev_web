---
name: ai-dev-legal-eu-sk
description: >
  Analyzuje web alebo aplikáciu individuálneho AI developera (živnostník / SZČO alebo EÚ firma)
  a pripravuje overené právne texty a zákonné náležitosti v súlade s právom EÚ a SR (GDPR, EU AI Act čl. 50,
  cookies, podmienky používania / VOP, AI disclaimer, vylúčenie zodpovednosti, povinné údaje / impressum).
  Použi tento skill vždy, keď používateľ žiada o právne dokumenty na web pre AI projekt, audit zberu dát,
  označenie AI generovaného obsahu, kontrolu cookie bannera, revíziu Privacy Policy / Terms / Disclaimer / Impressum,
  alebo kontrolu súladu webu či SaaS nástroja s právom EÚ a SR — aj keď nepoužije presný názov predpisu.
---

# AI Developer Web Legal Compliance (EÚ & SR)

Špecializovaný pracovný postup na audit webu alebo aplikácie individuálneho AI developera (SZČO / živnostník alebo EÚ právnická osoba) a vypracovanie zákonných právnych textov v súlade s právom EÚ a Slovenskej republiky, pri dôslednom dodržaní hierarchie právnych noriem.

> **Upozornenie:** Výstupy slúžia na prípravu technicko-právnych podkladov a transparentnosti webu; nenahrádzajú individuálne právne poradenstvo advokáta podľa zákona č. 586/2003 Z. z. o advokácii.

---

## Krok 1: Audit webu a zberu údajov (pred písaním textov)

Nikdy negeneruj generické šablóny naslepo. Najprv zanalyzuj projekt používateľa (z poskytnutého kódu, URL, popisu alebo cielených otázok) a zhrň:

1. **Identifikácia prevádzkovateľa:** Živnostník (SZČO) vs. s. r. o. / iná EÚ firma, miesto podnikania/sídlo, IČO, DIČ/IČ DPH, registrácia (Živnostenský register / OR SR), oficiálny kontaktný e-mail (nepoužívaj súkromné adresy, ak má projekt dedikovaný kontakt).
2. **Cieľová skupina a monetizácia:** B2B (podnikatelia), B2C (spotrebitelia) alebo čisto bezplatný informačný/vzdelávací projekt? Pri B2C platia kogentné spotrebiteľské normy, ktoré nemožno zmluvne vylúčiť.
3. **Funkcionalita a AI komponenty:** Čo web ponúka (statický obsah generovaný AI, agentom triedený e-mail, interaktívny chatbot, SaaS nástroj, API, generovanie obrázkov/kódu)? Aké AI modely a tretie strany používa (napr. OpenRouter, OpenAI, Google, Anthropic, self-hosted)?
4. **Tok a zber dát:** Kde presne sa zbierajú osobné údaje (všetky formuláre, IP logy, e-maily, WhatsApp/kontakt, účty, platby, vstupy/prompty používateľov)? Aké cookies, localStorage a analytiku web reálne používa (technicky nevyhnutné vs. opt-in analytika/marketing)? Dochádza k prenosu údajov do tretích krajín (napr. USA — EU-US Data Privacy Framework / SCC)?

Ak kľúčové údaje chýbajú, polož používateľovi stručný zoznam otázok pred vypracovaním finálnych textov. Ak používateľ žiada návrh ihneď, použi jasne označené placeholdery `[DOPLNIŤ: ...]` a upozorni na ne.

---

## Krok 2: Právna analýza a hierarchia noriem

Každý právny text a odporúčanie musí rešpektovať hierarchiu právnej sily noriem (od najvyššej po najnižšiu):

1. **Primárne právo EÚ:** Zmluvy EÚ, Charta základných práv EÚ (najmä čl. 7 a 8).
2. **Sekundárne právo EÚ — Nariadenia** *(priamo účinné a nadradené národným zákonom)*:
   - Nariadenie (EÚ) 2016/679 (**GDPR**).
   - Nariadenie (EÚ) 2024/1689 (**Akt o umelej inteligencii — AI Act**), najmä čl. 50 (povinnosti transparentnosti a označovania AI obsahu, uplatniteľný od 2. 8. 2026).
   - Nariadenie (EÚ) 2022/2065 (**DSA**), ak ide o sprostredkovateľskú službu.
   - Nariadenie (EÚ) 2024/3228 *(zrušenie EÚ ODR platformy k 20. 7. 2025 — už na ňu neodkazuj ako na aktívnu službu)*.
3. **Judikatúra Súdneho dvora EÚ (SDEU / CJEU):** Záväzný výklad práva EÚ (súhlas s cookies, prenosy dát, zodpovednosť prevádzkovateľa).
4. **Smernice EÚ (transponované do národného práva):** Smernica ePrivacy (2002/58/ES), smernica o elektronickom obchode (2000/31/ES), smernice o ochrane spotrebiteľa.
5. **Ústava SR a zákony SR:**
   - Zákon č. 18/2018 Z. z. o ochrane osobných údajov (dopĺňa GDPR tam, kde to nariadenie umožňuje).
   - Zákon č. 452/2021 Z. z. o elektronických komunikáciách (pravidlá pre cookies a úložiská v SR — § 109 ods. 8).
   - Zákon č. 22/2004 Z. z. o elektronickom obchode (§ 4 — povinné identifikačné údaje na webe).
   - Obchodný zákonník (zákon č. **513/1991 Zb.** — pozor na `Zb.`, nie `Z. z.`) — § 3a povinné údaje.
   - Občiansky zákonník (zákon č. **40/1964 Zb.**) a zákon č. **108/2024 Z. z.** o ochrane spotrebiteľa (pri B2C vzťahoch).
   - Autorský zákon (zákon č. 185/2015 Z. z.) — licencia k obsahu, promptom a kódu (§ 39, § 40, § 87 a nasl.).
6. **Podzákonné predpisy, usmernenia a národná judikatúra:** Usmernenia EDPB, stanoviská ÚOOÚ SR, judikatúra ÚS SR a NS SR.

**Pravidlo overovania:** Vždy over aktuálne znenie a účinnosť predpisov z oficiálnych zdrojov (EUR-Lex, Slov-Lex, Curia). Nikdy si nevymýšľaj čísla paragrafov, článkov ani spisové značky. Ak si nie si istý aktuálnym znením, over ho alebo explicitne upozorni používateľa.

---

## Krok 3: Vypracovanie alebo oprava povinných dokumentov

Podľa výsledkov auditu z Kroku 1 priprav alebo zreviduj tieto dokumenty (vždy s jednotným dátumom účinnosti v hlavičke aj pätičke a synchronizovanými `.md` verziami, ak ich web používa):

- **Povinné údaje prevádzkovateľa (Impressum / pätička):** Meno a priezvisko / obchodné meno, miesto podnikania/sídlo, IČO, DIČ / status DPH, zápis v registri (okresný úrad, č. ŽR / OR SR), oficiálny e-mail, prípadne orgán dozoru (SOI, ÚOOÚ SR).
- **Zásady ochrany osobných údajov (GDPR — čl. 13/14):** Identita prevádzkovateľa, **všetky reálne miesta zberu dát** (formuláre, bezpečnostné logy, priamy kontakt / agentom triedený e-mail), účely a právne základy (čl. 6 ods. 1 GDPR), príjemcovia/sprostredkovatelia vrátane AI API (Cloudflare, Google Workspace, PostHog, OpenRouter a pod.), prenosy do tretích krajín (DPF / SCC), doby uchovávania, práva dotknutých osôb a dozorný orgán (ÚOOÚ SR).
- **Zásady používania cookies a úložísk:** Presný zoznam toho, čo kód skutočne ukladá (`localStorage`, `sessionStorage`, cookies) — rozlíšenie nevyhnutných (bez súhlasu podľa § 109 ods. 8 zákona č. 452/2021 Z. z.) a voliteľných (len po aktívnom opt-in súhlase s rovnocennými tlačidlami *Prijať / Odmietnuť*).
- **Podmienky používania webu a AI Disclaimer:**
  - Označenie AI obsahu (čl. 50 AI Act + human-in-the-loop zodpovednosť).
  - Výlučne informačný/vzdelávací účel — jasné vylúčenie právneho, daňového, investičného a medicínskeho poradenstva.
  - Obmedzenie zodpovednosti s rešpektovaním kogentných limitov (§ 424 OZ — úmysel a hrubá nedbanlivosť; zákonné práva spotrebiteľa) + **salvatórna doložka**.
  - Duševné vlastníctvo (licencia, nie prevod autorských práv).

### Príklad formulácie zodpovednosti (B2C / zmiešané publikum)

- **Nesprávne (riziko neplatnosti v EÚ/SR):** *„Autor nepreberá absolútne žiadnu zodpovednosť za akékoľvek škody vzniknuté použitím tohto webu alebo AI výstupov.“*
- **Správne:** *„Obsah a bezplatné nástroje sa poskytujú v stave ‚tak, ako sú‘ (AS-IS) v maximálnom rozsahu dovolenom platným právom. Zodpovednosť za škodu spôsobenú úmyselne alebo z hrubej nedbanlivosti sa nevylučuje ani neobmedzuje (§ 424 Občianskeho zákonníka) a nič v týchto podmienkach neobmedzuje zákonné práva spotrebiteľa podľa zákona č. 108/2024 Z. z. Ak sa niektoré ustanovenie stane neplatným, ostatné zostávajú v platnosti (salvatórna doložka).“*

---

## Krok 4: Štruktúra výstupu

Pri audite alebo tvorbe právnych dokumentov použi túto prehľadnú štruktúru:

```markdown
# Právny audit a návrh dokumentov — [Názov projektu]

## 1. Zhrnutie auditu a aplikované predpisy (hierarchia práva)
## 2. Nájdené chyby / chýbajúce náležitosti (prioritizované)
## 3. Upravené alebo vypracované právne texty
## 4. Implementačný checklist pre developera
```

---

## Časté chyby (Gotchas)

- **Absolútne vylúčenie zodpovednosti v B2C:** Bez doložky *„v maximálnom rozsahu povolenom platným právom“* a výnimky pre úmysel/hrubú nedbanlivosť môže byť klauzula neplatná.
- **Zrušená EÚ ODR platforma:** Platforma `ec.europa.eu/consumers/odr` skončila 20. júla 2025 (nariadenie (EÚ) 2024/3228) — neuvádzaj ju ako funkčný kanál.
- **Zámena `Zb.` a `Z. z.`:** Obchodný zákonník je **513/1991 Zb.** a Občiansky zákonník **40/1964 Zb.** (nie `Z. z.`).
- **Zabudnuté formuláre alebo AI API sprostredkovatelia:** Vždy over skutočný kód (všetky `#leadForm`, analytiku, AI API ako OpenRouter/OpenAI), nielen to, čo tvrdí starý text na webe.
- **Rozdielne dátumy účinnosti alebo staré e-maily:** Skontroluj hlavičku, telo, pätičku aj JSON-LD na všetkých jazykových mutáciách a `.md` verziách.
