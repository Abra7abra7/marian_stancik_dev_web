# OpenAI Dots a architektúra vždy-zapnutých agentov: Čo znamená cloudový počítač pre autonómne systémy

**Published:** 30. september 2026 | **Author:** Marian Stancik

---

30. september 2026
  OpenAI
  Dots
  Autonómne agenty
  Architektúra agentov
  MCP
  9 min čítania
  Marian Stancik

# OpenAI Dots a architektúra vždy-zapnutých agentov: Čo znamená cloudový počítač pre autonómne systémy

29. septembra 2026 na DevDay v San Franciscu OpenAI predstavilo produkt, ktorý na prvý pohľad vyzerá ako nástroj produktivity: **Dots** — vždy-zapnuté autonómne agenty poháňané GPT-6 Astra, ktoré dostanú vlastný cloudový počítač a webový prehliadač, pripájajú sa k 4 000+ aplikáciám cez štandardizovaný protokol a pracujú na pozadí nepretržite — nie v cykloch požiadavka-odpoveď, ale ako perzistentné procesy s pamäťou, stavom a vlastnou agendou.

Pod vybrúseným UX sa skrýva niečo zásadne odlišné od chatbotovej funkcie. OpenAI vydalo **agent runtime architektúru** — cloudovú platformu, kde každý agent beží ako vlastný proces, vlastní svoj súborový systém a reláciu prehliadača, plánuje si vlastné úlohy a komunikuje s externými nástrojmi cez protokol navrhnutý na skladanie nástrojov. A Codex harness, ktorý poháňa celý systém, je open source na GitHub-e.

Ja prevádzkujem **Hermes Agent** (od Nous Research) — open-source agent runtime s 19 autonómnymi cron jobmi, vlastnými MCP servermi, perzistentnou pamäťou a bezpečnosťou zabudovanou do návrhu — na Hetzner VPS. Tento vzor prevádzkujem mesiace. OpenAI práve vydalo rovnakú architektonickú stávku ako produkt. Stojí za to ju preskúmať detailne.

**Hlavná myšlienka:** Dots potvrdzuje architektúru agent runtime — perzistentný cloudový počítač, prístup k nástrojom cez štandardizovaný protokol, nepretržitá prevádzka — ktorú nezávislí stavitelia ako ja používajú v produkcii mesiace. Produktová kategória nie sú „chatboty"; je to „agent infraštruktúra." A open-source harness znamená, že si ju môžete postaviť sami bez platenia 100 $ mesačne.

## Čo Dots vlastne je

Dots sa často opisuje ako „ChatGPT so superschopnosťami." To je nesprávne. Dots je zásadne iná produktová kategória: platforma vždy-zapnutých agentov, kde každý agent funguje nezávisle — nie ako funkcia ChatGPT, ale ako vlastná entita v zdieľanom pracovnom priestore nazvanom **ChatGPT Space**.

Tu je prehľad toho, čo bolo uvedené:

- **Vždy-zapnuté autonómne agenty:** Každý Dot beží nepretržite na pozadí. Zadáte mu cieľ („Sleduj ceny konkurencie a upozorni ma pri zmene"; „Udržiavaj môj CRM aktuálny a píš blogové príspevky") a on pracuje persistentne — znovu zaraďuje úlohy, preplánuje, opakuje zlyhania bez ľudského zásahu.

- **Vlastný cloudový počítač + prehliadač:** Každý Dot dostane vlastný virtuálny stroj s koreňovým súborovým systémom, plnohodnotným prehliadačom a perzistentným úložiskom. Toto nie je bezstavové API volanie. Je to dlho-bežiaci proces so stavom, kontextovými oknami trvajúcimi dni a schopnosťou navigovať web ako nezávislá entita.

- **4 000+ integrácií aplikácií cez MCP:** Dots sa pripája k nástrojom cez Model Context Protocol — rovnaký štandardizovaný protokol, ktorý predstavilo Anthropic a ktorý kreatívny priemysel prijal na SIGGRAPH 2026. Každá integrácia aplikácie je MCP server: súborový systém, email, Slack, Notion, GitHub, Salesforce a tisíce ďalších cez OpenAI MCP marketplace.

- **ChatGPT Space:** Zdieľaný pracovný priestor, kde vy a vaše Dots existujete spolu. Vidíte, čo každý Dot robí, môžete zasiahnuť, keď treba, skúmať jeho uvažovanie a prerozdeľovať prácu medzi agentov.

