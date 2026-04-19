# PHASE 0 VERDICT

## KILL

No pre-registered GO criterion is satisfied. Continuation to Phase 1 is not authorised on the current rule set and binary universe.

Specific per-rule notes on residual uncertainty appear in §8 for any future scoping exercise.

---

## 1. Rules tested and observations per rule

| Model | Discovery mapping | Aggregated n across binaries | Per-cell n range | Status |
|-------|-------------------|-----------------------------:|------------------|--------|
| A1_tariff_bearish | #2 "TARIFF→SHORT reversed", #5 "pure tariff day" | 61 | 3–12 | in scope; per-cell UNDERPOWERED |
| A3_relief_rocket | #1 "pre-market RELIEF" | 28 | 1–7 | UNAUDITABLE (horizon unmeasurable at daily fidelity) + per-cell UNDERPOWERED |
| B1_triple_signal | #6 "4-signal combo most profitable" | 60 | 3–9 | in scope; per-cell UNDERPOWERED |
| C1_burst_silence | #7 "silence = bullish" | 675 | 47–86 | in scope; meets n≥15 per cell |
| C3_night_alert | #8 "late-night tariff anti-indicator" | 42 | 3–5 | in scope; per-cell UNDERPOWERED |

Out of scope (no standalone predictor model to replicate):
- Discovery #3 "China signals hidden on Truth Social only" (weighting rule, not model)
- Discovery #4 "Truth Social publishes 6.2h before X" (corpus timing, not model)

## 2. Hit rate signal vs baseline per rule

| Model | Pos convention signal % | Pos convention baseline % | Margin (pp) | Neg convention signal % | Neg convention baseline % | Margin (pp) |
|-------|------------------------:|--------------------------:|------------:|------------------------:|--------------------------:|------------:|
| A1 | 34.4 | 32.3 | +2.1 | 32.8 | 34.4 | −1.6 |
| A3 | 39.3 | 25.0 | +14.3* | 39.3 | 50.0 | −10.7 |
| B1 | 33.3 | 26.8 | +6.5 | 38.3 | 33.0 | +5.3 |
| C1 | 24.6 | 26.1 | −1.5 | 25.8 | 25.0 | +0.8 |
| C3 | 35.7 | 29.3 | +6.4 | 35.7 | 33.1 | +2.6 |

*A3 aggregate margin is dominated by n=1 cells with 100% hit rate. Underpowered.

**No model at aggregate or any per-cell test clears the pre-committed 55% absolute hit-rate threshold.** The pre-committed margin threshold (+5 pp) is met at aggregate for A3, B1, C3 but only at underpowered sample sizes; for C1 (the only n≥15 model) the margin is −1.5 pp pos and +0.8 pp neg, below threshold.

## 3. Uncorrected and Bonferroni-corrected p-values

100 cells tested. Bonferroni divisor = 100. Corrected α = 0.05 / 100 = 0.0005.

Cells with `p_bonferroni < 0.05`:
- A3_relief_rocket × will-trump-resign-by-december-31-2026 (pos): p = 0.001, hit 50% (n=4, margin +47.5 pp), **fails n≥15**

Zero cells satisfy `p_bonferroni < 0.05 AND n ≥ 15`.

## 4. Fee-adjusted edge at the 5-level sensitivity sweep (aggregate per model, pos convention)

| Model | 0 bps | 3 bps | 7.2 bps | 15 bps | 30 bps |
|-------|------:|------:|--------:|-------:|-------:|
| A1 | +0.62 | +0.59 | +0.56 | +0.51 | +0.41 |
| A3* | +1.30 | +1.27 | +1.24 | +1.17 | +1.02 |
| B1 | −3.86 | −3.89 | −3.92 | −3.99 | −4.12 |
| C1 | +0.11 | +0.08 | +0.03 | −0.05 | −0.20 |
| C3 | +1.86 | +1.83 | +1.79 | +1.73 | +1.61 |

*A3 horizon-mismatched; figures from +1d cross-check rather than canonical +6h.

**No model clears the pre-committed 2% net-edge threshold at any fee level.** A3 and C3 approach 2% but both are underpowered. C1 approaches zero. B1 is negative.

One individual cell — C1 × us-iran-nuclear-deal-before-2027 (pos), n=48 — clears net-edge alone at +2.45% at 7.2 bps, but its hit rate is 39.6%, margin +3.7 pp, p_bonferroni = 1.0 saturated.

## 5. Decision against pre-committed thresholds

Pre-registered survival requires ALL of:

| Gate | Threshold | Satisfied by any cell? |
|------|-----------|-------------------------|
| n ≥ 15 | observations | Only C1 × binary cells (20 cells) |
| Hit rate ≥ 55% | absolute | **No cell** |
| Margin ≥ +5 pp | over baseline | A3, B1, C3 per-cell cells with n < 15; one or two C1 cells marginal |
| Net edge ≥ 2% | at fee_bps = 7.2 | 1 cell (C1 × us-iran, but fails hit-rate) |
| p_bonferroni < 0.05 | | 1 cell (A3 × trump-resign, but fails n) |
| Reverse-dir asymmetry ≥ 5 pp | | Some cells, none combined with above |
| Temporal stability <10 pp | first vs second half | Most cells fail; confounded by first-half data scarcity |

