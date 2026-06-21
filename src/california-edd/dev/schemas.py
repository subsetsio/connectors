import json
from subsets_utils import get

BASE = "https://data.ca.gov/api/3"
EIDS = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/california-edd/work/entity_union.json"))

def j(action, **params):
    r = get(f"{BASE}/action/{action}", params=params, timeout=(10, 120))
    r.raise_for_status()
    return r.json()["result"]

out = {}
for eid in EIDS:
    pkg = j("package_show", id=eid)
    title = pkg["title"]
    csvres = [r for r in pkg["resources"] if (r.get("format") or "").upper() == "CSV"]
    fields = None
    rid = None
    for r in csvres:
        try:
            ds = j("datastore_search", resource_id=r["id"], limit=0)
            fields = [(f["id"], f["type"]) for f in ds["fields"] if f["id"] != "_id"]
            rid = r["id"]
            break
        except Exception as e:
            continue
    out[eid] = {"title": title, "n_csv": len(csvres), "fields": fields}
    print(f"\n## {eid}  {title}  ({len(csvres)} csv)")
    if fields:
        for fid, ftype in fields:
            print(f"   {ftype:12} {fid}")
    else:
        print("   <no datastore fields>")
