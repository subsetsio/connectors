"""NBP currency reference table.

One row per currently quoted ISO 4217 code, with flags for the NBP exchange-rate
tables that publish it.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, save_raw_parquet
from utils import _get_json

_CURRENCY_SCHEMA = pa.schema([
    ("code", pa.string()),
    ("currency", pa.string()),
    ("in_table_a", pa.bool_()),
    ("in_table_b", pa.bool_()),
    ("in_table_c", pa.bool_()),
])


def fetch_currencies(node_id: str) -> None:
    """Current NBP currency reference membership across tables A, B, and C."""
    by_code: dict[str, dict] = {}
    for table in ("A", "B", "C"):
        payload = _get_json(f"exchangerates/tables/{table}/")
        for rate in payload[0]["rates"]:
            code = rate["code"]
            row = by_code.setdefault(
                code,
                {
                    "code": code,
                    "currency": rate.get("currency") or rate.get("country"),
                    "in_table_a": False,
                    "in_table_b": False,
                    "in_table_c": False,
                },
            )
            row[f"in_table_{table.lower()}"] = True

    rows = [by_code[code] for code in sorted(by_code)]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_CURRENCY_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="narodowy-bank-polski-currencies", fn=fetch_currencies, kind="download"),
]
