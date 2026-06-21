import sys; sys.path.insert(0, "src")
import numpy as np, pyarrow as pa
import netCDF4 as nc
from nodes.berkeley_earth import (
    _fetch_text, _fetch_bytes, _parse_trend, _build_ts_table, _decode_time,
    _flush_grid, SCHEMA_GRID, BASE_S3, BASE_AUTO,
)

# 1) timeseries parse: one regional + one global
t = _fetch_text(BASE_AUTO + "Regional/TMAX/Text/france-TMAX-Trend.txt")
cols = _parse_trend(t)
tbl = _build_ts_table({"slug":"france","name":"France","level":"country","variable":"TMAX","surface":"land"}, cols)
print("france TMAX rows:", tbl.num_rows, "yr range", min(cols[0]), max(cols[0]))
g = _fetch_text(BASE_S3 + "Global/Land_and_Ocean_complete.txt")
gt = _build_ts_table({"slug":"global","name":"Global","level":"global","variable":"TAVG","surface":"land_ocean"}, _parse_trend(g))
print("global L+O rows:", gt.num_rows, "schema ok:", gt.schema.equals(tbl.schema))
print("sample row:", {k: gt.column(k)[0].as_py() for k in ("region_slug","variable","surface","year","month","monthly_anomaly","monthly_unc")})
print("nulls in 20yr col:", gt.column("twenty_year_anomaly").null_count, "/", gt.num_rows)

# 2) gridded: first 30 time slices of TAVG EqualArea
content = _fetch_bytes(BASE_S3 + "Global/Gridded/Complete_TAVG_EqualArea.nc")
ds = nc.Dataset("inmem", memory=content)
lat = np.asarray(ds.variables["latitude"][:], dtype=np.float32)
lon = np.asarray(ds.variables["longitude"][:], dtype=np.float32)
times = np.asarray(ds.variables["time"][:], dtype=np.float64)
clim = np.asarray(ds.variables["climatology"][:], dtype=np.float32)
temp = ds.variables["temperature"]
print("decode first:", _decode_time(float(times[0])), "last:", _decode_time(float(times[-1])))
buf=[]
batches=[]
class W:
    def write_batch(self, b): batches.append(b)
for ti in range(30):
    y,m=_decode_time(float(times[ti]))
    row=np.asarray(temp[ti,:],dtype=np.float32); valid=~np.isnan(row)
    if not valid.any(): continue
    anom=row[valid]; absolute=anom+clim[m-1][valid]
    buf.append((y,m,lat[valid],lon[valid],anom,absolute))
_flush_grid(W(), "land", buf)
b=batches[0]
print("grid batch rows:", b.num_rows, "cols:", b.schema.names)
print("lat range:", float(pa.compute.min(b.column("latitude")).as_py()), float(pa.compute.max(b.column("latitude")).as_py()))
print("sample:", {k: b.column(k)[0].as_py() for k in b.schema.names})
