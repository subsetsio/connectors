from subsets_utils import get
import time, json
SQL="https://discodata.eea.europa.eu/sql"
def q(query, **p):
    p["query"]=query; return get(SQL, params=p, timeout=(10,180)).json()
def show(label,j):
    print(label, ("ERROR "+str(j["errors"])) if "errors" in j else f"rows {len(j.get('results',[]))}")
T="[StatisticalData].[latest].[eea_s_wat009]"
print("count:", q(f"SELECT COUNT(*) AS n FROM {T}"))
time.sleep(1)
for size in [5, 1000, 50000, 200000]:
    show(f"nrOfHits={size}", q(f"SELECT * FROM {T}", nrOfHits=size, p=0)); time.sleep(1)
a=q(f"SELECT * FROM {T}", nrOfHits=20, p=0).get("results",[]); time.sleep(1)
b=q(f"SELECT * FROM {T}", nrOfHits=20, p=1).get("results",[])
if a:
    ka=[json.dumps(r,sort_keys=True) for r in a]; kb=set(json.dumps(r,sort_keys=True) for r in b)
    print("page0",len(a),"page1",len(b),"overlap",len(set(ka)&kb))
    print("cols:", list(a[0].keys()))
    print("row0:", a[0])
