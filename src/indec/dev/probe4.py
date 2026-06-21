from subsets_utils import get
import json

SEARCH="https://apis.datos.gob.ar/series/api/search/"
SERIES="https://apis.datos.gob.ar/series/api/series/"
SRC="Instituto Nacional de Estadística y Censos (INDEC)"

# 1. search pagination shape
r=get(SEARCH,params={"dataset_source":SRC,"limit":3,"start":0},timeout=(10,60))
d=r.json()
print("search count:",d["count"],"keys:",list(d.keys()))
ex=d["data"][0]
print("field keys:",list(ex["field"].keys()))
print("dataset keys:",list(ex["dataset"].keys()))
ids=[x["field"]["id"] for x in d["data"]]
print("sample ids:",ids)

# 2. multi-id /series JSON shape (mixed)
r2=get(SERIES,params={"ids":",".join(ids),"format":"json","limit":5,"metadata":"only"},timeout=(10,60))
print("\nseries meta-only status",r2.status_code)
print(json.dumps(r2.json(),ensure_ascii=False)[:800])

r3=get(SERIES,params={"ids":",".join(ids),"format":"json","limit":4},timeout=(10,60))
d3=r3.json()
print("\nseries data count(periods):",d3["count"])
print("data rows sample:",json.dumps(d3["data"][:3],ensure_ascii=False))
