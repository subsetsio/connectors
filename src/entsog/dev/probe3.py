from collections import Counter
from subsets_utils import get

BASE = "https://transparency.entsog.eu/api/v1/"


def raw(path, params):
    r = get(BASE + path, params=params, timeout=(10, 180))
    print(f"\n=== {path} {params} -> HTTP {r.status_code} ===")
    if r.status_code != 200:
        print("body:", r.text[:200])
        return None
    doc = r.json()
    rk = next((k for k in doc if k != "meta" and isinstance(doc[k], list)), None)
    rows = doc.get(rk, []) if rk else []
    print("rows:", len(rows))
    return rows


# aggregatedData — try many param shapes to find what it wants
for p in [
    {"limit": 3, "periodType": "Day", "from": "2024-01-01", "to": "2024-01-02"},
    {"limit": 3, "periodType": "day", "periodFrom": "2024-01-01", "periodTo": "2024-01-02"},
    {"limit": 3, "from": "2024-01-01", "to": "2024-01-02"},
    {"limit": 3, "periodType": "hour", "from": "2024-01-01", "to": "2024-01-02"},
    {"limit": 3, "periodType": "day", "from": "2024-01-01", "to": "2024-01-31", "indicator": "Physical Flow"},
    {"limit": 3, "periodType": "day", "directionKey": "entry", "from": "2024-01-01", "to": "2024-01-02"},
    {"limit": 3, "indicator": "Physical Flow", "from": "2023-01-01", "to": "2023-12-31"},
]:
    rr = raw("aggregatedData", p)
    if rr:
        print("  KEYS:", list(rr[0].keys()))
        print("  sample:", {k: rr[0].get(k) for k in list(rr[0].keys())[:12]})
        break

# operationaldata earliest data — probe a few historical dates
for d in ["2013-01-01", "2015-01-01", "2016-01-01", "2017-01-01", "2018-01-01"]:
    raw("operationaldata", {"limit": 1, "from": d, "to": d})

# full-corpus single-pull endpoints: how big?
for ep in ["operators", "operatorpointdirections", "connectionpoints", "interconnections"]:
    rr = raw(ep, {"limit": 100000})
    if rr is not None:
        print(f"  {ep} full corpus size: {len(rr)}")

# urgentmarketmessages / tariffs full size
for ep in ["urgentmarketmessages", "tariffssimulations", "tariffsfulls"]:
    rr = raw(ep, {"limit": 100000})
    if rr is not None:
        print(f"  {ep} full size: {len(rr)}")
