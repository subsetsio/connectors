"""SIPRI military expenditure — long-format country x year x measure panel,
parsed from the milex .xlsx workbook. Stateless full re-pull (SIPRI revises
prior years on every annual release).
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import find_xlsx, isnum, load_wb

_MILEX_MEASURES = {
    "Constant (2024) US$": "constant_2024_usd_mn",
    "Current US$": "current_usd_mn",
    "Share of GDP": "share_of_gdp",
    "Per capita": "per_capita_current_usd",
    "Share of Govt. spending": "share_of_govt_spending",
}

_MILEX_SCHEMA = pa.schema([
    ("measure", pa.string()),
    ("country", pa.string()),
    ("year", pa.int32()),
    ("value", pa.float64()),
])


def fetch_military_expenditure(node_id: str) -> None:
    asset = node_id
    url = find_xlsx("/databases/milex", "Milex-data")
    wb = load_wb(url)
    out = []
    for sheet, measure in _MILEX_MEASURES.items():
        if sheet not in wb.sheetnames:
            raise RuntimeError(f"milex workbook missing expected sheet '{sheet}'")
        rows = list(wb[sheet].iter_rows(values_only=True))
        hdr = next(
            (i for i, r in enumerate(rows)
             if r and isinstance(r[0], str) and r[0].strip() == "Country"),
            None,
        )
        if hdr is None:
            raise RuntimeError(f"milex sheet '{sheet}': no 'Country' header row found")
        year_cols = {j: int(c) for j, c in enumerate(rows[hdr]) if isnum(c) and 1900 < int(c) < 2100}
        if not year_cols:
            raise RuntimeError(f"milex sheet '{sheet}': no year columns detected")
        for r in rows[hdr + 1:]:
            name = r[0]
            if not (isinstance(name, str) and name.strip()):
                continue  # blank separators / region headers carry no values anyway
            for j, yr in year_cols.items():
                v = r[j] if j < len(r) else None
                if isnum(v):
                    out.append({"measure": measure, "country": name.strip(), "year": yr, "value": float(v)})
    if not out:
        raise RuntimeError("military-expenditure parse produced 0 rows")
    save_raw_parquet(pa.Table.from_pylist(out, schema=_MILEX_SCHEMA), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="sipri-military-expenditure", fn=fetch_military_expenditure, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="sipri-military-expenditure-transform",
        deps=["sipri-military-expenditure"],
        sql='''
            SELECT
                country,
                CAST(year AS INTEGER) AS year,
                measure,
                CAST(value AS DOUBLE) AS value
            FROM "sipri-military-expenditure"
            WHERE value IS NOT NULL
        ''',
    ),
]
