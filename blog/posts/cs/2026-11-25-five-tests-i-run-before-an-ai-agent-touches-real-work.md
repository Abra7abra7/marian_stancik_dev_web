# Pět testů, které spouštím, než se AI agent dotkne skutečné práce

> **Published:** 2026-11-25  
> **Author:** Marian Stancik  
> **Summary:** Levný agent, který tiše selže, stojí víc než drahý, který se zastaví. Pět nudných kontrol, které provádím, než předám skutečný úkol.

---

25. listopadu 2026
  AI Agents
  5 min čtení
  Marian Stancik

### Pět testů, které spouštím, než se AI agent dotkne skutečné práce

Pět kontrol. Tak dlouho mi trvá rozhodnout, zda AI agent získá přístup ke skutečné práci, nebo zůstane v sandboxu. Žádné benchmarky, žádné snímky obrazovky z žebříčků — pět nudných testů, které stojí pár dolarů a jedno odpoledne.

### Proč většina lidí testuje agenty špatně

Většina lidí hodnotí agenta podle jeho dema. Napíšete hezkou otázku, on hezky odpoví, všichni přikývnou. Problém je, že demo běží po čisté cestě: dokonalý vstup, žádná chybějící pole, žádné napůl rozbité API, nikdo na druhé straně nečeká.

Skutečná práce je chaotická. Přijde formulář s prázdným polem DPH. V doručené poště je zpráva ve třech jazycích. API vrátí 200 OK s chybou ukrytou uvnitř těla odpovědi. Agent, který zvládne demo a pak u chaotické verze tiše selže, je horší než žádný agent — protože přestanete kontrolovat.

Náklady nejsou v tokenech. Náklady jsou e-mail, který nikdy neodešel, faktura se špatným číslem, klient, který dva dny čekal na odpověď, kterou agent údajně vyřídil.

### Jak testuji agenta, než se dotkne čehokoli skutečného

Stavím na open-source frameworcích — většinou Hermes Agent a OpenBot (open-source alternativa k Grok bot) — a model směruji přes DeepSeek on OpenRouter. Tahle kombinace je dost levná na to, aby bylo testování v podstatě zdarma. Tady je postup.

- 1. Test prázdného vstupu. Nepošlu nic. Pak jednu mezeru. Pak 40stránkové PDF. Pak soubor se špatnou příponou. Pokud agent místo zastavení vymyslí odpověď, selže.

- 2. Test zastavení a dotazu. Dám mu úkol s jedním záměrně chybějícím detailem — datum, částka, příjemce. Dobrý agent se zeptá. Špatný agent sebevědomě hádá, a sebevědomé hádání je nejdražší chování v celém systému.

- 3. Náklady na dokončený úkol, ne na token. Ceny tokenů odvádějí pozornost. Záleží na tom, kolik stojí jeden dokončený úkol. Minulý měsíc jsem přes DeepSeek on OpenRouter protlačil zhruba 4 miliardy tokenů za přibližně $200. Stejný objem na nejdražších špičkových modelech by se vyšplhal k přibližně $15,000. Poučení je stejné v obou případech: měřte dokončenou práci, ne účtenku.

- 4. Test opakovatelnosti. Spustím identický úkol desetkrát a porovnám výstupy. Pokud se struktura při každém běhu mění, agent není připravený na nic, co plní databázi nebo obsluhuje klienta.

- 5. Test vrácení zpět. Než cokoli zapíše, odešle nebo smaže, potřebuji dry-run režim a log, který skutečně přečtu. Pokud to nemůžu vrátit zpět, nezapínám to.

Nic z toho není důmyslné. Je to stejná disciplína, jakou byste uplatnili u nového zaměstnance v jeho prvním týdnu — jen ten zaměstnanec se nikdy neunaví a nikdy se nenaučí z trapasu.

### Kde to selhává

Projít pěti testy znamená, že agent fungoval v den, kdy jste ho testovali. Neznamená to, že bude fungovat ve třetím týdnu. Modely se aktualizují, prompty stárnou, upstream API přejmenuje jedno pole a celý řetězec tiše produkuje brak, který pořád vypadá správně naformátovaný.

Testy jsou tedy snímek, ne certifikát. Levné testy spouštím znovu každý týden a u všeho, co opustí budovu, držím člověka ve smyčce. AI je nástroj, ne magie — a nástroj potřebuje údržbu.

Ještě dvě upřímná omezení. Za prvé, nemůžu testovat to, co neumím změřit, a spousta úkolů (psaní, úsudek, tón) se čistému měření brání. Za druhé, pokud váš agent pracuje s osobními údaji nebo spadá pod EU AI Act, moje poznámky tady jsou přesně tím — subjektivní postřehy studenta třetího ročníku práv. Nejsem právník a neposkytuji právní poradenství. Promluvte si s advokátem.

### Shrnutí

Testujte nudná selhání, ne působivé úspěchy. Prázdný vstup, chybějící detail, opakovatelnost, náklady na dokončený úkol a způsob, jak to vrátit zpět — to je celý kontrolní seznam a ušetřil mi víc peněz než jakékoli srovnání modelů.

Pokud si chcete projít vlastní nastavení, napište mi na WhatsApp na +421 940 377 855 nebo si vezměte bezplatné nástroje na /sk/tools/. Tento článek, stejně jako zbytek webu, připravují AI agenti a závěrečná lidská kontrola.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
