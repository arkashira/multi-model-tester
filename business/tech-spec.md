Generated `tech-spec.md` for **multi-model-tester**. Summary of the v1 decisions:

- **Stack:** TypeScript/Node 20 + Fastify; official SDKs for OpenAI/Anthropic/Mistral/Gemini behind one normalized `Provider` interface; pluggable graders (exact, regex, json-schema, embedding-cosine, llm-as-judge); CLI-first with a Next.js diff grid.
- **Hosting ($0 v1):** Fly.io for the long-running diff worker (not serverless — jobs are N×M fan-outs), Vercel for UI, Supabase/Neon Postgres+pgvector, Cloudflare R2 for raw outputs (zero egress). Spend is BYO provider keys only.
- **Data model:** versioned-immutable `test_suites` → `test_cases` → `runs` → `results` (one per case×model) → `scores` (many graders per result) → precomputed `diffs`; envelope-encrypted `api_keys`.
- **API:** 10 endpoints incl. `POST /runs` (async), `GET /runs/:id/diff` (the side-by-side matrix), and `POST /runs/:id/replay` (the versioned/replayable hook from the hypothesis).
- **Security:** dual auth (bearer keys for CI, Supabase JWT for web), Postgres RLS, envelope-encrypted BYO keys, signed-TTL artifact URLs.
- **Observability:** correlation-id-per-run logs, Prometheus metrics centered on **cost-per-run by provider** and grader pass rate, OTel spans attributing latency (queue vs provider vs grading).
- **CI:** fixture-based provider tests (no live keys in PR), nightly real-key smoke that alerts on **provider schema/pricing drift**, ≥80% coverage gate on the eval/diff core.

Two notes worth flagging for downstream chain steps:
1. The file at `/tmp/tech-spec.md` previously held a spec for a different product (`agent-orchestra`) — I overwrote it. If that was meant to persist, it's recoverable from whatever wrote it, but it wasn't this product.
2. `agent-orchestra` overlaps heavily with the existing portfolio candidate *"managing multiple AI agents"* — worth a dedup check upstream, though it's outside this task's scope.

Design choices that most directly de-risk the hypothesis: **replayable versioned suites** (immutable `test_suites` + `/replay`) and **cost/latency/quality as first-class metrics** surfaced both in `/metrics` and the diff grid — that's the "diffs side-by-side" promise made measurable.