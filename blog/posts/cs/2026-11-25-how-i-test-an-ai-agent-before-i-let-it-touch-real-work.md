# Jak testuji AI agenta, než ho pustím na skutečnou práci

> **Published:** 2026-11-25  
> **Author:** Marian Stancik  
> **Summary:** Agent, který funguje v demu, a agent, který funguje v pondělí ráno, jsou dvě různé věci. Tady je pět kontrol, které provádím, než nějaký agent dostane skutečnou práci.

---

25. listopadu 2026
  AI Agents
  6 min čtení
  Marian Stancik

### Jak testuji AI agenta, než ho pustím na skutečnou práci

Agent, který funguje v demu, a agent, který funguje v normální pondělní ráno, jsou dvě různé věci. Než nechám jakéhokoli agenta sáhnout na skutečnou práci, projde pěti kontrolami. Většina z nich zabere méně než deset minut a později ušetří hodiny úklidu.

### Problém: agenty hodnotíme podle dema

Téměř každý agent, kterého vidím prezentovat online, je ukazován stejně: jeden čistý vstup, přátelský příklad, člověk sledující obrazovku. Vypadá to skvěle. Pak ho připojíte ke skutečné schránce, skutečné tabulce nebo skutečnému požadavku klienta a rozpadne se — ne s pádem, ale tiše.

Tichá selhání jsou ta drahá. Agent řekne „hotovo“, zapíše napůl správný řádek do vaší tabulky, pošle odpověď s nesprávným jménem nebo zacyklí stejné volání nástroje patnáctkrát. Nikdo si toho týden nevšimne.

Náklady to zhoršují. Přes DeepSeek na OpenRouteru protáhnu měsíčně asi 4 miliardy tokenů zhruba za $200. Stejný objem na nejdražších frontier modelech by stál kolem $15,000. Levné tokeny jsou skvělé, ale také znamenají, že zacyklený agent nebolí hned — takže špatný výstup přežije déle, než si ho někdo všimne.

### Jak testuji agenty, než dostanou skutečnou práci

Stavím na open-source frameworcích — většinou Hermes Agent a OpenBot (open-source alternativa k botu Grok) — s DeepSeek přes OpenRouter pro levné iterování. Následujících pět kontrol je stejných bez ohledu na framework.

- 1. Začněte tím nejošklivějším vstupem, jaký máte. Ne ukázkovým příkladem napsaným na klávesnici — skutečným screenshotem, napůl napsaným e-mailem, PDF s tabulkou, která se neparsuje. Pokud agent funguje jen s dokonalým vstupem, postavili jste skript, ne agenta.

- 2. Spusťte ho dvakrát na stejném vstupu. Stejný úkol, stejná data, dvakrát. Pokud se odpovědi liší, zjistěte proč, než mu uvěříte: teplota, pořadí nástrojů, časové razítko skryté v promptu. Nedeterminismus není automaticky špatný, ale nevysvětlený nedeterminismus ano.

- 3. Odeberte nástroj. Odpojte jedno API nebo zrušte jeden klíč a spusťte úkol znovu. Dobrý agent selže hlasitě a řekne vám, co chybí. Špatný si odpověď vymyslí. Hlasité selhání je funkce, kterou chcete.

- 4. Počítejte kroky a tokeny. Logujte každé volání nástroje. Jednoduchý úkol, který zabere čtrnáct kroků, obvykle znamená vágní prompt nebo špatně napsaný popis nástroje, ne těžký úkol.

- 5. Přečtěte si výstup jako cizí člověk. Pochopil by kolega, který nezná vaše nastavení, výsledek, aniž by se vás zeptal? Pokud ne, agent není hotový — jen přesunul práci na někoho jiného.

Nic z toho nepotřebuje testovací framework ani CI pipeline. Potřebuje to dvacet minut a ochotu nenechat se ohromit.

### Kde to selhává a na co si dát pozor

Poctivé limity: pět kontrol nepokryje skutečný svět. Agent může projít všemi a přesto se v úterý rozbít, když web změní HTML nebo klient pošle něco, co jste nikdy neviděli. Testy snižují překvapení; neodstraňují je.

Dvě další pasti, do kterých jsem narazil:

- Testování na jiném modelu, než na kterém nasazujete. Levné modely pro iteraci jsou v pořádku, ale chování se mezi modely mění. Závěrečná kontrola musí běžet na modelu, který skutečně dělá práci.

- Neuvědomované hlídání. Pokud jste vždy nablízku, abyste ho popostrčili, netestujete agenta — testujete sebe. Nechte ho jeden den samotného a podívejte se, co se stane.

A právní stránka: pokud váš agent pracuje s osobními údaji, vstupují do hry GDPR a EU AI Act. Jsem student třetího ročníku práv, ne právník — cokoli píšu o regulaci, je subjektivní poznámka, a pro skutečná rozhodnutí potřebujete advokáta.

### Sečteno a podtrženo

AI je nástroj, ne magie. Rozdíl mezi agentem, který vám šetří čas, a agentem, který tiše nadělá nepořádek, obvykle není v modelu — je v tom, jestli jste strávili dvacet minut tím, že jste se ho nejdřív snažili rozbít.

Pokud si chcete vyměnit poznatky o testování vlastního nastavení, napište mi na WhatsApp na +421 940 377 855, nebo vyzkoušejte bezplatné nástroje na /en/tools/. Tento článek a web jsou připraveny s pomocí AI agentů a závěrečné lidské kontroly.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
