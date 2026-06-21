from subsets_utils import get
BASE = "https://api.uktradeinfo.com"

def j(path, **params):
    return get(f"{BASE}/{path}", params=params, timeout=(10,120)).json()

# Date dimension: shape + count
d = j("Date", **{"$top": 3})
print("Date sample:", d["value"][:3])
print("Date count:", get(f"{BASE}/Date/$count", timeout=(10,120)).text.strip())

# Min/max MonthId in OTS and RTS
for ent in ["OTS","RTS","Trade","Import","Export"]:
    lo = j(ent, **{"$orderby":"MonthId asc","$top":1,"$select":"MonthId"})["value"]
    hi = j(ent, **{"$orderby":"MonthId desc","$top":1,"$select":"MonthId"})["value"]
    print(f"{ent} MonthId: {lo} .. {hi}")

# YearlyTrade year range
lo = j("YearlyTrade", **{"$orderby":"Year asc","$top":1,"$select":"Year"})["value"]
hi = j("YearlyTrade", **{"$orderby":"Year desc","$top":1,"$select":"Year"})["value"]
print("YearlyTrade Year:", lo, "..", hi)

# How big is one month of OTS? (gauge per-batch memory)
c = get(f"{BASE}/OTS/$count", params={"$filter":"MonthId eq 202401"}, timeout=(10,120)).text.strip()
print("OTS rows for 202401:", c)
c = get(f"{BASE}/Trade/$count", params={"$filter":"MonthId eq 202401"}, timeout=(10,120)).text.strip()
print("Trade rows for 202401:", c)

# Does nextLink appear on a full default page (no $top)? fetch first page of a busy month
r = j("OTS", **{"$filter":"MonthId eq 202401"})
print("OTS busy-month page rows:", len(r["value"]), "nextLink?", "@odata.nextLink" in r)
if "@odata.nextLink" in r:
    print("nextLink:", r["@odata.nextLink"][:160])
