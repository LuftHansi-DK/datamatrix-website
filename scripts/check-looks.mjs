// Validates per-look copy (src/looks/<x>.json) against src/looks/skeleton.json and enforces
// Hans's rule (15 Oct 2026): every look has its OWN text — no two looks may share the same sentence.
// Deterministic, no network. Run: node scripts/check-looks.mjs
import { readFileSync, existsSync } from "node:fs";

const ONLY = (process.argv.find((a) => a.startsWith("--only=")) || "").slice(7);
const LOOKS = ONLY ? [ONLY] : ["i", "j", "k", "l", "m"];
const EXTRA = { i: [], l: [], m: ["hint"], j: ["hint", "tabs", "paneH"], k: ["flow", "flowIntro", "player", "playLabel", "foundation"] };
const skel = JSON.parse(readFileSync("src/looks/skeleton.json", "utf8"));
let errors = 0;
const err = (m) => { console.error("check-looks: " + m); errors++; };

function shape(ref, val, path) {
  if (typeof ref === "string") {
    if (typeof val !== "string" || !val.trim()) return err(`${path}: missing/empty text`);
    if (/<[^>]*>/.test(val)) err(`${path}: placeholder or markup left: ${val.slice(0, 60)}`);
    return;
  }
  if (Array.isArray(ref)) {
    if (!Array.isArray(val)) return err(`${path}: expected list`);
    if (val.length !== ref.length) err(`${path}: expected ${ref.length} items, got ${val.length}`);
    ref.forEach((r, i) => shape(r, val[i], `${path}[${i}]`));
    return;
  }
  if (typeof val !== "object" || val === null) return err(`${path}: expected object`);
  for (const k of Object.keys(ref)) if (!k.startsWith("_")) shape(ref[k], val[k], `${path}.${k}`);
  for (const k of Object.keys(val)) if (!k.startsWith("_") && !(k in ref)) err(`${path}.${k}: unknown key`);
}

function pickExtra(look) {
  const o = {};
  for (const k of EXTRA[look]) o[k] = skel.extra[k];
  return o;
}

const data = {};
for (const look of LOOKS) {
  const f = `src/looks/${look}.json`;
  if (!existsSync(f)) { err(`${f} missing`); continue; }
  const d = JSON.parse(readFileSync(f, "utf8"));
  data[look] = d;
  const ref = { footer: skel.footer, front: skel.front, pages: skel.pages, en: { footer: skel.en.footer, front: skel.en.front, about: skel.en.about } };
  if (EXTRA[look].length) { ref.extra = pickExtra(look); ref.en.extra = pickExtra(look); }
  shape(ref, d, look);
  if (d._look !== look) err(`${f}: _look must be "${look}"`);
}

// Cross-look uniqueness. Fixed labels/titles/numbers are exempt (short strings, listed keys).
const EXEMPT_KEY = /(^|\.)(lab|time|role|_look|_doc)$|timeline\[\d+\]\[0\]$/;
// Proper names/fixed terms are removed before comparing, so a shared product or degree name alone is not a "duplicate".
const FIXED = ["management information systems", "san diego state university", "vmware vsphere", "hyper-v", "microsoft 365", "sharepoint", "onedrive", "teams", "azure", "hermes agent", "openclaw", "grok-bot", "grok bot", "openai dots", "teamviewerqs", "delt san-lager", "shared san storage", "datamatrix aps", "datamatrix", "b.sc."];
const norm = (s) => FIXED.reduce((a, f) => a.split(f).join(" "), s.toLowerCase()).replace(/\{[a-z]+\}/g, "").replace(/[^a-zæøå0-9 ]+/gi, " ").replace(/\s+/g, " ").trim();
const strings = []; // [look, path, text]
function collect(look, v, path) {
  if (typeof v === "string") { if (!EXEMPT_KEY.test(path)) strings.push([look, path, v]); return; }
  if (Array.isArray(v)) return v.forEach((x, i) => collect(look, x, `${path}[${i}]`));
  if (v && typeof v === "object") for (const [k, x] of Object.entries(v)) if (!k.startsWith("_")) collect(look, x, path ? `${path}.${k}` : k);
}
for (const [look, d] of Object.entries(data)) collect(look, d, "");

const grams = (s) => { const w = norm(s).split(" "); const g = new Set(); for (let i = 0; i + 2 < w.length; i++) g.add(w.slice(i, i + 3).join(" ")); return g; };
const byNorm = new Map();
for (const [look, path, text] of strings) {
  const n = norm(text);
  if (n.length < 24) continue; // short labels may coincide
  if (byNorm.has(n) && byNorm.get(n)[0] !== look) err(`same text in ${byNorm.get(n)[0]}:${byNorm.get(n)[1]} and ${look}:${path}: "${text.slice(0, 70)}"`);
  else byNorm.set(n, [look, path]);
}
// near-duplicates: long sentences sharing most word trigrams across looks
const longs = strings.filter(([, , t]) => norm(t).split(" ").length >= 8).map(([l, p, t]) => [l, p, t, grams(t)]);
for (let a = 0; a < longs.length; a++) for (let b = a + 1; b < longs.length; b++) {
  if (longs[a][0] === longs[b][0]) continue;
  const A = longs[a][3], B = longs[b][3];
  let inter = 0; for (const g of A) if (B.has(g)) inter++;
  const j = inter / Math.min(A.size, B.size);
  if (j >= 0.6) err(`near-duplicate (${Math.round(j * 100)}%) ${longs[a][0]}:${longs[a][1]} ~ ${longs[b][0]}:${longs[b][1]}`);
}

if (errors) { console.error(`\ncheck-looks: ${errors} problem(s)`); process.exit(1); }
console.log(`check-looks: OK (${Object.keys(data).length} looks, ${strings.length} texts)`);
