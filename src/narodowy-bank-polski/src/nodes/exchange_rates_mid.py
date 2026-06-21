"""NBP exchange rates — tables A (majors, daily) + B (exotics, weekly), mid
reference rate, long format. -> (date, table, code, currency, mid)
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _FX_START, _fetch_windows

_MID_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("table", pa.string()),
    ("code", pa.string()),
    ("currency", pa.string()),
    ("mid", pa.float64()),
])


def fetch_mid(node_id: str) -> None:
    """Tables A + B (mid reference rates), long format."""
    rows = []
    for table in ("A", "B"):
        for day in _fetch_windows(
            f"exchangerates/tables/{table}/{{start}}/{{end}}/", _FX_START
        ):
            eff = day["effectiveDate"]
            for r in day["rates"]:
                rows.append({
                    "date": eff,
                    "table": table,
                    "code": r["code"],
                    # Pre-~2013 responses name the field `country` (+`symbol`)
                    # instead of `currency`; fall back so history parses.
                    "currency": r.get("currency") or r.get("country"),
                    "mid": r["mid"],
                })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_MID_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="narodowy-bank-polski-exchange-rates-mid", fn=fetch_mid, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="narodowy-bank-polski-exchange-rates-mid-transform",
        deps=["narodowy-bank-polski-exchange-rates-mid"],
        sql='''
            SELECT DISTINCT
                CAST(date AS DATE) AS date,
                "table" AS rate_table,
                code AS currency_code,
                currency AS currency_name,
                CAST(mid AS DOUBLE) AS mid
            FROM "narodowy-bank-polski-exchange-rates-mid"
            WHERE mid IS NOT NULL
        ''',
    ),
]
