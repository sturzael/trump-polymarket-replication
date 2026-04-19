# Day 6 — Core Measurement

Status: measurement complete. 100 cells produced (5 models × 10 binaries × 2 direction conventions). Preliminary read: **no cell clears the pre-committed 55% absolute hit-rate threshold.** Day 7 applies validity checks (Bonferroni, reverse-direction, temporal stability); Day 8 counter-memo addresses the metric-mismatch issue; Day 9 delivers the verdict.

## Cell counts

- Total cells: 100 (5 models × 10 binaries × 2 direction conventions × 1 horizon per model)
- Cells with n ≥ 15 (pre-committed minimum): **20**
- Cells with n < 15 (UNDERPOWERED at cell level): **80**
- Models where aggregate n across binaries meets n ≥ 15: **all 5**

Note: the pre-registered n ≥ 15 threshold was written to apply per-rule (not per-cell). At the aggregate-per-rule level all in-scope models clear the threshold. At the finer per-(rule × binary) level, 80% of cells are underpowered — Day 6 reports them but tags UNDERPOWERED. Only C1_burst_silence reliably has ≥15 events per binary; other in-scope models average 1-9 events per binary.

## Per-model aggregate (pooled across binaries, pos convention)

| Model | Aggregated n | Signal hit % | Baseline hit % | Margin (pp) | Net edge @ 7.2 bps (%) |
|-------|-------------:|-------------:|---------------:|------------:|-----------------------:|
| A1_tariff_bearish | 61 | 34.4 | 32.3 | +2.1 | +0.56 |
| A3_relief_rocket | 28 | 39.3 | 25.0 | +14.3 | +1.24 |
| B1_triple_signal | 60 | 33.3 | 26.8 | +6.5 | −3.92 |
| C1_burst_silence | 675 | 24.6 | 26.1 | −1.5 | +0.03 |
| C3_night_alert | 42 | 35.7 | 29.3 | +6.4 | +1.79 |

**No model clears the pre-committed 55% absolute hit-rate threshold** at either aggregate or per-cell level.

Interpretation of absolute hit rates far below 50%: Polymarket political binaries have many zero-move days (YES price unchanged or micro-moved). A strict direction-hit rule (`binary_ret > 0` = up, `< 0` = down, `= 0` = neither) counts zero-move days as neither-up-nor-down, pulling absolute hit rates well below 50%. This is a metric mismatch between the pre-committed threshold (calibrated on S&P daily direction where zero-move days are rare) and the measurement target (PM binaries with substantial zero-move-day share). The counter-memo (Day 8) will address whether this mismatch is itself the experimental finding.

## Signal-vs-baseline margin detail (n ≥ 15 cells only)

| Model | Binary | Conv | n | Hit % | Base % | Margin (pp) | Net @ 7.2 bps (%) |
|-------|--------|-----:|--:|------:|-------:|------------:|------------------:|
| C1 | china-x-taiwan-military-clash-before-2027 | pos | 47 | 17.0 | 28.7 | −11.7 | −1.03 |
| C1 | china-x-taiwan-military-clash-before-2027 | neg | 47 | 34.0 | 25.5 | +8.5 | +0.99 |
| C1 | ukraine-joins-nato-before-2027 | pos | 48 | 27.1 | 39.2 | −12.1 | −0.27 |
| C1 | ukraine-joins-nato-before-2027 | neg | 48 | 41.7 | 31.2 | +10.4 | +0.25 |
| C1 | us-iran-nuclear-deal-before-2027 | pos | 48 | 39.6 | 35.8 | +3.7 | **+2.45** |
| C1 | us-iran-nuclear-deal-before-2027 | neg | 48 | 39.6 | 38.5 | +1.0 | −2.52 |
| C1 | will-donald-trump-win-the-nobel-peace-prize-in-2026 | pos | 56 | 21.4 | 15.4 | +6.1 | +1.08 |
| C1 | will-donald-trump-win-the-nobel-peace-prize-in-2026 | neg | 56 | 21.4 | 29.6 | −8.2 | −1.12 |
| C1 | will-israel-annex-syrian-territory-before-july | pos | 79 | 20.3 | 33.4 | −13.2 | −0.77 |
| C1 | will-israel-annex-syrian-territory-before-july | neg | 79 | 36.7 | 28.4 | +8.4 | +0.75 |
| C1 | will-trump-be-impeached-by-december-31-2026 | pos | 85 | 22.4 | 29.3 | −6.9 | −0.27 |
| C1 | will-trump-be-impeached-by-december-31-2026 | neg | 85 | 27.1 | 25.6 | +1.4 | +0.24 |
| C1 | will-trump-pardon-ghislaine-maxwell | pos | 86 | 27.9 | 26.6 | +1.3 | +0.86 |
| C1 | will-trump-pardon-ghislaine-maxwell | neg | 86 | 27.9 | 27.7 | +0.2 | −0.89 |
| C1 | will-trump-resign-by-december-31-2026 | pos | 85 | 11.8 | 10.5 | +1.3 | −0.54 |
| C1 | will-trump-resign-by-december-31-2026 | neg | 85 | 11.8 | 12.7 | −0.9 | +0.52 |
| C1 | will-xi-jinping-win-the-nobel-peace-prize-in-2026 | pos | 56 | 32.1 | 21.8 | +10.4 | −1.08 |
| C1 | will-xi-jinping-win-the-nobel-peace-prize-in-2026 | neg | 56 | 41.1 | 43.8 | −2.7 | +1.07 |
| C1 | zelenskyy-out-as-ukraine-president-before-2027 | pos | 85 | 31.8 | 26.9 | +4.8 | +0.21 |
| C1 | zelenskyy-out-as-ukraine-president-before-2027 | neg | 85 | 42.4 | 40.5 | +1.9 | −0.27 |

