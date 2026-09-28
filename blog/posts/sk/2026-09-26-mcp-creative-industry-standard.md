# Ako sa MCP stal univerzálnym konektorom pre AI agentov po SIGGRAPH 2026

**Published:** 26. september 2026 | **Author:** Marian Stancik

---

20. júla 2026 na konferencii SIGGRAPH v Los Angeles urobila NVIDIA niečo, čo zásadne zmenilo infraštruktúru AI agentov. Oznámila, že Adobe, Blender, Unreal Engine, SideFX Houdini, Boris FX Silhouette, Foundry Nuke a Affinity od Canva otvárajú Model Context Protocol (MCP) spojenia, aby AI agenty mohli pracovať priamo v ich nástrojoch. Nie prototypy. Nie výskumné práce. Kompletné MCP servery, ktoré agenty môžu volať dnes.

Toto nebolo uvedenie produktu. Bol to štandardizačný moment. Počas jedného keynote prešiel MCP z "protokolu, ktorý Anthropic predstavil na prepojenie jazykových modelov s nástrojmi" na priemyselný štandard pre interakciu AI agentov s profesionálnym kreatívnym softvérom — a v dôsledku toho s akoukoľvek aplikáciou, ktorá vystavuje scriptingové API.

Prevádzkujem Hermes Agent (Nous Research) so sadou vlastných MCP serverov — filesystem, databáza, webové vyhľadávanie, CRM integrácia, terminálový prístup — 24/7 na Hetzner VPS. Staviam na MCP už od čias pred stateless revíziou 2026-07-28. To, čo SIGGRAPH 2026 dokázal, je, že táto architektonická stávka nebola len správna — bola nevyhnutná. Každá aplikácia sa stáva agent-ready a MCP je konektor, na ktorom sa štandardizujú.

**Hlavný záver:** Po SIGGRAPH 2026 už MCP nie je voľba protokolu. Je to predvolený konektor pre AI agentov v kreatívnom priemysle. Ak staviáš AI agentov, ktorí interagujú s externými nástrojmi — kreatívnymi alebo inými — MCP je štandard, na ktorom by si mal stavať.

## Čo sa vlastne stalo na SIGGRAPH 2026

NVIDIA keynote, ktorú viedli Neil Ashton, Edward Liu a Ming-Yu Liu s úvodným rámcom od Jensena Huanga, bola postavená na troch pilieroch: fyzikálne AI world modely (Cosmos 3 Edge), dôvera v syntetické médiá (Synthetic Video Detector NIM) a agentické kreatívne nástroje (MCP naprieč ekosystémom). Tretí pilier dostal najviac pozornosti, pretože priamo mení spôsob, akým budú fungovať umelci, technickí riaditelia a štúdiové pipeliny.

Tu je kompletná mapa partnerov a toho, čo na SIGGRAPH 2026 vyšlo:

| **Aplikácia** | **MCP rozhranie** | **Čo agenty dokážu** 

| Adobe Creative Cloud | Firefly kreatívny agent; Express MCP Server | Multi-krokové workflow naprieč Firefly, Express, Creative Cloud; tvorba Express doplnkov 

| Blender (Blender Lab) | Ľahký MCP server | Prirodzený jazyk na Python API, dokumentáciu a komplexné nastavenia 

| Unreal Engine | Editor MCP spojenie | Ovládanie editora — scény, assety, projektový stav 

| SideFX Houdini 22 | APEX Script MCP server | Generovanie a dolaďovanie procedurálneho rig kódu 

| Boris FX Silhouette | MCP server + FX Scripting API | Inšpekcia projektov, node tree, tvary a keyframes; online aj headless režim 

| Foundry Griptape | Natívna MCP orchestrácia | Multi-model VFX pipeliny cez Blender + Nuke 

| Affinity by Canva | AI konektor pre Claude cez MCP | Premenovanie vrstiev, zmena veľkosti artboardov, dávkové úpravy 

