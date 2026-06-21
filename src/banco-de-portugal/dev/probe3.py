import json
from subsets_utils import get
BASE="https://bpstat.bportugal.pt/data/v1"

# Try to find openapi spec
for u in ["https://bpstat.bportugal.pt/data/openapi.json","https://bpstat.bportugal.pt/data/v1/openapi.json","https://bpstat.bportugal.pt/data/docs/openapi.json","https://bpstat.bportugal.pt/data/v1/swagger.json","https://bpstat.bportugal.pt/data/schema"]:
    try:
        r=get(u, timeout=(10,60))
        print(u, r.status_code, r.headers.get("content-type"), len(r.content))
    except Exception as e:
        print(u,"ERR",str(e)[:80])

# Does dataset endpoint list ALL series? check 'series' endpoint under dataset
ds="08ea9a8e70896fd8c1fd3b99d71c7dc4"
for u in [f"{BASE}/domains/3/datasets/{ds}/series/?lang=EN",
          f"{BASE}/datasets/{ds}/series/?lang=EN",
          f"{BASE}/domains/3/datasets/{ds}/?lang=EN&series_ids=all"]:
    try:
        r=get(u, timeout=(10,60))
        print("\n",u, r.status_code, len(r.content))
        if r.status_code==200:
            print(r.text[:300])
    except Exception as e:
        print(u,"ERR",str(e)[:80])
