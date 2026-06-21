from subsets_utils import get
import time, json
SQL="https://discodata.eea.europa.eu/sql"
def q(query, **p):
    p["query"]=query
    return get(SQL, params=p, timeout=(10,180)).json()
def show(label,j):
    print(label, ("ERROR "+str(j["errors"])) if "errors" in j else f"rows {len(j.get('results',[]))}")
j=q("SELECT COUNT(*) AS n FROM [WISE_BWD].[latest].[BWD_Status]")
print("BWD_Status count:", j)
time.sleep(1)
for size in [5, 1000, 50000, 100000]:
    show(f"nrOfHits={size}", q("SELECT * FROM [WISE_BWD].[latest].[BWD_Status]", nrOfHits=size, p=0))
    time.sleep(1)
a=q("SELECT * FROM [WISE_BWD].[latest].[BWD_Status]", nrOfHits=50, p=0).get("results",[])
time.sleep(1)
b=q("SELECT * FROM [WISE_BWD].[latest].[BWD_Status]", nrOfHits=50, p=1).get("results",[])
if a and b:
    ka=[json.dumps(r,sort_keys=True) for r in a]; kb=set(json.dumps(r,sort_keys=True) for r in b)
    print("page0",len(a),"page1",len(b),"overlap",len(set(ka)&kb))
    print("cols:", list(a[0].keys()))
