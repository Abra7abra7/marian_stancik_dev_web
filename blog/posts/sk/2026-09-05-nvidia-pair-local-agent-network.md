# Navrhovanie lokálnej agentovej siete pre NVIDIA PAIR — Distribuovaná inferencia naprieč zariadeniami

> **Published:** 2026-09-05  
> **Author:** Marian Stancik  
> **Summary:** NVIDIA PAIR mení nečinné domáce PC na distribuovaný inferenčný cluster pre AI agentov. Ako navrhnúť lokálnu agentovú sieť s viacúrovňovým smerovaním a Hermes Agent.

---

Na veľtrhu IFA 2026 v Berlíne tento týždeň NVIDIA uviedla PAIR — Personal AI Router, bezplatný open-source nástroj, ktorý objavuje nečinné PC v lokálnej sieti a distribuuje inferenčné požiadavky naprieč nimi. Jeden agent môže spustiť päť sub-agentov, ktoré bežia paralelne na troch zariadeniach namiesto čakania v rade na jednej GPU. NVIDIA benchmarky ukazujú 2,04-násobné zrýchlenie — 18 minút na jednom zariadení oproti 8 minútam 48 sekundám pri distribúcii na tri zariadenia.

    

Toto mení spôsob, akým uvažujeme o lokálnych AI agentoch. Problém nikdy nebol výpočtový výkon — bola to nevyužitá kapacita. Viac ako polovica domácností v USA má dva alebo viac počítačov a väčšina z nich leží nečinná počas pracovného dňa. PAIR mení túto latentnú kapacitu na distribuovaný inferenčný cluster, ktorý nakonfigurujete raz a zabudnete naň.

    

Svoju agentovú infraštruktúru prevádzkujem na Hetzner VPS, ale architektonické vzory, ktoré potrebujete na návrh distribuovanej agentovej siete, sú rovnaké bez ohľadu na to, či nasadzujete lokálne alebo v cloude. Tu je vysvetlenie, čo PAIR robí, ako zapadá do vznikajúcej dvojúrovňovej agentovej architektúry a praktický návod na nastavenie vlastnej multi-zariadovej agentovej siete.

    

### Čo je NVIDIA PAIR

    

PAIR nie je distribuovaný tréningový framework. Nie je to spôsob, ako zlúčiť GPU pamäť z viacerých zariadení na spustenie jedného veľkého modelu. Je to load balancer na úrovni požiadaviek pre lokálnu inferenciu.

    

Každé pripojené PC prevádzkuje svoj vlastný lokálny AI stack (Ollama alebo LM Studio s lokálnymi modelmi). PAIR objavuje dostupné zariadenia v lokálnej sieti, monitoruje ich zaťaženie a dostupnosť a smeruje jednotlivé inferenčné požiadavky na zariadenie, ktoré je najlepšie vybavené na ich spracovanie. Keď sa zariadenie pripojí alebo odpojí od siete — notebook príde domov, desktop ide spať — PAIR sa automaticky prispôsobí.

    

Kľúčové rozhodnutie od NVIDIA: PAIR pracuje na úrovni agentových úloh, nie na úrovni individuálnych volaní modelov. Agent, ktorý spúšťa viacero sub-agentov, môže mať inferenčné požiadavky každého sub-agenta distribuované na rôzne zariadenia. Toto je zásadne odlišné od spúšťania jedného modelu na viacerých GPU — je to paralelizmus na úrovni agentov, ktorý zrkadlí, ako multi-agentový systém funguje architektonicky.

    

PAIR podporuje GeForce RTX 20-series a novejšie GPU, RTX PRO Workstation GPU, DGX Spark a Apple M4 alebo novšie čipy — pokrýva tak veľkú väčšinu moderných osobných počítačov.

    

### Ako PAIR zapadá do dvojúrovňovej architektúry

    

Môj predchádzajúci článok sa venoval konvergencii k dvojúrovňovej agentovej architektúre — oddeleniu riadenia/governance od behu/koordinácie. PAIR zapadá do runtime vrstvy, konkrétne do smerovania modelov a paralelného vykonávania.

    

