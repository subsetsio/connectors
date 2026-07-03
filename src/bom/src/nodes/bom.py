"""bom node module — Australian Bureau of Meteorology, anonymous FTP.

Two subsets, both stateless full re-pulls (shape 1) from the Bureau's sanctioned
anonymous-FTP channel (ftp.bom.gov.au); the www HTTP site blocks programmatic
access. Both corpora are small enough to re-pull in full every refresh, which
also picks up any revisions for free.

- daily-weather-observations: the whole Daily Weather Observations corpus
  (product IDCKWCDEA0), pulled as the single bulk archive IDCKWCDEA0.tgz (~60MB,
  ~104k per-station/per-month CSVs) and reshaped into one long-format table —
  one row per (station, date) with the shared daily variables.
- stations: the climate station catalogue (stations_db.txt), parsed from its
  fixed layout into joinable reference data.
"""

import csv as csvmod
import datetime
import io
import re
import tarfile

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer, save_raw_parquet
from utils import ftp_retrieve

# --------------------------------------------------------------------------- #
# daily-weather-observations
# --------------------------------------------------------------------------- #

DWO_TGZ_PATH = "/anon/gen/clim_data/IDCKWCDEA0.tgz"

# Flush a row group roughly every this many parsed rows (bounded memory).
BATCH_ROWS = 250_000

_DATE_RE = re.compile(r"^\d{2}/\d{2}/\d{4}$")

DWO_SCHEMA = pa.schema(
    [
        ("state", pa.string()),
        ("station_slug", pa.string()),
        ("station_name", pa.string()),
        ("date", pa.date32()),
        ("evapotranspiration_mm", pa.float64()),
        ("rainfall_mm", pa.float64()),
        ("pan_evaporation_mm", pa.float64()),
        ("max_temp_c", pa.float64()),
        ("min_temp_c", pa.float64()),
        ("max_relative_humidity_pct", pa.float64()),
        ("min_relative_humidity_pct", pa.float64()),
        ("wind_speed_ms", pa.float64()),
        ("solar_radiation_mj_m2", pa.float64()),
    ]
)

# data columns in each CSV (after the station name + date):
#   evapotranspiration, rain, pan evaporation, max temp, min temp,
#   max RH, min RH, 10m wind speed, solar radiation
_NUM_FIELDS = [
    "evapotranspiration_mm",
    "rainfall_mm",
    "pan_evaporation_mm",
    "max_temp_c",
    "min_temp_c",
    "max_relative_humidity_pct",
    "min_relative_humidity_pct",
    "wind_speed_ms",
    "solar_radiation_mj_m2",
]


def _num(s: str):
    s = s.strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _new_buffers() -> dict:
    return {f.name: [] for f in DWO_SCHEMA}


def _to_batch(cols: dict) -> pa.RecordBatch:
    arrays = [pa.array(cols[f.name], type=f.type) for f in DWO_SCHEMA]
    return pa.record_batch(arrays, schema=DWO_SCHEMA)


def fetch_observations(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    data = ftp_retrieve(DWO_TGZ_PATH)

    cols = _new_buffers()
    pending = 0
    with raw_parquet_writer(asset, DWO_SCHEMA) as writer:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
            for member in tf:
                if not member.isfile() or not member.name.endswith(".csv"):
                    continue
                # tables/<state>/<station_slug>/<station_slug>-<YYYYMM>.csv
                parts = member.name.split("/")
                if len(parts) < 4:
                    continue
                state, slug = parts[1], parts[2]
                fobj = tf.extractfile(member)
                if fobj is None:
                    continue
                text = fobj.read().decode("latin-1")
                for row in csvmod.reader(text.splitlines()):
                    if len(row) < 11 or not _DATE_RE.match(row[1].strip()):
                        continue
                    dd, mm, yy = row[1].strip().split("/")
                    cols["state"].append(state)
                    cols["station_slug"].append(slug)
                    cols["station_name"].append(row[0].strip())
                    cols["date"].append(datetime.date(int(yy), int(mm), int(dd)))
                    for i, name in enumerate(_NUM_FIELDS, start=2):
                        cols[name].append(_num(row[i]))
                    pending += 1
                    if pending >= BATCH_ROWS:
                        writer.write_batch(_to_batch(cols))
                        cols = _new_buffers()
                        pending = 0
        if pending:
            writer.write_batch(_to_batch(cols))


# --------------------------------------------------------------------------- #
# stations
# --------------------------------------------------------------------------- #

STATIONS_DB_PATH = "/anon/gen/clim_data/IDCKWCDEA0/tables/stations_db.txt"

# stations_db.txt fixed layout: id, state, district, name, open-date-range, lat, lon
_STATION_RE = re.compile(
    r"^(\S+)\s+(\S+)\s+(\S+)\s+(.+?)\s+(\d{8})\.\.(\d{0,8})\s+"
    r"(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*$"
)

STATIONS_SCHEMA = pa.schema(
    [
        ("bom_station_id", pa.string()),
        ("state", pa.string()),
        ("district_code", pa.string()),
        ("station_name", pa.string()),
        ("open_date", pa.string()),
        ("close_date", pa.string()),
        ("latitude", pa.float64()),
        ("longitude", pa.float64()),
    ]
)


def fetch_stations(node_id: str) -> None:
    asset = node_id
    text = ftp_retrieve(STATIONS_DB_PATH).decode("latin-1")
    rows = {name: [] for name in STATIONS_SCHEMA.names}
    for line in text.splitlines():
        if not line.strip():
            continue
        m = _STATION_RE.match(line)
        if not m:
            raise ValueError(f"unparseable stations_db row: {line!r}")
        sid, state, district, name, open_d, close_d, lat, lon = m.groups()
        rows["bom_station_id"].append(sid)
        rows["state"].append(state)
        rows["district_code"].append(district)
        rows["station_name"].append(name.strip())
        rows["open_date"].append(open_d or None)
        rows["close_date"].append(close_d or None)
        rows["latitude"].append(float(lat))
        rows["longitude"].append(float(lon))
    table = pa.table(
        {n: pa.array(rows[n], type=STATIONS_SCHEMA.field(n).type) for n in STATIONS_SCHEMA.names},
        schema=STATIONS_SCHEMA,
    )
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# specs
# --------------------------------------------------------------------------- #

DOWNLOAD_SPECS = [
    NodeSpec(id="bom-daily-weather-observations", fn=fetch_observations, kind="download"),
    NodeSpec(id="bom-stations", fn=fetch_stations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="bom-daily-weather-observations-transform",
        deps=["bom-daily-weather-observations"],
        key=("station_slug", "date"),
        temporal="date",
        sql='''
            SELECT
                state,
                station_slug,
                station_name,
                CAST(date AS DATE)              AS date,
                evapotranspiration_mm,
                rainfall_mm,
                pan_evaporation_mm,
                max_temp_c,
                min_temp_c,
                max_relative_humidity_pct,
                min_relative_humidity_pct,
                wind_speed_ms,
                solar_radiation_mj_m2
            FROM "bom-daily-weather-observations"
            WHERE date IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY station_slug, date ORDER BY station_name
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="bom-stations-transform",
        deps=["bom-stations"],
        key=("bom_station_id",),
        sql='''
            SELECT
                bom_station_id,
                state,
                district_code,
                station_name,
                open_date,
                close_date,
                CAST(latitude  AS DOUBLE) AS latitude,
                CAST(longitude AS DOUBLE) AS longitude
            FROM "bom-stations"
            WHERE bom_station_id IS NOT NULL
        ''',
    ),
]
