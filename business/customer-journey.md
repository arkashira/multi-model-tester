Generated `customer-journey.md` for **multi-model-tester**.

Note: the output slot held a stale `pain-sentry` journey from a prior pipeline run — unrelated to this product, so I overwrote it with the correct content.

The map covers Aware → Consider → Try → Adopt → Expand, each with trigger event, friction points, user emotions, opportunities to delight, and a phase metric. Key opinionated calls:

- **North-star = Time-to-First-Diff (< 5 min).** The whole funnel hinges on a surprising cross-provider quality/latency/cost diff on the user's *own* prompt — that's the conversion engine, so Phase 3 (Try) gets the over-investment.
- **The moat is the CI loop (Phase 4),** not a dashboard — versioned, replayable cases living in PR checks turn "a tool I tried" into load-bearing infra. That's where retention is won.
- **Differentiation must be explicit in Consider** or we get filed as "promptfoo with a logo" — lead with the tri-axis (quality + latency + cost) verdict across providers.
- Deliberately positioned **out of the observability lane** (Helicone et al.) — we're the pre-prod gate, not prod logging.