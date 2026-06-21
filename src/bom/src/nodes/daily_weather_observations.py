"""bom daily-weather-observations: the full Daily Weather Observations corpus.

Product IDCKWCDEA0, pulled as the single bulk archive IDCKWCDEA0.tgz (~60MB,
~104k per-station/per-month CSVs) and reshaped into one long-format table — one
row per (station, date) with the shared daily variables.

Small enough to re-pull in full every run, so this is a stateless full re-pull
(shape 1) — no watermark, no cursor. The corpus is a rolling window (~2016 to
current month), so a fresh full snapshot each refresh also picks up any
revisions for free.
"""

import csv as csvmod
import datetime
import io
import re
import tarfile

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer
from utils import ftp_retrieve

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


DOWNLOAD_SPECS = [
    NodeSpec(id="bom-daily-weather-observations", fn=fetch_observations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="bom-daily-weather-observations-transform",
        deps=["bom-daily-weather-observations"],
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
]
