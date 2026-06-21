from subsets_utils import get
import time, json
SQL="https://discodata.eea.europa.eu/sql"
def q(query, **p):
    p["query"]=query; return get(SQL, params=p, timeout=(10,180)).json()
T="[StatisticalData].[latest].[eea_s_wat009]"  # 880 rows, no blob, flagship SDG-style
for wait in [90, 60, 60]:
    print(f"sleeping {wait}s..."); time.sleep(wait)
    j=q(f"SELECT * FROM {T}", nrOfHits=2000, p=0)
    if "errors" in j:
        print("  still:", j["errors"])
    else:
        rs=j["results"]; print("  OK rows", len(rs), "cols", list(rs[0].keys()))
        print("  row0", rs[0]); break
