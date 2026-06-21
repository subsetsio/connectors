"""NSIDC Sea Ice Index — monthly sea ice extent (N_/S_ {01..12}_extent CSVs).

Published subset: nsidc-sea-ice-extent-monthly
"""

import csv
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import download_csv, parse_float

_MONTHLY_FILES = (
    [(f"north/monthly/data/N_{m:02d}_extent_v4.0.csv", "Arctic") for m in range(1, 13)]
    + [(f"south/monthly/data/S_{m:02d}_extent_v4.0.csv", "Antarctic") for m in range(1, 13)]
)

_MONTHLY_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("hemisphere", pa.string()),
    ("source_dataset", pa.string()),
    ("extent_million_km2", pa.float64()),
    ("area_million_km2", pa.float64()),
])


def _parse_monthly(content: str, hemisphere: str) -> list[dict]:
    rows = list(csv.reader(io.StringIO(content)))
    header = [h.strip() for h in rows[0]]
    i_year = header.index("year")
    i_mo = header.index("mo")
    i_extent = header.index("extent")
    i_area = header.index("area")
    i_src = header.index("source_dataset") if "source_dataset" in header else None
    span = max(i_year, i_mo, i_extent, i_area)

    out = []
    for r in rows[1:]:
        if len(r) <= span:
            continue
        year = r[i_year].strip()
        if not year.isdigit():
            continue
        month = r[i_mo].strip().zfill(2)
        src = r[i_src].strip() if i_src is not None and len(r) > i_src else None
        out.append({
            "date": f"{year}-{month}-01",
            "hemisphere": hemisphere,
            "source_dataset": src or None,
            "extent_million_km2": parse_float(r[i_extent]),
            "area_million_km2": parse_float(r[i_area]),
        })
    return out


def fetch_monthly(node_id: str) -> None:
    asset = node_id
    records: list[dict] = []
    for path, hemisphere in _MONTHLY_FILES:
        records.extend(_parse_monthly(download_csv(path), hemisphere))
    table = pa.Table.from_pylist(records, schema=_MONTHLY_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="nsidc-sea-ice-extent-monthly", fn=fetch_monthly, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nsidc-sea-ice-extent-monthly-transform",
        deps=["nsidc-sea-ice-extent-monthly"],
        sql='''
            SELECT DISTINCT
                CAST(date AS DATE)              AS date,
                hemisphere,
                NULLIF(source_dataset, '-9999') AS source_dataset,
                extent_million_km2,
                area_million_km2
            FROM "nsidc-sea-ice-extent-monthly"
            -- Drop fully-missing months (e.g. the Dec 1987-Jan 1988 sensor gap):
            -- a monthly-extent table should carry only real observations.
            WHERE extent_million_km2 IS NOT NULL
               OR area_million_km2 IS NOT NULL
            ORDER BY hemisphere, date
        ''',
    ),
]
