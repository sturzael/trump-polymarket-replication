# Day 3 AM — Lag-Before-Trade Audit

**Gate status: NOT TRIGGERED.** Aggregate lag contamination 25.9% across in-scope hold_days≥1 models vs pre-committed kill threshold of 30%. Phase 0 proceeds to Day 3 PM (fee verification) and Day 4 (binary selection).

## Methodology

The pre-registered plan assumed minute-level S&P data to compare S&P level at a realistic trade-decision point (post_ts + 10 min) against the verification horizon. We have only daily OHLC from their `market_SP500.json`. We therefore ran a coarser but conservative test.

For each verified prediction, classify the signal day by post-time bucket (pre-open / intraday / after-close). For models with `hold_days ≥ 1`, compute the hit rate under two entry conventions:

- `their_entry` = open(d_entry) — what their published measurement uses
- `realistic_entry` = close(d_entry) — the latest-possible realistic entry for a live operator who saw the signal-firing post after market close of the signal day

A *flipped* prediction is one that is correct under `their_entry` but incorrect under `realistic_entry`. The flip rate is the share of their correct predictions whose edge was captured pre-close-of-signal-day — i.e. reporting, not prediction.

`realistic_entry` = close(d_entry) is the **worst-case** late-trader assumption. An actual trader acting on an afternoon post could enter at some intraday point earlier than close, so real lag contamination is somewhere between the open-entry and close-entry hit rates. The flip rate is therefore an upper bound on reporting contamination for each model.

For hold_days=0 (A3), the test is degenerate: `realistic_entry = close(d_entry) = exit_point`, zero window. A3 cannot be audited without intraday minute data and is flagged separately.

Bucket assignment uses Eastern Time with market hours 09:30–16:00 ET. Post times come from their `trump_posts_lite.json` (44,070 posts, 1,420 dates indexed).

## Results

Post-time distribution per in-scope model (verified predictions):

| Model | hold_days | PRE_OPEN | INTRADAY | AFTER_CLOSE | PRE_AND_AFTER_CLOSE |
|-------|----------:|---------:|---------:|------------:|--------------------:|
| A1_tariff_bearish | 1 | 0 | 20 | 2 | 1 |
| A3_relief_rocket | 0 | 0 | 11 | 0 | 0 |
| B1_triple_signal | 3 | 0 | 17 | 0 | 0 |
| C1_burst_silence | 1 | 0 | 160 | 0 | 16 |
| C3_night_alert | 1 | 1 | 7 | 0 | 0 |

**Every in-scope model fires overwhelmingly on days with intraday Trump posts.** This is the structural condition that makes the lag audit meaningful: entry=open(d) is set before the posts that determine the signal.

### Hit rate comparison (their_entry vs realistic_entry)

| Model | hold | Bucket | n | Their hit | Realistic hit | Δ (pp) | Flipped / correct |
|-------|-----:|--------|--:|----------:|--------------:|-------:|------------------:|
| A1_tariff_bearish | 1 | INTRADAY | 20 | 60.0% | 45.0% | −15.0 | 4/12 = 33% |
| A1_tariff_bearish | 1 | AFTER_CLOSE | 2 | 50.0% | 0.0% | −50.0 | 1/1 = 100% |
| A1_tariff_bearish | 1 | PRE_AND_AFTER_CLOSE | 1 | 0.0% | 0.0% | 0 | — |
| A3_relief_rocket | **0** | INTRADAY | 11 | 72.7% | degenerate | — | **unauditable without intraday data** |
| B1_triple_signal | 3 | INTRADAY | 17 | 64.7% | 70.6% | **+5.9** | 1/11 = 9% |
| C1_burst_silence | 1 | INTRADAY | 160 | 65.0% | 53.1% | −11.9 | 29/104 = 28% |
| C1_burst_silence | 1 | PRE_AND_AFTER_CLOSE | 16 | 75.0% | 62.5% | −12.5 | 2/12 = 17% |
| C3_night_alert | 1 | PRE_OPEN | 1 | 0.0% | 0.0% | 0 | — |
| C3_night_alert | 1 | INTRADAY | 7 | 42.9% | 42.9% | 0 | 0/3 = 0% |

### Aggregate kill metric

Excluding A3's degenerate test: **37 flipped / 143 correct = 25.9%**.

Pre-committed kill threshold: 30%. Gate: **NOT TRIGGERED**. Experiment proceeds.

## Per-model lag-contamination findings

These feed into the Day 8 counter-memo and the Day 9 verdict:

- **B1_triple_signal — LAG-ROBUST.** 9% flip rate; actually improves under realistic entry (+5.9pp). 3-day hold dilutes entry timing. Strongest in-scope candidate for Polymarket translation on lag-audit grounds. Sample size (n=17) remains a constraint.

- **C1_burst_silence — BORDERLINE.** 27% flip rate; net hit rate at close-entry ≈ 53%. C1 carries the largest share of the headline 61.3% claim (176/564 predictions). A 12pp drop in realistic hit rate materially compresses the post-fee tradeable edge. Worth testing on Polymarket, but with the expectation that any observed edge will be smaller than their published figure.

- **A1_tariff_bearish — LAG-CONTAMINATED.** 38% flip rate on INTRADAY bucket; 100% flip on AFTER_CLOSE (n=2, low confidence). Above the per-model-level 30% threshold that the aggregate kill criterion is defined against. Marked as reporting-contaminated; any Polymarket edge measured should be heavily discounted.

- **A3_relief_rocket — UNAUDITABLE + STRUCTURALLY VULNERABLE.** hold_days=0 (same-day open→close) combined with 100% intraday posts means entry=open predates every signal-firing post. Daily OHLC cannot decompose the open→close move into pre-post vs post-post portions. Structurally this is a reporting-heavy design: the model "predicts" a move that has already partially or fully occurred by the time any post could fire the signal. Sample size (n=11) is already below the n≥15 threshold. Will be flagged UNAUDITABLE / UNDERPOWERED in the Day 9 verdict regardless of Polymarket results.

- **C3_night_alert — UNAUDITABLE (n too small).** n=8 already below the n≥15 threshold; INTRADAY bucket has n=7 with 3 correct, insufficient for a 30% flip test to be meaningful. Marked UNDERPOWERED in the verdict.

## Limitations

1. **Daily OHLC only.** Without intraday minute-level S&P data, we cannot precisely locate trade-decision points within a trading day. The close(d) realistic-entry assumption is a worst-case proxy.
2. **Time-zone assumption.** All post times interpreted as Eastern Time. If the underlying Truth Social timestamps are UTC or another timezone, bucket assignments would shift. Inspection of post patterns (posts cluster around US daytime hours) is consistent with ET storage; not independently verified.
3. **Signal-firing post identification.** The audit treats all posts on `date_signal` as potentially signal-firing. Their actual signal-firing post could be a specific one. Using "any post on signal day" is the most conservative reading (earliest post triggers the entry timing concern).

## What this does NOT say

- It does not say Polymarket edge exists — that is the Day 5–7 measurement.
- It does not say C1/A1 rules are invalid — only that their published hit rates overstate the capturable edge by 10–15 percentage points.
- It does not validate B1's predictive character absolute — only that B1 is robust to the specific lag confound tested here.

## Artifacts

- Script: `day3/lag_audit.py`
- Inputs: `data/trump_code_refs/{predictions_log,market_SP500,trump_posts_lite}.json` (gitignored)
