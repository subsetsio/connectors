from subsets_utils import get
BASE = "https://api.unhcr.org/population/v1/"
# no year filter, full breakdown, big page
r = get(BASE+"population/", params={"limit":20000,"page":1,"coo_all":"true","coa_all":"true","cf_type":"ISO"}, timeout=(10,180))
d = r.json()
yrs = sorted({i["year"] for i in d["items"]})
print("population no-year maxPages@20000:", d.get("maxPages"), "page1 rows:", len(d["items"]), "year span sample:", yrs[0], "..", yrs[-1])
# unrwa span
r2 = get(BASE+"unrwa/", params={"limit":20000,"page":1,"coo_all":"true","coa_all":"true","cf_type":"ISO"}, timeout=(10,180))
d2=r2.json(); yrs2=sorted({i["year"] for i in d2["items"]})
print("unrwa maxPages:", d2.get("maxPages"), "rows:", len(d2["items"]), "years:", yrs2[0],"..",yrs2[-1])
