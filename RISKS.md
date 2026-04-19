# Phase 0 Design Risks

The five specific failure modes this experimental design is vulnerable to, and the mitigation committed to for each. Each risk is phrased as the failure mode, not the symptom. If Phase 0 produces a positive verdict, these are the questions a reviewer should press on first.

---

## Risk 1 — The signal is reporting, not predicting

**Failure mode.** The trump-code 61.3% hit rate is measured on S&P outcomes at +1h / +3h / +6h after *the post*, not after a realistic trade-decision point. If the S&P has already moved by the time a live operator could have detected the post, classified the signal, and placed an order, the reported hit rate captures price moves that were never capturable. Replicating a non-predictive signal on a second venue is wasted effort regardless of how well the replication is executed.

**Mitigation.** Day 3 Phase 0a lag audit. For every one of their 566 verified predictions, compare the S&P level at post_timestamp + 10 min (realistic trade-decision point) against the S&P level at their verification horizon. If >30% of their reported hit rate is attributable to moves that had already fully occurred by the trade-decision point, KILL the experiment. This check costs one day and saves the remaining nine if the answer is unfavourable.

---

## Risk 2 — Multiple-testing false positives at smaller scale

**Failure mode.** Trump-code's original publication tested 31.5M model combinations and retained 551 that survived train/test split. The selection process itself introduces survivorship bias. By testing 8 of those surviving rules against 10 Polymarket binaries at 3 horizons (240 cells), uncorrected p<0.05 produces an expected ~12 false positives by chance alone. Without correction, a single "winning" cell looks compelling when it is noise.

**Mitigation.** Three layers:
1. **Pre-registration** of the 8 rules, 10 binaries, and 3 horizons before any Polymarket price data is accessed. The test universe is frozen in a git commit whose timestamp predates the first SII query on aligned data.
2. **Bonferroni correction** reported alongside every uncorrected p-value. Corrected threshold = 0.05 / n_tests.
3. **Decision-rule default is KILL on mixed results.** A GO requires a specific sub-rule that survives corrected significance, not just any cell below 0.05.

---

## Risk 3 — Directional drift confound (no control = no inference)

**Failure mode.** Political prediction markets often drift in one direction regardless of any specific catalyst — Trump-themed binaries tend to trend upward on favorable news cycles, downward on unfavorable ones, and these cycles correlate with Trump's posting frequency. A 58% hit rate on signal-fired events is uninterpretable without knowing the base rate on non-signal events from the same market over the same period. If baseline drift hits 55% in the same direction, the signal contributes effectively nothing.

**Mitigation.** Matched non-signal baseline sampling. For each signal-fire event, draw N=10 non-signal timestamps from the same binary's history, sampled to match time-of-day and day-of-week distributions. Report signal hit rate AND baseline hit rate side-by-side for every rule. The go-criterion requires a ≥5 percentage-point margin of signal over baseline, not just a 55% absolute signal hit rate.

---

## Risk 4 — Classifier schema dependence

**Failure mode.** This experiment uses trump-code's signal classifications as-is rather than rebuilding the classifier. If their classifier was overfit to S&P outcomes during the original 31.5M-model brute-force search — for instance, if "tariff signal" was implicitly defined partly by posts that *happened to* precede S&P moves — then any apparent edge we find on Polymarket would come from information that cannot be recovered in forward-only signal classification. Worse, we might simply be misreading their schema and attributing signals to the wrong posts.

**Mitigation.** Day 2 sanity replication gate. Before any Polymarket work, reproduce one of their published named discoveries ("Pre-market RELIEF = strongest buy signal") on their own S&P data using their published rule files and prediction log. If we cannot reproduce the published figure within a small noise band, KILL — the schema is either wrong or misread, and no Polymarket result would be interpretable. This forces the experiment to demonstrate it can correctly read the rule files before claiming anything about a second venue.

---

## Risk 5 — Survivorship bias in binary selection

**Failure mode.** If binary market selection is done by taking a current snapshot and filtering to "mid-TVL political binaries that overlapped with signal fires," the resulting universe is biased toward markets that attracted enough attention to stay liquid long enough to appear in a current listing. Markets that had low TVL at signal-fire time and subsequently faded are excluded; markets that had low TVL at signal-fire time and subsequently grew are included. The selected universe is not a representative sample of what was tradeable at signal-fire time.

**Mitigation.** Day 4 volume-adjusted selection. TVL is measured *at the time of each overlapping signal fire*, not from a current snapshot. Only binaries in the $100k–$1M band during the signal-fire window are retained. The full inclusion/exclusion log is committed so the verdict reviewer can see which markets were dropped and why. The binary list is frozen in a pre-registration amendment before any price-series access.

---

## Residual risks not fully mitigated

Documented for the verdict reviewer even though no clean mitigation fits the 10-day budget.

- **V2 cutover structural break.** The 2026-04-22 CTF Exchange / CLOB V2 cutover may have changed fee mechanics and microstructure in ways that make pre-cutover backtests non-representative of post-cutover trading. Phase 0 is retrospective and cannot address this; Phase 1 design would need to treat pre- and post-cutover data separately.
- **Corpus completeness.** Trump-code's Truth Social corpus may have gaps (deleted posts, rate-limited windows). If gaps correlate with signal types, the 566-prediction set is itself biased. Not checkable without an independent Truth Social archive, which is not available in Phase 0 scope.
- **Partial-fill exposure.** Even if Phase 0 finds edge, the multi-leg nature of some political-binary positions means non-atomic order submission could eat the edge in live execution. This is a Phase 2 concern, flagged here only so the Phase 0 verdict is not mistaken for a Phase 2 green light.
