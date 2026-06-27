"""National Bank of Rwanda (BNR) — daily exchange rates.

One subset: `exchange-rates`, a long-format daily reference-rate time series
(buying / average / selling, in RWF per unit of foreign currency) published by
the BNR at https://fxrates.bnr.rw/currency_history/.

Mechanism (fx_rest, from research): public unauthenticated JSON REST. One GET
per currency over a wide [start_date, end_date] window returns that currency's
full daily history in a single response — verified: USD returns ~3,500 rows
back to Jan-2012. There is no currency-list endpoint, so the supported ISO
codes are enumerated from `constants.CURRENCIES` (discovered by probing).

Fetch shape: stateless full re-pull (shape 1). The whole corpus is ~150k rows
across ~43 currencies and re-pulls in well under a minute, so there is no
watermark/cursor — every run re-fetches the full history and overwrites, which
also picks up the source's daily revisions for free.

Raw is saved as parquet with an all-string schema (faithful to the API's string
payload — rates arrive as decimal strings, sometimes with thousands commas;
dates as `DD-Mon-YY`). The SQL transform is the correctness gate: it strips
commas, casts to DOUBLE/DATE, and dedups to one row per (currency, date).
"""

from datetime import date

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry
from constants import CURRENCIES

_BASE = "https://fxrates.bnr.rw/currency_history/"
# Lower bound only — not an enumerated range. The API returns whatever history
# exists from this date forward (data begins ~2012); end is frozen at run start.
_START_DATE = "01/01/2000"

# Raw schema: keep the source's string payload verbatim; the transform casts.
_RAW_SCHEMA = pa.schema([
    ("currency_name", pa.string()),
    ("buying_rate", pa.string()),
    ("average_rate", pa.string()),
    ("selling_rate", pa.string()),
    ("post_date", pa.string()),
])


@transient_retry()  # 6 attempts, exp backoff; retries 429/5xx/transient network
def _fetch_currency(currency: str, end_date: str) -> list[dict]:
    resp = get(
        _BASE,
        params={"currency_name": currency, "start_date": _START_DATE, "end_date": end_date},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_exchange_rates(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    end_date = date.today().strftime("%d/%m/%Y")  # frozen for this run

    rows: list[dict] = []
    for currency in CURRENCIES:
        data = _fetch_currency(currency, end_date)
        for r in data:
            rows.append({
                "currency_name": r.get("currency_name") or currency,
                "buying_rate": _s(r.get("buying_rate")),
                "average_rate": _s(r.get("average_rate")),
                "selling_rate": _s(r.get("selling_rate")),
                "post_date": _s(r.get("post_date")),
            })

    if not rows:
        # The endpoint returns [] only for an unknown currency or a broken
        # response; an empty whole-corpus pull is a real failure, not a no-op.
        raise AssertionError(f"{asset}: fetched 0 rows across {len(CURRENCIES)} currencies")

    table = pa.Table.from_pylist(rows, schema=_RAW_SCHEMA)
    save_raw_parquet(table, asset)


def _s(v):
    return None if v is None else str(v)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="national-bank-of-rwanda-exchange-rates",
        fn=fetch_exchange_rates,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="national-bank-of-rwanda-exchange-rates-transform",
        deps=["national-bank-of-rwanda-exchange-rates"],
        sql='''
            WITH parsed AS (
                SELECT
                    currency_name                                              AS currency,
                    try_strptime(post_date, '%d-%b-%y')::DATE                   AS date,
                    TRY_CAST(REPLACE(buying_rate,  ',', '') AS DOUBLE)          AS buying_rate,
                    TRY_CAST(REPLACE(average_rate, ',', '') AS DOUBLE)         AS average_rate,
                    TRY_CAST(REPLACE(selling_rate, ',', '') AS DOUBLE)        AS selling_rate
                FROM "national-bank-of-rwanda-exchange-rates"
                WHERE post_date IS NOT NULL
            )
            -- Source carries a few corrupt records (a date string in a rate
            -- field, an unparseable post_date); TRY_* nulls them and we drop
            -- rows missing the essentials (valid date + positive average rate).
            SELECT currency, date, buying_rate, average_rate, selling_rate
            FROM (
                SELECT *,
                       row_number() OVER (PARTITION BY currency, date ORDER BY average_rate) AS rn
                FROM parsed
                WHERE date IS NOT NULL AND average_rate IS NOT NULL AND average_rate > 0
            )
            WHERE rn = 1
        ''',
    ),
]
