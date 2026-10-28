// Weekly look rotation. Pure functions, no I/O, so they can be unit-tested with node.
// Used by functions/_middleware.js (Cloudflare Pages Function).
//
// Rules (Hans, 15 Oct 2026; M replaced J 28 Oct 2026):
// - Order I -> M -> K -> L, one look per week, 4-week cycle.
// - The week changes Monday 00:00 Europe/Copenhagen (DST handled by Intl).
// - NO cookies, no storage. The look is computed from the date only.
// - Fallback (function down / anything unknown) = L, which is also what the plain static pages are.
// - ?look=i|m|k|l overrides for preview; the middleware carries it on internal links.
// - A "pin" (look-pin.json) sets the look for EVERYBODY until a given Monday.

export const LOOKS = ["i", "m", "k", "l"];
export const FALLBACK = "l";
// Monday that starts an "I" week. Every 4 weeks after it is I again.
export const ANCHOR_MONDAY = "2026-10-19";

const DAY = 86400000;

// Local calendar date (YYYY-MM-DD) in Copenhagen for an instant.
export function copenhagenDate(now) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Europe/Copenhagen", year: "numeric", month: "2-digit", day: "2-digit",
  }).formatToParts(now);
  const get = (t) => parts.find((p) => p.type === t).value;
  return `${get("year")}-${get("month")}-${get("day")}`;
}

// Whole days between two YYYY-MM-DD dates (calendar arithmetic in UTC, no DST issues).
function dayIndex(ymd) {
  const [y, m, d] = ymd.split("-").map(Number);
  return Math.floor(Date.UTC(y, m - 1, d) / DAY);
}

// Monday (YYYY-MM-DD) of the Copenhagen week containing `now`.
export function weekMonday(now) {
  const idx = dayIndex(copenhagenDate(now));
  const dow = (new Date(idx * DAY).getUTCDay() + 6) % 7; // 0 = Monday
  return new Date((idx - dow) * DAY).toISOString().slice(0, 10);
}

export function rotationLook(now, anchor = ANCHOR_MONDAY) {
  const weeks = Math.floor((dayIndex(copenhagenDate(now)) - dayIndex(anchor)) / 7);
  return LOOKS[((weeks % 4) + 4) % 4];
}

export function isLook(x) {
  return typeof x === "string" && LOOKS.includes(x);
}

// pin = { look: "k", until: "2026-10-26" } -> look k for everybody until Monday 2026-10-26 00:00 Copenhagen.
export function activePin(pin, now) {
  if (!pin || !isLook(pin.look) || !/^\d{4}-\d{2}-\d{2}$/.test(pin.until || "")) return null;
  return copenhagenDate(now) < pin.until ? pin.look : null;
}

// Final decision. Returns { look, source } where source is override | pin | rotation | fallback.
export function chooseLook({ now = new Date(), override = null, pin = null, anchor = ANCHOR_MONDAY } = {}) {
  try {
    if (isLook(override)) return { look: override, source: "override" };
    const p = activePin(pin, now);
    if (p) return { look: p, source: "pin" };
    return { look: rotationLook(now, anchor), source: "rotation" };
  } catch {
    return { look: FALLBACK, source: "fallback" };
  }
}
