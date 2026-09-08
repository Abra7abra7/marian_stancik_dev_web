# NVIDIA AVO: Keď autonómne agenty bežia 7 dní a prekonajú expertov

> **Published:** 2026-08-27  
> **Author:** Marian Stancik  
> **Summary:** Architektúra AVO od NVIDIA bežala autonómne 7 dní, optimalizovala GPU jadrá a dosiahla 100% na ARC-AGI-3. Systémový dizajn > výber modelu.

---

Minulý týždeň NVIDIA zverejnila výsledky, ktoré zmenili spôsob, akým rozmýšľam o autonómnych agentoch. Ich architektúra AVO (Agentic Variation Operators) bežala nepretržite sedem dní, autonómne preskúmala viac ako 500 optimalizačných smerov, vytvorila 40 verzií jadier a vyprodukovala multi-head attention jadrá, ktoré prekonali FlashAttention-4 až o 10,5% na systémoch DGX B200.

    

Potom zobrali presne tú istú architektúru, pripojili ju k inému prostrediu (ARC-AGI-3, interaktívny reasoning benchmark) a dosiahli 100% — všetkých 183 úrovní v 25 prostrediach, s 12% menej akcií ako predchádzajúci state-of-the-art.

    

Toto nie je príbeh o modeli. Je to príbeh o systémovej architektúre.

    

### Architektúra, ktorá to umožňuje

    

AVO má tri kľúčové mechanizmy:

    

### 1. Perzistentná pamäť
    

Väčšina agentov stratí všetko na konci kontextového okna. AVO uchováva progres — zmeny kódu, výstupy kompilátora, profiler výsledky a nahromadené uvažovanie prežívajú v perzistentnom úložisku. Agent pokračuje z aktuálneho stavu, nie od nuly.

    

### 2. Supervízna slučka
    

Samostatný supervízor monitoruje trajektóriu hlavného agenta a deteguje stagnáciu. Keď sa vyhľadávanie zasekne, supervízor presmeruje agenta na alternatívne stratégie. Počas 7-dňového behu hlavný agent rozhodoval čo preskúmať, zmeniť, otestovať a vyhodnotiť — supervízor ho len udržiaval v pohybe.

    

### 3. Spätná väzba z nástrojov
    

Každá akcia je validovaná proti reálnemu vykonaniu — kompilátory, testy, benchmarky. Agent neháda; meria. To je rozdiel medzi "myslím že to bude fungovať" a "toto jadro sa skompilovalo, spustilo a beží o 3,5% rýchlejšie".

    

### Čo to znamená pre každého, kto nasadzuje agentov

    

Kľúčový insight od NVIDIA: "Schopnosť dlhodobého horizontu je vlastnosťou celého systému. Pamäť určuje čo prežije, nástroje určujú aké akcie sú možné, spätná väzba ukotvuje progres a obnova umožňuje pokračovať aj po vyčerpaní kontextu."

    

To isté robím s Hermes Agentom — SQLite + Obsidian vault ako perzistentná pamäť, watchdog cron ako supervízia, MCP tool calls ako grounded feedback.

    

### Čo to znamená pre rok 2026

    

Systémový dizajn > výber modelu. AVO bežal s Claude Opus 5 aj GPT-5.6 Sol s podobnými výsledkami. Architektúra bola dôležitejšia ako konkrétny model.

    

Autonómne ≠ bez dozoru. Supervízna slučka bola kľúčová. Agenty bez mantinelov driftujú do neproduktívnych cyklov.

    

Dlhý horizont je nová hranica. Väčšina agentov dnes operuje v minútach. AVO operuje v dňoch. Infraštruktúra pre viacdňovú autonómnu prevádzku sa stáva rovnako dôležitou ako samotný model.

    
      🤖 AI-generované — Tento článok bol vytvorený s pomocou autonómneho AI agenta (Hermes Agent od Nous Research) a pred publikovaním bol skontrolovaný Marianom Stancikom. Celé zrieknutie.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
