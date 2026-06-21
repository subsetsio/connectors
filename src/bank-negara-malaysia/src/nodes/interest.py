"""Bank Negara Malaysia — product-iterated interest feeds (interest-rate,
interest-volume).

Access pattern: month-iterated with a `?product=` query param crossed over the
three products (overall, interbank, money_market_operations):
/<res>/year/{y}/month/{m}?product=<p>. Both resources share the same fetch body
(parametric on resource); their published schemas differ only in that
interest-volume additionally carries an `other` tenor. Stateless full re-pull.
"""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import (
    PREFIX,
    _discover_start_year,
    _month_grid,
    _norm_tenor,
    _parallel,
)

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


def fetch_one(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_by_product(resource)
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}interest-rate", fn=fetch_one, kind="download"),
    NodeSpec(id=f"{PREFIX}interest-volume", fn=fetch_one, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{PREFIX}interest-rate-transform",
        deps=[f"{PREFIX}interest-rate"],
        sql=f'''
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
    ),
    SqlNodeSpec(
        id=f"{PREFIX}interest-volume-transform",
        deps=[f"{PREFIX}interest-volume"],
        sql=f'''
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
    ),
]
