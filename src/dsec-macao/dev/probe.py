from subsets_utils import get, post
import json

# 1) batching: multiple indicator_ids, wide year range, all periods
body = {
    "indicator_ids": ["9029", "9031", "9020"],  # mixed: yearly-only and yearly+monthly
    "language": "en-us",
    "types": ["VAL"],
    "dataPeriods": ["Yearly", "Quarterly", "Monthly", "ThreeConsecutiveMonths"],
    "fromYear": 1980,
    "toYear": 2026,
}
r = post("https://www.dsec.gov.mo/TimeSeriesApi/App/IndicatorValue/LatestSameEndPeriodv3",
         json=body, timeout=(10, 120))
print("HTTP", r.status_code)
d = r.json()
print("Status:", d["Status"], "Debug:", (d.get("Debug_msg") or "")[:120])
v = d["Value"]
print("num indicators returned:", len(v))
for ind in v:
    rows = ind["dsecIndicatorData"]
    periods = sorted(set((row.get("type"), row.get("PeriodID")) for row in rows))
    yrs = sorted(set(row["Year"] for row in rows))
    print(f"  id={ind['indicatorId']} rows={len(rows)} year_range={yrs[0] if yrs else None}-{yrs[-1] if yrs else None} sample_row={rows[0] if rows else None}")
