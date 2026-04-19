# Phase 0 Plan — Trump-Code × Polymarket Replication

**Budget:** 10 working days. Observation-only. No capital deployed.
**Goal:** Produce a defensible GO/KILL decision on whether the sstklen/trump-code signal set has tradeable edge on Polymarket mid-TVL political binaries.
**Non-goal:** Prove or disprove the original claim on S&P 500. Their equity-side finding is taken as-given for evaluation purposes only.

---

## Non-goals (locked)

To prevent scope creep during the 10-day window:

1. **No live trading at any phase.** Paper only through Phase 2.
2. **No rebuilding their signal classifier.** Their classifications are used as-is. If classifications are wrong, that is itself a finding.
3. **No expansion beyond the 8 named rules** until after the Phase 0 kill/survive decision.
4. **No equity-side trading or modeling.** Phase 0 evaluates only Polymarket translation.
5. **No looking at PM price data before Day 4.** All pre-registration, schema-sanity, lag-audit, and fee-verification work must complete before PM price series are pulled.

---

## Blocking vs. non-blocking items

Every item below is tagged **[BLOCKING]** (the experiment cannot produce a defensible verdict without it) or **[NON-BLOCKING]** (validity-strengthening; skip only if a blocking item overruns the buffer).

| # | Item | Status | Day |
|---|------|--------|-----|
| 1 | Pre-registration file committed before any data pull | **BLOCKING** | 1 |
| 2 | Sanity replication of one named discovery on their own S&P data | **BLOCKING** | 2 |
| 3 | Phase 0a — lag-before-trade verification | **BLOCKING** | 3 |
| 4 | Political-markets fee verification (SII taker-fee fields) | **BLOCKING** | 3 (parallel) |
| 5 | Binary market selection (TVL at time-of-signal, not now) | **BLOCKING** | 4 |
| 6 | Signal alignment + matched non-signal baseline sampling | **BLOCKING** | 5 |
| 7 | Signal vs baseline hit-rate measurement | **BLOCKING** | 6 |
| 8 | Fee-adjusted edge at fee_bps ∈ {0, 3, 7.2, 15, 30} | **BLOCKING** | 6 |
| 9 | Minimum-n interpretation gate (n<15 per rule = underpowered) | **BLOCKING** | 6 |
| 10 | Bonferroni correction (reported alongside uncorrected) | **BLOCKING** | 7 |
| 11 | Reverse-direction test | NON-BLOCKING | 7 |
| 12 | Temporal stability split (first-half vs second-half) | NON-BLOCKING | 7 |
| 13 | Counter-memo written before verdict | **BLOCKING** | 8 |
| 14 | PHASE_0_VERDICT.md single-page decision gate | **BLOCKING** | 9 |

---

## Day-by-day schedule

### Day 1 — Pre-registration [BLOCKING]

- Fill in `PRE_REGISTRATION.md`:
  - Paste the 8 named rules verbatim from trump-code README key-discoveries table.
  - Map each discovery to its corresponding model_id in `predictions_log.json` (the source of the verified 61.3% hit rate). Note: the plan originally referenced `surviving_rules.json` — Day 1 schema inspection found the 8 discoveries map to the 11-model `predictions_log.json` system, not the 600-rule brute-force survivor list. Rationale documented in PRE_REGISTRATION.md §1 schema note.
  - Record per-model verified-n and verified hit rate from their data.
  - Flag discoveries #3 (China weighting) and #4 (TS-before-X lag) as out-of-scope (no standalone predictor).
  - Flag models with n<15 verified predictions pre-filter as likely UNDERPOWERED.
  - Record fixed thresholds: hit rate ≥55%, net fee-adjusted edge ≥2%.
  - Record fixed horizons: +1h, +3h, +6h.
  - Record commitment to report all in-scope rules × all binaries, not only positive results.
  - Record non-goals block (above).
