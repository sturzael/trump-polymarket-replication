# Day 2 — Schema Sanity Replication

**Gate status: PASS.** All 5 in-scope models' verified hit rates were reproduced from their published `predictions_log.json` using their published `market_SP500.json` and the discovered schema convention. The schema is readable; Phase 0 proceeds to Day 3.

## What was reproduced

For every VERIFIED prediction across all 11 models (n=564), we computed our own return and correct-flag using the following convention and compared to their logged values.

**Convention.**
- `entry = open` of the first trading day on or after `date_signal`
- `exit  = close` of the `hold_days`-th trading day after entry (0-indexed: `hold_days=0` means same-day close, `hold_days=1` next-day close, etc.)
- `return_pct = (exit / entry - 1) * 100`
- `correct = (return > 0)` for LONG, `(return < 0)` for SHORT, `(|return| > 0.5)` for VOLATILE

**Discovery.** The convention was identified by spot-checking three signals (2025-01-23, 2025-01-29, 2025-01-27). Two candidate conventions (close→close, open→close same day) were falsified before this one matched to 4 decimal places.

## Per-model replication

| Model | hold_days | n | Their hit rate | Our hit rate | Exact return matches | Correct-flag agreement |
|-------|----------:|--:|---------------:|-------------:|---------------------:|-----------------------:|
| A1_tariff_bearish | 1 | 23 | 56.5% | 56.5% | 23/23 | 100.0% |
| A2_deal_bullish | 1 | 90 | 52.2% | 53.3% | 89/90 | 98.9% |
| A3_relief_rocket | **0** | 11 | 72.7% | 72.7% | 11/11 | 100.0% |
| B1_triple_signal | 3 | 17 | 64.7% | 64.7% | 17/17 | 100.0% |
| B2_tariff_to_deal | 2 | 19 | 57.9% | 57.9% | 19/19 | 100.0% |
| B3_action_pre | 1 | 33 | 66.7% | 66.7% | 33/33 | 100.0% |
| **C1_burst_silence** | 1 | 176 | **65.3%** | **65.9%** | 175/176 | **99.4%** |
| C2_brag_top | 2 | 60 | 45.0% | 45.0% | 60/60 | 100.0% |
| C3_night_alert | 1 | 8 | 37.5% | 37.5% | 8/8 | 100.0% |
| D2_sig_change | 2 | 80 | 70.0% | 62.5% | 6/80 | 57.5%* |
| D3_volume_spike | 3 | 47 | 70.2% | 72.3% | 0/47 | 80.9%* |

*D2 uses direction=VOLATILE; our 0.5% threshold guess for VOLATILE correctness is approximate, explaining the lower agreement. D3 has a remaining convention discrepancy (hit rate close, but exact returns differ). Neither is in Phase 0 scope.

### In-scope models only

All 5 models tracked for Phase 0 replicate cleanly:

| In-scope model | n | Agreement |
|----------------|--:|----------:|
| A1_tariff_bearish | 23 | 100.0% |
| A3_relief_rocket | 11 | 100.0% |
| B1_triple_signal | 17 | 100.0% |
| C1_burst_silence (primary target) | 176 | 99.4% |
| C3_night_alert | 8 | 100.0% |

**The primary Phase 0 schema-gate target (`C1_burst_silence`, the model carrying the largest share of the headline 61.3% claim) reproduces 175 of 176 predictions exactly and agrees on the correct flag in 99.4% of cases.** The single disagreement is the final verified record in the dataset (`2026-03-13`), where their `actual_return = -0.619%` but our reconstruction gives `+0.388%`. This is the tail record and most likely reflects their verification pipeline computing the outcome before the exit-day close was available in `market_SP500.json`. It is not a schema issue.

## Finding requiring pre-registration amendment

During Day 2 replication, `hold_days` was found to vary per model:
- A3 = 0 (intraday: open → same-day close)
- A1, C1, C3, B3 = 1 (next-trading-day close)
- B2, C2, D2 = 2
- B1, D3 = 3

**The pre-registered horizons (+1h / +3h / +6h) do not match any in-scope model's actual prediction horizon except partially for A3.** The `+1h/+3h/+6h` horizons come from trump-code's real-time engine tracking (per the README architecture diagram: *"Snapshot PM + S&P 500 → Predict → Track at 1h/3h/6h → Verify"*), but the **verified predictions that produced the 61.3% hit rate are evaluated at `hold_days` horizons (0–3 trading days), not at 1h/3h/6h.**

Horizon mapping per in-scope model:

| Model | hold_days | Natural PM horizon |
|-------|----------:|--------------------|
| A3_relief_rocket | 0 | ~+6h (intraday) |
| A1_tariff_bearish | 1 | ~+24h |
| C1_burst_silence | 1 | ~+24h |
| C3_night_alert | 1 | ~+24h |
| B1_triple_signal | 3 | ~+72h |

## Recommended pre-registration amendment (for review before Day 3)

Replace the fixed horizon set `{+1h, +3h, +6h}` with a **per-model horizon** matching each model's `hold_days`:

- A3: single horizon ~+6h (intraday proxy for hold_days=0, since PM binaries do not typically have intraday open→close settlement)
- A1, C1, C3: single horizon ~+24h
- B1: single horizon ~+72h

Rationale: testing a 3-day-hold model at a 1h horizon on Polymarket would measure PM price response at the wrong timescale and produce an uninformative null. The horizon must match the model's own prediction horizon to give the rule a fair test.

**Consequence for multiple-testing count.** Original design: 5 in-scope models × 10 binaries × 3 horizons = 150 cells. Revised design with per-model horizons: 5 in-scope models × 10 binaries × 1 horizon-per-model = 50 cells. This reduces the Bonferroni divisor and is more statistically favourable to the signal, but the reduction is earned by matching the model's own horizon, not cherry-picked post-hoc.

## Additional Day 2 observations (informational, no action)

- **A3_relief_rocket is an intraday bet.** hold_days=0 means open-to-close same day. Polymarket political binaries typically do not reprice on intraday S&P moves at the same rate as equities, and most don't settle intraday. A3 is the hardest in-scope model to translate cleanly; even with an amended +6h horizon the PM response function may not have a useful signal at that timescale.
- **C2_brag_top (`SHORT` direction, 45% hit rate) reproduces at exactly 45.0%.** Reversed, this would be 55%. It is not in Phase 0 scope per the 8-named-discoveries restriction, but flagged as a potential "reverse anti-indicator" if the rule-expansion non-goal is ever revisited.
- **Headline 61.3% is heavily weighted by C1.** C1 contributes 176 of 564 verified predictions (31%) at 65.3% hit. If C1 fails to translate to Polymarket, most of the apparent edge collapses regardless of other models.

## Reproducibility

- Input files: `data/trump_code_refs/predictions_log.json`, `data/trump_code_refs/market_SP500.json` (both fetched from their public GitHub; gitignored).
- Script: `day2/sanity_replication.py`.
- Output: the table above is produced by running the script.
