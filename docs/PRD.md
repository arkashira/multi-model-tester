# Product Requirements Document (PRD)  
**Project:** multi-model-tester  
**Version:** 1.0 – 2026‑06‑22  
**Author:** Senior Product/Engineering Lead, Axentx  
**Status:** Draft  

---

## 1. Executive Summary  

The **multi-model-tester** is a prompt/LLM test harness that executes a single prompt and an edge‑case suite across multiple large‑language‑model (LLM) providers—OpenAI, Anthropic, Mistral, and Gemini. It captures output quality, latency, and token cost, then presents a diff view that is versioned and replayable. The goal is to give data‑driven insight into model performance for product teams, data scientists, and operations, enabling informed decisions about model selection, prompt engineering, and cost optimization.

---

## 2. Problem Statement  

1. **Fragmented Testing** – Teams currently run separate scripts per provider, leading to inconsistent test conditions and duplicated effort.  
2. **Lack of Comparative Metrics** – There is no unified view of latency, token usage, and output quality across providers, making it hard to benchmark and justify model choices.  
3. **Reproducibility Issues** – Tests are often ad‑hoc; reproducing a specific run for audit or debugging is difficult.  
4. **Cost Visibility** – Teams lack a clear, side‑by‑side cost comparison tied to actual prompts and responses.

---

## 3. Target Users  

| Persona | Role | Pain Points | How the Tool Helps |
|---------|------|-------------|--------------------|
| **ML Ops Engineer** | Deploy & maintain LLM workloads | Need reproducible benchmarks, cost monitoring | Versioned test runs, cost diff |
| **Data Scientist** | Experiment with prompts & models | Inconsistent test harnesses, hard to compare | Unified harness, side‑by‑side diff |
| **Product Manager** | Prioritize model features | No clear ROI data for model choices | Quantitative metrics (latency, cost, quality) |
| **Finance Analyst** | Budget LLM spend | Lack of granular cost breakdown | Token‑level cost per provider |

---

## 4. Goals & Success Metrics  

| Goal | Success Metric | Target |
|------|----------------|--------|
| **Unified Testing** | 1 test script runs across all providers | 100 % coverage |
| **Reproducibility** | Ability to replay any past run | 99 % success rate |
| **Insightful Comparison** | Side‑by‑side diff view available | 95 % of test cases |
| **Cost Transparency** | Token cost per provider displayed | 0 % missing data |
| **Developer Adoption** | 10+ internal teams using the tool | 10 % of Axentx teams |
| **Performance** | Average test run time ≤ 30 s per prompt | ≤ 30 s |

---

## 5. Key Features (Prioritized)  

1. **Provider‑agnostic Prompt Execution**  
   * One API to submit a prompt to OpenAI, Anthropic, Mistral, Gemini.  
   * Automatic selection of the correct endpoint, API key, and model version.

2. **Edge‑Case Suite Support**  
   * Load a YAML/JSON suite of prompts and expected outputs.  
   * Support for parameterized prompts (e.g., variable placeholders).

3. **Metrics Collection**  
   * **Latency** – request‑to‑response round‑trip per provider.  
   * **Token Usage** – prompt tokens, completion tokens, total.  
   * **Cost** – calculated from provider pricing APIs.  
   * **Quality Score** – optional user‑defined scoring (e.g., BLEU, ROUGE, or custom rubric).

4. **Diff Engine**  
   * Side‑by‑side comparison of raw outputs.  
   * Highlight differences at token, sentence, and semantic levels.  
   * Visual diff (diff‑style view) and statistical summary.

5. **Versioning & Replayability**  
   * Store each run in a lightweight database (SQLite or embedded JSON).  
   * Tag runs with commit hash, timestamp, and environment metadata.  
   * CLI/API to replay a specific run and regenerate diffs.

6. **CLI & Web UI**  
   * **CLI** – quick execution, scripting, CI integration.  
   * **Web UI** – interactive dashboard, filter by provider, date, prompt.  
   * Exportable reports (CSV, PDF).

