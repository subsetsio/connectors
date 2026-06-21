import sys
sys.path.insert(0, "src")
from nodes.apartment_list import _discover_csv_url, _download_csv, _WIDE, _SUMMARY, _MONTH_COL, _float, _dims
import datetime as dt

# 1) discovery for a small product
url = _discover_csv_url("Apartment List Time On Market", "Apartment_List_Time_On_Market_")
print("discovered:", url[:90], "...")
rows = _download_csv(url)
print("tom rows:", len(rows), "first dims:", {k:rows[0][k] for k in ("location_name","location_type")})
mcols=[c for c in rows[0] if _MONTH_COL.match(c)]
print("month cols:", len(mcols), mcols[0], mcols[-1])
# melt count
n=sum(1 for r in rows for c in mcols if _float(r.get(c)) is not None)
print("tom melted valued rows:", n)

# 2) summary discovery
surl=_discover_csv_url("Apartment List Rent Estimates Summary","Apartment_List_Rent_Estimates_Summary_")
srows=_download_csv(surl)
print("summary rows:", len(srows), "cols:", list(srows[0].keys())[:6], "...")
print("summary sample:", {k:srows[0][k] for k in ("year","month","price_overall","rent_change_yoy")})
