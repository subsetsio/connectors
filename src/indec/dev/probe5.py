from subsets_utils import get
import json
SERIES="https://apis.datos.gob.ar/series/api/series/"
ids=["1.1_OGP_D_1993_A_17","2.3_DGE_1993_A_26"]
# metadata=full to see per-id ordering in meta
r=get(SERIES,params={"ids":",".join(ids),"format":"json","limit":2,"metadata":"full"},timeout=(10,60))
d=r.json()
print("meta len:",len(d["meta"]))
for m in d["meta"]:
    if "field" in m: print(" field.id:",m["field"]["id"])
    else: print(" (catalog block)", list(m.keys()))
print("data[0]:",d["data"][0])
# pagination check: limit + start
r2=get(SERIES,params={"ids":ids[0],"format":"json","limit":3,"start":0},timeout=(10,60))
r3=get(SERIES,params={"ids":ids[0],"format":"json","limit":3,"start":3},timeout=(10,60))
print("page0:",r2.json()["data"])
print("page1:",r3.json()["data"])
# bogus id behaviour
rb=get(SERIES,params={"ids":"NOT_A_REAL_ID","format":"json"},timeout=(10,60))
print("bogus status:",rb.status_code, rb.text[:160])
