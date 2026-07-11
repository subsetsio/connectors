"""Download nodes for the Narodowy Bank Polski Web API."""

from datetime import date

import pyarrow as pa

from subsets_utils import NodeSpec, save_raw_parquet
from utils import _FX_START, _fetch_windows, _get_json

_GOLD_START = date(2013, 1, 2)

_CURRENCY_SCHEMA = pa.schema([
    ("code", pa.string()),
    ("currency", pa.string()),
    ("in_table_a", pa.bool_()),
    ("in_table_b", pa.bool_()),
    ("in_table_c", pa.bool_()),
])

_MID_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("table", pa.string()),
    ("code", pa.string()),
    ("currency", pa.string()),
    ("mid", pa.float64()),
])

_BIDASK_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("code", pa.string()),
    ("currency", pa.string()),
    ("bid", pa.float64()),
    ("ask", pa.float64()),
])

_GOLD_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("price_pln_per_g", pa.float64()),
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


def fetch_mid(node_id: str) -> None:
    """Tables A + B mid reference rates, long format."""
    rows = []
    for table in ("A", "B"):
        for day in _fetch_windows(
            f"exchangerates/tables/{table}/{{start}}/{{end}}/", _FX_START
        ):
            eff = day["effectiveDate"]
            for rate in day["rates"]:
                rows.append({
                    "date": eff,
                    "table": table,
                    "code": rate["code"],
                    "currency": rate.get("currency") or rate.get("country"),
                    "mid": rate["mid"],
                })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_MID_SCHEMA), node_id)


def fetch_bid_ask(node_id: str) -> None:
    """Table C buy/sell rates, long format."""
    rows = []
    for day in _fetch_windows("exchangerates/tables/C/{start}/{end}/", _FX_START):
        eff = day["effectiveDate"]
        for rate in day["rates"]:
            rows.append({
                "date": eff,
                "code": rate["code"],
                "currency": rate.get("currency") or rate.get("country"),
                "bid": rate["bid"],
                "ask": rate["ask"],
            })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_BIDASK_SCHEMA), node_id)


def fetch_gold(node_id: str) -> None:
    """NBP accounting price of gold, long format."""
    rows = [
        {"date": item["data"], "price_pln_per_g": item["cena"]}
        for item in _fetch_windows("cenyzlota/{start}/{end}/", _GOLD_START)
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_GOLD_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="narodowy-bank-polski-currencies", fn=fetch_currencies, kind="download"),
    NodeSpec(id="narodowy-bank-polski-exchange-rates-mid", fn=fetch_mid, kind="download"),
    NodeSpec(id="narodowy-bank-polski-exchange-rates-bid-ask", fn=fetch_bid_ask, kind="download"),
    NodeSpec(id="narodowy-bank-polski-gold-prices", fn=fetch_gold, kind="download"),
]
