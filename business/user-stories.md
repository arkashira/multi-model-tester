# user-stories.md — multi-model-tester

## Epic 1: Cross-Provider Test Execution

### US-1.1 — Run one prompt across all providers
**As a** prompt engineer, **I want** to submit a single prompt and have it execute against OpenAI, Anthropic, Mistral, and Gemini in one command, **so that** I can compare provider behavior without wiring four SDKs by hand.
- **AC:** A single CLI/API call fans out to all configured providers concurrently.
- **AC:** Per-provider API keys are read from env/secrets, never hardcoded; missing-key providers are skipped with a warning, not a hard fail.
- **AC:** Partial failures (one provider 500s/times out) do not abort the run; failed providers are marked `error` with the raw message.
- **AC:** Default model per provider is configurable (e.g. `gpt-4o`, `claude-opus-4-8`, `mistral-large`, `gemini-2.5-pro`).
- **Complexity:** L

### US-1.2 — Pin model + sampling params per run
**As a** ML engineer, **I want** to pin exact model IDs and sampling params (temperature, top_p, max_tokens, seed) per provider, **so that** my comparison is reproducible and not skewed by silent default drift.
- **AC:** Each provider entry accepts an explicit model ID and param block.
- **AC:** Resolved params (including provider defaults that were filled in) are recorded in the run manifest.
- **AC:** Unsupported params for a given provider produce a validation warning rather than a crash.
- **Complexity:** M

### US-1.3 — Run an edge-case suite, not just one prompt
**As a** QA engineer, **I want** to attach a suite of edge-case inputs (empty, max-length, injection, non-English, malformed JSON) to a prompt template, **so that** I catch provider-specific failure modes before they hit production.
- **AC:** A suite is a set of named cases that share one prompt template with variable substitution.
- **AC:** Each case runs against every provider; results are addressable by `(case, provider)`.
- **AC:** Suite runs are parallelized with a configurable concurrency cap to respect rate limits.
- **AC:** A suite can be filtered to a subset of cases via tag or name for fast iteration.
- **Complexity:** L

---

## Epic 2: Comparison & Diffing

### US-2.1 — Side-by-side quality/latency/cost diff
**As a** prompt engineer, **I want** a side-by-side view of output, latency, and token cost for each provider on the same input, **so that** I can pick the best price/quality/speed tradeoff at a glance.
- **AC:** Output table shows response text, p50/p95 latency, input+output tokens, and computed USD cost per provider.
- **AC:** Cost is derived from a per-model pricing table that is versioned and overridable.
- **AC:** The cheapest, fastest, and (if a baseline is set) most-similar provider are visually flagged.
- **AC:** View is available as both terminal output and exportable JSON/HTML.
- **Complexity:** M

### US-2.2 — Semantic + textual output diff
**As a** ML engineer, **I want** to diff outputs across providers both textually and semantically, **so that** I can tell whether providers actually disagree in meaning or just in phrasing.
- **AC:** Textual diff highlights character/line-level deltas between any two selected providers.
- **AC:** An optional semantic similarity score (embedding cosine) is shown between each provider and a chosen baseline.
- **AC:** Similarity scoring is opt-in and works with a configurable/local embedding model to avoid forced extra cost.
- **Complexity:** M

### US-2.3 — Assertion-based pass/fail scoring
**As a** QA engineer, **I want** to attach assertions to a test case (regex match, JSON-schema valid, contains/excludes, latency < N ms, cost < $X), **so that** the harness gives me a deterministic pass/fail instead of eyeballing.
- **AC:** Each case supports multiple assertion types evaluated against every provider's output.
- **AC:** A run reports a pass/fail matrix and an aggregate pass rate per provider.
- **AC:** Exit code is non-zero when any assertion fails (CI-friendly).
- **AC:** Custom assertions can be supplied as a user-defined function/plugin.
- **Complexity:** L

---

## Epic 3: Versioning & Replay

### US-3.1 — Version test cases as code
**As a** prompt engineer, **I want** prompts, suites, and assertions stored as version-controlled files, **so that** prompt changes get reviewed and tracked like any other code.
- **AC:** Test cases are defined in human-readable files (YAML/JSON) checked into the repo.
- **AC:** A run records the case-file content hash so results map to an exact definition.
- **AC:** Schema validation catches malformed case files before execution.
- **Complexity:** S

### US-3.2 — Replay a past run deterministically
**As a** ML engineer, **I want** to replay any prior run by its run ID, **so that** I can reproduce or re-evaluate results without re-hitting paid APIs.
- **AC:** Every run persists inputs, resolved params, raw outputs, and metrics to a durable store.
- **AC:** Replay reconstructs the full comparison view from stored artifacts with zero new API calls.
- **AC:** Replay clearly labels results as cached vs. live.
- **Complexity:** M

### US-3.3 — Regression diff between two runs
**As a** QA engineer, **I want** to diff a new run against a saved baseline run, **so that** I get alerted when a model upgrade or prompt edit silently changes outputs, cost, or pass rate.
- **AC:** Two run IDs can be compared, surfacing deltas in pass rate, latency, cost, and output similarity per provider.
- **AC:** Regressions beyond a configurable threshold cause a non-zero exit code.
- **AC:** The diff is exportable as a report artifact for PR review.
- **Complexity:** M

---

## Epic 4: CI/CD & Team Integration

### US-4.1 — Run in CI on every prompt change
**As a** DevOps engineer, **I want** to run the harness headlessly in CI with a thresholded pass/fail gate, **so that** prompt regressions block merges automatically.
- **AC:** A single command runs a suite, emits JUnit/SARIF-style results, and sets exit code by gate result.
- **AC:** Secrets are injected via CI env vars; no interactive prompts.
- **AC:** Runtime and total spend per CI run are reported and capped by an optional budget limit.
- **Complexity:** M

### US-4.2 — Share results with the team
**As a** engineering lead, **I want** to publish a run's comparison report to a shareable HTML/link artifact, **so that** non-CLI stakeholders can review provider tradeoffs and sign off on a model choice.
- **AC:** A run exports a self-contained HTML report with the full comparison matrix.
- **AC:** Sensitive inputs can be redacted via a config flag before export.
- **AC:** Report includes run metadata (timestamp, models, case-file hash) for traceability.
- **Complexity:** S

### US-4.3 — Add a new provider without core changes
**As a** platform engineer, **I want** to register a new LLM provider via a plugin/adapter interface, **so that** we can adopt new models (or self-hosted endpoints) without forking the tool.
- **AC:** A documented adapter interface defines request, response-normalization, and cost-calculation hooks.
- **AC:** A new provider can be added by implementing the interface plus a pricing entry, with no changes to core run logic.
- **AC:** OpenAI-compatible endpoints (vLLM, Together, Groq, local) work through a single generic adapter.
- **Complexity:** M