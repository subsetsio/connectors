import json
from collections import Counter
from subsets_utils import get

BASE = "https://custom.resbank.co.za/SarbWebApi/WebIndicators"

rel = get(f"{BASE}/ReleaseOfSelectedData", timeout=(10, 120)).json()
print("release groups:", len(rel))
for r in rel:
    print("  ", r.get("DataType"), "|", r.get("Indicator"), "| latest", r.get("LatestDate"))

# Probe a couple of groups for shape, size, date format.
for dt in ["MRGEI", "CDACA"]:
    print("\n=== MonthlyIndicatorsAll/%s ===" % dt)
    resp = get(f"{BASE}/ReleaseOfSelectedData/MonthlyIndicatorsAll/{dt}", timeout=(10, 240))
    data = resp.json()
    print("records:", len(data), "| bytes:", len(resp.content))
    if data:
        rec = data[0]
        print("keys:", sorted(rec.keys()))
        print("sample:", json.dumps(rec))
        print("distinct TimeseriesCode (this group):", len({d.get("TimeseriesCode") for d in data}))
        print("Date samples:", [d.get("Date") for d in data[:5]])
        print("Value types:", Counter(type(d.get("Value")).__name__ for d in data))
        print("UpDown values:", Counter(d.get("UpDown") for d in data[:1000]))
