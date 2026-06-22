import sys
sys.path.insert(0,'src')
from subsets_utils import get
BASE="https://data.iadb.org/api/3/action"
rid="ba412771-9c90-4613-a96a-e18c005c0ab6"
# test datastore_search_sql keyset
import json
sql=f'SELECT * FROM "{rid}" WHERE _id > 0 ORDER BY _id LIMIT 3'
r=get(f"{BASE}/datastore_search_sql", params={"sql": sql}, timeout=60)
j=r.json()
print("sql success:", j.get("success"), "status", r.status_code, flush=True)
if j.get("success"):
    recs=j["result"]["records"]
    print("got", len(recs), "max_id", max(int(x["_id"]) for x in recs), flush=True)
else:
    print("error:", str(j.get("error"))[:200], flush=True)
