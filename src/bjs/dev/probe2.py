from subsets_utils import get

BASE = "https://api.ojp.gov/bjsdataset/v1/"

def g(rid, params):
    r = get(f"{BASE}{rid}.json", params=params, timeout=(10.0, 180.0))
    return r

# test :id ordering for stable offset paging
r = g("r32q-bdaw", {"$order": ":id", "$limit": 3})
print(":id order status", r.status_code, "ctype", r.headers.get("content-type"))
print("body head:", r.text[:200])
print("---")

# test offset
r = g("r32q-bdaw", {"$order": ":id", "$limit": 2, "$offset": 9446})
print("offset near-end status", r.status_code, "n rows", len(r.json()))
print("---")

# test big limit page count for a large dataset
import time
t=time.time()
r = g("uy37-xgmh", {"$order": ":id", "$limit": 50000})
print("uy37 50000 page: status", r.status_code, "rows", len(r.json()), "secs", round(time.time()-t,1), "bytes", len(r.content))
