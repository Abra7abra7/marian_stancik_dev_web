/**
 * Three.js Ambient Particle Background
 * Non-blocking, mobile-optimized, adaptive WebGL neural network visualizer
 * Mobile: skipped entirely (CSS gradient fallback) — 0 TBT
 */

const _isMobile = window.innerWidth < 768 || ('ontouchstart' in window && window.innerWidth < 1024);
const _lowEndDevice = (navigator.hardwareConcurrency || 8) < 4;
const _prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Skip on mobile / low-end hardware / reduced motion (saves 250KB download + 2.5s TBT)
// The seamless fixed body background provides the visual backdrop without any cutoff


async function initThreeBackground() {
  if (_isMobile || _lowEndDevice || _prefersReducedMotion) return;
  const canvas = document.getElementById('three-canvas');
  if (!canvas) return;

  // Check WebGL support on a throwaway canvas — calling getContext('webgl') on the real
  // canvas would lock it to WebGL1 and make three.js fail with
  // "Canvas has an existing context of a different type" when it requests WebGL2.
  const probe = document.createElement('canvas');
  const gl = probe.getContext('webgl2') || probe.getContext('webgl');
  if (!gl) return;
  const loseProbe = gl.getExtension('WEBGL_lose_context');
  if (loseProbe) loseProbe.loseContext();

  try {
    // Dynamic import — no importmap in HTML, avoid early pre-fetch of 250KB
    const THREE = await import('https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js');

    const isMobile = window.innerWidth < 768;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 45;

    const renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: !isMobile,
      powerPreference: 'high-performance'
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, isMobile ? 1.5 : 2));

    // Particle count: 220 on mobile, 650 on desktop
    const count = isMobile ? 220 : 650;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      const r = 30 + Math.random() * 40;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);

      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.cos(phi) * Math.sin(theta * 0.5);
      positions[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);

      const bronze = new THREE.Color().setHSL(0.08, 0.4, 0.3 + Math.random() * 0.35);
      colors[i * 3] = bronze.r;
      colors[i * 3 + 1] = bronze.g;
      colors[i * 3 + 2] = bronze.b;
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: isMobile ? 0.16 : 0.12,
      vertexColors: true,
      transparent: true,
      opacity: 0.6,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      sizeAttenuation: true
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // Efficient Line Connections - Linear Sampling O(N)
    const linePositions = [];
    const maxLineDist = 12;
    const maxLineDistSq = maxLineDist * maxLineDist;
    const lineStep = isMobile ? 4 : 2;

    for (let i = 0; i < count; i += lineStep) {
      // Connect to a few adjacent particles rather than checking all N^2 pairs
      const neighbors = Math.min(i + 12, count);
      for (let j = i + 1; j < neighbors; j++) {
        const dx = positions[i * 3] - positions[j * 3];
        const dy = positions[i * 3 + 1] - positions[j * 3 + 1];
        const dz = positions[i * 3 + 2] - positions[j * 3 + 2];
        const distSq = dx * dx + dy * dy + dz * dz;

        if (distSq < maxLineDistSq) {
          linePositions.push(positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2]);
          linePositions.push(positions[j * 3], positions[j * 3 + 1], positions[j * 3 + 2]);
        }
      }
    }

    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
    const lines = new THREE.LineSegments(
      lineGeo,
      new THREE.LineBasicMaterial({ color: 0xA27B50, transparent: true, opacity: 0.08 })
    );
    scene.add(lines);

    // Floating neural nodes
    const nodeCount = isMobile ? 12 : 30;
    const nodeMat = new THREE.MeshBasicMaterial({ color: 0xEBC37D, transparent: true, opacity: 0.15 });
    const nodeGeom = new THREE.SphereGeometry(0.3, 6, 6);
    const nodes = [];

    for (let i = 0; i < nodeCount; i++) {
      const mesh = new THREE.Mesh(nodeGeom, nodeMat.clone());
      const idx = Math.floor(Math.random() * count);
      mesh.position.set(positions[idx * 3], positions[idx * 3 + 1], positions[idx * 3 + 2]);
      mesh.userData = {
        baseX: positions[idx * 3],
        baseY: positions[idx * 3 + 1],
        baseZ: positions[idx * 3 + 2],
        speed: 0.2 + Math.random() * 0.5
      };
      scene.add(mesh);
      nodes.push(mesh);
    }

    // Pointer parallax
    let mouseX = 0, mouseY = 0;
    if (!isMobile) {
      document.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX / window.innerWidth) * 2 - 1;
        mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
      }, { passive: true });
    }

    // Resize handler with debounce
    let resizeTimeout;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      }, 150);
    }, { passive: true });

    let time = 0;
    let isAnimating = true;

    function animate() {
      if (!isAnimating) return;
      requestAnimationFrame(animate);

      time += 0.001;
      particles.rotation.y += 0.0003;
      lines.rotation.y += 0.0003;

      for (let i = 0; i < nodes.length; i++) {
        const node = nodes[i];
        const d = node.userData;
        node.position.x = d.baseX + Math.sin(time * d.speed + i) * 1.5;
        node.position.y = d.baseY + Math.cos(time * d.speed * 0.7 + i * 0.5) * 1.5;
        node.position.z = d.baseZ + Math.sin(time * d.speed * 0.5 + i * 0.3) * 1.5;
        node.material.opacity = 0.08 + Math.sin(time * 2 + i) * 0.06;
      }

      if (!isMobile) {
        particles.rotation.x += (mouseY * 0.02 - particles.rotation.x) * 0.02;
        particles.rotation.y += (mouseX * 0.02 - particles.rotation.y) * 0.02;
        lines.rotation.x = particles.rotation.x;
        lines.rotation.y = particles.rotation.y;
      }

      renderer.render(scene, camera);
    }

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        isAnimating = false;
      } else {
        if (!isAnimating && !prefersReducedMotion) {
          isAnimating = true;
          animate();
        }
      }
    });

    if (prefersReducedMotion) {
      renderer.render(scene, camera);
    } else {
      animate();
    }
  } catch (err) {
    // Graceful fallback if WebGL or Three.js fails to load
    console.warn('Three.js background initialization skipped:', err);
  }
}

// User-interaction or deferred idle initialization (0ms TBT during critical load)
let initialized = false;
function triggerInit() {
  if (initialized || _isMobile || _lowEndDevice || _prefersReducedMotion) return;
  initialized = true;
  cleanupListeners();
  if ('requestIdleCallback' in window) {
    requestIdleCallback(initThreeBackground);
  } else {
    setTimeout(initThreeBackground, 50);
  }
}

function cleanupListeners() {
  window.removeEventListener('scroll', triggerInit, { passive: true });
  window.removeEventListener('mousemove', triggerInit, { passive: true });
  window.removeEventListener('touchstart', triggerInit, { passive: true });
  window.removeEventListener('pointerdown', triggerInit, { passive: true });
  window.removeEventListener('keydown', triggerInit, { passive: true });
}

if (!_isMobile && !_lowEndDevice && !_prefersReducedMotion) {
  window.addEventListener('scroll', triggerInit, { passive: true, once: true });
  window.addEventListener('mousemove', triggerInit, { passive: true, once: true });
  window.addEventListener('touchstart', triggerInit, { passive: true, once: true });
  window.addEventListener('pointerdown', triggerInit, { passive: true, once: true });
  window.addEventListener('keydown', triggerInit, { passive: true, once: true });

  // Fallback idle timeout if no interaction occurs
  setTimeout(triggerInit, 2500);
}

