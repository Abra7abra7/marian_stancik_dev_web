# Konwergencja Architektur Agentów: Dlaczego wszyscy budują ten sam dwupoziomowy system

> **Published:** 2026-09-02  
> **Author:** Marian Stancik  
> **Summary:** NVIDIA AVO, architektura referencyjna AOS i Auton framework przyjęły ten sam wzorzec: oddzielenie zarządzania od wykonania.

---

W ciągu ostatnich sześciu miesięcy trzy niezależne zespoły inżynierskie opublikowały swoje referencyjne architektury dla autonomicznych agentów AI: NVIDIA (AVO), projekt AOS oraz framework Auton. Wszystkie trzy zbiegły się w tym samym punkcie: dwupłaszczyznowym modelu (Two-Plane Architecture) rozdzielającym zarządzanie od wykonania.

### Dwie Płaszczyzny Systemu

### 1. Płaszczyzna Sterowania (Control Plane)

Zarządza regułami, stanem, limitami budżetowymi i zgodnością z RODO/AI Act oraz trwałą pamięcią (Obsidian Markdown, SQLite).

### 2. Płaszczyzna Wykonawcza (Runtime Plane)

Realizuje zadania narzędziowe przez protokół MCP, dynamiczny dobór modeli LLM oraz bezpieczną izolację błędów.

### Wnioski

Rozdzielenie decyzyjności od wykonania to jedyny sposób na bezpieczne wdrożenia autonomicznych agentów AI w firmach.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
