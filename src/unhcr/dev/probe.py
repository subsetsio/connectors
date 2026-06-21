from subsets_utils import get
BASE = "https://api.unhcr.org/population/v1/"
eps = ["population","asylum-applications","asylum-decisions","demographics","solutions","idmc","unrwa","nowcasting"]
for ep in eps:
    params = {"limit": 2, "page": 1, "coo_all": "true", "coa_all": "true", "cf_type": "ISO", "yearFrom": 2022, "yearTo": 2022}
    if ep == "nowcasting":
        params = {"limit": 2}
    r = get(BASE+ep+"/", params=params, timeout=(10,120))
    d = r.json()
    it = d["items"][0] if d["items"] else {}
    print("===", ep, "maxPages=", d.get("maxPages"))
    for k,v in it.items():
        print(f"   {k}: {type(v).__name__} = {v!r}")
