import json
from subsets_utils import get

def show(url, label):
    print(f"\n===== {label} :: {url}")
    r = get(url, timeout=(10,120))
    print("status", r.status_code, "ctype", r.headers.get("content-type"))
    try:
        d = r.json()
    except Exception:
        print("TEXT head:", r.text[:300]); return None
    return d

# 1. STFM dataset endpoint (REPO - nested?)
d = show("https://data.financialresearch.gov/v1/series/dataset/?dataset=REPO", "STFM REPO dataset")
print("top keys:", list(d.keys()) if isinstance(d, dict) else type(d))
ts = d.get("timeseries", {})
print("num series:", len(ts))
k0 = next(iter(ts))
print("series key:", k0)
print("series[0] keys:", list(ts[k0].keys()))
print("series[0] json head:", json.dumps(ts[k0], default=str)[:900])
