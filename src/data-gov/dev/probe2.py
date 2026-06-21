from subsets_utils import get
BASE = "https://catalog-old.data.gov/api/3"
def j(path, **params):
    r = get(f"{BASE}/{path}", params=params, timeout=(10.0,120.0))
    r.raise_for_status()
    return r.json()

# deep paging test
for start in (10000, 50000, 100000, 200000, 401000):
    try:
        d = j("action/package_search", rows=5, start=start)
        res = d["result"]
        print(f"start={start} success={d['success']} returned={len(res['results'])}")
    except Exception as e:
        print(f"start={start} ERROR {type(e).__name__}: {str(e)[:120]}")

# org list offset pagination
for off in (0,25,50):
    d = j("action/organization_list", all_fields="true", offset=off, limit=25)
    names=[o['name'] for o in d['result'][:3]]
    print(f"org offset={off} -> n={len(d['result'])} first3={names}")

# organization_show
d = j("action/organization_show", id="noaa-gov")
o=d["result"]
print("\norg_show keys:", sorted(o.keys()))
print("org_show sample:", {k:o.get(k) for k in ("name","title","display_name","package_count","organization_type","created","state","description")})
