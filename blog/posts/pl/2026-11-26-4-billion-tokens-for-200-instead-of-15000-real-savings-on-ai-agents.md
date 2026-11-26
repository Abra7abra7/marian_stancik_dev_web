# 4 miliardy tokenów za 200 dolarów zamiast 15 000 dolarów: realne oszczędności na agentach AI

> **Published:** 2026-11-26  
> **Author:** Marian Stancik  
> **Summary:** Uruchamianie każdego zadania agenta na modelu klasy frontier to sposób, w jaki budżety po cichu znikają. Oto jak przekierowanie rutynowej pracy do DeepSeek przez OpenRouter obniżyło mój rachunek za tokeny o około 98%.

---

26 listopada 2026
  AI Agents
  6 min czytania
  Marian Stancik

### 4 miliardy tokenów za 200 dolarów zamiast 15 000 dolarów: realne oszczędności na agentach AI

W zeszłym roku moje agenty przetworzyły około 4 miliardów tokenów. Rachunek wyniósł około 200 USD. To samo obciążenie na modelu frontier najwyższej klasy wyniosłoby gdzieś około 15,000 USD. To nie jest sprytny hack — to jedna decyzja o routingu, podjęta raz, a potem mierzona przez dwanaście miesięcy.

### Gdzie naprawdę znikają pieniądze

Większość ludzi konfiguruje agenta, podłącza najdroższy model, jaki znajdzie, i nie zagląda do faktury, dopóki nie zaboli. Czat wydaje się tani, bo wysyłasz jedną wiadomość i dostajesz jedną odpowiedź. Agent tak nie działa.

Pojedyncze zadanie „napisz mi raport” może łatwo zamienić się w 40 do 80 wywołań modelu. Agent czyta plik, wywołuje narzędzie, ponownie odczytuje kontekst, ponawia nieudany krok, streszcza to, co znalazł, a następnie formatuje wynik. Każde z tych wywołań niesie ze sobą całą rozmowę. Twój koszt skaluje się z długością kontekstu, a nie z długością końcowej odpowiedzi.

Drugi wyciek to używanie modelu frontier do pracy, która go nie potrzebuje. Klasyfikowanie e-maila, wyodrębnianie trzech pól z faktury, przeformatowywanie JSON, decydowanie, które narzędzie wywołać następne — nic z tego nie wymaga najdroższego silnika rozumowania na rynku. Ale dokładnie to większość konfiguracji tam wysyła, bo to jest domyślne i nikt tego nie zmienia.

### Jak to routuję

Używam dwóch frameworków open source: Hermes Agent i OpenBot (alternatywa open source dla bota Grok). Oba komunikują się z modelami przez OpenRouter, który daje mi jeden klucz, wielu dostawców i logi poszczególnych żądań, które naprawdę mogę audytować.

- Poziom domyślny: DeepSeek V4/V4.1 Flash obsługuje około 82% mojego ruchu. GLM Flash odpowiada za około 10% — tania klasyfikacja, decyzje o routingu, krótkie streszczenia.

- Poziom frontier: zarezerwowany na trudne rozumowanie, niejednoznaczne decyzje i końcowy przegląd. To niewielki, jednocyfrowy odsetek wywołań.

- Buforowanie promptów: mój 12-miesięczny wskaźnik trafień cache wynosi 86.1%. Prompt systemowy i schematy narzędzi są stabilne, więc pełną cenę płacę tylko za część, która faktycznie się zmienia.

- Krótki kontekst: wyniki narzędzi są przycinane, stare tury są streszczane, a ja nigdy nie wrzucam całego pliku do okna, gdy wystarczyłyby trzy akapity.

Przez dwanaście miesięcy dało to 11.5 miliarda tokenów, 113K żądań i łącznie 416.19 USD — średnio 0.04 USD za milion tokenów. Hermes Agent odpowiadał za 6.67B z tych tokenów, OpenBot za 4.67B.

### Jak mierzyć ROI tokenów

Sama cena tokenów nic ci nie mówi. Liczy się koszt ukończonego zadania.

- Loguj każde żądanie: model, tokeny wejściowe, tokeny wyjściowe, tokeny z cache, koszt i ID zadania.

- Grupuj według ID zadania i obliczaj rzeczywisty koszt jednej ukończonej pracy.

- Porównaj to z minutami pracy człowieka, które zastąpiło. Zadanie, które kosztuje dwa centy i oszczędza sześć minut, to dobry interes. Zadanie, które kosztuje cztery dolary i oszczędza dwie minuty, już nie — niezależnie od tego, jak imponujący jest model.

- Co tydzień obserwuj wskaźnik trafień cache. Gdy spada, ktoś zwykle zmienił prompt systemowy albo dodał znacznik czasu na jego początku.

- Ustaw twardy miesięczny limit w OpenRouter. Nie dlatego, że planujesz go osiągnąć, ale dlatego, że agent uwięziony w pętli ponowień ochoczo wyda twój budżet przez noc.

### Gdzie się to psuje i na co uważać

Tanie modele są tańsze z jakiegoś powodu. DeepSeek Flash jest zauważalnie słabszy w długim wieloetapowym rozumowaniu i w subtelnym przestrzeganiu instrukcji. Zdarzyło mi się, że po cichu pominął ograniczenie, które wyraźnie ustawiłem. Tani model plus niedbały prompt równa się tanie śmieci, a i tak potrzebujesz małego zestawu przypadków testowych, żeby to wyłapać.

Buforowanie działa tylko wtedy, gdy prefiks promptu jest stabilny. Wstaw dynamiczny znacznik czasu na górze i stracisz większość oszczędności, nawet tego nie zauważając.

Opóźnienia i limity szybkości różnią się w zależności od dostawcy, więc wszystko, co jest widoczne dla użytkownika, potrzebuje trasy awaryjnej. A wysyłanie danych biznesowych do zewnętrznych dostawców to kwestia GDPR, a nie techniczna. Jestem studentem trzeciego roku prawa, nie prawnikiem — wszystko, co piszę o prywatności lub EU AI Act, to subiektywna uwaga, a do rzeczywistych decyzji potrzebujesz prawnika.

Jeszcze jedna rzecz warta powiedzenia wprost: ten artykuł i ta strona są przygotowywane z pomocą agentów AI, z końcową redakcyjną kontrolą człowieka. To szczera wersja, a także to, czego wymagają zasady przejrzystości EU AI Act.

### Podsumowanie

Routowanie rutynowej pracy do DeepSeek przez OpenRouter to największa dźwignia kosztowa, jaką znalazłem — około 98% mniej na rachunku, bez istotnej straty w zadaniach, które mają znaczenie. Mierz koszt na zadanie, a nie na token, i ustaw limit budżetu, zanim będzie potrzebny.

Jeśli chcesz omówić własną konfigurację, napisz do mnie na WhatsAppie pod numer +421 940 377 855. Darmowe narzędzia i prompty są pod 
```
/sk/tools/
```
.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
