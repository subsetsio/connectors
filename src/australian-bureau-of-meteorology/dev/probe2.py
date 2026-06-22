import time
from collections import Counter
from subsets_utils import get

BASE = "http://www.bom.gov.au/waterdata/services"

PARAMS = [
    "Rainfall", "Ground Water Level", "Water Course Level", "Water Course Discharge",
    "Evaporation", "Water Temperature", "Electrical Conductivity @ 25C", "pH",
    "Turbidity", "Storage Volume", "Storage Level",
]


def kiwis(request, timeout=240, **params):
    q = {"service": "kisters", "type": "QueryServices", "request": request,
         "datasource": "0", "format": "json"}
    q.update(params)
    t = time.time()
    r = get(BASE, params=q, timeout=(10.0, float(timeout)))
    r.raise_for_status()
    dt = time.time() - t
    return r.json(), dt


for p in PARAMS:
    try:
        payload, dt = kiwis("getTimeseriesList", parametertype_name=p,
                            ts_name="DMQaQc.Merged.Daily*",
                            returnfields="ts_id,ts_name")
        if not payload or not isinstance(payload, list) or (isinstance(payload, dict)):
            print(f"{p:32s} -> non-list payload: {str(payload)[:120]}")
            continue
        header = payload[0]
        rows = payload[1:]
        names = Counter(r[header.index("ts_name")] for r in rows)
        print(f"{p:32s} -> {len(rows):6d} daily series in {dt:5.1f}s  ts_names={dict(names)}")
    except Exception as e:
        print(f"{p:32s} -> ERROR {type(e).__name__}: {str(e)[:120]}")
