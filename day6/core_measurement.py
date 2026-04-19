"""
Day 6 — Core measurement: hit rate, signal-vs-baseline, fee-adjusted edge.

For each (model × binary × horizon × direction_convention) cell, compute:
    n_signal, n_baseline
    hit_rate_signal, hit_rate_baseline
    mean_signed_ret_signal (percent)
    mean_signed_ret_baseline (percent)
    net_edge @ fee_bps ∈ {0, 3, 7.2, 15, 30}
    underpowered (True if n_signal < 15)

Direction convention:
    "pos" → predicted_binary_direction = same sign as rule's S&P direction
            (LONG → binary YES goes up; SHORT → YES goes down)
    "neg" → predicted_binary_direction = opposite sign

Signed return under direction convention D and rule direction R:
    LONG + pos  → signed_ret = +binary_ret
    SHORT + pos → signed_ret = -binary_ret
    LONG + neg  → signed_ret = -binary_ret
    SHORT + neg → signed_ret = +binary_ret

Hit: signed_ret > 0.
Mean edge: mean(signed_ret) across sample.
Fee model: Polymarket per-trade fee = size × fee_rate × p × (1-p) where p
is entry price; per-unit fee = fee_rate × p × (1-p). Deduct 2× this
(round-trip) from gross signed return to get net.

Horizon: use "canonical" (per-model hold_days horizon, per Day 2
amendment). For A3 (hold=0, unmeasurable at daily fidelity), record
with note and also report the plus1d cross-check horizon.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

FEE_BPS_SWEEP = [0, 3, 7.2, 15, 30]
IN_SCOPE_MODELS = ["A1_tariff_bearish", "A3_relief_rocket", "B1_triple_signal",
                   "C1_burst_silence", "C3_night_alert"]
CANONICAL_HORIZON = {
    "A1_tariff_bearish": "canonical",
    "A3_relief_rocket": "plus1d_crosscheck",  # A3 canonical is +6h, unmeasurable; use +1d cross-check and flag
    "B1_triple_signal": "canonical",
    "C1_burst_silence": "canonical",
    "C3_night_alert": "canonical",
}


def signed_ret(rule_direction: str, binary_ret: float, convention: str) -> float:
    sign_rule = +1 if rule_direction == "LONG" else -1 if rule_direction == "SHORT" else 0
    sign_conv = +1 if convention == "pos" else -1
    return sign_rule * sign_conv * binary_ret


def fee_per_trade(entry_px: float, fee_rate: float) -> float:
    # Polymarket per-unit fee = fee_rate × p × (1-p), round trip = ×2
    return 2 * fee_rate * entry_px * (1 - entry_px)


def main() -> None:
    aligned = json.load(open("data/aligned.json"))

    # Bucket by (model, binary, horizon, direction)
    cells = defaultdict(list)  # key → list of dicts
    for r in aligned:
        mid = r["model_id"]
        if mid not in IN_SCOPE_MODELS:
            continue
        slug = r["binary_slug"]
        hd = r["hold_days"]
        direction = r["direction"]

        # Horizon column mapping
        canonical_ret = r["canonical_ret"]
        plus1_ret = r["plus1_ret"]
        # A3 uses plus1d_crosscheck (canonical is None); others use canonical
        if CANONICAL_HORIZON[mid] == "plus1d_crosscheck":
            binary_ret = plus1_ret
        else:
            binary_ret = canonical_ret

        if binary_ret is None:
            continue

        entry_px = r["entry_px"]
        # Collect signal and baseline entries
        cells[(mid, slug, "signal", "pos")].append({"ret": signed_ret(direction, binary_ret, "pos"),
                                                    "entry_px": entry_px})
        cells[(mid, slug, "signal", "neg")].append({"ret": signed_ret(direction, binary_ret, "neg"),
                                                    "entry_px": entry_px})
        # Baselines
        for b in r["baselines"]:
            b_ret = b["plus1_ret"] if CANONICAL_HORIZON[mid] == "plus1d_crosscheck" else b["canonical_ret"]
            if b_ret is None:
                continue
            cells[(mid, slug, "baseline", "pos")].append({"ret": signed_ret(direction, b_ret, "pos"),
                                                          "entry_px": b["entry_px"]})
            cells[(mid, slug, "baseline", "neg")].append({"ret": signed_ret(direction, b_ret, "neg"),
                                                          "entry_px": b["entry_px"]})

    # Summarise per (model × binary × direction)
    rows = []
    slugs = sorted(set(k[1] for k in cells.keys()))
    for mid in IN_SCOPE_MODELS:
        for slug in slugs:
            for conv in ["pos", "neg"]:
                sig = cells.get((mid, slug, "signal", conv), [])
                base = cells.get((mid, slug, "baseline", conv), [])
                if not sig:
                    continue
                n_sig = len(sig)
                n_base = len(base)
                hit_sig = sum(1 for s in sig if s["ret"] > 0) / n_sig * 100 if n_sig else 0
                hit_base = sum(1 for s in base if s["ret"] > 0) / n_base * 100 if n_base else 0
                gross_edge_sig = sum(s["ret"] for s in sig) / n_sig * 100 if n_sig else 0  # percent
                gross_edge_base = sum(s["ret"] for s in base) / n_base * 100 if n_base else 0

                net_edges = {}
                for bps in FEE_BPS_SWEEP:
                    rate = bps / 10000
                    fees = [fee_per_trade(s["entry_px"], rate) for s in sig]
                    mean_fee = sum(fees) / n_sig if n_sig else 0  # as fraction
                    net_edge = gross_edge_sig - mean_fee * 100  # in percent
                    net_edges[bps] = net_edge

                rows.append({
                    "model_id": mid,
                    "binary_slug": slug,
                    "horizon_label": CANONICAL_HORIZON[mid],
                    "direction_convention": conv,
                    "n_signal": n_sig,
                    "n_baseline": n_base,
                    "hit_rate_signal": hit_sig,
                    "hit_rate_baseline": hit_base,
                    "hit_rate_margin": hit_sig - hit_base,
                    "gross_edge_signal_pct": gross_edge_sig,
                    "gross_edge_baseline_pct": gross_edge_base,
                    "net_edge_fee_bps": net_edges,
                    "underpowered": n_sig < 15,
                })

    # Save
    with open("results/day6_core_measurement.json", "w") as f:
        json.dump(rows, f, indent=2, default=str)

    # Console summary: per model × direction aggregate + cells that clear the hit-rate + edge threshold
    print(f"total cells: {len(rows)}")
    print(f"cells with n_signal >= 15: {sum(1 for r in rows if not r['underpowered'])}")
    print()
    print(f"{'model':<20} {'binary':<46} {'dir':<4} {'n':>4} {'hit%':>6} {'base%':>6} {'Δ':>5} {'net@7.2':>8} {'flag':<6}")
    for r in rows:
        flag = "UP" if r["underpowered"] else ""
        # Show cells that either clear 55% hit rate AND margin >= 5pp AND net >= 2
        # or are non-underpowered and might matter
        cond = (not r["underpowered"] and
                r["hit_rate_signal"] >= 50 and
                r["hit_rate_margin"] >= 3)
        marker = " ⋆" if (r["hit_rate_signal"] >= 55 and r["hit_rate_margin"] >= 5 and r["net_edge_fee_bps"][7.2] >= 2 and r["n_signal"] >= 15) else ""
        if cond or marker or r["n_signal"] >= 40:
            print(f"{r['model_id']:<20} {r['binary_slug'][:46]:<46} {r['direction_convention']:<4} "
                  f"{r['n_signal']:>4} {r['hit_rate_signal']:>5.1f}% {r['hit_rate_baseline']:>5.1f}% "
                  f"{r['hit_rate_margin']:>+4.1f} {r['net_edge_fee_bps'][7.2]:>+7.2f} {flag:<6}{marker}")

    # Aggregate per model
    print(f"\nPer-model aggregate (pooled across binaries, positive direction convention):")
    print(f"{'model':<20} {'n':>4} {'hit%':>6} {'base%':>6} {'Δ':>5} {'net@7.2':>8}")
    for mid in IN_SCOPE_MODELS:
        pos_rows = [r for r in rows if r["model_id"] == mid and r["direction_convention"] == "pos"]
        n = sum(r["n_signal"] for r in pos_rows)
        if n == 0:
            continue
        hit = sum(r["hit_rate_signal"] * r["n_signal"] for r in pos_rows) / n
        hit_b = sum(r["hit_rate_baseline"] * r["n_baseline"] for r in pos_rows) / sum(r["n_baseline"] for r in pos_rows)
        net_72 = sum(r["net_edge_fee_bps"][7.2] * r["n_signal"] for r in pos_rows) / n
        print(f"{mid:<20} {n:>4} {hit:>5.1f}% {hit_b:>5.1f}% {hit-hit_b:>+4.1f} {net_72:>+7.2f}")


if __name__ == "__main__":
    main()
