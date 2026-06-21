"""Bank Negara Malaysia — exchange-rate subset.

Access pattern: per-currency historical fan-out
(/exchange-rate/{cur}/year/{y}/month/{m}). The current currency set is read
from the latest snapshot (/exchange-rate); each currency is then pulled month by
month back to its discovered start year. The heaviest BNM resource
(~27 currencies x ~19 years x 12 months). Stateless full re-pull.
"""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import (
    PREFIX,
    _discover_start_year,
    _fetch,
    _month_grid,
    _parallel,
)


def _collect_exchange_rate():
    snap = _fetch("exchange-rate")
    currencies = sorted({r["currency_code"] for r in (snap or {}).get("data", [])
                         if r.get("currency_code")})
    if not currencies:
        raise RuntimeError("exchange-rate: no currencies in latest snapshot")
    start = _discover_start_year(lambda y: f"exchange-rate/USD/year/{y}/month/6")
    tasks = []
    for cur in currencies:
        for y, m in _month_grid(start):
            tasks.append(((cur, y, m), f"exchange-rate/{cur}/year/{y}/month/{m}"))
    rows = []
    for (cur, _y, _m), payload in _parallel(tasks):
        if not payload:
            continue
        d = payload.get("data")
        if not d:
            continue
        unit = d.get("unit")
        code = d.get("currency_code", cur)
        rate = d.get("rate")
        if isinstance(rate, dict):
            rate = [rate]
        for rr in rate or []:
            rows.append({
                "currency_code": code,
                "unit": unit,
                "date": rr.get("date"),
                "buying_rate": rr.get("buying_rate"),
                "selling_rate": rr.get("selling_rate"),
                "middle_rate": rr.get("middle_rate"),
            })
    return rows


def fetch_one(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_exchange_rate()
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}exchange-rate", fn=fetch_one, kind="download"),
]

# The per-currency historical feed only populates buying/selling (and only for
# the 7 major currencies); middle_rate is always null there, so it is dropped
# rather than published as a dead column.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{PREFIX}exchange-rate-transform",
        deps=[f"{PREFIX}exchange-rate"],
        sql=f'''
            SELECT currency_code,
                   CAST(unit AS INTEGER)       AS unit,
                   CAST(date AS DATE)          AS date,
                   CAST(buying_rate AS DOUBLE) AS buying_rate,
                   CAST(selling_rate AS DOUBLE) AS selling_rate
            FROM "{PREFIX}exchange-rate"
            WHERE date IS NOT NULL AND currency_code IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY currency_code, date ORDER BY date) = 1
        ''',
    ),
]
