// Shared bits for the Monolit round-2 prototypes (F/G/H). Prototype code — not production.
window.RM = matchMedia('(prefers-reduced-motion:reduce)').matches;

// B2 logo as a CSS-3D object. host = .world element. Returns {set(progress)}.
// progress 0 = assembled logo (white block breathing out at the front), 1 = blocks pulled apart.
window.Monolith = function (world, opts = {}) {
  const C = [{k:'b',x:1,z:0},{k:'b',x:0,z:0},{k:'b',x:1,z:1},{k:'w',x:0,z:1}];
  const faces = '<div class="f t"></div><div class="f bo"></div><div class="f fr"></div><div class="f bk"></div><div class="f r"></div><div class="f l"></div>';
  const els = C.map(c => { const d = document.createElement('div'); d.className = 'cube' + (c.k === 'w' ? ' w' : ''); d.innerHTML = faces; world.append(d); return d; });
  const css = getComputedStyle(world);
  let rx = -32, ry = 45, trx = -32, tr = 45, prog = 0, hi = -1;
  const base = opts.ry || 45;
  addEventListener('pointermove', e => { if (RM) return; trx = -32 + (e.clientY / innerHeight - .5) * -18; tr = base + (e.clientX / innerWidth - .5) * 40; });
  addEventListener('deviceorientation', e => { if (e.gamma == null) return; tr = base + e.gamma * .6; trx = -32 + (e.beta - 45) * -.3; });
  function frame() {
    const S = parseFloat(css.getPropertyValue('--S')), G = parseFloat(css.getPropertyValue('--G'));
    rx += (trx - rx) * .06; ry += (tr + prog * (opts.spin || 30) - ry) * .06;
    world.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg)`;
    els.forEach((el, i) => {
      const c = C[i]; let x = (c.x - .5) * G, z = (c.z - .5) * G, y = 0;
      const slide = c.k === 'w' ? (.18 + .06 * Math.sin(Date.now() / 900)) * G * (1 - prog) : 0;
      x -= slide; z += slide; x *= 1 + prog * 1.4; z *= 1 + prog * 1.4; y = -prog * [0.2, 0.8, 1.4, 2.2][i] * S * .5;
      const lift = hi === i ? -S * .35 : 0;
      el.style.transform = `translate3d(${x - S / 2}px,${y - S / 2 + lift}px,${z}px) rotateY(${c.k === 'w' ? prog * 90 : 0}deg)`;
      el.classList.toggle('hi', hi === i);
    });
    if (!RM) requestAnimationFrame(frame);
  }
  frame();
  return { set(p) { prog = p; if (RM) frame(); }, highlight(i) { hi = i; if (RM) frame(); } };
};

// Rack focus: photos start soft (bokeh) and pull into focus as they enter the viewport.
window.rackFocus = function (sel = '.rf') {
  const els = [...document.querySelectorAll(sel)];
  const upd = () => els.forEach(el => {
    const r = el.getBoundingClientRect(), vh = innerHeight;
    const p = Math.min(1, Math.max(0, (vh - r.top) / (vh * .6)));
    el.style.filter = RM ? 'none' : `blur(${(1 - p) * 14}px) saturate(${.7 + p * .3})`;
    el.style.transform = RM ? 'none' : `scale(${1.08 - p * .08})`;
  });
  addEventListener('scroll', upd, { passive: true }); addEventListener('resize', upd); upd();
};

// Magnetic buttons
window.magnetic = function (sel = '.mag') {
  document.querySelectorAll(sel).forEach(b => {
    b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); b.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * .18}px,${(e.clientY - r.top - r.height / 2) * .3}px)`; });
    b.addEventListener('pointerleave', () => b.style.transform = '');
  });
};
