import json
from subsets_utils import get

BASE = "https://euvdservices.enisa.europa.eu/api"

def fetch(page, size=100):
    r = get(f"{BASE}/search", params={
        "fromScore": 0, "toScore": 10, "fromEpss": 0, "toEpss": 100,
        "page": page, "size": size,
    }, headers={"accept": "application/json"}, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r.json()

d = fetch(0, 100)
print("total:", d["total"], "n:", len(d["items"]))
# field presence / null survey across 100 records
keys = {}
no_products = 0
null_score = 0
empty_vector = 0
for it in d["items"]:
    for k, v in it.items():
        keys.setdefault(k, {"present": 0, "null": 0})
        keys[k]["present"] += 1
        if v is None or v == "":
            keys[k]["null"] += 1
    if not it.get("enisaIdProduct"):
        no_products += 1
    if it.get("baseScore") is None:
        null_score += 1
    if not it.get("baseScoreVector"):
        empty_vector += 1
print("field presence/null over 100 rows:")
for k, c in keys.items():
    print(f"  {k}: present={c['present']} null/empty={c['null']}")
print("rows with no products:", no_products)
print("rows with null baseScore:", null_score)
print("rows with empty baseScoreVector:", empty_vector)

# deep page near the end and beyond
total = d["total"]
last_page = total // 100
print("\nlast_page approx:", last_page)
dl = fetch(last_page, 100)
print("page", last_page, "n items:", len(dl["items"]))
dbeyond = fetch(last_page + 5, 100)
print("page", last_page + 5, "n items:", len(dbeyond["items"]))
# sample id format at deep page
if dl["items"]:
    print("sample ids deep:", [it["id"] for it in dl["items"][:3]])
