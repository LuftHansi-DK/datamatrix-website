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
- A fixed network of experienced consultants **with their own companies** steps in for holidays, illness, busy periods and specialist projects. Niels Bertelsen and Niels Nordal may be named under the look L approval below.
- Customer environments are documented so a colleague can take over without starting over.
- Alarms and backup checks run around the clock ("døgnet rundt").
- Reachability may be described ("også uden for kontortid, når det brænder på", "også kl. 22 en søndag" for AI prioritisation), NEVER guaranteed. No "24/7 guarantee".
- Works in Danish and English.
- Own rule of thumb (motto): "Den bedste løsning er den enkleste, der virker." / "The best solution is the simplest one that works." (may be paraphrased, attributed to DataMatrix, not to a famous person).

## Hans (bio — facts fixed, wording free)
- B.Sc. in Management Information Systems, San Diego State University, 1990.
- Then years in the USA: first developer of database systems, later IT director and member of the management.
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
- Uptime %, team size, round-the-clock guarantees, customer names/logos/quotes/cases, named partner technicians except Niels Bertelsen and Niels Nordal (Hans OK 17 Nov 2026, t146u), prices except the explicitly approved look L packages below, brand names of hardware.
- "AI triages alarms" (not live yet). quotes attributed to famous people. Superlatives about our AI ("most advanced", "unique").
- Fake people/premises. The two approved real consultants may be presented as the team behind the work; their portraits and Hans’s portrait are real. Other photos are illustrative.
- Cookie talk other than: no cookies, no tracking, no analytics, fonts/images from our own server; hosted at Cloudflare, which may log technical data like IP address for security; email/phone data used only to answer and for a customer relationship.

## Pakker og priser (look L, Hans 13 Nov 2026)
- Hans approved these packages and from-prices (starting prices) for look L only on 13 Nov 2026. The exact price is agreed before work starts. All amounts exclude VAT (ekskl. moms); the other looks retain their existing service descriptions.
- AI-tjek: fra 8.500 kr. (from DKK 8,500), starting one-off price. Maps apps and AI tools with Microsoft 365 access, who granted permission and mail-sending rights; delivers a short report with the ten most important fixes. The customer's administrator grants read access with guidance; no duration or content-access limitation is promised.
- AI-sikring: fra 24.500 kr. (from DKK 24,500), starting one-off price. Implements fixes under a customer-approved plan; approval for new apps, appropriate mail-sending rights and protection of sensitive data; includes an AI policy in Danish and a short staff guide. The customer approves before changes.
- AI-tilsyn: fra 2.500 kr. pr. måned (from DKK 2,500 per month). Monthly checks for new apps, permissions and forwarding, notification of changes, assessment of proposed AI tools before use and a brief quarterly status report. Customers submit the tools they want to use.
- AI-start (recommended): fra 4.500 kr. pr. måned i 12 måneder (from DKK 4,500 per month for 12 months). Includes AI-tjek + AI-sikring + 12 months of AI-tilsyn in one agreement with one regular contact.
- AI agents prepare package work; an experienced consultant reviews and takes responsibility for the result. No proportion of automated work or delivery time is promised.

## Look L strategy update (DM-02396, 17 Nov 2026 — pending Hans's approval in the PR)

These additions apply to look L only; the other looks keep their existing copy. Copy drafted by Grok Bot from Hans's answers of 17 Nov 2026 (t146u) and the Opus 5.5 strategy review. Hans OK'd naming Niels Bertelsen and Niels Nordal and using their photos from the old site (t146u); role lines come from the old WordPress site (2016) with the years brought forward conservatively. Final approval of every line below = Hans ticking the CLAIMS-PENDING list in the PR and merging.

