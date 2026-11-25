/**
 * Lightweight 2D Canvas Ambient Constellation Background
 * Zero external dependencies (replaces ~650KB Three.js CDN bundle).
 * Mobile / low-end / reduced-motion: skipped completely (0 ms TBT).
 * Automatically pauses when tab is hidden to save laptop battery.
 */
(function initAmbientCanvas() {
  const isMobile = window.innerWidth < 768 || ('ontouchstart' in window && window.innerWidth < 1024);
  const lowEnd = (navigator.hardwareConcurrency || 8) < 4;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (isMobile || lowEnd || reducedMotion) return;

  const canvas = document.getElementById('three-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  let w = 0;
  let h = 0;
  let rafId = 0;
  const COUNT = 48;
  const MAX_DIST = 140;
  const pts = [];

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  resize();
  for (let i = 0; i < COUNT; i++) {
    pts.push({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.28,
      vy: (Math.random() - 0.5) * 0.28,
      r: Math.random() * 1.4 + 0.6,
      gold: Math.random() > 0.45
    });
  }

  let mx = -9999;
  let my = -9999;
  window.addEventListener('mousemove', (e) => { mx = e.clientX; my = e.clientY; }, { passive: true });
  window.addEventListener('resize', resize, { passive: true });

  function draw() {
    if (document.hidden) {
      rafId = 0;
      return;
    }
    ctx.clearRect(0, 0, w, h);

    for (let i = 0; i < COUNT; i++) {
      const p = pts[i];
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > w) p.vx *= -1;
      if (p.y < 0 || p.y > h) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.gold ? 'rgba(235, 195, 125, 0.55)' : 'rgba(148, 174, 206, 0.35)';
      ctx.fill();

      for (let j = i + 1; j < COUNT; j++) {
        const q = pts[j];
        const dx = p.x - q.x;
        const dy = p.y - q.y;
        const dist = Math.hypot(dx, dy);
        if (dist < MAX_DIST) {
          const alpha = (1 - dist / MAX_DIST) * 0.14;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(q.x, q.y);
          ctx.strokeStyle = `rgba(205, 127, 50, ${alpha.toFixed(3)})`;
          ctx.lineWidth = 0.7;
          ctx.stroke();
        }
      }

      const mdx = p.x - mx;
      const mdy = p.y - my;
      const mdist = Math.hypot(mdx, mdy);
      if (mdist < 160) {
        const alpha = (1 - mdist / 160) * 0.22;
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(mx, my);
        ctx.strokeStyle = `rgba(235, 195, 125, ${alpha.toFixed(3)})`;
        ctx.lineWidth = 0.8;
        ctx.stroke();
      }
    }

    rafId = requestAnimationFrame(draw);
  }

  document.addEventListener('visibilitychange', () => {
    if (!document.hidden && !rafId) rafId = requestAnimationFrame(draw);
  });

  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => { rafId = requestAnimationFrame(draw); }, { timeout: 1200 });
  } else {
    setTimeout(() => { rafId = requestAnimationFrame(draw); }, 250);
  }
})();
