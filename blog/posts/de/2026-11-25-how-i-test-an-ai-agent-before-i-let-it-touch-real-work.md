# Wie ich einen AI Agent teste, bevor ich ihn an echte Arbeit lasse

> **Published:** 2026-11-25  
> **Author:** Marian Stancik  
> **Summary:** Ein Agent, der in einer Demo funktioniert, und einer, der am Montagmorgen funktioniert, sind zwei verschiedene Dinge. Hier sind die fünf Checks, die ich durchführe, bevor ein Agent echte Arbeit übernimmt.

---

25. November 2026
  AI Agents
  6 Min. Lesezeit
  Von Marian Stancik

### Wie ich einen AI Agent teste, bevor ich ihn an echte Arbeit lasse

Ein Agent, der in einer Demo funktioniert, und ein Agent, der an einem normalen Montagmorgen funktioniert, sind zwei verschiedene Dinge. Bevor ich einen Agenten echte Arbeit anfassen lasse, durchläuft er fünf Prüfungen. Die meisten dauern unter zehn Minuten und sparen später Stunden an Aufräumarbeit.

### Das Problem: Wir beurteilen Agenten nach der Demo

Fast jeder Agent, den ich online präsentiert sehe, wird auf dieselbe Weise gezeigt: eine saubere Eingabe, ein freundliches Beispiel, ein Mensch, der auf den Bildschirm schaut. Das sieht großartig aus. Dann verbindest du ihn mit einem echten Posteingang, einer echten Tabellenkalkulation oder einer echten Kundenanfrage, und er fällt auseinander – nicht mit einem Absturz, sondern still.

Stilles Scheitern ist die teure Art. Der Agent sagt „erledigt“, schreibt eine halb richtige Zeile in deine Tabelle, sendet eine Antwort mit dem falschen Namen oder läuft fünfzehn Mal durch denselben Tool-Aufruf. Eine Woche lang bemerkt es niemand.

Die Kosten verschlimmern das. Ich verbrauche etwa 4 Milliarden Token pro Monat für rund 200 $ über DeepSeek auf OpenRouter. Dasselbe Volumen auf den teuersten Frontier-Modellen würde etwa 15.000 $ kosten. Günstige Token sind großartig, aber sie bedeuten auch, dass ein in einer Schleife hängender Agent nicht sofort wehtut – falsche Ausgaben überleben länger, bevor sie jemand bemerkt.

### Wie ich Agenten teste, bevor sie echte Arbeit bekommen

Ich baue auf Open-Source-Frameworks – hauptsächlich Hermes Agent und OpenBot (eine Open-Source-Alternative zum Grok-Bot) – mit DeepSeek über OpenRouter für günstige Iterationen. Die fünf Prüfungen unten sind unabhängig vom Framework dieselben.

- 1. Beginne mit dem hässlichsten Input, den du hast. Nicht mit einem getippten Beispiel – dem echten Screenshot, der halb geschriebenen E-Mail, dem PDF mit einer Tabelle, die sich nicht parsen lässt. Wenn der Agent nur mit perfektem Input funktioniert, hast du ein Skript gebaut, keinen Agenten.

- 2. Führe ihn zweimal mit demselben Input aus. Dieselbe Aufgabe, dieselben Daten, zweimal. Wenn die Antworten abweichen, finde heraus, warum, bevor du ihm vertraust: Temperatur, Tool-Reihenfolge, ein im Prompt versteckter Zeitstempel. Nicht-Determinismus ist nicht automatisch schlecht, aber unerklärter Nicht-Determinismus ist es.

- 3. Nimm ein Tool weg. Trenne eine API oder widerrufe einen Schlüssel und führe die Aufgabe erneut aus. Ein guter Agent scheitert laut und sagt dir, was fehlt. Ein schlechter erfindet eine Antwort. Lautes Scheitern ist eine Funktion, die du willst.

- 4. Zähle Schritte und Token. Protokolliere jeden Tool-Aufruf. Eine einfache Aufgabe, die vierzehn Schritte braucht, bedeutet meist einen vagen Prompt oder eine schlecht geschriebene Tool-Beschreibung, nicht eine schwere Aufgabe.

- 5. Lies die Ausgabe wie ein Fremder. Würde ein Kollege, der dein Setup nicht kennt, das Ergebnis verstehen, ohne dich zu fragen? Wenn nicht, ist der Agent nicht fertig – er hat die Arbeit nur an jemand anderen verschoben.

Nichts davon braucht ein Test-Framework oder eine CI-Pipeline. Es braucht zwanzig Minuten und die Bereitschaft, unbeeindruckt zu sein.

### Wo das scheitert und worauf du achten musst

Ehrliche Grenzen: Fünf Prüfungen decken die reale Welt nicht ab. Ein Agent kann alle bestehen und am Dienstag trotzdem kaputtgehen, wenn eine Website ihr HTML ändert oder ein Kunde etwas schickt, das du noch nie gesehen hast. Tests reduzieren Überraschungen; sie beseitigen sie nicht.

Zwei weitere Fallen, in die ich getappt bin:

- Mit einem anderen Modell testen, als du auslieferst. Günstige Modelle für Iterationen sind in Ordnung, aber das Verhalten ändert sich zwischen Modellen. Die abschließende Prüfung muss mit dem Modell laufen, das die Arbeit tatsächlich erledigt.

- Unbewusstes Babysitten. Wenn du immer in der Nähe bist, um nachzuhelfen, testest du keinen Agenten – du testest dich selbst. Lass ihn einen Tag allein und schau, was passiert.

Und die rechtliche Seite: Wenn dein Agent personenbezogene Daten berührt, kommen DSGVO und der EU AI Act ins Spiel. Ich bin Jura-Student im dritten Jahr, kein Anwalt – alles, was ich über Regulierung schreibe, ist eine subjektive Anmerkung, und für echte Entscheidungen brauchst du einen Rechtsanwalt.

### Fazit

KI ist ein Werkzeug, keine Magie. Der Unterschied zwischen einem Agenten, der dir Zeit spart, und einem, der still ein Chaos anrichtet, ist meist nicht das Modell – sondern ob du zwanzig Minuten damit verbracht hast, ihn zuerst kaputtzumachen.

Wenn du dich über das Testen deines eigenen Setups austauschen möchtest, schreib mir auf WhatsApp unter +421 940 377 855, oder probiere die kostenlosen Tools unter /en/tools/ aus. Dieser Artikel und die Website werden mit KI-Agenten und abschließender menschlicher Prüfung erstellt.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
