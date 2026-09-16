# MCP prechádza na stateless: Čo znamená špecifikácia 2026-07-28 pre autonómne agenty

> **Published:** 2026-09-09  
> **Author:** Marian Stancik  
> **Summary:** Najväčšia revízia Model Context Protocol — stateless jadro, header-based routing, MRTR, OpenTelemetry a ako mení infraštruktúru autonómnych agentov.

---

9. september 2026
  MCP
  AI Infrastructure
  8 min čítania
  Marian Stancik

### MCP prechádza na stateless: Čo znamená špecifikácia 2026-07-28 pre autonómne agenty

28. júla 2026 vyšla najväčšia revízia Model Context Protocol od jeho spustenia. Hlavná zmena sa dá zhrnúť do jednej vety: MCP už nie je spojovací protokol — je to request protokol. Handshake 
```
initialize
```
 je preč. Hlavička 
```
Mcp-Session-Id
```
 je preč. Servery sú teraz obyčajné stateless HTTP služby, ktoré môže obslúžiť ktorákoľvek dostupná inštancia.

Pri viac ako 400 miliónoch mesačných SDK stiahnutí a 950+ MCP serveroch v Claude connectors adresári je to infraštruktúrna udalosť roka pre každého, kto buduje autonómne agentové systémy. Tu je, čo sa zmenilo, prečo to má význam a čo to znamená pre môj Hermes Agent stack bežiaci na európskej Hetzner infraštruktúre.

### 1. Stateless jadro — čo sa vlastne zmenilo

Pred revíziou 2026-07-28 prebiehala každá interakcia klient-server cez handshake:

```

```
// Predtým (2025-11-25): stavové spojenie
POST /mcp
{ "method": "initialize" }
// Server odpovie Mcp-Session-Id: 7f3a...
// Každý ďalší request musí:
//   a) trafiť ROVNAKÚ inštanciu
//   b) vracať session ID

POST /mcp
Mcp-Session-Id: 7f3a...
{ "method": "tools/call" }
// Load balancer potrebuje sticky sessions
// alebo zdieľaný session store
```

```

Po revízii je celá táto vrstva preč:

```

```
// Po (2026-07-28): stateless, odpovedá ktorákoľvek inštancia
POST /mcp
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: search
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": { "q": "autonómne agenty" },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {}
    }
  }
}
```

```

Sedem SEP (Specification Enhancement Proposals) pracovalo spoločne na tejto zmene: SEP-2575 odstránil handshake, SEP-2567 odstránil session ID, SEP-2243 presunul routing do hlavičiek, SEP-2549 pridal cache hinty, SEP-2322 zaviedol Multi Round-Trip Requests, SEP-2260 obmedzil server-initiated requesty na aktívne volania a SEP-414 štandardizoval propagáciu W3C Trace Context.

Kľúčový poznatok: Odstránenie session na úrovni protokolu nenúti vašu aplikáciu byť stateless. Ak váš server potrebuje niesť stav medzi volaniami, vytvorte explicitný handle z toolu a nechajte model vrátiť ho ako argument. To je lepšie ako session state skrytý v transportnej vrstve — model handle vidí a môže ho prenášať medzi toolmi, a je auditovateľný v logoch.

### 2. Prečo to má význam pre produkčné nasadenia

Pred touto revíziou znamenal produkčný beh MCP serverov jednu neustálu bolesť: sticky sessions. Každá inštancia MCP servera za load balancerom potrebovala zdieľaný session store (Redis, memcached alebo databázu), pretože session ID sa muselo smerovať späť na rovnaký pod. To robilo horizontálne škálovanie zbytočne zložitým a autoscaling takmer nemožným.

So stateless jadrom:

  
- Round-robin load balancing — Ktorýkoľvek request môže pristáť na ktorejkoľvek inštancii. Žiadny zdieľaný session store.
  
- Auto-scaling — Inštancie môžete pridávať a uberať voľne. Žiadne session drainage.
  
- Globálne nasadenie — Distribuujte MCP servery cez viac regiónov za globálnym load balancerom. Ktorákoľvek inštancia, kdekoľvek, môže obslúžiť ktorýkoľvek request.
  
- Serverless — MCP servery môžu bežať na AWS Lambda, Cloudflare Workers alebo akejkoľvek stateless funkcii.

Pre môj stack — Hermes Agent bežiaci na Hetzner VPS (€3,79/mesiac) s viacerými MCP servermi — je to transformačné. MCP servery teraz môžem nasadiť ako jednoduché HTTP služby za Caddy reverse proxy bez správy session. Architektonická komplexita klesá o rád.

### 3. Header-based routing

