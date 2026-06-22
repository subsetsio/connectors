import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from subsets_utils import get

BASE = "https://unstats.un.org/SDGAPI/v1/sdg"

s = get(f"{BASE}/Series/List", timeout=(10,120)).json()
print("Series/List type:", type(s).__name__, "len:", len(s))
print("series sample:", json.dumps(s[0], indent=2)[:600])

d = get(f"{BASE}/Series/Data", params={"seriesCode": s[0]["code"], "pageSize": 3, "page": 1}, timeout=(10,120)).json()
print("\nData top-level keys:", list(d.keys()))
for k in ("size","totalElements","totalPages","pageNumber"):
    print(f"  {k}:", d.get(k))
print("  attributes:", json.dumps(d.get("attributes"))[:200])
print("  dimensions:", json.dumps(d.get("dimensions"))[:200])
print("\none data record:", json.dumps(d["data"][0], indent=2)[:1500])
