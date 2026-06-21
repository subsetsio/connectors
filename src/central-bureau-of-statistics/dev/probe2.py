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
        print("non-json:", e, r.text[:400])
        return None
    print(json.dumps(j, ensure_ascii=False)[:2000])
    return j

# data/path with the path of series 3763 = [2,1,1,1,2]
show("data/path query", "https://apis.cbs.gov.il/series/data/path",
     id="2,1,1,1,2", last=2, format="json", lang="en")
show("data/path subject form", "https://apis.cbs.gov.il/series/data/path",
     subject="2,1,1,1,2", last=2, format="json", lang="en")

# Try a catalog leaf path [12,2,1,1,1323] via data/path
show("data/path leaf 12,2,1,1,1323", "https://apis.cbs.gov.il/series/data/path",
     id="12,2,1,1,1323", last=2, format="json", lang="en")

# catalog/path - maybe returns series ids
show("catalog/path subject=2", "https://apis.cbs.gov.il/series/catalog/path",
     id=5, subject=2, lang="en", format="json", pagesize=3)

# multi-id data/list
show("data/list multi id", "https://apis.cbs.gov.il/series/data/list",
     id="3763,3764", last=1, format="json", lang="en")
