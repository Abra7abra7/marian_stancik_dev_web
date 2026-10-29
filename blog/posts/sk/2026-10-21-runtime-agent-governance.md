# Runtime Governance pre AI agentov: Prečo každý produkčný agent potrebuje pas

> **Published:** 2026-10-21  
> **Author:** Marian Stancik  
> **Summary:** Október 2026: ServiceNow spustil AI Passport, Netzilo predstavil Drift Control, RSA odhalil Agent ID — tri enterprise platformy v 48 hodinách. Ako postaviť governančnú architektúru pre autonómnych agentov s open-source toolingom a Linux primitívami bez enterprise vendor lock-in.

---

21. október 2026
    ·
    12 min čítania
    AI Governance
    Runtime Governance
    ServiceNow
    MCP
    Hermes Agent
  

  

### Runtime Governance pre AI agentov: Prečo každý produkčný agent potrebuje pas

  

14. októbra 2026 Netzilo AI Edge spustil Drift Control — System One modely, ktoré v runtime overujú, či agent ešte vykonáva prácu, na ktorú bol postavený. 15. októbra ServiceNow AI Passport prišiel na trh — kryptograficky podpísané credentials, ktoré agenty nosia do každého tool callu, vynútené Super Intelligence Control Tower. V tom istom týždni RSA Agent ID vstupil na trh — agenty sú traktované ako nazvané identity s risk tier, access review a lifecycle automation.

  

Tri enterprise platformy. Jeden problém. 48 hodín.

  

Agent governance nie je budúcou otázkou. Je scaling bottleneckom októbra 2026. A vendorzy sa pretekajú, aby predali riešenie — cena za agenta, za gateway, za seat. Ale architektúra za ich produktmi nie je proprietárna. Je to zbierka patternov, ktoré každý samostatný tvorca autonómnych agentov môže replikovať dnes s open-source toolingom a Linux primitívami.

  

Bežím 20+ autonómnych agentov na Hermes Agenti od mája 2026. Tento príspevok rozoberá, čo governančná vlna októbra 2026 znamená pre produkčnú architektúru agentov, a ako postaviť open-source ekvivalent AI Passport bez vendor lock-in.

  

### Októbrová governančná vlna: Tri produkty v 48 hodinách

  

Aby sme rozumeli, prečo to je dôležité, pozerajme čo sa spustilo, nie čo sa oznámilo.

  

### 1. Netzilo AI Edge — Drift Control (14. október)

  

Netzilo rozšírilo svoj AI control plane z developer endpointov na SaaS runtimes. Klúčový doplnok: Drift Control, runtime vrstva ktorá používa light-weight System One modely a LLM judges, aby v milisekundách overila, či aktuálna akcia agenta je v rámci roboty, na ktorú bol postavený.

  

Pred Netzilovým releaseom agent governance znamenal dashboardy a audit logy — reaktívny dizajn. Drift Control je profylaktický: interceptuje tool cally agenta na gateway a overuje intent oproti deklarovanému scopovi predtým, než akcia dosiahne cielový systém. Ak agent drifuje — používa tool, k nemá mať prístup, alebo volá API mimo svojej operačnej domény — gateway preusmeruje, ohraničuje, alebo zabíja call v strojovej rychlosti.

  

Toto je prvá produkčná implementácia runtime governančného patternu, ktorý security výskumníci vyzývajú od DseWiki incidentu mája 2026. Každá akcia agenta je traktovaná ako autorizačné rozhodnutie, nie monitorovací event.

  

### 2. ServiceNow AI Passport — Atestovaná autorita (15. október)

  

ServiceNow AI Passport je najarchitektonickejšie dôležitejší produkt z troch. Je to kryptograficky podpísané credential, ktoré každý AI agent nosí v runtime, zakotvené v live business contexte organizácie — CMDB konfigurácie, GRC politiky a approval workflowy.

  

Pas definuje tri věci: identitu agenta, autorizovaný scope a hranice, ktoré nemôže prekročiť. Agent prezentuje tento pas každému service, ktorý volá. Service verifikuje signatúru oproti Control Tower. Ak scope permiti akciu, execúcia proceduje. Ak agent drifuje — pokúša sa volať MCP server, na ktorý nemá autorizáciu, alebo invokovať tool mimo svojho tieru — pas trigeruje gradual enforcement: redirect (log + warn), restrict (deny konkrétnej akcii) alebo kill (terminácia agentovej runtime session).

  

