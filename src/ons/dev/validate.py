from subsets_utils import get
import json, re

ids = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/ons/work/entity_union.json"))
no_csv, errs = [], []
fmt = {"v4":0, "obs":0, "other":0}
for i, did in enumerate(ids):
    try:
        d = get(f"https://api.beta.ons.gov.uk/v1/datasets/{did}", timeout=(10,60)).json()
        lv = d.get("links",{}).get("latest_version",{}).get("href")
        if not lv:
            errs.append((did,"no latest_version")); continue
        v = get(lv, timeout=(10,60)).json()
        csv = v.get("downloads",{}).get("csv",{}).get("href")
        if not csv:
            no_csv.append((did, list(v.get("downloads",{}).keys()))); continue
    except Exception as e:
        errs.append((did, f"{type(e).__name__}:{e}"))
print("checked", len(ids))
print("no_csv:", no_csv)
print("errs:", errs)
