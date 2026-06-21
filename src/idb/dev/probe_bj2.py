import sys
sys.path.insert(0,'src')
from subsets_utils import get
BASE="https://data.iadb.org/api/3/action"
rid="b58cb948-edd5-4004-bb63-d190b74e931e"
j=get(f"{BASE}/datastore_search",params={"resource_id":rid,"limit":2},timeout=60).json()
print("success:", j.get("success"))
r=j.get("result",{})
print("total:", r.get("total"))
print("fields:", [f["id"] for f in r.get("fields",[])])
print("n records:", len(r.get("records",[])))
