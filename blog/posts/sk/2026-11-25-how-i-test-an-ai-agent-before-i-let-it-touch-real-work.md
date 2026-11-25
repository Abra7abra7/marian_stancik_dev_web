# Ako testujem AI agenta, kým ho pustím na reálnu prácu

> **Published:** 2026-11-25  
> **Author:** Marian Stancik  
> **Summary:** Agent, ktorý funguje v ukážke, a agent, ktorý funguje v pondelok ráno, sú dve rôzne veci. Päť kontrol, ktoré robím predtým, než agent dostane reálnu prácu.

---

25. november 2026
  AI Agents
  6 min čítania
  Marian Stancik

### Ako testujem AI agenta, kým ho pustím na reálnu prácu

Agent, ktorý funguje v ukážke, a agent, ktorý funguje v pondelok ráno, sú dve rôzne veci. Kým pustím akéhokoľvek agenta na reálnu prácu, prejde piatimi kontrolami. Väčšina zaberie menej ako desať minút a ušetrí hodiny čistenia.

### Problém: agentov hodnotíme podľa ukážky

Takmer každý agent, ktorého vidíš na internete, je predvedený rovnako: jeden čistý vstup, pekný príklad, človek pozerá na obrazovku. Vyzerá to skvele. Potom ho pripojíš k reálnej schránke, reálnej tabuľke alebo reálnej požiadavke od klienta a rozsype sa — nie s pádom, ale ticho.

Tiché zlyhanie je to najdrahšie. Agent napíše „hotovo“, zapíše polopravdivý riadok do tabuľky, pošle odpoveď s nesprávnym menom alebo pätnásťkrát zopakuje to isté volanie nástroja. Nikto si to týždeň nevšimne.

Náklady to ešte zhoršujú. Mne prejde za mesiac približne 4 miliardy tokenov za zhruba 200 USD cez DeepSeek na OpenRouteri. Rovnaký objem na najdrahších modeloch by bol okolo 15 000 USD. Lacné tokeny sú super, ale zároveň znamenajú, že agent v slučke hneď nebolí — a nesprávny výstup tak prežije dlhšie, kým si ho niekto všimne.

### Ako to testujem ja

Staviam na open-source frameworkoch — najčastejšie Hermes Agent a OpenBot (open-source alternatíva ku Grok botovi) — s DeepSeek cez OpenRouter na lacné iterovanie. Päť kontrol nižšie platí bez ohľadu na framework.

- 1. Začni tým najškaredším vstupom, aký máš. Nie vymysleným príkladom — reálnou screenshotou, rozposlaným emailom, PDF s tabuľkou, ktorá sa nedá parsovať. Ak agent funguje len s dokonalým vstupom, postavil si skript, nie agenta.

- 2. Pusť ho dvakrát na ten istý vstup. Rovnaká úloha, rovnaké dáta, dvakrát. Ak sa odpovede líšia, zisti prečo, kým mu začneš veriť: teplota, poradie nástrojov, časová značka skrytá v prompte. Nedeterminizmus nie je automaticky zlý, nevysvetlený nedeterminizmus áno.

- 3. Vezmi mu nástroj. Odpoj jedno API alebo zruš jeden kľúč a pusť úlohu znova. Dobrý agent zlyhá nahlas a povie ti, čo chýba. Zlý agent si odpoveď vymyslí. Hlasné zlyhanie je funkcia, ktorú chceš.

- 4. Spočítaj kroky a tokeny. Loguj každé volanie nástroja. Jednoduchá úloha, ktorá zaberie štrnásť krokov, zvyčajne znamená vágny prompt alebo zle napísaný popis nástroja, nie ťažkú úlohu.

- 5. Prečítaj výstup ako cudzí človek. Pochopil by kolega, ktorý nepozná tvoje nastavenie, výsledok bez toho, aby sa ťa musel pýtať? Ak nie, agent nie je hotový — len presunul prácu na niekoho iného.

Na nič z toho nepotrebuješ testovací framework ani CI pipeline. Potrebuješ dvadsať minút a ochotu nenechať sa ohúriť.

### Kde to zlyháva a na čo si dať pozor

Úprimné limity: päť kontrol nepokryje reálny svet. Agent môže prejsť všetkými a v utorok sa aj tak rozsype, keď web zmení HTML alebo klient pošle niečo, čo si ešte nevidel. Testy znižujú prekvapenia, neodstraňujú ich.

Dve ďalšie pasce, do ktorých som spadol:

- Testuješ na inom modeli, než na akom to reálne beží. Lacné modely na iterovanie sú v poriadku, ale správanie sa medzi modelmi mení. Posledná kontrola musí bežať na modeli, ktorý tú prácu naozaj robí.

- Nevedomé kočíkovanie. Ak si stále nablízku a postrkuješ ho, netestuješ agenta — testuješ seba. Nechaj ho deň samého a pozri sa, čo sa stane.

A právna stránka: ak agent pracuje s osobnými údajmi, nastupuje GDPR a EU AI Act. Som študent 3. ročníka práva, nie advokát — zo zákona neposkytujem právne poradenstvo. Všetko, čo o regulácii píšem, je len môj subjektívny poznámkový blok a na reálne rozhodnutia potrebuješ advokáta.

### Krátky záver

AI je nástroj, nie mágia. Rozdiel medzi agentom, ktorý ti šetrí čas, a agentom, ktorý potichu robí neporiadok, zvyčajne nie je v modeli — ale v tom, či si mu najprv dvadsať minút skúšal podkopať nohy.

Ak si chceš porovnať poznámky k testovaniu vlastného nastavenia, napíš mi na WhatsApp +421 940 377 855 alebo si vyskúšaj bezplatné nástroje na /sk/tools/. Tento článok aj web pripravujú AI agenti s finálnou ľudskou kontrolou.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
