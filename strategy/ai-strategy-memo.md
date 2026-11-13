# DataMatrix and AI agents: strategy memo

To: Hans Kristiansen · Status: draft for discussion · Not website content

> This repo is public. Customers and people are anonymised on purpose: "the anchor customer" is the AI-mature
> production company where agents already resolve Opgaver; "small customers" are the rest of the book.
> All prices are my suggestions to test, not market data.

## 1. The honest picture

You are right, and the timeline is shorter than is comfortable. Agents are commoditising **execution**: the
hours spent resetting, configuring, migrating, documenting and answering tickets. That is most of what an IT
consultancy has historically billed for. An AI-mature customer with its own IT lead and its own agent will stop
buying that from you, probably gradually over the next one to two years, and sooner if the budget gets tight.
Resisting it would only make it happen faster, as you say.

What agents do **not** commoditise, at least not yet:

- **Accountability.** Someone has to own the decision when an agent wants to delete, send, buy or open access.
  Boards, auditors, insurers and NIS2/GDPR obligations all need a named human.
- **Judgement across systems.** Knowing which change in Entra breaks the backup job, the VPN and the ERP
  integration at the same time is 30 years of scar tissue, not a prompt.
- **Recovery.** When something goes badly wrong, whether by ransomware, a bad migration or an agent acting on
  the wrong tenant, customers need someone who has restored things before. Backup and DR are your roots.
- **Trust in a small market.** Danish SMB owners buy from a person they know.

Your real edge is not "AI". In 12 months every IT provider's website will say "ansvarlig AI". Your edge is that
you **run a supervised agent workforce in production, with written guardrails, today**, on a security, backup
and infrastructure foundation. Sell that evidence, not the slogan.

**Recommendation in one line:** move DataMatrix from *the person who does the IT work* to *the person who is
accountable for how AI and IT are allowed to act*. That means governing, designing and supervising agents and
people, sold as subscriptions and fixed-scope work, not hours.

## 2. AI-mature customers (the anchor customer and those like it)

Your role shifts from operator to **architect, governor and second key**:

- **Architect:** design the customer's agent setup, covering which agents, which tools, least-privilege scopes,
  tenant separation, memory and KB rules, and model and cost choices.
- **Governor:** own the guardrails, including approval classes (what an agent may do alone, what needs a human,
  what needs two), consent and permission reviews, logging and audit, and the AI policy.
- **Second key and incident lead:** approve high-risk changes, run DR and restore tests, and be the escalation
  point when an agent or a person breaks something.
- **Coach:** make the incoming IT head successful. If he succeeds *with* you, you stay. If he has to succeed
  *despite* you, you are gone. Offer to be his senior bench, not his competitor.

**Commercial model:** propose a fixed monthly **governance retainer** with a written scope (architecture,
monthly review, quarterly permission and consent audit, change approval, DR tests, a fixed pool of escalation
time). Anchor it near today's average monthly spend for the first year, then let it fall slowly as their own
team matures. A predictable decline you agree on is better than an unpredictable one you don't. Bill projects
(migrations, new agent setups) at a **fixed price per outcome**. Never bill hours for work your agents did in
minutes: it either undercharges you or looks dishonest, and an AI-aware customer will notice.

Have this conversation **proactively, before** they raise it. Bring a written proposal that includes a
deliberate handover plan. Making yourself replaceable on paper is what makes a mature customer keep you.

## 3. Small companies without AI or IT depth

This is the growth market for the next two to four years. Their staff are already connecting AI tools to mail,
files and calendars with one click, AI note-takers are joining Teams meetings, and apps are sending mail as the
company. Nobody has decided any of it. Microsoft will keep shipping better governance defaults, which will
shrink the checklist part over time, but SMBs will still need someone to switch them on, interpret them and
take responsibility.

The offer is **responsible AI adoption**, starting from what they already have:

- **Shadow-AI and connector audit:** Entra enterprise apps and OAuth grants (who consented to what, with which
  scopes, e.g. `Mail.Send`, `Files.ReadWrite.All`, `offline_access`), user-consent settings, browser
  extensions, AI note-takers, Power Automate and Copilot Studio flows and their connectors.
- **Lockdown:** turn off user consent and turn on the admin-consent workflow; restrict which apps can send
  mail and as whom (Exchange RBAC for applications), turn off legacy SMTP AUTH and external auto-forwarding;
  baseline DLP and sensitivity labels; Power Platform DLP for connectors.
