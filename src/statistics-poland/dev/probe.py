import json
from subsets_utils import get

BASE = "https://bdl.stat.gov.pl/api/v1"

def g(path, **params):
    params.setdefault("format", "json")
    params.setdefault("lang", "en")
    r = get(f"{BASE}/{path}", params=params, timeout=(10, 120))
    r.raise_for_status()
    return r.json()

# 1. Subgroups (P) under a group, e.g. G7 POPULATION and G541 GDP NUTS2
for gid in ["G7", "G541"]:
    subs = g("subjects", **{"parent-id": gid, "page-size": 100})
    print(f"\n=== group {gid}: {subs['totalRecords']} subgroups ===")
    for s in subs["results"][:4]:
        print("  P", s["id"], s.get("hasVariables"), s["name"][:50])
    # variables under first P subgroup
    if subs["results"]:
        p = subs["results"][0]["id"]
        v = g("variables", **{"subject-id": p, "page-size": 100})
        print(f"  variables under {p}: total={v['totalRecords']}")
        for vv in v["results"][:3]:
            print("    var", vv["id"], "n1=", vv.get("n1"), "unit=", vv.get("measureUnitName"))

# 2. Does subject-id=G (group) return variables directly?
v = g("variables", **{"subject-id": "G7", "page-size": 5})
print("\nvariables with subject-id=G7 (group level):", v["totalRecords"])

# 3. data-by-variable with unit-level filter (national=0, voivodship=2)
print("\n--- data-by-variable 3643 unit-level=0 ---")
d0 = g("data/by-variable/3643", **{"unit-level": 0, "page-size": 100})
print("total units:", d0["totalRecords"], "| keys:", list(d0.keys()))
if d0["results"]:
    r0 = d0["results"][0]
    print("unit:", r0["id"], r0["name"], "| #values:", len(r0["values"]), "| sample:", r0["values"][:2])
print("--- data-by-variable 3643 unit-level=2 (voivodship) ---")
d2 = g("data/by-variable/3643", **{"unit-level": 2, "page-size": 100})
print("total units:", d2["totalRecords"])