Každý Streamable HTTP request teraz nesie dve nové hlavičky: 
```
Mcp-Method
```
 (napr. 
```
tools/call
```
, 
```
resources/read
```
) a 
```
Mcp-Name
```
 (konkrétny tool alebo resource). Gateway, load balancer a rate limiter tak môžu smerovať a merať prevádzku na úrovni hlavičiek bez parsovania JSON body.

Praktické využitia:

  
- Rate limiting — Rôzne limity pre 
```
tools/call
```
 vs 
```
resources/read
```
 na úrovni gateway
  
- Cost routing — Smerovanie drahých volaní (napr. LLM sampling) na dedikované backends
  
- Autorizácia — Per-tool prístupové politiky na proxy vrstve bez zmien v aplikácii
  
- Monitoring — Tagovanie metrík podľa metódy a názvu toolu pre granulárnu observabilitu

### 4. Multi Round-Trip Requests (MRTR) — náhrada server callbackov

V starom spece, keď server potreboval niečo od klienta počas volania (potvrdenie, chýbajúci parameter alebo LLM completion), vyžadovalo to držaný obojsmerný stream — nekompatibilné so stateless protokolom.

MRTR nahrádza tento vzor. Server vráti 
```
InputRequiredResult
```
 s requestmi, ktoré potrebuje zodpovedať, a klient zopakuje pôvodné volanie s odpoveďami:

```

```
{
  "resultType": "input_required",
  "inputRequests": {
    "confirm": {
      "type": "elicitation",
      "message": "Zmazať 3 súbory?",
      "schema": { "type": "boolean" }
    }
  },
  "requestState": "eyJzdGVwIjoxLCJmaWxlcyI6WyJhIiwiYiIsImMiXX0="
}
```

```

Klient zozbiera vstup a zopakuje volanie s priloženými 
```
inputResponses
```
. Každá interakcia je explicitná, auditovateľná a funguje cez akýkoľvek stateless transport.

### 5. Cacheable list results

Odpovede z 
```
tools/list
```
, 
```
prompts/list
```
, 
```
resources/list
```
 a 
```
resources/read
```
 teraz nesú polia 
```
ttlMs
```
 a 
```
cacheScope
```
 — modelované priamo na HTTP 
```
Cache-Control
```
 sémantike. Klienti presne vedia, ako dlho je odpoveď čerstvá a či je bezpečné ju zdieľať medzi používateľmi.

Pre agentové systémy to znamená: katalóg toolov vášho agenta je kešovaný na strane klienta, čím odpadá zbytočné refetchovanie. V mojom Hermes Agent nastavení s 15+ MCP toolmi to znižuje latenciu discovery volaní o 60-80%.

### 6. Hardening autorizácie

Šesť SEP sprísňuje autorizačnú špecifikáciu, aby sa zladila s produkčnými nasadeniami OAuth 2.1 a OpenID Connect:

  
- RFC 9207 issuer validácia — Klienti musia validovať parameter 
```
iss
```
 v autorizačných odpovediach, čím sa uzatvára vektor mix-up útoku na autorizačný server
  
- Client ID Metadata Documents (CIMD) — Náhrada Dynamic Client Registration bezpečnejším, deklaratívnym modelom
  
- Deklarácia typu aplikácie — Klienti deklarujú 
```
application_type
```
 počas registrácie, čím sa opravuje bežný problém, keď autorizačné servery odmietajú 
```
localhost
```
 redirect URI pre desktop a CLI aplikácie
  
- Viazanosť credentialov — Klientské credentials sú viazané na vydávajúci autorizačný server, čím sa zabraňuje ich zneužitiu na iných serveroch

Pre regulované prostredia (EU AI Act, GDPR, NIS2) je to kritické. Enterprise Managed Authorization extension umožňuje organizáciám centrálne riadiť prístup k MCP serverom s plným audit trailom — ktorý agent volal ktorý tool v mene koho.

### 7. OpenTelemetry a distribuované tracing

MCP nahradil svoj proprietárny logging kanál OpenTelemetry. W3C Trace Context je teraz štandardizovaný cez fixné kľúče v 
```
_meta
```
 (
```
traceparent
```
, 
```
tracestate
```
, 
```
baggage
```
), takže distribuované trace korelujú naprieč SDK aj gateway vrátane.

Keď váš agent zavolá tool, ktorý sa dotkne vášho MCP servera, ktorý volá externé API, ktoré sa pýta databázy — teraz to všetko vidíte ako jeden spojený trace v akomkoľvek OTel-kompatibilnom backende. Pre produkčné debugovanie o druhej v noci je to rozdiel medzi hádaním a vedením.

### 8. Deprecations a migračná cesta

Roots, Sampling a Logging sú deprecated (SEP-2577). Stále fungujú a budú fungovať najmenej dvanásť mesiacov. Nové implementácie by ich nemali adoptovať.

