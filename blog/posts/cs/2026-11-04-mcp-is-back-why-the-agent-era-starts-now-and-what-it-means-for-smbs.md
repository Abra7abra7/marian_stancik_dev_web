# MCP se vrací: Proč éra agentů začíná právě teď — a co to znamená pro malé a střední podniky

> **Published:** 2026-11-04  
> **Author:** Marian Stancik  
> **Summary:** MCP Registry překonal 47 879 serverů (40násobný růst za 10 měsíců) a specifikace z 2026-07-28 učinila tento protokol bezstavovým a připraveným pro produkční nasazení. Zatímco velké podniky nasazují agenty, slovenské MSP jsou na ~5% adopci AI. Proč éra agentů začíná právě teď – a 3kroková cesta od nuly k vašemu prvnímu agentovi.

---

4. listopadu 2026
  AI Agents
  4 min čtení
  Marian Stancik

### MCP se vrací: Proč éra agentů začíná právě teď — a co to znamená pro malé a střední podniky

### Číslo, které by mělo probudit každé MSP

Dne 21. října 2026 překonal oficiální MCP Registry 47 879 názvů serverů – ve srovnání s 1 204 na konci roku 2025. To je 40násobný růst za deset měsíců. Dvě třetiny těchto serverů nyní vystavují vzdálený koncový bod, což znamená, že se nejedná o žádné ukázkové hračky v README; jsou to služby, které firmy skutečně volají přes síť.

Čísla z npm vyprávějí stejný příběh. Oficiální TypeScript SDK (
```
@modelcontextprotocol/sdk
```
) zaznamenal nárůst z 31,3 milionu stažení v září 2025 na 231,9 milionu v září 2026 – což je 7,4násobný meziroční skok. Napříč všemi Tier-1 SDK vykazuje projekt MCP téměř půl miliardy stažení měsíčně.

Tohle je návrat, který nikdo neplánoval: po vlně odporu z počátku roku 2026, kdy se tvrdilo, že „MCP je přeceňovaný“, Model Context Protocol nezmizel. Stal se sice nudným, ale připraveným pro produkční nasazení – a přesně proto éra agentů začíná právě teď.

### Proč vlna odporu minula cíl

Koncem roku 2025 a začátkem roku 2026 spousta chytrých lidí MCP odepsala. Stížnosti byly reálné: protokol byl příliš upovídaný, SDK byly v plenkách, každé demo se připojovalo k API pro počasí a z „MCP serveru“ se stal vtip označující pouhý wrapper kolem jednoho volání nástroje.

Kritici však přehlédli, že protokol není produkt – je to kontrakt. Ekosystém udělal to, co ekosystémy dělají: zachoval kontrakt a nahradil vše kolem něj. Předání MCP pod křídla Agentic AI Foundation spadající pod Linux Foundation v prosinci 2025 (spoluzaložené společnostmi Anthropic, Block a OpenAI, s podporou Google, Microsoft, AWS, Cloudflare a Bloomberg) smetlo otázku správy a řízení ze stolu. Žádný samostatný dodavatel už nyní nemůže tento standard rozbít.

Poté dospěl i samotný protokol. Specifikace z 2026-07-28 penzionovala handshake 
```
initialize
```
 a hlavičku 
```
Mcp-Session-Id
```
 – jádro je nyní bezstavové, s požadavky na více cest tam a zpět (MRTR) a směrováním založeným na hlavičkách (
```
Mcp-Method
```
, 
```
Mcp-Name
```
). Bezstavovost znamená triviálně škálovatelná serverless nasazení: spustíte MCP koncový bod, pošlete na něj zátěž a nemusíte spravovat žádný stav relace. AgentCore od Amazon Bedrock to podporuje nativně. OpenAI, Google DeepMind a Microsoft to dodávají ve výchozím nastavení. Podnikový plán přidává OAuth 2.1, auditní záznamy a chování brány – ty nudné věci, které odlišují dema od skutečné infrastruktury.