Architektúra ServiceNow je postavená na open specifikáciách — každý identity provider alebo enforcement point môže issue a verify pasy. To je kritické: pattern je implementovateľný mimo ServiceNow platformy.

  
    Čo nám to hovorí: Architektonický pattern za AI Passport nie je nový. Je to OAuth 2.0 scoped tokens, aplikované na tool cally agentov namiesto API endpointov. Insight je, že identita a autorita agenta by mali byť bindované k verifikovateľnému credentialu, nie k systemd service file alebo environment variable. Implementácia je ten istý pattern, ktorý bežím so scoped MCP toolmi od júla 2026 — ale kryptograficky podpísaný a live-revokable.
  

  

### 3. RSA Agent ID — Nazvané identity pre neľudských actorov (okt. 2026)

  

RSA spustil Agent ID, aby rozriešil governančný problém unikálny pre regulované industrije: nemôžete auditovať, čo nemôžete nazvať. Agent ID discovery known a shadow AI agentov cez identity, cloud, endpoint a gateway sources, potom registruje každého s nazvaným ownerom, risk tier a lifecycle state.

  

Platforma má tri komponenty — Discover, Secure, Govern — ktoré zrkadla lifecycle, ktorý identity management prináša ľudským zamestnancom: nájdi každého agenta, aplikuj politiku, prezeraj access, decommission. Každá high-risk akcia vyžaduje verifikovaného ľudského operatora, ktorý ju schvalí s phising-resistant credential. AI a MCP gateway môže bežať úplne on-premises, s policy decisions v environmente klienta a tenant data ostávajúca v US alebo EU regióne podla výberu klienta.

  

Gartner forecast, ktorý RSA citoval — typická Fortune 500 bude bežať 150,000 agentov do 2028, z menej než 15 v 2025 — robí naming problem existenciálnym. Nemôžete zaistiť, čo nevieže že existuje.

  

### Architektonický pattern: Čo tieto tri produkty zdieľajú

  

Napriek rôznemu brandingu všetky tri produkty implementujú rovnakú štyrvrstvovú architektúru:

  
```

```
Runtime Governance Stack
──────────────────────────────────────────────────
Level 1: Agent Identity    — Kto je ten agent? Kto ho vlastní?
         RSA Agent ID, AI Passport identity binding

Level 2: Scope Definition  — Čo agent má autorizáciu robiť?
         AI Passport scope, Netzilo drift boundaries

Level 3: Runtime Gateway   — Enforce pri každom tool call
         Netzilo AI Gateway, ServiceNow Control Tower

Level 4: Audit & Revoke    — Logovať všetko, killovať pri drifte
         Všetky tri: gradual responses + audit trail
```

```

  

Toto je rovnaký pattern ako agent control plane, ktorý BCG popísal v septembri 2026, rovnaké separation-of-concerns, ktoré AOS referenčná architektúra definovala v auguste, a rovnaký governance-first dizajn, ktorý bežím na Hermes Agenti od júna.

  

Jediný rozdiel medzi enterprise produktmi a open-source implementáciou je kryptografická atestácia — a tá gapa sa rychlo zamyká, keď MCP specifikácia dodává signed tool invocations a arxiv paper "From TCP/IP to MCP" vyzýva formalizovaný security governance pre agent protokoly.

  

### Budovanie samostatného AI Passport

  

Enterprise produkty cenná za agenta, za gateway, za seat. Pre sólo foundera bežiaceho 20 agentov na jednom VPS je tá cena prohibitívna. Ale architektúra nie je. Tu je open-source ekvivalent bežaci na mojom stacku dnes.

  

### Level 1: Agent Identity — Systemd Scopes + Hermes Profily

  

Každý agent v mojom Hermes stacku beží ako nazvaný systemd scope s vlastným Unix userom, environmentom a MCP profilom. Identita agenta je jeho systemd service meno a Hermes profile meno — obe scoped na účel agenta.

  
```

```
# Každý agent má vlastnú identitu scope
/etc/systemd/system/hermes-blog.service
/etc/systemd/system/hermes-crm.service
/etc/systemd/system/hermes-legal-monitor.service

# MCP profily obmedzujú tool access per agent
~/.hermes/profiles/blog/mcp-config.json
~/.hermes/profiles/crm/mcp-config.json
```

```

  

Toto je RSA Agent ID Discover funkcia, implementovaná s Linux primitívami. Každý agent je registrovaný, nazvaný a scoped. Neexistuje shadow agent problém, keď každý agentov execúcijny path je systemd unit file.

  

### Level 2: Scope Definition — Deklarativne MCP Tool Permissions

  

