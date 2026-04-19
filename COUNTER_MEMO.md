# Counter-Memo — Phase 0

**Date:** 2026-04-19 (Day 8 of Phase 0)
**Purpose:** Written before the Day 9 verdict. Pre-committed in the plan as a required adversarial step. Argues, from the same data produced in Days 1-7, why the emerging verdict direction might be wrong or incomplete — whether toward a false KILL or a false GO.

---

## 1. The case that the verdict is a false KILL (signal exists, measurement mis-specified)

### 1a. The 55% hit-rate threshold is mis-calibrated for PM binaries

The threshold was selected by analogy to S&P daily-direction testing, where a coin-flip baseline is ~50% and 55% represents a modest edge. On Polymarket political binaries, daily P(price moves up) is ~25% (reflecting substantial zero-move-day share and negative drift on many probability-depletion binaries). A genuine +5 percentage-point edge over a 25% baseline would register as 30% absolute hit rate — not 55%. The 55% absolute threshold on PM binaries corresponds to a +25–30 pp edge over baseline, which is an enormous effect and would be surprising to find even if the signal exists.

**What the Day 6 data shows under margin-only reading:**
- 5 of 20 high-n C1 cells show ≥ 5 pp margin over baseline in one direction convention
- Two C1 cells show ≥ 10 pp margin: xi-jinping-nobel (+10.4), ukraine-joins-nato (+10.4)

**Is this a false KILL?** Probably no. Three reasons:

1. **The 10 pp margins disappear under Bonferroni correction.** With 100 cells and α=0.0005, none of the margin-positive cells achieve corrected significance — they are consistent with noise given the multiple-testing burden.
2. **Direction conventions cancel.** For every cell showing +margin under pos, the same binary typically shows −margin under neg (not always, but most). This means the "signal" is symmetric with the binary's drift rather than direction-specific, reinforcing the reverse-direction-asymmetry finding.
3. **The baseline-hit-rate itself varies widely across binaries** (10–45%), indicating the baseline is not a stable reference. A +5 pp margin over a 20% baseline means different things than +5 pp over a 40% baseline.

### 1b. The pre-registered horizon may have been wrong for PM binary measurement

We amended horizons on Day 2 from `{+1h, +3h, +6h}` to per-model `hold_days`. But `hold_days` was derived for S&P measurements. On PM binaries, the "right" horizon could be entirely different — perhaps the binary needs longer to reprice because political markets have few bot market-makers and reprice at human speed.

**What we should have done if rewriting the experiment:** test multiple horizons (+1d, +3d, +7d) and pick the best, with Bonferroni correction for the horizon search.

**Does this salvage a GO?** Unlikely. If the signal were real at any horizon, we would expect at least one cell to cross the gates even at the "wrong" horizon, especially for C1 which has 85+ events per binary. The failure at +1d for C1 is broad and consistent.

### 1c. Baseline sampling may have been contaminated

We excluded ALL signal-fire days from the baseline pool (not just in-scope-model signal days). The 11-model system has 564 verified-prediction days; excluding those plus ~6000 non-in-scope model signal days leaves the baseline pool as "days the model didn't fire for any reason." This may not be the right counterfactual — the "days the model didn't fire" set could be systematically different (e.g., Sundays, holidays) from "days the model fired."

**What would the corrected baseline show?** Baseline hit rate on matched day-type would likely be similar to our current 25–35% range, because the "different" days (weekends, holidays) have low or zero binary trading volume and zero price change, so they would actually have even LOWER hit rates, making the signal-minus-baseline margin look BETTER. This is a bias in the KILL direction, not the GO direction.

### 1d. The direction-mapping is doubled-tested

We report both pos and neg conventions, Bonferroni-correct against the doubled test count. A single pre-committed direction (say, "binary correlation with S&P determines sign") would halve the Bonferroni divisor and halve the corrected significance threshold. If a cell clears corrected significance under one specific direction, it might clear with the halved divisor.

