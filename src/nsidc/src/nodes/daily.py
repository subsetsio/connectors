"""NSIDC Sea Ice Index — daily sea ice extent (N_/S_ seaice_extent_daily CSVs).

Published subset: nsidc-sea-ice-extent-daily
"""

import csv
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import download_csv, parse_float

_DAILY_FILES = [
    ("north/daily/data/N_seaice_extent_daily_v4.0.csv", "Arctic"),
    ("south/daily/data/S_seaice_extent_daily_v4.0.csv", "Antarctic"),
]

_DAILY_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("hemisphere", pa.string()),
    ("extent_million_km2", pa.float64()),
    ("missing_million_km2", pa.float64()),
])


def _parse_daily(content: str, hemisphere: str) -> list[dict]:
    # csv.reader so the quoted 'Source Data' list column (commas inside) parses.
    rows = list(csv.reader(io.StringIO(content)))
    header = [h.strip() for h in rows[0]]
    i_year = header.index("Year")
    i_month = header.index("Month")
    i_day = header.index("Day")
    i_extent = header.index("Extent")
    i_missing = header.index("Missing")
    span = max(i_year, i_month, i_day, i_extent, i_missing)

    out = []
    # rows[0] = column names, rows[1] = units row — skip both.
    for r in rows[2:]:
        if len(r) <= span:
            continue
        year = r[i_year].strip()
        if not year.isdigit():
            continue
        month = r[i_month].strip().zfill(2)
        day = r[i_day].strip().zfill(2)
        out.append({
            "date": f"{year}-{month}-{day}",
            "hemisphere": hemisphere,
            "extent_million_km2": parse_float(r[i_extent]),
            "missing_million_km2": parse_float(r[i_missing]),
        })
    return out


def fetch_daily(node_id: str) -> None:
    asset = node_id
    records: list[dict] = []
    for path, hemisphere in _DAILY_FILES:
        records.extend(_parse_daily(download_csv(path), hemisphere))
    table = pa.Table.from_pylist(records, schema=_DAILY_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="nsidc-sea-ice-extent-daily", fn=fetch_daily, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nsidc-sea-ice-extent-daily-transform",
        deps=["nsidc-sea-ice-extent-daily"],
        sql='''
            SELECT DISTINCT
                CAST(date AS DATE)          AS date,
                hemisphere,
                extent_million_km2,
                missing_million_km2
            FROM "nsidc-sea-ice-extent-daily"
            ORDER BY hemisphere, date
        ''',
    ),
]
