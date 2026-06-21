import json
from subsets_utils import get
coll = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/ksh/assets/collect/entities/current.json"))
bad=[]
for rid,e in coll.items():
    sm=e["source_metadata"]; fmt=sm["data_format"]; did=sm["dataset_id"]
    r=get(f"https://data.ksh.hu/datasets/{did}/data/{rid}.{fmt}", timeout=60)
    ct=r.headers.get("content-type","")
    ok = r.status_code==200 and "text/html" not in ct
    flag="" if ok else "  <-- BAD"
    if not ok:
        bad.append((rid,fmt,did))
        # try the other format
        other = "xml" if fmt=="csv" else "csv"
        r2=get(f"https://data.ksh.hu/datasets/{did}/data/{rid}.{other}", timeout=60)
        print(rid[:8], "advertised",fmt, r.status_code, ct[:25], "| other",other,"->",r2.status_code, r2.headers.get("content-type","")[:20], flag)
    # else: silent ok
print("\nBAD count:", len(bad))
