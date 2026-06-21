import json
from subsets_utils import get

BASE = "https://www.climatewatchdata.org/api/v1/data"

for ep in ["historical_emissions", "ndc_content", "net_zero_content"]:
    print("=" * 60)
    print(ep)
    # page 1, small limit, see envelope + pagination behavior
    r = get(f"{BASE}/{ep}", params={"limit": 5, "page": 1}, timeout=(10, 120))
    print("status", r.status_code, "headers-of-interest:",
          {k: r.headers.get(k) for k in ("link", "total", "x-total", "per-page", "total-count")})
    d = r.json()
    print("top keys:", list(d.keys()))
    data = d.get("data", [])
    print("n in page:", len(data))
    if data:
        rec = data[0]
        print("record keys:", list(rec.keys()))
        # show value types
        for k, v in rec.items():
            if isinstance(v, list):
                print(f"   {k}: list len {len(v)} sample {v[:2]}")
            else:
                print(f"   {k}: {type(v).__name__} = {repr(v)[:60]}")
    # check page 2 differs & whether out-of-range returns empty
    r2 = get(f"{BASE}/{ep}", params={"limit": 5, "page": 2}, timeout=(10, 120))
    d2 = r2.json()
    ids1 = [x.get("id") for x in data]
    ids2 = [x.get("id") for x in d2.get("data", [])]
    print("page2 n:", len(d2.get("data", [])), "ids overlap with p1:", set(ids1) & set(ids2))
    # huge page out of range
    r3 = get(f"{BASE}/{ep}", params={"limit": 5, "page": 100000}, timeout=(10, 120))
    print("page 100000 n:", len(r3.json().get("data", [])))