- Experience band: experience from demanding international projects is applied with the same care whether a business has 5 or 500 employees; this is an example business size range, not a team-size claim.
- Shell Prelude is Hans's project experience, not a claim that Shell was a DataMatrix customer. As an external consultant for an anonymous international machinery-monitoring supplier, he managed large parts of its internal Danish infrastructure for several years and was sent to Singapore and South Korea to work on vibration monitoring for Prelude's gas turbines. Prelude is described as the world's largest floating offshore facility (Shell/Technip wording: "the largest floating offshore facility in the world"), with an estimated project value of around DKK 100 billion (Shell USD 12.6 bn in 2017; Wood Mackenzie ~USD 17 bn in 2019; ≈ DKK 85–115 bn at 6.79 DKK/USD). Built by the Technip Samsung Consortium at Samsung Heavy Industries, Geoje, South Korea. Do not name the monitoring supplier unless Hans approves (it is still active in Denmark).
- Since 2007, DataMatrix and Niels Bertelsen have built and operated large parts of the infrastructure at an anonymous international manufacturing company, today alongside its own IT department. The company must remain anonymous.
- Working across businesses, industries and sizes brings an outside perspective that is hard to build within one IT department. DataMatrix supports in-house IT with projects, reviews and advice, or handles all operations.
- Niels Bertelsen: real portrait `/img/niels-bertelsen.webp` with JPG fallback; consultant with his own company, more than 30 years of IT experience, networks as his main speciality, and shared infrastructure work with Hans at the anonymous manufacturing company.
- Niels Nordal: real portrait `/img/niels-nordal.webp` with JPG fallback; consultant with his own company, more than 25 years across a broad range of IT systems; holiday, illness and busy-period cover. Both named consultants can take over when Hans is away. Documented environments support handover; specialist work uses the same fixed network.
- Digital employee: an AI agent with one defined task, built, tested and maintained in the customer's own Microsoft 365 with Microsoft Copilot and existing permissions. Permissions are reviewed before launch, with monthly oversight afterwards. Data stays in the customer's environment and in the EU; the customer owns the agent.
- Illustrative tasks: shared inbox sorting/routing and draft replies; quote and order-confirmation drafts from emails and price lists; matching invoices to orders and flagging exceptions for accounts approval; answers from internal documents with source links; Teams meeting minutes and task lists for organiser approval; IT guidance, detailed support tickets and human handover. Any stated task times are illustrative and depend on the customer's workday.
- Digital employees can read, sort and prepare around the clock, including at night. This is capability wording, not a service availability guarantee. Sending, paying, changing or buying waits for human approval, including until the customer's approver is at work. Inbox routing in the example does not authorise autonomous external replies.
- DataMatrix's own agents read all enquiries daily, identify customer/task, assess urgency, and prepare plans and drafts; the same workflow is built for customers. A human approves actions.
- A fixed weekly day at the customer's premises is available by agreement. Remote support remains available; no response-time promise is added.
- AI-tjek is renamed AI- og Copilot-tjek. Its deliverable adds three tasks a digital employee could take on, alongside the report with the ten most important fixes. Existing read-access scope and starting one-off price of DKK 8,500 remain unchanged.
- Digital medarbejder: one defined task, customer chooses the task and approver; “Pris efter aftale” / price by agreement, setup plus monthly payment. No numeric price is asserted.
- AI-sikring stays from DKK 24,500 one-off; AI-tilsyn stays from DKK 2,500 per month. Prices exclude VAT and are agreed before work starts.
- AI-start moves from the front page to a look L-only bundle box on /ai/: AI- og Copilot-tjek, AI-sikring and one year of AI-tilsyn, one agreement and one regular contact, from DKK 4,500 per month for 12 months excluding VAT.
- Timeline/today line: IT partner for companies "fra lokale firmaer til internationale koncerner" (look L /om/).
- Certification: Hans holds Microsoft Certified: Azure Administrator Associate (AZ-104), renewed 17 Nov 2026 (Hans OK 17 Nov 2026, t148u). Plain text only; no logo, no expiry date. No other certifications are claimed.
