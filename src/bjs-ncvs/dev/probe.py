from subsets_utils import get
import json
BASE="https://api.ojp.gov/bjsdataset/v1"
for rid in ["gcuy-rt5g","r4j4-fdwx","gkck-euys","ya4e-n9zp"]:
    r=get(f"{BASE}/{rid}.json", params={"$limit":1}, timeout=(10,120))
    print(rid, r.status_code, "fields=", r.headers.get("X-SODA2-Fields"))
    print("  types=", r.headers.get("X-SODA2-Types"))
# pagination beyond end
r=get(f"{BASE}/gcuy-rt5g.json", params={"$limit":5,"$offset":1_000_000}, timeout=(10,120))
print("beyond-end rows:", len(r.json()))
# sample a row of personal victimization
r=get(f"{BASE}/gcuy-rt5g.json", params={"$limit":1}, timeout=(10,120))
print("sample row:", json.dumps(r.json()[0]))