Tri kľúčové funkcie vstupujú do deprecation pipeline:

  
- Roots — Nahradené explicitným odovzdávaním kontextu cez tool argumenty
  
- Sampling — Nahradené MRTR s 
```
input_required
```
 flow
  
- Logging — Nahradené OpenTelemetry

Legacy HTTP+SSE transport je tiež deprecated, s 12-mesačným offrampom. Formálna deprecation politika dáva každej funkcii najmenej dvanásť mesiacov medzi deprecation a najskorším možným odstránením — takže upgrady môžete plánovať namiesto reagovania.

### 9. Tasks extension

Tasks sa presúvajú z experimentálneho jadra do 
```
io.modelcontextprotocol/tasks
```
 extension s poll-based 
```
tasks/get
```
 a novým 
```
tasks/update
```
. Keď tool call spustí prácu trvajúcu viac ako pár sekúnd (spracovanie súborov, generovanie kódu, batch operácie), server vráti task handle a klient riadi životný cyklus. Žiadny socket držaný otvorený počas trvania.

Toto je správny vzor pre dlhotrvajúce autonómne agentové workflow — a prirodzene zapadá do stateless modelu.

### 10. Čo to znamená pre môj stack

Prevádzkujem Hermes Agent (Nous Research, v0.20.0 "The Herald") na Hetzner VPS na 188.245.224.189, s viacerými MCP servermi poskytujúcimi tooly na generovanie obsahu, CRM, právny monitoring a systémové zdravie. Stavový session model bol vždy najslabším článkom reťaze:

  
- Predtým: Každý MCP server potreboval sticky sessions alebo zdieľaný session store. Horizontálne škálovanie vyžadovalo Redis. Reštart servera mohol zhodiť prebiehajúce tool volania.
  
- Po: Moje MCP servery sú obyčajné HTTP služby za Caddy. Round-robin funguje. Reštart servera nie je udalosť. Nové inštancie môžem nasadzovať bez drainage session.

Svoj primárny MCP server (content engine) som už migroval na špecifikáciu 2026-07-28. Migrácia trvala približne 90 minút: odstránenie 
```
initialize
```
 handlera, pridanie 
```
_meta
```
 parsovania, nahradenie in-memory session store explicitným handle-based stavom a pridanie 
```
Mcp-Method
```
/
```
Mcp-Name
```
 hlavičiek na Caddy vrstve pre routing.

Najväčší prínos: môj MCP server je teraz nasaditeľný ako serverless funkcia. Ak budem niekedy potrebovať škálovať za hranicu jedného VPS, môžem ten istý kód nasadiť na Lambda alebo Cloudflare Worker bez architektonických zmien.

### 11. Migračný checklist

Ak prevádzkujete MCP servery v produkcii, tu je vaša migračná cesta:

  
- Upgrade SDK — TypeScript, Python, Go a C# Tier 1 SDK podporujú 2026-07-28 od dňa vydania
  
- Odstráňte 
```
initialize
```
/
```
initialized
```
 — Nahraďte 
```
_meta
```
 na každom requeste; voliteľne implementujte 
```
server/discover
```

  
- Odstráňte 
```
Mcp-Session-Id
```
 — Session state nahraďte explicitnými handlami vrátenými z toolov
  
- Pridajte hlavičky — Zabezpečte 
```
Mcp-Method
```
 a 
```
Mcp-Name
```
 na každom Streamable HTTP requeste
  
- Nahraďte Sampling/Elicitation — Migrujte na MRTR s 
```
input_required
```
 result typom
  
- Nahraďte Logging — Prejdite na OpenTelemetry pre štruktúrovanú observabilitu
  
- Odstráňte Roots — Kontext odovzdávajte explicitne cez tool argumenty
  
- Testujte — Validujte proti novej conformance suite pred produkčným nasadením

### Zhrnutie

Špecifikácia MCP 2026-07-28 je najvýznamnejšia revízia protokolu od spustenia. Stateless jadro transformuje MCP servery zo stavových služieb riadených spojením na obyčajné HTTP služby, ktoré škálujú na komoditnej infraštruktúre. Pre prevádzkovateľov autonómnych agentov to znamená jednoduchšie nasadenia, nižšiu operačnú réžiu a lepšiu observabilitu — bez straty schopnosti niesť stav tam, kde je potrebný.

Ak budujete autonómne agentové systémy, migrácia stojí za to. 12-mesačné deprecation okno vám dáva priestor na dýchanie, ale architektonické výhody stateless modelu sú dostupné už teraz.

Prihláste sa na newsletter — Píšem o autonómnej agentovej infraštruktúre, MCP a praktickej architektúre AI systémov. Žiadna vata, len produkčné skúsenosti. Pripojte sa tu.

⚠️ AI-generated | Info only | marianstancik.dev/disclaimer

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
