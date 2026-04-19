# Day 7 — Validity Checks

Status: **no cell passes all pre-registered gates.** Bonferroni-corrected significance (α = 0.05 / 100 = 0.0005) eliminates all nominal-looking cells. Reverse-direction and temporal-stability checks reinforce the null.

## Bonferroni correction

100 cells tested (5 models × 10 binaries × 2 direction conventions × 1 horizon each). Corrected significance threshold:

```
α_corrected = 0.05 / 100 = 0.0005
```

Cells with `p_bonferroni < 0.05`:
- **A3_relief_rocket × will-trump-resign-by-december-31-2026 (pos):** hit 50%, margin +47.5pp, net +5.62% — but **n=4**, far below the n≥15 threshold.

That is the only cell where the corrected p is sub-0.05, and it fails the n-gate. Every other cell with nominally-attractive hit rates has n ≤ 4 and saturates to p_bonferroni = 1.000 under the normal-approximation test (underpowered to produce a significant signal).

## All gates pass

Pre-registered survival requires simultaneously:
1. n ≥ 15
2. Hit rate ≥ 55%
3. Margin over baseline ≥ +5 pp
4. Net edge at fee_bps = 7.2 ≥ +2%
5. Bonferroni-corrected p < 0.05
6. Reverse-direction asymmetry ≥ 5 pp
7. Temporal stability: |first-half hit − second-half hit| < 10 pp

**No cell passes all seven gates.** The binding constraints in order of stringency:
- n ≥ 15 eliminates all A1, A3, B1, C3 per-cell tests (only C1 × binary cells clear)
- Hit rate ≥ 55% eliminates all C1 cells (C1 hit rates 11–42% absolute)
- So no cell clears the first two gates simultaneously.

## Cells clearing 3 of 7 gates (informational — all underpowered)

| Model | Binary | Conv | n | Hit % | Margin (pp) | Net @ 7.2 (%) | Gates cleared |
|-------|--------|-----:|--:|------:|------------:|--------------:|---------------|
| A3 | china-x-taiwan-military-clash-before-2027 | pos | 1 | 100.0 | +90.0 | +10.70 | hit, margin, net |
| A3 | ukraine-joins-nato-before-2027 | pos | 1 | 100.0 | +80.0 | +31.19 | hit, margin, net |
| A3 | us-iran-nuclear-deal-before-2027 | neg | 1 | 100.0 | +60.0 | +6.32 | hit, margin, net |
| A3 | will-trump-resign-by-december-31-2026 | pos | 4 | 50.0 | +47.5 | +5.62 | margin, net, p_bonf |
| A3 | will-xi-jinping-win-nobel | neg | 1 | 100.0 | +70.0 | +8.00 | hit, margin, net |
| B1 | china-x-taiwan-military-clash-before-2027 | neg | 3 | 66.7 | +6.7 | +3.08 | hit, margin, net |
| B1 | us-iran-nuclear-deal-before-2027 | neg | 3 | 66.7 | +20.0 | +9.24 | hit, margin, net |
| B1 | will-trump-nobel | neg | 4 | 75.0 | +30.0 | +7.16 | hit, margin, net |
| B1 | will-trump-be-impeached | neg | 9 | 66.7 | +18.9 | +8.55 | hit, margin, net |
| B1 | zelenskyy-out | neg | 9 | 77.8 | +23.3 | +4.25 | hit, margin, net |
| C3 | ukraine-joins-nato-before-2027 | pos | 4 | 75.0 | +37.5 | +7.99 | hit, margin, net |
| C3 | will-israel-annex-syrian | pos | 3 | 100.0 | +73.3 | +8.57 | hit, margin, net |

**All of these cells have n ≤ 9, well below the n ≥ 15 minimum.** The 100% hit rates at n=1 are the most obvious — a single observation cannot establish a hit rate. The cells with n=9 (B1 × will-trump-be-impeached, B1 × zelenskyy-out) are closest to meaningful but still 6 observations short of the n-gate. Their 66-78% hit rates could easily reverse with 6 more observations.

No high-n cell (n ≥ 15) clears the hit-rate threshold. The n-gate and hit-gate are mutually unsatisfiable in the current dataset for any in-scope rule.