V dvojúrovňovom modeli:
    
      
- Riadiaca vrstva (Control Plane): Definuje úlohu, nastavuje hranice politík, prideľuje sub-agentov. Nezaujíma sa o to, kde inferencia beží, len že výsledky spĺňajú prah kvality
      
- Runtime vrstva: Rozhoduje, ktorý model, na ktorom zariadení, s akým rozpočtom. PAIR je tu — je to mechanizmus, ktorý prekladá "spusti týchto päť sub-agentov" na "sub-agent A → desktop RTX 4090, sub-agenti B a C → notebook RTX 4070, sub-agenti D a E → DGX Spark"
    

    

Toto oddelenie je dôvod, prečo PAIRova architektúra funguje: riadiaca vrstva nemusí poznať hardvérovú topológiu. Deleguje vykonávanie na runtime vrstvu, ktorá používa PAIR na distribúciu inferencie. Abstrakcia udržiava agentovú logiku čistú, zatiaľ čo infraštruktúrna vrstva sa stará o komplexitu orchestrácie naprieč zariadeniami.

    

Rovnaký princíp platí v mojom stacku. Prevádzkujem 19 cronových agentov na Hetzner VPS s Hermes Agent. Riadiaca vrstva (AGENTS.md policy súbory + watchdog skripty) definuje, čo môže každý agent robiť a aký má rozpočet. Runtime vrstva (MCP servery + OpenRouter) rozhoduje, ktorý model zavolať pre každú úlohu. Pridanie PAIR do tohto stacku znamená, že runtime vrstva môže tiež rozhodovať, kde spustiť inferenciu — lokálne pre citlivé dáta, cloud pre náročné úlohy, distribuovane naprieč zariadeniami pre paralelné sub-agentové úlohy.

    

### Tri architektonické vzory pre multi-zariadovú inferenciu

    

Na základe oznámenia NVIDIA PAIR a mojich skúseností s multi-modelovým smerovaním identifikujem tri vzory pre integráciu distribuovanej inferencie do agentového stacku. Každý rieši iný prípad použitia.

    

### Vzor 1: Paralelizmus na úrovni úloh (natívny režim PAIR)

    

To je to, na čo je PAIR navrhnutý. Koordinujúci agent dostane komplexnú požiadavku, rozloží ju na nezávislé podúlohy a každú priradí špecifickému sub-agentovi. Inferencia každého sub-agenta beží na inom zariadení.

    
```

```
# Pseudokód pre paralelizmus na úrovni úloh s PAIR
def coordinate_complex_task(user_request):
    # Rozloženie na nezávislé podúlohy
    sub_tasks = decompose(user_request)
    # ["Preskúmaj ceny konkurencie",
    #  "Vygeneruj štruktúru reportu",
    #  "Analyzuj trhové trendy",
    #  "Napíš exekutívne zhrnutie",
    #  "Validuj voči historickým dátam"]

    # Pridelenie každého sub-agenta — PAIR smeruje inferenciu
    sub_agents = [spawn_sub_agent(task) for task in sub_tasks]

    # PAIR distribuuje inferenciu každého sub-agenta
    # na najmenej vyťažené dostupné zariadenie
    # Zariadenie A (RTX 4090 desktop): sub_agents[0], sub_agents[2]
    # Zariadenie B (RTX 4070 notebook):  sub_agents[1], sub_agents[3]
    # Zariadenie C (DGX Spark):          sub_agents[4]

    # Zber výsledkov paralelne
    results = await gather([agent.run() for agent in sub_agents])
    return synthesize(results)
```

```

    

Kľúčový poznatok: PAIR rieši smerovanie transparentne. Koordinujúci agent nešpecifikuje cieľové zariadenia — spúšťa sub-agentov a PAIR objavuje dostupné zariadenia, kontroluje, ktoré modely sú nainštalované, a smeruje inferenciu na optimálne miesto.

    

### Vzor 2: Viacúrovňové smerovanie s NeMo Switchyard

    

