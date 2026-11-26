# 4 Milliarden Tokens für $200 statt $15,000: Echte Einsparungen bei KI-Agenten

> **Published:** 2026-11-26  
> **Author:** Marian Stancik  
> **Summary:** Wenn jede Agent-Aufgabe auf einem Frontier-Modell läuft, verschwinden Budgets ganz leise. Hier ist, wie das Routen von Routinearbeit zu DeepSeek über OpenRouter meine Token-Rechnung um rund 98 % gesenkt hat.

---

26. November 2026
  AI Agents
  6 Min. Lesezeit
  Von Marian Stancik

### 4 Milliarden Tokens für $200 statt $15,000: Echte Einsparungen bei KI-Agenten

Letztes Jahr haben meine Agenten etwa 4 Milliarden Token verarbeitet. Die Rechnung lag bei etwa 200 USD. Dieselbe Arbeitslast auf einem Top-Tier-Frontier-Modell wäre irgendwo bei 15,000 USD gelandet. Das ist kein cleverer Hack — es ist eine Routing-Entscheidung, einmal getroffen und dann zwölf Monate lang gemessen.

### Wo das Geld tatsächlich verschwindet

Die meisten Leute richten einen Agenten ein, schließen das teuerste Modell an, das sie finden können, und schauen sich die Rechnung erst an, wenn es wehtut. Chat wirkt günstig, weil du eine Nachricht sendest und eine Antwort bekommst. Ein Agent funktioniert nicht so.

Eine einzelne Aufgabe wie „Schreib mir einen Bericht“ kann leicht zu 40 bis 80 Modellaufrufen werden. Der Agent liest eine Datei, ruft ein Tool auf, liest den Kontext erneut, wiederholt einen fehlgeschlagenen Schritt, fasst zusammen, was er gefunden hat, und formatiert dann die Ausgabe. Jeder dieser Aufrufe trägt die gesamte Konversation mit sich. Deine Kosten skalieren mit der Kontextlänge, nicht mit der Länge der endgültigen Antwort.

Das zweite Leck ist der Einsatz eines Frontier-Modells für Arbeit, die keines braucht. Eine E-Mail zu klassifizieren, drei Felder aus einer Rechnung zu extrahieren, JSON neu zu formatieren, zu entscheiden, welches Tool als Nächstes aufgerufen wird — nichts davon erfordert die teuerste Reasoning-Engine auf dem Markt. Aber genau das schicken die meisten Setups dorthin, weil es der Standard ist und niemand ihn ändert.

### Wie ich es route

Ich betreibe zwei Open-Source-Frameworks: Hermes Agent und OpenBot (eine Open-Source-Alternative zum Grok bot). Beide kommunizieren über OpenRouter mit Modellen, was mir einen Schlüssel, viele Anbieter und Protokolle pro Anfrage gibt, die ich tatsächlich prüfen kann.

- Standard-Stufe: DeepSeek V4/V4.1 Flash verarbeitet etwa 82% meines Traffics. GLM Flash übernimmt ungefähr 10% — günstige Klassifizierung, Routing-Entscheidungen, kurze Zusammenfassungen.

- Frontier-Stufe: reserviert für schwieriges Reasoning, mehrdeutige Entscheidungen und den abschließenden Review-Durchgang. Das ist ein kleiner einstelliger Prozentsatz der Aufrufe.

- Prompt-Caching: Meine Cache-Trefferquote über 12 Monate liegt bei 86.1%. Der System-Prompt und die Tool-Schemas sind stabil, daher zahle ich den vollen Preis nur für den Teil, der sich tatsächlich ändert.

- Kurzer Kontext: Tool-Ausgaben werden gekürzt, alte Turns werden zusammengefasst, und ich kippe niemals eine ganze Datei ins Fenster, wenn drei Absätze ausreichen.

Über zwölf Monate ergab das 11.5 Milliarden Token, 113K Anfragen und insgesamt 416.19 USD — ein durchschnittlicher Preis von 0.04 USD pro Million Token. Auf Hermes Agent entfielen 6.67B dieser Token, auf OpenBot 4.67B.

### So misst man den Token-ROI

Der Token-Preis allein sagt dir nichts. Entscheidend sind die Kosten pro abgeschlossener Aufgabe.

- Protokolliere jede Anfrage: Modell, Input-Token, Output-Token, gecachte Token, Kosten und eine Task-ID.

- Gruppiere nach Task-ID und berechne die tatsächlichen Kosten einer abgeschlossenen Arbeitseinheit.

- Vergleiche das mit den menschlichen Minuten, die es ersetzt hat. Eine Aufgabe, die zwei Cent kostet und sechs Minuten spart, ist ein guter Deal. Eine Aufgabe, die vier Dollar kostet und zwei Minuten spart, ist keiner, egal wie beeindruckend das Modell ist.

- Beobachte die Cache-Trefferquote wöchentlich. Wenn sie sinkt, hat jemand normalerweise den System-Prompt geändert oder oben einen Zeitstempel hinzugefügt.

- Setze in OpenRouter eine harte monatliche Obergrenze. Nicht weil du planst, sie zu erreichen, sondern weil ein Agent, der in einer Retry-Schleife feststeckt, dein Budget über Nacht fröhlich ausgeben wird.

### Wo es bricht und worauf man achten sollte

Günstige Modelle sind aus einem Grund günstiger. DeepSeek Flash ist merklich schwächer bei langem mehrstufigem Reasoning und beim Befolgen subtiler Anweisungen. Es hat mir schon stillschweigend eine Einschränkung fallen lassen, die ich ausdrücklich gesetzt hatte. Günstiges Modell plus schlampiger Prompt ergibt günstigen Müll, und du brauchst trotzdem eine kleine Sammlung von Testfällen, um das zu erkennen.

Caching funktioniert nur, wenn dein Prompt-Präfix stabil ist. Setze oben einen dynamischen Zeitstempel ein, und du verlierst die meisten Einsparungen, ohne es zu merken.

Latenz und Rate-Limits variieren je nach Anbieter, daher braucht alles, was nutzerseitig sichtbar ist, eine Fallback-Route. Und das Senden von Geschäftsdaten an Drittanbieter ist eine DSGVO-Frage, keine technische. Ich bin Jurastudent im dritten Jahr, kein Anwalt — alles, was ich über Datenschutz oder den EU AI Act schreibe, ist eine subjektive Anmerkung, und für echte Entscheidungen brauchst du einen Anwalt.

Noch etwas, das klar gesagt werden sollte: Dieser Artikel und diese Website werden mit KI-Agenten erstellt, unter abschließender menschlicher redaktioneller Kontrolle. Das ist die ehrliche Version, und es ist auch das, was die Transparenzregeln des EU AI Act verlangen.

### Fazit

Routinearbeit über OpenRouter an DeepSeek zu routen, ist der größte Kostenhebel, den ich gefunden habe — ungefähr 98% weniger Rechnung, ohne nennenswerte Verluste bei den Aufgaben, die zählen. Miss die Kosten pro Aufgabe, nicht pro Token, und begrenze das Budget, bevor du es brauchst.

Wenn du dein eigenes Setup durchsprechen möchtest, schreib mir auf WhatsApp unter +421 940 377 855. Kostenlose Tools und Prompts findest du unter 
```
/sk/tools/
```
.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
