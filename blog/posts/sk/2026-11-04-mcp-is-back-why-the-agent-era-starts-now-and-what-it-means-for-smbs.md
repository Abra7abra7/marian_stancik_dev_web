# MCP sa vrátil: Prečo práve teraz začína éra agentov — a čo to znamená pre slovenské SME

> **Published:** 2026-11-04  
> **Author:** Marian Stancik  
> **Summary:** MCP Registry prekročil 47 879 serverov (40-násobný rast za 10 mesiacov) a špecifikácia z 28. 7. 2026 urobila protokol stateless a produkčne zrelým. Kým podniky nasadzujú agentov, slovenské SME sú na ~5 % adopcii AI. Prečo začína éra agentov teraz — a ako sa dostať od nuly k prvému agentovi v 3 krokoch.

---

4. november 2026
  AI Agents
  4 min čítania
  Marian Stancik

### MCP sa vrátil: Prečo práve teraz začína éra agentov — a čo to znamená pre slovenské SME

### Číslo, ktoré by malo zobudiť každého podnikateľa

21. októbra 2026 prekročil oficiálny MCP Registry hranicu 47 879 serverov — oproti 1 204 na konci roka 2025. To je 40-násobný rast za desať mesiacov. Dve tretiny serverov dnes ponúkajú vzdialený endpoint, čo znamená, že to nie sú ukážkové príklady v README, ale služby, ktoré firmy reálne volajú cez sieť.

Čísla z npm hovoria to isté. Oficiálny TypeScript SDK (
```
@modelcontextprotocol/sdk
```
) vzrástol z 31,3 milióna stiahnutí v septembri 2025 na 231,9 milióna v septembri 2026 — medziročne 7,4-násobok. Naprieč všetkými SDK prvej kategórie projekt MCP počíta mesačne takmer pol miliardy stiahnutí.

Toto je návrat, ktorý nikto neplánoval: po „MCP je len hype" vlne z začiatku roka 2026 protokol nezmizol. Stal sa nudným a produkčne zrelým — a presne preto začína éra agentov teraz.

### Prečo „backlash" minul pointu

Koncom roka 2025 a začiatkom 2026 MCP odpísalo veľa múdrych ľudí. Sťažnosti boli oprávnené: protokol bol ukecaný, SDK mladé, každá demo ukážka sa pripájala na API s počasím a „MCP server" sa stal vtipom o wrappery okolo jedného volania.

Čo si kritici nevšimli: protokol nie je produkt, je to zmluva. Ekosystém spravil to, čo ekosystémy robia — ponechal zmluvu a vymenil všetko okolo nej. Decembrové odovzdanie MCP do Linux Foundation's Agentic AI Foundation (spoluzakladatelia Anthropic, Block a OpenAI, podpora od Google, Microsoft, AWS, Cloudflare a Bloomberg) definitívne vyriešilo otázku vládnutia. Žiadny jeden vendor už štandard nemôže zlomiť.

Potom dospel aj samotný protokol. Špecifikácia z 28. júla 2026 zrušila 
```
initialize
```
 handshake a hlavičku 
```
Mcp-Session-Id
```
 — jadro je teraz stateless, s multi round-trip requestami (MRTR) a routovaním cez hlavičky (
```
Mcp-Method
```
, 
```
Mcp-Name
```
). Stateless znamená triviálne škálovateľné serverless nasadenia: zapnite MCP endpoint, hoďte naň záťaž, žiadny session state na správu. Amazon Bedrock AgentCore to podporuje natívne. OpenAI, Google DeepMind a Microsoft to majú štandardne zapnuté. Enterprise roadmap pridáva OAuth 2.1, audit trail a gateway správanie — presne tie nudné veci, ktoré odlišujú demo od infraštruktúry.

Pointa: 66 % aktívnych MCP serverov dnes beží na vzdialených endpointoch, Forrester predpovedá, že v roku 2026 bude 30 % enterprise vendorov prevádzkovať vlastné MCP servery, a trh s MCP mal v roku 2025 hodnotu 1,2 mld. USD s projektovaným rastom 37,2 % ročne do roku 2035. Protokol vyhral — nie tým, že bol sexy, ale tým, že bol jedinou otvorenou zmluvou, na ktorej sa všetci zhodli.

### Medzitým sa priepasť zväčšuje

A tu prichádza nepríjemná časť. Kým podniky nasadzujú flotily agentov a protokolová infraštruktúra sa stáva stateless a remote-first, väčšina slovenských SME stále vníma AI ako chatbot. Country Report Európskej komisie k Digital Decade uvádza adopciu AI na Slovensku na úrovni približne 5 % — oproti európskemu priemeru okolo 8 %. Za všetkým stojí obvyklý podozrivý, nedostatok zručností, a krajina má na jeho riešenie alokovaných 1,2 mld. EUR digitálnych prostriedkov.

Stretávam majiteľov firiem, ktorí nikdy nepracovali s API a ktorí si myslia, že „integrácia" je niečo, čo za nich spraví vendor za prihlasovacou stránkou. Éra agentov to nerieši. Odmeňuje firmy, ktoré vedia svoje dáta a procesy sprístupniť ako volateľné služby — a trestá tie, ktoré to nevedia, pretože agentové nástroje sa stavajú na rozprávanie so službami, nie s ľuďmi vo webových formulároch.

Dobrá správa: nemusíte sa najprv stať softvérovou firmou. Cesta od nuly k prvému fungujúcemu agentovi má tri kroky a prvý z nich máte zvyčajne z 80 % hotový.

### Od nuly k prvému agentovi v 3 krokoch

