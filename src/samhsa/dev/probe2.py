import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
from collections import Counter

def fetch_state(sid, page=1, ps=2000):
    r = get("https://findtreatment.gov/locator/exportsAsJson/v2",
            params={"sAddr":'"39.5,-98.35"',"limitType":0,"limitValue":sid,"sType":"both","pageSize":ps,"page":page},
            timeout=(10,120))
    return r.json()

for sid in (5, 18, 44):
    d = fetch_state(sid)
    rows = d["rows"]
    states = Counter(r["state"] for r in rows)
    print(f"stateId={sid} recordCount={d['recordCount']} totalPages={d['totalPages']} returned={len(rows)} distinct_states={dict(states)}")

# check pagination: does page beyond totalPages return empty?
d = fetch_state(5, page=1, ps=2000)
print("state5 ps2000 page1 returned", len(d["rows"]), "totalPages", d["totalPages"])
# stable-ish key check: any duplicate (name1,street1,city,zip)?
keys = [(r["name1"],r["street1"],r["city"],r["zip"]) for r in d["rows"]]
print("rows", len(keys), "distinct (name,street,city,zip)", len(set(keys)))
# typeFacility shape
print("typeFacility sample:", d["rows"][0].get("typeFacility"))
