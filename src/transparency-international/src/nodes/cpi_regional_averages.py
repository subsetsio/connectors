"""CPI regional averages — region-year average scores.

One published subset parsed from the "CPI 2025 Regional Averages" sheet of the
annual TI CPI workbook: each "Average of CPI score YYYY" column is followed by
its "N" count column.
"""

import re

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import build_reader, download_workbook, find_header, col_index, num, as_int


def _parse_regional(rows_of) -> list:
    rows = rows_of("CPI 2025 Regional Averages")
    h = find_header(rows, "Region")
    hdr = rows[h]
    ordered = sorted([c for c in hdr if hdr[c]], key=col_index)
    # "Average of CPI score YYYY" followed by its "N" count column.
    avg_year = {}
    n_for_year = {}
    for i, col in enumerate(ordered):
        m = re.match(r"Average of CPI score\s+(\d{4})", (hdr[col] or "").strip(),
                     re.IGNORECASE)
        if m:
            y = int(m.group(1))
            avg_year[col] = y
            if i + 1 < len(ordered):
                n_for_year[y] = ordered[i + 1]
    assert avg_year, "no 'Average of CPI score YYYY' columns; layout changed"

    out = []
    for r in rows[h + 1:]:
        region = (r.get("A") or "").strip()
        if not region or region.lower().startswith("note"):
            continue
        for col, y in avg_year.items():
            avg = num(r.get(col))
            if avg is None:
                continue
            out.append({
                "region": region,
                "year": y,
                "avg_cpi_score": avg,
                "n": as_int(r.get(n_for_year.get(y))),
            })
    return out


_REGIONAL_SCHEMA = pa.schema([
    ("region", pa.string()),
    ("year", pa.int32()),
    ("avg_cpi_score", pa.float64()),
    ("n", pa.int32()),
])


def fetch_regional(node_id: str) -> None:
    rows = _parse_regional(build_reader(download_workbook()))
    assert rows, "CPI regional averages parsed to 0 rows"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_REGIONAL_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="transparency-international-cpi-regional-averages", fn=fetch_regional, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="transparency-international-cpi-regional-averages-transform",
        deps=["transparency-international-cpi-regional-averages"],
        sql='''
            SELECT
                region,
                CAST(year AS INTEGER)          AS year,
                CAST(avg_cpi_score AS DOUBLE)  AS avg_cpi_score,
                CAST(n AS INTEGER)             AS n
            FROM "transparency-international-cpi-regional-averages"
            WHERE avg_cpi_score IS NOT NULL
        ''',
    ),
]
