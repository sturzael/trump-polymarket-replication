"""
Day 5 — Price alignment + matched non-signal baseline sampling.

For each of 10 selected binaries, align each in-scope verified prediction
whose signal-date falls within the binary's price-history coverage, and
sample N=10 matched non-signal days per event.

Horizon coverage:
  Available: daily resolution (1440-min fidelity on CLOB /prices-history)
  Per-model canonical horizons (Day 2 amendment):
    A3_relief_rocket:  +0d (hold=0, open->close same day) — NOT MEASURABLE
                       without intraday data; marked NA for A3
    A1_tariff_bearish: +1d
    C1_burst_silence:  +1d
    C3_night_alert:    +1d
    B1_triple_signal:  +3d

  Extra column: +1d measured for all models regardless (common-horizon
  cross-check in Day 6).

Output: data/aligned.json with one record per (event, binary, horizon).
"""
from __future__ import annotations

import json
import random
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

REF = Path("data/trump_code_refs")
IN_SCOPE = ["A1_tariff_bearish", "A3_relief_rocket", "B1_triple_signal",
            "C1_burst_silence", "C3_night_alert"]
HOLD_DAYS = {
    "A1_tariff_bearish": 1, "A3_relief_rocket": 0, "B1_triple_signal": 3,
    "C1_burst_silence": 1, "C3_night_alert": 1,
}
BASELINE_N = 10
RNG_SEED = 42


def load_daily_prices(history):
    """history = list of {t, p}; return dict date_str -> price, using close of each UTC day."""
    by_date = {}
    for h in history:
        dt = datetime.fromtimestamp(h["t"])
        d = dt.strftime("%Y-%m-%d")
        by_date[d] = h["p"]  # last write wins; data is already daily fidelity
    return by_date


def advance_days(d: str, days: int) -> str:
    dt = datetime.strptime(d, "%Y-%m-%d") + timedelta(days=days)
    return dt.strftime("%Y-%m-%d")


def nearest_on_or_before(d: str, prices_by_date: dict, max_back: int = 7) -> tuple | None:
    """Return (date_used, price) — nearest trading/price-day on or before d. None if no such day within max_back."""
    for back in range(max_back + 1):
        candidate = advance_days(d, -back)
        if candidate in prices_by_date:
            return candidate, prices_by_date[candidate]
    return None


