"""RBI foreign exchange reserves — dbie_foreignExchangeReserves.

India's official FX reserves (components FCA / Gold / SDR / Reserve-Tranche /
IMF), Weekly and Monthly, full history from 1990. Stateless full re-pull each
run (~1400 weekly rows per component — small and cheap).
"""

from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _call, _clean, _open_session

# FX reserves: components and frequencies to pull. Currency is USD (the only
# currency the endpoint serves for these component codes).
_FX_RESERVE_CODES = ["FCA", "GOLD", "SDR", "TR", "IMF"]
_FX_FREQUENCIES = ["Weekly", "Monthly"]
_FX_FROM = "1990-01-01 00:00:00"  # source min; we re-pull the full history each run

_FX_SCHEMA = pa.schema([
    ("reserve_code", pa.string()),
    ("reserve_name", pa.string()),
    ("frequency", pa.string()),
    ("currency_code", pa.string()),
    ("amount", pa.float64()),
    ("unit", pa.int64()),
    ("unit_description", pa.string()),
    ("timedate_ms", pa.int64()),
    ("fiscal_year", pa.string()),
])


def fetch_foreign_exchange_reserves(node_id: str) -> None:
    asset = node_id
    headers = _open_session()
    to_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d 00:00:00")
    rows = []
    for code in _FX_RESERVE_CODES:
        for freq in _FX_FREQUENCIES:
            body = {
                "currencyCode": "USD",
                "reserveCode": code,
                "fromDate": _FX_FROM,
                "toDate": to_date,
                "frequency": freq,
            }
            result = _call("dbie_foreignExchangeReserves", body, headers).get("resultList", [])
            for rec in result:
                ts = rec.get("timeDate")
                rows.append({
                    "reserve_code": _clean(rec.get("fxReservesCode")) or code,
                    "reserve_name": _clean(rec.get("fxReservesDescription")),
                    "frequency": freq,
                    "currency_code": _clean(rec.get("currencyCode")) or "USD",
                    "amount": float(rec["amount"]) if rec.get("amount") is not None else None,
                    "unit": int(rec["unit"]) if rec.get("unit") is not None else None,
                    "unit_description": _clean(rec.get("unitDescription")),
                    "timedate_ms": int(ts) if ts is not None else None,
                    "fiscal_year": _clean(rec.get("timeFisYear")),
                })
    if not rows:
        raise RuntimeError("dbie_foreignExchangeReserves returned no rows across all components")
    table = pa.Table.from_pylist(rows, schema=_FX_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="rbi-foreign-exchange-reserves", fn=fetch_foreign_exchange_reserves, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="rbi-foreign-exchange-reserves-transform",
        deps=["rbi-foreign-exchange-reserves"],
        sql='''
            SELECT
                epoch_ms(timedate_ms)::DATE AS date,
                frequency,
                reserve_code,
                reserve_name,
                currency_code,
                CAST(amount AS DOUBLE) AS amount,
                fiscal_year
            FROM "rbi-foreign-exchange-reserves"
            WHERE timedate_ms IS NOT NULL
              AND amount IS NOT NULL
        ''',
    ),
]
