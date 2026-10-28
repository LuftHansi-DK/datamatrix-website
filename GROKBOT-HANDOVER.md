# Handover: datamatrix.dk → Grok Bot (28 Oct 2026)

From Hermes (hk-assistant, claude-opus-5-5), who designed and built the site 14–15 Oct 2026.
From now on Grok Bot manages the site for Hans. Hermes no longer works on it unless Hans asks.
**This repo is public.** Never put credentials, customer data or internal notes in it.

## Read in this order
1. `AGENTS.md`: the binding rules. Short version: branch → `npm run check` → PR → **stop**. Hans merges = publish.
2. This file: state, how things work, and what's open.
3. `.hermes.md`: technical detail for the rotating looks (rotation, `/v/` rewrites, photos, copy files).
4. `REVIEW.md`: Hans's answers about what the site may claim. `SEO.md`: visibility plan.
5. `src/looks/FACTS.md`: the only claims allowed in page text.

## What is live (verified 28 Oct 2026)
- https://www.datamatrix.dk is served by Cloudflare Pages project `datamatrix-website` from `main`.
  Every branch/PR gets a preview at `https://<branch>.datamatrix-website.pages.dev` (noindex).
- Apex `https://datamatrix.dk/…` gives a 301 to `www`. The redirect comes from the old Curanet webhotel (LiteSpeed), not from Cloudflare.
  DNS lives at Curanet (ns1/ns2.123hotel.dk): `www` is a CNAME → `datamatrix-website.pages.dev`.
  **MX/mail (Centera → M365) must never be touched.**
- Old WordPress URLs (`/about`, `/service`, `/news`) give a 301 to the new pages (PR #4).
- Rotating looks are live. This week (from Mon 26 Oct) the header is `X-DM-Look: j; rotation`.
- PRs #1–#6 are all merged. No open PRs. `npm run check` passes on `main` (`edd8bad`).
- Stack: Astro static site, Node 22, `npm run build` → `dist/`, plus one Pages Function, `functions/_middleware.js`.

## The four rotating looks (Hans's design decisions, 15 Oct)
- **I Fokus**: warm and quiet, zigzag photo rows, parallax.
- **J Lommelygte**: dark server room; the cursor is a torch. On touch screens the torch sweeps and follows your finger. With reduced motion, photos are fully lit.
- **K Kapitler**: a chapter player the visitor controls, plus an animated agent-flow diagram.
- **L Dag**: daylight version of I. This is also the **fallback** if the function fails.
- They rotate I → J → K → L weekly. Each switch happens **Monday 00:00 Europe/Copenhagen** for everybody (anchor Mon 2026-10-19 = I).
  The whole site follows the look, Danish and English.
- **No cookies, no storage, no consent banner. Ever.** The look depends only on the date.
- Preview any look: add `?look=i|j|k|l` to any URL. The `/looks/` page (unlinked, noindex) shows the live look and the next 8 weeks.
- **Show one look to everybody:** set `lib/look-pin.json` (`look`, `until` = a Monday) via PR. It ends automatically. To return to rotation, set both to `null`.
- Each look has its own photo set and its **own wording**, Danish and English. Hans wants no two looks to share a sentence.
  `npm run check` (`scripts/check-looks.mjs`) fails on shared or near-duplicate sentences.
  Titles and meta descriptions are shared on purpose (stable SEO). So are the Indsigt article bodies.
- Brand: logo B2 (iso 2×2 blocks, the white one slides out), name **"DataMatrix"** (no "IT"), blue `#3569B4` family.

## Common tasks
- **Change a text:** edit the same field in all four of `src/looks/{i,j,k,l}.json`, saying it differently in each.
  Fix the English (`en`) too. Run `npm run check`, open a PR, and give Hans the preview link.
- **Change contact facts** (phone, mail, address, CVR, support link): only in `src/data/site.json`.
- **New claim** (anything not in `FACTS.md`): ask Hans first, then add it to `FACTS.md` in the same PR.
- **New Indsigt post:** `src/content/indsigt/<slug>.md` with `title`, `description` (≤200 chars), `date`, and `draft: true`
  until Hans approves. SEO.md suggests 1–2 a month on real customer questions (backup that never ran, Copilot oversharing,
  MFA, NIS2 for SMV, AI rules). Plain Danish, no hype.
- **Photos:** AI-generated photos are the production photos (Hans's decision). The Hans portrait `/img/hans.jpg` must stay real,
  and appears once per page. No implied fake team or premises. No small-NAS photos, only big serious racks. Plants here and there are fine.
  The optimised files are in `public/looks/photos/<look>/`. The originals were local on the Hermes VM (`design/photo-src/`, not in git).
  New photos: generate them, then run `python3 scripts/optimize-photos.py` (expects originals in `design/photo-src/<look>/`).
  Before showing Hans, check hands, connectors, cables and labels.
- **Design/CSS:** `public/looks/looks.css` and `looks.js`. They are unminified on purpose: Vite's minifier breaks `animation-timeline`, so keep them out of `src/`.
  Templates: `src/looks/*.astro`. Don't hard-code text in templates.

## Hard rules (from Hans; full list in AGENTS.md)
- Never push to `main`, merge, or change repo settings, Cloudflare or DNS. Hans does that, or says yes that turn.
- No customer names, logos, quotes or cases without Hans's written OK for that customer, recorded in the PR.
- No prices, uptime figures, team sizes or "guaranteed 24/7". Describe reachability, never guarantee it.
- AI: the approver is "a human" (not "Hans"). No "konkurrencedygtige priser". No "AI-genererede" footer line.
  Harnesses may be named on /ai/ (Hermes Agent, OpenClaw, own Grok bot, OpenAI Dots), without superlatives.
- No trackers, analytics, external fonts or third-party embeds.

## Open items (oldest first)
1. **REVIEW 13/14:** is Ops Center monitoring live for agreement customers? Is alarm triage by AI live?
   The site currently says AI triages "henvendelser" only. Add "og alarmer" only once Hans confirms it is live.
2. **WordPress shutdown** (Hans wants it): apex already redirects to www. Remaining: final WP backup, keep the webhotel 1–2 weeks
   as rollback, then cancel (next Curanet invoice 01-10-2027). The apex redirect currently depends on that webhotel,
   so a new apex solution is needed first. Options: Curanet DNS ALIAS/redirect, or move DNS to Cloudflare. Check what Curanet offers.
   Hans decides, and DNS changes need his yes.
3. **SEO actions only Hans can do** (SEO.md): Google Business Profile, Search Console + Bing (DNS TXT, with his yes), LinkedIn, reviews.
4. **Optional, later (Hans's call):** a one-click "set look" admin button (Cloudflare KV + Access, with a cookie only on Hans's own login) instead of the pin-file PR.
5. **Optional:** a newer real portrait of Hans, when he has one.

## Access
- Repo: `LuftHansi-DK/datamatrix-website` (public). Ruleset `protect-main`: changes go through PRs only.
- Grok Bot's GitHub account needs collaborator **write** access to push branches and open PRs. Hans grants it.
- Cloudflare and Curanet: Hans only.
- The Hermes VM has its own repo-scoped token for this repo. Hans can revoke it once Grok Bot is set up.

## Verify after a change is merged
```
curl -sI https://www.datamatrix.dk/ | grep -i x-dm-look      # e.g. "j; rotation" (or "pin" when pinned)
curl -sI "https://www.datamatrix.dk/?look=k" | grep -i x-dm-look   # "k; override"
curl -sI https://www.datamatrix.dk/ | grep -i set-cookie      # must print nothing
```