**What if the pre-committed mapping had been "signed by binary-S&P correlation"?** Let me check specifically:
- The C1 × ukraine-joins-nato neg cell shows +10.4 pp margin at p_bonf = 1.0 (saturated).
- Uncorrected p for that cell was approximately 0.29 (normal approximation on n=48). Even with 50-test Bonferroni (instead of 100), p_corrected ≈ 14.5, saturated. Still fails.

The single-direction Bonferroni would not change the verdict.

---

## 2. The case that the verdict is a false GO

### 2a. Underpowered cells showing 100% hit rates might be real

Several A3 and C3 cells show 100% hit rate at n=1. Statistically these are uninterpretable. But consider: A3 fires only 11 times in 14 months of S&P measurement, and with 100% hit rate on the single PM-overlapping signal on specific binaries (like china-taiwan-clash), there is a directional signal claim worth checking with more data.

**Is this likely a real signal?** No. Multiple reasons:
- At n=1, 100% hit rate is the binomial expectation 50% of the time under chance.
- A3 is flagged from Day 3 as structurally lag-vulnerable (same-day open→close with intraday posts = pre-post reporting).
- A3 horizon is unmeasurable at daily fidelity; the +1d cross-check horizon is not A3's actual prediction horizon.

No escalation of A3 conclusions warranted. Mark UNAUDITABLE in verdict.

### 2b. B1 at n=9 showing 66–78% hit rate across multiple binaries

B1 × will-trump-be-impeached (neg, n=9, 66.7%), B1 × zelenskyy-out (neg, n=9, 77.8%), B1 × trump-nobel (neg, n=4, 75%), and others show nominally high hit rates. B1 is also the model that *passed* the Day 3 lag audit (9% flip rate, 3-day hold dilutes entry timing).

**Is this real?** Possibly but underpowered. All B1 cells fail n≥15. An n=9 showing 77.8% has a binomial 95% CI of approximately [40%, 97%] — consistent with no effect. The reverse-direction test for B1 aggregate is -5.0pp, which is above zero but marginal. If B1 is genuine, the per-cell n is too small to demonstrate it in Phase 0.

**Recommendation:** B1 merits attention in any Phase 1 scoping, conditional on a fresh sample. It is the only in-scope model that combines lag-robust (Day 3) with directionally-plausible reverse asymmetry. But Phase 0 strict verdict still KILL because the pre-committed gate requires n≥15.

---

## 3. Specific pre-registered failure modes to address

### 3a. Selection bias in binaries

**Did the binary universe end up dominated by high-movement markets?** Our selection targeted $100k–$1M TVL proxy. The actual high-movement markets are likely in the high-TVL end. We excluded the highest-TVL markets (Fed chair basket variants > $2M proxy). This biases toward LOWER-movement markets, which makes the null more likely to hold — conservative, not hypothesis-favourable.

**Did the selection inadvertently select for markets that drift in a specific direction?** Most Trump-action markets (resign, pardon, impeach) have strong downward drift because "nothing happens" is the modal outcome. This means baseline hit rates (P(YES up)) are low ~10–30%. This is accounted for by the baseline comparison per cell.

### 3b. Signal-category × market-category correlation

**Did tariff rules only fire when tariff markets were most active?** No evidence. C1_burst_silence fires 176 times across the verification window, distributed evenly. Binary activity isn't clustered on C1-signal days specifically (we checked).

### 3c. Horizon mismatch (their rules vs PM binary repricing)

**Their rules predict S&P at 1d–3d. PM binaries might reprice on different timescales.** This is plausible and fits the finding that PM binaries have high zero-move-day rate. If PM political binaries reprice on 1-week+ timescales for slow-developing political events, testing at +1d/+3d horizons captures only the immediate reaction, missing the cumulative move. However:
- We tested the horizons the rules themselves use
- Testing longer horizons would introduce a pre-registration deviation (post-hoc horizon search)
- Even if the signal is real at +7d, the 2% net-edge threshold would likely be met at longer horizons, not shorter, which doesn't save the current verdict

### 3d. Lookback confound (signal source vs market prices in same dataset)

