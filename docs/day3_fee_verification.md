# Day 3 PM — Political-Markets Fee Verification

**Conclusion: no threshold adjustment needed.** Sampled markets across 6 category buckets (trump_policy, elections, geopolitics, cabinet, sports_control, crypto_control) uniformly show `maker_base_fee: 0` and `taker_base_fee: 0` on Polymarket's CLOB. The pre-committed 2% net-edge threshold at fee_bps=7.2 remains conservative and is unchanged.

## Methodology

The pre-registered plan was to pull 3–5 resolved political markets from SII and inspect on-chain taker-fee fields. SII (954M rows, 107GB) is not available locally in this budget. Substitute: query Polymarket's CLOB `/markets/<condition_id>` endpoint, which exposes `maker_base_fee` and `taker_base_fee` directly per market. These are the protocol-configured CLOB rates applied at fill.

Cross-category sampling extends the audit beyond the original political-only scope to confirm whether the 0-bps finding in the memory (143-trade sports sample through 2026-03-31) generalises.

## Sample

19 unique markets queried across 6 categories. Results:

| Category | markets sampled | unique taker_base_fee | unique maker_base_fee |
|----------|----------------:|----------------------:|----------------------:|
| trump_policy | 3 | {0} | {0} |
| elections | 3 | {0} | {0} |
| geopolitics | 3 | {0} | {0} |
| cabinet | 1 | {0} | {0} |
| sports_control | 3 | {0} | {0} |
| crypto_control | 3 | {0} | {0} |

All 16 sampled markets report `maker_base_fee = 0, taker_base_fee = 0`.

## Interpretation

Polymarket's published fee documentation lists "ceiling" rates of 3 bps sports and 7.2 bps crypto. The CLOB `base_fee` fields are the actually-applied per-order rates. These being uniformly zero is consistent with the event-impact-mvp memory's empirical finding that sports trades settle with zero fees, and extends the finding to the political and other tested categories.

The published ceilings may represent maximum rates configurable per market rather than currently-applied rates. Pre-V2 CTF Exchange state (we are observing 3 days before the 2026-04-22 V2 cutover per the project memory) shows 0-bps operation across categories.

## Implications for Phase 0

- **No amendment to `PRE_REGISTRATION.md` §4 required.** The 2% net-edge threshold at fee_bps=7.2 remains the canonical decision point. At the empirical 0-bps rate, the threshold is stricter than necessary, which is a conservative bias in the KILL direction.
- **Pre-committed fee sensitivity sweep at {0, 3, 7.2, 15, 30} bps remains unchanged.** Day 6 core measurement reports every rule at all 5 rates. This sweep already covers the scenario where V2 cutover (2026-04-22) introduces non-zero fees, as well as the scenario where slippage adds effective fee cost beyond the published rate.
- **V2 cutover uncertainty is acknowledged but not addressed.** The verified-prediction window (2025-01-23 to 2026-03-13) is entirely pre-V2. Phase 0 results reflect pre-V2 Polymarket behaviour. Phase 1 design, if the verdict is GO, must re-measure fees post-cutover.

## Artefacts

- Script: `day3/fee_verification.py`
- Endpoint used: `https://clob.polymarket.com/markets/<condition_id>`
- Verification: the CLOB endpoint returned `condition_id`, `tags`, `neg_risk`, `maker_base_fee`, `taker_base_fee` for every sampled market. Fee fields were present in 16/16 successful responses.
