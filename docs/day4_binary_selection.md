# Day 4 — Binary Market Selection

Status: 10 binaries frozen in `PRE_REGISTRATION.md §2` via amendment. Binary list cannot be revised after Day 5 price access.

## Selected 10 binaries (diversified, $100k–$1.05M TVL proxy band)

| # | Slug | Category | Signal events | TVL proxy |
|---|------|----------|--------------:|----------:|
| 1 | `will-israel-annex-syrian-territory-before-july` | iran_israel | 235 | $103,757 |
| 2 | `us-iran-nuclear-deal-before-2027` | iran_israel | 60 | $216,035 |
| 3 | `zelenskyy-out-as-ukraine-president-before-2027` | russia_ukraine | 110 | $936,822 |
| 4 | `ukraine-joins-nato-before-2027` | russia_ukraine | 60 | $339,859 |
| 5 | `will-xi-jinping-win-the-nobel-peace-prize-in-2026` | china | 70 | $372,388 |
| 6 | `china-x-taiwan-military-clash-before-2027` | china | 57 | $478,863 |
| 7 | `will-donald-trump-win-the-nobel-peace-prize-in-2026-382` | nobel_trump | 70 | $1,043,568 |
| 8 | `will-trump-resign-by-december-31-2026` | trump_action | 110 | $189,792 |
| 9 | `will-trump-pardon-ghislaine-maxwell` | trump_action | 111 | $238,333 |
| 10 | `will-trump-be-impeached-by-december-31-2026` | trump_action | 110 | $304,495 |

Full conditionIds stored in `data/phase0_selected_binaries.json` (gitignored; regenerable via `day4/select_binaries.py`).

## Pipeline

1. **Raw candidates (2,251).** Gamma API, all closed + active markets with political-keyword slug match that overlap the verified-prediction signal window (2025-01-23 to 2026-03-13).
2. **Tier-1 signal-responsive (287).** Keyword filter on slugs: tariff, china, russia, ukraine, iran, israel, fed, cabinet, resign, impeach, tariff, nuke, nato, trump. Exclude obvious long-shot 2028-candidate markets. Require lifetime volume ≥ $50k.
3. **Overlap-and-resolution constrained (117).** Retain markets with ≥60 days signal-window overlap and endDate in Feb-2025 to Dec-2026 (limits post-signal-window volume-dilution effects on the TVL proxy).
4. **TVL-proxy band (60).** Restrict to `$100k ≤ volume × overlap_share ≤ $3M` and `signal_events ≥ 50`. Wider than final target to allow proxy-to-truth noise. 60 candidates survive.
5. **Diversified 10.** Manual selection enforcing category spread (2 iran_israel / 2 russia_ukraine / 2 china / 1 nobel_trump / 3 trump_action), all within $100k-$1.05M TVL proxy.

## Rejected candidates (rationale logged)

- **Fed-chair nomination basket (20+ variants).** Same neg-risk basket; prices move together; multiple selections would be double-counting the same signal. Retained category coverage through the Trump-Nobel and Trump-action markets which are more price-responsive to Trump posts per category analysis.
- **`putin-out-before-2027`** ($1.83M TVL proxy), **`will-the-supreme-court-rule-in-favor-of-trumps-tariffs`** ($1.88M), **`will-trump-nominate-david-malpass-as-the-next-fed-chair`** ($2.71M): above $1M target ceiling. Zelenskyy-out and Ukraine-NATO serve the Russia/Ukraine category at in-band TVL.
- **`us-strikes-iran-by-*`** markets: high TVL proxies ($3.9M) concentrated in Iran-strike catalyst events; volume not representative of broader-signal responsiveness.
- **Long-tail 2028 presidential candidate markets:** resolution horizon too distant to respond to short-term posts. Excluded at Tier-1.
- **`will-china-unban-bitcoin-by-2027`, `will-china-invade-taiwan-before-2027`**: low direct-signal response (China invade Taiwan was 19.6M TVL — far outside target band regardless).

## TVL-proxy caveat

The pre-registered criterion specifies TVL "at the time of each overlapping signal fire." This requires aggregating Polymarket trades timestamp-filtered to the signal window. Two blockers prevented direct measurement:

1. Polymarket `data-api/trades` endpoint does not support timestamp filtering. All parameter variants tested (`timestampMin`, `timestamp_min`, `startTs`, `start_ts`, `after`, `before`) returned the latest trades regardless.
2. Client-side pagination is capped at `offset=5000`. Markets with >5,000 lifetime trades (which includes several selected markets) cannot be paginated to reach signal-window trades.
3. Downloading SII (954M rows, ≈107 GB) is out-of-budget for this Phase 0.

Substitute: `tvl_proxy = lifetime_volume × (signal_window_overlap_days / total_active_days)`, which assumes uniform volume distribution over a market's active window. This is false in general — political markets concentrate volume near catalysts. The proxy can under- or over-estimate true signal-window TVL.

**Mitigation accepted as trade-off:** The $100k-$1M band is a proxy band. Two asymmetric consequences:
- Markets with true signal-window TVL < $100k could produce noisy / slippage-dominated Day 6 measurements. Flagged in verdict if this turns out to be the case.
- Markets with true signal-window TVL > $1M are not a validity threat — deeper liquidity reduces noise.

The binary list is frozen at this amendment timestamp and will not be revised after Day 5 price access. Revising selections based on post-access information would recreate selection bias.

## Signal-event density per binary

Every selected binary has ≥57 in-scope signal events during its active window. The heaviest-active market (`will-israel-annex-syrian-territory-before-july`, 414-day active span, 235 events) will drive most of the n per rule. The minimum (`china-x-taiwan-military-clash-before-2027`, 119 days, 57 events) is still enough to contribute meaningful per-rule observations after binary-level splits.

## Artifacts

- Script: `day4/select_binaries.py` (regenerates selection deterministically from Gamma state)
- Output: `data/phase0_selected_binaries.json` (gitignored)
- Intermediate: `data/candidates_pre_tvl_filter.json`, `data/candidates_good.json` (gitignored)
