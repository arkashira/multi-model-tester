# TECH_SPEC.md – Multi‑Model Tester

## 1. Overview

**Multi‑Model Tester** is a prompt‑/LLM‑test harness that executes a single prompt (or a suite of edge‑case prompts) against multiple large‑language‑model (LLM) providers (OpenAI, Anthropic, Mistral, Gemini, etc.).  
It records:

* **Output quality** – token‑level diff, semantic similarity, custom metrics.  
* **Latency** – request/response round‑trip, token‑rate.  
* **Token cost** – provider‑specific pricing.  

All results are stored in a versioned, replayable format enabling side‑by‑side comparison and regression testing.

---

## 2. Architecture

```
┌─────────────────────┐
│  Prompt Repository  │  <-- JSON/YAML files + edge‑case metadata
└─────────────┬───────┘
              │
              ▼
┌─────────────────────┐
│  Test Orchestrator  │  <-- CLI / REST API
└───────┬─────────────┘
        │
        ▼
┌─────────────────────┐
│  Provider Adapters  │  <-- OpenAI, Anthropic, Mistral, Gemini, etc.
└───────┬─────────────┘
        │
        ▼
┌─────────────────────┐
│  Result Collector   │  <-- Aggregates metrics, diffs, cost
└───────┬─────────────┘
        │
        ▼
┌─────────────────────┐
│  Storage Layer      │  <-- PostgreSQL + JSONB + S3 for raw logs
└───────┬─────────────┘
        │
        ▼
┌─────────────────────┐
│  Reporting & UI     │  <-- FastAPI + React (optional)
└─────────────────────┘
```

### 2.1 Components

| Component | Responsibility | Key Interfaces |
|-----------|----------------|----------------|
| **Prompt Repository** | Stores prompts, edge‑case suites, and metadata. | `PromptLoader.load(path) -> PromptSuite` |
| **Test Orchestrator** | CLI/REST entry point; schedules runs, handles concurrency. | `run_suite(suite_id, provider_list)` |
| **Provider Adapters** | Abstracts provider APIs, handles auth, retries, rate‑limits. | `LLMAdapter.invoke(prompt, params) -> LLMResponse` |
| **Result Collector** | Normalizes responses, computes metrics, stores diffs. | `collect(response, metadata) -> ResultRecord` |
| **Storage Layer** | Persists results, metrics, raw logs. | CRUD via SQLAlchemy ORM |
| **Reporting & UI** | Visualizes results, diff charts, cost breakdown. | REST endpoints, WebSocket for live updates |

---

## 3. Data Model

### 3.1 Core Tables

| Table | Columns | Notes |
|-------|---------|-------|
| `prompt_suite` | `id`, `name`, `description`, `created_at`, `updated_at` | One suite = one test run set |
| `prompt` | `id`, `suite_id`, `prompt_text`, `metadata_json` | Edge‑case flags, tags |
| `provider_run` | `id`, `prompt_id`, `provider_name`, `model_name`, `timestamp`, `latency_ms`, `tokens_in`, `tokens_out`, `cost_usd` | One row per provider per prompt |
| `response` | `run_id`, `content`, `metadata_json` | Raw response text + provider metadata |
| `diff` | `run_id_a`, `run_id_b`, `diff_text`, `semantic_score` | Side‑by‑side diff between two runs |
| `metric` | `run_id`, `metric_name`, `value` | e.g., BLEU, ROUGE, custom |

### 3.2 JSONB Fields

* `metadata_json` in `prompt`, `response`, `metric` tables stores provider‑specific fields (e.g., `temperature`, `top_p`).

---

## 4. Key APIs / Interfaces

### 4.1 Provider Adapter Interface

```python
class LLMAdapter(Protocol):
    name: str
    model: str

    async def invoke(
        self,
        prompt: str,
        **params: Any
    ) -> LLMResponse: ...
```

`LLMResponse` contains:

```python
@dataclass
class LLMResponse:
    content: str
    usage: UsageMetrics
    metadata: Dict[str, Any]
```

### 4.2 Orchestrator API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/run` | POST | Trigger a test run. Body: `{ "suite_id": int, "providers": ["openai", "anthropic"] }` |
| `/status/{run_id}` | GET | Poll status. |
| `/results/{run_id}` | GET | Retrieve aggregated results. |

### 4.3 CLI Commands

```
multi-model-tester run <suite-id> --providers openai,anthropic
multi-model-tester status <run-id>
multi-model-tester results <run-id> --format json
```

---

