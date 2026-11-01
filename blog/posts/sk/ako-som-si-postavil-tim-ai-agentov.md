# Ako som si postavil tím 14 špecializovaných AI agentov (a prečo jeden univerzálny asistent nestačil)

> **Published:** 2026-11-01  
> **Author:** Marian Stancik  
> **Summary:** Jeden univerzálny asistent zvláda úlohy, ale nie prácu. Rozpis tímu 14 špecializovaných agentov: role, tri pravidlá, ktoré držia tím pokope, a ako začať tromi agentmi.

---

Autor Marian Stancik
    ·
    1. novembra 2026
    ·
    10 min čítania
    AI agenti
    Tím AI agentov
    Multi-agent systém
    Chief of Staff
    Orkestrácia
    

  

### Ako som si postavil tím 14 špecializovaných AI agentov (a prečo jeden univerzálny asistent nestačil)

  

Priama odpoveď: Jeden univerzálny AI asistent zvládne úlohy, ale nie prácu. Ja nevediem jeden prompt, ale tím 14 špecializovaných agentov s jasne delenými rolami — výskum, právo, financie, kalendár, písanie textov — a nad nimi orkestrátora (Chief of Staff), ktorý úlohy rozdelí, skontroluje a spojí do jednej odpovede. V tomto článku rozpíšem, ako je tím postavený a aké tri pravidlá ho držia pokope.

  

Keď mi niekto povie, že používa ChatGPT ako asistent, väčšinou myslí jedno okno, do ktorého naleje desať rôznych úloh. Presne tak som začínal aj ja — a presne tak sa to končí: odpoveď na e-mail miešaná s hľadaním zmluvy, polovica úloh zabudnutá, kvalita závislá od toho, ako dobre sa práve popísal prompt.

  

Dnes nevediem jedno okno. Vedím tím štrnástich agentov. Každý má jednu rolu, jednu oblasť a jeden formát výstupu. Nad nimi stojí orkestrátor, ktorý berie zadanie, rozdelí ho, pošle správnemu agentovi a spojí výsledky do jednej odpovede. Nepíšem prompty — zadávam úlohy.

  

### Prečo nie jeden asistent
  

Univerzálny asistent je fajn na náčrt, ale keď v jednom kontexte rieši účtovníctvo, právnu analýzu aj text pre klienta, stráca hĺbku v každom z nich. Špecializácia je to isté, čo u ľudí: právnik nebalancuje knihy a účtovník nepíše uznesenia.
  

K problému sa pridávajú tri mechanické príčiny:
  
    
- Zmiešané roly. Rovnaká konverzácia nesie zadanie, argumenty aj finálny text. Kontext rastie, kvalita klesá.
    
- Strata kontextu. Dlhá konverzácia bez štruktúry zabúda skôr, než sa úloha dotiahne do konca.
    
- Nekonzistentná kvalita. Bez pevného formátu výstupu je každá odpoveď trochu iná — a kontrola kvality sa nedá delegovať.
  

  

### Ako vyzerá môj tím: role a delenie práce
  

Tím nie je zoznam chatbotov. Je to organizačná štruktúra, v ktorej má každý agent napísané aj to, čo nie je jeho práca. Hlavné roly:
  
    
- Chief of Staff (orkestrátor) — prijíma úlohy, rozdeľuje ich, kontroluje kvalitu a spája výsledky do jedného brífingu. Nič vágne sa ku mne nedostane.
    
- Výskum — prináša len aktuálne, overiteľné fakty so zdrojom a dátumom. „Pravdepodobne“ nemá vo výstupe miesto.
    
- Právo — pracuje s metódou: fakty → právny režim → subsumpcia → záver so zdrojmi. Nikdy si nevymyslí paragraf; návrhy kontroluje licencovaný právnik.
    
- Financie — počíta len z overených podkladov a účty rôznych subjektov drží striktne oddelené.
    
- Inbox a kalendár — triedia poštu a chránia rozvrh; nič neodosielajú ani nepresúvajú bez schválenia.
    
- Písanie (writer) — všetky odchádzajúce texty v jednom hlase, študovanom z reálnych odoslaných správ.
    
- Dokumenty, vývoj, marketing, dizajn, GitHub, sociálne siete, podpora — každý s vlastným rozsahom a vlastným formátom výstupu.
  
  

Celú mapu tímu, vrátane toho, čo každý agent robí deň za dňom, rozpísaná na stránke Ako to funguje.

  

### Pravidlo 1: jedna úloha = jeden vlastník
  

Ak dvaja agenti riešia tú istú vec, vznikajú dve pravdy. Preto má každá úloha presne jedného vlastníka. Keď zadanie spadá do dvoch oblastí — napríklad právny text, ktorý treba aj graficky spracovať — úloha putuje k jednému vlastníkovi a druhý dostane len podklady, nie paralelnú verziu tej istej práce.
  

Každý agent má v profile explicitne napísané, čo nie je jeho práca. To znie ako detail, ale je to jedna z vecí, ktoré najviac znižujú množstvo zbytočnej práce: úlohy neblúdia medzi agentmi, pretože každý vie, kedy má povedať „toto nie je moja úloha“ a odovzdať ju ďalej s plným kontextom.

  

### Pravidlo 2: formát výstupu
  

Každý agent vracia odpoveď v jednom formáte:
  
    
- Zhrnutie — kľúčové zistenia v krátkych bodoch.
    
- Návrh — konkrétny návrh, draft alebo ďalší krok.
    
- Čaká na rozhodnutie — jedna jasná otázka, na ktorú odpovieš áno/nie.
  
  

Človek neschvaľuje sto detailov, ale jednu otázku. A keďže je formát rovnaký pre všetkých agentov, kontrola je rýchla: vidím hneď, či je návrh konkrétny, či má zdroje a či je otázka zodpovedateľná jednoduchým áno/nie.

  

### Pravidlo 3: kontrola kvality medzi agentmi
  

Slabý výstup sa neopravuje ručne a neprijíma sa — vracia sa autorovi s jednou konkrétnou inštrukciou. Nie „skús to lepšie“, ale „pridaj produkty, termíny a vedenie so zdrojmi“. Iteruje sa, kým nie je výstup konkrétny, so zdrojmi a kompletný. Výstup bez zdrojov pre kľúčové tvrdenia nie je hotový.

  

### Čo mi to reálne dáva
  

Nemám merné jednotky typu „ušetrené hodiny“, a aj keby ich mal, neveril by som im. Kvalitatívne sa to dá popísať jednou vetou: namiesto desiatich rozpätých konverzácií dostávam jeden konsolidovaný výstup s jasnou otázkou na konci. Rozhodnutia trvajú minúty, nie večery, a nič sa nestratí medzi dvoma oknami chatu.

  

### Ako začať
  

Nepotrebuješ štrnásť agentov. Začni tromi: orkestrátor, jeden špecialista a pravidlo formátu. Keď to funguje, pridávaj ďalšie roly podľa toho, čo sa opakuje.
  Krok za krokom: Presné prompty — vrátane orkestrátora, formátu výstupu a pravidiel „čo agent nikdy nesmie urobiť“ — dávam zadarmo v AI Agent Starter Kite. A ak chceš vidieť, ako vyzerá celý tím v praxi, pozri ako tím funguje.
 
  

  
    

Chceš týždenné novinky o architektúre a governance autonómnych agentov?
    

Jeden email týždenne. Žiadny spam. Kedykoľvek sa odhlás.
    
      
      
      Odoberať
    
  

  

⚠️ AI-generated | Len info | marianstancik.dev/disclaimer

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