Každý agent má deklaratívny config, ktorý definuje, ktoré MCP servery a tooly môže používať. Blog agent môže volať SEO MCP server a filesystem tool, ale nie CRM dispatcher. CRM agent môže čitať z SQLite a písať do Google Sheets, ale nie modifikovať cron schedule.

  
```

```
// hermes/profile/blog/mcp-config.json — scoped tool access
{
  "mcpServers": {
    "openseo": {
      "allowedTools": ["keyword_research", "competitor_analysis"],
      "disabled": false
    },
    "filesystem": {
      "allowedTools": ["read_file"],
      "disabled": false
    },
    "crm": {
      "disabled": true  // blog agent netrapí CRM
    }
  }
}
```

```

  

Toto je ServiceNow AI Passport scope definition, implementovaná ako JSON config file. Autorizačné rozhodnutie nastáva na MCP client vrstve predtým, než tool call je dispatchnutý. Drift je preduvrátený konfiguráciou, nie monitorovaním.

  

### Level 3: Runtime Gateway — Watchdog Cron s Anomaly Detection

  

Každá agentova akcia — tool invocation, LLM call, file write — je logovaná do struktúrovanej SQLite tabuly. Watchdog cron job beží každých 10 minút a porovnáva chovanie každého agenta oproti baseline profilu: očakúvaná token konzumácia, tool call frekvencia a output destinácie.

  
```

```
Agent Behavior Baseline — Hermes SQLite Log
──────────────────────────────────────────────────
blog-agent:
  tools: openseo/keyword_research (avg 3.2 calls/run)
         filesystem/read_file (avg 1.1 calls/run)
  tokens: 4,200-8,100 per run
  output: /var/www/blog/

crm-agent:
  tools: gdrive/sheets_append (avg 2.0 calls/run)
         sqlite/query (avg 5.4 calls/run)
  tokens: 2,800-5,600 per run
  output: /opt/hermes-vault/01-ASCENTIA/03-CRM/

Anomaly: Akýkoľvek agent deviujúci >3 sigma od baseline
         → kill + alert cez Telegram do @marian_s_ai
```

```

  

Toto je Netzilo Drift Control, implementovaný ako cron-based statistický monitor. Je menej sofistikovaný než System One model judge, ale beží na tom istom €6/mo VPS bez dodatočných inferenčných nákladov. Pre 20 agentov sú statistické baselines dostatočné. Keď flota vzráste do 200 agentov, architektúra škáluje na pravý ML judge — ale len tam, kde statistický monitor signalizuje ambigutu.

  
    Prečo to funguje: Rovnaká architektúra, ktorá robí enterprise governance produkty drahými — per-agent gateway, kryptografická signatúra verifikácia, real-time ML inferenc — je nepotrebna v deploymentov, kde každý agent beží na jednom VPS, hovorí s MCP servermi na localhost, a je vlastnený jednou osobou. Výhoda samostatného tvorcu je lokalita. Enterprise vendorzy riešujú cross-machine federáciu. Ak nepotrebujete federáciu, neplatte jej komplexitný náklad.
  

  

### Level 4: Audit a Revoke — Kill Switch

  

Execúcijny trace každého agenta je rekordovaný v write-once SQLite tabule s tamper-evident hash chain. Ak watchdog trigeruje, alebo ak manuálne revokujem pas agenta, systemd service nastáva v fail state a agentov MCP profil je nahradený null configom, ktorý neautorizuje nič.

  
```

```
# Manuálny kill switch — revoke všetkého tool access
#!/bin/bash
# usage: revoke-agent.sh 

echo "{}" > ~/.hermes/profiles/$1/mcp-config.json
systemctl stop hermes-$1.service
systemctl disable hermes-$1.service
logger "[GOVERNANCE] Agent $1 revoked — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

