"""Local smoke test: fetch 2 regions, build the parquet batch the node would
write, then run the actual transform SQL through DuckDB. No production raw I/O."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import duckdb
import pyarrow as pa
from nodes.statcounter import (
    _get_text, _parse_timeseries_csv, _parse_resolution_csv,
    _TIMESERIES_SCHEMA, BASE_URL, _timeseries_sql, _RESOLUTION_SQL,
)

# --- timeseries (browser) for ww + GB ---
rows = []
for rc in ["ww", "GB"]:
    txt = _get_text(BASE_URL, {
        "statType_hidden": "browser", "region_hidden": rc, "granularity": "monthly",
        "csv": "1", "device_hidden": "desktop+tablet+mobile", "multi-device": "true",
        "fromMonthYear": "2009-01", "toMonthYear": "2026-06",
    })
    lr = _parse_timeseries_csv(txt)
    for d, c, v in lr:
        rows.append({"date": d, "region_code": rc, "region_name": rc,
                     "region_type": "worldwide" if rc == "ww" else "country",
                     "category": c, "market_share": v})
print("timeseries rows:", len(rows))
t = pa.Table.from_pylist(rows, schema=_TIMESERIES_SCHEMA)
con = duckdb.connect()
con.register("statcounter-browser", t)
sql = _timeseries_sql("statcounter-browser")
out = con.execute(sql).fetch_arrow_table()
print("transform rows:", out.num_rows, "cols:", out.column_names)
dup = con.execute(
    f"SELECT count(*) - count(DISTINCT (date, region_code, category)) FROM ({sql})"
).fetchone()[0]
print("duplicate (date,region,category) keys:", dup)
print("sample:", con.execute(
    f"SELECT date, region_code, category, market_share FROM ({sql}) ORDER BY date DESC, market_share DESC LIMIT 3"
).fetchall())

# --- resolution ww 2015 ---
txt = _get_text(BASE_URL, {
    "statType_hidden": "resolution", "region_hidden": "ww", "granularity": "yearly",
    "csv": "1", "device_hidden": "desktop+tablet+mobile", "multi-device": "true",
    "fromYear": "2015", "toYear": "2015",
})
pairs = _parse_resolution_csv(txt)
import pyarrow as pa
from nodes.statcounter import _RESOLUTION_SCHEMA
rt = pa.table({
    "year": [2015]*len(pairs), "region_code": ["ww"]*len(pairs),
    "region_name": ["Worldwide"]*len(pairs), "region_type": ["worldwide"]*len(pairs),
    "resolution": [r for r,_ in pairs], "market_share": [v for _,v in pairs],
}, schema=_RESOLUTION_SCHEMA)
con.register("statcounter-screen-resolution", rt)
rout = con.execute(_RESOLUTION_SQL).fetch_arrow_table()
print("resolution transform rows:", rout.num_rows, "cols:", rout.column_names)
print(rout.slice(0, 3).to_pylist())
