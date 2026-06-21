from subsets_utils import get
BASE = "https://api.uktradeinfo.com"

# What does the orderby+select error look like?
r = get(f"{BASE}/OTS", params={"$orderby":"MonthId asc","$top":1,"$select":"MonthId"}, timeout=(10,120))
print("orderby+select:", r.status_code, repr(r.text[:300]))

# orderby alone?
r = get(f"{BASE}/OTS", params={"$orderby":"MonthId desc","$top":1}, timeout=(10,120))
print("orderby alone:", r.status_code, repr(r.text[:200]))

# Date max MonthId (sorted)
r = get(f"{BASE}/Date", params={"$orderby":"MonthId desc","$top":1}, timeout=(10,120))
print("Date max:", r.status_code, r.text[:200])

# per-month filter + count
for ent, mid in [("OTS",202401),("Trade",202401),("Import",202401),("Export",202401),("RTS",202401)]:
    c = get(f"{BASE}/{ent}/$count", params={"$filter":f"MonthId eq {mid}"}, timeout=(10,120)).text.strip().lstrip("﻿")
    print(f"{ent} {mid} count:", c)

# busy month page: rows + nextLink
r = get(f"{BASE}/OTS", params={"$filter":"MonthId eq 202401"}, timeout=(30,180)).json()
print("OTS 202401 page rows:", len(r["value"]), "nextLink?", "@odata.nextLink" in r)
if "@odata.nextLink" in r:
    print("nextLink:", r["@odata.nextLink"][:200])
