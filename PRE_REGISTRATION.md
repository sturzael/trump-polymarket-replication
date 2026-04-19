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

Populated Day 4. Entries below are frozen before any price-series access (Day 5). See also "Amendment 2026-04-19 — Binary selection (§2): selection methodology and TVL-proxy caveat" below.

| # | Slug | conditionId | Category | Signal events¹ | TVL proxy² ($) | Overlap days |
|---|------|-------------|----------|---------------:|---------------:|-------------:|
| 1 | `will-israel-annex-syrian-territory-before-july` | `0x04cba107396183f9f85bbbe6bb2e2b03f3e41aefd77cd957f1aaeb3d64f9f3e7`³ | iran_israel | 235 | 103,757 | 414 |
| 2 | `us-iran-nuclear-deal-before-2027` | `0x182390641d3b...`³ | iran_israel | 60 | 216,035 | 127 |
| 3 | `zelenskyy-out-as-ukraine-president-before-2027` | `0x51f624dbbf14...`³ | russia_ukraine | 110 | 936,822 | 231 |
| 4 | `ukraine-joins-nato-before-2027` | `0x48c2b06383f2...`³ | russia_ukraine | 60 | 339,859 | 127 |
| 5 | `will-xi-jinping-win-the-nobel-peace-prize-in-2026` | `0x7f347ed73325...`³ | china | 70 | 372,388 | 147 |
| 6 | `china-x-taiwan-military-clash-before-2027` | `0x4c80df6f557b...`³ | china | 57 | 478,863 | 119 |
| 7 | `will-donald-trump-win-the-nobel-peace-prize-in-2026-382` | `0x962e5b226a77...`³ | nobel_trump | 70 | 1,043,568 | 147 |
| 8 | `will-trump-resign-by-december-31-2026` | `0x448f73e89890...`³ | trump_action | 110 | 189,792 | 230 |
| 9 | `will-trump-pardon-ghislaine-maxwell` | `0x0dc45815251a...`³ | trump_action | 111 | 238,333 | 232 |
| 10 | `will-trump-be-impeached-by-december-31-2026` | `0x4c8ceef9b9c0...`³ | trump_action | 110 | 304,495 | 230 |

¹ Number of in-scope verified predictions (models A1/A3/B1/C1/C3) whose `date_signal` falls within the market's [startDate, endDate] active window.
² TVL proxy = `lifetime_volume × signal_window_overlap_share`. See caveat in amendment below.
³ Full conditionIds are stored in `data/phase0_selected_binaries.json`. Shortened here for readability only; full values are the authoritative reference for Day 5 price pulls.

**Category distribution:**
- iran_israel: 2
- russia_ukraine: 2
- china: 2
- nobel_trump: 1
- trump_action: 3

Total: 10 binaries, all within $100k–$1.05M TVL proxy band.

### Day 4 selection log

Candidate pipeline:
- 2,251 Polymarket markets with political slug + signal-window overlap initially identified
- 287 after Tier-1 signal-responsive keyword filter and $50k minimum lifetime volume
- 117 after requiring ≥60 days overlap with signal window and resolution in Feb-2025 to Dec-2026 range
- 60 after restricting TVL proxy to $100k–$3M and requiring ≥50 in-scope signal events
- **10 selected** via diversification across 5 categories, staying within $100k–$1.05M TVL proxy band

Markets considered but rejected:
- All `will-trump-nominate-X-as-fed-chair` variants: same neg-risk basket (move together); including multiple would not add independent observations
- `putin-out-before-2027`, `will-the-supreme-court-rule-in-favor-of-trumps-tariffs`: TVL proxy above $1M band ceiling
- 2028 presidential-candidate long-tail markets: excluded at Tier-1 as resolution horizon too distant to respond to short-term posts
- Fed-rate-cut-count markets (`will-11-fed-rate-cuts-happen-in-2026` etc.): considered but dropped in favour of Ukraine NATO for category diversification (Fed category was already well-covered by proxy-based logic; dropping it does not leave a signal-type uncovered since Trump-Fed posts most strongly move the chair-nomination basket, which was excluded for being above the TVL ceiling).

### Amendment 2026-04-19 — Binary selection (§2): selection methodology and TVL-proxy caveat

