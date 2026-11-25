# Fünf Tests, die ich durchführe, bevor ein KI-Agent echte Arbeit anfasst

> **Published:** 2026-11-25  
> **Author:** Marian Stancik  
> **Summary:** Ein billiger Agent, der stillschweigend scheitert, kostet mehr als ein teurer, der stoppt. Fünf langweilige Checks, die ich durchführe, bevor ich eine echte Aufgabe übergebe.

---

25. November 2026
  AI Agents
  5 Min. Lesezeit
  Von Marian Stancik

### Fünf Tests, die ich durchführe, bevor ein KI-Agent echte Arbeit anfasst

Fünf Prüfungen. So lange brauche ich, um zu entscheiden, ob ein KI-Agent Zugriff auf echte Arbeit bekommt oder in einer Sandbox bleibt. Keine Benchmarks, keine Leaderboard-Screenshots — fünf langweilige Tests, die ein paar Dollar und einen Nachmittag kosten.

### Warum die meisten Menschen Agenten falsch testen

Die meisten beurteilen einen Agenten nach seiner Demo. Man tippt eine schöne Frage ein, er antwortet schön, alle nicken. Das Problem ist, dass eine Demo auf einem sauberen Pfad läuft: perfekte Eingaben, keine fehlenden Felder, keine halb kaputte API, niemand wartet auf der anderen Seite.

Echte Arbeit ist chaotisch. Ein Formular kommt mit einem leeren Umsatzsteuerfeld an. Ein Posteingang enthält eine Nachricht in drei Sprachen. Eine API liefert 200 OK mit einem im Body versteckten Fehler. Ein Agent, der die Demo bewältigt und dann bei der chaotischen Version stillschweigend scheitert, ist schlimmer als gar kein Agent — weil man aufhört zu prüfen.

Die Kosten sind nicht die Tokens. Die Kosten sind die E-Mail, die nie rausging, die Rechnung mit der falschen Nummer, der Kunde, der zwei Tage auf eine Antwort wartete, die der Agent angeblich erledigt hat.

### Wie ich einen Agenten teste, bevor er irgendetwas Reales anfasst

Ich baue auf Open-Source-Frameworks auf — meist Hermes Agent und OpenBot (eine Open-Source-Alternative zu Grok bot) — und leite das Modell über DeepSeek auf OpenRouter. Diese Kombination ist so günstig, dass Testen praktisch kostenlos ist. Hier ist die Routine.

- 1. Der Leere-Eingabe-Test. Ich sende nichts. Dann ein einzelnes Leerzeichen. Dann ein 40-seitiges PDF. Dann eine Datei mit der falschen Endung. Wenn der Agent eine Antwort erfindet, statt zu stoppen, fällt er durch.

- 2. Der Stopp-und-Fragen-Test. Ich gebe ihm eine Aufgabe, bei der absichtlich ein Detail fehlt — ein Datum, ein Betrag, ein Empfänger. Ein guter Agent fragt. Ein schlechter Agent rät selbstbewusst, und selbstbewusstes Raten ist das teuerste Verhalten im gesamten System.

- 3. Kosten pro erledigter Aufgabe, nicht pro Token. Token-Preise sind eine Ablenkung. Entscheidend ist, was eine abgeschlossene Aufgabe kostet. Letzten Monat habe ich etwa 4 Milliarden Tokens für rund $200 durch DeepSeek auf OpenRouter geschickt. Dasselbe Volumen auf den teuersten Frontier-Modellen würde bei nahezu $15,000 landen. So oder so dieselbe Lehre: Miss den erledigten Job, nicht die Rechnung.

- 4. Der Wiederholbarkeitstest. Ich führe dieselbe Aufgabe zehnmal aus und vergleiche die Ausgaben. Wenn sich die Struktur bei jedem Lauf ändert, ist der Agent nicht bereit für irgendetwas, das eine Datenbank oder einen Kunden versorgt.

- 5. Der Rückgängig-Test. Bevor etwas schreibt, sendet oder löscht, brauche ich einen Dry-Run-Modus und ein Log, das ich tatsächlich lesen kann. Wenn ich es nicht rückgängig machen kann, schalte ich es nicht ein.

Nichts davon ist besonders clever. Es ist dieselbe Disziplin, die man bei einem neuen Mitarbeiter in seiner ersten Woche anwendet — nur dass der Mitarbeiter nie müde wird und nie daraus lernt, bloßgestellt zu werden.

### Wo das an Grenzen stößt

Fünf Tests zu bestehen bedeutet, dass der Agent an dem Tag funktionierte, an dem man ihn testete. Es bedeutet nicht, dass er in Woche drei funktioniert. Modelle werden aktualisiert, Prompts verrotten, eine vorgelagerte API benennt ein Feld um, und die ganze Kette produziert still und leise Müll, der immer noch korrekt formatiert aussieht.

Die Tests sind also eine Momentaufnahme, kein Zertifikat. Die günstigen führe ich wöchentlich erneut aus und binde bei allem, was das Gebäude verlässt, einen Menschen in den Prozess ein. KI ist ein Werkzeug, keine Magie — und ein Werkzeug braucht Wartung.

Zwei weitere ehrliche Grenzen. Erstens kann ich nicht testen, was ich nicht messen kann, und viele Aufgaben (Schreiben, Urteilsvermögen, Ton) entziehen sich einer sauberen Messung. Zweitens: Wenn Ihr Agent personenbezogene Daten berührt oder unter den EU AI Act fällt, sind meine Notizen hier genau das — subjektive Beobachtungen eines Jura-Studenten im dritten Jahr. Ich bin kein Anwalt und gebe keine Rechtsberatung. Sprechen Sie mit einem Anwalt.

### Fazit

Testen Sie die langweiligen Fehler, nicht die beeindruckenden Erfolge. Leere Eingabe, fehlendes Detail, Wiederholbarkeit, Kosten pro erledigter Aufgabe und eine Möglichkeit zum Rückgängigmachen — das ist die ganze Checkliste, und sie hat mir mehr Geld gespart als jeder Modellvergleich.

Wenn Sie Ihr eigenes Setup durchgehen möchten, schreiben Sie mir auf WhatsApp unter +421 940 377 855 oder holen Sie sich die kostenlosen Tools unter /sk/tools/. Dieser Artikel wird, wie der Rest der Website, mit KI-Agenten und einer abschließenden menschlichen Prüfung erstellt.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