- **Copilot and agent governance:** oversharing clean-up in SharePoint and OneDrive before Copilot,
  who may build agents, and where they are allowed to act.
- **AI acceptable-use policy** in plain Danish (one to two pages) plus a short staff session. This also
  covers the AI Act's AI-literacy duty for deployers (Art. 4), which has applied since February 2025.
- **Managed agent setups:** a few well-scoped agents built and operated under your rules
  (drafts only, approval before action, logging, customer data separation).

## 4. Service packages (suggested price shapes, DKK excl. VAT, to be tested)

| Package | What | Suggested shape |
|---|---|---|
| **AI-tjek** | Audit of apps, consents, connectors, mail-sending and sharing; short red/amber/green report with the ten most important fixes | Fixed price, roughly 8–15k depending on size |
| **AI-grundsikring** | Implementing the lockdown and policy above, plus Copilot readiness and a staff session | Fixed project, roughly 20–45k |
| **AI-tilsyn** | Monthly drift report (new apps, consents, agents, connectors), an approval desk for new AI tools, quarterly review | Subscription, roughly 1.5–4k/month, or per user |
| **Styret agent** | One agent workflow designed, built and operated under your guardrails | Setup roughly 15–40k, plus 1.5–5k/month; model costs passed through openly |
| **AI-governance retainer** | Architect, governor and second key for AI-mature customers (section 2) | Monthly fee calibrated to current spend [Hans] |

Bundle AI-tilsyn into existing operations agreements where possible: it should become the reason the agreement
renews, not an extra.

## 5. Risks

- **Commoditisation.** Checklists become product features. Mitigate by selling accountability and evidence,
  and by having your own agents do the audit legwork so your price can fall while your margin holds.
- **Liability.** An agent you set up sends the wrong mail or deletes the wrong data. Mitigate with drafts-only
  defaults, written approval classes, logs, contract liability caps, updated data-processing agreements that
  list model providers as sub-processors, and **ask your insurer explicitly whether agent work is covered**.
- **Vendor lock-in.** Your harnesses, model providers and Microsoft can each change price or terms overnight.
  Keep KB, runbooks and policies in portable formats you own, keep at least two harnesses viable (you already
  do), and do not build customers onto a platform you cannot export from.
- **You as the single point of failure.** Agents multiply your capacity but concentrate knowledge in you and
  your agents. Customers buying "accountability" will ask who takes over. Give your technician network
  read access to the KB, document break-glass procedures per customer, and consider one senior partner who can
  co-sign.
- **Your own blast radius.** An agent workforce with access to many tenants is a high-value target. Strict
  per-customer separation and least privilege are both a necessity and a selling point.
- **Timeline.** The small-customer window is real, but not permanent. Plan for the governance work itself to
  become cheaper in three to five years. The durable business is trust plus recovery plus judgement.

## 6. Phased plan (6–12 months)

**Months 0–1: decide and talk.** Answer the interview questions. Have the future-role conversation with the
anchor customer and bring a written retainer proposal. Check insurance and update the DPA template. Write
one-page package descriptions.

**Months 1–3: productise.** Build the AI-tjek as an agent-assisted procedure (Graph queries, a report template,
your approval) so it takes hours, not days. Run it with two or three existing small customers as discounted
pilots. Update the website via PR (see `homepage-proposal.md`) and publish two Indsigt articles: one on
app consents and connectors, one on apps that send mail in your name.

**Months 3–6: convert.** Turn pilots into AI-tilsyn subscriptions and put the anchor customer on the retainer.
Deliver the first managed agent at a customer other than the anchor. Standardise the Danish AI-policy template.

**Months 6–12: shift the mix.** Move remaining hourly customers to agreements. Set a target share of revenue
from fixed fees [Hans]. Train one network technician in the method. Decide on a partner or second senior.
Re-price based on what pilots actually took.

## 7. What to stop doing

- Billing hours for work agents do.
- Taking ad-hoc break/fix from new customers without an agreement.
- Doing by hand what your agents can prepare for your approval.
- Treating hardware and licence resale as a business rather than a convenience inside agreements.
- Defending tasks the customer's own AI can do; let them go and move up.
- Being the only place knowledge lives.
- Presenting DataMatrix as "vi". You are the product. Say "jeg" and back it with the network.
