# Konvergencia agentových architektúr: Prečo všetci stavajú rovnaký dvojúrovňový systém

> **Published:** 2026-09-02  
> **Author:** Marian Stancik  
> **Summary:** NVIDIA AVO, AOS referenčná architektúra a Auton framework sa zhodli na rovnakom vzore: dvojúrovňový dizajn oddeľujúci riadenie od vykonávania pre produkčné autonómne agenty.

---

Za posledné tri mesiace tri nezávislé výskumné tímy — NVIDIA AVO, AOS referenčná architektúra (arXiv 2608.03214) a Auton Agentic AI Framework (arXiv 2602.23720) — nezávisle dospeli k rovnakému architektonickému vzoru pre produkčné autonómne agenty. Dvojúrovňový dizajn, ktorý oddeľuje riadenie a governance od runtime a koordinácie.

    

Toto nie je náhoda. Je to dozrievanie odboru.

    

Keď tímy pracujúce na optimalizácii GPU jadier, interaktívnych reasoning benchmarkoch a enterprise governance agentov nezávisle prídu na rovnaký architektonický split, pozeráte sa na vznikajúci štandard. Názvy sa líšia — AVO to volá "supervision loop + agent loop," AOS "Control & Governance Plane + Runtime & Coordination Plane," Auton "Cognitive Blueprint + Runtime Engine" — ale štrukturálne rozdelenie je identické vo všetkých troch.

    

Tu je vysvetlenie, čo dvojúrovňová architektúra je, prečo je dôležitá pre každého, kto nasadzuje agentov v produkcii, a ako si postaviť vlastnú.

    

### Vzor, pomenovaný rôzne každým tímom

    
      
        
          Framework
          Úroveň 1 — Riadenie
          Úroveň 2 — Runtime
        
      
      
        
          NVIDIA AVO
          Supervízna slučka + vynucovanie politík
          Agent slučka + perzistentná pamäť + nástroje
        
        
          AOS Paper
          Control & Governance: zámer, politika, dôvera, audit
          Runtime & Coordination: životný cyklus, routing, pamäť, plánovanie
        
        
          Auton Framework
          Cognitive Blueprint + constraint manifold
          Runtime Engine + MCP integrácia + paralelné vykonávanie
        
      
    

    

Názvy sa líšia, ale sémantický split je identický: jedna úroveň odpovedá na čo by sa malo stať, druhá na ako to spraviť. Riadiaca úroveň je zdrojom pravdy pre zámer, politiky a autoritu. Runtime úroveň je vykonávací substrát, ktorý premieňa tieto rozhodnutia na koordinované akcie naprieč agentmi, nástrojmi, modelmi a pamäťovými systémami.

    

### Prečo dve úrovne?

    

Súčasné agentové systémy zlievajú riadiacu a vykonávaciu logiku do jedného LLM volania. Model rozhoduje a koná v jednom kroku. To funguje pre jednoduché chatboty. Zlyháva pre viacdňové autonómne operácie, kde potrebujete auditné trail-y, vynucovanie politík, obnovu po zlyhaní a ľudský dohľad.

    

AOS paper formalizuje tento argument definovaním, čo patrí do každej úrovne.

    

Control & Governance Plane vlastní:
    
      
- Zámer (intent): čo používateľ naozaj chce, nie čo model odvodil z nejednoznačného kontextu
      
- Politiky: povolené akcie, rozpočty zdrojov, bezpečnostné obmedzenia, povolené kategórie nástrojov
      
- Dôvera a autorita: delegovaný rozsah, správa credentials, revokačný reťazec
      
- Confidence: podporujú nahromadené dôkazy pokračovanie s touto akciou?
      
- Auditovateľnosť: kto autorizoval čo, kedy, s akými dôkazmi a pod akými obmedzeniami
      
- Ľudský dohľad: stop tlačidlá, schvaľovacie brány, eskalácia, override kontroly
      
- Reconcialiácia stavu: keď sa pozorovaný stav odchýli od autorizovaného, zruš alebo eskaluj
    

    

Runtime & Coordination Plane vlastní:
    
      
- Životný cyklus agenta: spawn, plánovanie, pauza, obnovenie, ukončenie sub-agentov
      
