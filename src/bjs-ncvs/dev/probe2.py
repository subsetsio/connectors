from subsets_utils import get
import json
BASE="https://api.ojp.gov/bjsdataset/v1"
r=get(f"{BASE}/gcuy-rt5g.json", params={"$select":"offtracenew, count(*) as n","$group":"offtracenew"}, timeout=(10,120))
print("offtracenew distinct:", r.json())
# check max year present
r=get(f"{BASE}/gcuy-rt5g.json", params={"$select":"max(year) as my, min(year) as ny"}, timeout=(10,120))
print("year range:", r.json())
