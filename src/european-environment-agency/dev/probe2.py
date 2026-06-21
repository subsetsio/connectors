from subsets_utils import get
import time
SQL="https://discodata.eea.europa.eu/sql"
def q(query, **p):
    p["query"]=query
    r=get(SQL, params=p, timeout=(10,180))
    return r.json()
def show(label, j):
    if "errors" in j: print(label, "ERROR", j["errors"])
    else: print(label, "rows", len(j.get("results",[])))

for size in [100, 1000, 10000, 50000, 100000, 200000]:
    time.sleep(2)
    j=q("SELECT * FROM [AirQualityDataFlows].[latest].[Models]", nrOfHits=size, p=0)
    show(f"nrOfHits={size} p=0", j)

# repeat p=0 small a few times to see if error was transient
for i in range(3):
    time.sleep(2)
    j=q("SELECT * FROM [AirQualityDataFlows].[latest].[Models]", nrOfHits=10, p=0)
    show(f"retry p=0 #{i}", j)

# does pagination need order? check overlap between consecutive pages
time.sleep(2)
p0=q("SELECT * FROM [AirQualityDataFlows].[latest].[Models]", nrOfHits=10, p=0).get("results",[])
time.sleep(2)
p1=q("SELECT * FROM [AirQualityDataFlows].[latest].[Models]", nrOfHits=10, p=1).get("results",[])
# pick a likely id col
if p0 and p1:
    k=list(p0[0].keys())[0]
    s0={r[k] for r in p0}; s1={r[k] for r in p1}
    print("page0/1 first-col overlap:", len(s0&s1), "k=",k)