Použijem konkrétny príklad slovenskej malej firmy: podnik, ktorý chce agenta na odpovedanie zákazníckych otázok o stave objednávky. Rovnaký vzor platí pre faktúry, sklad, konzultácie — čokoľvek.

### Krok 1 — Sprístupnite jeden endpoint (túto časť už máte)

Dáta takmer určite máte. Potrebujete jediný HTTP endpoint, ktorý ich vráti v štruktúrovanej podobe. Najmenšia užitočná verzia:

```
# order_status.py — minimálny read-only endpoint (FastAPI)
from fastapi import FastAPI
app = FastAPI()

ORDERS = {"OBJ-1001": "shipped", "OBJ-1002": "in warehouse", "OBJ-1003": "paid"}

@app.get("/api/order/{order_id}")
def order_status(order_id: str):
    return {"order_id": order_id, "status": ORDERS.get(order_id, "unknown")}
```

To je celá integračná zmluva. Nepotrebujete OAuth, dashboard ani zákaznícky portál. Jeden endpoint na jeden proces.

### Krok 2 — Zabaľte ho ako MCP server (nová štandardná vrstva)

Teraz endpoint sprístupnite akémukoľvek AI agentovi. S oficiálnym Python SDK je to zámerne malé:

```
# mcp_order_server.py — endpoint ako MCP nástroj
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("order-status")

@mcp.tool()
def get_order_status(order_id: str) -> str:
    r = httpx.get(f"https://api.example.sk/api/order/{order_id}").json()
    return f"Order {r['order_id']} is {r['status']}."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

Jeden Python súbor. Agent — Claude, Gemini, vaša vlastná orchestračná vrstva, akýkoľvek klient, ktorý hovorí MCP — tento nástroj objaví, prečíta jeho schému a zavolá ho, keď otázka zákazníka sedí. Už nestaviate samostatnú integráciu pre každého AI vendora; postavíte ju raz a dostane ju každý agent kompatibilný s MCP.

### Krok 3 — Pripojte agenta (a nechajte človeka v slučke)

Posledný krok je konfigurácia, nie kód:

```
# agent_config.json — pripojenie klienta k MCP serveru
{
  "mcpServers": {
    "order-status": {
      "url": "https://api.example.sk/mcp/order-status",
      "auth": {"scheme": "bearer", "env": "MCP_TOKEN"}
    }
  }
}
```

Od tohto momentu agent vie skontrolovať stav objednávky, eskalovať hraničné prípady človeku, logovať každé volanie a — keď pridáte write endpoint — aj aktualizovať záznamy s vaším schválením. To je celý trik: agent je volateľná služba plus slučka a MCP je jediné rozhranie, ktoré oboje pripája k akémukoľvek modelu.

### Čo reálne prevádzkujem

Toto nepíšem z teórie. Od roku 2025 moja produkčná architektúra — Hermes Agent od Nous Research — beží na tomto presnom vzore na VPS od Hetznera za 6 €/mesiac: Telegram gateway, SQLite pamäťová vrstva, multi-LLM routovanie cez OpenRouter a sada cron agentov, ktorí publikujú obsah, strážia servery a udržiavajú digitálne dvojča môjho vlastného vývoja. Devätnásť agentov, 24/7, pod jednou MCP zmluvou, na ktorej dnes stoja aj enterprise stacky.

Poučenie z každodenného behu: model je vymeniteľný, protokol nie. Pod tými istými MCP serverami som vymenil modely viackrát, než stíham počítať — nástroje, pamäť a povolenia sa nikdy nezmenili. To je architektonický argument pre MCP v jednej vete: oddeľuje vaše dáta a procesy od toho, kto náhodou vyrába najlepší model túto štvrťrok.

### Prečo je to aj compliance príbeh

Slovenské firmy nemôžu ignorovať ani regulačnú vrstvu. Článok 50 AI Aktu EÚ — transparentnosť AI-generovaného obsahu a interakcií s AI — je vynútiteľný od 2. augusta 2026 a nové zákazy deepfake platia od 2. decembra 2026. Najprísnejšie high-risk pravidlá sa posunuli na december 2027, čo kupuje čas — ale nie naveky.

Praktický dôsledok: firmy, ktoré stavajú agentov teraz, budú mať vzory governance, logovania a ľudského dohľadu pripravené, keď high-risk povinnosti prídu. Tie, ktoré čakajú, budú hasiť. Audit-trail smer MCP a oprávnenia na úrovni nástrojov sa pritom nápadne podobajú na to, čo budú regulátori pýtať — štandardné rozhrania robia compliance overiteľnou namiesto improvizácie.

Môj názor: éra agentov nezačína stadiónovou keynote ani predplatným za 500 $ mesačne. Začína tým, že jedna malá firma sprístupní jeden endpoint, zabalí ho do jedného MCP servera a deleguje jednu opakovanú úlohu niečomu, čo pracuje cez deň aj v noci. Zopakujte to trikrát a ste pred väčšinou firiem v krajine.

Ak prevádzkujete slovenské SME a chcete vidieť, ako by vyzeral váš prvý agent — ktoré procesy sa oplatí sprístupniť, koľko to stojí a ako zostať v súlade s reguláciou — ponúkam bezplatnú konzultáciu prvým piatim firmám, ktoré si ju zarezervujú. Detaily sú na mojej kontaktnej stránke; žiadny záväzok, žiadna prezentácia, len vaše reálne dáta a na konci funkčný prototyp.

Prihláste sa na newsletter pre technické hlboké ponory — jeden e-mail týždenne o agentovej architektúre, EU AI Act compliance a tom, čo nasadzujem do produkcie.

⚠️ AI-generated | Info only | marianstancik.dev/disclaimer

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
