import json
import time
from subsets_utils import get

BASE = "http://www.bom.gov.au/waterdata/services"


def kiwis(request, timeout=300, **params):
    q = {"service": "kisters", "type": "QueryServices", "request": request,
         "datasource": "0", "format": "json"}
    q.update(params)
    t = time.time()
    r = get(BASE, params=q, timeout=(10.0, float(timeout)))
    r.raise_for_status()
    return r.json(), time.time() - t


tsl, _ = kiwis("getTimeseriesList", parametertype_name="Ground Water Level",
               ts_name="DMQaQc.Merged.DailyMean.24HR", returnfields="ts_id,coverage")
hdr = tsl[0]; fi = hdr.index("from")
withcov = [r for r in tsl[1:] if r[fi]]
ids = [r[0] for r in withcov[:250]]
print(f"picked {len(ids)} ground-water series with coverage")

for label, frm in [("wide 1900", "1900-01-01"), ("recent 2024", "2024-01-01")]:
    payload, dt = kiwis("getTimeseriesValues", ts_id=",".join(ids),
                        **{"from": frm, "to": "2026-12-31"})
    rows_per = [int(b.get("rows", 0) or 0) for b in payload]
    total = sum(rows_per)
    print(f"\n[{label}] {len(payload)} blocks, {total} rows in {dt:.1f}s, "
          f"~{len(json.dumps(payload))/1e6:.2f}MB; max={max(rows_per)} "
          f"top5={sorted(rows_per, reverse=True)[:5]}")
