# 4 miliardy tokenů za 200 USD místo 15 000 USD: Skutečné úspory u AI agentů

> **Published:** 2026-11-26  
> **Author:** Marian Stancik  
> **Summary:** Spouštět každý úkol agenta na frontier modelu je způsob, jak tiše mizí rozpočty. Tady je, jak přesměrování rutinní práce na DeepSeek přes OpenRouter snížilo můj účet za tokeny zhruba o 98 %.

---

26. listopadu 2026
  AI Agents
  6 min čtení
  Marian Stancik

### 4 miliardy tokenů za 200 USD místo 15 000 USD: Skutečné úspory u AI agentů

V loňském roce moji agenti zpracovali přibližně 4 miliardy tokenů. Účet byl asi 200 USD. Stejná zátěž na špičkovém frontier modelu by se vyšplhala někam k 15,000 USD. Není to žádný chytrý hack — je to jedno rozhodnutí o směrování, učiněné jednou a poté dvanáct měsíců měřené.

### Kam peníze skutečně mizí

Většina lidí nastaví agenta, připojí nejdražší model, který najdou, a na fakturu se nepodívají, dokud to nezačne bolet. Chat působí levně, protože pošlete jednu zprávu a dostanete jednu odpověď. Agent tak nefunguje.

Jediný úkol „napiš mi zprávu“ se snadno změní na 40 až 80 volání modelu. Agent přečte soubor, zavolá nástroj, znovu přečte kontext, zopakuje neúspěšný krok, shrne, co našel, a poté naformátuje výstup. Každé z těchto volání s sebou nese celou konverzaci. Vaše náklady rostou s délkou kontextu, ne s délkou konečné odpovědi.

Druhý únik je používání frontier modelu na práci, která ho nepotřebuje. Klasifikace e-mailu, extrakce tří polí z faktury, přeformátování JSON, rozhodování, který nástroj zavolat příště — nic z toho nevyžaduje nejdražší reasoning engine na trhu. Ale přesně to tam posílá většina nastavení, protože je to výchozí a nikdo to nemění.

### Jak to směruji

Provozuji dva open-source frameworky: Hermes Agent a OpenBot (open-source alternativa k botu Grok). Oba komunikují s modely přes OpenRouter, který mi dává jeden klíč, mnoho poskytovatelů a logy jednotlivých požadavků, které skutečně mohu auditovat.

- Výchozí úroveň: DeepSeek V4/V4.1 Flash zvládá asi 82 % mého provozu. GLM Flash zabírá přibližně 10 % — levná klasifikace, rozhodování o směrování, krátká shrnutí.

- Frontier úroveň: vyhrazena pro obtížné uvažování, nejednoznačná rozhodnutí a závěrečnou kontrolu. To je malé jednociferné procento volání.

- Prompt caching: moje míra zásahů do cache za 12 měsíců je 86.1 %. Systémový prompt a schémata nástrojů jsou stabilní, takže plnou cenu platím jen za část, která se skutečně mění.

- Krátký kontext: výstupy nástrojů se ořezávají, stará kola se shrnují a nikdy nevkládám celý soubor do okna, když by stačily tři odstavce.

Za dvanáct měsíců to dalo dohromady 11.5 miliardy tokenů, 113K požadavků a celkem 416.19 USD — blended cena 0.04 USD za milion tokenů. Hermes Agent tvořil 6.67B z těchto tokenů, OpenBot 4.67B.

### Jak měřit ROI tokenů

Cena tokenu sama o sobě nic neříká. Záleží na nákladech na dokončený úkol.

- Logujte každý požadavek: model, vstupní tokeny, výstupní tokeny, cachované tokeny, cenu a ID úkolu.

- Seskupujte podle ID úkolu a spočítejte skutečné náklady na jeden dokončený kus práce.

- Porovnejte to s minutami lidské práce, které to nahradilo. Úkol, který stojí dva centy a ušetří šest minut, je dobrý obchod. Úkol, který stojí čtyři dolary a ušetří dvě minuty, dobrý není, bez ohledu na to, jak působivý model je.

- Sledujte míru zásahů cache týdně. Když klesne, někdo obvykle změnil systémový prompt nebo na jeho začátek přidal časové razítko.

- Nastavte tvrdý měsíční limit v OpenRouteru. Ne proto, že ho plánujete dosáhnout, ale protože agent uvíznutý ve smyčce opakování vám ochotně utratí rozpočet přes noc.

### Kde to selhává a na co si dávat pozor

Levné modely jsou levnější z nějakého důvodu. DeepSeek Flash je znatelně slabší v dlouhém vícestupňovém uvažování a v jemném dodržování instrukcí. Stalo se mi, že tiše zahodil omezení, které jsem výslovně nastavil. Levný model plus nedbalý prompt rovná se levný brak a stále potřebujete malou sadu testovacích případů, abyste to zachytili.

Cache funguje jen tehdy, pokud je váš prefix promptu stabilní. Dejte na začátek dynamické časové razítko a přijdete o většinu úspor, aniž byste si toho všimli.

Latence a limity rychlosti se liší podle poskytovatele, takže cokoli vystavené uživatelům potřebuje záložní trasu. A posílání obchodních dat poskytovatelům třetích stran je otázka GDPR, ne technická otázka. Jsem student třetího ročníku práv, ne právník — cokoli píšu o soukromí nebo EU AI Act, je subjektivní poznámka, a pro skutečná rozhodnutí potřebujete advokáta.

Ještě jedna věc, kterou stojí za to říct přímo: tento článek a tento web jsou připravovány pomocí AI agentů, s konečnou lidskou redakční kontrolou. To je ta poctivá verze a je to také to, co požadují pravidla transparentnosti EU AI Act.

### Sečteno a podtrženo

Směrování rutinní práce na DeepSeek přes OpenRouter je největší páka na náklady, kterou jsem našel — zhruba 98% sleva z účtu, bez smysluplné ztráty na úkolech, na kterých záleží. Měřte náklady na úkol, ne na token, a zastropujte rozpočet dřív, než ho budete muset řešit.

Pokud si chcete probrat vlastní nastavení, napište mi na WhatsApp na +421 940 377 855. Bezplatné nástroje a prompty najdete na 
```
/sk/tools/
```
.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
