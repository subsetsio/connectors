"""Download nodes for the RBI DBIE connector."""

from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import NodeSpec, save_raw_parquet
from utils import _call, _clean, _open_session


_FX_RESERVE_CODES = ("FCA", "GOLD", "SDR", "TR", "IMF")
_FX_FREQUENCIES = ("Weekly", "Monthly")
_FX_FROM = "1990-01-01 00:00:00"

_FX_SCHEMA = pa.schema(
    [
        ("reserve_code", pa.string()),
        ("reserve_name", pa.string()),
        ("frequency", pa.string()),
        ("currency_code", pa.string()),
        ("amount", pa.float64()),
        ("unit", pa.int64()),
        ("unit_description", pa.string()),
        ("timedate_ms", pa.int64()),
        ("fiscal_year", pa.string()),
    ]
)

_RATES_SCHEMA = pa.schema(
    [
        ("name", pa.string()),
        ("rate", pa.float64()),
        ("currency_desc", pa.string()),
        ("time_month", pa.string()),
        ("timedate_ms", pa.int64()),
    ]
)


def fetch_foreign_exchange_reserves(node_id: str) -> None:
    headers = _open_session()
    to_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d 00:00:00")
    rows = []

    for code in _FX_RESERVE_CODES:
        for frequency in _FX_FREQUENCIES:
            result = _call(
                "dbie_foreignExchangeReserves",
                {
                    "currencyCode": "USD",
                    "reserveCode": code,
                    "fromDate": _FX_FROM,
                    "toDate": to_date,
                    "frequency": frequency,
                },
                headers,
            ).get("resultList", [])

            for rec in result:
                ts = rec.get("timeDate")
                rows.append(
                    {
                        "reserve_code": _clean(rec.get("fxReservesCode")) or code,
                        "reserve_name": _clean(rec.get("fxReservesDescription")),
                        "frequency": frequency,
                        "currency_code": _clean(rec.get("currencyCode")) or "USD",
                        "amount": float(rec["amount"]) if rec.get("amount") is not None else None,
                        "unit": int(rec["unit"]) if rec.get("unit") is not None else None,
                        "unit_description": _clean(rec.get("unitDescription")),
                        "timedate_ms": int(ts) if ts is not None else None,
                        "fiscal_year": _clean(rec.get("timeFisYear")),
                    }
                )

    if not rows:
        raise RuntimeError("dbie_foreignExchangeReserves returned no rows across all components")

    save_raw_parquet(pa.Table.from_pylist(rows, schema=_FX_SCHEMA), node_id)


def fetch_key_policy_rates(node_id: str) -> None:
    headers = _open_session()
    result = _call("dbie_getPublicationDataImpala", {}, headers).get("result", [])
    rows = []

    for rec in result:
        ts = rec.get("timeDate")
        rows.append(
            {
                "name": _clean(rec.get("name")),
                "rate": float(rec["rate"]) if rec.get("rate") is not None else None,
                "currency_desc": _clean(rec.get("currencyDesc")),
                "time_month": _clean(rec.get("timeMonth")),
                "timedate_ms": int(ts) if ts is not None else None,
            }
        )

    if not rows:
        raise RuntimeError("dbie_getPublicationDataImpala returned no rows")

    save_raw_parquet(pa.Table.from_pylist(rows, schema=_RATES_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="rbi-foreign-exchange-reserves",
        fn=fetch_foreign_exchange_reserves,
        kind="download",
    ),
    NodeSpec(
        id="rbi-key-policy-rates",
        fn=fetch_key_policy_rates,
        kind="download",
    ),
]