- Model routing: výber a dispečing optimálneho modelu podľa typu úlohy a rozpočtu
      
- Vykonávanie nástrojov: volania MCP serverov, validácia výstupov voči schémam, error handling a retry
      
- Koordinácia pamäte: epizodická, sémantická, procedurálna — doručenie kontextu naprieč sessionami
      
- Workflow progress: stavové automaty, retry politiky, circuit breakers, timeouty
      
- Telemetria: čo sa skutočne stalo, s akou latenciou, za akú cenu
    

    

Oddelenie je dôležité, pretože tieto úrovne sa škálujú inak. Riadiaca úroveň je nenáročná na priepustnosť, ale kritická z hľadiska správnosti — jedno zlé rozhodnutie o politike kontaminuje všetko. Runtime úroveň je náročná na priepustnosť, ale tolerantná voči zlyhaniu — nepodarené tool volanie sa zopakuje, zle smerované modelové volanie plytvá výkonom, ale neporušuje politiku.

    

NVIDIA AVO 7-dňový autonómny beh optimalizácie GPU jadier demonštruje tento princíp v praxi. Hlavný agent (runtime) rozhoduje čo preskúmať, zmeniť, otestovať a vyhodnotiť. Supervízor (control) monitoruje stagnáciu, prekročenie rozpočtu a neproduktívne cykly. Keď sa vyhľadávanie zasekne, supervízor presmeruje. Riadiaca úroveň nemusí rozumieť optimalizácii GPU jadier — potrebuje len detegovať, že progres sa zastavil, a spustiť korektívnu akciu.

    

### Tri mechanizmy, na ktorých sa všetci zhodli

    

Naprieč všetkými troma architektúrami sú tri mechanizmy nevyhnutné pre produkčné autonómne agenty.

    

### 1. Perzistentná pamäť mimo kontextového okna

    

Každá architektúra sa zhoduje: agent, ktorý sa resetuje na nulu na konci každého kontextového okna, nedokáže udržať dlhodobú prácu. LLM sú bezstavové naprieč sessionami — keď sa kontextové okno naplní alebo session skončí, všetky skúsenosti sú stratené, pokiaľ nie sú explicitne uchované.

    

AVO používa perzistentné úložisko pre zmeny kódu, výstupy kompilátora, profiler výsledky a nahromadené uvažovanie počas 7-dňových behov. AOS paper definuje štyri typy stavov — intended state, authorized state, observed state a resulting state — ktoré prežívajú medzi invokáciami a tvoria základ pre audit a reconciliáciu. Auton framework zavádza reflector-driven konsolidačný protokol, inšpirovaný biologickým hippocampálnym prehrávaním, ktorý počas nečinnosti komprimuje epizodické skúsenosti do sémantickej a procedurálnej pamäte.

    

Implementačný vzor: ukladajte štruktúrovaný stav do SQLite alebo vektorovej databázy. Keď sa kontextové okno blíži k kapacite, runtime úroveň zapíše checkpoint. Riadiaca úroveň validuje výsledný stav voči politikám pred začiatkom ďalšieho cyklu. Tým sa limitácia kontextového okna mení z chyby na feature — každé okno sa stáva ohraničenou atomickou jednotkou práce.

    

### 2. Supervízia a constraint-based guardrails

    

Všetky tri architektúry odmietajú predstavu, že prompt engineering sám o sebe udrží agentov v bezpečí v produkčnom meradle. Prompt-based safety je krehká, neriaditeľná a neprodukuje auditný trail.

    

NVIDIA AVO používa vyhradený supervízor, ktorý beží paralelne s hlavným agentom. Jeho jedinou úlohou je detegovať stagnáciu — opakujúce sa chybové vzory, plató metriky, neproduktívne cykly — a spúšťať presmerovanie. Supervízor nemusí rozumieť doméne. Potrebuje jasnú definíciu "zaseknutia" a eskaláčnú cestu.

    

