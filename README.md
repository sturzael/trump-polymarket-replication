# Trump-Code × Polymarket Replication

An observation-only, pre-registered replication study testing whether the sstklen/trump-code signal set (8 named discoveries derived from Trump social-media posts) has tradeable edge on Polymarket mid-TVL political binaries.

**Status:** pre-planning. No data pulls have occurred. No code has been written.

## Integrity artefacts

- [`PRE_REGISTRATION.md`](PRE_REGISTRATION.md) — pre-registered rule set, binary-selection criteria, survival thresholds. Committed before any Polymarket price data is accessed.
- [`PHASE_0_PLAN.md`](PHASE_0_PLAN.md) — 10-day day-by-day schedule with blocking/non-blocking tagging and kill gates.
- [`RISKS.md`](RISKS.md) — five specific failure modes this experimental design is vulnerable to, with committed mitigations.

## What Phase 0 produces

A single-page `PHASE_0_VERDICT.md` with an explicit GO or KILL decision. GO requires at least one specific rule × horizon cell that clears every pre-committed threshold including Bonferroni-corrected significance. Default on mixed results is KILL.

## What Phase 0 does not produce

Any live trading, any capital deployment, any paper-trade harness against live markets, any Phase 1 design. Phase 1 scoping is a separate exercise conditional on a GO verdict.
