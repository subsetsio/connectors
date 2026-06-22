"""Bank Negara Malaysia (BNM) Open API connector — every subset.

REST at https://api.bnm.gov.my/public; every request carries the versioned
`Accept: application/vnd.BNM.API.v1+json` header (see utils). JSON payload sits
under a top-level `data` key. No auth, no documented rate limit. The corpus is
small (daily-cadence rate/price series, MB-scale), so every subset is a
**stateless full re-pull**: re-fetch the whole series each run and overwrite —
revisions and late corrections are picked up for free.

There is no single bulk endpoint; history is reached by iterating path params,
and the iteration shape differs by resource. The fetch functions group by that
shape (one top-level fn per family, dispatched on the resource recovered from
the node id):

  - fetch_snapshot      base-rate, renminbi-fx-forward-price
                        single latest-state call (/<res>), no history endpoint.
  - fetch_exchange_rate exchange-rate
                        per-currency month-grid fan-out; the live currency set
                        is read from the latest /exchange-rate snapshot.
  - fetch_interest      interest-rate, interest-volume
                        month-grid crossed with three `?product=` slices.
  - fetch_monthly       kl-usd-reference-rate, usd-interbank-intraday-rate,
                        fx-turn-over, kijang-emas, islamic-interbank-rate,
                        interbank-swap
                        one call per (year, month); a per-resource normalizer
                        shapes each record.
  - fetch_opr           opr
                        year-iterated policy decisions (/opr/year/{y}).

Shared transport (versioned Accept header, retrying JSON fetch, bounded
thread-pool fan-out, start-year discovery, month grid, tenor normalizer) lives
in `src/utils.py`.
"""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import (
    PREFIX,
    _discover_start_year,
    _fetch,
    _has_rows,
    _month_grid,
    _norm_tenor,
    _now,
    _parallel,
)


# ============================================================ snapshot family
# base-rate: a list of per-bank rates, stamped with the snapshot effective_date.
# renminbi-fx-forward-price: one nested record flattened into selling_*/buying_*.

def _collect_snapshot(resource: str):
    payload = _fetch(resource)
    if not _has_rows(payload):
        raise RuntimeError(f"{resource}: empty snapshot")
    data = payload.get("data")
    meta = payload.get("meta") or {}
    rows = []
    if resource == "base-rate":
        eff = meta.get("effective_date")
        for rec in data:
            row = dict(rec)
            row["effective_date"] = eff
            rows.append(row)
    else:  # renminbi-fx-forward-price: single nested record
        rec = data
        row = {"date": rec.get("date")}
        for side in ("selling", "buying"):
            for k, v in (rec.get(side) or {}).items():
                row[f"{side}_{k}"] = v
        rows.append(row)
    return rows


