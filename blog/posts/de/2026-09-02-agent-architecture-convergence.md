# Die Konvergenz der Agenten-Architekturen: Warum alle das gleiche Zwei-Ebenen-System bauen

**Datum:** 2. September 2026 | **Autor:** Marian Stancik


In den letzten sechs Monaten haben drei völlig unabhängige Entwicklungsteams ihre Referenzarchitekturen für autonome KI-Agenten veröffentlicht: NVIDIA (AVO), das AOS-Projekt und das Auton-Framework. Obwohl sie für unterschiedliche Anwendungsbereiche entwickelt wurden, sind alle drei zu exakt demselben Grundmuster konvergiert: einem Zwei-Ebenen-System (Two-Plane Architecture), das Governance von der Ausführung trennt.

Dies ist kein Zufall. Es ist das unvermeidliche Ergebnis, wenn man versucht, autonome Agenten 24/7 in Produktionsumgebungen stabil zu betreiben.

Die Zwei Ebenen im Detail

1. Die Steuerungsebene (Control Plane / Governance)
Die Steuerungsebene definiert WAS getan werden darf und welche Leitplanken gelten. Sie enthält:

  Zustands- und Speicherverwaltung: Persistente Wissensgraphen (z. B. Obsidian Markdown Vaults oder SQLite).
  Policy & Guardrails: Sicherheitsregeln, EU AI Act Konformität, Budgetlimits.
  Watchdog & Supervisor: Überwachung von Schleifen, Deadlocks und Erkennung von Halluzinationen.



2. Die Ausführungsebene (Runtime / Execution Plane)
Die Ausführungsebene steuert WIE die Aufgaben umgesetzt werden:

  Model Context Protocol (MCP) Server: Werkzeugaufrufe, API-Schnittstellen, Dateisystemzugriff.
  Dynamisches Modell-Routing: Zuweisung von Sub-Aufgaben an DeepSeek, Claude 3.5 Sonnet oder GPT-4o.
  Fehlerbehandlung & Retry-Logik: Isolierte Wiederholungsversuche ohne Kontrollverlust.



Warum monolithische Agenten scheitern
Wenn Steuerung und Ausführung in einer einzigen Prompt-Schleife vermischt werden, führt jede Fehlentscheidung des Modells zum Systemstillstand. Die strikte Trennung garantiert Ausfallsicherheit und Auditierbarkeit.