- Git-commit the completed file. Commit timestamp becomes the pre-registration timestamp.
- **Blocking gate:** no SII queries, no Polymarket API calls, no price data access before this commit lands. (Exception: Day 1 read-only fetch of their public `predictions_log.json` and `surviving_rules.json` from GitHub is permitted for schema inspection; these are their publicly-published reference files, not Polymarket price data.)

### Day 2 — Sanity replication on their S&P data [BLOCKING — item 14]

- Pick **one** named discovery ("Pre-market RELIEF = strongest buy signal" — their clearest published claim).
- Reproduce its expected return at +1h on their own published S&P historical data using their `surviving_rules.json` schema and `predictions_log.json` records.
- **Kill gate:** if the reproduced +1h expected return on S&P is inconsistent with their published figure by more than a small noise band, we have misread their schema or their data has changed. KILL — do not proceed to Polymarket testing. Document schema issue in `docs/schema_mismatch.md`.
- No Polymarket access today.

### Day 3 — Phase 0a: lag-before-trade + fee verification [BLOCKING — items 2, 3]

**Morning: lag audit (item 2).** For every one of their 566 verified predictions:

- Extract Truth Social post timestamp from their corpus.
- Compute rule-fire timestamp (post timestamp + 5 min detection+classification lag).
- Compute trade-decision timestamp (fire + 5 min for order placement) = post + 10 min.
- Compare S&P level at trade-decision timestamp vs at their +1h / +3h / +6h verification points.
- Compute: fraction of their 61.3% hit rate attributable to moves that had already fully occurred by the trade-decision point.

**Kill gate:** if >30% of their hit rate comes from post-decision-point moves (i.e., the rule is reporting, not predicting), KILL the whole experiment here. Document in `docs/lag_audit_result.md`. No point replicating a non-predictive signal on a second venue.

**Afternoon (parallel): fee verification (item 3).** Pull 3–5 resolved Polymarket political markets from 2025-2026 (not sports) from SII; inspect on-chain taker-fee fields. If non-zero taker fees are observed on political markets, adjust the pre-registered ≥2% net-edge threshold upward accordingly. Record adjustment in `PRE_REGISTRATION.md` amendment (timestamped, not overwritten).

### Day 4 — Binary market selection [BLOCKING — items 5, 13]

- Using a date filter on SII that pre-dates any price-series access: identify all active Polymarket political binaries whose active window overlapped with their 566 signal-fire timestamps.
- **Volume-adjusted selection:** for each candidate binary, compute TVL *at the time of each overlapping signal fire* (not current snapshot). Retain only binaries in the $100k–$1M band during the signal-fire window.
- Target: 5–10 binaries. If more than 10 qualify, take the top 10 by median TVL during signal-fire window.
- Append the final binary list (slug + condition_id) to `PRE_REGISTRATION.md` via amendment commit. Binary list is now frozen.
- **Blocking gate:** no price-series pulls before this file is committed.

### Day 5 — Price alignment + baseline sampling [BLOCKING — item 6]

- Pull CLOB price series for the frozen binary set from SII across all matched signal-fire windows and +6h post-fire tails.
- For each (signal-fire event, binary) pair, record binary price at t, t+1h, t+3h, t+6h.
- **Matched baseline sampling (item 4):** for each signal-fire event, sample N=10 non-signal timestamps from the same binary's history (same time-of-day distribution, same day-of-week distribution where possible), record binary price at each non-signal t, t+1h, t+3h, t+6h.
- Persist aligned dataset to `data/aligned.parquet`. No interpretation yet.

### Day 6 — Core measurement [BLOCKING — items 7, 8, 9]

For each (rule × binary × horizon) cell:

