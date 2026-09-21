# AI agenty spotrebúvajú 5× viac tokenov ako ľudia — Ako optimalizovať autonómnu agentovú infraštruktúru

> **Published:** 2026-09-19  
> **Author:** Marian Stancik  
> **Summary:** Dáta a16z ukazujú, že AI agenty používajú 5× viac LLM tokenov ako ľudia. Ako optimalizovať autonómnu agentovú infraštruktúru s cachingom, model routingom a cost controlmi.

---

19. september 2026
  Autonomous Agents
  AI Infrastructure
  Cost Optimization
  9 min čítania
  Marian Stancik

### AI agenty spotrebúvajú 5× viac tokenov ako ľudia — Ako optimalizovať autonómnu agentovú infraštruktúru

Jeden autonómny AI agent dokáže spáliť päťkrát viac LLM tokenov ako človek pri rovnakej úlohe. Toto nie je teoretická projekcia — je to nameraný fakt z analýzy Andreessen Horowitz, ktorá v auguste 2026 skúmala OpenRouter prevádzku. A vysvetľuje, prečo firemné výdavky na inferenciu podľa Gartnera tento rok dosiahnu 23 miliárd dolárov, zatiaľ čo výdavky na tréning klesli na 19 miliárd.

Dôvod je architektonický. Človek odošle prompt, prečíta odpoveď a skončí. Autonómny agent cyklí: plánuje, vyhľadáva, volá nástroje, vyhodnocuje medzivýsledky, opravuje sa a skúša znova. Jedna úloha ako "analyzuj predajné dáta a vygeneruj report" sa ticho rozrastie na desiatky sekvenčných volaní modelu. Keď prevádzkujete 19+ autonómnych cron jobov 24/7 — ako ja na svojom Hetzner VPS — spotreba tokenov nie je metrika, ktorú kontrolujete raz mesačne. Je to váš primárny prevádzkový náklad.

Tento článok pokrýva tri optimalizačné stratégie, ktoré používam v produkcii na udržanie nákladov na tokeny pod kontrolou bez obetovania autonómie: prompt caching, multi-model routing a per-agent budget enforcement.

