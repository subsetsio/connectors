"""RBI key policy rates — dbie_getPublicationDataImpala.

The headline policy rates (Repo, Reverse Repo, SDF, CRR, SLR, ...) as a current
snapshot. No history is available anonymously; each run overwrites with the
latest values.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _call, _clean, _open_session

_RATES_SCHEMA = pa.schema([
    ("name", pa.string()),
    ("rate", pa.float64()),
    ("currency_desc", pa.string()),
    ("time_month", pa.string()),
    ("timedate_ms", pa.int64()),
])


def fetch_key_policy_rates(node_id: str) -> None:
    asset = node_id
    headers = _open_session()
    result = _call("dbie_getPublicationDataImpala", {}, headers).get("result", [])
    rows = []
    for rec in result:
        ts = rec.get("timeDate")
        rows.append({
            "name": _clean(rec.get("name")),
            "rate": float(rec["rate"]) if rec.get("rate") is not None else None,
            "currency_desc": _clean(rec.get("currencyDesc")),
            "time_month": _clean(rec.get("timeMonth")),
            "timedate_ms": int(ts) if ts is not None else None,
        })
    if not rows:
        raise RuntimeError("dbie_getPublicationDataImpala returned no rows")
    table = pa.Table.from_pylist(rows, schema=_RATES_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="rbi-key-policy-rates", fn=fetch_key_policy_rates, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="rbi-key-policy-rates-transform",
        deps=["rbi-key-policy-rates"],
        sql='''
            -- Keep only the %-denominated monetary/policy rates; exclude the
            -- mixed-unit ticker rows (Exchange Rate in INR/USD, CPI Inflation)
            -- that share the homepage snapshot but are not policy rates.
            SELECT
                name AS rate_name,
                CAST(rate AS DOUBLE) AS rate_percent,
                CASE WHEN timedate_ms IS NOT NULL
                     THEN epoch_ms(timedate_ms)::DATE END AS as_of_date
            FROM "rbi-key-policy-rates"
            WHERE name IS NOT NULL
              AND name NOT ILIKE '%Exchange Rate%'
              AND name NOT ILIKE '%CPI%'
              AND name NOT ILIKE '%Inflation%'
        ''',
    ),
]
