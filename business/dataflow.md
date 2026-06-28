### `dataflow.md`

```markdown
## System Dataflow Architecture

### External Data Sources
- OpenAI API
- Anthropic API
- Mistral API
- Local/LLM model containers (optional)
- Git repositories (test case storage)
- Metadata sources (e.g., latency benchmarks, cost estimators)

---

### Ingestion Layer
- **API Gateway**
  - Unified REST/gRPC interface for test jobs
  - AuthN/Z via JWT/OAuth 2.0
- **Webhook Listener**
  - Git push -> trigger test execution
- **CLI Client**
  - Local test execution + results upload
- **Test Case Parser**
  - Parses YAML/JSON test suites into execution trees
  - Validates edge-case templates

---

### Processing/Transform Layer
- **Prompt Preprocessor**
  - Normalizes prompts across providers
  - Injects edge-case variations (typos, locale variants, etc.)
- **Model Router**
  - Dynamic model affinity (e.g., `gpt-4o` → OpenAI, `claude-3.5` → Anthropic)
- **Execution Engine**
  - Parallel LLM calls with timeout/rate-limit control
  - Token-cost calculator (per-provider pricing models)
- **Comparator**
  - Deterministic diffing: exact match, semantic similarity, hallucination scoring
  - Multi-metric scoring (BLEU, ROUGE, custom logic)
- **Cache Layer**
  - Provider response cache (Redis)
  - Cache invalidation on prompt/template change

---

### Storage Tier
- **Metadata DB** (PostgreSQL)
  - Test suites (schema: test_id, prompt, edge_cases, metadata)
  - Provider configs (API endpoints, rate limits)
  - Historical results (timestamp, model_version, metrics)
- **Object Storage** (S3-compatible)
  - Raw LLM responses
  - Binary artifacts (e.g., screenshots for GUI prompts)
- **Time-Series DB** (TimescaleDB)
  - Latency/cost trends over time

---
### Query/Serving Layer
- **REST API**
  - Retrieve test results (filter by model, suite, date range)
  - Generate reports (CSV/JSON/PDF)
- **GraphQL Gateway**
  - Aggregated metrics across providers/suites
- **Dashboard (React)**
  - Real-time test execution visualization
  - Regression heatmaps

---
### Egress to User
- **CLI Tool**
  - Local execution + diffing workflow
- **VS Code Extension**
  - Inline test results for prompt files
- **Web UI**
  - Shareable benchmark suites (public/private)
- **PDF/CSV Reports**
  - For stakeholder presentations

---
### **ASCII Block Diagram**
```plaintext
┌───────────────────────────────────────────────────────────────────────────────┐
│                            EXTERNAL DATA SOURCES                              │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────────┤
│  OpenAI API     │ Anthropic API   │  Mistral API    │ Git Repos (Test Suites)│
└────────┬────────┴────────┬────────┴────────┬────────┴─────────────┬─────────────┘
         │                 │                 │                     │
         ▼                 ▼                 ▼                     ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                            INGESTION LAYER                                    │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────────┤
│  API Gateway    │ Webhook Listener│ CLI Client      │ Test Case Parser       │
└────────┬────────┴────────┬────────┴────────┬────────┴─────────────┬─────────────┘
         │                 │                 │                     │
         ▼                 ▼                 ▼                     ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                       PROCESSING/TRANSFORM LAYER                              │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────────┤
│ Prompt Preproc. │ Model Router    │ Execution Eng.  │ Comparator              │
├─────────────────┼─────────────────┼─────────────────┼─────────────────────────┤
│ Cache Layer     │                 │                 │ Cache                   │
└────────┬────────┴────────┬────────┴────────┬────────┴─────────────┬─────────────┘
         │                 │                 │                     │
         ▼                 ▼                 ▼                     ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                            STORAGE TIER                                       │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────────┤
│ Metadata DB     │ Object Storage  │ Time-Series DB  │                         │
└────────┬────────┴────────┬────────┴────────┬────────┴─────────────┬─────────────┘
         │                 │                 │                     │
         ▼                 ▼                 ▼                     ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                         QUERY/SERVING LAYER                                   │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────────┤
│ REST API        │ GraphQL Gateway │ Dashboard       │                         │
└────────────┬────────┴────────┬────────┴────────┬────────┴─────────────┬─────────────┘
         │                 │                 │                     │
         ▼                 ▼                 ▼                     ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                          EGRESS TO USER                                        │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────────┤
│ CLI Tool        │ VS Code Ext.    │ Web UI          │ PDF/CSV Reports         │
└─────────────────┴─────────────────┴─────────────────┴─────────────────────────┘
```

---
### Auth Boundaries
1. **Ingestion** → API Gateway enforces JWT/OAuth 2.0 for test submissions.
2. **Processing** → Execution engine uses provider-specific API keys (stored in Vault).
3. **Storage** → Metadata DB rows scoped to team/project (row-level security).
4. **Egress** → Dashboard/VS Code extension inherits auth via JWT delegation.