from subsets_utils import get
import time, json
SQL="https://discodata.eea.europa.eu/sql"
def q(query, **p):
    p["query"]=query; return get(SQL, params=p, timeout=(10,180)).json()
T="[StatisticalData].[latest].[eea_s_wat009]"
print("count:", q(f"SELECT COUNT(*) AS n FROM {T}")); time.sleep(2)
# single request, large nrOfHits
j=q(f"SELECT * FROM {T}", nrOfHits=100000, p=0)
print("single nrOfHits=100000 rows:", len(j.get("results",[])) if "results" in j else j); time.sleep(2)
# paginate 300
allrows=[]; seen=set(); dup=0
for p in range(10):
    j=q(f"SELECT * FROM {T}", nrOfHits=300, p=p)
    if "errors" in j: print("page",p,"ERR",j["errors"]); break
    rs=j["results"]
    for r in rs:
        h=json.dumps(r,sort_keys=True)
        if h in seen: dup+=1
        seen.add(h)
    allrows+=rs
    print(f"page {p}: {len(rs)} rows")
    if len(rs)<300: break
    time.sleep(1)
print("total fetched:", len(allrows), "unique:", len(seen), "dups:", dup)
