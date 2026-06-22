from subsets_utils import get

BASE = "https://bdl.stat.gov.pl/api/v1"
POLAND = "000000000000"

def g(path, **params):
    params.setdefault("format", "json"); params.setdefault("lang", "en")
    r = get(f"{BASE}/{path}", params=params, timeout=(10, 120))
    r.raise_for_status(); return r.json()

def first_vars(gid, n=3):
    subs = g("subjects", **{"parent-id": gid, "page-size": 100})["results"]
    vids = []
    for s in subs:
        vs = g("variables", **{"subject-id": s["id"], "page-size": 100})["results"]
        for v in vs:
            vids.append(v["id"])
            if len(vids) >= n: return vids, subs
    return vids, subs

for gid, label in [("G640", "CENSUS 2021 POP"), ("G201", "VOIVODSHIP BUDGET EXP"), ("G652","CENSUS21 ECON ACTIVITY")]:
    vids, subs = first_vars(gid)
    d = g(f"data/by-unit/{POLAND}", **{"var-id": vids, "page-size": 100})
    print(f"{gid} {label}: {len(subs)} subgroups, sample vids {vids} -> national results {d['totalRecords']}")
    for r in d.get("results", [])[:2]:
        print("   var", r["id"], "vals", r["values"][:2])