## Reverse-direction asymmetry

Pre-registered: rule predicted-direction hit rate should be materially different from the reversed-direction hit rate. If both directions have similar hit rates, the measurement is broken or the signal has no directional content.

Aggregated per model (positive convention vs negative convention hit rate):

| Model | pos hit % | neg hit % | Asymmetry (pp) |
|-------|----------:|----------:|---------------:|
| A1 | 34.4 | 32.8 | +1.6 |
| A3 | 39.3 | 39.3 | 0.0 |
| B1 | 33.3 | 38.3 | −5.0 |
| C1 | 24.6 | 25.8 | −1.2 |
| C3 | 35.7 | 35.7 | 0.0 |

**Asymmetries are small (|Δ| ≤ 5 pp aggregate), and A3 and C3 show zero asymmetry.** This is consistent with "the signal has no direction-specific informational content about Polymarket binary direction, beyond the S&P correlation structure of each binary." When one binary favours pos and another favours neg (as observed in Day 6), the aggregate asymmetry cancels.

## Temporal stability

Pre-registered: absolute hit-rate delta between first-half (≤ 2025-08-19) and second-half (> 2025-08-19) of signal window should be < 10 pp. Rules with delta ≥ 10 pp are regime-dependent and will not generalise.

| Model | n cells with valid split | Mean |Δ| (pp) | Stable cells |
|-------|-------------------------:|---------------:|--------------|
| A1 | 0 | — | 0/0 (no binaries span split date) |
| A3 | 4 | 25.0 | 2/4 |
| B1 | 4 | 12.5 | 1/4 |
| C1 | 4 | 15.9 | 1/4 |
| C3 | 4 | 62.5 | **0/4** |

Most cells are temporally unstable (|Δ| ≥ 10 pp). Many first-half cells have n=0 or n=1 because most binaries didn't exist pre-mid-2025 — the "instability" partly reflects the structural lack of first-half data. But this is itself a signal-quality issue: rules that can only be evaluated in the second half have not demonstrated regime-stability.

A1 has zero valid splits because none of its 61 signal events in binaries exist pre-SPLIT_DATE on binaries that also existed post-SPLIT_DATE. This is another marker that the test is heavily biased toward the second half of the signal window.

## Fee sensitivity — does anything work at fee_bps=0?

Strict test: at fee_bps = 0, cells with hit ≥ 55% AND margin ≥ 5 pp AND n ≥ 15:

None. Fee rate is not the binding constraint. Even at zero fees, no n ≥ 15 cell clears the 55% hit-rate threshold.

## Counter-memo implications (Day 8)

Day 7 findings the counter-memo must address:

1. **n-gate and hit-gate are mutually unsatisfiable.** C1 has n ≥ 15 but hit rates of 11–42%. Other in-scope models have n ≤ 9 per binary. The pre-registered design could not in principle produce a passer given these data characteristics.

2. **The 55% hit threshold does not map to PM binaries.** S&P daily direction coin flip is ~50%. PM binary "up-on-day" rate is ~25% (reflecting zero-move-day share). The 55% threshold on PM binaries corresponds to a +25–30 pp move over baseline, a much higher bar than the equivalent S&P threshold.

3. **Reverse-direction zero-asymmetry for A3 and C3** suggests those signals carry no directional information about PM binaries. This is stronger evidence against these models than the hit-rate gate alone.

4. **Temporal instability across most cells** indicates regime-dependent behaviour — but is confounded by the first-half data scarcity problem. Cannot cleanly distinguish "signal changed" from "measurement is noisy due to sparse first-half data."

## Verdict direction

Strict pre-registered reading: **KILL.** No cell clears all 7 gates; no cell clears even 2 of the 7 binding gates (n-gate and hit-gate) simultaneously at any sample size.

Secondary reading (hit-margin + net edge, ignoring absolute hit-rate threshold): some positive signal on C1 cells, concentrated in specific direction conventions, but all fail Bonferroni correction due to the 100-test multiplicity and cell-level sample sizes.

## Artifacts

- Script: `day7/validity_checks.py`
- Input: `results/day6_core_measurement.json`, `data/aligned.json`
- Output: `results/day7_validity.json` (gitignored)