7. **Extensibility Hooks**  
   * Plugin system to add new providers or custom scoring functions.  
   * Open‑source SDK for community contributions.

8. **Security & Compliance**  
   * Secure storage of API keys (environment variables, secrets manager).  
   * GDPR‑friendly data handling (option to scrub PII from logs).

9. **Documentation & Sample Suites**  
   * Comprehensive README, API docs, and example edge‑case suites.  
   * Integration guide for CI/CD pipelines.

---

## 6. Out‑of‑Scope  

| Item | Reason |
|------|--------|
| Real‑time streaming responses | Focus on batch prompt/response for now |
| Model fine‑tuning | Not part of testing harness |
| Proprietary scoring algorithms | Users can plug in their own |
| Multi‑tenant SaaS deployment | Internal tool for Axentx teams |
| Native integration with all possible LLM providers | Start with OpenAI, Anthropic, Mistral, Gemini |

---

## 7. Technical Architecture  

```
+----------------+      +----------------+      +----------------+
|  CLI/Web UI    |<---> |  Test Runner   |<---> |  Provider API  |
+----------------+      +----------------+      +----------------+
          |                        |                     |
          v                        v                     v
+----------------+      +----------------+      +----------------+
|  Metrics Store |<---> |  Diff Engine   |<---> |  Reporting API |
+----------------+      +----------------+      +----------------+
```

* **Test Runner** orchestrates prompt dispatch, collects responses, and records metadata.  
* **Metrics Store** is a lightweight SQLite DB with tables: `runs`, `prompts`, `responses`, `metrics`.  
* **Diff Engine** uses `difflib` for token‑level diffs and optional semantic similarity via embeddings.  
* **Reporting API** exposes REST endpoints for UI and external integrations.

---

## 8. Milestones  

| Milestone | Deliverable | Due |
|-----------|-------------|-----|
| 1 | Core CLI + provider abstraction | 2026‑07‑10 |
| 2 | Edge‑case suite loader + metrics collection | 2026‑07‑24 |
| 3 | Diff engine + versioning | 2026‑08‑07 |
| 4 | Web UI + reporting | 2026‑08‑21 |
| 5 | Documentation & CI integration | 2026‑09‑04 |
| 6 | Beta release to internal teams | 2026‑09‑18 |

---

## 9. Risks & Mitigations  

| Risk | Impact | Mitigation |
|------|--------|------------|
| API rate limits | Test failures | Implement back‑off, parallelism control |
| Pricing changes | Cost metrics inaccurate | Cache pricing data, update endpoint |
| Data privacy | PII leakage | Provide scrub option, enforce env vars |
| Adoption | Low usage | Early evangelism, demo sessions |

---

## 10. Dependencies  

| Dependency | Owner | Status |
|------------|-------|--------|
| Provider SDKs (OpenAI, Anthropic, Mistral, Gemini) | External | Up‑to‑date |
| Pricing APIs | Providers | Public |
| Internal secrets manager | Ops | Available |
| Axentx BRAIN (pgvector) | Internal | Optional for semantic diff |

---

## 11. Acceptance Criteria  

1. **CLI** runs a test suite and outputs a JSON report with all metrics.  
2. **Web UI** displays a diff view for each provider side‑by‑side.  
3. **Replay** a past run by ID and regenerate the same diff.  
4. **Cost** calculation matches provider pricing within ±5 %.  
5. **Documentation** includes a “Getting Started” guide and a sample suite.  

---

## 12. Appendix  

* **Sample Prompt Suite (YAML)**  
```yaml
- id: 001
  prompt: "Translate the following sentence to French: '{{sentence}}'"
  variables:
    sentence: "The quick brown fox jumps over the lazy dog."
  expected:
    - provider: openai
      output: "Le rapide renard brun saute par-dessus le chien paresseux."
```

* **License** – MIT (per repo)  

---
