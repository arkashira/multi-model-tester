# Roadmap

## Overview

`multi-model-tester` is a prompt/LLM test harness that runs the same prompt + edge‑case suite across OpenAI, Anthropic, Mistral, Gemini and diffs output quality, latency, and token cost side‑by‑side with versioned, replayable results.  
The roadmap below aligns with Axentx’s product‑creation pipeline: **MVP → v1 → v2**. Each phase is broken into concrete, shippable milestones, with clear MVP‑critical items highlighted.

---

## MVP (Launch)

| # | Milestone | Description | Deliverable | MVP‑Critical |
|---|-----------|-------------|-------------|--------------|
| 1 | **Prompt & Edge‑Case Engine** | Allow users to upload a prompt file (JSON/YAML) and a list of edge‑case prompts. | CLI tool `load-prompt` that parses and validates input files. | ✔ |
| 2 | **Model Adapter Layer** | Implement adapters for OpenAI, Anthropic, Mistral, Gemini. Each adapter must support: <br>• Authentication via env vars <br>• Unified request/response interface <br>• Token counting (prompt + completion) | `src/adapters/*.py` | ✔ |
| 3 | **Execution Engine** | Run the same prompt + edge‑case suite against all enabled models, collecting: <br>• Raw output <br>• Latency <br>• Token usage <br>• Cost (if available) | `src/executor.py` | ✔ |
| 4 | **Diff & Reporting** | Generate a side‑by‑side diff (textual diff + numeric comparison) and export to CSV/JSON. | `src/reporter.py` | ✔ |
| 5 | **CLI & Config** | Provide a command‑line interface (`multi-model-tester run`) with flags for: <br>• Prompt file <br>• Edge‑case file <br>• Output format <br>• Model selection | `cli.py` | ✔ |
| 6 | **Basic CI Pipeline** | GitHub Actions that run the test harness on push to `main` and publish a coverage badge. | `.github/workflows/ci.yml` |  |
| 7 | **Documentation** | README with usage, examples, and contribution guidelines. | Updated README |  |

**MVP Goal:** A fully functional CLI that can run a prompt suite against all four providers, collect metrics, and output a diff report. Release version `0.1.0`.

---

## v1 – Feature‑Rich Core

| # | Theme | Milestone | Description | Deliverable |
|---|-------|-----------|-------------|-------------|
| 1 | **Result Replay & Versioning** | Implement a lightweight SQLite store for test runs, keyed by commit hash and timestamp. | `src/store.py` |
| 2 | **Web UI Prototype** | Minimal React/Flask UI to upload prompts, view results, and compare runs. | `ui/` directory |
| 3 | **Advanced Metrics** | Add: <br>• Per‑token latency <br>• Temperature/Top‑P consistency <br>• Failure rate (e.g., timeouts) | `metrics.py` |
| 4 | **Custom Model Support** | Allow users to plug in local LLMs via vLLM or SGLang adapters. | `adapters/local.py` |
| 5 | **CI/CD Integration** | GitHub Action to automatically run tests on PRs and comment results. | `.github/workflows/pr-test.yml` |
| 6 | **Documentation & Tutorials** | Step‑by‑step guide, API reference, and example datasets. | `docs/` |
| 7 | **Beta Program** | Invite 5 external teams to test and provide feedback. | Feedback loop |

**MVP‑Critical for v1:** Result replay/store, advanced metrics, and local model support. These enable real‑world usage and differentiate from the baseline.

---

## v2 – Scale & Automation

| # | Theme | Milestone | Description | Deliverable |
|---|-------|-----------|-------------|-------------|
| 1 | **Distributed Execution** | Parallelize runs across multiple workers (Docker/K8s). | `src/distributed.py` |
| 2 | **Cost Estimation Engine** | Predict cost per run using provider pricing APIs. | `cost_estimator.py` |
| 3 | **Alerting & Monitoring** | Integrate with Prometheus/Grafana for real‑time metrics. | `monitoring/` |
| 4 | **Plugin System** | Allow third‑party adapters and reporters via entry points. | `plugins/` |
| 5 | **Security & Compliance** | Encrypt stored results, audit logs, and provide GDPR‑ready export. | `security/` |
| 6 | **Marketplace Integration** | Publish as a Docker image and Helm chart for easy deployment. | `docker/`, `helm/` |
| 7 | **Performance Benchmarks** | Publish benchmark suite comparing all providers on standard workloads. | `benchmarks/` |

**MVP‑Critical for v2:** Distributed execution, cost estimation, and plugin system. These enable enterprise adoption and extensibility.

---

## Release Cadence

| Version | Target Date | Key Deliverables |
|---------|-------------|------------------|
| 0.1.0 (MVP) | 2026‑07‑15 | CLI, adapters, diff report |
| 1.0.0 | 2026‑09‑30 | Store, UI prototype, advanced metrics |
| 2.0.0 | 2026‑12‑31 | Distributed exec, cost engine, plugin system |

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Test coverage | ≥ 90% |
| Average latency per run | ≤ 2 × provider baseline |
| Cost accuracy | ±5% |
| User adoption | ≥ 50 active installations by v1.0 |
| Feedback loop | ≥ 80% actionable feedback from beta program |

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Provider API changes | Abstract adapters, maintain versioned adapters, monitor changelogs |
| Token counting discrepancies | Use provider‑specific tokenizers, validate against official SDK |
| Data privacy | Encrypt local storage, provide opt‑out flags for sensitive data |
| Performance bottlenecks | Profile executor, implement async I/O, add caching |

---

### Next Steps

1. **Kickoff Sprint** – Assign tasks for MVP milestones.  
2. **Set up CI** – Ensure automated tests and linting.  
3. **Engage beta testers** – Reach out to existing Axentx clients.  

---
