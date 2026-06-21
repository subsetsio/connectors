import json
from subsets_utils import get
ids = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/fcc/work/entity_union.json"))
if isinstance(ids, dict):
    ids = list(ids.keys())
print("n entities", len(ids))
tot=0
for rid in ids:
    try:
        c=get(f"https://opendata.fcc.gov/resource/{rid}.json", params={"$select":"count(*)"}, timeout=(10,120)).json()
        n=int(c[0]["count"]); tot+=n
        print(f"{rid}\t{n}")
    except Exception as e:
        print(f"{rid}\tERR {type(e).__name__} {e}")
print("TOTAL", tot)
