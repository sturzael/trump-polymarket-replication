"""
Day 2 — Schema sanity replication.

Goal: reproduce the per-model verified hit rate from trump-code's published
predictions_log.json using their published market_SP500.json and the schema
convention we believe they use. If we cannot reproduce, we have misread the
schema and Phase 0 kills here.

Convention discovered on Day 2 spot checks:
  entry = open price of the first trading day on or after date_signal
  exit  = close price of the hold_days-th trading day after entry (0-indexed
          from entry: hold_days=0 means same-day close, hold_days=1 means
          next trading day's close, etc.)
  return_pct = (exit / entry - 1) * 100

Correct-flag reconstruction:
  LONG:      correct iff return_pct > 0
  SHORT:     correct iff return_pct < 0
  VOLATILE:  correct iff |return_pct| > 0.5 (approximate threshold)

Run:  python3 day2/sanity_replication.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

REF = Path("data/trump_code_refs")


def load_sp(path: Path) -> dict[str, dict]:
    return {r["date"]: r for r in json.load(open(path))}


def nth_trading_day(d: str, offset: int, sp: dict[str, dict]) -> str | None:
    dt = datetime.strptime(d, "%Y-%m-%d")
    count = 0
    for _ in range(30):
        s = dt.strftime("%Y-%m-%d")
        if s in sp:
            if count == offset:
                return s
            count += 1
        dt = dt + timedelta(days=1)
    return None


def reconstruct_return(p: dict, sp: dict[str, dict]) -> tuple[float, str, str] | None:
    d_entry = nth_trading_day(p["date_signal"], 0, sp)
    d_exit = nth_trading_day(p["date_signal"], p["hold_days"], sp)
    if d_entry is None or d_exit is None:
        return None
    ret = (sp[d_exit]["close"] / sp[d_entry]["open"] - 1) * 100
    return ret, d_entry, d_exit


def reconstruct_correct(direction: str, ret: float) -> bool:
    if direction == "LONG":
        return ret > 0
    if direction == "SHORT":
        return ret < 0
    if direction == "VOLATILE":
        return abs(ret) > 0.5
    raise ValueError(f"unexpected direction {direction!r}")


def main() -> None:
    preds = json.load(open(REF / "predictions_log.json"))
    sp = load_sp(REF / "market_SP500.json")

    buckets = defaultdict(list)
    for p in preds:
        if p["status"] != "VERIFIED":
            continue
        r = reconstruct_return(p, sp)
        if r is None:
            continue
        ret, d_e, d_x = r
        correct_r = reconstruct_correct(p["direction"], ret)
        buckets[p["model_id"]].append({
            "date_signal": p["date_signal"],
            "their_ret": p["actual_return"],
            "repro_ret": ret,
            "abs_err": abs(ret - p["actual_return"]),
            "their_correct": p["correct"],
            "repro_correct": correct_r,
            "hold_days": p["hold_days"],
            "direction": p["direction"],
        })

    print(f"{'model_id':<25} {'hold':>4} {'n':>4} {'their_hit%':>10} {'repro_hit%':>10} "
          f"{'ret_mae':>8} {'exact<0.01':>11} {'agree%':>7}")
    for mid in sorted(buckets):
        rows = buckets[mid]
        their_hit = sum(r["their_correct"] for r in rows) / len(rows) * 100
        repro_hit = sum(r["repro_correct"] for r in rows) / len(rows) * 100
        mae = sum(r["abs_err"] for r in rows) / len(rows)
        exact = sum(1 for r in rows if r["abs_err"] < 0.01)
        agree = sum(1 for r in rows if r["their_correct"] == r["repro_correct"]) / len(rows) * 100
        hold = rows[0]["hold_days"]
        print(f"{mid:<25} {hold:>4} {len(rows):>4} {their_hit:>9.1f}  {repro_hit:>9.1f}  "
              f"{mae:>7.4f}  {exact:>11}  {agree:>6.1f}%")


if __name__ == "__main__":
    main()
