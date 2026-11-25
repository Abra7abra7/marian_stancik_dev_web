# Päť testov, ktoré robím, kým agent dostane reálnu prácu

> **Published:** 2026-11-25  
> **Author:** Marian Stancik  
> **Summary:** Lacný agent, ktorý zlyhá potichu, ťa stojí viac než drahý, ktorý sa zastaví. Päť nudných testov predtým, než agentovi dáš reálnu úlohu.

---

25. november 2026
  AI Agents
  5 min čítania
  Marian Stancik

### Päť testov, ktoré robím, kým agent dostane reálnu prácu

Päť testov. Presne toľko mi stačí na to, aby som sa rozhodol, či AI agent dostane prístup k reálnej práci, alebo zostane v pieskovisku. Žiadne benchmarky, žiadne screenshoty z rebríčkov — päť nudných testov, ktoré stoja pár dolárov a jedno popoludnie.

### Prečo väčšina ľudí testuje agentov zle

Väčšina ľudí hodnotí agenta podľa ukážky. Napíšeš peknú otázku, on odpovie pekne, všetci prikyvujú. Lenže ukážka ide po čistej ceste: dokonalý vstup, žiadne chýbajúce polia, žiadne polofunkčné API, nikto nečaká na druhej strane.

Reálna práca je neporiadna. Príde formulár s prázdnym poľom pre DPH. V schránke leží správa v troch jazykoch. API vráti 200 OK a chybu schovanú v tele odpovede. Agent, ktorý zvládne ukážku a potom potichu zlyhá na tej neporiadnej verzii, je horší než žiadny agent — prestaneš totiž kontrolovať.

Nestojí ťa to na tokenoch. Stojí ťa to e-mail, ktorý nikdy neodišiel, faktúru so zlým číslom a klienta, ktorý dva dni čakal na odpoveď, ktorú mal agent vraj vybaviť.

### Ako testujem agenta, kým pustím čokoľvek reálne

Staviam na open-source frameworkoch — najčastejšie Hermes Agent a OpenBot (open-source alternatíva ku Grok botovi) — a model ťahám cez DeepSeek na OpenRouteri. Taká kombinácia je dosť lacná na to, aby bolo testovanie v podstate zadarmo. Tu je postup.

- 1. Test prázdneho vstupu. Pošlem nič. Potom jednu medzeru. Potom 40-stranové PDF. Potom súbor so zlou príponou. Ak si agent vymyslí odpoveď namiesto toho, aby sa zastavil, neprešiel.

- 2. Test zastav sa a spýtaj sa. Dám mu úlohu, v ktorej zámerne chýba jeden údaj — dátum, suma, príjemca. Dobrý agent sa spýta. Zlý agent sebavedomo hádže a sebavedomé hádanie je najdrahšia vlastnosť celého systému.

- 3. Cena za dokončenú úlohu, nie za token. Ceny tokenov sú rozptýlenie. Podstatné je, koľko stojí jedna hotová úloha. Minulý mesiac som pretlačil približne 4 miliardy tokenov za zhruba 200 USD cez DeepSeek na OpenRouteri. Rovnaký objem na najdrahších frontier modeloch by vyšiel okolo 15 000 USD. Lekcia je v oboch prípadoch rovnaká: meraj hotovú prácu, nie bloček.

- 4. Test opakovateľnosti. Spustím identickú úlohu desaťkrát a porovnám výstupy. Ak sa štruktúra pri každom behu pohne, agent ešte nie je pripravený na nič, čo ide do databázy alebo ku klientovi.

- 5. Test návratu. Kým niečo zapisuje, posiela alebo maže, potrebujem suchý beh a log, ktorý sa dá čítať. Ak to neviem vrátiť späť, nezapnem to.

Nič z toho nie je geniálne. Je to tá istá disciplína, akú by si použil na nového človeka v prvom týždni — len ten človek sa nikdy neunaví a nikdy sa nepoučí z trápnej situácie.

### Kde to zlyháva

Prejsť piatimi testami znamená, že agent fungoval v deň, keď si ho testoval. Neznamená to, že bude fungovať v treťom týždni. Modely sa aktualizujú, prompty starnú, niekto v cudzom API premenuje jedno pole a celá reťaz potichu vyrába odpad, ktorý stále vyzerá správne naformátovaný.

Testy sú teda snímka, nie certifikát. Tie lacné púšťam každý týždeň a pri všetkom, čo opúšťa firmu, držím vo vzorke človeka. AI je nástroj, nie mágia — a nástroj potrebuje údržbu.

Dve úprimné hranice. Prvá: nedá sa otestovať to, čo sa nedá zmerať, a veľa úloh (písanie, úsudok, tón) sa čistému meraniu bráni. Druhá: ak agent pracuje s osobnými údajmi alebo spadá pod EU AI Act, moje poznámky sú presne tým — subjektívne postrehy študenta 3. ročníka práva. Nie som advokát a neposkytujem právne poradenstvo. Na právne veci si zavolaj advokáta.

### Zrnutie

Testuj nudné zlyhania, nie pôsobivé úspechy. Prázdny vstup, chýbajúci údaj, opakovateľnosť, cena za hotovú úlohu a možnosť vrátiť sa späť — to je celý zoznam a ušetril mi viac peňazí než akékoľvek porovnávanie modelov.

Ak si chceš prejsť vlastné nastavenie, napíš mi na WhatsApp +421 940 377 855 alebo si vezmi bezplatné nástroje na /sk/tools/. Tento článok aj celý web pomáhajú pripravovať AI agenti s finálnou ľudskou kontrolou.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
