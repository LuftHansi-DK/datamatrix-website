// node --test scripts/test-look.mjs   (also run by `npm run check`)
import test from "node:test";
import assert from "node:assert/strict";
import { chooseLook, rotationLook, weekMonday, copenhagenDate, activePin } from "../lib/look.mjs";

const at = (iso) => new Date(iso);

test("anchor week is I, then J, K, L, I", () => {
  assert.equal(rotationLook(at("2026-10-19T10:00:00+02:00")), "i");
  assert.equal(rotationLook(at("2026-10-26T10:00:00+01:00")), "j");
  assert.equal(rotationLook(at("2026-11-02T10:00:00+01:00")), "k");
  assert.equal(rotationLook(at("2026-11-09T10:00:00+01:00")), "l");
  assert.equal(rotationLook(at("2026-11-16T10:00:00+01:00")), "i");
});

test("week before anchor (launch week) is L = fallback look", () => {
  assert.equal(rotationLook(at("2026-10-15T12:00:00+02:00")), "l");
});

test("switch is Monday 00:00 Copenhagen, not UTC", () => {
  // Sunday 23:59 CEST = Sunday 21:59 UTC -> still L week
  assert.equal(rotationLook(at("2026-10-18T23:59:00+02:00")), "l");
  // Monday 00:00 CEST = Sunday 22:00 UTC -> I week already
  assert.equal(rotationLook(at("2026-10-18T22:00:00Z")), "i");
});

test("DST end night (25 Oct 2026) does not shift the switch", () => {
  assert.equal(rotationLook(at("2026-10-25T22:59:00Z")), "i"); // Sun 23:59 CET
  assert.equal(rotationLook(at("2026-10-25T23:00:00Z")), "j"); // Mon 00:00 CET
});

test("cycle is stable across New Year (ISO week 53 years)", () => {
  const seen = [];
  let t = at("2026-12-21T12:00:00+01:00").getTime();
  for (let i = 0; i < 8; i++, t += 7 * 864e5) seen.push(rotationLook(new Date(t)));
  for (let i = 1; i < seen.length; i++) assert.notEqual(seen[i], seen[i - 1]);
  assert.equal(seen.join(""), seen.slice(0, 4).join("").repeat(2));
});

test("weekMonday and copenhagenDate", () => {
  assert.equal(copenhagenDate(at("2026-10-18T22:30:00Z")), "2026-10-19");
  assert.equal(weekMonday(at("2026-10-22T12:00:00+02:00")), "2026-10-19");
  assert.equal(weekMonday(at("2026-10-19T00:00:00+02:00")), "2026-10-19");
});

test("override beats pin beats rotation; bad input ignored", () => {
  const now = at("2026-10-20T12:00:00+02:00"); // I week
  assert.deepEqual(chooseLook({ now }), { look: "i", source: "rotation" });
  assert.deepEqual(chooseLook({ now, pin: { look: "k", until: "2026-10-26" } }), { look: "k", source: "pin" });
  assert.deepEqual(chooseLook({ now, override: "j", pin: { look: "k", until: "2026-10-26" } }), { look: "j", source: "override" });
  assert.deepEqual(chooseLook({ now, override: "x" }), { look: "i", source: "rotation" });
  assert.deepEqual(chooseLook({ now, pin: { look: "z", until: "2026-10-26" } }), { look: "i", source: "rotation" });
});

test("preview look M: override works, never in rotation", () => {
  const now = at("2026-10-20T12:00:00+02:00");
  assert.deepEqual(chooseLook({ now, override: "m" }), { look: "m", source: "override" });
  let t = at("2026-10-19T12:00:00+02:00").getTime();
  for (let w = 0; w < 60; w++, t += 7 * 864e5) assert.notEqual(rotationLook(new Date(t)), "m");
});

test("pin expires Monday 00:00 Copenhagen", () => {
  const pin = { look: "k", until: "2026-10-26" };
  assert.equal(activePin(pin, at("2026-10-25T22:59:00Z")), "k");
  assert.equal(activePin(pin, at("2026-10-25T23:00:00Z")), null);
  assert.equal(activePin({ look: null, until: null }, at("2026-10-20T12:00:00Z")), null);
});
