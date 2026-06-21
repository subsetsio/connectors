import json
from subsets_utils import get

BASE = "https://api.seaaroundus.org/api/v1"

def gj(url):
    r = get(url, timeout=(10, 120))
    print(f"\n=== {url} :: HTTP {r.status_code} :: {len(r.content)} bytes")
    return r.json()

# eez list structure
j = gj(f"{BASE}/eez/")
print("top keys:", list(j.keys()))
print("meta:", json.dumps(j.get("meta"))[:300])
data = j["data"]
print("data type:", type(data).__name__)
if isinstance(data, dict):
    print("data keys:", list(data.keys()))
    for k, v in data.items():
        print(f"  {k}: {type(v).__name__}", (f"len {len(v)}" if hasattr(v, '__len__') else ""))
        if isinstance(v, list) and v:
            print("    sample[0]:", json.dumps(v[0])[:300] if not isinstance(v[0], dict) else {kk: str(v[0][kk])[:40] for kk in list(v[0])[:8]})
