from subsets_utils import get
import json

# 1. SDG Series/Data shape + pagination
r = get("https://unstats.un.org/SDGAPI/v1/sdg/Series/Data",
        params={"seriesCode": "SI_POV_DAY1", "pageSize": 5, "page": 1}, timeout=(10,120))
d = r.json()
print("SDG keys:", list(d.keys()))
for k in ("size","totalElements","totalPages","pageNumber","page"):
    print("  ", k, "=", d.get(k))
obs = d.get("data", [])
print("SDG sample obs keys:", sorted(obs[0].keys()) if obs else "NONE")
print("SDG sample obs:", json.dumps(obs[0], default=str)[:600] if obs else "")
