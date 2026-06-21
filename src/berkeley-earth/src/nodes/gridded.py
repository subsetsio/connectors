"""Berkeley Earth gridded-temperature subset — monthly equal-area anomaly fields.

Land TAVG and land+ocean fields are parsed from NetCDF and unpivoted to one row
per (cell, month). The EqualArea grid is the area-weighted publication grid
(5,498 land cells / 15,984 land+ocean cells), far more compact than the 1-degree
LatLong1 grids. Files are overwritten in place on each ~monthly release with
stable filenames, so we re-pull the full corpus every run (~170MB of NetCDF).
"""
from __future__ import annotations

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer

from utils import BASE_S3, fetch_bytes

# --------------------------------------------------------------------------- #
# Sources
# --------------------------------------------------------------------------- #
# Equal-area gridded NetCDF products (Global/Gridded/<file>): (filename, surface).
GRIDDED_PRODUCTS = (
    ("Complete_TAVG_EqualArea.nc", "land"),
    ("Land_and_Ocean_EqualArea.nc", "land_ocean"),
)

# --------------------------------------------------------------------------- #
# Schema
# --------------------------------------------------------------------------- #
SCHEMA_GRID = pa.schema([
    ("surface", pa.string()),             # land | land_ocean
    ("year", pa.int16()),
    ("month", pa.int8()),
    ("latitude", pa.float32()),
    ("longitude", pa.float32()),
    ("temperature_anomaly", pa.float32()),    # vs Jan 1951-Dec 1980 baseline (C)
    ("temperature_absolute", pa.float32()),   # anomaly + monthly climatology (C)
])

# --------------------------------------------------------------------------- #
# NetCDF parsing
# --------------------------------------------------------------------------- #
_GRID_BATCH_SLICES = 100  # time-slices buffered per parquet record batch


def _decode_time(frac: float) -> tuple[int, int]:
    """Fractional 'year A.D.' (month center) -> (year, month 1-12)."""
    import math
    year = int(math.floor(frac))
    month = int(round((frac - year) * 12 + 0.5))
    return year, min(12, max(1, month))


def _flush_grid(writer, surface: str, buf: list) -> None:
    import numpy as np
    lat = np.concatenate([b[2] for b in buf])
    lon = np.concatenate([b[3] for b in buf])
    anom = np.concatenate([b[4] for b in buf])
    absolute = np.concatenate([b[5] for b in buf])
    years = np.concatenate(
        [np.full(b[2].shape[0], b[0], dtype=np.int16) for b in buf])
    months = np.concatenate(
        [np.full(b[2].shape[0], b[1], dtype=np.int8) for b in buf])
    n = lat.shape[0]
    batch = pa.record_batch({
        "surface": pa.array([surface] * n, type=pa.string()),
        "year": pa.array(years, type=pa.int16()),
        "month": pa.array(months, type=pa.int8()),
        "latitude": pa.array(lat, type=pa.float32()),
        "longitude": pa.array(lon, type=pa.float32()),
        "temperature_anomaly": pa.array(anom, type=pa.float32()),
        "temperature_absolute": pa.array(absolute, type=pa.float32()),
    }, schema=SCHEMA_GRID)
    writer.write_batch(batch)


# --------------------------------------------------------------------------- #
# Download
# --------------------------------------------------------------------------- #
def fetch_gridded(node_id: str) -> None:
    """Parse equal-area NetCDF anomaly fields and stream the long form to parquet."""
    import netCDF4 as nc
    import numpy as np

    asset = node_id
    wrote = False
    with raw_parquet_writer(asset, SCHEMA_GRID) as writer:
        for fname, surface in GRIDDED_PRODUCTS:
            content = fetch_bytes(BASE_S3 + "Global/Gridded/" + fname)
            ds = nc.Dataset("inmem", memory=content)
            try:
                lat = np.asarray(ds.variables["latitude"][:], dtype=np.float32)
                lon = np.asarray(ds.variables["longitude"][:], dtype=np.float32)
                times = np.asarray(ds.variables["time"][:], dtype=np.float64)
                clim = np.asarray(ds.variables["climatology"][:], dtype=np.float32)
                temp = ds.variables["temperature"]  # (ntime, npts), read lazily

                buf: list = []
                for ti in range(times.shape[0]):
                    year, month = _decode_time(float(times[ti]))
                    row = np.asarray(temp[ti, :], dtype=np.float32)
                    valid = ~np.isnan(row)
                    if not valid.any():
                        continue
                    anom = row[valid]
                    absolute = anom + clim[month - 1][valid]
                    buf.append((year, month, lat[valid], lon[valid], anom, absolute))
                    if len(buf) >= _GRID_BATCH_SLICES:
                        _flush_grid(writer, surface, buf)
                        wrote = True
                        buf = []
                if buf:
                    _flush_grid(writer, surface, buf)
                    wrote = True
            finally:
                ds.close()

    if not wrote:
        raise RuntimeError("gridded-temperature: no rows written")


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(
        id="berkeley-earth-gridded-temperature",
        fn=fetch_gridded,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="berkeley-earth-gridded-temperature-transform",
        deps=["berkeley-earth-gridded-temperature"],
        sql='''
            SELECT
                surface,
                make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
                CAST(year AS INTEGER)  AS year,
                CAST(month AS INTEGER) AS month,
                latitude,
                longitude,
                temperature_anomaly,
                temperature_absolute
            FROM "berkeley-earth-gridded-temperature"
            WHERE temperature_anomaly IS NOT NULL
              AND NOT isnan(temperature_anomaly)
        ''',
    ),
]
