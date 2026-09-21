00_GAP-REPORT_marianstancik.dev-FO
NÁVRH / DRAFT — nie je právna rada. Pred použitím overiť advokátom. Balík FO marianstancik.dev · 2026-09-21 (Europe/Bratislava).
Gap report — marianstancik.dev (FO Marián Stančík)
NÁVRH — pred použitím overiť advokátom. Nie finálny posudok.
Dátum analýzy: 2026-09-21 · Zdroj identity: FinStat (overené 2026-09-21)
1. Verdikt
Live web nespĺňa požiadavky identifikácie e-commerce a transparentnosti prevádzkovateľa: footer, schema.org affiliation a dokumenty /privacy a /terms stále uvádzajú ASCENTIA s.r.o. namiesto FO Mariána Stančíka (IČO 57068917). Existencia privacy/terms/disclaimer a GDPR checkboxu pri lead formulári je čiastočne v poriadku, chýba však konzistentná SK dokumentácia FO, spoľahlivá cookie politika/banner a oddelenie od ASCENTIA.
2. Checklist
| Položka
| Požiadavka (predpis)
| Stav
| Poznámka
| Identifikácia FO (nie s.r.o.)
| zák. č. 22/2004 Z. z. (e-commerce); zák. č. 455/1991 Zb. (živnostenský)
| FAIL
| Footer + schema affiliation = ASCENTIA
| IČO / DIČ / miesto podnikania na webe
| zák. č. 22/2004 Z. z.; zák. č. 222/2004 Z. z. (DPH — status platiteľa)
| FAIL
| Chýbajú údaje FO; ASCENTIA namiesto IČO 57068917 / DIČ 1082585075
| Kontakt (e-mail, web)
| zák. č. 22/2004 Z. z.; GDPR Art. 13
| PARTIAL
| E-mail/web FO existujú; telefón neuvedený (voliteľné)
| Privacy Policy — controller = FO
| GDPR 2016/679; zák. č. 18/2018 Z. z.
| FAIL
| /privacy uvádza ASCENTIA ako controller
| Cookies + banner súhlas (neesenciálne)
| zák. č. 452/2021 Z. z.; GDPR Art. 6/7
| FAIL / PARTIAL
| Samostatná cookie politika / plný banner neoverené ako vyhovujúce
| VOP — poskytovateľ = FO
| zák. č. 22/2004; ObZ/OZ; zák. č. 108/2024 Z. z.
| FAIL
| /terms = ASCENTIA ako provider
| B2C odstúpenie / digitálny obsah
| zák. č. 108/2024 Z. z.
| PARTIAL
| Ceny transparentné čiastočne; strata práva na odstúpenie pri digitálnom obsahu nie je jasne ošetrená
| AI Act Art. 50 labeling
| AI Act (nariadenie EÚ) Art. 50
| FAIL / PARTIAL
| Transparentnosť AI interakcie / označenie nie systematicky
| Oddelenie od ASCENTIA
| zák. č. 22/2004; transparentnosť prevádzkovateľa
| FAIL
| Kritické — ASCENTIA vo footeri, schema, privacy, terms
| Fakturačné údaje (IBAN, nie platiteľ DPH)
| zák. č. 222/2004; zák. č. 431/2002 (účtovníctvo)
| PARTIAL
| Status DPH treba explicitne; IBAN = SK60 1100 0000 0029 4827 4072
| DPA ak FO spracúva údaje klientov
| GDPR Art. 28
| FAIL
| Chýba spracovateľská zmluva pre custom AI agent / klientské dáta
| Jazyk dokumentov SK vs EN
| prax spotrebiteľskej informovanosti (SK cieľová skupina)
| PARTIAL
| Live docs EN; CoS požaduje SK návrhy (tento balík)
| Ceny služieb (€199 / €200 / €300 / from €500)
| zák. č. 108/2024; 22/2004
| PASS (čiastočne)
| Transparentnosť cien na webe existuje
| Existencia privacy, terms, disclaimer, lead GDPR checkbox
| GDPR Art. 7/13; 18/2018
| PARTIAL PASS
| Dokumenty a checkbox existujú, ale s nesprávnym prevádzkovateľom
3. Kritické FAIL — ASCENTIA
Footer + schema.org affiliation uvádzajú ASCENTIA s.r.o. (IČO 51858959) — zakázané. Prevádzkovateľ je výhradne Marián Stančík, FO, IČO 57068917.
/privacy a /terms označujú ASCENTIA ako controller / provider — porušenie identifikácie podľa zák. č. 22/2004 Z. z. a transparentnosti GDPR Art. 13.
Riziko: spotrebiteľ / B2B partner uzavrie zmluvu s nesprávnou osobou; fakturácia, zodpovednosť a GDPR role sú právne zmätené.
Náprava: odstrániť všetky zmienky ASCENTIA ako prevádzkovateľa/poskytovateľa; nahradiť FO údajmi z FinStat; aktualizovať JSON-LD / schema.
4. Odporúčané poradie fixov
Okamžite: footer, schema, imprint — FO údaje (IČO, DIČ, miesto podnikania, e-mail).
Okamžite: nahradiť /privacy a /terms dokumentmi FO (02_GDPR-ZASADY.md, 04_VOP.md).
Nasadiť /impressum (01_IMPRESSUM.md) a odkazy z footera.
Cookie politika + banner (03_COOKIE-POLITIKA.md) — súhlas pre neesenciálne; Umami cookieless deklarovať.
B2C: checkbox VOP+privacy + výslovný súhlas so začatím digitálnej služby a stratou 14-dňového odstúpenia (06_…).
B2B zmluva + DPA pre custom agent (05_…, 07_…).
AI Act Art. 50: označenie AI obsahu / interakcie na webe a vo VOP.
Preklad SK → EN až po právnom overení SK verzie.
Overiť platiteľstvo DPH na FS (potvrdené faktúrou 21. 9. 2026 — nie je platiteľ DPH); IBAN doplnený (SK60 1100 0000 0029 4827 4072); doplniť [TELEFÓN] a procesorov.
5. Zdroje
Nariadenie (EÚ) 2016/679 (GDPR)
Zákon č. 18/2018 Z. z. o ochrane osobných údajov
Zákon č. 452/2021 Z. z. o elektronických komunikáciách (cookies / súhlas)
Zákon č. 22/2004 Z. z. o elektronickom obchode
Zákon č. 108/2024 Z. z. o ochrane spotrebiteľa
Zákon č. 391/2015 Z. z. o alternativnom riešení spotrebiteľských sporov (ARS)
Zákon č. 185/2015 Z. z. Autorský zákon
Občiansky zákonník č. 40/1964 Zb.
Obchodný zákonník č. 513/1991 Zb. (B2B)
Zákon č. 455/1991 Zb. o živnostenskom podnikaní
Zákon č. 222/2004 Z. z. o DPH
Zákon č. 431/2002 Z. z. o účtovníctve (uchovávanie dokladov)
AI Act — Art. 50 (transparentnosť)
FinStat profil FO Marián Stančík — overenie 2026-09-21
Koniec gap reportu.
Dokument vygenerovaný z overených údajov FO (IČO 57068917, DIČ 1082585075, nie je platiteľ DPH, IBAN SK60 1100 0000 0029 4827 4072, Tatra banka a.s.). Placeholdery [TELEFÓN] a údaje zmluvnej strany klienta zostávajú na doplnenie. Hosting/platby: Vercel / Stripe podľa auditu webu — overiť pred publikáciou.