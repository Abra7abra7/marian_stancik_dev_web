# Pięć testów, które przeprowadzam, zanim agent AI dotknie prawdziwej pracy

> **Published:** 2026-11-25  
> **Author:** Marian Stancik  
> **Summary:** Tani agent, który zawodzi po cichu, kosztuje więcej niż drogi, który się zatrzymuje. Pięć nudnych kontroli, które wykonuję, zanim powierzę mu prawdziwe zadanie.

---

25 listopada 2026
  AI Agents
  5 min czytania
  Marian Stancik

### Pięć testów, które przeprowadzam, zanim agent AI dotknie prawdziwej pracy

Pięć testów. Tyle zajmuje mi podjęcie decyzji, czy agent AI dostanie dostęp do prawdziwych zadań, czy zostanie w sandboxie. Żadnych benchmarków, żadnych zrzutów ekranu z rankingów — pięć nudnych testów, które kosztują kilka dolarów i jedno popołudnie.

### Dlaczego większość ludzi testuje agentów w niewłaściwy sposób

Większość ludzi ocenia agenta po jego demo. Wpisujesz ładne pytanie, on ładnie odpowiada, wszyscy kiwają głowami. Problem w tym, że demo działa na czystej ścieżce: idealne dane wejściowe, żadnych brakujących pól, żadnego na wpół zepsutego API, nikt nie czeka po drugiej stronie.

Prawdziwa praca jest chaotyczna. Przychodzi formularz z pustym polem VAT. W skrzynce odbiorczej jest wiadomość w trzech językach. API zwraca 200 OK z błędem ukrytym w treści odpowiedzi. Agent, który radzi sobie z demo, a potem po cichu zawodzi na chaotycznej wersji, jest gorszy niż brak agenta — bo przestajesz sprawdzać.

Koszt to nie tokeny. Kosztem jest e-mail, który nigdy nie został wysłany, faktura z błędnym numerem, klient, który czekał dwa dni na odpowiedź, którą agent rzekomo obsłużył.

### Jak testuję agenta, zanim dotknie czegokolwiek prawdziwego

Buduję na frameworkach open source — głównie Hermes Agent i OpenBot (alternatywa open source dla Grok bot) — i kieruję model przez DeepSeek on OpenRouter. Ten zestaw jest wystarczająco tani, że testowanie jest praktycznie darmowe. Oto rutyna.

- 1. Test pustego wejścia. Nie wysyłam nic. Potem pojedynczą spację. Potem 40-stronicowy PDF. Potem plik z niewłaściwym rozszerzeniem. Jeśli agent wymyśla odpowiedź zamiast się zatrzymać, oblewa test.

- 2. Test zatrzymania się i zapytania. Daję mu zadanie z jednym celowo brakującym szczegółem — datą, kwotą, odbiorcą. Dobry agent pyta. Zły agent pewnie zgaduje, a pewne zgadywanie to najdroższe zachowanie w całym systemie.

- 3. Koszt ukończonego zadania, nie tokenu. Ceny tokenów odwracają uwagę. Liczy się to, ile kosztuje jedno ukończone zadanie. W zeszłym miesiącu przepuściłem przez DeepSeek na OpenRouter około 4 miliardów tokenów za około $200. Ta sama objętość na najdroższych modelach frontierowych wyniosłaby blisko $15,000. Wniosek jest ten sam w obu przypadkach: mierz ukończoną pracę, nie rachunek.

- 4. Test powtarzalności. Uruchamiam to samo zadanie dziesięć razy i porównuję wyniki. Jeśli struktura zmienia się przy każdym uruchomieniu, agent nie jest gotowy na nic, co zasila bazę danych lub trafia do klienta.

- 5. Test cofania. Zanim cokolwiek zapisze, wyśle lub usunie, potrzebuję trybu dry-run i logu, który naprawdę mogę przeczytać. Jeśli nie mogę tego odwrócić, nie włączam tego.

Nic z tego nie jest sprytne. To ta sama dyscyplina, którą zastosowałbyś wobec nowego pracownika w jego pierwszym tygodniu — z tą różnicą, że pracownik nigdy się nie męczy i nigdy nie uczy się na zawstydzeniu.

### Gdzie to zawodzi

Zaliczenie pięciu testów oznacza, że agent działał w dniu, w którym go testowałeś. Nie oznacza, że działa w trzecim tygodniu. Modele są aktualizowane, prompty gniją, nadrzędne API zmienia nazwę jednego pola i cały łańcuch po cichu produkuje śmieci, które wciąż wyglądają na poprawnie sformatowane.

Testy są więc migawką, a nie certyfikatem. Tanie testy uruchamiam ponownie co tydzień, a przy wszystkim, co opuszcza budynek, utrzymuję człowieka w pętli. AI to narzędzie, nie magia — a narzędzie wymaga konserwacji.

Jeszcze dwa uczciwe ograniczenia. Po pierwsze, nie mogę testować tego, czego nie umiem zmierzyć, a wiele zadań (pisanie, ocena, ton) nie poddaje się czystemu pomiarowi. Po drugie, jeśli twój agent dotyka danych osobowych lub podlega unijnemu AI Act, moje uwagi są dokładnie tym — subiektywnymi obserwacjami studenta trzeciego roku prawa. Nie jestem prawnikiem i nie udzielam porad prawnych. Skonsultuj się z prawnikiem.

### Podsumowanie

Testuj nudne porażki, nie imponujące sukcesy. Puste dane wejściowe, brakujący szczegół, powtarzalność, koszt ukończonego zadania i sposób na cofnięcie — to cała lista kontrolna, która zaoszczędziła mi więcej pieniędzy niż jakiekolwiek porównanie modeli.

Jeśli chcesz przejrzeć własną konfigurację, napisz do mnie na WhatsAppie pod numer +421 940 377 855 lub skorzystaj z darmowych narzędzi pod /sk/tools/. Ten artykuł, podobnie jak reszta strony, jest przygotowywany z pomocą agentów AI i końcowej weryfikacji przez człowieka.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
