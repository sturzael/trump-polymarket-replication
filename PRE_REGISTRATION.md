# Pre-Registration — Trump-Code × Polymarket Replication, Phase 0

**Status:** SCAFFOLD — not yet completed. Sections marked TODO are filled in on Day 1 of Phase 0 per `PHASE_0_PLAN.md`. This file's initial commit timestamp serves as the pre-registration timestamp; later edits appear as amendment commits with their own timestamps.

**Purpose.** Lock the test universe before any Polymarket price data is accessed. Without this, the experiment recreates the multiple-testing problem it is trying to escape.

**Amendment policy.** This file is append-only. If a value must be revised (e.g., fee threshold adjusted after Day 3 fee verification), the revision goes in a dated `## Amendment` section below, not in the original section. Original values remain visible.

---

## 1. Rules under test (the 8 named discoveries)

Verbatim from the trump-code README key-discoveries table. Mapped to `predictions_log.json` model_ids (see Day 1 schema note below for why this file, not `surviving_rules.json`).

| # | Discovery (verbatim from their README) | Their published evidence | Their published impact | `predictions_log.json` model_id | Their verified n | Their verified hit rate | Status for Phase 0 |
|---|----------------------------------------|--------------------------|------------------------|----------------------------------|------------------|--------------------------|---------------------|
| 1 | Pre-market RELIEF = strongest buy signal | Apr 9, 2025: S&P +9.52% | Avg +1.12% same-day | `A3_relief_rocket` | 11 | 72.7% | **Pre-filter underpowered** (n<15 before binary alignment) |
| 2 | TARIFF→SHORT is 70% wrong | Circuit breaker analysis | Auto-reversed to LONG | `A1_tariff_bearish` | 23 | 56.5% | In scope |
| 3 | China signals hidden on Truth Social only | 203 TS posts / 0 on X | 1.5x weight boost | (no model — weighting rule) | — | — | **Out of Phase 0 scope** (not a standalone predictor) |
| 4 | Truth Social publishes 6.2h before X | 38/39 posts matched | 6-hour trading window | (no model — timing observation) | — | — | **Out of Phase 0 scope** (corpus-timing finding, not a predictor) |
| 5 | Pure tariff day = most dangerous | Apr 3: -4.84%, Apr 4: -5.97% | Avg -1.057% | `A1_tariff_bearish` (shared with #2) | 23 | 56.5% | In scope (tested via the same model) |
| 6 | 4 signals combo = most profitable | 12 occurrences, 66.7% up | Avg +2.792% | `B1_triple_signal` | 17 | 64.7% | In scope |
| 7 | Silence = 80% bullish | Zero-post days analysis | Avg +0.409% | `C1_burst_silence` | 176 | 65.3% | In scope |
| 8 | Late-night tariff tweets = anti-indicator | 62% wrong → reverse = 62% right | Auto-inverted | `C3_night_alert` | 8 | 37.5% (62.5% reversed) | **Pre-filter underpowered** (n<15 before binary alignment) |

**Effective test set for Phase 0:** 6 in-scope discoveries mapped to 5 unique models (`A3_relief_rocket`, `A1_tariff_bearish`, `B1_triple_signal`, `C1_burst_silence`, `C3_night_alert`). Two discoveries (#3, #4) have no standalone predictor model to replicate and are marked out-of-scope. Two models (`A3_relief_rocket`, `C3_night_alert`) are already below the n≥15 minimum before Polymarket-binary overlap filtering further reduces usable n, and will almost certainly be marked UNDERPOWERED in the verdict. Reported regardless, not silently dropped.

**Locked before any Polymarket price access.** No rules will be added during Phase 0. No rules will be silently dropped; underpowered rules (n<15 observations) are marked UNDERPOWERED in the verdict, not excluded from reporting.

### Day 1 schema note

The plan as originally written instructed the Day 1 operator to look up rule IDs in `surviving_rules.json`. Inspection on Day 1 revealed that `surviving_rules.json` (600 composite-ID rules from the 31.5M-model brute-force search) is not the file that produced the headline 61.3% hit rate. The 564 verified predictions underlying the claim come from `predictions_log.json`, which is populated by **11 named models** operating at prediction time. The 8 named discoveries map to this 11-model system, not to the 600-rule survivor list. Pre-registration therefore uses `predictions_log.json` model_ids.

Independent verification: the overall verified hit rate computed locally from `predictions_log.json` is 61.35%, matching their published 61.3% to two decimal places. This is consistent with `predictions_log.json` being the correct source. It does not independently validate the claim; see Day 2 (sanity replication) and Day 3 (lag audit) for the structural checks.

One model in `predictions_log.json` (`D2_sig_change`, direction=VOLATILE, n=80, 70.0% hit) predicts magnitude not direction and is not mappable to a directional PM binary even if it were in the named-8 scope; out-of-scope for Phase 0 regardless.

Five other models in `predictions_log.json` (`A2_deal_bullish`, `B2_tariff_to_deal`, `B3_action_pre`, `C2_brag_top`, `D3_volume_spike`) are not among the 8 named discoveries and per the non-goal against scope expansion are excluded from Phase 0 testing.

---

## 2. Binary markets under test

**TODO Day 4.** To be populated during Day 4 binary selection per `PHASE_0_PLAN.md`. Selection criteria are pre-committed here; the selected list is appended as an amendment after Day 4 completes.

### Selection criteria (pre-committed)

- Polymarket political binaries (not sports, not crypto, not weather).
- Active window overlapped with at least one of trump-code's 566 signal-fire timestamps.
- TVL in the band **$100,000–$1,000,000 at the time of the overlapping signal fire**, measured from SII on-chain data, not from current Gamma snapshot.
- Maximum 10 binaries. If more qualify, retain the top 10 by median TVL during signal-fire windows.

### Selected binaries

(Populated Day 4 via amendment. Entries: slug + condition_id + overlap count.)

TODO Day 4.

---

## 3. Observation horizons

Fixed to match trump-code's published rules:

- **+1h** post signal fire
- **+3h** post signal fire
- **+6h** post signal fire

No additional horizons will be tested in Phase 0. No horizon will be dropped in reporting.

---

## 4. Survival thresholds

A rule is reported as "survives Phase 0" only if **all** of the following hold at the same (rule × horizon) cell:

| Threshold | Value |
|-----------|-------|
| Signal hit rate (direction matches prediction) | ≥ **55%** |
| Net fee-adjusted edge at fee_bps=7.2 | ≥ **2%** per trade |
| Signal hit rate margin over matched baseline | ≥ **5 percentage points** |
| Observations for the rule | ≥ **15** |
| Bonferroni-corrected p-value | < 0.05 / n_tests |
| Reverse-direction asymmetry | predicted-direction hit rate materially ≠ reverse-direction hit rate |
| Temporal stability | <10 percentage-point hit-rate differential between first-half and second-half |

**Default on mixed results is KILL.** A Phase 0 GO requires a *specific* rule × horizon that clears all seven criteria above, not an aggregate or averaged result.

### Fee sensitivity sweep (mandatory reporting)

Edge will be reported at `fee_bps ∈ {0, 3, 7.2, 15, 30}` for every rule, regardless of whether the rule meets the threshold at the canonical 7.2 bps. A rule that clears the threshold only at fee_bps=0 is documented but does not qualify as surviving.

---

## 5. Reporting commitment

- Results will be reported for **all 8 rules × all selected binaries × all 3 horizons**, not only the cells that appear favourable.
- Rules excluded for insufficient observations (n<15) will be reported as UNDERPOWERED with their observation count. They are not silently dropped.
- Both uncorrected and Bonferroni-corrected p-values will appear in every result table.
- Baseline hit rate will appear alongside signal hit rate in every result table.

---

## 6. Non-goals (locked)

1. No live trading at any phase. Paper only through Phase 2.
2. No rebuilding of the signal classifier. Trump-code's classifications are used as-is.
3. No expansion beyond the 8 named rules until after the Phase 0 kill/survive decision.
4. No equity-side trading or modeling. Polymarket only on the trading side.

---

## Amendments

(None yet. Each amendment is a dated subsection appended below, referencing the section it modifies. Original values above are not edited.)
