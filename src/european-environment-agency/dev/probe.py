from subsets_utils import get
import json, time

SQL="https://discodata.eea.europa.eu/sql"
def q(query, **p):
    p["query"]=query
    r=get(SQL, params=p, timeout=(10,120))
    return r

# small table full
r=q("SELECT * FROM [AirQualityDataFlows].[latest].[Models]", nrOfHits=5, p=0)
print("status", r.status_code, "ct", r.headers.get("content-type"))
j=r.json()
print("top keys:", list(j.keys()))
res=j.get("results",[])
print("rows:", len(res))
if res: print("row0 keys:", list(res[0].keys())[:12]); print("row0 sample:", {k:res[0][k] for k in list(res[0].keys())[:4]})

# large nrOfHits behavior on a small table
r2=q("SELECT * FROM [AirQualityDataFlows].[latest].[Models]", nrOfHits=1000000, p=0)
print("large nrOfHits rows:", len(r2.json().get("results",[])))

# page beyond end
r3=q("SELECT * FROM [AirQualityDataFlows].[latest].[Models]", nrOfHits=5, p=999)
print("page 999 rows:", len(r3.json().get("results",[])))

# count to know size
r4=q("SELECT COUNT(*) AS n FROM [AirQualityDataFlows].[latest].[Models]")
print("Models count:", r4.json())

# error shape (bad table)
r5=q("SELECT * FROM [Nope].[latest].[Nope]", nrOfHits=1, p=0)
print("bad table status", r5.status_code, "body", str(r5.text)[:200])