| NVIDIA Agent Toolkit | MCP klient + MCP server | Pripojenie k vzdialeným MCP serverom; publikovanie vlastných nástrojov 

NVIDIA tiež oznámila, že Hermes Agent (Nous Research) — systém, ktorý prevádzkujem v produkcii — pridal Blender do svojho MCP katalógu, spolu s NVIDIA Agent Toolkit MCP klientom a serverom. Toto nie je okrajová poznámka: znamená to, že agent runtime, ktorý používam, má teraz priamy MCP vstup do profesionálnych 3D a VFX nástrojov.

## Prečo MCP vyhral: Dizajn protokolu, ktorý to umožnil

MCP sa nestal štandardom, pretože mal najlepší marketing. Stal sa ním, pretože jeho protokolový dizajn presne mapuje to, čo kreatívny softvérový priemysel potrebuje: štandardizovaný spôsob, ako vystaviť scriptingové API ako sadu volateľných nástrojov s typovanými vstupmi a výstupmi, objaviteľných za behu a nezávislých od transportnej vrstvy.

Tri dizajnové rozhodnutia umožnili vlnu adoptácie na SIGGRAPH:

### 1. Objavovanie nástrojov cez server/discover

Revízia 2026-07-28 zaviedla `server/discover` — stateless endpoint, ktorý vráti kompletný manifest nástrojov MCP servera v jednom volaní. Predtým museli klienti vyjednávať schopnosti cez viackrokový inicializačný handshake. Teraz môže každý agent poslať jednu požiadavku a dostať kompletný zoznam dostupných nástrojov s JSON Schema 2020-12 špecifikáciami. To je kľúčové pre kreatívne aplikácie, pretože plocha nástrojov je obrovská (Blenderovo Python API vystavuje stovky funkcií) a dynamická (pluginy pridávajú nástroje za behu).

### 2. JSON Schema 2020-12 pre vstupné a výstupné parametre

Každý vstup a výstup MCP nástroja je špecifikovaný ako plná JSON Schema. To nie je implementačný detail — je to vlastnosť, ktorá umožňuje kreatívnym aplikáciám vystavovať komplexné dátové štruktúry (scény, node stromy, animačné krivky, 3D mesh údaje) s presnou typovou validáciou, bez toho aby agent potreboval poznať internú schému každej aplikácie.

### 3. Nezávislosť na transporte (stdio + HTTP/SSE)

MCP funguje cez stdio (lokálna komunikácia agent ↔ nástroj na rovnakom stroji) a HTTP so Server-Sent Events (vzdialená komunikácia). Tento duálny transport je enormne dôležitý pre kreatívne štúdiá: lokálne MCP servery bežia na workstation pre nízku latenciu, zatiaľ čo vzdialené MCP servery spracúvajú dávkové operácie na render farmách.

`# Výber MCP transportu — rovnaký server, iné nasadenie
# Lokálna workstation (interaktívna, nízka latencia)
mcp_server = MCPServer(
    name="blender-lab",
    transport="stdio",
    command="blender --background --python mcp_server.py"
)

# Cloud render farma (dávkové, asynchrónne)
mcp_server = MCPServer(
    name="blender-lab-farm",
    transport="http",
    endpoint="https://renderfarm.internal/mcp/blender",
    headers={"Authorization": "Bearer $(cat /run/secrets/mcp_token)"}
)`

## Čo to znamená pre autonómnu architektúru agentov

Po SIGGRAPH 2026 sa MCP server už nepovažuje za vlastnú infraštruktúru. Pred SIGGRAPH ste MCP servery stavali sami. Pre kreatívnu a produktívnu vrstvu sú teraz MCP servery dodávané priamo výrobcami aplikácií. Blender Lab dodáva MCP server. Boris FX dodáva MCP server. NVIDIA Agent Toolkit dodáva MCP klienta aj server.

