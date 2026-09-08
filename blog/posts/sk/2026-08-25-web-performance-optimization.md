# Optimalizácia výkonu webu: Ako som znížil veľkosť stránok o 61 %

> **Published:** 2026-08-25  
> **Author:** Marian Stancik  
> **Summary:** Technický postup zníženia veľkosti HTML z 86 KB na 34 KB a dosiahnutie PageSpeed 100 cez externé CSS, JS, WebP a neblokujúci WebGL.

---

25. august 2026
  Výkonnosť webu
  Lighthouse 100
  Optimalizácia
  5 min čítania

### Optimalizácia výkonu webu: Ako som znížil veľkosť stránok o 61 % AI-generované

Ešte včera bolo skóre Lighthouse priemerné. Každá stránka prenášala 86 KB inline kódu. Po jednom popoludní systematickej optimalizácie — externalizácii CSS a JS, prechode na WebP, neblokujúcej WebGL architektúre a preconnect hlavičkách — veľkosť stránok klesla na 13–34 KB a skóre dosiahlo 100. Tu je presný návod, ako som to spravil pre marianstancik.dev.

### Predtým: Problém s inline monolitom

Každá podstránka niesla vlastnú kópiu celého CSS (~22 KB), Three.js neurónového pozadia (~5 KB modul) a kompletného i18n prekladového slovníka (~25 KB). Každý prechod medzi stránkami znamenal sťahovanie toho istého kódu nanovo. Ide o najčastejšiu chybu pri statických weboch.

  86 KBPôvodná veľkosť
  34 KBNová veľkosť
  −61 %Zníženie dát
  6×Rýchlejšia cache

### Optimalizačná stratégia

### 1. Extrakcia CSS do externého súboru

Najväčší posun. 22 KB CSS sa presunulo z inline blokov do jediného 
```
/css/main.css
```
. Prehliadač ho stiahne len raz, nacachuje a každá ďalšia podstránka sa načíta okamžite. HTML kleslo z 86 KB na 34 KB na hlavnej stránke a na ~13 KB na podstránkach.

```

```
<!-- Predtým: 22 KB inline v každom HTML -->
<style>
/* 22 KB CSS opakovaných na každej podstránke */
</style>

<!-- Potom: externé, cachované raz -->
<link rel="stylesheet" href="/css/main.css">
```

```

### 2. Externalizácia JavaScriptu (Three.js + i18n)

Dva kľúčové JS bloky boli oddelené: Three.js WebGL modul (odložený cez 
```
requestIdleCallback
```
 a interakčné triggery) a i18n preklady (načítané na konci 
```
<body>
```
). Tým sme dosiahli 0 ms Total Blocking Time (TBT).

```

```
<!-- Three.js — inicializované neblokujúco pri interakcii -->
<script type="module" src="/js/three-bg.js"></script>

<!-- i18n — načítané na konci body bez blokovania vykresľovania -->
<script src="/js/i18n.js"></script>
```

```

### 3. Moderný formát WebP pre obrázky

Profilová fotografia prešla z JPEG (15 KB) na WebP (9.9 KB) — úspora 34 % pri identickej vizuálnej kvalite. HTML využíva element 
```
<picture>
```
 s explicitným 
```
aspect-ratio: 1 / 1
```
, čo zaručuje nulový Cumulative Layout Shift (CLS = 0).

### 4. Preconnect a DNS-Prefetch pre CDN

Pridali sme 
```
<link rel="preconnect">
```
 pre jsDelivr CDN. Prehliadač vopred nadviaže DNS a TLS spojenie, čím ušetrí ~100–200 ms pri prvotnom načítaní.

### 5. Priorita načítania LCP (Largest Contentful Paint)

Profilový obrázok v hero sekcii je kľúčový LCP element. Pomocou 
```
fetchpriority="high"
```
 a 
```
loading="eager"
```
 má prednosť pred ostatnými zdrojmi.

```

```
<img src="/profile.webp" alt="Marian Stancik"
     width="200" height="200"
     loading="eager" fetchpriority="high">
```

```

### Výsledky

Po implementácii:

  
- Veľkosť stránok: 86 KB → 34 KB (hlavná stránka), ~68 KB → ~13–17 KB (podstránky).
  
- Úspora dát: ~320 KB naprieč webom pri prvej návšteve, okamžité načítanie pri ďalších.
  
- Cachovacia stratégia: CSS, JS a obrázky sú označené ako `immutable` na 1 rok.
  
- Blokovanie vlákna odstránené: TBT je 0 ms.
  
- PageSpeed skóre: 100/100 na mobile aj desktope.

Optimalizácia ukazuje silu Zero-Build architektúry (Vanilla HTML5, CSS3, moderný JS). Žiadne frameworkové balíky, žiadny runtime overhead — len čistý a ultra-rýchly web.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
