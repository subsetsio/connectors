import json
from subsets_utils import get
BASE = "https://api.waterdata.usgs.gov/ogcapi/v0"

def show(coll, params):
    r = get(f"{BASE}/collections/{coll}/items", params=params, timeout=(10,180))
    j = r.json()
    print(f"--- {coll} params={params} status={r.status_code}")
    print("    numberMatched:", j.get("numberMatched"), "numberReturned:", j.get("numberReturned"))
    links = j.get("links",[])
    for l in links:
        if l.get("rel") in ("next","prev"):
            print("    link", l.get("rel"), "->", l.get("href")[:160])
    return j

# count support
show("peaks", {"f":"json","limit":1})
# try a small page and see next link / offset
show("daily", {"f":"json","limit":2})
# sortby support
try:
    show("daily", {"f":"json","limit":2,"sortby":"time"})
except Exception as e:
    print("sortby time err", e)
# datetime filter
try:
    show("daily", {"f":"json","limit":2,"datetime":"2024-01-01T00:00:00Z/2024-01-02T00:00:00Z"})
except Exception as e:
    print("datetime err", e)
# monitoring_location_id filter on daily
try:
    show("daily", {"f":"json","limit":2,"monitoring_location_id":"USGS-01646500"})
except Exception as e:
    print("ml filter err", e)
