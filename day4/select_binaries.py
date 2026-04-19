"""
Day 4 — Binary selection.

Goal: pick 10 Polymarket political binaries diversified across signal
categories, within the pre-registered $100k-$1M TVL band at signal-window
time, with sufficient in-scope signal events to power the Day 6 tests.

TVL-at-signal-time limitation (see PRE_REGISTRATION.md amendment for full
reasoning): data-api /trades does not support timestamp filter, pagination
capped at offset=5000. We use the proxy:

    tvl_proxy = lifetime_volume * (signal_window_overlap_days / total_active_days)

This assumes uniform volume over time — an approximation. The binary list
is frozen in PRE_REGISTRATION.md §2 via amendment regardless of proxy
error; it will not be revised after Day 5 price access.

Pipeline:
1. Fetch all closed + active political markets from Gamma, keyword-filter
   for Trump-signal-responsive slugs.
2. Filter by signal-window overlap >= 60 days and resolution in 2025-02
   to 2026-12.
3. Restrict to $100k-$3M TVL proxy band (wider than target for noise).
4. Score by (signal_events × diversification_weight).
5. Select 10 across iran_israel / russia_ukraine / china / nobel_trump /
   trump_action categories.

Run:  python3 day4/select_binaries.py
"""
from __future__ import annotations

import json
import time
import urllib.request
from collections import defaultdict
from datetime import datetime

SIG_START = datetime(2025, 1, 23)
SIG_END = datetime(2026, 3, 13)

TIER1_KW = [
    "tariff", "trade-deal", "trade-war",
    "china", "xi-jinping", "taiwan",
    "russia", "ukraine", "putin", "ceasefire",
    "iran", "israel", "gaza", "hamas", "hezbollah",
    "fed-rate", "powell", "fed-chair",
    "cabinet", "resign", "fire-", "removed",
    "executive-order", "signed", "sign-", "announce",
    "congress", "speaker", "impeach",
    "epstein", "release", "classified",
    "nato", "mexico", "cartel", "sanction", "pardon",
    "nuke", "invasion", "invade",
    "trump",
]

EXCLUDE_KW = [
    "lebron", "kardashian", "vivek", "tulsi", "ramaswamy",
    "warsh", "shelton", "2028-us-presidential",
    "2028-election", "2028-democratic",
]

IN_SCOPE = [
    "A1_tariff_bearish", "A3_relief_rocket", "B1_triple_signal",
    "C1_burst_silence", "C3_night_alert",
]


def fetch(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"__error__": str(e)}


def parse_iso(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return None


def categorize(slug: str) -> str:
    s = slug.lower()
    if any(k in s for k in ["iran", "khamenei", "hormuz", "israel"]):
        return "iran_israel"
    if any(k in s for k in ["russia", "ukraine", "putin", "zelenskyy", "nato"]):
        return "russia_ukraine"
    if any(k in s for k in ["china", "xi", "taiwan"]):
        return "china"
    if "nobel" in s and "trump" in s:
        return "nobel_trump"
    if "fed" in s or "powell" in s:
        return "fed"
    if "tariff" in s or "supreme-court" in s:
        return "tariff"
    if any(k in s for k in ["resign", "impeach", "pardon", "cabinet"]):
        return "trump_action"
    return "other"


def collect_candidates():
    candidates = []
    seen = set()
    for closed_val in ["false", "true"]:
        for offset in range(0, 6000, 500):
            url = (f"https://gamma-api.polymarket.com/markets?"
                   f"closed={closed_val}&limit=500&offset={offset}"
                   f"&order=endDate&ascending=false")
            data = fetch(url)
            if not isinstance(data, list) or not data:
                break
            for m in data:
                if not isinstance(m, dict):
                    continue
                slug = m.get("slug", "").lower()
                if any(kw in slug for kw in EXCLUDE_KW):
                    continue
                if not any(kw in slug for kw in TIER1_KW):
                    continue
                cid = m.get("conditionId")
                if not cid or cid in seen:
                    continue
                seen.add(cid)
                sd = parse_iso(m.get("startDate") or m.get("startDateIso"))
                ed = parse_iso(m.get("endDate") or m.get("endDateIso"))
                if not sd or not ed:
                    continue
                overlap_start = max(sd, SIG_START)
                overlap_end = min(ed, SIG_END)
                overlap_days = max(0, (overlap_end - overlap_start).days)
                active_days = max(1, (ed - sd).days)
                if overlap_days < 60:
                    continue
                if not ("2025-02" <= ed.strftime("%Y-%m") <= "2026-12"):
                    continue
                vol = float(m.get("volume") or 0)
                if vol < 50_000:
                    continue
                tvl_proxy = vol * (overlap_days / active_days)
                if not (100_000 <= tvl_proxy <= 3_000_000):
                    continue
                candidates.append({
                    "slug": m["slug"],
                    "conditionId": cid,
                    "volume": vol,
                    "startDate": sd.isoformat(),
                    "endDate": ed.isoformat(),
                    "overlap_days": overlap_days,
                    "active_days": active_days,
                    "overlap_share": overlap_days / active_days,
                    "tvl_proxy": tvl_proxy,
                    "category": categorize(m["slug"]),
                })
            time.sleep(0.4)
    return candidates


def count_signal_events(preds, startDate_iso, endDate_iso):
    sd = datetime.fromisoformat(startDate_iso)
    ed = datetime.fromisoformat(endDate_iso)
    total = 0
    per_model = defaultdict(int)
    for p in preds:
        if p["status"] != "VERIFIED" or p["model_id"] not in IN_SCOPE:
            continue
        d = datetime.strptime(p["date_signal"], "%Y-%m-%d")
        if sd <= d <= ed:
            total += 1
            per_model[p["model_id"]] += 1
    return total, dict(per_model)


def main():
    preds = json.load(open("data/trump_code_refs/predictions_log.json"))
    candidates = collect_candidates()
    for m in candidates:
        total, per_m = count_signal_events(preds, m["startDate"], m["endDate"])
        m["signal_events"] = total
        m["per_model"] = per_m

    candidates = [m for m in candidates if m["signal_events"] >= 50 and m["tvl_proxy"] <= 1_100_000]

    # Bucket by category, pick 10 diversified
    by_cat = defaultdict(list)
    for m in candidates:
        by_cat[m["category"]].append(m)
    for cat in by_cat:
        by_cat[cat].sort(key=lambda m: -m["signal_events"])

    wanted = ["iran_israel", "iran_israel",
              "russia_ukraine", "russia_ukraine",
              "china", "china",
              "nobel_trump",
              "trump_action", "trump_action", "trump_action"]

    selections = []
    pool = {k: list(v) for k, v in by_cat.items()}
    for wc in wanted:
        if pool.get(wc):
            selections.append(pool[wc].pop(0))

    # Persist (overrides Day 4 json with a fresh run)
    with open("data/phase0_selected_binaries.json", "w") as f:
        json.dump(selections, f, default=str, indent=2)

    print(f"selected {len(selections)}:")
    for m in selections:
        print(f'  {m["conditionId"][:14]}... n={m["signal_events"]:>3} '
              f'tvl_proxy={m["tvl_proxy"]:>10,.0f} cat={m["category"]:<15} {m["slug"][:60]}')


if __name__ == "__main__":
    main()
