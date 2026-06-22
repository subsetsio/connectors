import json
import time
from subsets_utils import get

BASE = "http://www.bom.gov.au/waterdata/services"


def kiwis(request, timeout=240, **params):
    q = {"service": "kisters", "type": "QueryServices", "request": request,
         "datasource": "0", "format": "json"}
    q.update(params)
    t = time.time()
    r = get(BASE, params=q, timeout=(10.0, float(timeout)))
    r.raise_for_status()
    return r.json(), time.time() - t


# Grab a handful of discharge daily-mean ts_ids
tsl, _ = kiwis("getTimeseriesList", parametertype_name="Water Course Discharge",
               ts_name="DMQaQc.Merged.DailyMean.24HR", returnfields="ts_id,station_no")
ids = [r[0] for r in tsl[1:][:10]]
print("sample ts_ids:", ids)

print("\n== multi ts_id getTimeseriesValues (10 ids, full coverage via from/to) ==")
payload, dt = kiwis("getTimeseriesValues", ts_id=",".join(ids),
                    **{"from": "2020-01-01", "to": "2020-12-31"})
print(f"  returned {len(payload)} series blocks in {dt:.1f}s")
for blk in payload[:3]:
    print(f"   ts_id={blk.get('ts_id')} rows={blk.get('rows')} columns={blk.get('columns')} "
          f"first={blk.get('data')[:1] if blk.get('data') else []}")

print("\n== full coverage (no from/to) for ONE long series — does it return whole history? ==")
payload2, dt2 = kiwis("getTimeseriesValues", ts_id=ids[0])
blk = payload2[0]
print(f"  ts_id={blk.get('ts_id')} rows={blk.get('rows')} in {dt2:.1f}s; "
      f"first={blk.get('data')[:1]} last={blk.get('data')[-1:] if blk.get('data') else []}")

print("\n== try a big batch: 250 ids ==")
tsl2, _ = kiwis("getTimeseriesList", parametertype_name="Ground Water Level",
                ts_name="DMQaQc.Merged.DailyMean.24HR", returnfields="ts_id")
big = [r[0] for r in tsl2[1:][:250]]
try:
    p3, dt3 = kiwis("getTimeseriesValues", ts_id=",".join(big),
                    **{"from": "2023-01-01", "to": "2023-12-31"})
    total = sum(int(b.get("rows", 0) or 0) for b in p3)
    print(f"  250-id batch: {len(p3)} blocks, {total} total rows, in {dt3:.1f}s, "
          f"~{len(json.dumps(p3))/1e6:.1f}MB json")
except Exception as e:
    print("  ERROR:", type(e).__name__, str(e)[:160])

print("\n== getTimeseriesValues with returnfields incl Quality Code ==")
try:
    p4, _ = kiwis("getTimeseriesValues", ts_id=ids[0],
                  returnfields="Timestamp,Value,Quality Code",
                  **{"from": "2020-01-01", "to": "2020-01-10"})
    print("  columns:", p4[0].get("columns"), "first rows:", p4[0].get("data")[:2])
except Exception as e:
    print("  ERROR:", type(e).__name__, str(e)[:160])
