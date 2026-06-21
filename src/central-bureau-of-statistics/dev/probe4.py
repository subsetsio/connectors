import json
from subsets_utils import get

def hit(label, url, **params):
    r = get(url, params=params, timeout=(10, 240))
    ct = r.headers.get("content-type")
    print(f"\n== {label} :: status {r.status_code} ct={ct}")
    return r

# All subjects + their series counts (last=1 light) to find the biggest
l1 = get("https://apis.cbs.gov.il/series/catalog/level",
         params=dict(id=1, lang="en", format="json"), timeout=(10,120)).json()
subjects = [c["path"][0] for c in l1["catalogs"]["catalog"]]
print("subjects:", subjects, "n=", len(subjects))
counts = {}
for s in subjects:
    try:
        j = get("https://apis.cbs.gov.il/series/data/path",
                params=dict(id=s, last=1, format="json", lang="en", pagesize=1), timeout=(10,180)).json()
        counts[s] = j["DataSet"]["paging"].get("total_items")
    except Exception as e:
        counts[s] = f"ERR {e}"
print("series counts per subject:", json.dumps(counts))
print("max:", max((v for v in counts.values() if isinstance(v,int)), default=None),
      "total:", sum(v for v in counts.values() if isinstance(v,int)))

# Does data/path paginate? compare Page=1 vs Page=2 first series id for a big subject
big = max(counts, key=lambda k: counts[k] if isinstance(counts[k],int) else -1)
print("\nbiggest subject:", big, counts[big])
for pg in (1, 2):
    j = get("https://apis.cbs.gov.il/series/data/path",
            params={"id": big, "last": 1, "format":"json","lang":"en","pagesize":100,"Page":pg}, timeout=(10,180)).json()
    ser = j["DataSet"]["Series"]
    print(f" Page={pg}: returned {len(ser)} series, first id={ser[0]['id'] if ser else None}, paging.current_page={j['DataSet']['paging'].get('current_page')}")

# ---- PRICE: enumerate index series via price_all (XML) ----
r = hit("price_all chapter=a", "https://api.cbs.gov.il/index/data/price_all", lang="en", chapter="a", download="false")
print(r.text[:1500])
