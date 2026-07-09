"""Maddison Project — country panel.

The 'Full data' sheet of mpd2023_web.xlsx: a long panel with one row per
(countrycode, year), already tidy. Copied through with light type coercion only.
"""

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import load_workbook, to_float, to_int

COUNTRY_SCHEMA = pa.schema([
    ("countrycode", pa.string()),
    ("country", pa.string()),
    ("region", pa.string()),
    ("year", pa.int64()),
    ("gdppc", pa.float64()),
    ("pop", pa.float64()),
])


def fetch_country_panel(node_id: str) -> None:
    """The 'Full data' sheet: one row per (countrycode, year). Already a tidy
    long panel — copied through, light type coercion only."""
    asset = node_id
    wb = load_workbook()
    ws = wb["Full data"]
    it = ws.iter_rows(values_only=True)
    header = [str(h).strip() if h is not None else "" for h in next(it)]
    expected = ["countrycode", "country", "region", "year", "gdppc", "pop"]
    assert header == expected, f"Full data header drift: {header!r}"

    rows = []
    for r in it:
        if r[0] is None:
            continue
        rows.append({
            "countrycode": r[0],
            "country": r[1],
            "region": r[2],
            "year": to_int(r[3]),
            "gdppc": to_float(r[4]),
            "pop": to_float(r[5]),
        })
    wb.close()
    assert rows, "Full data sheet produced no rows"
    table = pa.Table.from_pylist(rows, schema=COUNTRY_SCHEMA)
    save_raw_parquet(table, asset)