Auton framework zavádza constraint manifold — formálne definovaný podpriestor akčného priestoru — na ktorý sa politika agenta premieta pred emisiou akcie. Bezpečnosť je vynútená konštrukciou, nie post-hoc filtrovaním. Eskalácia privilégií a nebezpečné operácie sú v manífoldle štrukturálne nemožné.

    "Bezpečnosť nie je delegovaná na prompt engineering alebo post-hoc output filtering. Namiesto toho sú obmedzenia vyjadrené ako špecifikácie na úrovni kódu, čo zaručuje, že eskalácia privilégií a nebezpečné operácie sú vylúčené už konštrukciou." — Auton Agentic AI Framework (arXiv 2602.23720)

    

AOS paper ide ďalej a definuje reconciliačné kontroléry, ktoré kontinuálne porovnávajú pozorovaný stav s autorizovaným. Keď sa odchýlia — agent prekročil rozpočet, pristúpil k obmedzenému nástroju, operoval mimo delegovaného rozsahu — kontrolér zruší operáciu, izoluje agenta a eskaluje človeku. Toto nie je guardrail prompt. Je to deterministická riadiaca slučka.

    

To isté robím s watchdog cron jobmi a Python monitor skriptami. 50-riadkový Python skript, ktorý zabije úlohu keď prekročí svoj iteračný rozpočet, je nekonečne spoľahlivejší ako akýkoľvek prompt-based guardrail. Constraint manifold prístup naznačuje, že by sme mali ísť ďalej — definovať povolený akčný priestor v kóde, nie v promptoch.

    

### 3. Typované, objaviteľné tool rozhrania

    

Všetky tri frameworky používajú typované tool rozhrania viazané cez Model Context Protocol (MCP) alebo ekvivalent. Evolúcia od neštruktúrovaných promptov k typovaným tool registrom zrkadlí evolúciu REST bez schémy k OpenAPI — a odvetvie je v rovnakom inflexnom bode.

    

AOS paper explicitne nazýva tool registre "agentovou analógiou API gateway" — enumerujú, verzionujú a access-controlujú každý nástroj dostupný agentovi. Auton framework robí MCP integráciu svojím primárnym externým rozhraním, pričom nástroje sú typované kontrakty so vstupno-výstupnými schémami a preconditionami. AVO tool rozhranie je najviac obmedzené z troch, presne preto, že jeho doména optimalizácie GPU jadier vyžaduje striktnú validáciu schém pre kompilátorové flagy, profiler parametre a testovacie konfigurácie.

    

Praktický dôsledok: ak váš agent volá nástroje cez free-text prompty, máte integráciu, nie architektúru. Bez typovanej vrstvy rozhrania nemôžete auditovať používanie nástrojov, validovať ich výstupy ani vynucovať prístupové politiky. MCP sa stáva štandardom pre túto vrstvu — tool registre sú, ako poznamenáva AOS paper, "miestom, kde sa agent stretáva s enterprise."

    

### Od architektonického vzoru ku compliance architektúre

    

Konvergencia nie je len technicky zaujímavá. Priamo sa mapuje na regulačné požiadavky, ktoré nadobudli účinnosť v auguste 2026.

    

EU AI Act požaduje presne tie schopnosti, ktoré dvojúrovňová architektúra poskytuje ako vstavané štrukturálne vlastnosti, nie ako dodatočné dokumentačné cvičenia:

    
      
- Článok 9 — Riadenie rizík: vynucovanie politík a constraint-based guardrails v riadiacej úrovni implementujú mitigáciu rizík konštrukciou
      
- Článok 12 — Vedenie záznamov: riadiaca úroveň už loguje každé autorizačné rozhodnutie, každú delegáciu, každý override politiky — to nie sú samostatné compliance záznamy, je to natívny auditný trail systému
      
- Článok 13 — Transparentnosť: riadiaca úroveň vie rekonštruovať prečo bolo rozhodnutie prijaté prehratím autorizovaného stavu pred akciou, politiky, ktorá ho riadila, a výsledného stavu po vykonaní
      
- Článok 14 — Ľudský dohľad: stop tlačidlo, schvaľovacie brány a eskalácia sú natívne architektonické prvky, nie dodatočné prídavky
    

    

Májová dohoda Digital Omnibus 2026 vyjasnila, že multi-agentové systémy sú považované za jeden regulovaný systém. To robí dvojúrovňovú architektúru ešte relevantnejšou: riadiaca úroveň spravuje celý multi-agentový cluster, nie jednotlivých agentov. Runtime úroveň vykonáva naprieč clusterom. Compliance sa vzťahuje na systém, nie na každého agenta samostatne.

    

