import json
from subsets_utils import get

def hit(label, url, **params):
    print("\n===== ", label, "=====", url, params)
    r = get(url, params=params, timeout=(10, 180))
    print("status:", r.status_code, "ctype:", r.headers.get("content-type"))
    try:
        return r.json()
    except Exception as e:
        print("non-json:", e, r.text[:300]); return None

# Does data/path?id=<subject> return all series under the subject?
j = hit("data/path subject=2 page1 small", "https://apis.cbs.gov.il/series/data/path",
        id=2, last=1, format="json", lang="en", pagesize=5)
if j:
    ds = j["DataSet"]
    print("paging:", ds["paging"].get("total_items"), "last_page:", ds["paging"].get("last_page"),
          "page_size:", ds["paging"].get("page_size"))
    print("n series this page:", len(ds["Series"]))

# Try big page size for values on a subject
j = hit("data/path subject=2 pagesize=1000 full obs", "https://apis.cbs.gov.il/series/data/path",
        id=2, format="json", lang="en", pagesize=1000)
if j:
    ds = j["DataSet"]
    print("VALUES total_items:", ds["paging"].get("total_items"), "last_page:", ds["paging"].get("last_page"),
          "page_size:", ds["paging"].get("page_size"))
    s0 = ds["Series"][0]
    print("series0 id:", s0["id"], "n_obs:", len(s0["obs"]), "first obs:", s0["obs"][0] if s0["obs"] else None)
    tot_obs = sum(len(s["obs"]) for s in ds["Series"])
    print("total obs on this page of", len(ds["Series"]), "series:", tot_obs)

# ---- PRICE API ----
j = hit("price catalog", "https://api.cbs.gov.il/index/catalog/catalog", lang="en", format="json")
if j:
    print("price catalog top type:", type(j), "keys:" , list(j.keys()) if isinstance(j, dict) else None)
    print(json.dumps(j, ensure_ascii=False)[:1500])

j = hit("price data CPI 120010", "https://api.cbs.gov.il/index/data/price",
        id=120010, startPeriod="01-2024", endPeriod="12-2024", format="json", lang="en")
if j:
    print(json.dumps(j, ensure_ascii=False)[:1800])
