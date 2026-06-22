from subsets_utils import get
import json

BASE = "https://community-api.coinmetrics.io/v4"

# 1) catalog-v2/asset-metrics: pagination shape + community daily coverage
r = get(f"{BASE}/catalog-v2/asset-metrics", params={"page_size": 50}, timeout=60).json()
print("catalog-v2 keys:", list(r.keys()))
print("has next_page_url:", "next_page_url" in r)
print("num assets in page:", len(r["data"]))
# build daily community metric set from this page
daily_pairs = 0
metrics_daily = set()
assets_with_daily = set()
for a in r["data"]:
    for m in a.get("metrics", []):
        for fr in m.get("frequencies", []):
            if fr.get("community") and fr["frequency"] == "1d":
                daily_pairs += 1
                metrics_daily.add(m["metric"])
                assets_with_daily.add(a["asset"])
print("daily community (asset,metric) pairs in 50-asset page:", daily_pairs)
print("distinct daily community metrics:", sorted(metrics_daily))
print("assets with daily community in page:", len(assets_with_daily))

# 2) timeseries wide response shape
ts = get(f"{BASE}/timeseries/asset-metrics", params={
    "assets": "btc,eth", "metrics": "PriceUSD,CapMrktEstUSD", "frequency": "1d",
    "page_size": 3}, timeout=60).json()
print("\ntimeseries sample rows:")
print(json.dumps(ts["data"][:3], indent=1))
print("has next_page_token:", "next_page_token" in ts)

# 3) reference-data pagination
rd = get(f"{BASE}/reference-data/asset-metrics", params={"page_size": 2}, timeout=60).json()
print("\nreference-data keys:", list(rd.keys()), "next?", "next_page_url" in rd)
print("ref sample:", json.dumps(rd["data"][0], indent=1)[:600])