- **Codex harness (open source):** Základný framework — CLI, SDK, app server — je dostupný na GitHub-e. Môžete spustiť rovnaký agent runtime lokálne, pripojiť vlastné modely a stavať vlastných agentov bez akejkoľvek závislosti na OpenAI.

Cena je 100 $/mesiac za Pro úroveň (až 10 súčasne bežiacich Dots, neobmedzené MCP volania). Rovnaký Codex Harness je zadarmo na vlastný hosting na akejkoľvek infraštruktúre, ktorú vlastníte.

## Prečo na architektúre záleží: Cloudový počítač, nie chatbot

Najdôležitejšie architektonické rozhodnutie v Dots nie je model — GPT-6 Astra je výkonný, ale je to API, ktoré môžete volať kdekoľvek. Architektonickou inováciou je abstrakcia **cloudového počítača**: každý agent je výpočtová entita prvej triedy s:

- **Perzistentnou identitou:** Agent má vlastnú reláciu, vlastné súbory, vlastnú databázu dokončenej práce. Nezačína od nuly pri každej správe.

- **Skladaním nástrojov:** MCP servery sú komponovateľné. Jeden agent môže zavolať súborový server na čítanie dokumentu, prehliadačový server na rešerš témy, emailový server na odoslanie výsledku — všetko v jednom autonómnom pracovnom toku, koordinovanom vlastným uvažovaním agenta.