Pointa: 66 % aktivních MCP serverů nyní běží na vzdálených koncových bodech, Forrester předpovídá, že 30 % dodavatelů podnikových aplikací dodá v roce 2026 své vlastní MCP servery, a trh s MCP měl v roce 2025 hodnotu 1,2 miliardy dolarů s předpokládaným ročním růstem 37,2 % do roku 2035. Protokol zvítězil – ne proto, že by byl sexy, ale protože byl tím jediným otevřeným kontraktem, na kterém se všichni dokázali shodnout.

### Mezitím se propast prohlubuje

Zde přichází ta nepříjemná část. Zatímco velké podniky nasazují flotily agentů a infrastruktura protokolu přechází na bezstavový a remote-first přístup, většina slovenských MSP stále vnímá AI jen jako chatbot. Zpráva Evropské komise o digitální dekádě (Digital Decade Country Report) uvádí míru přijetí AI na Slovensku na přibližně 5 % – oproti průměru EU, který se pohybuje kolem 8 %. Hlavním podezřelým je nedostatek dovedností a země má vyčleněno 1,2 miliardy eur z digitálních fondů právě na to, aby tuto mezeru zaplnila.

Potkávám majitele firem, kteří se nikdy nedotkli API a předpokládají, že „integrace“ je něco, co pro ně udělá dodavatel někde za přihlašovací stránkou. Éře agentů je to ale jedno. Odměňuje firmy, které dokážou svá data a procesy vyjádřit jako volatelné služby – a trestá ty, které to nedokážou, protože nástroje pro agenty jsou vyvíjeny tak, aby komunikovaly se službami, nikoli s lidmi přes webové formuláře.

Dobrá zpráva: nemusíte se nejprve stát softwarovou firmou. Cesta od nuly k vašemu prvnímu funkčnímu agentovi má tři kroky a ten první je obvykle už z 80 % hotový.

### Od nuly k prvnímu agentovi ve 3 krocích

Použiji konkrétní příklad slovenské malé firmy: společnost, která chce agenta pro odpovídání na dotazy zákazníků ohledně stavu objednávky. Stejný vzorec platí pro faktury, zásoby, konzultace, cokoli.

### Krok 1 – Vystavte jeden koncový bod (část, kterou už máte)

Data téměř jistě máte. To, co potřebujete, je jediný HTTP koncový bod, který je vrátí ve strukturovaném formátu. Nejmenší užitečná verze:

```
# order_status.py — minimální koncový bod pouze pro čtení (FastAPI)
from fastapi import FastAPI
app = FastAPI()

ORDERS = {"OBJ-1001": "shipped", "OBJ-1002": "in warehouse", "OBJ-1003": "paid"}

@app.get("/api/order/{order_id}")
def order_status(order_id: str):
    return {"order_id": order_id, "status": ORDERS.get(order_id, "unknown")}
```

To je celý integrační kontrakt. Zatím nepotřebujete OAuth, nástěnku ani zákaznický portál. Jeden koncový bod na jeden proces.

### Krok 2 – Zabalte jej jako MCP server (nová standardní vrstva)

Nyní tento koncový bod zviditelněte pro jakéhokoli AI agenta. S oficiálním Python SDK je to záměrně minimalistické:

