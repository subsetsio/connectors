"""Validate the transform SQL + fetch/parse logic on a tiny slice (no save_raw)."""
import sys
sys.path.insert(0, "src")
sys.path.insert(0, "src/nodes")

import duckdb
import pyarrow as pa

import australian_bureau_of_meteorology as M

# --- tiny fetches ------------------------------------------------------------
print("fetch stations sample...")
sp = M._kiwis("getStationList",
              returnfields="station_no,station_id,station_name,station_latitude,station_longitude",
              read_timeout=240.0)
sh, sd = M._table(sp)
sidx = {n: sh.index(n) for n in sh}
st_rows = [{
    "station_no": r[sidx["station_no"]], "station_id": r[sidx["station_id"]],
    "station_name": r[sidx["station_name"]],
    "latitude": M._to_float(r[sidx["station_latitude"]]),
    "longitude": M._to_float(r[sidx["station_longitude"]]),
} for r in sd[:2000]]
stations = pa.Table.from_pylist(st_rows, schema=M.STATIONS_SCHEMA)
print("  stations sample rows:", stations.num_rows)

print("fetch timeseries (Water Course Discharge canonical)...")
ts = M._canonical_series("Water Course Discharge", "DMQaQc.Merged.DailyMean.24HR")[:200]
timeseries = pa.Table.from_pylist(ts, schema=M.TIMESERIES_SCHEMA)
print("  timeseries sample rows:", timeseries.num_rows)

print("fetch values for first chunk window...")
ids = [m["ts_id"] for m in ts[:M.SERIES_PER_CALL]]
from datetime import date
vrows = M._fetch_window(ids, date(2015, 1, 1), date(2016, 3, 1))
values = pa.Table.from_pylist(vrows, schema=M.VALUES_SCHEMA)
print("  values sample rows:", values.num_rows)

# --- run the transform SQL ---------------------------------------------------
con = duckdb.connect()
con.register("australian-bureau-of-meteorology-stations", stations)
con.register("australian-bureau-of-meteorology-timeseries", timeseries)
con.register("australian-bureau-of-meteorology-values", values)

for spec in M.TRANSFORM_SPECS:
    out = con.execute(spec.sql).fetch_arrow_table()
    name = spec.id.replace("-transform", "").replace("australian-bureau-of-meteorology-", "")
    print(f"\n[{name}] -> {out.num_rows} rows; columns: {out.column_names}")
    print(out.slice(0, 3).to_pylist())