Pre môj stack to znamená, že agent, ktorý predtým volal 5-10 vlastných MCP serverov, môže teraz volať Blenderovo plné Python API, schopnosti Unreal Engine editora, Houdiniho APEX Script a celú Adobe Creative Cloud sadu — všetko cez rovnaký protokol, rovnaký autentifikačný vzor a rovnaké spracovanie chýb.

**Poznámka z produkcie:** Nie všetky tieto MCP servery som ešte integroval do svojho produkčného stacku. Ale architektonická plocha je pripravená. Ktorýkoľvek z mojich Hermes agentov môže byť nasmerovaný na ktorýkoľvek MCP server a okamžite začať volať nástroje, pretože MCP štandardizuje spojenie — nie špecifické API nástroja.

## Tri praktické kroky pre staviteľov MCP serverov

Ak prevádzkuješ MCP servery — či už pre biznis nástroje, kreatívne pipeliny alebo osobnú automatizáciu — vlna adopcie po SIGGRAPH 2026 znamená, že by si mal spraviť tri veci:

### 1. Prejdi na stateless core 2026-07-28

Stateless revízia je povinná pre interoperabilitu s novým ekosystémom. Vendorské MCP servery dodávajú stateless core. Ak tvoje vlastné servery stále používajú starý initialize handshake a session hlavičky, nezaregistrujú sa v rovnakom katalógu nástrojov ako Adobe server alebo Blender server.

### 2. Implementuj server/discover

Toto je endpoint, ktorý každý MCP klient volá po pripojení. Vracia kompletný manifest nástrojov. Bez neho je tvoj server neviditeľný pre agentov, ktorí používajú štandardný discovery flow.

### 3. Priprav duálny transport (lokálny + vzdialený)

Kreatívne MCP servery potrebujú bežať lokálne (nízka latencia, žiadna cloudová závislosť) aj vzdialene (dávkové spracovanie, render farmy). Ak tvoj MCP server podporuje len stdio, pridaj HTTP transport.

## Čo príde ďalej

Najdôležitejšia veta z NVIDIA SIGGRAPH keynote nebola o žiadnom konkrétnom produkte: "Aplikácie nie sú len rýchlejšie — stávajú sa agent-ready." Toto rámcovanie posúva úlohu architekta AI agentov z "postav nástroje, ktoré tvoji agenti potrebujú" na "pripoj svojich agentov k nástrojom, ktoré priemysel už postavil."

Pre môj produkčný systém je najbližším krokom integrácia Blender Lab MCP servera do môjho content pipeline — agent, ktorý dokáže autonómne generovať 3D vizualizácie pre blogové príspevky, používajúc rovnaký MCP protokol a guardian policy vrstvu, ktorú môj blog publisher používa na písanie textu.

Control plane sa nemení. Audit trail sa nemení. Mení sa len MCP server.

To je pointa štandardizovaného konektora. Zapojíš iný nástroj a všetko ostatné zostáva rovnaké.

`MCP ako univerzálny konektor po SIGGRAPH 2026 — Sumár
────────────────────────────────────────────────────────────
Pred SIGGRAPH:   Vlastné MCP servery na všetko
Po SIGGRAPH:     Vendorské MCP servery + vlastné MCP servery
                 Rovnaký protokol, rovnaký guardian, rovnaký audit trail

Ekosystém:       7 veľkých kreatívnych vendorov dodáva MCP servery
Hardvér:         Lokálne (DGX Station) + vzdialené (VPS) cez duálny transport
Štandard:        2026-07-28 stateless core s server/discover
Dopad na agentov: Laterálne škálovanie — žiadny nový integračný vzor na nástroj
────────────────────────────────────────────────────────────
`

&#x1f916; AI-generated | Info only | [marianstancik.dev/disclaimer](/disclaimer)

---

*⚠️ AI-generated | Info only | marianstancik.dev/disclaimer*