Súbežne s PAIR vydala NVIDIA aj NeMo Switchyard, open-source knižnicu pre smerovanie modelov, ktorá inteligentne presmeruje každú požiadavku na najschopnejší a nákladovo najefektívnejší model. V kombinácii s PAIR vytvára trojúrovňovú routing architektúru:

    

Úroveň 1 — Lokálna (cez PAIR): Malé lokálne modely (Llama 3.2, Phi-4, Nemotron 3 Nano) pre rutinnú klasifikáciu, sumarizáciu a úlohy s nízkym rizikom. Beží na akomkoľvek RTX PC v lokálnej sieti. Nulová latencia, nulové náklady, plne súkromné.

    

Úroveň 2 — Lokálna prémiová (cez PAIR): Väčšie lokálne modely (Nemotron 3.5 Lightning, DeepSeek Harness) pre komplexné uvažovanie, generovanie kódu a štruktúrovanú analýzu. Smeruje na najschopnejšie lokálne zariadenie — DGX Spark pre ťažké úlohy, RTX 5090 desktop pre stredné úlohy.

    

Úroveň 3 — Cloud (cez OpenRouter): Frontier modely (Claude Opus 5, GPT-5.6 Sol, DeepSeek V4-Flash) pre najťažšie problémy: viacúrovňové uvažovanie, kreatívnu syntézu a úlohy vyžadujúce špecializované znalosti. Volajú sa len vtedy, keď lokálne modely nedosahujú požadovanú kvalitu.

    

### Vzor 3: Bezpečnostne izolované inferenčné zóny

    

Na konferencii Fal.Con 2026 začiatkom tohto týždňa NVIDIA a CrowdStrike oznámili SafeMind — agentový kybernetický bezpečnostný systém postavený na NVIDIA Nemotron. Kľúčový architektonický princíp z tohto oznámenia: bezpečnostné kontroly by mali byť vynucované mimo agenta, v infraštruktúrnej vrstve.

    

PAIR umožňuje tento vzor prirodzene. Ak máte v sieti vyhradený počítač, ktorý sa nikdy nepripája k internetu, môžete nakonfigurovať PAIR tak, aby smeroval citlivú inferenciu — spracovanie dokumentov, správu poverení, analýzu proprietárneho kódu — výhradne na toto izolované zariadenie. Ostatná inferencia smeruje na menej obmedzené stroje.

    

### Návrh vlastného PAIR-kompatibilného agentového stacku

    

PAIR je open source a dostupný teraz pre Windows, macOS a Linux. Tu je návrh, ako navrhnúť stack, ktorý ho plne využíva.

    

### 1. Začnite s koordinujúcim agentom na stabilnom stroji

    

Váš koordinátor by mal bežať na stroji, ktorý je zapnutý 24/7 — domáci server, vyhradený desktop alebo VPS (PAIR funguje cez siete, ale latencia lokálnej siete je nižšia). Tento stroj prevádzkuje Hermes Agent (alebo váš obľúbený agent framework) a slúži ako vstupný bod pre všetky agentové úlohy.

    

Koordinátor nemusí sám vykonávať inferenciu. Rozkladá úlohy, spúšťa sub-agentov a deleguje inferenciu na PAIR-objavené zariadenia. NVIDIA potvrdila na IFA, že Hermes Agent dostane jednoklikové nastavenie lokálneho modelu na RTX GPU, čo toto prepojenie ešte viac utuží.

    

### 2. Nakonfigurujte každé zariadenie s Ollama alebo LM Studio

    
```

```
# Zariadenie A (RTX 4090 — výkonný desktop)
ollama pull nemotron-3.5-lightning
ollama pull llama-3.2-8b

# Zariadenie B (RTX 4070 — notebook)
ollama pull llama-3.2-8b
ollama pull phi-4

# Zariadenie C (DGX Spark — dedikovaný AI box)
ollama pull nemotron-3.5-lightning
ollama pull nemotron-3-nano
```

```

    

### Kde PAIR mení ekonomiku prevádzky agentov

    

