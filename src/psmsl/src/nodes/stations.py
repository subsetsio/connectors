"""PSMSL station reference catalog (from filelist.txt).

The Metric product covers the broadest station set; its filelist is the superset
joinable to every value feed.
"""

import zipfile

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import MET_MONTHLY_ZIP, download_zip

_STATIONS_SCHEMA = pa.schema(
    [
        ("station_id", pa.int32()),
        ("latitude", pa.float64()),
        ("longitude", pa.float64()),
        ("station_name", pa.string()),
        ("coastline_code", pa.string()),
        ("station_code", pa.string()),
        ("documentation_flag", pa.string()),
    ]
)


def _parse_filelist(zf: zipfile.ZipFile) -> list[dict]:
    name = next(n for n in zf.namelist() if n.endswith("filelist.txt"))
    rows = []
    for line in zf.read(name).decode("latin-1").splitlines():
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(";")]
        rows.append(
            {
                "station_id": int(parts[0]),
                "latitude": float(parts[1]),
                "longitude": float(parts[2]),
                "station_name": parts[3],
                "coastline_code": parts[4] or None,
                "station_code": parts[5] or None,
                "documentation_flag": parts[6] if len(parts) > 6 else None,
            }
        )
    return rows


def fetch_stations(node_id: str) -> None:
    asset = node_id
    zf = download_zip(MET_MONTHLY_ZIP)
    rows = _parse_filelist(zf)
    table = pa.Table.from_pylist(rows, schema=_STATIONS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="psmsl-stations", fn=fetch_stations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="psmsl-stations-transform",
        deps=["psmsl-stations"],
        sql="""
            SELECT
                station_id,
                station_name,
                latitude,
                longitude,
                coastline_code,
                station_code,
                documentation_flag
            FROM "psmsl-stations"
        """,
    ),
]
