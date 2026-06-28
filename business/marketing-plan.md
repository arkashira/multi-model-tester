# marketing-plan.md — multi-model-tester

## Positioning

**Primary (1-line):** The Git-for-prompts eval harness — run one prompt across OpenAI, Anthropic, Mistral & Gemini and diff quality, latency, and $/token in versioned, replayable test cases.

**Alternatives (for A/B in ads/landing):**
1. *"Stop eyeballing prompt changes. Regression-test your LLM the way you test code."*
2. *"Switching providers shouldn't be a gamble — prove the swap before you ship it."*
3. *"CI for prompts: catch quality, cost, and latency drift before your users do."*

> Opinionated call: lead with **(Primary)** for devtools-literate buyers; A/B **(2)** against the cost-anxiety segment chasing GPT→Mistral/Gemini cost cuts — that's the sharpest near-term wedge in 2026.

---

## ICP — 3 personas

| Persona | Daily job | Pain we kill | Budget authority |
|---|---|---|---|
| **"Pipeline Priya" — AI/ML Platform Engineer** (Series A–C SaaS, 20–200 eng) | Owns the LLM gateway/abstraction layer; fields "which model should we use?" weekly. | No deterministic way to prove a model/prompt swap won't regress 100s of prompts. | Owns/influences **$500–2k/mo** tooling line; can expense ≤$300/mo solo. |
| **"Founder Felix" — technical solo/seed founder shipping an AI feature** | Codes the product + the prompts; burning runway on inference. | Can't see if Gemini Flash/Mistral gives 80% quality at 30% cost without manual testing. | Discretionary **$50–200/mo**; PLG self-serve, card on file. |
| **"Compliance Carla" — Eng Lead / Staff at regulated mid-market (fintech/health)** | Signs off that the AI feature is reliable + auditable before release. | Needs replayable, versioned eval evidence for audit & change-management. | Controls **$2k–10k/mo**; buys annual on invoice. |

> Wedge order: **Priya → Felix (volume/PLG) → Carla (expansion/$ACV)**. Priya is the champion who brings Carla's budget.

---

## Channels — top 3 with CAC

1. **Developer content + SEO (own the eval-keyword graph).** Target "openai vs anthropic cost", "llm regression testing", "prompt versioning". Plus an **open-source core** (MIT harness) as the top-of-funnel magnet → GitHub stars → cloud upsell.
   - *CAC est: ~$40–80 / activated user* (content cost amortized; OSS does the distribution).
2. **Community founder-led (Reddit r/SaaS, r/LocalLLaMA, HN "Show HN", Latent Space / MLOps Discords).** Ship comparison teardowns ("we ran the same 50 prompts across 4 models — here's the cost/quality table").
   - *CAC est: ~$15–50 / signup* (time, not $; highest ROI early).
3. **Targeted paid: LinkedIn + Google Search on bottom-funnel intent.** Retarget OSS visitors; bid on "llm evaluation tool".
   - *CAC est: ~$120–250 / qualified team trial* — turn on only after channels 1–2 prove activation.

> Blended target CAC ≤ **$90**, payback < **3 months** at a $29–49 entry seat.

---

## Content cadence (week-by-week, 12 weeks)

- **W1:** Launch "Model Cost/Quality Index" blog (live benchmark) — flagship SEO asset.
- **W2:** OSS repo polish + README demo GIF; "Show HN" draft.
- **W3:** Teardown: *"GPT-4 → Mistral Large: we replayed 200 prod prompts. Here's what broke."*
- **W4:** Tutorial: *"Add prompt regression tests to your CI in 10 min."*
- **W5:** Reddit/Discord teardown #2 (Gemini Flash cost story).
- **W6:** Guest pod/newsletter (Latent Space / MLOps).
- **W7:** Case-study #1 (design partner — Priya persona).
- **W8:** Comparison page vs. manual/notebook eval + vs. Langfuse/Promptfoo (capture competitor SEO).
- **W9:** Webinar/live stream: "Prove a provider swap in 30 min."
- **W10:** Template pack: 20 reusable edge-case test suites (lead magnet).
- **W11:** Case-study #2 + cost-savings calculator (interactive).
- **W12:** Update the Cost/Quality Index w/ new models → re-distribute everywhere (compounding asset).

> Cadence rule: **2 distribution touches per asset** (publish + syndicate). One flagship SEO asset/month, one community teardown/week.

---

## Launch milestones

- **D-30 — Private beta.** 5 design partners (3 Priya, 2 Felix). Lock core diff (quality/latency/cost) + replay. Instrument activation. Index v1 drafted.
- **D-0 — Public launch.** OSS repo public + Show HN + Product Hunt + Cost/Quality Index goes live. Goal: **300+ GitHub stars, 150 signups week 1.**
- **D+30 — PLG self-serve live.** Paid tier ($29 solo / $99 team) shipped; CI integration (GitHub Action) GA. First paying logos. Goal: **15 paying accounts.**
- **D+90 — Repeatable motion.** Channel 1+2 producing predictable signups; 2 published case studies; Carla-segment (annual/invoice) outbound pilot started.

---

## Success metrics (by D+90)

| Metric | D+30 | D+90 target |
|---|---|---|
| GitHub stars | 400 | **1,000+** |
| Signups (cumulative) | 400 | **1,500** |
| Activated (ran ≥1 multi-model diff) | 35% | **≥45%** |
| **DAU** | ~40 | **120–150** |
| Paying accounts | 15 | **60** |
| **MRR** | ~$700 | **$4–6k MRR** |
| Logo CAC / payback | — | **≤$90 / <3 mo** |
| OSS→paid conversion | — | **3–5%** |

> Honest stance: $4–6k MRR by D+90 is a *traction-proof*, not a business — the win condition is **activation ≥45% + OSS star velocity**, which are the leading indicators that the $50k+ ARR ramp in months 4–9 is real.

---

I wrote this as the `marketing-plan.md` section of the business pack. Want me to save it to a file in `/tmp` or generate the next section (pricing, GTM-economics, or competitive teardown)?