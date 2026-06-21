import duckdb
import pyarrow as pa
import sys
sys.path.insert(0, "src")
from nodes import nsidc as N

# Parse without writing to production raw.
daily = []
for path, hemi in N._DAILY_FILES:
    daily.extend(N._parse_daily(N._download_csv(path), hemi))
dt = pa.Table.from_pylist(daily, schema=N._DAILY_SCHEMA)
print("daily rows", len(dt), dt.schema)

monthly = []
for path, hemi in N._MONTHLY_FILES:
    monthly.extend(N._parse_monthly(N._download_csv(path), hemi))
mt = pa.Table.from_pylist(monthly, schema=N._MONTHLY_SCHEMA)
print("monthly rows", len(mt))

clim = []
for path, hemi in N._CLIMATOLOGY_FILES:
    clim.extend(N._parse_climatology(N._download_csv(path), hemi))
ct = pa.Table.from_pylist(clim, schema=N._CLIMATOLOGY_SCHEMA)
print("clim rows", len(ct))

con = duckdb.connect()
con.register("nsidc-sea-ice-extent-daily", dt)
con.register("nsidc-sea-ice-extent-monthly", mt)
con.register("nsidc-sea-ice-extent-daily-climatology", ct)
for spec in N.TRANSFORM_SPECS:
    res = con.execute(spec.sql).arrow()
    print("===", spec.id, "->", len(res), "rows")
    print(res.schema)
    print(res.slice(0, 2).to_pylist())
    print("...tail", res.slice(len(res) - 2, 2).to_pylist())
    # duplicate key check
    if "monthly" in spec.id or ("daily" in spec.id and "climatology" not in spec.id):
        d = con.execute(f"SELECT date, hemisphere, count(*) c FROM ({spec.sql}) GROUP BY 1,2 HAVING c>1").arrow()
        print("dup keys:", len(d))
    if "climatology" in spec.id:
        d = con.execute(f"SELECT day_of_year, hemisphere, count(*) c FROM ({spec.sql}) GROUP BY 1,2 HAVING c>1").arrow()
        print("dup keys:", len(d))
