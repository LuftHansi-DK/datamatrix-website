// Look copy + photos. Copy lives in src/looks/<look>.json (one per look, Danish + English),
// facts in src/data/site.json. Tokens {phone} {email} {founded} {years} are filled here.
import site from "../data/site.json";
import i from "./i.json";
import j from "./j.json";
import k from "./k.json";
import l from "./l.json";

export const LOOKS = ["i", "j", "k", "l"] as const;
export type Look = (typeof LOOKS)[number];
export const VARIANT_LOOKS: Look[] = ["i", "j", "k"]; // L = the plain static pages (fallback)
export const LOOK_NAMES: Record<Look, string> = { i: "I · Fokus", j: "J · Lommelygte", k: "K · Kapitler", l: "L · Dag" };

const years = String(new Date().getFullYear() - site.founded);
const fill = (s: string) =>
  s.replaceAll("{phone}", site.phone).replaceAll("{email}", site.email).replaceAll("{founded}", String(site.founded)).replaceAll("{years}", years);
function deep(v: any): any {
  if (typeof v === "string") return fill(v);
  if (Array.isArray(v)) return v.map(deep);
  if (v && typeof v === "object") return Object.fromEntries(Object.entries(v).map(([a, b]) => [a, deep(b)]));
  return v;
}
const RAW: Record<Look, any> = { i, j, k, l };
const CACHE: Partial<Record<Look, any>> = {};
export function copy(look: Look): any {
  return (CACHE[look] ??= deep(RAW[look]));
}

// Which photo each look uses for each slot (files in public/looks/photos/<look>/<name>-768|1536.webp + -1536.jpg).
const P: Record<Look, Record<string, string>> = {
  i: { hero: "hero", ai: "ai", sikkerhed: "sikkerhed", cloud: "cloud", drift: "drift", backup: "backup", cta: "cta" },
  j: { hero: "hero", ai: "ai", approve: "approve", runbook: "runbook", sikkerhed: "sikkerhed", cloud: "cloud", drift: "drift", backup: "backup", cta: "cta" },
  k: { hero: "hero", ai: "ai", sikkerhed: "sikkerhed", cloud: "cloud", drift: "drift", backup: "backup", cta: "cta" },
  l: { hero: "hero", ai: "ai", sikkerhed: "sikkerhed", cloud: "cloud", drift: "drift", backup: "backup", cta: "cta" },
};
export function photo(look: Look, slot: string) {
  const name = P[look][slot] ?? P[look].hero;
  const b = `/looks/photos/${look}/${name}`;
  return { webp: `${b}-768.webp 768w, ${b}-1536.webp 1536w`, jpg: `${b}-1536.jpg` };
}
// Inner-page header photo per page
export const PAGE_PHOTO: Record<string, string> = { ydelser: "drift", ai: "ai", om: "cta", kontakt: "cta", fjernsupport: "cloud", privatliv: "sikkerhed", indsigt: "backup", notfound: "hero" };

export { site };
