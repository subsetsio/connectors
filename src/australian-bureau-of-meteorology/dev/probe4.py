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


# Discharge daily-mean series, with coverage so we can pick long-history ones.
tsl, _ = kiwis("getTimeseriesList", parametertype_name="Water Course Discharge",
               ts_name="DMQaQc.Merged.DailyMean.24HR", returnfields="ts_id,coverage")
hdr = tsl[0]
fi, ti = hdr.index("from"), hdr.index("to")
# pick series that have a from date (long history), take 250
withcov = [r for r in tsl[1:] if r[fi]]
ids = [r[0] for r in withcov[:250]]
print(f"picked {len(ids)} discharge series with coverage")

print("\n== 250-id FULL COVERAGE (no from/to) ==")
payload, dt = kiwis("getTimeseriesValues", ts_id=",".join(ids))
rows_per = [int(b.get("rows", 0) or 0) for b in payload]
total = sum(rows_per)
print(f"  {len(payload)} blocks, {total} total rows in {dt:.1f}s, ~{len(json.dumps(payload))/1e6:.1f}MB")
print(f"  rows/series: max={max(rows_per)} min={min(rows_per)} "
      f"n_with_data={sum(1 for x in rows_per if x>0)}")
# Is the max suspiciously round (=> truncation cap)?
print(f"  top 5 row counts: {sorted(rows_per, reverse=True)[:5]}")
# A daily series since ~1960 should have ~20000+ rows. If max is capped low, we hit a limit.
longest = max(payload, key=lambda b: int(b.get("rows", 0) or 0))
print(f"  longest series ts_id={longest['ts_id']} first={longest['data'][:1]} last={longest['data'][-1:]}")
