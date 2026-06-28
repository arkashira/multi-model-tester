# breakeven.md

## Unit Economics — Cost per Active User

Assumptions: the harness is BYO-key (users plug in their own provider API keys), so LLM inference cost is **not** on our P&L — that's the structural margin advantage of an eval tool vs. a wrapper. Our COGS is orchestration, storage of versioned test cases/results, and result diffing/replay compute.

| Cost component | Basis | Light user | Active user | Power user |
|---|---|---|---|---|
| Orchestration compute (fan-out runs, diffing, replay) | ~$0.00004/test-case exec on shared workers | 2K runs/mo → $0.08 | 25K runs/mo → $1.00 | 150K runs/mo → $6.00 |
| Storage (versioned cases + result blobs, pgvector embeds) | ~$0.05/GB-mo, ~0.5KB/result + embeddings | 0.4 GB → $0.02 | 3 GB → $0.15 | 18 GB → $0.90 |
| Bandwidth (provider egress proxy + dashboard) | ~$0.02/GB | 1 GB → $0.02 | 8 GB → $0.16 | 40 GB → $0.80 |
| Control plane amortized (API, auth, queue) | flat per-seat | $0.30 | $0.45 | $0.70 |
| **Total COGS / user / mo** | | **~$0.42** | **~$1.76** | **~$8.40** |

**Blended COGS at target mix (70% active / 20% light / 10% power): ≈ $2.18/user/mo.** Gross margin at the Team tier (below) is **~93%**.

> Risk fl: if we ever offer managed keys (pooled provider billing), COGS jumps 20–80× and margin collapses to wrapper economics. Keep BYO-key as the default; managed-keys is a metered pass-through line item only.

---

## Pricing Tiers

| Tier | $/mo | Target | Key features |
|---|---|---|---|
| **Solo** | **$29** | Individual devs, indie builders | BYO keys, 4 providers (OpenAI/Anthropic/Mistral/Gemini), 1 user, 50 versioned test suites, 10K runs/mo, side-by-side quality/latency/cost diff, 30-day result history, CLI + web |
| **Team** | **$149** | Eng teams shipping LLM features | Everything in Solo + 5 seats ($25/extra seat), unlimited suites, 150K pooled runs/mo, CI/CD integration (GitHub Actions/GitLab), regression gates (fail build on quality/cost drift), shared replay library, 1-yr history, Slack alerts |
| **Scale** | **$599** | Platform/AI-infra orgs | Everything in Team + 20 seats, SSO/SAML, 1M pooled runs/mo, custom provider/self-hosted model endpoints, audit logs, SLA, eval dataset import from our BRAIN corpora, priority support, on-prem runner option |

Annual: 2 months free (≈17% off). Overage runs billed at $1 / 10K runs.

---

## CAC Range

PLG-led, bottom-up motion (content + OSS harness core + dev communities).

- **Solo (self-serve):** $40–$90 — SEO/content, Reddit r/SaaS & r/LLMDevs, organic. Payback < 2 months.
- **Team (self-serve + light sales-assist):** $300–$650 — trials converting via CI integration; some founder-led demos. Payback ~3–4 months.
- **Scale (sales-touch):** $2,500–$5,000 — outbound + design-partner motion. Payback ~5–8 months.
- **Blended target CAC:** **~$220** at a 75/20/5 tier mix.

---

## LTV Estimate

Assumed gross margin **92%**; monthly logo churn by tier: Solo 6%, Team 3%, Scale 1.5%.

| Tier | ARPA/mo | Avg lifetime | Gross-margin LTV |
|---|---|---|---|
| Solo | $29 | ~17 mo | **~$453** |
| Team | $149 | ~33 mo | **~$4,525** |
| Scale | $599 | ~67 mo | **~$36,900** |

**Blended LTV (75/20/5 mix): ≈ $2,000.** Blended **LTV:CAC ≈ 9:1** — healthy; the economics are carried by Team, which should be the primary funnel target.

---

## Break-Even Users Count

Fixed monthly burn (lean: 2 founders + infra base + tooling): **~$22,000/mo**.

Contribution margin per user/mo (price − blended COGS $2.18):
- Solo: $26.82
- Team: $146.82 (÷5 seats ≈ effective)
- Scale: $596.82

Break-even scenarios (single-tier equivalent):
- **All Solo:** ~820 paying users
- **All Team:** ~150 accounts
- **Realistic mix (75/20/5):** **≈ 430 paying accounts** → covers the $22K burn.

---

## Path to $10K MRR

Anchor on **Team @ $149** as the workhorse tier — it has the best LTV:CAC and aligns with the CI/regression-gate value prop that drives retention.

**Recommended path — Team-led mix:**
| Tier | Accounts | MRR |
|---|---|---|
| Team ($149) | 55 | $8,195 |
| Solo ($29) | 45 | $1,305 |
| Scale ($599) | 1 | $599 |
| **Total** | **101** | **$10,099** |

**Simplest single-tier path:** **68 Team accounts × $149 = $10,132 MRR.**

**Realistic ramp (BYO-key, PLG):**
1. **M0–2:** OSS harness core + free tier → top of funnel; convert first 30 Solo.
2. **M3–5:** Land CI/CD integration → flip 15–20 Solo teams to Team; first design-partner Scale account.
3. **M6:** ~55 Team + 45 Solo + 1 Scale → **$10K MRR crossed**, ~$8K CAC-recovered, contribution-positive against the $22K burn within ~2 further months of the same slope.

**At $10K MRR:** ~101 accounts, blended COGS ~$0.6K/mo → **~94% gross margin**, leaving the wedge cleanly profitable per-account well before fixed-cost break-even at ~430 accounts.