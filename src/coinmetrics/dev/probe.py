import json
from subsets_utils import get

BASE = "https://community-api.coinmetrics.io/v4"

def jget(path):
    r = get(f"{BASE}/{path}", timeout=(10, 120))
    r.raise_for_status()
    return r.json()

# catalog filtered to btc
d = jget("catalog-v2/asset-metrics?assets=btc")
a = d["data"][0]
metrics = sorted({m["metric"] for m in a["metrics"]
                  for f in m["frequencies"]
                  if f["frequency"] == "1d" and f.get("community")})
print("btc community-1d metrics:", len(metrics))
print(metrics[:30])

# timeseries wide shape with many metrics, full history page1
ts = jget(f"timeseries/asset-metrics?assets=btc&metrics={','.join(metrics)}&frequency=1d&page_size=10000")
rows = ts["data"]
print("\nbtc rows page1:", len(rows), "has_next:", "next_page_url" in ts)
print("earliest:", rows[0]["time"], "latest:", rows[-1]["time"])
print("row key count (asset+time+metrics):", len(rows[0].keys()))
print("sample row keys:", list(rows[0].keys())[:12])
print("sample:", json.dumps(rows[0])[:250])
# does a metric ever come back non-numeric? check value parse
import re
nonnum = set()
for r in rows[:50]:
    for k, v in r.items():
        if k in ("asset", "time"):
            continue
        if v is None:
            continue
        try:
            float(v)
        except (ValueError, TypeError):
            nonnum.add(k)
print("non-numeric metric fields in btc sample:", nonnum)

# test metric-count cap: try a huge metric list (repeat to ~200)
big = (metrics * 20)[:200]
try:
    t2 = jget(f"timeseries/asset-metrics?assets=btc&metrics={','.join(big)}&frequency=1d&page_size=1")
    print("\n200-metric request OK")
except Exception as e:
    print("\n200-metric request failed:", str(e)[:160])

# institution metrics
ic = jget("catalog-v2/institution-metrics")
insts = [i["institution"] for i in ic["data"]]
imetrics = sorted({m["metric"] for m in ic["data"][0]["metrics"]
                   for f in m["frequencies"]
                   if f["frequency"] == "1d"})
print("\ninstitutions:", insts, "metric count:", len(imetrics))
its = jget(f"timeseries/institution-metrics?institutions={insts[0]}&metrics={','.join(imetrics[:50])}&frequency=1d&page_size=3")
print("inst row sample:", json.dumps(its["data"][0])[:250])