## 5. Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Backend** | Python 3.12 | Mature async ecosystem |
| **Web Framework** | FastAPI | Async, auto‑docs, lightweight |
| **Database** | PostgreSQL 16 | ACID, JSONB, full‑text search |
| **ORM** | SQLAlchemy 2.0 | Declarative, async support |
| **Provider SDKs** | `openai`, `anthropic`, `mistralai`, `google-generativeai` | Official clients |
| **Diff Engine** | `difflib`, `semantic-text-similarity` (sentence‑transformers) | Text diff + semantic score |
| **Metrics** | `nltk`, `rouge-score`, `bleurt` | NLP evaluation |
| **Containerization** | Docker, Docker‑Compose | Reproducible builds |
| **CI/CD** | GitHub Actions | Lint, test, build, publish |
| **Deployment** | Kubernetes (Helm) | Horizontal scaling, secrets |
| **Secrets** | Vault / KMS | Store API keys |
| **Logging** | Loguru + Loki | Structured logs |
| **Monitoring** | Prometheus + Grafana | Latency, cost metrics |

---

## 6. Dependencies

| Category | Package | Version |
|----------|---------|---------|
| Core | `fastapi` | ^0.110.0 |
| | `uvicorn[standard]` | ^0.29.0 |
| | `sqlalchemy` | ^2.0.30 |
| | `asyncpg` | ^0.29.0 |
| | `pydantic` | ^2.7.0 |
| | `openai` | ^1.30.0 |
| | `anthropic` | ^0.20.0 |
| | `mistralai` | ^0.4.0 |
| | `google-generativeai` | ^0.5.0 |
| | `sentence-transformers` | ^3.0.0 |
| | `rouge-score` | ^0.1.2 |
| | `bleurt` | ^0.1.0 |
| | `difflib` | stdlib |
| | `loguru` | ^0.7.2 |
| | `prometheus-client` | ^0.20.0 |
| | `pytest` | ^8.2.0 |
| | `httpx` | ^0.27.0 |
| | `docker` | ^7.0.0 |

All dependencies are pinned in `pyproject.toml` and `requirements.txt`.

---

## 7. Deployment

### 7.1 Local Development

```bash
# Install dependencies
poetry install

# Run migrations
alembic upgrade head

# Start API
poetry run uvicorn app.main:app --reload

# Run CLI
poetry run multi-model-tester run 1 --providers openai,anthropic
```

### 7.2 Docker

```bash
docker build -t axentx/multi-model-tester:latest .
docker run -e DATABASE_URL=postgres://... -e OPENAI_API_KEY=... \
  -e ANTHROPIC_API_KEY=... -p 8000:8000 axentx/multi-model-tester:latest
```

### 7.3 Kubernetes

* Helm chart `charts/multi-model-tester` contains:
  * Deployment (replicas, resources)
  * Service (ClusterIP)
  * Ingress (TLS)
  * ConfigMap for provider config
  * Secret for API keys
  * PersistentVolumeClaim for PostgreSQL (or external DB)

```bash
helm upgrade --install multi-model-tester ./charts/multi-model-tester \
  --set image.tag=latest \
  --set env.OPENAI_API_KEY=...
```

### 7.4 CI/CD Pipeline

* **Lint**: `ruff`, `black`
* **Test**: `pytest --cov`
* **Build**: Docker image, push to registry
* **Deploy**: Helm upgrade on merge to `main`

---

## 8. Security & Compliance

| Concern | Mitigation |
|---------|------------|
| API Keys | Stored in Vault/KMS, injected as env vars |
| Data Leakage | All provider responses are encrypted at rest (PostgreSQL TLS) |
| Rate‑Limiting | Adapter layer respects provider limits, exponential backoff |
| GDPR | Prompt & response data can be flagged for deletion; audit logs retained 30 days |

---

## 9. Extensibility

* **Add Provider**: Implement `LLMAdapter` for new SDK, register in `adapters/__init__.py`.
* **Custom Metrics**: Add to `metrics/` package, expose via `MetricRegistry`.
* **UI Enhancements**: React SPA consumes `/results` endpoint; can plug into existing Axentx dashboard.

---

## 10. Roadmap

| Milestone | Description | Target |
|-----------|-------------|--------|
| **v1.0** | Core multi‑provider harness, basic diff, cost, latency | Q3 2026 |
| **v1.1** | Semantic similarity metric, replayable logs | Q4 2026 |
| **v2.0** | UI dashboard, CI integration, auto‑scaling | Q2 2027 |

---

*Prepared by: Senior Product/Engineering Lead – Axentx*
