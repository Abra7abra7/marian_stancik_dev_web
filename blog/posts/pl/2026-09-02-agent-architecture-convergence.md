# Konwergencja Architektur Agentów: Dlaczego wszyscy budują ten sam dwupoziomowy system

**Data:** 2 września 2026 | **Autor:** Marian Stancik


W ciągu ostatnich sześciu miesięcy trzy niezależne zespoły inżynierskie opublikowały swoje referencyjne architektury dla autonomicznych agentów AI: NVIDIA (AVO), projekt AOS oraz framework Auton. Mimo różnych założeń początkowych, wszystkie trzy projekty zbiegły się w tym samym punkcie: dwupłaszczyznowym modelu (Two-Plane Architecture) rozdzielającym zarządzanie od wykonania.

Dwie Płaszczyzny Systemu

1. Płaszczyzna Sterowania (Control Plane)
Odpowiada za reguły, stan i nadzór:

  Pamięć trwała: Grafy wiedzy w Markdownie (Obsidian) i relacyjne bazy SQLite.
  Polityki i Bezpieczeństwo: Limity budżetowe, zgodność z RODO i EU AI Act.
  Watchdog: Monitorowanie pętli decyzyjnych i zapobieganie zacięciom agenta.



2. Płaszczyzna Wykonawcza (Runtime Plane)
Realizuje konkretne zadania narzędziowe:

  Serwery MCP (Model Context Protocol): Integracje z bazami, przeglądarkami i API.
  Dynamiczny Routing: Dobór modeli LLM zależnie od stopnia trudności zadania.



Wnioski
Rozdzielenie płaszczyzny decyzyjnej od wykonawczej to jedyna droga do stabilnych i bezpiecznych wdrożeń AI w biznesie.

