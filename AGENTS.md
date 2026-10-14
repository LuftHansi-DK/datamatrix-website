# Rules for any agent working on this site (Hermes, Grok bot, Codex, …)

This is the public website of DataMatrix ApS (www.datamatrix.dk). Owner and only approver: Hans Kristiansen.

## The one rule
**Never publish on your own.** Work on a branch, open a pull request, and stop.
Hans merges = publish. Cloudflare Pages deploys `main` to production and every PR branch to a preview URL.
Do not push to `main`, do not merge, do not change repo settings, Cloudflare or DNS.

## Workflow
1. `git switch -c <short-topic>` from an up-to-date `main`.
2. Make the smallest change that does the job. Keep the existing design.
3. `npm ci && npm run check` must pass (content guard + build).
4. Open a PR: what changed, why, and the preview URL once Cloudflare posts it.

## Where things live
- Contact facts (phone, mail, address, CVR, remote-support link): `src/data/site.json` — the only place to change them.
- Pages: `src/pages/*.astro` (Danish), `src/pages/en/index.astro` (English).
- News/articles ("Indsigt"): one Markdown file per post in `src/content/indsigt/`
  with frontmatter `title`, `description` (≤200 chars), `date` (YYYY-MM-DD), `draft`. Use `draft: true` until Hans approves.
- Design: `src/styles/global.css`. Logo mark: `src/components/Mark.astro`, `public/img/mark.svg`.

## Content rules
- Danish first; plain, warm, professional. No buzzwords, no hype. English page mirrors the Danish facts.
- Only true, checkable claims. No uptime figures, no team-size numbers, no "guaranteed 24/7".
  Reachability may be described ("også uden for kontortid, når det brænder på"), never guaranteed.
- **No customer names, logos, quotes or cases** without Hans's written OK *for that customer* recorded in the PR.
- No named partner technicians without their OK.
- No prices unless Hans provides them.
- No cookies, trackers, analytics scripts, external fonts or third-party embeds (privacy page promises this).
- Never put credentials, tokens, customer data or internal details in this repo — it may be public.

`scripts/check-content.mjs` enforces part of this. Passing it is necessary, not sufficient.
