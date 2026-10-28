// Cloudflare Pages Function: serves this week's look for the WHOLE site.
// No cookies, no storage, no consent banner — ever. The look depends only on the date
// (or on ?look= while previewing, or on a pin Hans sets for everybody).
//
// How: the plain static pages are look L (fallback). Looks I/M/K are pre-built under /v/<look>/...
// This function rewrites /ydelser/ -> /v/k/ydelser/ internally; the visitor's URL never changes.
// If anything here fails, the plain static page (L) is served.
import { chooseLook, isLook, FALLBACK } from "../lib/look.mjs";
import pinFile from "../lib/look-pin.json";

const VARIANT_PREFIX = /^\/v\/([a-z])(\/.*)$/;

async function readPin(env) {
  // Optional future: KV namespace bound as LOOK_KV with key "pin" (set from a protected admin button).
  try {
    if (env && env.LOOK_KV) {
      const kv = await env.LOOK_KV.get("pin", "json");
      if (kv) return kv;
    }
  } catch { /* ignore: fall back to the file */ }
  return pinFile;
}

function carryLook(look) {
  // Keep ?look= on internal page links so the whole site follows the preview. Pages only, not assets.
  return {
    element(el) {
      const href = el.getAttribute("href");
      if (!href || !href.startsWith("/") || href.startsWith("//")) return;
      const [pathAndQuery, hash = ""] = href.split("#");
      const [path, query = ""] = pathAndQuery.split("?");
      if (/\.[a-z0-9]+$/i.test(path)) return; // file, not a page
      const qs = new URLSearchParams(query);
      qs.set("look", look);
      el.setAttribute("href", `${path}?${qs.toString()}${hash ? "#" + hash : ""}`);
    },
  };
}

export async function onRequest(context) {
  const { request, env, next } = context;
  try {
    if (request.method !== "GET" && request.method !== "HEAD") return next();
    const url = new URL(request.url);
    const path = url.pathname;

    // Direct hits on the internal variant paths -> clean URL (with ?look= only for valid looks).
    // Retired looks (e.g. old /v/j/...) redirect to the same path without override.
    const m = path.match(VARIANT_PREFIX);
    if (m) {
      const dest = new URL(m[2], url);
      if (isLook(m[1])) dest.searchParams.set("look", m[1]);
      return Response.redirect(dest.toString(), 301);
    }

    // Only pages (Astro uses trailing slashes). Assets, files, redirects: untouched.
    if (!path.endsWith("/") || path.startsWith("/looks/")) return next();

    const override = url.searchParams.get("look");
    const pin = await readPin(env);
    const { look, source } = chooseLook({ override: isLook(override) ? override : null, pin });

    let res;
    if (look === FALLBACK) {
      res = await next();
    } else {
      const variant = new URL(`/v/${look}${path}`, url);
      res = await env.ASSETS.fetch(new Request(variant.toString(), { method: request.method, headers: request.headers }));
      if (res.status === 404 || res.status >= 500) res = await next(); // page not built for this look -> plain page
    }

    const out = new Response(res.body, res);
    out.headers.set("X-DM-Look", `${look}; ${source}`);
    out.headers.set("Cache-Control", "public, max-age=0, must-revalidate");
    if (source === "override") {
      out.headers.set("X-Robots-Tag", "noindex");
      const type = out.headers.get("content-type") || "";
      if (type.includes("text/html")) return new HTMLRewriter().on("a[href]", carryLook(look)).transform(out);
    }
    return out;
  } catch {
    return next();
  }
}
