from subsets_utils import get
import time, json
SQL="https://discodata.eea.europa.eu/sql"
def q(query, **p):
    p["query"]=query; return get(SQL, params=p, timeout=(10,180)).json()
# minimal load, single tiny query
j=q("SELECT TOP 3 * FROM [StatisticalData].[latest].[eea_s_wat009]")
print("tiny SELECT:", json.dumps(j)[:300])