def fetch_snapshot(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_snapshot(resource)
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


# ============================================================== exchange-rate
# Per-currency historical fan-out (/exchange-rate/{cur}/year/{y}/month/{m}). The
# current currency set is read from the latest snapshot, then each currency is
# pulled month by month back to its discovered start year. Heaviest BNM resource.

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


def fetch_exchange_rate(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_exchange_rate()
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


# ================================================ product-iterated interest feeds
# interest-rate, interest-volume: month-iterated with a `?product=` query param
# crossed over the three products. Both share this body (parametric on resource);
# their schemas differ only in that interest-volume carries an extra `other` tenor.

PRODUCTS = ["overall", "interbank", "money_market_operations"]


def _collect_by_product(resource: str):
    start = _discover_start_year(
        lambda y: f"{resource}/year/{y}/month/6?product=overall"
    )
    tasks = []
    for product in PRODUCTS:
        for y, m in _month_grid(start):
            tasks.append(((product, y, m),
                          f"{resource}/year/{y}/month/{m}?product={product}"))
    rows = []
    for (product, _y, _m), payload in _parallel(tasks):
        if not payload:
            continue
        for rec in payload.get("data") or []:
            row = _norm_tenor(rec)
            row["product"] = product
            rows.append(row)
    return rows


def fetch_interest(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_by_product(resource)
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


# ============================================================= month-iterated
# One call per (year, month) over /<res>/year/{y}/month/{m}, returning a whole
# month of daily records. A single parametric body drives every resource here;
# they differ only in their per-record normalizer (selected from a config map).

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


def fetch_monthly(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_monthly(resource)
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


# ======================================================================== opr
# Year-iterated (/opr/year/{y}); one call per year from the discovered start year
# through the current year. Each call returns that year's policy decisions.

def _collect_opr():
    start = _discover_start_year(lambda y: f"opr/year/{y}")
    cur_year, _ = _now()
    tasks = [(y, f"opr/year/{y}") for y in range(start, cur_year + 1)]
    rows = []
    for _y, payload in _parallel(tasks):
        if not payload:
            continue
        for rec in payload.get("data") or []:
            rows.append({
                "year": rec.get("year"),
                "date": rec.get("date"),
                "change_in_opr": rec.get("change_in_opr"),
                "new_opr_level": rec.get("new_opr_level"),
            })
    return rows


def fetch_opr(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_opr()
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


# =================================================================== download
DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}base-rate", fn=fetch_snapshot, kind="download"),
    NodeSpec(id=f"{PREFIX}renminbi-fx-forward-price", fn=fetch_snapshot, kind="download"),
    NodeSpec(id=f"{PREFIX}exchange-rate", fn=fetch_exchange_rate, kind="download"),
    NodeSpec(id=f"{PREFIX}interest-rate", fn=fetch_interest, kind="download"),
    NodeSpec(id=f"{PREFIX}interest-volume", fn=fetch_interest, kind="download"),
    NodeSpec(id=f"{PREFIX}kl-usd-reference-rate", fn=fetch_monthly, kind="download"),
    NodeSpec(id=f"{PREFIX}usd-interbank-intraday-rate", fn=fetch_monthly, kind="download"),
    NodeSpec(id=f"{PREFIX}fx-turn-over", fn=fetch_monthly, kind="download"),
    NodeSpec(id=f"{PREFIX}kijang-emas", fn=fetch_monthly, kind="download"),
    NodeSpec(id=f"{PREFIX}islamic-interbank-rate", fn=fetch_monthly, kind="download"),
    NodeSpec(id=f"{PREFIX}interbank-swap", fn=fetch_monthly, kind="download"),
    NodeSpec(id=f"{PREFIX}opr", fn=fetch_opr, kind="download"),
]


# ================================================================== transform
# One published Delta table per subset. Each is a thin parse-and-type pass with a
# QUALIFY dedup (the overlap/iteration safety net). The per-currency historical
# exchange feed never populates middle_rate, and the Islamic interbank feed never
# reports the 1-year tenor, so those dead columns are dropped rather than published.
_TRANSFORM_SQL = {
    "base-rate": f'''
        SELECT bank_code, bank_name,
               CAST(base_rate AS DOUBLE)                   AS base_rate,
               CAST(base_lending_rate AS DOUBLE)           AS base_lending_rate,
               CAST(indicative_eff_lending_rate AS DOUBLE) AS indicative_eff_lending_rate,
               CAST(effective_date AS DATE)                AS effective_date
        FROM "{PREFIX}base-rate"
        WHERE bank_code IS NOT NULL
    ''',
    "renminbi-fx-forward-price": f'''
        SELECT CAST(date AS DATE) AS date, * EXCLUDE (date)
        FROM "{PREFIX}renminbi-fx-forward-price"
        WHERE date IS NOT NULL
    ''',
    "exchange-rate": f'''
        SELECT currency_code,
               CAST(unit AS INTEGER)        AS unit,
               CAST(date AS DATE)           AS date,
               CAST(buying_rate AS DOUBLE)  AS buying_rate,
               CAST(selling_rate AS DOUBLE) AS selling_rate
        FROM "{PREFIX}exchange-rate"
        WHERE date IS NOT NULL AND currency_code IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY currency_code, date ORDER BY date) = 1
    ''',
    "interest-rate": f'''
        SELECT product,
               CAST(date AS DATE)        AS date,
               CAST(overnight AS DOUBLE) AS overnight,
               CAST(week_1 AS DOUBLE)    AS week_1,
               CAST(month_1 AS DOUBLE)   AS month_1,
               CAST(month_3 AS DOUBLE)   AS month_3,
               CAST(month_6 AS DOUBLE)   AS month_6,
               CAST(year_1 AS DOUBLE)    AS year_1
        FROM "{PREFIX}interest-rate"
        WHERE date IS NOT NULL AND product IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY product, date ORDER BY date) = 1
    ''',
    "interest-volume": f'''
        SELECT product,
               CAST(date AS DATE)        AS date,
               CAST(overnight AS DOUBLE) AS overnight,
               CAST(week_1 AS DOUBLE)    AS week_1,
               CAST(month_1 AS DOUBLE)   AS month_1,
               CAST(month_3 AS DOUBLE)   AS month_3,
               CAST(month_6 AS DOUBLE)   AS month_6,
               CAST(year_1 AS DOUBLE)    AS year_1,
               CAST(other AS DOUBLE)     AS other
        FROM "{PREFIX}interest-volume"
        WHERE date IS NOT NULL AND product IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY product, date ORDER BY date) = 1
    ''',
    "kl-usd-reference-rate": f'''
        SELECT CAST(date AS DATE)   AS date,
               CAST(rate AS DOUBLE) AS rate
        FROM "{PREFIX}kl-usd-reference-rate"
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
    "fx-turn-over": f'''
        SELECT CAST(date AS DATE)        AS date,
               CAST(total_sum AS DOUBLE) AS total_sum
        FROM "{PREFIX}fx-turn-over"
        WHERE date IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
    ''',
    "kijang-emas": f'''
        SELECT CAST(date AS DATE)                 AS date,
               CAST(one_oz_buying AS DOUBLE)      AS one_oz_buying,
               CAST(one_oz_selling AS DOUBLE)     AS one_oz_selling,
               CAST(half_oz_buying AS DOUBLE)     AS half_oz_buying,
               CAST(half_oz_selling AS DOUBLE)    AS half_oz_selling,
               CAST(quarter_oz_buying AS DOUBLE)  AS quarter_oz_buying,
               CAST(quarter_oz_selling AS DOUBLE) AS quarter_oz_selling
        FROM "{PREFIX}kijang-emas"
        WHERE date IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
    ''',
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
    "opr": f'''
        SELECT CAST(date AS DATE)            AS date,
               CAST(year AS INTEGER)         AS year,
               CAST(change_in_opr AS DOUBLE) AS change_in_opr,
               CAST(new_opr_level AS DOUBLE) AS new_opr_level
        FROM "{PREFIX}opr"
        WHERE date IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_TRANSFORM_SQL[s.id[len(PREFIX):]],
    )
    for s in DOWNLOAD_SPECS
]
