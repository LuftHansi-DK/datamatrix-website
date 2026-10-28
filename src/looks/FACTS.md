# Facts every look may use (and nothing else)

The site rotates four looks (I, M, K, L) weekly. Each look has its **own wording** (Danish and English),
but every look tells the **same true facts**. Copywriters (human or agent) may only use the facts below.
Anything new → ask Hans before it goes in a PR (list it in the PR under "Nye påstande").

Source of truth for contact data: `src/data/site.json` (use tokens, never hard-code):
`{phone}` (+45 2026 1188), `{email}`, `{founded}` (2004), `{years}` (years since 2004, computed).

## Company
- DataMatrix ApS, founded 2004 by Hans Kristiansen, Lindevej 5, 4520 Svinninge, CVR 28124147. Name is "DataMatrix" (no "IT").
- Senior IT partner for small and mid-sized businesses; customers range from small local firms to international production companies (no names!).
- More than 30 years of experience (Hans).
- One fixed senior contact; you talk directly to the owner. Hans is personally involved in and responsible for all customers.
- Deliberately small. A fixed network of experienced technicians **with their own companies** (unnamed) steps in for holiday, illness, busy periods; specialists (e.g. network/infrastructure) for bigger projects.
- Customer environments are documented so a colleague can take over without starting over.
- Alarms and backup checks run around the clock ("døgnet rundt").
- Reachability may be described ("også uden for kontortid, når det brænder på", "også kl. 22 en søndag" for AI prioritisation), NEVER guaranteed. No "24/7 guarantee".
- Works in Danish and English.
- Own rule of thumb (motto): "Den bedste løsning er den enkleste, der virker." / "The best solution is the simplest one that works." (may be paraphrased, attributed to DataMatrix, not to a famous person).

## Hans (bio — facts fixed, wording free)
- B.Sc. in Management Information Systems, San Diego State University, 1990.
- Then years in the USA: first developer of database systems, later IT director and board member.
- Back in Denmark: self-employed IT consultant for several years, then founded DataMatrix in 2004.
- Portrait: real photo `/img/hans.jpg` only.

## Services
- **Drift og overvågning**: monitoring of servers, clients, backup, certificates; updates/maintenance on a fixed plan; user support by phone, mail, remote support; documentation.
- **Missed backup**: most monitoring warns when a backup fails; ours also notices the backup that never started (no error message). Rare, but that is when it counts.
- **IT-sikkerhed**: firewall, network segmentation, secure remote access; mail and endpoint protection; access control, MFA, cleaning up permissions; security review with concrete priorities. Security has been the common thread since 2004.
- **Backup og beredskab**: backup of servers, Microsoft 365 and data, local and offsite; disaster recovery plans and restore tests (DR is one of our specialities); contingency plan (who does what); fast help at outages/incidents. Backup is only worth something if it can be restored — we test it.
- **Microsoft 365 og cloud**: setup, migration, operation of mail, Teams, SharePoint, OneDrive; Azure and hybrid; licence optimisation; advice on what to move to cloud and what not. No one-size-fits-all.
- **Servere, netværk og virtualisering**: design of IT/network infrastructure; servers and virtualisation (VMware vSphere and Hyper-V, incl. shared SAN storage — VMware is the bigger practice); switches, Wi-Fi, firewalls; planning replacements and moves.
- **Indkøb**: hardware (servers, PCs, network gear from recognised manufacturers — NO brand names) and Microsoft/other licences; clear quotes; installation.
- Engagement: fixed agreement or single tasks; full IT operation or sparring for the customer's own IT person.
- Getting started: informal talk (phone, mail or we visit) → review of IT/security/backup with an honest assessment → plan and price, most important first → operation and ongoing improvement.

## AI (only these claims)
- DataMatrix uses AI daily in its own operations. Several AI agents work side by side.
- AI agents read every incoming **request** (henvendelser — NOT alarms), sort it, link it to the right customer and task, judge what is urgent, create the task, and write a runbook (step-by-step plan: what the agent can do itself and what a human must do), for themselves and for us. Drafts of replies, documentation and quotes are prepared.
- **Nothing is sent, changed or bought without a human saying yes.** (core rule; must appear in every look)
- Four rules: the human decides (AI proposes, a person approves); data stays where it belongs (we know what AI can access and what not); everything can be verified (actions are logged); start small (one concrete task that works before the next).
- What we offer customers: Copilot readiness (Copilot sees what the user sees → clean up permissions/sharing in M365); automating routine tasks AI prepares and people approve; simple rules for which AI tools may be used for what, with which data.
- For experienced people: we build and run our own AI agents in daily operations, several agent harnesses side by side: **Hermes Agent, OpenClaw, our own Grok bot, OpenAI Dots** (names OK, no superlatives) — with tools, memory, skills and fixed security rules. Topics to spar on: agents and orchestration (when one is better than five); tools/integrations with least privilege (mail, calendar, Microsoft 365, own systems); memory and skills (what to remember, what not, transparent); security in practice (drafts only, approval before action, logging, strict separation between customers); model choice and cost.
- AI FAQ facts: small companies often gain most because every hour counts; data safety depends on setup, so we start by checking what data AI can reach; first step is often an M365 review and a couple of concrete tasks.

## Never write
- Uptime %, team size, round-the-clock guarantees, customer names/logos/quotes/cases, named partner technicians, prices, brand names of hardware.
- "AI triages alarms" (not live yet). quotes attributed to famous people. Superlatives about our AI ("most advanced", "unique").
- Fake people/premises ("our team", "our office/workshop"). Photos are illustrative.
- Cookie talk other than: no cookies, no tracking, no analytics, fonts/images from our own server; hosted at Cloudflare, which may log technical data like IP address for security; email/phone data used only to answer and for a customer relationship.
