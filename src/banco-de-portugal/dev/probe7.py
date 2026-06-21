import json, math
from subsets_utils import get
BASE="https://bpstat.bportugal.pt/data/v1"
ds="08ea9a8e70896fd8c1fd3b99d71c7dc4"  # 917 series
url=f"{BASE}/domains/3/datasets/{ds}/?lang=EN"
# page 1 with explicit page_size
r=get(url, params={"page":1,"page_size":1000}, timeout=(10,120))
print("page_size=1000 status",r.status_code)
print("pagination headers:", {k:v for k,v in r.headers.items() if 'page' in k.lower() or 'count' in k.lower() or 'link' in k.lower() or 'throttle' in k.lower()})
d=r.json()
print("size:", d["size"], "prod_nondate:", math.prod(d["size"][:-1]))
print("ext series count:", len(d["extension"]["series"]))
print("value entries:", len(d["value"]))
print("link keys:", list(d.get("link",{}).keys()) if "link" in d else "no link")
# try huge page_size
r2=get(url, params={"page":1,"page_size":5000}, timeout=(10,120))
d2=r2.json()
print("\npage_size=5000: ext series", len(d2["extension"]["series"]), "nondate prod", math.prod(d2["size"][:-1]), "value entries", len(d2["value"]))