```

  

Toto je ServiceNow kill switch a RSA lifecycle management, implementovaný ako 10-riadkový bash script. Keď poviem "agent je revokovaný," regulator môže verifikovať: agentov posledný MCP config bol prázdny JSON objekt, jeho systemd state je inactive, a audit log ukazuje exactný timestamp revokácie. To je tak binding ako kryptografická atestácia, keď audit trail je primárny evidence.

  

### MCP Governance Gap — a prečo to je dôležité

  

Arxiv paper "From TCP/IP to MCP: Security and Governance Lessons from Internet Protocols" (október 2026) robí kritickú observáciu: MCP specifikácia centralizuje governančnú autoritu v malom počte individuí — dvoch BDFL lead maintainerov a šiestich core maintainerov Agentic AI Foundation. Ak MCP stane kritickou digitálnou infraštruktúrou (170,000+ podporných toolov, backeri vrátane OpenAI, Amazon a Google), jeho governance deficit stáva problémom každého.

  

ServiceNow AI Passport a Netzilo AI Gateway oba adresujú toto z enforcement strany — sedia medzi agentom a jeho MCP toolmi a aplikujú politiku nezavisle od MCP vlastnej governance štruktúry. Ale protokol sám ešte nemá standardizované security primitívy: signed tool invocations, attesting session identity a verifikovateľné scope claims.

  

Mitigácia samostatného tvorcu je rovnaká ako enterprise gapa: enforceovať politiku na MCP gateway, nie na protocol layer. Hermes Agentovo MCP tool filtrovanie — kde klient overuje tool permissions pred dispatchom — je rovnaký pattern. Protokol možno neverifikuje identity, ale váš gateway môže.

  
    Architektúrna rule: Nikdy never trust agentov self-declared scope. Trust len gateway-enforced policy. Toto je Zero Trust princip aplikovaný na agent tool cally — a to je prečo ServiceNow passport verifikácia v runtime je konceptuálne lepšia než MCP súčasný permission model, ktorý relies na agent, aby deklaroval, čo potrebuje.
  

  

### Čo október 2026 mení pre samostatných tvorcov

  

Tri enterprise governance produkty v 48 hodinách je signál, že agent deploymenty prekročili invisiblenú líniu. Otázkou nie je viac "máte governovať svojich agentov?" ale "ako ich governovať bez enterprise cenovej etikety?"

  
    
- Governance je teraz table stakes pre produkčných agentov. Ak deploynete agenta, ktorý interaktuje s externými toolmi, potrebujete štyri vrstvy: identitu, scope, enforcement, audit. ICO októbrová investigácia, EU AI Act enforcement (live od 2. augusta) a októbrová kontajnmentová kaskáda všetky konvergujú na rovnaký requirement. Toto nie je budúca regulácia. Je súčasná enforcement realita.
    
- Lokalitná výhoda samostatného tvorcu je reálna. Enterprise produkty riešujú pre 150,000 agentov cez departments, regióny a cloud providerov. Ak bežíte 20 agentov na jednom serveri, váš governance problém je jednoduchšý o rady magnitúdy. Patterny sú identické. Implementácia je lacnejšia. Ale principy — identita, scope, enforcement, audit — sú non-negotiable pri každej škále.
    
- Kryptografická atestácia ide do MCP. ServiceNow open-spec passport model a AAIF governance reform pressure značia, že natívna MCP identita a scope verifikácia je pravdepodobná v priebehu najbližších dvoch spec revízií. Budovanie vašej governance vrstvy na vrchu MCP tool filtrovania dnes značí, že adoptujete standard keď príde, namiesto nahrádzania proprietárneho riešenia.
  

  
    Metrika, ktorá sa počíta: Bežím 20+ autonómnych agentov so scoped MCP tool accessom, statistickým drift detectionom a auditovateľnými kill switchmi od júla 2026 — mesiace predtým, než ktorýkoľvek z týchto enterprise produktov spustil. Náklad architektúry: nula dodatočných vendor spend. Komplexita architektúry: štyri Linux primitívy (systemd scopes, JSON config file, cron-based monitoring, SQLite audit logy). Kontajnmentový rekord: nula zlyhaní cez 4,000+ hodín agent runtime. Enterprise governance nie je drahý, pretože architektúra je drahá. Je drahý, pretože vendorzy cenná enterprise willingness to pay, nie marginálne náklady enforcementu.
  

  

Keď ServiceNow hovorí "každý AI agent potrebuje pas," nie sú v omylke. Čo nehovoria je, že ten pas môžete issueovať sami — a mali by ste, pretože alternatíva je bežať agentov bez governance vrstvy, ktorú regulátori, klienti a októbrový incident rekord všetky vyžadujú.

  

Otázkou nie je, či vaši agenty potrebujú governance. Je, či stavia te ju predtým, alebo po prvom kontajnment zlyhaní.

  
    

### ☢ Prihláste sa na odber esejí o architektúre agentov
    

Každý príspevok rozoberá, ako vyzerá produkčná agentová infraštruktúra — vzory, zlyhania, architektonické rozhodnutia zo systému, ktorý beží 24/7 mesiace.
    

Prihlásiť sa emailom
    

Žiadny spam. Kedykoľvek sa odhláste.
  

  

🤖 AI-generated | Len informácie | marianstancik.dev/disclaimer

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
