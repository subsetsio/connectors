from subsets_utils import get
import json

# 1. small cube CSV
def show(url, label, n=1200):
    r = get(url, timeout=(10,120))
    print(f"=== {label} status={r.status_code} ctype={r.headers.get('content-type')} len={len(r.content)}")
    txt = r.text
    print(txt[:n])
    print("---")
    return r

# small cube: as1001rs (3 dims: year, indicator, gender)
show("https://data.statistics.sk/api/v2/dataset/as1001rs/all/all/all?lang=en&type=csv", "as1001rs CSV all/all/all")

# json-stat version to see structure + size
r = get("https://data.statistics.sk/api/v2/dataset/as1001rs/all/all/all?lang=en", timeout=(10,120))
d = r.json()
print("jsonstat keys:", list(d.keys()))
print("class:", d.get("class"), "id:", d.get("id"), "size:", d.get("size"))
import math
print("total cells:", math.prod(d.get("size",[1])))
print("value type sample:", type(d.get("value")), (d.get("value")[:5] if isinstance(d.get("value"),list) else list(d.get("value").items())[:5] if isinstance(d.get("value"),dict) else None))