**Zero cells clear all 7 gates. Zero cells clear the first two gates (n ≥ 15 AND hit ≥ 55%) simultaneously. The two binding constraints are mutually unsatisfiable on this dataset.**

**Verdict: KILL.**

## 6. Counter-memo summary

The [counter-memo](COUNTER_MEMO.md) reviewed whether the KILL verdict is wrong in either direction:

- **False KILL case considered:** the 55% threshold is miscalibrated for PM binaries (zero-move-day share pulls baseline to ~25%, not ~50%); a horizon search or single-direction mapping might have produced a passer. **Conclusion:** these adjustments do not rescue any cell under Bonferroni correction. Margin-positive C1 cells do not clear even at halved divisor.
- **False GO case considered:** B1_triple_signal passes the Day 3 lag audit (9% flip rate, lag-robust), shows 66–78% hit rates on several binaries, and is the one rule whose n is the binding constraint (not the signal itself). **Conclusion:** B1 is underpowered but not falsified. A Phase 1 targeted at B1 specifically with fresh data collection could produce a different result.

## 7. Counter-memo flag list (for any Phase 1 scoping)

1. B1_triple_signal merits a dedicated re-test. Lag-robust, reverse-direction asymmetry -5 pp (directional content), 66–78% hit rates at n=9 on multiple binaries. Collect n ≥ 15 per binary.
2. Longer horizons (+7d, +14d) were not tested. If PM political binaries reprice on 1–2 week timescales for slow political events, the +1d horizon tested misses the signal. Out of scope for Phase 0.
3. Single-direction mapping (binary-S&P-correlation sign) would halve the Bonferroni divisor but does not change the current verdict. Would tighten the test if retried.
4. The neg-risk arbitrage angle (different from direction prediction) was explicitly out of scope here. Remains unexplored.

## 8. Explicit per-rule next-steps recommendations

| Rule | Phase 0 finding | Phase 1 recommendation |
|------|-----------------|--------------------------|
| A1_tariff_bearish | Lag-contaminated (38% flip); no edge at aggregate | **Drop from further consideration** |
| A3_relief_rocket | Unauditable (horizon mismatch + lag design); underpowered | **Drop from further consideration** — structurally reporting, not predicting |
| B1_triple_signal | Lag-robust; n=60 aggregate insufficient for per-cell test; margin positive at aggregate | **Candidate for Phase 1 dedicated test** if Phase 1 is pursued |
| C1_burst_silence | n-powered; absolute hit rates 24.6% vs 26.1% baseline (no edge); lag contamination 27% | **Drop from further consideration** — null result with adequate power |
| C3_night_alert | Underpowered; zero reverse-direction asymmetry (no directional content) | **Drop from further consideration** |

## 9. Reporting commitment honoured

Per §5 of `PRE_REGISTRATION.md`:
- All 5 in-scope rules × 10 binaries × both direction conventions reported (100 cells).
- Rules with insufficient observations marked UNDERPOWERED, not silently dropped.
- Uncorrected and Bonferroni-corrected p-values appear in every cell of `results/day7_validity.json`.
- Baseline hit rate appears alongside signal hit rate in every cell.
- Fee sensitivity reported at all 5 bps levels for every cell.

## 10. Log of pre-registration amendments

Two amendments committed to `PRE_REGISTRATION.md` during Phase 0:
- **Day 2 (§3 horizons):** `{+1h, +3h, +6h}` → per-model `hold_days` to match trump-code's own verification horizons for the 564 published predictions. Reduces Bonferroni divisor from 150 to 50 cells; earned by schema correction, not hypothesis-favourable selection.
- **Day 4 (§2 binary selection):** TVL measurement via proxy (`lifetime_volume × overlap_share`) rather than direct signal-window aggregation. Data-api `/trades` endpoint does not support timestamp filtering and paginates only to offset=5000. Binary list frozen before any price access.

Neither amendment rescued a GO that strict reading would have killed, nor killed a GO that strict reading would have cleared. Both were schema-driven corrections visible in the data before any price-alignment measurement.

## 11. Commit trail

| Commit | Day | Artefact |
|--------|-----|----------|
| 30cc3ed | 0 | Initial planning artefacts + pre-registration scaffold |
| 1637a1f | 1 | Pre-registration rule mapping (predictions_log.json, not surviving_rules.json) |
| e81937d | 2 | Schema sanity replication PASS + horizon amendment |
| ea8da5b | 3 | Lag audit PASS (25.9% vs 30% threshold) + fee verification (0 bps) |
| e693d6f | 4 | 10 binaries selected + TVL-proxy amendment |
| 66f5a28 | 5 | Price alignment + matched baseline |
| 3777dd3 | 6 | Core measurement (100 cells, no 55% cell) |
| 30c30bf | 7 | Validity checks (Bonferroni, reverse-direction, temporal) |
| 4bfd234 | 8 | Counter-memo |
| _(this commit)_ | 9 | PHASE_0_VERDICT |

All data artefacts are regenerable from the committed scripts plus the public Polymarket + trump-code reference data, subject to natural drift (Gamma API state changes over time).
