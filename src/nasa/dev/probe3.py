from subsets_utils import get
import json
for ep in ["sentry.api","nhats.api"]:
    print("\n=== "+ep+" ===")
    r=get("https://ssd-api.jpl.nasa.gov/"+ep, timeout=(20,180))
    d=r.json()
    print("top keys", list(d.keys()))
    data=d.get("data")
    print("data type", type(data).__name__, "len", len(data) if isinstance(data,list) else "?")
    if isinstance(data,list) and data:
        e0=data[0]
        print("elem type", type(e0).__name__)
        if isinstance(e0,dict):
            print("elem keys", list(e0.keys()))
            print("elem sample", json.dumps(e0)[:400])
        else:
            print("elem", e0)
    # any other top-level descriptive
    for k in ("signature","count"): print(k, d.get(k))
