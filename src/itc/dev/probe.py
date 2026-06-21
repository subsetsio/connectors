import json
from subsets_utils import get

BASE = "https://open.intracen.org/api/v1/itc"

def g(path):
    r = get(f"{BASE}/{path}", timeout=(10,120))
    r.raise_for_status()
    p = r.json()
    assert p.get("success") is True, p
    return p["data"]

info = g("general-info"); print("timespan:", info["timespan"])
s = g("summary?year=2024"); print("summary 2024:", s)

m = g("map?year=2024")
k = next(iter(m)); print("map area sample:", k, json.dumps(m[k], default=str)[:300])

acts = g("activities")
print("activities count:", acts["count"], "page size:", len(acts["results"]))
print("list keys:", sorted(acts["results"][0].keys()))
print("sample list row:", json.dumps(acts["results"][0], default=str)[:300])

ident = acts["results"][0]["identifier"]
d = g(f"activities/{ident}")
print("detail keys:", sorted(d.keys()))
print("budgets:", d.get("budgets"))
print("expenses:", d.get("expenses"))
print("reporting_org:", d.get("reporting_org"))
print("budget_utilisation:", d.get("budget_utilisation"))
at = d.get("all_transactions", {})
print("txn types:", {k: len(v) for k,v in at.items()})
for t,v in at.items():
    if v:
        print("sample txn", t, json.dumps(v[0], default=str)[:200]); break
