# Jak testuję agenta AI, zanim dopuszczę go do prawdziwej pracy

> **Published:** 2026-11-25  
> **Author:** Marian Stancik  
> **Summary:** Agent, który działa w demo, i agent, który działa w poniedziałek rano, to dwie różne rzeczy. Oto pięć kontroli, które przeprowadzam, zanim jakikolwiek agent dostanie prawdziwą pracę.

---

25 listopada 2026
  AI Agents
  6 min czytania
  Marian Stancik

### Jak testuję agenta AI, zanim dopuszczę go do prawdziwej pracy

Agent, który działa w demo, i agent, który działa w zwykły poniedziałkowy poranek, to dwie różne rzeczy. Zanim pozwolę jakiemukolwiek agentowi zabrać się za prawdziwą pracę, przechodzi on przez pięć kontroli. Większość z nich zajmuje mniej niż dziesięć minut i oszczędza godziny późniejszego sprzątania.

### Problem: oceniamy agentów po demo

Niemal każdego agenta, którego widzę prezentowanego online, pokazuje się w ten sam sposób: jedno czyste wejście, przyjazny przykład, człowiek patrzący na ekran. Wygląda świetnie. Potem podłączasz go do prawdziwej skrzynki odbiorczej, prawdziwego arkusza kalkulacyjnego albo prawdziwego zapytania klienta i wszystko się rozpada — nie z hukiem, ale po cichu.

Cicha awaria jest tym kosztownym rodzajem. Agent mówi „gotowe”, wpisuje na wpół poprawny wiersz do twojego arkusza, wysyła odpowiedź z niewłaściwym imieniem albo zapętla to samo wywołanie narzędzia piętnaście razy. Nikt tego nie zauważa przez tydzień.

Koszt pogarsza sprawę. Przepuszczam około 4 miliardów tokenów miesięcznie za mniej więcej $200 przez DeepSeek w OpenRouter. Ten sam wolumen na najdroższych modelach frontier kosztowałby około $15,000. Tanie tokeny są świetne, ale oznaczają też, że zapętlający się agent nie powoduje natychmiastowych szkód — więc błędne wyniki przetrwają dłużej, zanim ktokolwiek je wychwyci.

### Jak testuję agentów, zanim dostaną prawdziwą pracę

Buduję na frameworkach open source — głównie Hermes Agent i OpenBot (alternatywa open source dla bota Grok) — z DeepSeek przez OpenRouter do taniej iteracji. Pięć poniższych kontroli jest takich samych niezależnie od frameworka.

- 1. Zacznij od najbrzydszego wejścia, jakie masz. Nie przykład wpisany ręcznie — prawdziwy zrzut ekranu, na wpół napisany e-mail, PDF z tabelą, której nie da się sparsować. Jeśli agent działa tylko z idealnym wejściem, zbudowałeś skrypt, a nie agenta.

- 2. Uruchom go dwa razy na tym samym wejściu. To samo zadanie, te same dane, dwa razy. Jeśli odpowiedzi się różnią, dowiedz się dlaczego, zanim mu zaufasz: temperatura, kolejność narzędzi, znacznik czasu ukryty w prompcie. Niedeterminizm nie jest automatycznie zły, ale niewyjaśniony niedeterminizm jest.

- 3. Odbierz jedno narzędzie. Odłącz jedno API albo unieważnij jeden klucz i uruchom zadanie ponownie. Dobry agent zawodzi głośno i mówi, czego brakuje. Zły wymyśla odpowiedź. Głośna porażka to funkcja, której chcesz.

- 4. Licz kroki i tokeny. Rejestruj każde wywołanie narzędzia. Proste zadanie, które zajmuje czternaście kroków, zwykle oznacza niejasny prompt albo źle napisany opis narzędzia, a nie trudne zadanie.

- 5. Przeczytaj wynik jak ktoś z zewnątrz. Czy współpracownik, który nie zna twojej konfiguracji, zrozumiałby wynik bez pytania cię? Jeśli nie, agent nie jest gotowy — po prostu przeniósł pracę na kogoś innego.

Nic z tego nie wymaga frameworka testowego ani potoku CI. Wymaga dwudziestu minut i gotowości, by nie dać się zachwycić.

### Gdzie to zawodzi i na co uważać

Uczciwe ograniczenia: pięć kontroli nie obejmuje prawdziwego świata. Agent może przejść wszystkie i nadal zepsuć się we wtorek, gdy strona zmieni swój HTML albo klient wyśle coś, czego nigdy nie widziałeś. Testy zmniejszają niespodzianki; nie usuwają ich.

Dwie kolejne pułapki, w które wpadłem:

- Testowanie na innym modelu niż ten, na którym wdrażasz. Tanie modele do iteracji są w porządku, ale zachowanie zmienia się między modelami. Końcowa kontrola musi zostać uruchomiona na modelu, który faktycznie wykonuje pracę.

- Nieświadome niańczenie. Jeśli zawsze jesteś w pobliżu, żeby go popchnąć, nie testujesz agenta — testujesz siebie. Zostaw go samego na jeden dzień i zobacz, co się stanie.

A strona prawna: jeśli twój agent dotyka danych osobowych, w grę wchodzą GDPR i EU AI Act. Jestem studentem trzeciego roku prawa, nie prawnikiem — wszystko, co piszę o regulacjach, jest subiektywną uwagą, a do prawdziwych decyzji potrzebujesz adwokata.

### Podsumowanie

AI to narzędzie, nie magia. Różnica między agentem, który oszczędza ci czas, a takim, który po cichu robi bałagan, zwykle nie tkwi w modelu — tkwi w tym, czy najpierw spędziłeś dwadzieścia minut, próbując go zepsuć.

Jeśli chcesz wymienić się uwagami na temat testowania własnej konfiguracji, napisz do mnie przez WhatsApp pod numer +421 940 377 855, albo wypróbuj darmowe narzędzia na /en/tools/. Ten artykuł i strona są przygotowywane przy użyciu agentów AI i końcowej weryfikacji przez człowieka.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