- Compute signal-fire hit rate (direction of PM binary move matches rule's predicted direction).
- Compute matched-baseline hit rate from the N=10 non-signal samples per event.
- Compute realized edge in basis points.
- Compute fee-adjusted edge at fee_bps ∈ **{0, 3, 7.2, 15, 30}**. Strategies that only work at fee_bps=0 are not robust.
- **Minimum-n gate (item 7):** any rule with <15 signal-fire observations across all binaries is marked "UNDERPOWERED" and excluded from interpretation. Report the count but do not compute a conclusion from it.

Persist result table to `results/core_measurement.csv`.

### Day 7 — Validity checks + significance [BLOCKING — item 10; NON-BLOCKING — items 11, 12]

- **Bonferroni correction [BLOCKING]:** 8 rules × 10 binaries × 3 horizons = 240 tests (or n_rules × n_binaries × n_horizons actually present after Day 6 exclusions). Corrected threshold = 0.05 / n_tests. Report uncorrected AND corrected p-values for every cell.
- **Reverse-direction test [NON-BLOCKING but strongly advised]:** for each rule, compute hit rate on predicted direction AND on reversed direction. A rule at 60%/40% is signal; a rule at 60%/60% means the measurement is broken.
- **Temporal stability [NON-BLOCKING]:** split the observation window into first-half and second-half. Rules with hit-rate differential >10 percentage points between halves are flagged as regime-dependent and will not be extrapolated.

Persist to `results/validity_checks.csv`. If schedule slips, items 11–12 may be deferred to Day 10 buffer.

### Day 8 — Counter-memo [BLOCKING — item 13]

Before writing any verdict, write an adversarial memo (`COUNTER_MEMO.md`) addressing:

- **Selection bias in binaries.** Did our binary universe end up dominated by high-movement markets?
- **Signal-category correlation.** Do tariff rules only fire when tariff markets are most active? Could that explain any apparent edge?
- **Horizon mismatch.** Their rules predict S&P at 1h/3h/6h; PM binaries may reprice on different timescales, especially around resolution events.
- **Lookback confound.** SII contains both the Truth Social mirrored data (if present) and market prices. Could the trump-code rule-survival process have indirectly fit to PM-adjacent price patterns?
- **V2 cutover structural break.** Data from 2026-04-22 onward reflects V2 mechanics. Any rule performance change pre/post may not reflect signal decay.

Required sections. Must be written before the verdict so the verdict author cannot rationalize around it.

### Day 9 — Phase 0 Verdict [BLOCKING — item 10]

Produce `PHASE_0_VERDICT.md`, ≤2 pages, with the following sections in order:

1. **GO or KILL** — explicit at top of file.
2. Number of rules tested; number of rules excluded for n<15.
3. Observations per rule (table).
4. Hit rate (signal) vs hit rate (baseline) per rule × horizon (table).
5. Uncorrected p-values AND Bonferroni-corrected p-values per rule × horizon.
6. Fee-adjusted edge at fee_bps ∈ {0, 3, 7.2, 15, 30} per rule (table).
7. Go/no-go decision against pre-committed thresholds.
8. Counter-memo summary (one paragraph, link to full `COUNTER_MEMO.md`).

**Decision rule:** default to KILL on mixed results. Only GO if at least one specific rule cleanly survives: hit rate ≥55%, net fee-adjusted edge ≥2% at fee_bps=7.2, Bonferroni-corrected p<0.05/n_tests, baseline-margin ≥5 percentage points, n≥15, reverse-direction test shows asymmetry, temporal stability <10pp differential.

### Day 10 — Buffer

- Slack capacity for overrun on any earlier day.
- If not consumed: run non-blocking items 11–12 if deferred from Day 7.
- If verdict is GO: write a one-page Phase 1 scaffold memo. Do not start building.
- If verdict is KILL: write the null result up for the findings log and close the branch.

---

## Commit discipline

- `PRE_REGISTRATION.md` is append-only. Amendments are new commits with timestamp, not edits to existing sections.
- Each day's outputs go into their own commit with the day number in the message.
- No force-pushes on this branch. The git history is part of the integrity claim.
- Any data artifact referenced in a result table must be reproducible from committed code and a documented SII query. If it is not reproducible, it does not appear in the verdict.

---

## What Phase 0 does NOT produce

- A trading strategy.
- A paper-trade harness configured against live markets.
- A capital-deployment recommendation.
- A Phase 1 design. (Phase 1 scoping is a post-verdict exercise if and only if the verdict is GO.)
