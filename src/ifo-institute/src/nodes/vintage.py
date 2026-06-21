"""ifo Institute — vintage / real-time business-cycle dataset.

Vintage / real-time (8 sector files, each with Climate/Situation/Expectations
sheets): row 0 is ``Date`` + one column per data vintage (``v2018m04`` …); rows
are "January 2005" months. Melted to ``(date, sector, indicator, vintage,
value)`` and unioned across the 8 sectors into one table.

The vintage files have stable, unstamped paths under ``facts/vintage/``.
"""

import io
import time

import openpyxl
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, configure_http, save_raw_parquet
from utils import (
    FILES,
    HTTP_HEADERS,
    THROTTLE_S,
    get_xlsx,
    parse_month,
    sheet_rows,
    to_float,
)

# Vintage / real-time sector files: stable, unstamped paths.
_VINTAGE_SECTORS = [
    "Germany",
    "Industry_and_Trade",
    "Manufacturing",
    "Services",
    "Trade",
    "Wholesale_Trade",
    "Retail_Trade",
    "Construction",
]


def _parse_vintage(content: bytes, sector: str) -> list[tuple]:
    """Parse a vintage workbook → list of (date, sector, indicator, vintage, value)."""
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    out: list[tuple] = []
    try:
        for sn in wb.sheetnames:  # Climate / Situation / Expectations
            rows = sheet_rows(wb[sn])
            if not rows:
                continue
            header = rows[0]
            vintages = {
                c: str(header[c]).strip()
                for c in range(1, len(header))
                if header[c] is not None and str(header[c]).strip()
            }
            for r in rows[1:]:
                d = parse_month(r[0] if r else None)
                if d is None:
                    continue
                for c, vlabel in vintages.items():
                    val = to_float(r[c] if c < len(r) else None)
                    if val is None:
                        continue
                    out.append((d, sector, sn, vlabel, val))
    finally:
        wb.close()
    return out


_VINTAGE_SCHEMA = pa.schema(
    [
        ("date", pa.date32()),
        ("sector", pa.string()),
        ("indicator", pa.string()),
        ("vintage", pa.string()),
        ("value", pa.float64()),
    ]
)


def fetch_vintage(node_id: str) -> None:
    """Fetch + parse all 8 sector vintage files into one real-time dataset."""
    asset = node_id

    configure_http(headers=HTTP_HEADERS)

    records: list[tuple] = []
    for raw_sector in _VINTAGE_SECTORS:
        url = FILES + f"facts/vintage/{raw_sector}-ifo-vintage.xlsx"
        sector = raw_sector.replace("_", " ").strip()
        status, content = get_xlsx(url)
        if status != 200:
            raise RuntimeError(f"{asset}: vintage file missing (404) for {sector}: {url}")
        records.extend(_parse_vintage(content, sector))
        time.sleep(THROTTLE_S)

    if not records:
        raise RuntimeError(f"{asset}: parsed 0 rows from {len(_VINTAGE_SECTORS)} vintage files")

    table = pa.table(
        {
            "date": [r[0] for r in records],
            "sector": [r[1] for r in records],
            "indicator": [r[2] for r in records],
            "vintage": [r[3] for r in records],
            "value": [r[4] for r in records],
        },
        schema=_VINTAGE_SCHEMA,
    )
    save_raw_parquet(table, asset)


_VINTAGE_DEP = "ifo-institute-ifo-business-climate-vintage"

DOWNLOAD_SPECS = [
    NodeSpec(id=_VINTAGE_DEP, fn=fetch_vintage, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_VINTAGE_DEP}-transform",
        deps=[_VINTAGE_DEP],
        sql=f'''
            SELECT
                CAST(date AS DATE)    AS date,
                sector,
                indicator,
                vintage,
                CAST(value AS DOUBLE) AS value
            FROM "{_VINTAGE_DEP}"
            WHERE value IS NOT NULL
            ORDER BY sector, indicator, vintage, date
        ''',
    ),
]