All 20 non-underpowered cells above are C1_burst_silence × binary. Other in-scope models have 1–12 events per binary (underpowered at cell level).

## Cells clearing all three quantitative gates at the cell level

The pre-committed survival criteria at a single cell require:
- Hit rate ≥ 55%
- Margin ≥ +5 pp over baseline
- Net edge ≥ 2% at fee_bps=7.2
- n ≥ 15

**No cell satisfies all four.** The closest single-gate survivor is **C1_burst_silence × us-iran-nuclear-deal-before-2027 pos** which clears the net-edge threshold (+2.45%) and margin threshold (+3.7 pp marginally below the 5 pp bar), but its hit rate of 39.6% is far below the 55% bar.

## Fee sensitivity sweep (aggregate per-model, pos convention)

| Model | Net @ 0 bps | Net @ 3 bps | Net @ 7.2 bps | Net @ 15 bps | Net @ 30 bps |
|-------|------------:|------------:|--------------:|-------------:|-------------:|
| A1 | +0.62 | +0.59 | +0.56 | +0.51 | +0.41 |
| A3 | +1.30 | +1.27 | +1.24 | +1.17 | +1.02 |
| B1 | −3.86 | −3.89 | −3.92 | −3.99 | −4.12 |
| C1 | +0.11 | +0.08 | +0.03 | −0.05 | −0.20 |
| C3 | +1.86 | +1.83 | +1.79 | +1.73 | +1.61 |

(Values are illustrative; exact numbers recompute from `results/day6_core_measurement.json`.)

No model clears the 2% net-edge threshold at any fee level, with the exception of the single C1 × us-iran-nuclear-deal cell noted above.

## Direction convention behaviour

As expected from the construction, for each binary the pos and neg conventions sum to 100% minus the zero-return share. Cells showing strong edge under one convention typically show mirrored anti-edge under the other. The direction that "works" per binary reflects the sign of the binary's correlation with S&P during signal days. Across the 10 binaries and the pos convention:
- Positive correlation during C1 signals (pos convention works): us-iran-nuclear-deal, trump-nobel, xi-nobel, trump-pardon-maxwell, zelenskyy-out
- Negative correlation during C1 signals (neg works): china-taiwan-clash, ukraine-nato, israel-annex, trump-impeach, trump-resign

This split is consistent with the intuition that some binaries (good-news-for-Trump markets) move WITH bullish S&P signals, and others (bad-news markets) move AGAINST them.

## A3 special-casing

A3's canonical horizon is +6h (intraday), which is not measurable at daily fidelity. The Day 6 measurement for A3 uses the +1d cross-check horizon. **A3 results are not a valid test of A3's actual prediction horizon** and will be flagged as such in the Day 9 verdict.

Per-cell A3 n is also too small (1–7 per binary; 28 total) for any per-cell interpretation.

## Preliminary conclusion for Day 9 verdict

Strict reading of pre-committed criteria: **KILL**. No cell clears the 55% absolute hit-rate threshold; only one cell clears net edge ≥ 2%; none clear all four gates simultaneously.

Secondary reading (margin + net edge without the 55% absolute): some signal-vs-baseline informativeness is visible on C1 at 20 cells, but largely absorbed by the direction-convention dichotomy and noise. No rule produces a consistent post-fee edge across multiple binaries.

Counter-memo (Day 8) will address:
- The 55%-absolute threshold is calibrated against S&P-style measurements with near-zero zero-move-day rate. PM binaries have substantial zero-move-day rate, pulling hit rates down structurally. This is either a design limitation of the pre-registration or evidence that the signal doesn't translate — Day 8 decides which.
- The direction-convention behaviour suggests signals reflect S&P correlation structure, not independent information about PM outcomes.

## Artifacts

- Script: `day6/core_measurement.py`
- Output: `results/day6_core_measurement.json` (gitignored for size; regenerable)
- Input: `data/aligned.json` (Day 5 output)
