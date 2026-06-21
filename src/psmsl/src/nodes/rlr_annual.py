"""PSMSL Revised Local Reference annual mean sea level."""

import zipfile

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import RLR_ANNUAL_ZIP, data_members, download_zip, parse_value

_ANNUAL_SCHEMA = pa.schema(
    [
        ("station_id", pa.int32()),
        ("year", pa.int32()),
        ("msl_mm", pa.float64()),
        ("missing_flag", pa.string()),
        ("data_flag", pa.string()),
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


def fetch_rlr_annual(node_id: str) -> None:
    asset = node_id
    zf = download_zip(RLR_ANNUAL_ZIP)
    rows = _parse_annual(zf, ".rlrdata")
    table = pa.Table.from_pylist(rows, schema=_ANNUAL_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="psmsl-rlr-annual", fn=fetch_rlr_annual, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="psmsl-rlr-annual-transform",
        deps=["psmsl-rlr-annual"],
        sql="""
            SELECT
                station_id,
                year,
                make_date(year, 1, 1) AS date,
                msl_mm,
                missing_flag,
                data_flag
            FROM "psmsl-rlr-annual"
            WHERE msl_mm IS NOT NULL
        """,
    ),
]