Najzaujímavejší dôsledok PAIR je ekonomický, nie technický. NVIDIA Nemotron 3.5 Lightning poskytuje až 4x rýchlejší výstup v porovnaní s modelmi vo svojej triede, s 30% rýchlejším dokončením agentových úloh. V kombinácii s PAIR klesajú náklady na inferenciu na existujúcom hardvéri prakticky na nulu — používate výpočtové cykly, ktoré už boli zaplatené a sedeli nevyužité.

    

Partnerstvo NVIDIA a CrowdStrike poskytuje ďalší údaj. Modely SafeMind od CrowdStrike, postavené na Nemotron, dosahujú vyššiu presnosť ako popredné frontier modely pri 99% nižších nákladoch. Kombinácia Nemotron 3.5 Lightning pre rýchlosť, NeMo Switchyard pre smerovanie a PAIR pre distribúciu znamená, že môžete dosiahnuť kvalitu frontier modelov bez ich cien.

    

Pre sólo zakladateľa alebo malý tím prevádzkujúci autonómne agenty to mení matematiku. PAIR cluster na existujúcom hardvéri plus Nemotron modely pre rutinné úlohy znamená, že cloudové API volania si rezervujete len pre 10-20% úloh, ktoré skutočne potrebujú frontier modely. Všetko ostatné beží lokálne, s nulovými marginálnymi nákladmi a bez toho, aby dáta opúšťali vašu sieť.

    

### Čo PAIR zatiaľ nerieši

    

PAIR je momentálne v beta fáze. Niekoľko medzier stojí za zmienku:
    
      
- Bez podpory cez siete: PAIR funguje v rámci jednej lokálnej siete. VPS v Hetznerovom dátovom centre v Norimbergu sa nemôže pripojiť k PAIR clusteru s vaším domácim PC. To obmedzuje hybridné lokálne+cloud nasadenia — na to stále potrebujete OpenRouter alebo samostatnú routing vrstvu
      
- Bez piningu modelov: PAIR smeruje na akékoľvek zariadenie s požadovaným modelom. Ak potrebujete špecifické zariadenie pre špecifické úlohy, musíte implementovať tagovanie zariadení v koordinátorovi
      
- Bez perzistentného stavu naprieč zariadeniami: Ak sub-agent A beží na Zariadení 1 a sub-agent B na Zariadení 2, nezdieľajú žiadnu pamäť. Potrebujete externú pamäťovú vrstvu (SQLite, vektorová DB), ku ktorej majú prístup obe zariadenia
    

    

Všetky tieto problémy sú riešiteľné na úrovni koordinátora. Môj Hermes Agent stack už rieši smerovanie cez siete pomocou OpenRouter a zdieľanú pamäť pomocou SQLite. Pridanie PAIR pre lokálnu distribúciu inferencie vypĺňa medzeru, ktorú som chcel zaplniť odvtedy, ako som začal prevádzkovať multi-agentové systémy: cenovo dostupnú, súkromnú a nízkolatenčnú inferenciu vo veľkom na existujúcom hardvéri.

    

### Smerom k autonómnemu desktopu

    

Oznámenia NVIDIA z IFA — PAIR, NeMo Switchyard, Nemotron 3.5 Lightning a RTX Spark N1X prichádzajúci v októbri — predstavujú koherentnú víziu: osobný počítač sa stáva centrom vykonávania autonómnych agentov. Nie tenký klient volajúci cloud. Nie herný stroj, ktorý popri tom spúšťa inferenciu. Vyhradená platforma, kde agenti bežia nepretržite, distribuujú prácu naprieč vašimi zariadeniami a escalujú do cloudu len v prípade potreby.

    

Toto je v súlade s tým, čo budujem s Hermes Agent na mojom VPS. Rovnaké architektonické vzory — dekompozícia úloh, viacúrovňové smerovanie, perzistentná pamäť, typované nástrojové rozhrania — fungujú vo všetkých mierkach. Rozdiel je v tom, že s PAIR sa "runtime vrstva" rozširuje za hranice jedného stroja na zariadenia, ktoré už vlastníte.

    
      🤖 AI-generated — This article was generated with the assistance of an autonomous AI agent (Hermes Agent by Nous Research) and reviewed by Marian Stancik before publication. Full disclaimer.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
