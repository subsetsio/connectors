import json
from subsets_utils import get

BASE="https://bpstat.bportugal.pt/data/v1"

# 1) Can we fetch a dataset WITHOUT knowing its domain? try a bogus domain id
ds="08ea9a8e70896fd8c1fd3b99d71c7dc4"  # 917 series, domain 3
for dom in [3, 999, 0]:
    try:
        r=get(f"{BASE}/domains/{dom}/datasets/{ds}/?lang=EN", timeout=(10,120))
        print(f"domain {dom}: status {r.status_code}, len {len(r.content)}")
    except Exception as e:
        print(f"domain {dom}: ERR {e}")

# 2) inspect structure of the small dataset
ds_small="05e2845d5d567afd88b699a91b0c20b8"
r=get(f"{BASE}/domains/3/datasets/{ds_small}/?lang=EN", timeout=(10,120))
d=r.json()
print("\n=== SMALL dataset keys:", list(d.keys()))
print("id:",d.get("id"))
print("size:",d.get("size"))
print("value type:", type(d.get("value")), "len:", len(d["value"]) if d.get("value") is not None else None)
print("value sample:", d["value"][:5] if isinstance(d.get("value"),list) else list(d["value"].items())[:5])
print("dimension keys:", list(d.get("dimension",{}).keys()) if "dimension" in d else "NO dimension")
ext=d.get("extension",{})
print("extension keys:", list(ext.keys()))
print("series[0]:", json.dumps(ext.get("series",[{}])[0])[:600])
