"""
Day 3 AM — Lag-before-trade audit.

Pre-registered kill threshold: KILL the whole experiment if >30% of their
hit rate is attributable to S&P moves that had already occurred by the
realistic trade-decision point (post_timestamp + 10 min).

The plan originally assumed intraday minute-level S&P data. We only have
daily OHLC (their market_SP500.json). We therefore run a coarser but
conservative test:

    For each verified prediction, classify by post-time bucket on the
    signal day (pre-open / intraday / after-close). Then, for models with
    hold_days >= 1, compute the hit rate under two entry conventions:

      their_entry      = open(d_entry)      # what their measurement uses
      realistic_entry  = close(d_entry)     # latest-possible realistic
                                              entry for a trader who saw
                                              the post after market

    A "flipped" prediction is one that is correct under their_entry but
    incorrect under realistic_entry. The flip rate is the share of their
    correct predictions whose edge was captured pre-close-of-signal-day
    — i.e. reporting, not prediction.

    For hold_days=0 (A3 intraday), the test is degenerate (realistic_entry
    = close(d) = exit point, zero window). A3 cannot be audited without
    intraday minute data. Flagged separately.

Kill logic applied in aggregate, excluding A3's degenerate test:
    aggregate_flip_rate = sum(flipped) / sum(their_correct) across in-scope
    KILL if aggregate_flip_rate > 30%.

Run:  python3 day3/lag_audit.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

REF = Path("data/trump_code_refs")
IN_SCOPE = [
    "A1_tariff_bearish",
    "A3_relief_rocket",
    "B1_triple_signal",
    "C1_burst_silence",
    "C3_night_alert",
]


def nth_trading_day(d: str, offset: int, sp: dict) -> str | None:
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


def classify_day(times: list) -> str:
    if not times:
        return "NO_POSTS"
    thr_open = datetime.strptime("09:30", "%H:%M").time()
    thr_close = datetime.strptime("16:00", "%H:%M").time()
    pre = any(t < thr_open for t in times)
    intra = any(thr_open <= t < thr_close for t in times)
    post = any(t >= thr_close for t in times)
    if intra:
        return "INTRADAY"
    if pre and post:
        return "PRE_AND_AFTER_CLOSE"
    if pre:
        return "PRE_OPEN"
    if post:
        return "AFTER_CLOSE"
    return "UNKNOWN"


def main() -> None:
    preds = json.load(open(REF / "predictions_log.json"))
    sp_list = json.load(open(REF / "market_SP500.json"))
    sp = {r["date"]: r for r in sp_list}
    posts = json.load(open(REF / "trump_posts_lite.json"))["posts"]

    by_date = defaultdict(list)
    for p in posts:
        try:
            t = datetime.strptime(p["time"], "%H:%M").time()
            by_date[p["date"]].append(t)
        except Exception:
            pass
    for d in by_date:
        by_date[d].sort()

    print(f"{'model':<22} {'hold':>4} {'bucket':<22} {'n':>4} "
          f"{'their%':>7} {'realistic%':>10} {'flipped/correct':>17}")
    agg_flipped = 0
    agg_correct = 0
    for mid in IN_SCOPE:
        rows = [p for p in preds if p["model_id"] == mid and p["status"] == "VERIFIED"]
        buckets = defaultdict(list)
        for p in rows:
            buckets[classify_day(by_date.get(p["date_signal"], []))].append(p)

        for bucket in ["PRE_OPEN", "INTRADAY", "AFTER_CLOSE", "PRE_AND_AFTER_CLOSE", "NO_POSTS"]:
            recs = buckets.get(bucket, [])
            if not recs:
                continue
            their_hits = 0
            realistic_hits = 0
            flipped = 0
            n_tested = 0
            for p in recs:
                h = p["hold_days"]
                d_e = nth_trading_day(p["date_signal"], 0, sp)
                d_x = nth_trading_day(p["date_signal"], h, sp)
                if not d_e or not d_x:
                    continue
                n_tested += 1
                their_entry = sp[d_e]["open"]
                exit_p = sp[d_x]["close"]
                their_ret = (exit_p / their_entry - 1) * 100
                if p["direction"] == "LONG":
                    their_correct = their_ret > 0
                elif p["direction"] == "SHORT":
                    their_correct = their_ret < 0
                else:
                    continue
                if their_correct:
                    their_hits += 1

                if h >= 1:
                    real_entry = sp[d_e]["close"]
                    if p["direction"] == "LONG":
                        real_correct = exit_p > real_entry
                    else:
                        real_correct = exit_p < real_entry
                    if real_correct:
                        realistic_hits += 1
                    if their_correct and not real_correct:
                        flipped += 1

            n = n_tested
            th = their_hits / n * 100 if n else 0
            # realistic only meaningful when h >= 1
            if rows[0]["hold_days"] >= 1:
                rl_disp = f"{realistic_hits / n * 100:.1f}"
                fl_disp = f"{flipped}/{their_hits}"
                agg_flipped += flipped
                agg_correct += their_hits
            else:
                rl_disp = "N/A"
                fl_disp = "N/A (hold=0)"
            hold = rows[0]["hold_days"]
            print(f"{mid:<22} {hold:>4} {bucket:<22} {n:>4} "
                  f"{th:>6.1f}  {rl_disp:>10}  {fl_disp:>17}")
        print()

    rate = agg_flipped / agg_correct * 100 if agg_correct else 0
    print(f"AGGREGATE (in-scope, hold>=1 only): {agg_flipped} flipped / {agg_correct} correct = {rate:.1f}%")
    print(f"Pre-committed kill threshold: 30.0%")
    print(f"GATE: {'TRIGGERED — KILL EXPERIMENT' if rate > 30 else 'NOT TRIGGERED — proceed'}")


if __name__ == "__main__":
    main()
