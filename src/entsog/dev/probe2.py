import json
from collections import Counter
from subsets_utils import get

BASE = "https://transparency.entsog.eu/api/v1/"


def raw(path, params):
    r = get(BASE + path, params=params, timeout=(10, 180))
    print(f"\n=== {path} {params} -> HTTP {r.status_code} ===")
    if r.status_code != 200:
        print("body:", r.text[:300])
        return None
    doc = r.json()
    rk = next((k for k in doc if k != "meta" and isinstance(doc[k], list)), None)
    rows = doc.get(rk, []) if rk else []
    print("rows returned:", len(rows))
    return rows


# 1) what indicator values actually exist in operationaldata for one day
rows = raw("operationaldata", {"limit": 10000, "from": "2024-01-01", "to": "2024-01-01"})
if rows:
    print("indicators present:", Counter(r.get("indicator") for r in rows))
    print("periodTypes:", Counter(r.get("periodType") for r in rows))
    print("units:", Counter(r.get("unit") for r in rows))
    print("row count for ONE day (all indicators), limit 10000:", len(rows))

# 2) try indicator filter with exact label, one day
for ind in ["Physical Flow", "Physical flow", "Nomination", "Allocation", "GCV"]:
    raw("operationaldata", {"limit": 5, "indicator": ind, "from": "2024-01-01", "to": "2024-01-02"})

# 3) operationaldata one day with limit 10001 to see if there's a hard cap on limit
rows2 = raw("operationaldata", {"limit": 50000, "from": "2024-06-01", "to": "2024-06-01"})
if rows2 is not None:
    print("one-day rows at limit 50000:", len(rows2))

# 4) offset pagination check
r_off = raw("operationaldata", {"limit": 5, "offset": 5, "from": "2024-01-01", "to": "2024-01-01"})

# 5) aggregatedData — figure out required params
for p in [
    {"limit": 5, "periodType": "day", "from": "2024-01-01", "to": "2024-01-02"},
    {"limit": 5, "indicator": "Physical Flow", "periodType": "day", "from": "2024-01-01", "to": "2024-01-02"},
    {"limit": 5},
    {"limit": 5, "periodType": "day", "indicator": "Physical Flow"},
]:
    rr = raw("aggregatedData", p)
    if rr:
        print("  aggregatedData sample keys:", list(rr[0].keys()))
        break

# 6) cmpUnavailables / cmpUnsuccessful / cmpAuctions field samples + counts for a year
for ep in ["cmpUnavailables", "cmpUnsuccessfulRequests"]:
    rr = raw(ep, {"limit": 3, "from": "2024-01-01", "to": "2024-12-31"})
    if rr:
        print(f"  {ep} keys:", list(rr[0].keys()))