def main():
    rng = random.Random(RNG_SEED)

    preds = json.load(open(REF / "predictions_log.json"))
    sp = {r["date"]: r for r in json.load(open(REF / "market_SP500.json"))}
    prices_all = json.load(open("data/binary_price_history.json"))

    # Verified in-scope predictions
    in_scope_preds = [p for p in preds if p["model_id"] in IN_SCOPE and p["status"] == "VERIFIED"]

    # Index signal dates globally — used to avoid sampling baseline on any-signal day
    all_signal_dates = set(p["date_signal"] for p in preds if p["status"] == "VERIFIED")

    aligned = []
    per_binary_counts = defaultdict(lambda: defaultdict(int))

    for slug, pdata in prices_all.items():
        prices = load_daily_prices(pdata["history"])
        # Valid date range for this binary
        dates_sorted = sorted(prices.keys())
        bin_start = dates_sorted[0]
        bin_end = dates_sorted[-1]

        # Candidate non-signal dates = dates in binary's range that are NOT a signal day in the entire
        # predictions log (so baseline sampling avoids any signal contamination, not just in-scope)
        nonsig_candidates = [d for d in dates_sorted if d not in all_signal_dates]

        for p in in_scope_preds:
            ds = p["date_signal"]
            if ds < bin_start or ds > bin_end:
                continue  # outside binary's price coverage
            hd = p["hold_days"]
            # Entry price at close of date_signal (or nearest-prior day if missing)
            entry = nearest_on_or_before(ds, prices)
            if not entry:
                continue
            entry_date, entry_px = entry

            # Per-model canonical horizon
            if hd >= 1:
                exit_d = advance_days(ds, hd)
                exit_hit = nearest_on_or_before(exit_d, prices)
                canonical_exit_date = exit_hit[0] if exit_hit else None
                canonical_exit_px = exit_hit[1] if exit_hit else None
                canonical_ret = ((exit_hit[1] / entry_px) - 1) if exit_hit and entry_px else None
            else:
                canonical_exit_date = None
                canonical_exit_px = None
                canonical_ret = None  # A3 not measurable at daily fidelity

            # Common +1d horizon (for cross-model sanity)
            exit_plus1 = advance_days(ds, 1)
            e1 = nearest_on_or_before(exit_plus1, prices)
            plus1_ret = ((e1[1] / entry_px) - 1) if e1 and entry_px else None

            # S&P return at same horizons (using their market data, open->close convention from Day 2)
            sp_entry = sp.get(ds)
            sp_exit_canonical = sp.get(advance_days(ds, hd)) if hd >= 1 else None
            sp_ret_canonical = ((sp_exit_canonical["close"] / sp_entry["open"]) - 1) if sp_entry and sp_exit_canonical else None

            # Baseline samples
            baselines = []
            sample_pool = nonsig_candidates[:]
            rng_local = random.Random(f"{slug}:{ds}:{RNG_SEED}")
            rng_local.shuffle(sample_pool)
            collected = 0
            for bdate in sample_pool:
                if collected >= BASELINE_N:
                    break
                b_entry = nearest_on_or_before(bdate, prices)
                if not b_entry:
                    continue
                if hd >= 1:
                    b_exit = nearest_on_or_before(advance_days(bdate, hd), prices)
                else:
                    b_exit = None
                b_plus1 = nearest_on_or_before(advance_days(bdate, 1), prices)
                # S&P baseline
                sp_b_entry = sp.get(bdate)
                sp_b_exit_canonical = sp.get(advance_days(bdate, hd)) if hd >= 1 else None
                baselines.append({
                    "date": bdate,
                    "entry_px": b_entry[1],
                    "exit_canonical_px": b_exit[1] if b_exit else None,
                    "canonical_ret": ((b_exit[1] / b_entry[1]) - 1) if b_exit and b_entry[1] else None,
                    "plus1_ret": ((b_plus1[1] / b_entry[1]) - 1) if b_plus1 and b_entry[1] else None,
                    "sp_ret_canonical": (sp_b_exit_canonical["close"] / sp_b_entry["open"] - 1)
                                        if sp_b_entry and sp_b_exit_canonical else None,
                })
                collected += 1

            aligned.append({
                "model_id": p["model_id"],
                "date_signal": ds,
                "hold_days": hd,
                "direction": p["direction"],
                "binary_slug": slug,
                "entry_date": entry_date,
                "entry_px": entry_px,
                "canonical_exit_date": canonical_exit_date,
                "canonical_exit_px": canonical_exit_px,
                "canonical_ret": canonical_ret,
                "plus1_ret": plus1_ret,
                "sp_ret_canonical": sp_ret_canonical,
                "their_correct": p.get("correct"),
                "their_actual_return": p.get("actual_return"),
                "baselines": baselines,
            })
            per_binary_counts[slug][p["model_id"]] += 1

    with open("data/aligned.json", "w") as f:
        json.dump(aligned, f)

    print(f"aligned records: {len(aligned)}")
    print(f'\n{"binary":<58} {"A1":>4} {"A3":>4} {"B1":>4} {"C1":>4} {"C3":>4} {"total":>5}')
    for slug in prices_all:
        counts = per_binary_counts[slug]
        total = sum(counts.values())
        print(f'{slug:<58} {counts.get("A1_tariff_bearish",0):>4} '
              f'{counts.get("A3_relief_rocket",0):>4} {counts.get("B1_triple_signal",0):>4} '
              f'{counts.get("C1_burst_silence",0):>4} {counts.get("C3_night_alert",0):>4} {total:>5}')

    # Also per-model totals
    model_totals = defaultdict(int)
    for r in aligned:
        model_totals[r["model_id"]] += 1
    print(f'\nper-model aligned n: {dict(model_totals)}')


if __name__ == "__main__":
    main()
