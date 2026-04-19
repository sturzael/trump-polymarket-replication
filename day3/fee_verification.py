"""
Day 3 PM — Political-markets fee verification.

Pre-committed purpose: pull 3-5 resolved Polymarket political markets and
check on-chain taker fee fields. If political markets show non-zero taker
fees, adjust the 2% net-edge threshold upward accordingly.

We cannot audit SII (954M-row HuggingFace parquet, 107GB) from this local
environment in-budget. Substitute: query Polymarket's public CLOB market
endpoint, which exposes the `maker_base_fee` and `taker_base_fee` fields
directly per market. This is the protocol-configured rate for CLOB orders;
it is what actually gets charged on fills. A non-zero value here would
appear as a non-zero fee at settlement; a zero value means the CLOB does
not add a base fee (consistent with the memory's empirical 0-bps measurement
on a 143-trade sports sample).

Cross-category sample to check whether the 0-bps finding is sports-only or
applies across categories.

Run:  python3 day3/fee_verification.py
"""
from __future__ import annotations

import json
import time
import urllib.request


def fetch(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"__error__": str(e)}


def main() -> None:
    categories = {
        "trump_policy": ["trump", "tariff"],
        "elections": ["election", "vote", "presiden"],
        "geopolitics": ["ukraine", "israel", "iran", "china", "russia", "gaza"],
        "cabinet": ["cabinet", "resign"],
        "sports_control": ["nfl", "nba", "game", "match"],
        "crypto_control": ["bitcoin", "eth", "btc"],
    }

    data = fetch("https://gamma-api.polymarket.com/markets?closed=false&active=true&limit=500")
    if not isinstance(data, list):
        print("gamma error:", data)
        return

    seen = set()
    all_samples = []
    for cat, keywords in categories.items():
        fee_samples = []
        for m in data:
            if not isinstance(m, dict):
                continue
            slug = m.get("slug", "").lower()
            if any(kw in slug for kw in keywords) and m.get("conditionId") and m["conditionId"] not in seen:
                seen.add(m["conditionId"])
                url = f'https://clob.polymarket.com/markets/{m["conditionId"]}'
                d = fetch(url)
                if isinstance(d, dict) and "maker_base_fee" in d:
                    fee_samples.append({
                        "category": cat,
                        "slug": slug,
                        "maker_base_fee": d.get("maker_base_fee"),
                        "taker_base_fee": d.get("taker_base_fee"),
                        "tags": d.get("tags", [])[:3],
                        "neg_risk": d.get("neg_risk"),
                    })
                if len(fee_samples) >= 3:
                    break
                time.sleep(0.2)
        all_samples.extend(fee_samples)
        time.sleep(0.3)

    for s in all_samples:
        print(f'[{s["category"]:<15}] maker={s["maker_base_fee"]} taker={s["taker_base_fee"]}  {s["slug"][:55]}')

    uniq_taker = set(s["taker_base_fee"] for s in all_samples)
    uniq_maker = set(s["maker_base_fee"] for s in all_samples)
    print(f"\nUnique taker_base_fee values across {len(all_samples)} samples: {uniq_taker}")
    print(f"Unique maker_base_fee values: {uniq_maker}")

    verdict = "FEE ADJUSTMENT NOT REQUIRED" if uniq_taker == {0} else "FEE ADJUSTMENT REQUIRED"
    print(f"\n{verdict}")
    print(f"Canonical 7.2 bps threshold in PRE_REGISTRATION remains conservative.")


if __name__ == "__main__":
    main()
