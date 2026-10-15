// DataMatrix rotating looks — shared JS (production port of look-prototypes monolit.js + r3.js).
// No cookies, no storage, no network. Every effect respects prefers-reduced-motion.
(() => {
  const RM = matchMedia("(prefers-reduced-motion:reduce)").matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Header gets a background after a little scroll (inner pages start solid).
  const hd = $(".site-header");
  if (hd && !hd.classList.contains("solid")) {
    const f = () => hd.classList.toggle("sc", scrollY > 40);
    addEventListener("scroll", f, { passive: true }); f();
  }

  // 3D B2 logo. progress 0 = assembled (white block breathing out), 1 = pulled apart while scrolling.
  function Monolith(world, opts = {}) {
    const C = [{ k: "b", x: 1, z: 0 }, { k: "b", x: 0, z: 0 }, { k: "b", x: 1, z: 1 }, { k: "w", x: 0, z: 1 }];
    const faces = '<div class="f t"></div><div class="f bo"></div><div class="f fr"></div><div class="f bk"></div><div class="f r"></div><div class="f l"></div>';
    const els = C.map((c) => { const d = document.createElement("div"); d.className = "cube" + (c.k === "w" ? " w" : ""); d.innerHTML = faces; world.append(d); return d; });
    const css = getComputedStyle(world);
    let rx = -32, ry = 45, trx = -32, tr = 45, prog = 0;
    const base = opts.ry || 45;
    if (!RM) addEventListener("pointermove", (e) => { trx = -32 + (e.clientY / innerHeight - 0.5) * -18; tr = base + (e.clientX / innerWidth - 0.5) * 40; });
    function frame() {
      const S = parseFloat(css.getPropertyValue("--S")), G = parseFloat(css.getPropertyValue("--G"));
      rx += (trx - rx) * 0.06; ry += (tr + prog * 30 - ry) * 0.06;
      world.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg)`;
      els.forEach((el, i) => {
        const c = C[i]; let x = (c.x - 0.5) * G, z = (c.z - 0.5) * G;
        const slide = c.k === "w" ? (0.18 + (RM ? 0 : 0.06 * Math.sin(Date.now() / 900))) * G * (1 - prog) : 0;
        x -= slide; z += slide; x *= 1 + prog * 1.4; z *= 1 + prog * 1.4;
        const y = -prog * [0.2, 0.8, 1.4, 2.2][i] * S * 0.5;
        el.style.transform = `translate3d(${x - S / 2}px,${y - S / 2}px,${z}px) rotateY(${c.k === "w" ? prog * 90 : 0}deg)`;
      });
      if (!RM) requestAnimationFrame(frame);
    }
    frame();
    return { set(p) { prog = p; if (RM) frame(); } };
  }
  const world = $("#world");
  if (world) {
    const M = Monolith(world);
    addEventListener("scroll", () => M.set(Math.min(1, scrollY / (innerHeight * 0.9))), { passive: true });
  }

  // Driftstavle clock (Copenhagen time)
  const clk = $("[data-clock]");
  if (clk) { const f = new Intl.DateTimeFormat("da-DK", { timeZone: "Europe/Copenhagen", hour: "2-digit", minute: "2-digit", second: "2-digit" }); const t = () => (clk.textContent = f.format(new Date())); t(); setInterval(t, 1000); }

  // Hero pull-focus (I/L)
  const hf = $(".hero-f");
  if (hf) requestAnimationFrame(() => setTimeout(() => hf.classList.add("focus"), 150));

  // Rack focus: photos start soft and pull into focus as they enter the viewport.
  const rf = $$(".rf img");
  if (rf.length && !RM) {
    const upd = () => rf.forEach((el) => {
      const r = el.getBoundingClientRect(), vh = innerHeight;
      const p = Math.min(1, Math.max(0, (vh - r.top) / (vh * 0.6)));
      el.style.filter = `blur(${(1 - p) * 12}px) saturate(${0.75 + p * 0.25})`;
      el.style.transform = `scale(${1.08 - p * 0.08})`;
    });
    addEventListener("scroll", upd, { passive: true }); addEventListener("resize", upd); upd();
  }

  // Parallax drift on zigzag photos (I/L)
  const px = $$(".px img");
  if (px.length && !RM) addEventListener("scroll", () => px.forEach((el) => {
    const r = el.closest(".ph").getBoundingClientRect();
    el.style.objectPosition = `50% ${50 + ((r.top + r.height / 2 - innerHeight / 2) / innerHeight) * 30}%`;
  }), { passive: true });

  // Magnetic buttons (pointer devices only)
  if (!RM && matchMedia("(pointer:fine)").matches) $$(".mag").forEach((b) => {
    b.addEventListener("pointermove", (e) => { const r = b.getBoundingClientRect(); b.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.18}px,${(e.clientY - r.top - r.height / 2) * 0.3}px)`; });
    b.addEventListener("pointerleave", () => (b.style.transform = ""));
  });

  // Agent console: lines come from data-lines (JSON) so each look/language has its own text.
  $$(".agent[data-lines]").forEach((el) => {
    const L = JSON.parse(el.dataset.lines);
    const esc = (s) => s.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
    const full = L.map(([c, s]) => `<span class="${c}">${esc(s)}</span>`).join("");
    if (RM) { el.innerHTML = full; return; }
    let started = false;
    new IntersectionObserver((es) => {
      if (!es[0].isIntersecting || started) return; started = true;
      let i = 0, j = 0, html = "";
      const step = () => {
        if (i >= L.length) { el.innerHTML = html + '<span class="caret"></span>'; setTimeout(() => { html = ""; i = 0; j = 0; step(); }, 7000); return; }
        const [c, s] = L[i]; j++;
        el.innerHTML = html + `<span class="${c}">${esc(s.slice(0, j))}</span><span class="caret"></span>`;
        if (j >= s.length) { html += `<span class="${c}">${esc(s)}</span>`; i++; j = 0; }
        setTimeout(step, s[j - 1] === "\n" ? 320 : 16);
      };
      step();
    }, { threshold: 0.35 }).observe(el);
  });

  // Missed-backup toasts
  $$("[data-toasts]").forEach((host) => {
    const ts = $$(".toast", host);
    if (RM) { ts.forEach((t) => t.classList.add("on")); return; }
    new IntersectionObserver((es, o) => {
      if (!es[0].isIntersecting) return; o.disconnect();
      ts.forEach((t, k) => setTimeout(() => t.classList.add("on"), 600 + k * 2000));
    }, { threshold: 0.4 }).observe(host);
  });

  // J: torch. Mouse = torch; touch = follows finger, otherwise sweeps slowly by itself. Reduced motion = fully lit (CSS).
  const H = $(".hero-t");
  if (H && !RM) {
    let auto = true, x = 30, y = 45, tx = 30, ty = 45, idle;
    const move = (cx, cy) => { auto = false; const r = H.getBoundingClientRect(); tx = ((cx - r.left) / r.width) * 100; ty = ((cy - r.top) / r.height) * 100; clearTimeout(idle); idle = setTimeout(() => (auto = true), 2500); };
    H.addEventListener("pointermove", (e) => move(e.clientX, e.clientY));
    H.addEventListener("touchmove", (e) => { const t = e.touches[0]; if (t) move(t.clientX, t.clientY); }, { passive: true });
    H.addEventListener("pointerleave", () => (auto = true));
    (function f(t) {
      if (auto) { tx = 38 + 26 * Math.sin(t / 2600); ty = 42 + 14 * Math.sin(t / 1700); }
      x += (tx - x) * 0.08; y += (ty - y) * 0.08;
      H.style.setProperty("--mx", x + "%"); H.style.setProperty("--my", y + "%");
      requestAnimationFrame(f);
    })(0);
  }

  // J: AI tabs auto-advance like stories; click to jump (then hold).
  const tabs = $$("#tabs button"), panes = $$("#stage .pane");
  if (tabs.length) {
    let cur = 0, t0 = performance.now(), hold = RM;
    const go = (i) => { cur = i; t0 = performance.now(); tabs.forEach((b, k) => { b.classList.toggle("on", k === i); b.setAttribute("aria-selected", k === i); b.querySelector("i").style.width = "0"; }); panes.forEach((p, k) => p.classList.toggle("on", k === i)); };
    tabs.forEach((b, i) => (b.onclick = () => { go(i); hold = true; }));
    $("#stage").addEventListener("pointerenter", () => (hold = true));
    (function f(t) { if (!hold) { const p = (t - t0) / 9000; tabs[cur].querySelector("i").style.width = Math.min(100, p * 100) + "%"; if (p >= 1) go((cur + 1) % tabs.length); } requestAnimationFrame(f); })(t0);
  }

  // J: expanding service cards
  const cards = $$("#deck .card");
  cards.forEach((c) => { const on = () => cards.forEach((k) => k.classList.toggle("on", k === c)); c.addEventListener("pointerenter", on); c.addEventListener("click", on); c.addEventListener("focus", on); });

  // K: chapter player — plays only while visible, pause button, tap a chapter to jump. No scroll hijack.
  const P = $("#player");
  if (P) {
    const S = $$(".sh", P), C = $$(".ptxt .c", P), T = $$("#thumbs button"), U = $$("#bars u");
    let cur = 0, el = 0, last = performance.now(), vis = false, paused = RM;
    const go = (i) => { cur = i; el = 0; S.forEach((s, k) => s.classList.toggle("on", k === i)); C.forEach((s, k) => s.classList.toggle("on", k === i)); T.forEach((s, k) => s.classList.toggle("on", k === i)); U.forEach((u, k) => (u.style.width = k < i ? "100%" : "0")); };
    T.forEach((b, i) => (b.onclick = () => go(i)));
    const pp = $("#pp");
    const label = () => (pp.textContent = paused ? pp.dataset.play : pp.dataset.pause);
    pp.onclick = () => { paused = !paused; label(); }; label();
    new IntersectionObserver((es) => (vis = es[0].isIntersecting), { threshold: 0.5 }).observe(P);
    (function f(t) { const dt = t - last; last = t; if (vis && !paused) { el += dt; U[cur].style.width = Math.min(100, (el / 6000) * 100) + "%"; if (el >= 6000) go((cur + 1) % S.length); } requestAnimationFrame(f); })(last);
  }

  // K: warm pulse travelling the agent pipeline; pauses at "human".
  const dot = $("#dot");
  if (dot && !RM) {
    const nodes = $$("#flow .node"), X = [100, 340, 580, 820, 1060], t0 = performance.now();
    (function f(t) {
      const k = Math.max(0, t - t0) / 1000, seg = Math.floor(k / 1.1) % 6, fr = (k % 1.1) / 1.1;
      const x = seg < 4 ? X[seg] + (X[seg + 1] - X[seg]) * Math.min(1, fr * 1.6) : X[4];
      dot.setAttribute("cx", x); nodes.forEach((n, i) => n.classList.toggle("lit", Math.abs(X[i] - x) < 40));
      requestAnimationFrame(f);
    })(t0);
  }
})();
