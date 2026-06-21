from subsets_utils import get

BASE = "https://transparency.entsog.eu/api/v1/"


def raw(path, params):
    r = get(BASE + path, params=params, timeout=(10, 180))
    print(f"\n=== {path} {params} -> HTTP {r.status_code} ===")
    if r.status_code != 200:
        print("body:", r.text[:160])
        return None
    doc = r.json()
    rk = next((k for k in doc if k != "meta" and isinstance(doc[k], list)), None)
    rows = doc.get(rk, []) if rk else []
    print("rows:", len(rows))
    return rows


# balancing zones for keys
bz = raw("balancingzones", {"limit": 5})
bzkeys = [b.get("bzKey") for b in (bz or [])][:3]
print("bzkeys:", bzkeys)

ops = raw("operators", {"limit": 5})
opkeys = [o.get("operatorKey") for o in (ops or [])][:3]
print("opkeys:", opkeys)

# aggregatedData attempts with real keys + recent windows
attempts = [
    {"limit": 3, "indicator": "Physical Flow", "periodType": "day", "from": "2025-01-01", "to": "2025-01-02"},
    {"limit": 3, "indicator": "Physical Flow", "periodType": "day", "from": "2025-01-01", "to": "2025-01-02", "timezone": "CET"},
]
if bzkeys and bzkeys[0]:
    attempts.append({"limit": 3, "balancingZoneKey": bzkeys[0], "from": "2025-01-01", "to": "2025-01-31"})
    attempts.append({"limit": 3, "bzKey": bzkeys[0], "from": "2025-01-01", "to": "2025-01-31"})
if opkeys and opkeys[0]:
    attempts.append({"limit": 3, "operatorKey": opkeys[0], "from": "2025-01-01", "to": "2025-01-31"})
for p in attempts:
    rr = raw("aggregatedData", p)
    if rr:
        print("  AGG KEYS:", list(rr[0].keys()))
        break

# pin operationaldata rolling start (today 2026-06-19, ~5yr)
for d in ["2021-01-01", "2021-06-01", "2021-07-01", "2021-08-01", "2021-09-01"]:
    raw("operationaldata", {"limit": 1, "from": d, "to": d})
