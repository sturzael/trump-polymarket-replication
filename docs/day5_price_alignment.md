# Day 5 — Price Alignment + Matched Non-Signal Baseline

Status: aligned dataset produced, 866 records × 10 matched non-signal baselines per record = 8,660 baseline rows. No binary returned empty data. Ready for Day 6 core measurement.

## Data acquired

Daily YES-outcome price history pulled via `https://clob.polymarket.com/prices-history?market=<yes_token>&interval=max&fidelity=1440`. Daily fidelity is the maximum temporal resolution available while covering each binary's full active window — hourly fidelity (`fidelity=60`) returns only the last ~30 days.

| Binary | Price-history coverage | n price points |
|--------|-------------------------|---------------:|
| will-israel-annex-syrian-territory-before-july | 2025-01-16 → 2025-07-01 | 167 |
| us-iran-nuclear-deal-before-2027 | 2025-11-06 → 2026-04-19 | 144 |
| zelenskyy-out-as-ukraine-president-before-2027 | 2025-07-25 → 2026-04-19 | 252 |
| ukraine-joins-nato-before-2027 | 2025-11-06 → 2026-04-19 | 149 |
| will-xi-jinping-win-the-nobel-peace-prize-in-2026 | 2025-10-17 → 2026-04-19 | 167 |
| china-x-taiwan-military-clash-before-2027 | 2025-11-14 → 2026-04-19 | 133 |
| will-donald-trump-win-the-nobel-peace-prize-in-2026-382 | 2025-10-17 → 2026-04-19 | 168 |
| will-trump-resign-by-december-31-2026 | 2025-07-26 → 2026-04-19 | 263 |
| will-trump-pardon-ghislaine-maxwell | 2025-07-24 → 2026-04-19 | 253 |
| will-trump-be-impeached-by-december-31-2026 | 2025-07-26 → 2026-04-19 | 249 |

Note: 7 of 10 binaries do not cover the first half of the signal window (2025-01-23 to mid-2025). This is a structural data limitation, not a design flaw — markets literally did not exist during the earlier period, so no price can be pulled. Day 6 n per (model × binary) reflects only the intersection.

## Per-binary × per-model aligned event counts

| Binary | A1 | A3 | B1 | C1 | C3 | Total |
|--------|---:|---:|---:|---:|---:|------:|
| will-israel-annex-syrian-territory-before-july | 12 | 7 | 7 | 79 | 3 | 108 |
| us-iran-nuclear-deal-before-2027 | 4 | 1 | 3 | 48 | 4 | 60 |
| zelenskyy-out-as-ukraine-president-before-2027 | 7 | 4 | 9 | 85 | 5 | 110 |
| ukraine-joins-nato-before-2027 | 4 | 1 | 3 | 48 | 4 | 60 |
| will-xi-jinping-win-the-nobel-peace-prize-in-2026 | 5 | 1 | 4 | 56 | 4 | 70 |
| china-x-taiwan-military-clash-before-2027 | 3 | 1 | 3 | 47 | 3 | 57 |
| will-donald-trump-win-the-nobel-peace-prize-in-2026-382 | 5 | 1 | 4 | 56 | 4 | 70 |
| will-trump-resign-by-december-31-2026 | 7 | 4 | 9 | 85 | 5 | 110 |
| will-trump-pardon-ghislaine-maxwell | 7 | 4 | 9 | 86 | 5 | 111 |
| will-trump-be-impeached-by-december-31-2026 | 7 | 4 | 9 | 85 | 5 | 110 |
| **Per-model total** | **61** | **28** | **60** | **675** | **42** | **866** |

Per-model aggregated n (sufficient for interpretation under the n≥15 threshold): all 5 in-scope models clear the threshold at aggregate level. Per (model × binary) cells vary: some A3/C3/B1 cells have n ≤ 4 and will be flagged underpowered in Day 6.

## Horizon coverage

Per Day 2 amendment horizons matched to each model's `hold_days`:

| Model | hold_days | Canonical horizon | Measurable at daily fidelity? |
|-------|----------:|-------------------|-------------------------------|
| A3_relief_rocket | 0 | +6h (intraday proxy) | **NO** — daily fidelity cannot measure intraday |
| A1_tariff_bearish | 1 | +24h | yes |
| C1_burst_silence | 1 | +24h | yes |
| C3_night_alert | 1 | +24h | yes |
| B1_triple_signal | 3 | +72h | yes |

**A3 canonical horizon not measurable.** A3 records are retained in the dataset with `canonical_ret = null` and a `plus1_ret` column for cross-model common-horizon comparison. Day 6 will report A3 only at the +1d cross-check horizon with an explicit note that this does not match A3's own prediction horizon (+0d / intraday). This is consistent with the Day 3 AM finding that A3 is unauditable under structural lag constraints.

## Matched non-signal baseline sampling

N=10 non-signal days sampled per signal event, drawn randomly (seeded `rng(f"{slug}:{date_signal}:42")`) from the same binary's active-window days that are **not** signal-fire days in the full `predictions_log.json` (including out-of-scope models, to avoid sampling baselines on any type of signal day). Same horizons computed (canonical + plus1d).

Total baseline rows: 10 × 866 = 8,660. No events returned <10 baselines (each binary has enough non-signal days within its active window).

## Direction-mapping decision (Day 6 methodology preview)

The pre-registration locked rules and binaries but did not specify how to translate each model's S&P direction (LONG/SHORT) into a YES-price direction prediction for each binary. Day 6 will report hit rates under **both** direction conventions per binary, and use the Bonferroni-corrected threshold against the doubled test count. Any cell that survives must survive in at least one direction convention cleanly, and that convention must align with the binary's observed signed correlation with S&P during non-signal days.

Rationale for two-convention reporting:
- A single "use S&P correlation sign" mapping derived from data introduces a mild look-ahead concern (the correlation is calibrated on the same data used for the hit test).
- Reporting both conventions makes the direction choice explicit and lets the reviewer see the unselected alternative — protecting against "pick the better direction post-hoc" bias when combined with Bonferroni correction.

Concrete: for each (model × binary × horizon) cell, Day 6 reports:
- `hit_rate_pos`: fraction of events where YES price rose in a signal-direction-positive scenario (LONG S&P → YES↑; SHORT S&P → YES↓)
- `hit_rate_neg`: the opposite convention
- `baseline_hit_rate_pos`, `baseline_hit_rate_neg`: corresponding non-signal baseline rates
- The pre-committed survival criteria apply to either direction; Bonferroni divisor doubles to account.

## What this does and does not produce

Produces: aligned dataset ready for Day 6 statistical measurement.
Does not produce: any hit rates, any edge estimates, any verdict. Those come from Day 6+.

## Artifacts

- Script: `day5/align.py`
- Inputs: `data/trump_code_refs/{predictions_log,market_SP500}.json`, `data/binary_price_history.json`, `data/phase0_selected_binaries.json`
- Output: `data/aligned.json` (866 event records + 8,660 baseline entries, gitignored)
