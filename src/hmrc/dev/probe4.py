import time
from subsets_utils import get
BASE = "https://api.uktradeinfo.com"

def slow_get(url, **params):
    time.sleep(1.5)  # throttle to avoid burst 403
    return get(url, params=params, timeout=(30,180))

# $select alone allowed?
r = slow_get(f"{BASE}/OTS", **{"$select":"MonthId,Value","$top":2})
print("select alone:", r.status_code, r.text[:120])

# Filtered busy month: first page rows + nextLink
r = slow_get(f"{BASE}/OTS", **{"$filter":"MonthId eq 202401"})
try:
    d = r.json()
    print("OTS 202401 page1 rows:", len(d["value"]), "nextLink?", "@odata.nextLink" in d)
    nl = d.get("@odata.nextLink")
    print("nextLink:", nl)
    if nl:
        # follow nextLink (absolute or relative?)
        url2 = nl if nl.startswith("http") else f"{BASE}/{nl}"
        time.sleep(1.5)
        r2 = get(url2, timeout=(30,180))
        d2 = r2.json()
        print("page2 rows:", len(d2["value"]), "nextLink?", "@odata.nextLink" in d2)
except Exception as e:
    print("ERR:", r.status_code, repr(r.text[:200]))

# manual $skip pagination (fallback if nextLink absent)
r = slow_get(f"{BASE}/OTS", **{"$filter":"MonthId eq 202401","$top":40000,"$skip":40000})
try:
    d = r.json()
    print("skip40000 rows:", len(d["value"]))
except Exception:
    print("skip ERR:", r.status_code, r.text[:150])
