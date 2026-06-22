import json
from subsets_utils import get

BASE = "https://api.boffsaopendata.fi/v4"


def show(label, obj):
    print(f"\n===== {label} =====")
    print(json.dumps(obj, indent=1, ensure_ascii=False)[:2000])


# 1. series shape for a small dataset
r = get(f"{BASE}/series/BOF_BKN1_PUBL", params={"pageSize": 9999}, timeout=(10, 120))
j = r.json()
print("series keys:", list(j.keys()), "totalCount", j["totalCount"], "totalPages", j["totalPages"], "items", len(j["items"]))
show("series item[0]", j["items"][0])

names = [it["name"] for it in j["items"]]
print("\nseries names sample:", names[:3])

# 2. observations batched (semicolon) with pageSize
batch = ";".join(names[:5])
r2 = get(f"{BASE}/observations/BOF_BKN1_PUBL", params={"seriesName": batch, "pageSize": 9999}, timeout=(10, 120))
j2 = r2.json()
print("\nobs keys:", list(j2.keys()), "totalCount", j2["totalCount"], "totalPages", j2["totalPages"], "items", len(j2["items"]))
show("obs item[0]", {k: (v if k != "observations" else v[:3]) for k, v in j2["items"][0].items()})
print("obs count for item0:", len(j2["items"][0]["observations"]))

# 3. check a value can be null? scan
nulls = 0
for it in j2["items"]:
    for o in it["observations"]:
        if o.get("value") is None:
            nulls += 1
print("null values in sample:", nulls)