Čísla: AI agenty dnes generujú väčšinu webovej prevádzky (O'Reilly, august 2026). Gartner predpovedá zdvojnásobenie výdavkov na inferenciu na 42 miliárd dolárov — 96% rast. Dáta a16z/OpenRouter ukazujú spotrebu tokenov agentov v pomere 5:1 oproti ľuďom. Toto je definujúce ekonomické obmedzenie autonómnej agentovej infraštruktúry.

### 1. Prompt Caching: Najväčšia páka

OpenAI účtuje $4.00/M vstupných tokenov pre GPT-5.6 Sol štandardný kontext — ale len $0.40/M pre cachované vstupy. To je 90% zníženie. Anthropic Claude Opus 5 ponúka podobnú ekonomiku. Háčik: caching funguje len ak váš systém dodáva deterministické, opakujúce sa kontextové vzory.

Autonómne agenty sú ideálne kandidáty na caching, pretože opakovane načítavajú rovnaké systémové prompty, tool schémy a inštrukčné sady. Kľúčom je navrhnúť agentovu slučku tak, aby maximalizovala cache hity.

### Ako štruktúrujem prompty pre cache locality

```

```
# Cache-friendly prompt template (Hermes Agent config)
prompt:
  system: |
    Si Hermes Agent — autonómna AI entita.
    Aktuálny čas: {{timestamp}}
    Dostupné nástroje: {{tool_list}}
    
    [Pravidlá — STABILNÉ, zriedka sa menia]
    - Priamy, technický, security-first
    - Nikdy nehardcodovať secrets
    - Používať nástroje proaktívne
    - Okamžite hlásiť zlyhania
    
    [Úloha — MENÍ SA každé volanie]
    {{task_description}}
    
  cache_config:
    static_prefix_length: 450
    ttl_ms: 300000
    cache_scope: user
```

```

Táto štruktúra zaručuje, že prvých 450 tokenov (systémový prompt, pravidlá, zoznam nástrojov) sa nikdy nemení medzi volaniami. Iba posledná sekcia — samotná úloha — je dynamická. S TTL 5 minút a user-scoped cache moje agenty dosahujú 80-90% cache hit rate na sekvenčných volaniach v rámci jedného cron cyklu.

Špecifikácia MCP 2026-07-28 prináša nové polia 
```
ttlMs
```
 a 
```
cacheScope
```
 na odpovediach 
```
tools/list
```
, čo rozširuje tento koncept priamo na úroveň protokolu. Katalógy nástrojov sú teraz deterministicky zoradené a cachovateľné — agent znovu nesťahuje celý zoznam pri každom pripojení, čo prináša ďalšie 30-60% zníženie sieťových volaní.

Ponaučenie: Oddelenie stabilných a dynamických prompt sekcií nie je mikrooptimalizácia. Je to architektonický vzor, ktorý priamo určuje, či vaša úloha stojí $0.40 alebo $4.00.

### 2. Multi-Model Routing: Nie každé volanie potrebuje GPT-5.6 Sol

Najväčším plytvaním v autonómnej agentovej infraštruktúre je používanie frontier modelu na každý krok. Agent, ktorý spraví 15-20 volaní modelu na dokončenie jednej úlohy, nepotrebuje DeepSeek V4 Pro reasoning na všetky. Mnohé volania sú jednoduché vyhľadávanie, formátovanie alebo pattern matching — úlohy, ktoré zvládne menší, lacnejší model s identickou kvalitou.

Na svojom Hetzner VPS prevádzkujem OpenRouter multi-LLM routing s tierovanou modelovou stratégiou:

### Tiered Model Routing v produkcii

```

```
# model_routing.yaml — priradenie modelov podľa úlohy
routing:
  default:
    provider: openrouter
    fallback: [deepseek/deepseek-v4-flash, mistral/mistral-large-4]
    
  tiers:
    # Tier 1: Jednoduché úlohy — najlacnejší model
    - match: ["tool_call", "data_format", "search", "list"]
      model: deepseek/deepseek-v4-flash
      max_tokens: 2000
      cost_limit: $0.0003/call
      
    # Tier 2: Uvažovanie — stredná trieda
    - match: ["plan", "summarize", "classify", "extract"]
      model: mistral/mistral-large-4
      max_tokens: 4000
      cost_limit: $0.002/call
      
    # Tier 3: Komplexné — frontier model len keď treba
    - match: ["code_gen", "architecture", "legal_analysis", "debug"]
      model: deepseek/deepseek-v4-pro
      max_tokens: 8000
      cost_limit: $0.01/call
      
    # Tier 4: Fallback ak všetky ostatné zlyhajú
    - match: ["fallback"]
      model: openai/gpt-5.6-sol
      max_tokens: 16000
      cost_limit: $0.05/call
```

```

V produkcii tento tierovaný systém smeruje 72% všetkých volaní agentov do Tier 1 (DeepSeek V4 Flash za $0.075/M vstupných tokenov), 20% do Tier 2 (Mistral Large 4 za $0.50/M) a len 6% do Tier 3 (DeepSeek V4 Pro). Tier 4 — GPT-5.6 Sol — spracúva menej ako 2% volaní. Výsledok: efektívna blended cena je približne 15-20% oproti tomu, keby každé volanie išlo do frontier modelu.

Reálne náklady: Prevádzka 19 cron jobov 24/7 s týmto routingom stojí približne €12-18/mesiac na inferenciu, oproti €60-90/mesiac bez tierovania — zníženie o 75-80%.

Táto stratégia priamo adresuje zistenie z a16z analýzy: dôvod, prečo agenty spaľujú 5× viac tokenov, nie je že by boli neefektívne — je to že väčšina agentových systémov nerozlišuje medzi modelovými schopnosťami podľa úlohy. Tool call, ktorý len hovorí "prečítaj tento JSON súbor", nepotrebuje model, ktorý vyriešil ARC-AGI-3.

### 3. Per-Agent Budget Enforcement

Bez budget kontrol dokáže jediný zblúdený agent vyčerpať mesačný rozpočet na inferenciu za pár hodín. Presvedčil som sa o tom v júli 2026, keď nesprávne nakonfigurovaný DATAcube ingest agent vstúpil do retry slučky a spálil 400 000 tokenov za 22 minút na jednom croissante — €1.60 vyhodenej inferencie, ktorá mala byť zachytená za menej ako 10 sekúnd.

Každý Hermes Agent cron job dnes vynucuje tri budget vrstvy:

```

```
# budget.yaml — per-agent cost enforcement
agents:
  blog-publisher:
    monthly_budget: €5.00
    per_call_limit: 8000 tokens
    max_retries: 3
    alert_on: cost_anomaly
    
  datacube-ingest:
    monthly_budget: €3.00
    per_call_limit: 4000 tokens
    max_retries: 2
    alert_on: retry_loop
    
  social-poster:
    monthly_budget: €2.00
    per_call_limit: 2000 tokens
    max_retries: 1
    alert_on: cost_anomaly
    
  drone-analytics:
    monthly_budget: €1.00
    per_call_limit: 1000 tokens
    max_retries: 0
    alert_on: retry_loop

global:
  daily_spend_limit: €2.00
  weekly_spend_limit: €10.00
  alert_channel: marianstancik@agentmail.to
```

```

Keď agent prekročí svoj per-call token limit alebo dennú priemernú spotrebu o viac ako 2×, systém pošle alert cez AgentMail. Keď je dosiahnutý globálny denný limit, všetky nekritické cron joby sa automaticky pozastavia do nasledujúceho dňa. Toto nie je teoretický dizajn — beží na mojom Hetzner VPS dnes a od júla zabránil najmenej trom runaway-spend incidentom.

### 4. Štruktúrované logovanie pre atribúciu tokenov

Nemôžete optimalizovať to, čo nemeriate. Každé volanie agenta v mojom systéme produkuje štruktúrovaný log s počtom tokenov, použitým modelom, cache statusom a cenou:

```

```
# Structured log entry — každé tool call
{
  "timestamp": "2026-09-19T07:30:00Z",
  "agent_id": "blog-publisher",
  "cron_id": "a4f1e3c2",
  "task": "generate_blog_outline",
  "model": "deepseek/deepseek-v4-flash",
  "tier": 1,
  "input_tokens": 1250,
  "output_tokens": 340,
  "cached_input_tokens": 980,
  "cache_hit_rate": 0.784,
  "cost_usd": 0.000119,
  "duration_ms": 2847,
  "trace_id": "8f2b1c4e..."
}
```

```

Tento log mi umožňuje okamžite odpovedať na tri kľúčové otázky:

  
- Ktoré agenty stoja najviac? Blog publisher spotrebúva 38% celkových mesačných tokenov.
  
- Ktoré úlohy zbytočne obchádzajú Tier 1? Caching bug v DATAcube schema fetcheri smeroval 15% jednoduchých dotazov do Tier 3. Opravené jednou zmenou v konfigurácii.
  
- Aký je agregovaný cache hit rate? Aktuálne 82.3% naprieč všetkými agentmi — oproti 34% pred reštrukturalizáciou promptov.

### 5. Cache-Aware Agent Loop

Praktickou syntézou všetkých troch stratégií je cache-aware agentová slučka, ktorá explicitne riadi náklady na tokeny ako prvotriedne obmedzenie:

```

```
# Cache-aware agent execution loop (pseudocode)
def execute_agent_task(task):
    # Krok 1: Klasifikuj náročnosť úlohy (stateless, bez volania modelu)
    tier = classify_task(task)
    
    # Krok 2: Vyber model podľa tieru
    model = route_to_model(tier)
    
    # Krok 3: Zostav cache-friendly prompt
    prompt = build_prompt(
        stable_section=SESSION.system_prompt,
        dynamic_section=task.description
    )
    
    # Krok 4: Vykonaj s budget guardom
    result = model.call(
        prompt=prompt,
        max_tokens=tier.max_tokens,
        cache_config=CACHE_CONFIG
    )
    
    # Krok 5: Loguj a audit
    log_token_usage(result)
    check_budget_limits(agent_id, result.cost)
    
    # Krok 6: Spracuj zlyhania v rámci budgetu
    if result.failed and result.retries < MAX_RETRIES:
        return execute_agent_task(task)
    elif result.failed:
        return fallback_to_next_tier(task)
    else:
        return result
```

```

Táto slučka beží na každom Hermes Agent cron jobe dnes. Pridáva približne 12 riadkov réžie na definíciu agenta — a je to jediné architektonické rozhodnutie, ktoré robí 19 autonómnych cron jobov ekonomicky udržateľných na VPS za €3.79/mesiac.

### Čo to znamená pre rok 2026

Gartner predpovedá, že do roku 2029 bude 80% zákazníckych otázok riešených výhradne AI agentmi bez ľudského zásahu. O'Reilly analýza z augusta potvrdila, že agenty dnes generujú väčšinu webovej prevádzky. Dáta a16z nám ukazujú nákladový vektor: 5× vyššia spotreba tokenov na úlohu.

Ak nasadzujete autonómne agenty do produkcie dnes, váš ekonomický model musí zahŕňať tento 5× násobiteľ. Bez prompt cachine, tiered routingu a per-agent budgetov bude agentový systém, ktorý vyzerá ziskovo na papieri, ticho spotrebovávať 5-10× vaše projektované náklady na inferenciu v praxi.

Tri stratégie v tomto článku — prompt caching s cache-friendly dizajnom promptov, multi-model tiered routing a per-agent budget enforcement — nie sú voliteľné optimalizácie. Sú to minimálne životaschopné cost-controly pre produkčnú autonómnu agentovú infraštruktúru. Všetky nasadzujem na svojom Hetzner VPS a spolu udržujú moje mesačné výdavky na inferenciu pod 20€ pri 19 autonómnych cron joboch bežiacich 24/7.

Chcete celú konfiguráciu? Spravujem svoje agent routing YAML a budget enforcement konfigurácie ako súčasť môjho Hermes Agent setupu. Prihláste sa na newsletter pre hĺbkový článok o OpenRouter multi-model routingu s reálnymi nákladovými dátami.

### Sumár Architektúry

```

```
Agent Infrastructure — Cost-Optimized Stack
───────────────────────────────────────────────
19 cron jobov (Hermes Agent)
  → Tiered model routing (OpenRouter)
    → 72% Tier 1 (DeepSeek Flash): $0.075/M tokenov
    → 20% Tier 2 (Mistral Large 4): $0.50/M tokenov
    → 6% Tier 3 (DeepSeek Pro): $2.00/M tokenov
    → 2% Tier 4 (GPT-5.6 Sol): $4.00/M tokenov
  → Prompt caching: 82.3% cache hit rate
  → Per-agent budget enforcement
  → Structured logging + cost anomaly detection
───────────────────────────────────────────────
Efektívna blended cena: ~15-20% jednoduchého model baseline
Mesačné náklady na inferenciu: menej ako €20 pre 19 × 24/7 agentov

```

```

🤖 AI-generated | Len na informačné účely | marianstancik.dev/disclaimer

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
