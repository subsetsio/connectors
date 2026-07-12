"""PSMSL bulk ZIP download nodes."""

import zipfile

import pyarrow as pa

from subsets_utils import NodeSpec, save_raw_parquet
from utils import (
    MET_MONTHLY_ZIP,
    MONTHLY_SCHEMA,
    RLR_ANNUAL_ZIP,
    RLR_MONTHLY_ZIP,
    data_members,
    download_zip,
    parse_monthly,
    parse_value,
)

_ANNUAL_SCHEMA = pa.schema(
    [
        ("station_id", pa.int32()),
        ("year", pa.int32()),
        ("msl_mm", pa.float64()),
        ("missing_flag", pa.string()),
        ("data_flag", pa.string()),
    ]
)

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


def _parse_annual(zf: zipfile.ZipFile, ext: str) -> list[dict]:
    rows = []
    for sid, lines in data_members(zf, ext):
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(";")]
            rows.append(
                {
                    "station_id": sid,
                    "year": int(float(parts[0])),
                    "msl_mm": parse_value(parts[1]),
                    "missing_flag": parts[2] if len(parts) > 2 else None,
                    "data_flag": parts[3] if len(parts) > 3 else None,
                }
            )
    return rows


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


def fetch_met_monthly(node_id: str) -> None:
    zf = download_zip(MET_MONTHLY_ZIP)
    rows = parse_monthly(zf, ".metdata")
    table = pa.Table.from_pylist(rows, schema=MONTHLY_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_rlr_annual(node_id: str) -> None:
    zf = download_zip(RLR_ANNUAL_ZIP)
    rows = _parse_annual(zf, ".rlrdata")
    table = pa.Table.from_pylist(rows, schema=_ANNUAL_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_rlr_monthly(node_id: str) -> None:
    zf = download_zip(RLR_MONTHLY_ZIP)
    rows = parse_monthly(zf, ".rlrdata")
    table = pa.Table.from_pylist(rows, schema=MONTHLY_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_stations(node_id: str) -> None:
    zf = download_zip(MET_MONTHLY_ZIP)
    rows = _parse_filelist(zf)
    table = pa.Table.from_pylist(rows, schema=_STATIONS_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="psmsl-met-monthly", fn=fetch_met_monthly, kind="download"),
    NodeSpec(id="psmsl-rlr-annual", fn=fetch_rlr_annual, kind="download"),
    NodeSpec(id="psmsl-rlr-monthly", fn=fetch_rlr_monthly, kind="download"),
    NodeSpec(id="psmsl-stations", fn=fetch_stations, kind="download"),
]
