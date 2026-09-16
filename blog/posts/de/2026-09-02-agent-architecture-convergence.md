# Die Konvergenz der Agenten-Architekturen: Warum alle das gleiche Zwei-Ebenen-System bauen

> **Published:** 2026-09-02  
> **Author:** Marian Stancik  
> **Summary:** NVIDIA AVO, die AOS-Referenzarchitektur und Auton einigten sich auf das gleiche Muster: Trennung von Governance und Ausführung.

---

In den letzten sechs Monaten haben drei unabhängige Entwicklungsteams ihre Referenzarchitekturen für autonome KI-Agenten veröffentlicht: NVIDIA (AVO), das AOS-Projekt und das Auton-Framework. Alle drei sind zu exakt demselben Grundmuster konvergiert: einem Zwei-Ebenen-System (Two-Plane Architecture), das Governance von der Ausführung trennt.

### Die Zwei Ebenen im Detail

### 1. Die Steuerungsebene (Control Plane)

Verwaltet Richtlinien, Sicherheitslimits, EU AI Act Konformität und persistente Speicherstrukturen (Obsidian Vaults, SQLite). Sie bestimmt, WAS erlaubt ist.

### 2. Die Ausführungsebene (Runtime Plane)

Führt Werkzeugaufrufe über das Model Context Protocol (MCP) aus, steuert dynamisches Modell-Routing und isoliert Fehler. Sie bestimmt, WIE Aufgaben gelöst werden.

### Fazit

Monolithische Agenten scheitern an Fehlentscheidungen in Endlosschleifen. Die Trennung in Steuerungs- und Ausführungsebene garantiert Produktionsstabilität.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
