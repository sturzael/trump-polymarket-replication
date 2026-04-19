"""
Day 7 — Bonferroni correction, reverse-direction test, temporal stability.

Inputs:
  results/day6_core_measurement.json — per-cell hit rates, baselines, edge
  data/aligned.json — raw records for temporal-stability first/second half

Outputs:
  results/day7_validity.json — enriched cell table with:
    - p_value_uncorrected (two-sided binomial test, signal vs baseline)
    - p_value_bonferroni (p_uncorrected × n_tests)
    - reverse_asymmetry_pp (hit_pos - hit_neg), magnitude indicates direction-informativeness
    - temporal_first_half_hit, temporal_second_half_hit, temporal_delta_pp
    - temporal_stable (abs(delta) < 10 pp)
    - passes_all_gates (bool, per pre-registration)
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path

FEE_BPS = 7.2
HIT_THRESHOLD = 55.0
MARGIN_THRESHOLD = 5.0
NET_EDGE_THRESHOLD = 2.0
N_MIN = 15
TEMPORAL_STABILITY_MAX = 10.0


def binomial_pvalue(k: int, n: int, p0: float) -> float:
    """Two-sided binomial test p-value via normal approximation (continuity-corrected).
    Fine for n>=15."""
    if n == 0 or p0 <= 0 or p0 >= 1:
        return 1.0
    mu = n * p0
    sigma = (n * p0 * (1 - p0)) ** 0.5
    if sigma == 0:
        return 1.0
    # Continuity correction
    z = (abs(k - mu) - 0.5) / sigma
    # Two-sided
    p = 2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2))))
    return max(0.0, min(1.0, p))


def main() -> None:
    cells = json.load(open("results/day6_core_measurement.json"))
    aligned = json.load(open("data/aligned.json"))

    # Bucket aligned records by (model, binary) and convention for temporal-stability check
    IN_SCOPE = ["A1_tariff_bearish", "A3_relief_rocket", "B1_triple_signal",
                "C1_burst_silence", "C3_night_alert"]

    # Compute first-half vs second-half by signal-window split
    SPLIT_DATE = "2025-08-19"  # midpoint of 2025-01-23 to 2026-03-13

    buckets = defaultdict(list)  # (model, binary, half) → list of signed rets per convention
    for r in aligned:
        if r["model_id"] not in IN_SCOPE:
            continue
        ret = r["plus1_ret"] if r["model_id"] == "A3_relief_rocket" else r["canonical_ret"]
        if ret is None:
            continue
        half = "first" if r["date_signal"] <= SPLIT_DATE else "second"
        for conv in ["pos", "neg"]:
            sign_rule = +1 if r["direction"] == "LONG" else -1 if r["direction"] == "SHORT" else 0
            sign_conv = +1 if conv == "pos" else -1
            signed = sign_rule * sign_conv * ret
            buckets[(r["model_id"], r["binary_slug"], conv, half)].append(signed)

    n_tests = len(cells)  # pre-specified Bonferroni divisor (100 cells)

    enriched = []
    for c in cells:
        mid, slug, conv = c["model_id"], c["binary_slug"], c["direction_convention"]
        n_sig = c["n_signal"]
        hit_s = c["hit_rate_signal"] / 100.0
        hit_b = c["hit_rate_baseline"] / 100.0

        # Binomial p-value: observed k = round(hit_s × n_sig), expected p0 = hit_b
        k = round(hit_s * n_sig)
        p_raw = binomial_pvalue(k, n_sig, hit_b)
        p_bonf = min(1.0, p_raw * n_tests)

        # Reverse-direction asymmetry: find opposite-convention cell for same (model, binary)
        opp = next((x for x in cells if x["model_id"] == mid and x["binary_slug"] == slug
                    and x["direction_convention"] != conv), None)
        rev_asym_pp = c["hit_rate_signal"] - (opp["hit_rate_signal"] if opp else c["hit_rate_signal"])

        # Temporal stability
        first_rets = buckets.get((mid, slug, conv, "first"), [])
        second_rets = buckets.get((mid, slug, conv, "second"), [])
        f_hit = (sum(1 for r in first_rets if r > 0) / len(first_rets) * 100
                 if first_rets else None)
        s_hit = (sum(1 for r in second_rets if r > 0) / len(second_rets) * 100
                 if second_rets else None)
        delta_pp = (abs(f_hit - s_hit) if f_hit is not None and s_hit is not None else None)
        temporal_stable = (delta_pp is not None and delta_pp < TEMPORAL_STABILITY_MAX)

        # Pre-registered survival: ALL of the following must hold
        net72 = c["net_edge_fee_bps"]["7.2"]
        passes = (
            n_sig >= N_MIN
            and c["hit_rate_signal"] >= HIT_THRESHOLD
            and c["hit_rate_margin"] >= MARGIN_THRESHOLD
            and net72 >= NET_EDGE_THRESHOLD
            and p_bonf < 0.05
            and abs(rev_asym_pp) >= 5  # reverse-direction asymmetry >= 5pp
            and temporal_stable
        )

        enriched.append({
            **c,
            "p_uncorrected": p_raw,
            "p_bonferroni": p_bonf,
            "reverse_asymmetry_pp": rev_asym_pp,
            "temporal_first_hit": f_hit,
            "temporal_second_hit": s_hit,
            "temporal_delta_pp": delta_pp,
            "temporal_stable": temporal_stable,
            "passes_all_gates": passes,
        })

    with open("results/day7_validity.json", "w") as f:
        json.dump(enriched, f, indent=2, default=str)

    # Print summary
    print(f"n_tests (Bonferroni divisor): {n_tests}")
    print(f"corrected alpha: 0.05 / {n_tests} = {0.05 / n_tests:.5f}")
    print()
    print("Cells passing all gates:")
    passers = [r for r in enriched if r["passes_all_gates"]]
    if not passers:
        print("  NONE")
    else:
        for r in passers:
            print(f"  {r['model_id']} × {r['binary_slug']} ({r['direction_convention']}):"
                  f" hit={r['hit_rate_signal']:.1f}% margin={r['hit_rate_margin']:+.1f}pp"
                  f" net@7.2={r['net_edge_fee_bps']['7.2']:+.2f}% p_bonf={r['p_bonferroni']:.3f}")

    # Cells that clear most gates
    print(f"\nCells clearing >= 3 gates (n, hit 55%, margin, net 2%, p_bonf):")
    for r in enriched:
        g = []
        if r["n_signal"] >= N_MIN: g.append("n")
        if r["hit_rate_signal"] >= HIT_THRESHOLD: g.append("hit55")
        if r["hit_rate_margin"] >= MARGIN_THRESHOLD: g.append("mgn5")
        if r["net_edge_fee_bps"]["7.2"] >= NET_EDGE_THRESHOLD: g.append("net2")
        if r["p_bonferroni"] < 0.05: g.append("p_bonf")
        if len(g) >= 3:
            print(f"  {r['model_id']:<20} {r['binary_slug'][:42]:<42} {r['direction_convention']:<4} "
                  f"gates={','.join(g):<28} hit={r['hit_rate_signal']:.1f}% margin={r['hit_rate_margin']:+.1f} "
                  f"net={r['net_edge_fee_bps']['7.2']:+.2f} p={r['p_bonferroni']:.3f}")

    # Per-model summary of temporal stability
    print(f"\nTemporal stability (absolute delta, first vs second half):")
    for mid in IN_SCOPE:
        rows = [r for r in enriched if r["model_id"] == mid and r["direction_convention"] == "pos"]
        deltas = [r["temporal_delta_pp"] for r in rows if r["temporal_delta_pp"] is not None]
        stable = [r["temporal_stable"] for r in rows if r["temporal_delta_pp"] is not None]
        if deltas:
            print(f"  {mid:<20} n_cells={len(deltas)} mean_delta={sum(deltas)/len(deltas):.1f}pp "
                  f"stable={sum(stable)}/{len(stable)}")


if __name__ == "__main__":
    main()