**Could the trump-code rule-survival process have indirectly fit to PM-adjacent price patterns?** Possible but unlikely:
- Their brute-force search was on S&P 500, not PM data
- The 11 models they publish are interpretable rules (tariff-on-market-day→short, etc.) not black-box fits
- PM data isn't in their pipeline until the 2026 real-time engine, post-survivor-ranking

Low concern.

### 3e. V2 cutover structural break

**Data from 2026-04-22 onward reflects V2 mechanics.** We are 3 days before V2 cutover as of 2026-04-19. All Day 5 price history is pre-V2, so no structural break inside the test window. Phase 1 consideration only.

---

## 4. What I expect would happen with double the data

If we had 28 months of signal-prediction history instead of 14, and 20 PM binaries instead of 10, the most likely outcome:

1. C1 aggregate hit rate remains ~25% (close to baseline). The null would firm up.
2. A3, C3 aggregate remain uninterpretable due to low signal-event rate (2–3× more events but still underpowered)
3. B1 would reach n ≈ 100 and cross the n-gate. At B1's nominal 65–78% hit rates (if sustained), this would plausibly clear the corrected significance test. This is the one result that could be different with more data.
4. Bonferroni divisor scales with more binaries, which works against GO.

**Expected probability of any rule cleanly passing all gates at 2× data: ~15%, with B1 × specific-binary being the most likely survivor.** At current data, 0%.

---

## 5. Honest assessment of what Phase 0 establishes and does not establish

**Phase 0 establishes:**
- Their schema is readable (Day 2 replication).
- Aggregate lag contamination is 25.9% — signal is not pure reporting, but not pure prediction either.
- Political market fees are empirically 0 bps pre-V2.
- On 10 mid-TVL political binaries across 5 categories, no in-scope rule produces a hit rate + margin + net-edge combination that clears the pre-committed gates with sample size ≥ 15.

**Phase 0 does NOT establish:**
- That the S&P signal is or isn't real (we don't re-verify their S&P claim end-to-end).
- That B1 has or doesn't have edge on PM (underpowered).
- That PM edge would emerge at longer horizons (not tested).
- That the direction-mapping is optimal (we tested two conventions, the binary-S&P-correlation single-mapping would not change the verdict).

---

## 6. Specific reasons the Day 9 verdict should be KILL despite margin-positive cells

1. Pre-committed threshold is the authoritative test, and 0 cells pass.
2. Every "clean" n ≥ 15 cell (C1 × binary) has absolute hit rate well below 55%.
3. Every "high hit rate" cell has n ≤ 9, uninterpretable at the pre-registered gate.
4. Reverse-direction asymmetry zero for A3 and C3 is independent evidence of no directional content.
5. Temporal stability generally fails, confounded by first-half data scarcity but not cleanly rescuable.
6. Direction-convention dichotomy + pos/neg cancellation across binaries suggests the "signal" we see on some cells is S&P-correlation structure, not independent PM information.
7. B1 is the one rule that might emerge with more data, but Phase 0's scope does not include "collect more data."

## 7. Specific reasons not to over-conclude from KILL

1. KILL here is on this specific venue (PM political binaries), this specific window, these specific 10 binaries, and these specific 5 in-scope rules. It does NOT falsify the trump-code S&P claim on its own data.
2. B1_triple_signal is under-tested on PM and could genuinely work at Phase 1 scale. A GO on B1 only, conditional on collecting n ≥ 15 per binary, would be a reasonable Phase 1 scoping output.
3. Longer horizons (+7d, +14d) were not tested. If PM political binaries reprice slowly for slow-developing events, the right horizon may be beyond the 3-day maximum tested here.
4. The neg-risk arbitrage angle (different from direction prediction) remains unexplored and was explicitly out of scope here.

---

## 8. Conclusion

The counter-memo does not produce evidence that reverses the emerging KILL verdict. It identifies specific residual uncertainty (B1 under-tested; horizon choice constrained) that should inform Phase 1 scoping if a Phase 1 is pursued. It also confirms that the most plausible failure modes (mis-calibrated threshold, direction-convention cancellation, baseline instability) would strengthen rather than weaken the KILL reading when properly accounted for.

**Day 9 verdict direction affirmed: KILL, with specific per-rule notes for Phase 1 consideration.**