```
# mcp_order_server.py — vystavení koncového bodu jako MCP nástroje
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("order-status")

@mcp.tool()
def get_order_status(order_id: str) -> str:
    r = httpx.get(f"https://api.example.sk/api/order/{order_id}").json()
    return f"Objednávka {r['order_id']} je ve stavu {r['status']}."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

Jeden Python soubor. Agent – Claude, Gemini, vaše vlastní orchestrační vrstva, jakýkoli klient, který ovládá MCP – nyní tento nástroj objeví, přečte si jeho schéma a zavolá jej, jakmile se objeví odpovídající dotaz zákazníka. Už nemusíte stavět vlastní integraci pro každého dodavatele AI zvlášť; vytvoříte ji jednou a získá ji každý agent kompatibilní s MCP.

### Krok 3 – Nasměrujte na něj agenta (a ponechte člověka v rozhodovací smyčce)

Posledním krokem je konfigurace, nikoli kód:

```
# agent_config.json — připojení klienta k MCP serveru
{
  "mcpServers": {
    "order-status": {
      "url": "https://api.example.sk/mcp/order-status",
      "auth": {"scheme": "bearer", "env": "MCP_TOKEN"}
    }
  }
}
```

Od této chvíle může agent kontrolovat stav objednávky, předávat hraniční případy člověku, logovat každé volání a – jakmile přidáte koncový bod pro zápis – dokonce s vaším schválením aktualizovat záznamy. V tom spočívá celý trik: agent je volitelná služba plus smyčka a MCP je rozhraní, které obojí propojuje s jakýmkoli modelem.

### Co sám reálně provozuji

Nepíšu to jen teoreticky. Od roku 2025 běží můj produkční stack – Hermes Agent od Nous Research – na přesně tomto vzorci na Hetzner VPS za 6 € měsíčně: Telegram brána, paměťová vrstva SQLite, směrování mezi více LLM přes OpenRouter a sada agentů řízených cronem, kteří publikují obsah, monitorují servery a udržují digitální dvojče mé vlastní vývojářské práce. Devatenáct agentů, 24/7, řízených stejným MCP kontraktem, který dnes tvoří základ podnikových stacků.

Poučení z každodenního provozu: model je nahraditelný, protokol nikoli. Pod stejnými MCP servery jsem vyměnil modely už tolikrát, že to ani nespočítám – nástroje, paměť i oprávnění přitom zůstaly beze změny. To je architektonický argument pro MCP v jedné větě: odděluje vaše data a procesy od toho, kdo zrovna v tomto čtvrtletí vyrábí nejlepší model.

### Proč je to také otázka compliance

Slovenské firmy nemohou ignorovat ani regulační rovinu. Článek 50 Aktu o AI (EU AI Act) – transparentnost pro obsah generovaný AI a interakce s AI – je vymahatelný od 2. srpna 2026 a nové zákazy deepfakes platí od 2. prosince 2026. Nejpřísnější pravidla pro vysoce rizikové systémy byla odsunuta na prosinec 2027, což sice poskytuje čas, ale ne navždy.

Praktický důsledek: firmy, které staví agenty už teď, budou mít zavedené postupy pro správu, logování a lidský dohled v momentě, kdy povinnosti pro vysoce rizikové systémy vstoupí v platnost. Ty, které budou čekat, budou pak narychlo zmatkovat. Směřování MCP k auditním záznamům a oprávněním na úrovni nástrojů se náhodou přesně shoduje s tím, co budou regulátoři vyžadovat – standardní rozhraní umožňují kontrolovatelnost compliance namísto improvizace.

Můj pohled: éra agentů nezačíná velkolepou prezentací na stadionu ani předplatným za 500 dolarů měsíčně. Začíná tím, že jedna malá firma vystaví jeden koncový bod, zabalí ho do jednoho MCP serveru a deleguje jeden opakující se úkol na něco, co pracuje v noci i o víkendech. Udělejte to třikrát a budete před většinou firem v zemi.

Pokud vedete slovenské MSP a chcete vidět, jak by vypadal váš první agent – které procesy má smysl vystavit, kolik to stojí a jak zajistit soulad s předpisy – nabízím bezplatnou konzultaci prvním pěti firmám, které si ji rezervují. Podrobnosti najdete na mé kontaktní stránce; žádné závazky, žádné prezentace, jen vaše reálná data a funkční prototyp na konci.

Přihlaste se k odběru newsletteru pro technické analýzy do hloubky – jeden e-mail týdně o architektuře agentů, souladu s EU AI Act a o tom, co sám nasazuji do produkce.

⚠️ Generováno AI | Pouze pro informační účely | marianstancik.dev/disclaimer

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
