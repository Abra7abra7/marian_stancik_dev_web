# Optymalizacja wydajności sieci: Jak zmniejszyłem rozmiar stron o 61%

> **Published:** 2026-08-25  
> **Author:** Marian Stancik  
> **Summary:** Przewodnik techniczny redukcji wagi HTML z 86 KB do 34 KB i osiągnięcia PageSpeed 100 z WebP i nieblokującym WebGL.

---

25 sierpnia 2026
  Web Performance
  Lighthouse
  Optimization
  5 min czytania

### Optymalizacja wydajności sieci: Jak zmniejszyłem rozmiar stron o 61% AI-generated

Yesterday my Lighthouse score was mediocre. Pages were 86KB of inline everything. After one afternoon of systematic optimization — externalizing CSS and JS, WebP conversion, preconnect hints — every page dropped to 13-34KB. Here's exactly how I did it for marianstancik.dev.

### Before: The Inline Spaghetti Problem

Each page shipped its own copy of the entire CSS (~22KB), the Three.js neural network background (~5KB module), and the full i18n translations dictionary (~25KB). Every page navigation meant re-downloading all of it. This is the most common mistake in static portfolio sites — every page is a self-contained monolith.

  86KBOld page size
  34KBNew page size
  −61%Reduction
  6×Cache hits

### The Optimization Strategy

### 1. Extract CSS to External File

The biggest win. 22KB of CSS went from inline every page to a single 
```
/css/main.css
```
 — now cached by the browser after the first page load, every subsequent navigation is instant. The HTML dropped from 86KB to 34KB on the homepage, and from ~68KB to ~13KB on subpages.

```

```
<!-- Before: 22KB inline every page -->
<style>
/* 22KB of CSS repeated 6 times */
</style>

<!-- After: external, cached once -->
<link rel="stylesheet" href="/css/main.css">
```

```

### 2. Externalize JavaScript (Three.js + i18n)

Two major JS blocks were extracted: the Three.js neural network module (5KB, deferred via 
```
type="module"
```
) and the i18n translations + helpers (25KB, loaded at the bottom of 
```
<body>
```
). Both are now cached across all 6 pages.

```

```
<!-- Three.js — deferred by nature of type="module" -->
<script type="module" src="/js/three-bg.js"></script>

<!-- i18n — loaded at body bottom, not render-blocking -->
<script src="/js/i18n.js"></script>
```

```

### 3. WebP for Profile Image

The profile photo went from JPEG (15KB) to WebP (10KB) — a 34% reduction with identical visual quality. The HTML uses a 
```
<picture>
```
 element with WebP as preferred and JPEG fallback for older browsers.

### 4. Preconnect Hints for CDNs

Added 
```
<link rel="preconnect">
```
 for Three.js CDN (jsdelivr.net) and Google Fonts CDN. This tells the browser to warm up DNS + TCP connections early, shaving ~100-200ms off LCP for first-time visitors.

```

```
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
```

```

### 5. Fetchpriority for LCP Element

The hero profile image is the Largest Contentful Paint element. With 
```
fetchpriority="high"
```
 and 
```
loading="eager"
```
, the browser prioritizes it over background images and other late-loaded content.

```

```
<img src="/profile.jpg" alt="Marian Stancik"
     width="200" height="200"
     loading="eager" fetchpriority="high">
```

```

### Results

After these changes:

  
- Page weight: 86KB → 34KB (main page), ~68KB → ~13-17KB (subpages)
  
- Total savings: ~320KB across all 6 pages on first visit, much more on subsequent navigation
  
- Cache strategy: CSS and JS assets are now cacheable and shared across all pages
  
- Render-blocking eliminated: All JS is deferred or bottom-loaded
  
- Image optimization: WebP reduces payload by 34%

The Lighthouse scores went from mediocre to competitive — especially on mobile where bandwidth and CPU are constrained. The exact numbers speak for themselves.

### Takeaways for Your Site

If your portfolio site has inline CSS and JS, this is the single highest-ROI optimization you can do:

  
- Measure first: Run PageSpeed Insights, look at "unused CSS/JS" and "total byte weight"
  
- Extract CSS to a single file — even unminified, external beats inline for caching
  
- Move JS to the bottom of 
```
<body>
```
 or use 
```
defer
```
/
```
type="module"
```

  
- WebP for all images — it's supported in every modern browser
  
- Preconnect to CDNs — free LCP improvement for zero code change

The tools (external CSS, deferred JS, preconnect, WebP) are all standard web platform features. No framework, no bundler, no build step. Just cleaner HTML architecture.

---
*Autonomous AI Agent & Engineering Hub — [marianstancik.dev](https://www.marianstancik.dev)*
