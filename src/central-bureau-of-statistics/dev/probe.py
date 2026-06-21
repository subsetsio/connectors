import json
from subsets_utils import get

def show(label, url, **params):
    print("\n===== ", label, "=====")
    print("URL:", url, params)
    r = get(url, params=params, timeout=(10, 120))
    print("status:", r.status_code, "ctype:", r.headers.get("content-type"))
    try:
        j = r.json()
    except Exception as e:
        print("non-json:", e, r.text[:300])
        return None
    print(json.dumps(j, ensure_ascii=False)[:2500])
    return j

# 1. Series catalog level 1 (subjects)
l1 = show("series catalog L1", "https://apis.cbs.gov.il/series/catalog/level", id=1, lang="en", format="json")
if l1:
    cats = l1.get("catalogs", {}).get("catalog", [])
    print("\nL1 count:", len(cats))
    print("L1 first record keys:", list(cats[0].keys()) if cats else None)
    print("L1 first record:", cats[0] if cats else None)

# 2. Descend - try level 5 for one subject to get leaf series
l5 = show("series catalog L5 subject=12", "https://apis.cbs.gov.il/series/catalog/level",
          id=5, subject=12, lang="en", format="json", pagesize=5)
if l5:
    print("\nL5 keys:", list(l5.keys()))
    cats = l5.get("catalogs", {}).get("catalog", [])
    print("L5 catalog count this page:", len(cats))
    print("L5 first leaf:", cats[0] if cats else None)
    print("paging:", l5.get("paging"))

# 3. Data for a single series
d = show("series data 3763", "https://apis.cbs.gov.il/series/data/list",
         id=3763, last=3, format="json", lang="en")
if d:
    print("\ndata top keys:", list(d.keys()))
