from subsets_utils import get
import json
data = get("https://data.nber.org/cycles/business_cycle_dates.json", timeout=(10,60)).json()
print("n", len(data))
print("first", data[0])
print("last", data[-1])
print("empty_peaks", sum(1 for d in data if not (d.get("peak") or "").strip()))