**What was not possible in-budget.** The pre-registered criterion calls for TVL measured "at the time of each overlapping signal fire." Accurate signal-window TVL requires aggregating Polymarket trade records during 2025-01-23 to 2026-03-13 per market. Polymarket's `data-api/trades` endpoint does not support server-side timestamp filtering (all tested parameter variants returned the latest trades regardless) and client-side pagination is capped at `offset=5000`. For markets with >5,000 lifetime trades (which includes several of our selections), we cannot reach signal-window trades via pagination. Downloading SII (954M rows, 107 GB) is also out-of-budget.

**Substitute used.** TVL proxy = `lifetime_volume × (signal_window_overlap_days / total_active_days)`. This assumes uniform volume distribution across a market's active window, which is false in general (political markets cluster volume near resolution events and news catalysts). The proxy therefore has potentially-asymmetric error: it can over-estimate signal-window TVL for markets with post-signal-window catalyst-driven volume spikes, or under-estimate for markets that peaked during signal window.

**Mitigation.** The $100k–$1M band is the *proxy* band. Actual signal-window TVL per market could fall outside this band in either direction. Two consequences for the verdict:
- If a market's true signal-window TVL was materially below $100k, observed price responses may reflect low-depth slippage artifacts rather than market consensus, and Day 6 measurements on that market should be flagged as potentially unreliable.
- If a market's true signal-window TVL was materially above $1M, that is not a validity threat — deeper liquidity reduces noise. No correction needed.
- The Day 6 core measurement remains valid as a pre-registered test of the rule set against this binary universe, regardless of proxy inaccuracy.

**Binary list frozen.** Despite the proxy limitation, the binary list is committed as of this amendment timestamp and will not be revised after Day 5 price data is accessed. Markets cannot be swapped mid-experiment for better-looking ones; that would recreate selection bias. The list stands.

**No other changes to the pre-registration.** Rules, horizons (per Day 2 amendment), thresholds, reporting commitment, and non-goals are unchanged.

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

Each amendment is a dated subsection appended below, referencing the section it modifies. Original values above are not edited.

### Amendment 2026-04-19 — Observation horizons (§3): per-model to match verified-prediction hold_days

**What changes.** The originally pre-registered horizon set `{+1h, +3h, +6h}` is replaced with **per-model horizons matching each in-scope model's `hold_days`** as observed in `predictions_log.json`. No horizon is added or removed post-hoc to favour any rule.

**Revised horizons (in-scope models only):**

| Model | hold_days | PM horizon tested |
|-------|----------:|-------------------|
| A3_relief_rocket | 0 | +6h (intraday proxy; PM binaries rarely settle open→close) |
| A1_tariff_bearish | 1 | +24h |
| C1_burst_silence | 1 | +24h |
| C3_night_alert | 1 | +24h |
| B1_triple_signal | 3 | +72h |

**Rationale.** The original horizons `{+1h, +3h, +6h}` come from the trump-code README architecture diagram's real-time-engine tracking line. Day 2 replication revealed that the verified predictions underlying the headline 61.3% hit rate are evaluated at `hold_days` horizons (0–3 trading days), not at the real-time tracking horizons. Testing a 3-day-hold rule at a 1-hour Polymarket horizon would measure PM response at the wrong timescale and produce an uninformative null, biasing the experiment against the hypothesis for reasons unrelated to whether the signal exists. Matching each model to its own verification horizon is the correct test.

**Multiple-testing accounting.** Original design: 5 in-scope models × 10 binaries × 3 horizons = 150 cells. Revised design: 5 in-scope models × 10 binaries × 1 horizon-per-model = 50 cells. The Bonferroni divisor becomes 50, not 150. This reduction is earned by matching each model to its own horizon, not cherry-picked post-hoc.

**Thresholds unchanged.** Hit rate ≥55%, net fee-adjusted edge ≥2% at fee_bps=7.2, baseline margin ≥5pp, n≥15, Bonferroni-corrected p<0.05/n_tests, reverse-direction asymmetry, temporal stability <10pp. The 2% net-edge threshold applies at each model's horizon; longer horizons permit larger PM moves and thus longer-horizon models have a mechanically easier path to 2%, which is acknowledged here but not adjusted (the threshold is against *net* edge after fees, which already dominates the decision at practical Polymarket fee levels).

**No other changes to the pre-registration.** Rules in scope, binary-selection criteria, reporting commitment, non-goals, and survival thresholds remain as originally committed.