Systémy bez samostatnej riadiacej úrovne budú mať problém preukázať čokoľvek z toho. Auditné trail-y dodatočne prichytené k monolytickej architektúre produkujú záznamy, ktoré hovoria čo sa stalo, ale nie prečo — a "prečo" je to, čo AI Act požaduje.

    

### Stavba vlastného dvojúrovňového stacku

    

Tu je praktický deploy pattern, ktorý používam a ktorý zrkadlí vznikajúci štandard. Beží na Hetzner CX33 VPS za €8,49/mesiac a aktuálne vykonáva 19 autonómnych cron jobov s 99,7% uptime.

    

Riadiaca úroveň (Hermes Agent + cron):
    
      
- Policy-as-code v AGENTS.md súboroch — deklaruje čo agent smie a nesmie, povolenú sadu nástrojov a rozpočtové limity
      
- Watchdog cron + monitor skripty — detegujú stagnáciu, prekročenie iterácií a porušenie politík; reštartujú, presmerujú alebo eskalujú
      
- Validácia checkpointov — overenie výsledného stavu voči autorizovanému stavu pred ďalším vykonávacím cyklom
      
- SQLite audit log — každá autorizácia, každá delegácia, každé zlyhanie so štruktúrovanými metadátami pre replay
    

    

Runtime úroveň (MCP servery + OpenRouter):
    
      
- MCP tool servery — typované, objaviteľné, verzované rozhrania. Každý nástroj deklaruje vstupnú schému, výstupnú schému a prístupové požiadavky vopred
      
- OpenRouter dynamický routing — výber optimálneho modelu podľa typu úlohy. Lacné modely pre rutinnú klasifikáciu, frontier modely pre komplexné uvažovanie
      
- SQLite pamäť — epizodické úložisko pre históriu session, sémantické pre znalostné triplety, procedurálne pre úspešné reťazce nástrojov
      
- Paralelné vykonávanie cez cognitive map-reduce — nezávislé tool volania súbežne, ohraničenie celkového runtime kritickou cestou namiesto súčtu všetkých krokov
    

    

Toto nie je hypotetická architektúra. Rovnaké princípy, ktoré NVIDIA aplikovala na 7-dňovú optimalizáciu GPU jadier, fungujú aj v tomto meradle — len s menším rozpočtom a kratším horizontom.

    

Kľúčový rozdiel oproti monolytickému prístupu: keď cron job zlyhá, riadiaca úroveň vie, že zlyhal, vie ktorú politiku porušil a vie či má retry-núť, eskalovať alebo zastaviť. Runtime úroveň toto rozhodnutie nemusí robiť. Len nahlási zlyhanie. Toto oddelenie zodpovedností je to, čo robí autonómnu prevádzku udržateľnou bez 24/7 ľudského dohľadu.

    

### Vznikajúci štandard

    

AOS paper zachytáva konvergenciu najlepšie: "AOS neprehlasuje žiadnu interpretáciu za neplatnú. Poskytuje vrstvený model, v ktorom každá implementácia môže uviesť, ktoré zodpovednosti poskytuje."

    

Prostredie agentových architektúr sa štandardizuje okolo tohto dvojúrovňového dizajnu. Či už operujete v meradle NVIDIA — 7-dňové behy optimalizácie GPU jadier na DGX B200 clastroch — alebo v meradle jedného VPS s 19 cron jobmi, architektonický vzor je rovnaký. Perzistentná pamäť, constraint-based guardrails a typované tool rozhrania sú nevyhnutné mechanizmy. Riadenie a governance sú oddelené od runtime a koordinácie.

    

Konvergencia sa deje rýchlejšie, než si väčina staviteľov uvedomuje. Tri nezávislé tímy, tri rôzne problémové domény, jedna architektonická odpoveď. Stavajte na tomto vzore. Odvetvie konverguje — či si to jednotliví stavitelia uvedomujú alebo nie.

    
      🤖 AI-generované — Tento článok bol vytvorený s pomocou autonómneho AI agenta (Hermes Agent od Nous Research) a pred publikovaním bol skontrolovaný Marianom Stancikom. Celé zrieknutie.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