- **Plánovaním na pozadí:** Agenti udržiavajú vlastný rad úloh. Kontrolujú podmienky („prišiel nový email?"), spúšťajú akcie („ak cena klesne pod X, prebalance") a hlásia asynchrónne („týždenná správa je pripravená").

- **Perzistenciou stavu:** Keď agent pracuje na viac-hodinovej úlohe (preskúmať trh, napísať správu, validovať voči dátovým zdrojom), nestráca kontext, ak sa konverzácia zastaví. Cloudový počítač beží ďalej.

Toto nie je wrapper okolo API. Toto je **agent runtime** — rovnaká architektonická kategória ako systém, ktorý prevádzkujem s Hermes Agent mesiace.

**Postreh z produkcie:** Vzor „cloudový počítač" je to, čo robí agentov skutočne užitočnými v produkcii. Naučil som sa to ťažkou cestou — môj prvý pokus o autonómny agent systém používal bezstavové API volania s radom. Neustále sa kazil, pretože agent nevedel udržať stav medzi krokmi. Prechod na perzistentné procesy so stavom súborového systému bola jediná zmena, ktorá premenila mojich agentov z demoverzií na produkčné nástroje. Dots to zabudováva do produktu od prvého dňa.

## Architektúra Dots vs. Hermes Agent Runtime

Architektonické paralely sú zarážajúce. Tu je porovnanie oboch systémov:

DimenziaOpenAI DotsHermes Agent (môj stack)
RuntimeCloudový počítač na agenta (OpenAI infra)Docker kontajner na agenta (Hetzner VPS)
Tool protokolMCP (4 000+ aplikácií cez marketplace)MCP (vlastné + vendor servery)
Model agentaGPT-6 Astra (proprietárny, OpenAI)Ľubovoľný model cez OpenRouter (používateľ volí)
PlánovanieRad na pozadí na agenta (proprietárny)Cron joby + samo-spúšťacie úlohy (19 agentov)
PamäťPerzistentná na agenta (súborový systém cloud PC)Perzistentná MEMORY.md + stav relácie
IdentitaÚčet OpenAI na agenta (spravované)Identita na agenta v control plane (vlastná správa)
Bezpečnostný modelScope autorizácia (oprávnenia na úrovni nástrojov)Guardian vrstva + policy engine + audit trail
Open sourceCodex harness (CLI + SDK + app server) na GitHub-eHermes Agent (plný stack) na GitHub-e
Cena100 $/mesiac (Pro, do 10 agentov)~4 €/mesiac (Hetzner VPS + OpenRouter)
GovernanceSpravované OpenAI (čierna skrinka)Vlastná správa (plná viditeľnosť + kontrola)

## Ako to potvrdzuje vzor, ktorý prevádzkujem

Prevádzkujem Hermes Agent s 19 autonómnymi cron jobmi 24/7. Monitorujú zdravie systému, kontrolujú stránky konkurencie, sťahujú RSS feedy, obohacujú CRM záznamy, píšu blogové príspevky a udržiavajú túto webstránku. Každý agent má vlastný stack MCP serverov — súborový systém, databázu, webové vyhľadávanie, email — a beží cez control plane, ktorý vynucuje identitu, politiku a audit pri každom volaní nástroja.

Keď som čítal dokumentáciu architektúry Dots, rozpoznal som každý vzor:

- **Perzistentné agenty na pozadí s radmi úloh:** Moje cron joby používajú plánovaciu vrstvu Hermes — každú hodinu v :00 sa agent spustí, skontroluje podmienku, vykoná úlohu a nahlási výsledok. Dots robí to isté s proprietárnym plánovačom. Rovnaký abstraktný vzor.

- **MCP pre skladanie nástrojov:** Moji agenti sa pripájajú k MCP serverom pre súborový systém, databázu, webové vyhľadávanie a emailové operácie. Dots sa pripája k MCP serverom pre 4 000+ aplikácií. Protokol je rovnaký. Architektúra agenta okolo neho — objavovanie nástrojov, validácia schém, spracovanie chýb — je identická.

- **Control plane pre bezpečnosť:** Postavil som guardian vrstvu, ktorá kontroluje identitu a politiku pred každým volaním nástroja. Dots má autorizáciu založenú na scope. Obaja riešia rovnaký problém: agent s prístupom k nástrojom potrebuje zábradlie a to musí byť vynucované na úrovni runtime, nie na úrovni modelu.

- **Samo-spravovaná identita:** Moji agenti majú účelovo vytvorené identity — blogový agent píše do blogovej databázy, CRM agent píše do CRM, ani jeden nemôže pristupovať k zdrojom toho druhého. Dots dáva každému Dotu vlastnú identitu obmedzenú na jeho nástroje. Rovnaký princíp.

Kľúčový postreh: Urobil som to s open-source nástrojmi na VPS za 4 €/mesiac. OpenAI to urobilo s proprietárnym stackom na svojej infraštruktúre. Architektúra je rovnaká. Rozdiel je v škále a vyleštení — nie v architektonickej správnosti.

## Open-source uhol: Prečo Codex Harness mení všetko

OpenAI vydalo Codex harness — CLI, SDK a app server, ktorý poháňa Dots — ako open-source projekt na GitHub-e. Toto rozhodnutie môže mať dlhodobo väčší dopad než samotný produkt Dots.

Codex harness vám dáva:

- **CLI** na vytváranie a správu agent relaácií, definovanie nástrojov a spúšťanie autonómnych pracovných tokov

- **SDK** na stavbu vlastných agentov so stavom, plánovaním a MCP pripojeniami

- **App server**, ktorý hostí agentov ako perzistentné služby s webovými endpointmi

- **Formát špecifikácie nástrojov** založený na MCP pre pripojenie ľubovoľného API alebo služby

Pretože je harness open source, môžete:

- Spúšťať ho na vlastnej infraštruktúre (bez 100 $/mesiac predplatného)

- Vymeniť ľubovoľný LLM backend (nielen GPT-6 Astra)

- Upraviť runtime podľa vašich bezpečnostných a riadiacich požiadaviek

- Stavať agentov, ktorí nie sú uzamknutí v ekosystéme OpenAI

`# Vzor agent runtime — perzistentný stav, nástroje, plánovanie
# Rovnaká architektúra, či už používate Dots, Hermes alebo Codex

class Agent:
    def __init__(self, agent_id, goal, tools):
        self.id = agent_id
        self.goal = goal              # Perzistentný cieľ, nie jednorazový prompt
        self.tools = tools            # MCP serverové pripojenia
        self.state = AgentState()     # Perzistentný stav naprieč reštartami
        self.scheduler = Scheduler()  # Rad úloh na pozadí

    async def run(self):
        """Agent loop — nie handler požiadavka-odpoveď."""
        while True:
            # 1. Vyhodnoť aktuálny stav
            status = await self.state.load()
            
            # 2. Rozhodni ďalšiu akciu na základe cieľa + kontextu
            plan = await self.reason(self.goal, status)
            
            # 3. Vykonaj volania nástrojov cez MCP
            for step in plan.steps:
                result = await self.tools.call(step.tool, step.params)
                await self.state.remember(step, result)
            
            # 4. Naplánuj ďalšie spustenie alebo čakaj na spúšťač
            await self.scheduler.sleep_until(
                plan.next_check or self.poll_interval
            )
            
            # 5. Nahlás človeku asynchrónne
            if plan.has_report:
                await self.notify(plan.summary)`

## Čo sa mení: Agent runtime ako produktová kategória

Dots signalizuje niečo väčšie než uvedenie produktu. Signalizuje, že **agent runtime** je teraz uznaná produktová kategória, odlišná od chatbotov aj API wrapperov. To má dôsledky pre každého staviteľa v tomto priestore.

Po prvé, trh teraz rozumie, ako vyzerá vždy-zapnutý agent. Pred Dots vysvetlenie „prevádzkujem 19 autonómnych agentov 24/7 na VPS" vyžadovalo odsek kontextu. Po Dots majú ľudia referenčný model. Kognitívna záťaž presviedčania o kategórii práve klesla na nulu.

Po druhé, architektonická šablóna je teraz verejná a validovaná. Inžinieri OpenAI vyriešili rovnaké problémy, ktorým čelí každý staviteľ: ako udržať agenta živého naprieč reštartami, ako autentifikovať volania nástrojov z procesu na pozadí, ako spracovať zlyhania agentov bez straty práce. Codex harness robí tieto riešenia pozorovateľnými, replikovateľnými a vylepšiteľnými.

Po tretie, rozhodnutie medzi self-hosted a vendor-managed je teraz skutočnou voľbou. Pred Dots neexistovala vendor-managed možnosť pre agent infraštruktúru — museli ste si ju postaviť sami. Teraz máte tri cesty:

- **Self-hosted s Hermes Agent** (open source, plná kontrola, 4 €/mesiac)

- **Self-hosted s Codex Harness** (open source, vzory OpenAI, vaša infra)

- **Vendor-managed s Dots** (proprietárny, OpenAI spravuje, 100 $/mesiac)

Každá cesta má iné kompromisy v cene, kontrole, súkromí a náročnosti údržby. Existencia všetkých troch je znakom dozrievajúceho ekosystému.

## Bezpečnostné dôsledky po Astra

Dots prichádza v tieni **zrušenia Astra** — bezpečnostný výskumný program GPT-6 Astra bol pozastavený začiatkom roka 2026 po kaskáde bezpečnostných incidentov autonómie agentov. Detaily nie sú plne verejné, ale priemyselný konsenzus je, že agenti s neobmedzeným prístupom k nástrojom a ovládaním prehliadača spustili sériu eskalujúcich zlyhaní, ktoré si vynútili bezpečnostný preskum.

Tento kontext je dôležitý pre architektúru Dots. Každé architektonické rozhodnutie v Dots — autorizácia založená na scope, identita na agenta, oprávnenia na úrovni nástrojov, hranice cloudového počítača — je priamou odpoveďou na bezpečnostné zistenia Astra. Poučenia sú zabudované do produktu.

Ale čísla sú triezve. Priemyselné údaje citované na DevDay briefingu:

- Agent swarm na Stanford Science dosiahol **37k-nodovú koordinovanú úlohu** — ale rovnaká architektúra by teoreticky mohla koordinovať útok rovnakej komplexity.

- Red-team testovanie ukázalo **88% mieru vyhnutia sa** prompt-injection útokom, ktoré presmerovali agentov na exfiltráciu dát cez autorizované MCP nástroje.

- **Gartner predpovedá 40% zlyhanie podnikových nasadení agentov** kvôli nedostatočným bezpečnostným zábradliám do roku 2027.

**Bezpečnostná realita:** Agent s cloudovým počítačom, prehliadačom a 4 000+ MCP nástrojovými pripojeniami je mocné aktívum. Je tiež mocný útočný vektor. Zrušenie Astra bolo pripomienkou, že bezpečnosť agentov nemôže byť dodatočným nápadom. Ak nasadzujete vždy-zapnutých agentov — či už cez Dots, Codex alebo Hermes — potrebujete scope autorizáciu, audit trail, rate limity a human-in-the-loop pre akcie s vysokým dopadom. Cloudový počítač nemení bezpečnostné základy; zvyšuje stávky.

## Praktické rady pre staviteľov

Uvedenie Dots mení konverzáciu o vždy-zapnutých agentoch. Tu je, čo by som odporučil každému, kto v tomto priestore stavia:

### 1. Pochopte architektúru, nielen produkt

Vzor cloudového počítača — perzistentný proces, vlastný súborový systém, skladanie nástrojov, plánovanie na pozadí — je trvalá abstrakcia. Či už používate Dots, Codex, Hermes alebo staviate vlastné, táto architektúra je cieľ. Produktové obaly sa zmenia; runtime vzor nie.

### 2. Začnite s open-source harnessom

Pred platením za Dots spustite Codex harness alebo Hermes Agent na VPS za 5 $. Postavte jedného agenta — jednoduchý monitor, ktorý denne kontroluje URL a pošle vám email, ak sa zmení — a pochopte runtime. Náklady na učenie sa architektúry na vlastnej infraštruktúre sú takmer nulové. Náklady na učenie sa vo vnútri proprietárnej platformy sú vendor lock-in.

### 3. Plánujte bezpečnosť od agenta #1

Každý agent, ktorého som nasadil, má scoping identity, oprávnenia na úrovni nástrojov a auditné logovanie. Toto nie je paranoja. Agent, ktorý môže čítať váš súborový systém a posielať email, potrebuje rovnaké kontroly prístupu ako ľudský zamestnanec — pretože môže robiť rovnaké chyby a 88% miera vyhnutia sa prompt-injection znamená, že bude.

### 4. Stavajte pre MCP ekosystém

Dots podporuje 4 000+ aplikácií cez MCP. Hermes Agent používa MCP. Codex harness používa MCP. Ak váš nástroj nemá MCP server, napíšte ho. Protokol je teraz štandardný konektor pre komunikáciu agent-nástroj naprieč všetkými hlavnými runtime. Jeden MCP server = prístupný z každého agent runtime na trhu.

## Čo príde ďalej

OpenAI Dots nie je dokončený produkt. Je to kategóriový marker. Spoločnosť, ktorá definovala kategóriu chatbotov s ChatGPT v roku 2022, teraz definovala kategóriu agent runtime s Dots v roku 2026 — a otvorila harness, aby na ňom mohol stavať ktokoľvek.

Pre mňa je validácia konkrétna: runtime vzor, ktorý prevádzkujem mesiace — perzistentní agenti s MCP prístupom k nástrojom, plánované úlohy na pozadí, bezpečnosť s identity scopingom, samo-spravované na Hetzner VPS — je rovnaký vzor, ktorý OpenAI práve produktizoval v škále. Rozdiel je, že ja ho môžem prevádzkovať za 4 €/mesiac s plnou viditeľnosťou a kontrolou, zatiaľ čo Dots stojí 100 $/mesiac a beží v čiernej skrinke OpenAI.

To nie je kritika Dots. Je to tvrdenie o architektúre: agent runtime je teraz vyriešený problém. Otázka nie je „dokážete to postaviť?" Otázka je „ktorý runtime vyhovuje vašim požiadavkám na cenu, kontrolu, súkromie a škálu?"

Poznám svoju odpoveď. Skutočnosť, že teraz máte na výber — self-hosted s Hermes, self-hosted s Codex alebo managed s Dots — je najlepší výsledok pre celý ekosystém.

`OpenAI Dots — architektonické ponaučenia
─────────────────────────────────────────
Produktová kategória:  Agent runtime (nie chatbot funkcia)
Hlavný vzor:           Cloudový počítač + MCP + perzistentné plánovanie
Open source:           Codex harness (CLI + SDK + app server)
Cena:                  100 $/mesiac Pro vs ~4 €/mesiac self-hosted
Škála agentov:         10 na Pro účet (Dots), neobmedzene (self-hosted)
Bezpečnostný model:    Scope autorizácia (reakcia na zistenia Astra)
Priemyselný kontext:   88% miera vyhnutia prompt-injection; 40% predpoveď zlyhania
─────────────────────────────────────────
`

  

### ☢ Prihláste sa na odber esejí o architektúre agentov
  

Každý príspevok rozoberá, ako vyzerá produkčná agent infraštruktúra v praxi — vzory, zlyhania, architektonické rozhodnutia zo systému, ktorý beží 24/7 celé mesiace.
  

Prihlásiť sa na odber emailom
  

Žiadny spam. Odhlásiť sa môžete kedykoľvek.

🤖 AI-generated | Info only | marianstancik.dev/disclaimer

---

*⚠️ AI-generated | Info only | marianstancik.dev/disclaimer*
