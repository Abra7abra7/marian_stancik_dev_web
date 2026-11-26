# 4 miliardy tokenov za 200 USD namiesto 15 000 USD: ako reálne šetriť

> **Published:** 2026-11-26  
> **Author:** Marian Stancik  
> **Summary:** Púšťať každú úlohu agenta na najdrahší model je najrýchlejšia cesta k vyhodeným peniazom. Takto mi routing na DeepSeek cez OpenRouter zrazil účet o približne 98 %.

---

26. november 2026
  AI Agents
  6 min čítania
  Marian Stancik

### 4 miliardy tokenov za 200 USD namiesto 15 000 USD: ako reálne šetriť

Za posledný rok moji agenti spracovali približne 4 miliardy tokenov. Účet bol okolo 200 USD. Rovnaká práca na najdrahšom frontier modeli by vyšla zhruba na 15 000 USD. Nie je to žiadny trik — je to jedno rozhodnutie o routingu, ktoré som urobil raz a potom dvanásť mesiacov meral.

### Kde peniaze naozaj miznú

Väčšina ľudí nastaví agenta, pripojí najdrahší model, aký nájde, a na faktúru sa pozrie až vtedy, keď to bolí. Chat pôsobí lacno, lebo pošleš jednu správu a dostaneš jednu odpoveď. Agent tak nefunguje.

Jedna úloha typu „napíš mi report“ sa ľahko zmení na 40 až 80 volaní modelu. Agent prečíta súbor, zavolá nástroj, znova si prečíta kontext, zopakuje nepodarený krok, zhrnie, čo našiel, a nakoniec to naformátuje. Každé z tých volaní so sebou nesie celú konverzáciu. Cena ti rastie s dĺžkou kontextu, nie s dĺžkou výsledku.

Druhý únik je používať frontier model na prácu, ktorá ho nepotrebuje. Roztriediť e-mail, vytiahnuť tri polia z faktúry, preformátovať JSON, rozhodnúť, ktorý nástroj zavolať ďalej — na nič z toho nepotrebuješ najdrahší model na trhu. Ale presne tam to väčšina nastavení posiela, lebo je to default a nikto to nezmení.

### Ako to riešim ja

Používam dva open-source frameworky: Hermes Agent a OpenBot (open-source alternatíva ku Grok botovi). Oba komunikujú s modelmi cez OpenRouter — jeden kľúč, veľa poskytovateľov a logy po jednotlivých requestoch, ktoré si viem reálne skontrolovať.

- Základná vrstva: DeepSeek V4/V4.1 Flash zvládne asi 82 % mojej prevádzky. GLM Flash berie približne 10 % — lacné triedenie, routing, krátke zhrnutia.

- Frontier vrstva: len na ťažké uvažovanie, nejasné rozhodnutia a záverečnú kontrolu. To je jednociferné percento volaní.

- Prompt caching: za 12 mesiacov mám 86,1 % cache hit rate. Systémový prompt a schémy nástrojov sú stabilné, takže plnú cenu platím len za časť, ktorá sa naozaj mení.

- Krátky kontext: výstupy nástrojov orezávam, staré kolá zhrniem a nikdy nelejem celý súbor do okna, keď stačia tri odseky.

Za dvanásť mesiacov to vyšlo na 11,5 miliardy tokenov, 113-tisíc requestov a 416,19 USD celkovo — v priemere 0,04 USD za milión tokenov. Z toho Hermes Agent 6,67 miliardy a OpenBot 4,67 miliardy tokenov.

### Ako merať ROI tokenov

Cena za token sama o sebe neznamená nič. Podstatná je cena za dokončenú úlohu.

- Loguj každý request: model, vstupné tokeny, výstupné tokeny, cachované tokeny, cena a ID úlohy.

- Zoskup to podľa ID úlohy a vypočítaj reálnu cenu jednej hotovej práce.

- Porovnaj to s minútami človeka, ktoré si nahradil. Úloha za dva centy, ktorá ušetrí šesť minút, je dobrý obchod. Úloha za štyri doláre, ktorá ušetrí dve minúty, nie je — nech je model akokoľvek pôsobivý.

- Sleduj cache hit rate každý týždeň. Keď padne, zvyčajne niekto zmenil systémový prompt alebo do jeho začiatku pridal časovú značku.

- Nastav si tvrdý mesačný limit v OpenRouteri. Nie preto, že ho plánuješ dosiahnuť, ale preto, že agent zaseknutý v retry slučke ti rozpočet minie cez noc.

### Kde to zlyháva a na čo si dať pozor

Lacné modely sú lacné z nejakého dôvodu. DeepSeek Flash je viditeľne slabší pri dlhom viackrokovom uvažovaní a pri jemnom dodržiavaní inštrukcií. Stalo sa mi, že ticho zahodil obmedzenie, ktoré som výslovne zadal. Lacný model plus neporiadny prompt rovná sa lacný odpad — a aj na to potrebuješ malú sadu testov.

Caching funguje len vtedy, keď je prefix promptu stabilný. Daj na začiatok dynamickú časovú značku a väčšinu úspory stratíš bez toho, aby si si to všimol.

Latencia a limity sa líšia podľa poskytovateľa, takže čokoľvek používateľské potrebuje záložnú cestu. A posielanie firemných dát tretím stranám je otázka GDPR, nie technická otázka. Som študent 3. ročníka práva, nie advokát — všetko, čo píšem o súkromí alebo EU AI Act, je len môj subjektívny pohľad a na reálne rozhodnutia potrebuješ advokáta.

Ešte jedna vec na rovinu: tento článok aj celý web pripravujú AI agenti s finálnou ľudskou kontrolou. Je to úprimná verzia a zároveň to, čo žiada transparentnosť podľa EU AI Act.

### Zhrnutie

Routing rutinnej práce na DeepSeek cez OpenRouter je najväčšia páka na náklady, akú som našiel — zhruba 98 % dole z účtu a bez zmysluplnej straty na úlohách, na ktorých záleží. Meraj cenu za úlohu, nie za token, a limit si nastav skôr, než ho budeš potrebovať.

Ak si chceš prebrať vlastné nastavenie, napíš mi na WhatsApp +421 940 377 855. Bezplatné nástroje a prompty nájdeš na 
```
/sk/tools/
```
.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
