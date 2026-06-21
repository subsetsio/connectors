"""Bank Negara Malaysia — month-iterated daily series.

Access pattern: one call per (year, month) over /<res>/year/{y}/month/{m},
returning a whole month of daily records per call. A single parametric fetch
body drives every resource in this family; they differ only in their per-record
normalizer (selected from a config map) and their published schema:
  - kl-usd-reference-rate, usd-interbank-intraday-rate, fx-turn-over : identity
  - kijang-emas                                                      : gold buy/sell pairs
  - islamic-interbank-rate, interbank-swap                           : tenor columns
Stateless full re-pull.
"""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import (
    PREFIX,
    _discover_start_year,
    _month_grid,
    _norm_tenor,
    _parallel,
)


def _norm_identity(rec: dict) -> dict:
    return dict(rec)


def _norm_kijang(rec: dict) -> dict:
    def pair(key):
        d = rec.get(key) or {}
        return d.get("buying"), d.get("selling")
    ob, os_ = pair("one_oz")
    hb, hs = pair("half_oz")
    qb, qs = pair("quarter_oz")
    return {
        "date": rec.get("effective_date"),
        "one_oz_buying": ob, "one_oz_selling": os_,
        "half_oz_buying": hb, "half_oz_selling": hs,
        "quarter_oz_buying": qb, "quarter_oz_selling": qs,
    }


# month-iterated resources -> their per-record normalizer
_MONTHLY_NORMALIZERS = {
    "kl-usd-reference-rate": _norm_identity,
    "usd-interbank-intraday-rate": _norm_identity,
    "fx-turn-over": _norm_identity,
    "kijang-emas": _norm_kijang,
    "islamic-interbank-rate": _norm_tenor,
    "interbank-swap": _norm_tenor,
}


def _collect_monthly(resource: str):
    start = _discover_start_year(lambda y: f"{resource}/year/{y}/month/6")
    norm = _MONTHLY_NORMALIZERS[resource]
    tasks = [((y, m), f"{resource}/year/{y}/month/{m}") for y, m in _month_grid(start)]
    rows = []
    for _key, payload in _parallel(tasks):
        if not payload:
            continue
        for rec in payload.get("data") or []:
            rows.append(norm(rec))
    return rows


def fetch_one(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_monthly(resource)
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{eid}", fn=fetch_one, kind="download")
    for eid in _MONTHLY_NORMALIZERS
]

_RESOURCE_SQL = {
    "kijang-emas": f'''
        SELECT CAST(date AS DATE)                   AS date,
               CAST(one_oz_buying AS DOUBLE)        AS one_oz_buying,
               CAST(one_oz_selling AS DOUBLE)       AS one_oz_selling,
               CAST(half_oz_buying AS DOUBLE)       AS half_oz_buying,
               CAST(half_oz_selling AS DOUBLE)      AS half_oz_selling,
               CAST(quarter_oz_buying AS DOUBLE)    AS quarter_oz_buying,
               CAST(quarter_oz_selling AS DOUBLE)   AS quarter_oz_selling
        FROM "{PREFIX}kijang-emas"
        WHERE date IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
    ''',
    # The Islamic interbank feed never reports the 1-year tenor (always null),
    # so year_1 is dropped rather than published as a dead column.
    "islamic-interbank-rate": f'''
        SELECT CAST(date AS DATE)        AS date,
               CAST(overnight AS DOUBLE) AS overnight,
               CAST(week_1 AS DOUBLE)    AS week_1,
               CAST(month_1 AS DOUBLE)   AS month_1,
               CAST(month_3 AS DOUBLE)   AS month_3,
               CAST(month_6 AS DOUBLE)   AS month_6
        FROM "{PREFIX}islamic-interbank-rate"
        WHERE date IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
    ''',
    "interbank-swap": f'''
        SELECT CAST(date AS DATE)          AS date,
               CAST(overnight AS DOUBLE)   AS overnight,
               CAST(week_1 AS DOUBLE)      AS week_1,
               CAST(week_2 AS DOUBLE)      AS week_2,
               CAST(month_1 AS DOUBLE)     AS month_1,
               CAST(month_2 AS DOUBLE)     AS month_2,
               CAST(month_3 AS DOUBLE)     AS month_3,
               CAST(month_6 AS DOUBLE)     AS month_6,
               CAST(month_9 AS DOUBLE)     AS month_9,
               CAST(month_12 AS DOUBLE)    AS month_12,
               CAST(more_1_year AS DOUBLE) AS more_1_year
        FROM "{PREFIX}interbank-swap"
        WHERE date IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
    ''',
    "fx-turn-over": f'''
        SELECT CAST(date AS DATE)        AS date,
               CAST(total_sum AS DOUBLE) AS total_sum
        FROM "{PREFIX}fx-turn-over"
        WHERE date IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
    ''',
    "usd-interbank-intraday-rate": f'''
        SELECT CAST(date AS DATE)           AS date,
               CAST(highest_rate AS DOUBLE) AS highest_rate,
               CAST(lowest_rate AS DOUBLE)  AS lowest_rate
        FROM "{PREFIX}usd-interbank-intraday-rate"
        WHERE date IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
    ''',
    "kl-usd-reference-rate": f'''
        SELECT CAST(date AS DATE)   AS date,
               CAST(rate AS DOUBLE) AS rate
        FROM "{PREFIX}kl-usd-reference-rate"
        WHERE date IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_RESOURCE_SQL[s.id[len(PREFIX):]],
    )
    for s in DOWNLOAD_SPECS
]
