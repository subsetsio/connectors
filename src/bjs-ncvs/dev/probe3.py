from subsets_utils import get
BASE="https://api.ojp.gov/bjsdataset/v1"
r=get(f"{BASE}/gcuy-rt5g.json", params={"$limit":2,"$offset":0,"$order":":id"}, timeout=(10,120))
print("order :id status", r.status_code, "rows", len(r.json()))
