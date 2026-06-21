"""bom stations: the climate station catalogue (stations_db.txt).

Joinable reference data, parsed from the fixed-layout stations_db.txt table.
Small enough to re-pull in full every run — stateless full re-pull (shape 1).
"""

import re

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import ftp_retrieve

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


DOWNLOAD_SPECS = [
    NodeSpec(id="bom-stations", fn=fetch_stations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="bom-stations-transform",
        deps=["bom-stations"],
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
