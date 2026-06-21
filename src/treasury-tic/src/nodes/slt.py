"""TIC SLT detailed cross-border long-term-securities tables (slt1..slt4).

These ship already in long form with a machine-readable snake_case header row
plus a TIC country_code; the fetch just skips the banner/footer and types the
values. One parametric fetch (`fetch_slt`) drives all four subsets from the
SLT_TABLES config; each transform is a thin DuckDB cast (YYYY-MM -> first-of-
month DATE, null drop).
"""
import csv as stdlib_csv
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import BASE_RC, _clean_country, _fetch_text, _val

# node_id -> resource-center SLT table filename (long-format detailed tables)
SLT_TABLES = {
    "treasury-tic-slt1-us-lt-securities-held-by-foreign-residents": "slt_table1",
    "treasury-tic-slt2-foreign-lt-securities-held-by-us-residents": "slt_table2",
    "treasury-tic-slt3-us-treasury-securities-held-by-foreign-residents": "slt_table3",
    "treasury-tic-slt4-us-purchases-sales-lt-securities-by-type": "slt_table4",
}


def _parse_slt(text: str):
    """Detailed SLT table: long format, snake_case machine header row, footer notes.

    Returns (columns, rows). First three columns are country/country_code/date
    (strings); the rest are numeric values (float or None).
    """
    lines = list(stdlib_csv.reader(io.StringIO(text), delimiter="\t"))
    hdr_idx = None
    for i, line in enumerate(lines):
        if line and line[0].strip() == "country":
            hdr_idx = i
            break
    if hdr_idx is None:
        raise ValueError("SLT machine-readable 'country' header row not found")
    cols = [c.strip() for c in lines[hdr_idx] if c.strip()]
    rows = []
    for line in lines[hdr_idx + 1:]:
        if not line or not line[0].strip():
            break  # footer / end of data block
        rec = {}
        for j, col in enumerate(cols):
            cell = line[j] if j < len(line) else ""
            rec[col] = cell.strip() if j < 3 else _val(cell)
        rec["country"] = _clean_country(rec["country"])
        rows.append(rec)
    return cols, rows


def fetch_slt(node_id: str) -> None:
    """Fetch one detailed SLT table and persist as long-format parquet."""
    asset = node_id
    fname = SLT_TABLES[node_id]
    text = _fetch_text(f"{BASE_RC}/{fname}.txt")
    cols, rows = _parse_slt(text)
    if not rows:
        raise ValueError(f"{asset}: parsed 0 rows from {fname}")
    schema = pa.schema(
        [(c, pa.string()) if j < 3 else (c, pa.float64()) for j, c in enumerate(cols)]
    )
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id="treasury-tic-slt1-us-lt-securities-held-by-foreign-residents", fn=fetch_slt, kind="download"),
    NodeSpec(id="treasury-tic-slt2-foreign-lt-securities-held-by-us-residents", fn=fetch_slt, kind="download"),
    NodeSpec(id="treasury-tic-slt3-us-treasury-securities-held-by-foreign-residents", fn=fetch_slt, kind="download"),
    NodeSpec(id="treasury-tic-slt4-us-purchases-sales-lt-securities-by-type", fn=fetch_slt, kind="download"),
]


# SLT detailed tables: keep all numeric value columns, just type the date.
# EXCLUDE drops the original string date/country/country_code so they aren't
# duplicated by the leading explicit projection.
def _slt_sql(download_id: str) -> str:
    return f'''
        SELECT
            country,
            country_code,
            CAST(date || '-01' AS DATE) AS date,
            * EXCLUDE (country, country_code, date)
        FROM "{download_id}"
        WHERE date IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{download_id}-transform",
        deps=[download_id],
        sql=_slt_sql(download_id),
    )
    for download_id in SLT_TABLES
]
