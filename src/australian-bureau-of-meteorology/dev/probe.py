import json
import time
from subsets_utils import get

BASE = "http://www.bom.gov.au/waterdata/services"


def kiwis(request, timeout=120, **params):
    q = {"service": "kisters", "type": "QueryServices", "request": request,
         "datasource": "0", "format": "json"}
    q.update(params)
    t = time.time()
    r = get(BASE, params=q, timeout=(10.0, float(timeout)))
    r.raise_for_status()
    print(f"  [{request}] {r.status_code} in {time.time()-t:.1f}s, {len(r.content)} bytes")
    return r.json()


def head(payload, n=5):
    if isinstance(payload, list):
        print("  header:", payload[0] if payload else None)
        for row in payload[1:1+n]:
            print("   row:", row)
        print("  total rows (incl header):", len(payload))


print("== getParameterTypeList ==")
p = kiwis("getParameterTypeList", returnfields="parametertype_id,parametertype_name,parametertype_unitname,parametertype_shortunitname")
head(p, 20)

print("\n== getStationList (count) ==")
s = kiwis("getStationList", returnfields="station_no,station_id,station_name,station_latitude,station_longitude")
print("  station count:", len(s) - 1)
head(s, 3)

print("\n== getTimeseriesList for one station 410713 (all ts_name values) ==")
ts = kiwis("getTimeseriesList", station_no="410713",
           returnfields="ts_id,ts_name,ts_unitname,station_no,station_name,parametertype_name,coverage")
head(ts, 60)

print("\n== getTimeseriesList filtered by ts_name=DMQaQc.Merged.DailyMean.09HR for Water Course Discharge ==")
try:
    ts2 = kiwis("getTimeseriesList", parametertype_name="Water Course Discharge",
                ts_name="DMQaQc.Merged.DailyMean.09HR",
                returnfields="ts_id,ts_name,station_no,parametertype_name,coverage", timeout=180)
    print("  discharge daily-mean series count:", len(ts2) - 1)
    head(ts2, 3)
    sample_ts_id = ts2[1][ts2[0].index("ts_id")] if len(ts2) > 1 else None
except Exception as e:
    print("  ERROR:", type(e).__name__, e)
    sample_ts_id = None

print("\n== getTimeseriesValues for one ts_id ==")
if sample_ts_id:
    v = kiwis("getTimeseriesValues", ts_id=sample_ts_id,
              **{"from": "2010-01-01", "to": "2010-12-31"})
    print("  type:", type(v))
    print(json.dumps(v, indent=2)[:1500])
