# Out-of-Venue Translation of a Published Equity-Signal Claim

**A pre-registered replication study testing whether the sstklen/trump-code signal set — claimed 61.3% hit rate on S&P 500 direction from Truth Social posts across 564 verified predictions — produces tradeable edge on Polymarket mid-TVL political binaries.**

> 👉 **Not a markets person?** Read the [Explain Like I'm Five version](docs/ELI5.md) instead.

---

## Abstract

This repository documents a ten-day pre-registered replication study. The target claim is public: [sstklen/trump-code](https://github.com/sstklen/trump-code) reports a 61.3% hit rate across 564 verified predictions from 11 named models operating on Trump's Truth Social posts to predict S&P 500 direction at 1–3 day horizons. The experimental question is whether those signals translate to tradeable edge on Polymarket mid-TVL political binaries active during the same prediction window (2025-01-23 to 2026-03-13).

Five rules from the eight named discoveries were mapped to predictor models and tested against ten political binaries selected via pre-committed TVL and category-diversification criteria. The full set of seven pre-committed survival gates — n ≥ 15, hit rate ≥ 55%, baseline margin ≥ 5 pp, net edge ≥ 2% at fee_bps=7.2, Bonferroni-corrected p < 0.05 against 100 tests, reverse-direction asymmetry ≥ 5 pp, temporal stability < 10 pp — was not cleared by any of the 100 tested cells. The verdict is **KILL**; continuation to a Phase 1 dedicated test is not authorised on this rule set and binary universe.

The negative result is specific to this rule set, this binary universe, the +1d/+3d horizons tested, and the 14-month measurement window. It does not falsify the trump-code claim on S&P data; it does not rule out edge at longer PM-binary repricing horizons; it does not cover the one rule (`B1_triple_signal`) that was underpowered rather than falsified and remains a Phase 1 candidate if pursued independently.

---

## Core findings

### On schema replication

The overall verified hit rate computed locally from `predictions_log.json` reproduces to **61.35%**, matching the published 61.3% to two decimal places. Under the entry/exit convention discovered on Day 2 — entry at open of the first trading day on or after `date_signal`, exit at close of the `hold_days`-th trading day after entry — every in-scope model's verified hit rate and per-prediction return reproduced with 99.4–100% correct-flag agreement. The schema is readable. This is necessary but not sufficient for the rest of the study to be informative.

Day 1 identified that the 8 "key discoveries" advertised in the README key-discoveries table do not map to `surviving_rules.json` (600 composite-ID rules from a 31.5M-model brute-force search) but to `predictions_log.json` (11 named models producing the published 564 verified predictions). The replication therefore tests the 11-model system, not the 600-rule brute-force survivor list.

### On lag contamination of the original claim

The published hit rates are measured at entry=open of the first trading day on or after `date_signal`. For any signal whose firing post occurs during market hours on a trading day, the "entry" timestamp predates the post — meaning part of the measured open→exit move is pre-post reporting rather than post-post prediction.

Day 3 replaced entry=open with entry=close(signal_day) as a worst-case late-trader proxy and measured the share of "correct" predictions that flip under this substitution. Aggregate in-scope flip rate: **25.9%** — below the pre-committed 30% kill threshold but not by much. Per-model detail:

- `B1_triple_signal` — 9% flip rate (lag-robust; 3-day hold dilutes entry timing)
- `C1_burst_silence` — 27% flip rate (late-trader hit rate drops to ~53%)
- `A1_tariff_bearish` — 38% flip rate (above per-model 30% line)
- `A3_relief_rocket` — test degenerate (hold_days=0, same-day open→close with 100% intraday posts = structurally pre-post reporting)
- `C3_night_alert` — n=8, underpowered for the test

### On translation to Polymarket binaries

Across 5 in-scope models × 10 diversified political binaries × 2 direction conventions = 100 cells tested:

- **No cell clears the absolute 55% hit-rate threshold.** Hit rates on PM binaries cluster 11–42% because political markets have substantial zero-move-day share (pull baseline to ~25%, not ~50% as on S&P).
- **Only `C1_burst_silence` has per-cell n ≥ 15.** Other in-scope models aggregate to n≥15 but per-binary n is 1–9.
- **The two binding gates (n ≥ 15 AND hit ≥ 55%) are mutually unsatisfiable on this dataset.** C1 is the only n-powered rule; C1's absolute hit rate is below 55% on every binary.
- Per-model aggregate hit vs baseline under positive convention: A1 34.4/32.3, A3 39.3/25.0 (underpowered), B1 33.3/26.8, C1 24.6/26.1, C3 35.7/29.3. Only A3, B1, C3 aggregate show ≥ 5 pp margin, and all are per-cell underpowered.

### On direction-convention behaviour

Both direction conventions were reported (LONG S&P → binary YES up vs LONG S&P → YES down) with doubled Bonferroni divisor. Per-binary the "working" convention is determined by each binary's sign correlation with S&P during signal days. Aggregate reverse-direction asymmetry per model:

- A1: +1.6 pp, A3: 0.0, B1: −5.0, C1: −1.2, C3: 0.0

A3 and C3 showing **zero aggregate asymmetry** is independent evidence that those signals carry no direction-specific informational content about PM binary movement beyond each binary's native S&P correlation structure.

### On sample power

C1_burst_silence contributes 176/564 (31%) of the published verified predictions — by far the largest contributor to the 61.3% figure — and is the only rule whose Polymarket test is adequately powered. C1's per-cell n=47–86 on PM binaries produced a hit rate of 24.6% against baseline 26.1% in the positive convention. C1 is the rule where the null result is robust, not underpowered.

B1_triple_signal is the only in-scope model that is lag-robust (Day 3), directionally-informative (reverse asymmetry −5 pp at aggregate), and shows 66–78% nominal hit rates at per-cell n=4–9. All B1 per-cell tests fail n ≥ 15 by 6–11 observations. B1 is not falsified; it is underpowered. A Phase 1 dedicated test on B1 with fresh sample collection could change the result.

---

## Methodology

### Data sources

**Primary inputs (all from trump-code's public GitHub):**
- [`predictions_log.json`](https://github.com/sstklen/trump-code/blob/main/data/predictions_log.json) — 566 records, 564 verified (source of the 61.3% claim).
- [`market_SP500.json`](https://github.com/sstklen/trump-code/blob/main/data/market_SP500.json) — 313 daily OHLC rows, 2025-01-17 to 2026-04-17.
- [`trump_posts_lite.json`](https://github.com/sstklen/trump-code/blob/main/data/trump_posts_lite.json) — 44,070 posts with HH:MM Eastern-Time timestamps.
- [`surviving_rules.json`](https://github.com/sstklen/trump-code/blob/main/data/surviving_rules.json) — retained for Day 1 schema inspection; not the source of the published hit rate.

**Polymarket sources:**
- Gamma API (`gamma-api.polymarket.com/markets`) for market metadata, volumes, start/end dates.
- CLOB API (`clob.polymarket.com/markets/<cid>`) for conditionId → token_id mapping and exchange-configured fee rates.
- CLOB prices-history (`/prices-history?market=<token_id>&interval=max&fidelity=1440`) for daily YES-price series per binary.

**Sources considered but not used:**
- SII-WANGZJ on-chain archive: 954M rows, ~107 GB on HuggingFace. Out-of-budget to download for this Phase 0.
- Polymarket data-api `/trades`: pagination capped at offset=5000; no functional timestamp filter (documented caveat in Day 4).

### Pre-registration structure

Before any Polymarket price data was accessed, [`PRE_REGISTRATION.md`](PRE_REGISTRATION.md) committed:

1. The exact 5 in-scope rules and their `predictions_log.json` model_ids.
2. The exact selection criteria for Polymarket binaries — political, ≥60 days signal-window overlap, TVL in $100k–$1M band at signal-fire time, ≥50 in-scope signal events.
3. The 7 survival thresholds (n, hit rate, margin, net edge, corrected significance, reverse asymmetry, temporal stability).
4. The 5-point fee sensitivity sweep at {0, 3, 7.2, 15, 30} bps.
5. The commitment to report all cells including underpowered ones, with both uncorrected and Bonferroni-corrected p-values.
6. The default-to-KILL behaviour on mixed results.
7. The four non-goals (no live trading, no classifier rebuild, no rule expansion beyond the 8 named discoveries, no equity-side trading).

The binary list was frozen in a timestamped amendment after Day 4 and not revised after Day 5 price access.

### Ten-day schedule with kill gates

See [`PHASE_0_PLAN.md`](PHASE_0_PLAN.md).

1. **Day 1** — pre-registration completion (blocking).
2. **Day 2** — schema sanity replication on their own S&P data (blocking kill gate; replicate one named discovery or kill).
3. **Day 3 AM** — lag-before-trade audit (blocking kill gate at 30% aggregate flip rate).
4. **Day 3 PM** — political-market fee verification (confirms 0 bps empirically across categories).
5. **Day 4** — binary selection (blocking; list frozen via amendment before Day 5).
6. **Day 5** — price alignment + matched non-signal baseline sampling.
7. **Day 6** — core measurement + fee sensitivity sweep + minimum-n gate.
8. **Day 7** — Bonferroni correction + reverse-direction asymmetry + temporal stability split.
9. **Day 8** — counter-memo (adversarial review written before the verdict).
10. **Day 9** — `PHASE_0_VERDICT.md` single-page decision.

### Methodological rules carried over from the parent project

Carried from the event-impact-mvp findings-log:

1. **Sample size drives the decision window, not vice versa.** Pre-commit thresholds before seeing data. (Honoured: all 7 gates fixed before Day 5.)
2. **Measure raw before parameterising.** Hit rates reported pre-fee; fee-sensitivity sweep published regardless of result at any single fee level.
3. **Write the counter-memo from the same data.** Written on Day 8 before the Day 9 verdict.
4. **Distinguish "pattern exists historically" from "pattern is capturable now."** Day 3 lag audit addresses this directly.
5. **Default to KILL on mixed results.** Applied on Day 9 despite some margin-positive cells.

---

## Pre-registration integrity log

Two amendments were committed during Phase 0. Both are schema-driven corrections visible in the data before any affected price-alignment measurement, not hypothesis-favourable threshold movement:

**Amendment 2026-04-19 (§3 horizons):** `{+1h, +3h, +6h}` → per-model horizons matching each model's `hold_days` (0d/1d/3d). Original horizons came from the trump-code README architecture-diagram's real-time-engine tracking line; Day 2 replication revealed the verified predictions underlying the 61.3% claim are evaluated at `hold_days` horizons. Multiple-testing divisor reduced from 150 to 50 cells (100 after the pos/neg direction doubling). No threshold changes.

**Amendment 2026-04-19 (§2 binary selection):** TVL measurement via proxy (`lifetime_volume × signal_window_overlap_share`) rather than direct signal-window aggregation. Polymarket `data-api/trades` endpoint accepts but does not honour timestamp-filter parameters; client-side pagination is capped at offset=5000; SII download was out-of-budget. The binary list was frozen via this amendment before Day 5 price access and was not revised afterwards.

Neither amendment rescued a GO that strict reading would have killed, nor killed a GO that strict reading would have cleared. The strict pre-committed reading returns KILL under either amendment state.

---

## Polymarket findings observed (independent of the trading verdict)

These are observations collected during Phase 0 that are not documented in Polymarket's public documentation and are included for the value of the observation independently:

- **CLOB `/prices-history` fidelity × interval behaviour.** `interval=max&fidelity=1440` returns up to ~500 daily bars covering a market's full active life. `fidelity=60` (hourly) returns only the last ~30 days. Hourly history is not available for historical research; only daily.
- **`data-api/trades` timestamp filtering is broken.** All of `timestampMin`, `timestamp_min`, `startTs`, `start_ts`, `after`, `before` are accepted without error but ignored; responses return the latest trades regardless. Pagination is capped at `offset=5000`, limiting paginated access to the most-recent ~5000 trades per market regardless of lifetime trade count.
- **Exchange-configured base fees are uniformly 0 bps pre-V2.** Sampled across 16 markets in 6 categories (politics, elections, geopolitics, cabinet, sports, crypto): every market reports `maker_base_fee = 0, taker_base_fee = 0`. Published "ceiling" rates (3 bps sports, 7.2 bps crypto) are maximum configurable rates, not applied rates.
- **CTF Exchange + CLOB V2 cutover at 2026-04-22** is 3 days after this Phase 0's completion date. Phase 0 data is entirely pre-V2. Post-V2 fee structure may differ; the pre-committed sensitivity sweep at {0, 3, 7.2, 15, 30} bps covers the uncertainty.

---

## Trump-code findings observed (independent of the trading verdict)

- **The 8 README "key discoveries" map to `predictions_log.json` not `surviving_rules.json`.** The 600 surviving rules are brute-force search survivors; the 11 named models in the predictions log are the actual source of the 61.3% claim.
- **C1_burst_silence carries the headline claim.** 176/564 predictions (31%), 65.3% hit rate; no other model has a combination of large sample and high hit rate at this scale.
- **Per-model hold_days varies.** A3=0 (intraday), A1/B3/C1/C3=1 (next-day), B2/C2/D2=2, B1/D3=3. Testing at a single horizon would mis-specify most rules.
- **D2_sig_change direction=VOLATILE** predicts magnitude not direction and is not mappable to a directional PM binary — out of scope regardless of the 8-named filter.
- **Classifier dependence risk is real but unaddressable here.** Their classifier is used as-is. If their classifications were indirectly fit to S&P outcomes (hindsight), any Polymarket result on the same classifications would be non-transferable. This is why Day 2 sanity replication was a kill gate — we confirmed we can read their schema, but not that the schema is free of upstream fit.

---

## Conditions under which the verdict would flip

The KILL verdict is specific to this rule set, this binary universe, these horizons, and this 14-month measurement window. Conditions under which the conclusion would merit re-examination:

- **Fresh sample for B1_triple_signal specifically.** B1 is not falsified by Phase 0; it is underpowered. A dedicated Phase 1 test with n ≥ 15 per binary (requires ~2× the observation window at B1's current fire rate) could flip the result.
- **Longer horizons (+7d, +14d).** If PM political binaries reprice on 1–2 week timescales for slow-developing political events, the +1d/+3d horizons tested here miss the move. Not tested in Phase 0.
- **Single-direction mapping (binary-S&P-correlation sign).** Halves the Bonferroni divisor and single-tests each cell. Would not change the current verdict but tightens any future test.
- **Neg-risk arbitrage angle.** Explicitly out of scope here (different from direction prediction). Unexplored.
- **V2-cutover-era markets.** Post-2026-04-22 data not measured. Phase 1 would need to re-measure under V2 microstructure regardless.

None of these is venue expansion away from Polymarket. The signal-capture question is binding on latency, classifier quality, and horizon choice — all of which travel with the rule rather than the venue.

---

## Tooling included

All code is MIT-licensed and runnable against the public inputs listed above. Raw data is gitignored; collectors are included and data is regenerable.

- [`PRE_REGISTRATION.md`](PRE_REGISTRATION.md) — pre-registered rules, binaries, thresholds, non-goals, amendment log.
- [`PHASE_0_PLAN.md`](PHASE_0_PLAN.md) — 10-day schedule with blocking/non-blocking tagging and kill gates.
- [`RISKS.md`](RISKS.md) — five specific failure modes with committed mitigations.
- [`PHASE_0_VERDICT.md`](PHASE_0_VERDICT.md) — single-page decision.
- [`COUNTER_MEMO.md`](COUNTER_MEMO.md) — adversarial review written before the verdict.
- [`day1/`](day1/) – [`day9/`](day9/) — per-day scripts and reproducibility harnesses.
- [`docs/day*.md`](docs/) — per-day write-ups with methodology, numbers, limitations.

Python 3.12+. No third-party dependencies beyond the standard library (`urllib.request`, `json`, `datetime`, `collections`, `math`, `random`).

```bash
python3 day2/sanity_replication.py    # schema sanity check
python3 day3/lag_audit.py             # lag-before-trade flip-rate audit
python3 day3/fee_verification.py      # Polymarket category fee sampling
python3 day4/select_binaries.py       # binary selection pipeline
python3 day5/align.py                 # price alignment + baseline sampling
python3 day6/core_measurement.py      # hit rate, margin, fee-adjusted edge
python3 day7/validity_checks.py       # Bonferroni, reverse-direction, stability
```

---

## A note on LLM-assisted research

This project was conducted with Claude as a research collaborator across specification, implementation, review, and iteration. The same failure modes observed in the parent project apply here and were mitigated accordingly:

- **Estimate inflation.** The headline "61.3% hit rate" was treated as a hypothesis requiring structural validation (Day 2 schema, Day 3 lag), not as authoritative.
- **Stale-memory citations.** Fee rates, rate limits, and exchange parameters were re-verified on Day 3 rather than cited from memory.
- **Motivated reasoning toward pre-existing conclusions.** Counter-memo (Day 8) was pre-committed and written before the verdict to force adversarial examination of both directions (false KILL and false GO).

A specific observation from this project: when tests produce near-threshold results (Day 3 lag audit at 25.9% vs 30% kill line, Day 7 Bonferroni saturated at underpowered cells), the LLM's natural tendency is to emphasise one framing. The pre-registration discipline — binding the interpretation to a prior-committed threshold — is the primary defence against this drift.

---

## Citation

If referencing this work:

```
Sturzaker, E. (2026). Out-of-Venue Translation of a Published Equity-Signal Claim:
A Pre-Registered Replication of Trump-Code on Polymarket.
GitHub: sturzael/trump-polymarket-replication
```

Target of replication:

```
sstklen (2026). Trump-Code: AI-powered cryptanalysis of presidential communications
× stock market impact. https://github.com/sstklen/trump-code
```

## Disclosure

No capital was deployed. No trading was conducted. All findings are based on observation of public trump-code data, public Polymarket metadata and price history, and the pre-registered measurement pipeline described above. The replication uses trump-code's published classifications as-is; the authors make no claim about the signal's validity on S&P 500 data beyond confirming that the published hit rate reproduces from the published inputs under the schema discovered on Day 2. No affiliation with Truth Social, Polymarket, sstklen, or any financial regulatory authority.
