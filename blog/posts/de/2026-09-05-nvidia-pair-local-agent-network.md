# Lokales Agenten-Netzwerk für NVIDIA PAIR — Verteilte Inferenz über Geräte

**Datum:** 5. September 2026 | **Autor:** Marian Stancik

Auf der IFA 2026 in Berlin hat NVIDIA PAIR — Personal AI Router vorgestellt, ein kostenloses Open-Source-Tool, das ungenutzte PCs im lokalen Netzwerk erkennt und Inferenzanfragen auf diese verteilt. Ein einzelner Agent kann fünf Sub-Agenten starten, die parallel auf drei Rechnern laufen, anstatt in einer Warteschlange auf einer einzigen GPU zu warten. NVIDIAs Benchmarks zeigen eine 2,04-fache Beschleunigung — 18 Minuten auf einem Gerät wurden auf 8 Minuten und 48 Sekunden bei der Verteilung auf drei Geräte reduziert.

Dies verändert unsere Sichtweise auf lokale KI-Agenten. Der Engpass war nie die reine Rechenleistung — es war die Auslastung. Mehr als die Hälfte der Haushalte verfügt über zwei oder mehr PCs, und die meisten stehen während des Arbeitstages ungenutzt da. PAIR verwandelt diese latente Kapazität in ein verteiltes Inferenz-Cluster, das man einmal konfiguriert und dann vergisst.

Ich betreibe meine Agenten-Infrastruktur auf einem Hetzner VPS, aber die Architekturmuster für ein verteiltes Agentennetzwerk sind identisch, egal ob man lokal oder in der Cloud deployt. Hier erfahren Sie, was PAIR leistet, wie es in die moderne Zwei-Ebenen-Architektur passt und wie Sie Ihr eigenes Multi-Device-Netzwerk aufbauen.

Was NVIDIA PAIR wirklich ist
PAIR ist kein verteiltes Trainings-Framework und poolt keinen GPU-Speicher für ein einzelnes Riesenmodell. Es ist ein Load Balancer auf Anfrage-Ebene für lokale Inferenz.
Jeder verbundene PC betreibt seinen eigenen lokalen KI-Stack (Ollama oder LM Studio mit lokalen Modellen). PAIR erkennt verfügbare Rechner im LAN, überwacht deren Auslastung und leitet einzelne Anfragen an das am besten geeignete Gerät weiter. Wenn ein Gerät beitritt oder das Netzwerk verlässt, passt sich PAIR vollautomatisch an.
Die zentrale Designentscheidung von NVIDIA: PAIR arbeitet auf der Ebene von Agenten-Aufgaben, nicht auf der Ebene einzelner Token-Aufrufe. Ein Agent, der mehrere Sub-Agenten spawnt, kann die Inferenzanfragen jedes Sub-Agenten auf verschiedene Geräte verteilen. Das ist Parallelität auf Agentenebene.
„PAIR ist ein persönlicher KI-Router, der KI-Inferenz intelligent über alle Geräte im lokalen Netzwerk verteilt. Er fasst nicht mehrere PCs zu einem zusammen, sondern verteilt Aufgaben an verfügbare Ressourcen.“ — NVIDIA, IFA 2026

Architekturmuster für Multi-Device-Inferenz
Muster 1: Parallelität auf Aufgabenebene
Ein koordinierender Agent empfängt eine komplexe Anfrage, zerlegt sie in unabhängige Teilaufgaben und delegiert sie an Sub-Agenten. Die Inferenz jedes Sub-Agenten läuft parallel auf einem anderen Rechner.
Muster 2: Gestaffeltes Modell-Routing
Unterschiedliche Geräte betreiben unterschiedliche Modelle nach Leistungsfähigkeit: Desktop (RTX 4090) für tiefes Reasoning, Laptop (RTX 4070) für schnelle Extraktionen, Mini-PC für Klassifizierung und Routing.
Muster 3: Lokaler + Cloud Hybrid-Modus
Lokale Geräte übernehmen datensensible Aufgaben und interne Dokumente. Bei komplexen Reasoning-Schritten greift der Agent transparent auf Cloud-Modelle (DeepSeek V3, Claude 3.5 Sonnet) zurück.
