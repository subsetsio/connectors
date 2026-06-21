"""NBP exchange rates — table C buy/sell rates, long format.
-> (date, code, currency, bid, ask)
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _FX_START, _fetch_windows

_BIDASK_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("code", pa.string()),
    ("currency", pa.string()),
    ("bid", pa.float64()),
    ("ask", pa.float64()),
])


def fetch_bid_ask(node_id: str) -> None:
    """Table C (buy/sell rates), long format."""
    rows = []
    for day in _fetch_windows("exchangerates/tables/C/{start}/{end}/", _FX_START):
        eff = day["effectiveDate"]
        for r in day["rates"]:
            rows.append({
                "date": eff,
                "code": r["code"],
                "currency": r.get("currency") or r.get("country"),
                "bid": r["bid"],
                "ask": r["ask"],
            })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_BIDASK_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="narodowy-bank-polski-exchange-rates-bid-ask", fn=fetch_bid_ask, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="narodowy-bank-polski-exchange-rates-bid-ask-transform",
        deps=["narodowy-bank-polski-exchange-rates-bid-ask"],
        sql='''
            SELECT DISTINCT
                CAST(date AS DATE) AS date,
                code AS currency_code,
                currency AS currency_name,
                CAST(bid AS DOUBLE) AS bid,
                CAST(ask AS DOUBLE) AS ask
            FROM "narodowy-bank-polski-exchange-rates-bid-ask"
            WHERE bid IS NOT NULL AND ask IS NOT NULL
        ''',
    ),
]
